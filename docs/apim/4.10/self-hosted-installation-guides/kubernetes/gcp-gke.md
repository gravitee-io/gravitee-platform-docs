<polished_content>
# GCP GKE

## Overview

This guide explains how to deploy a complete self-hosted Gravitee APIM platform on Google Kubernetes Engine (GKE) using Helm charts.

## Prerequisites

Before you install Gravitee APIM, complete the following steps:

* Install `gcloud` CLI and configure it with your credentials
* Install `kubectl`
* Install `helm`
* Have a valid GCP account with billing enabled
* Have appropriate GCP project permissions (Kubernetes Engine Admin, Service Account Admin, Compute Admin)
* (Optional) License key for Enterprise features
* (Optional) Register a domain name in Cloud DNS or have access to DNS management

## Components overview

This self-hosted APIM deployment includes several components that work together to provide a complete API management platform:

* **Management API**: Handles API configuration, policies, and administrative operations
* **Gateway**: Processes API requests, applies policies, and routes traffic to backend services
* **Management Console UI**: Web interface for API administrators to configure and monitor APIs
* **Developer Portal UI**: Self-service portal for developers to discover and consume APIs

## Configure GCP infrastructure components

To prepare your GKE cluster for Gravitee APIM deployment, configure the following GCP infrastructure components.

### Create GKE cluster

Create a GKE cluster with the following command:

```bash
# Replace these values:
# <cluster-name>: Your desired cluster name (e.g., "gravitee-cluster")
# <region>: Your GCP region (e.g., "us-central1", "europe-west1")
# <project-id>: Your GCP project ID

gcloud container clusters create <cluster-name> \
  --region <region> \
  --project <project-id> \
  --num-nodes 3 \
  --machine-type n1-standard-4 \
  --disk-size 100 \
  --disk-type pd-standard \
  --enable-autoscaling \
  --min-nodes 3 \
  --max-nodes 10 \
  --enable-autorepair \
  --enable-autoupgrade \
  --addons HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver \
  --workload-pool=<project-id>.svc.id.goog
```

### Configure kubectl

Configure `kubectl` to use your new cluster:

```bash
gcloud container clusters get-credentials <cluster-name> \
  --region <region> \
  --project <project-id>
```

### Verify cluster access

Verify cluster access:

```bash
kubectl cluster-info
kubectl get nodes
```

The output should show your cluster information and nodes in Ready status:

```
NAME                                           STATUS   ROLES    AGE   VERSION
gke-gravitee-cluster-default-pool-xxxxx-xxxx   Ready    <none>   2m    v1.27.x-gke.x
gke-gravitee-cluster-default-pool-xxxxx-xxxx   Ready    <none>   2m    v1.27.x-gke.x
gke-gravitee-cluster-default-pool-xxxxx-xxxx   Ready    <none>   2m    v1.27.x-gke.x
```

## Create default storage class

GKE comes with a default storage class, but you can customize it for better performance.

Create a file named `storageclass.yaml` with the following configuration:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: pd-ssd
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: pd.csi.storage.gke.io
parameters:
  type: pd-ssd
  replication-type: regional-pd
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```

Apply the storage class using the following command:

```bash
kubectl apply -f storageclass.yaml
```

### Verify storage class

To verify that your storage class was created successfully, use the following command:

```bash
kubectl get storageclass
```

The output should show the pd-ssd storage class as the default, indicated by (default) next to the name:

```
NAME                PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
pd-ssd (default)    pd.csi.storage.gke.io   Delete          WaitForFirstConsumer   true                   30s
standard            pd.csi.storage.gke.io   Delete          Immediate              true                   5m
```

## Configure GCP Ingress and Load Balancer

GKE automatically configures Google Cloud Load Balancer when you create Ingress resources. However, you need to ensure proper service account permissions.

### Create service account for Workload Identity

Create a GCP service account for your workloads:

```bash
# Replace these values:
# <project-id>: Your GCP project ID
# <service-account-name>: Name for the service account (e.g., "gravitee-sa")

gcloud iam service-accounts create <service-account-name> \
  --project=<project-id> \
  --description="Service account for Gravitee APIM" \
  --display-name="Gravitee APIM Service Account"
```

### Grant necessary permissions

```bash
# Grant Compute Viewer role
gcloud projects add-iam-policy-binding <project-id> \
  --member="serviceAccount:<service-account-name>@<project-id>.iam.gserviceaccount.com" \
  --role="roles/compute.viewer"

# Grant Storage Object Viewer role (if using GCS)
gcloud projects add-iam-policy-binding <project-id> \
  --member="serviceAccount:<service-account-name>@<project-id>.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"
```

### Enable Workload Identity binding

```bash
# Replace <namespace> with your Kubernetes namespace (e.g., "gravitee-apim")
# Replace <k8s-service-account> with your Kubernetes service account name (e.g., "gravitee-apim")

gcloud iam service-accounts add-iam-policy-binding \
  <service-account-name>@<project-id>.iam.gserviceaccount.com \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:<project-id>.svc.id.goog[<namespace>/<k8s-service-account>]"
```

## (Optional) Reserve static IP addresses

Reserve static IP addresses for your load balancers:

```bash
# Reserve global static IP for HTTPS load balancer
gcloud compute addresses create gravitee-apim-ip \
  --global \
  --project <project-id>

# Get the reserved IP address
gcloud compute addresses describe gravitee-apim-ip \
  --global \
  --project <project-id> \
  --format="get(address)"
```

Note the IP address for DNS configuration.

## (Optional) Create Google-managed SSL certificates

Create managed SSL certificates for your domains.

Create a file named `managed-certificate.yaml`:

```yaml
apiVersion: networking.gke.io/v1
kind: ManagedCertificate
metadata:
  name: gravitee-cert
  namespace: gravitee-apim
spec:
  domains:
    - api.yourdomain.com
    - gateway.yourdomain.com
    - console.yourdomain.com
    - portal.yourdomain.com
```

Apply the certificate configuration:

```bash
kubectl apply -f managed-certificate.yaml
```

{% hint style="info" %}
DNS records must be configured and pointing to your load balancer IP before the certificate can be provisioned. This process can take 15-60 minutes.
{% endhint %}

## Install Gravitee APIM

To install Gravitee APIM, complete the following steps.

### Create namespace

Kubernetes namespaces provide logical isolation and organization within a cluster. Creating a dedicated namespace for Gravitee APIM:

* **Isolates resources**: Separates APIM components from other applications
* **Simplifies management**: Groups related services, pods, and configurations together

Create the namespace using the following command:

```bash
kubectl create namespace gravitee-apim
```

### Create Kubernetes service account

Create a Kubernetes service account that will use Workload Identity:

```bash
kubectl create serviceaccount gravitee-apim \
  --namespace gravitee-apim
```

Annotate the service account with the GCP service account:

```bash
kubectl annotate serviceaccount gravitee-apim \
  --namespace gravitee-apim \
  iam.gke.io/gcp-service-account=<service-account-name>@<project-id>.iam.gserviceaccount.com
```

### Install MongoDB

To support API definitions and configuration, you must install MongoDB into your Kubernetes cluster. For more information about installing MongoDB, see the [official chart documentation](https://artifacthub.io/packages/helm/bitnami/mongodb).

Install MongoDB with Helm using the following command:

```bash
helm install gravitee-mongodb oci://registry-1.docker.io/bitnamicharts/mongodb \
  -n gravitee-apim \
  --set auth.enabled=false \
  --set persistence.enabled=true \
  --set persistence.storageClass=pd-ssd \
  --set persistence.size=10Gi \
  --set resources.requests.memory=512Mi \
  --set resources.requests.cpu=250m
```

#### Verify MongoDB deployment

To verify that your MongoDB deployment succeeded, check pod status using the following command:

```bash
kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-mongodb
```

The command generates the following output:

```
NAME                  READY   STATUS    RESTARTS   AGE
gravitee-mongodb-0    1/1     Running   0          2m
```

### Install Elasticsearch

To support analytics and logging, you must install Elasticsearch into your Kubernetes cluster. For more information on installing Elasticsearch, see the [official chart documentation](https://artifacthub.io/packages/helm/elastic/elasticsearch).

Install Elasticsearch with Helm using the following command:

```bash
helm repo add elastic https://helm.elastic.co

helm repo update

helm install elasticsearch elastic/elasticsearch \
  -n gravitee-apim \
  --set persistence.enabled=true \
  --set volumeClaimTemplate.storageClassName=pd-ssd \
  --set volumeClaimTemplate.resources.requests.storage=30Gi \
  --set replicas=1 \
  --set minimumMasterNodes=1
```

Follow the instructions that appear in your terminal, and retrieve the Elastic user's password:

```
NAME: elasticsearch
LAST DEPLOYED: Fri Oct 24 12:13:02 2025
NAMESPACE: gravitee-apim
STATUS: deployed
REVISION: 1
NOTES:
1. Watch all cluster members come up.
  $ kubectl get pods --namespace=gravitee-apim -l app=elasticsearch-master -w
2. Retrieve elastic user's password.
  $ kubectl get secrets --namespace=gravitee-apim elasticsearch-master-credentials -ojsonpath='{.data.password}' | base64 -d
3. Test cluster health using Helm test.
  $ helm --namespace=gravitee-apim test elasticsearch
```

#### Verify Elasticsearch deployment

To verify that your Elasticsearch deployment succeeded, check pod status using the following command:

```bash
kubectl get pods -n gravitee-apim -l app=elasticsearch-master
```

The command generates the following output:

```
NAME                     READY   STATUS    RESTARTS   AGE
elasticsearch-master-0   1/1     Running   0          55m
```

### (Optional) Install Redis

To support caching and rate-limiting, you must install Redis into your Kubernetes cluster. For more information about installing Redis, see the [official chart documentation](https://artifacthub.io/packages/helm/bitnami/redis).

Install Redis with Helm using the following command:

```bash
helm install gravitee-redis oci://registry-1.docker.io/bitnamicharts/redis \
  -n gravitee-apim \
  --set auth.enabled=true \
  --set auth.password=redis-password \
  --set master.persistence.storageClass=pd-ssd \
  --set master.persistence.size=8Gi
```

#### Verify Redis deployment

To verify that your Redis deployment succeeded, check pod status using the following command:

```bash
kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-redis
```

The command generates the following output:

```
NAME                      READY   STATUS    RESTARTS   AGE
gravitee-redis-master-0   1/1     Running   0          2m
```

### (Optional) Install PostgreSQL

To support management data, you can install PostgreSQL into your Kubernetes cluster. For more information on installing PostgreSQL, see the [official chart documentation](https://artifacthub.io/packages/helm/bitnami/postgresql).

Install PostgreSQL with Helm using the following command:

```bash
helm install gravitee-postgresql oci://registry-1.docker.io/bitnamicharts/postgresql \
  -n gravitee-apim \
  --set auth.database=gravitee \
  --set auth.username=gravitee \
  --set auth.password=changeme \
  --set primary.persistence.enabled=true \
  --set primary.persistence.storageClass=pd-ssd \
  --set primary.persistence.size=10Gi \
  --set primary.resources.requests.memory=512Mi \
  --set primary.resources.requests.cpu=250m
```

#### Verify PostgreSQL deployment

To verify that your PostgreSQL deployment succeeded, retrieve the password using the following command:

```bash
kubectl get secret --namespace gravitee-apim gravitee-postgresql -o jsonpath="{.data.password}" | base64 -d
```

Check pod status using the following command:

```bash
kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-postgresql
```

The command generates the following output:

```
NAME                    READY   STATUS    RESTARTS   AGE
gravitee-postgresql-0   1/1     Running   0          2m
```

### (Enterprise Edition only) Create secret

Before installing Gravitee APIM for Enterprise Edition, you need to create a Kubernetes secret for your license key.

Create the secret using the following command:

```bash
kubectl create secret generic gravitee-license \
  --from-file=license.key=./license.key \
  --namespace gravitee-apim
```

{% hint style="info" %}
* Ensure your license key file is named `license.key` and located in your current directory.
* The secret will be named `gravitee-license` and referenced in your Helm configuration.
* If you don't have a license key, you can still proceed with community features.
{% endhint %}

## Prepare the values.yaml for Helm

Create a `values.yaml` file in your working directory and copy the following Gravitee configuration into it. This is the base configuration for your self-hosted APIM platform:

```yaml
# MongoDB Configuration
mongo:
  uri: mongodb://gravitee-mongodb.gravitee-apim.svc.cluster.local:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000

# Elasticsearch Configuration
es:
  enabled: true
  endpoints:
    - https://elasticsearch-master:9200
  security:
    enabled: true
    username: elastic
    password: [ELASTIC PASSWORD FROM ES INSTALLATION]
  ssl:
    verifyHostname: false
    trustAll: true

# Repository types
management:
  type: mongodb

ratelimit:
  type: mongodb

analytics:
  type: elasticsearch

# Management API Configuration
api:
  enabled: true
  replicaCount: 1
  image:
    repository: graviteeio/apim-management-api
    tag: latest
    pullPolicy: Always

  env:
    # CORS Configuration
    - name: gravitee_http_cors_enabled
      value: "true"
    - name: gravitee_http_cors_allow-origin
      value: "*"
    - name: gravitee_http_cors_allow-headers
      value: "Authorization,Content-Type,X-Requested-With,Accept,Origin,Access-Control-Request-Method,Access-Control-Request-Headers,Cookie"
    - name: gravitee_http_cors_allow-methods
      value: "GET,POST,PUT,DELETE,OPTIONS,PATCH"
    - name: gravitee_http_cors_exposed-headers
      value: "X-Total-Count,Set-Cookie"
    - name: gravitee_http_cors_allow-credentials
      value: "true"

    # Cookie Configuration for HTTPS
    - name: gravitee_http_cookie_sameSite
      value: "None"
    - name: gravitee_http_cookie_secure
      value: "true"

    # Security exclusions for public endpoints
    - name: gravitee_management_security_providers_0_type
      value: "memory"
    - name: gravitee_management_security_exclude_0
      value: "/auth/**"
    - name: gravitee_management_security_exclude_1
      value: "/organizations/*/environments/*/configuration"
    - name: gravitee_management_security_exclude_2
      value: "/_health"
    - name: gravitee_management_security_exclude_3
      value: "/info"
    - name: gravitee_management_security_exclude_4
      value: "/portal/**"

    # Make portal public by default
    - name: gravitee_portal_authentication_forceLogin_enabled
      value: "false"

  service:
    type: ClusterIP
    externalPort: 83
    internalPort: 8083

  ingress:
    management:
      enabled: true
      ingressClassName: gce
      pathType: Prefix
      path: /management
      hosts:
        - api.yourdomain.com
      annotations:
        kubernetes.io/ingress.class: "gce"
        kubernetes.io/ingress.global-static-ip-name: "gravitee-apim-ip"
        networking.gke.io/managed-certificates: "gravitee-cert"
        kubernetes.io/ingress.allow-http: "true"
        ingress.gcp.kubernetes.io/pre-shared-cert: "gravitee-cert"

    portal:
      enabled: true
      ingressClassName: gce
      pathType: Prefix
      path: /portal
      hosts:
        - api.yourdomain.com
      annotations:
        kubernetes.io/ingress.class: "gce"
        kubernetes.io/ingress.global-static-ip-name: "gravitee-apim-ip"
        networking.gke.io/managed-certificates: "gravitee-cert"
        kubernetes.io/ingress.allow-http: "true"

  resources:
    requests:
      memory: "1Gi"
      cpu: "500m"
    limits:
      memory: "2Gi"
      cpu: "1"

  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 5
    targetAverageUtilization: 70
    targetMemoryAverageUtilization: 80

  # License volume configuration for Management API (uncomment for enterprise edition using license key)
  # extraVolumes: |
  #   - name: gravitee-license
  #     secret:
  #       secretName: gravitee-license
  # extraVolumeMounts: |
  #   - name: gravitee-license
  #     mountPath: "/opt/graviteeio-management-api/license/license.key"
  #     subPath: license.key
  #     readOnly: true

# Gateway Configuration
gateway:
  enabled: true
  replicaCount: 1
  image:
    repository: graviteeio/apim-gateway
    tag: latest
    pullPolicy: Always

  service:
    type: ClusterIP
    externalPort: 82
    internalPort: 8082

  ingress:
    enabled: true
    ingressClassName: gce
    pathType: Prefix
    path: /
    hosts:
      - gateway.yourdomain.com
    annotations:
      kubernetes.io/ingress.class: "gce"
      kubernetes.io/ingress.global-static-ip-name: "gravitee-apim-ip"
      networking.gke.io/managed-certificates: "gravitee-cert"
      kubernetes.io/ingress.allow-http: "true"

  resources:
    requests:
      memory: "1Gi"
      cpu: "500m"
    limits:
      memory: "2Gi"
      cpu: "1"

  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 10
    targetAverageUtilization: 70
    targetMemoryAverageUtilization: 80

# Management Console UI
ui:
  enabled: true
  replicaCount: 1
  image:
    repository: graviteeio/apim-management-ui
    tag: latest
    pullPolicy: Always

  env:
    - name: MGMT_API_URL
      value: "https://api.yourdomain.com/management/organizations/DEFAULT/environments/DEFAULT/"

  service:
    type: ClusterIP
    externalPort: 8002
    internalPort: 8080

  ingress:
    enabled: true
    ingressClassName: gce
    pathType: ImplementationSpecific
    path: /console(/.*)?
    hosts:
      - console.yourdomain.com
    annotations:
      kubernetes.io/ingress.class: "gce"
      kubernetes.io/ingress.global-static-ip-name: "gravitee-apim-ip"
      networking.gke.io/managed-certificates: "gravitee-cert"
      kubernetes.io/ingress.allow-http: "true"

  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "250m"

  autoscaling:
    enabled: true
    minReplicas: 1
    maxReplicas: 3
    targetAverageUtilization: 70
    targetMemoryAverageUtilization: 80

# Developer Portal UI
portal:
  enabled: true
  replicaCount: 1
  image:
    repository: graviteeio/apim-portal-ui
    tag: latest
    pullPolicy: Always

  env:
    - name: PORTAL_API_URL
      value: "https://api.yourdomain.com/portal/environments/DEFAULT"

  service:
    type: ClusterIP
    externalPort: 8003
    internalPort: 8080

  ingress:
    enabled: true
    ingressClassName: gce
    pathType: Prefix
    path: /
    hosts:
      - portal.yourdomain.com
    annotations:
      kubernetes.io/ingress.class: "gce"
      kubernetes.io/ingress.global-static-ip-name: "gravitee-apim-ip"
      networking.gke.io/managed-certificates: "gravitee-cert"
      kubernetes.io/ingress.allow-http: "true"

  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "250m"

  autoscaling:
    enabled: true
    minReplicas: 1
    maxReplicas: 3
    targetAverageUtilization: 70
    targetMemoryAverageUtilization: 80

# External dependencies
elasticsearch:
  enabled: false

mongodb:
  enabled: false

postgresql:
  enabled: false

redis:
  enabled: false

# Alert Engine
alerts:
  enabled: false

# Global configuration
apim:
  name: apim

# Main ingress disabled
ingress:
  enabled: false
```

### Configure values.yaml

1. Replace `[ELASTIC PASSWORD FROM ES INSTALLATION]` with your Elasticsearch password.
2. Replace all instances of `yourdomain.com` with your actual domain name.
3. Replace `gravitee-apim-ip` with the name of your reserved static IP (or remove these annotations if not using a reserved IP).
4. If your Kubernetes cluster does not support IPv6 networking, both the UI and Portal deployments must set the `IPV4_ONLY` environment variable to true.
5. (Enterprise Edition only) Navigate to the Management API section, and then uncomment the following configuration:

    ```yaml
    # License volume configuration for Management API (uncomment for enterprise edition)
    # extraVolumes: |
    #   - name: gravitee-license
    #     secret:
    #       secretName: gravitee-license
    # extraVolumeMounts: |
    #   - name: gravitee-license
    #     mountPath: "/opt/graviteeio-management-api/license/license.key"
    #     subPath: license.key
    #     readOnly: true
    ```

6. Save your Gravitee `values.yaml` file in your working directory.

## Install using Helm

To install your Gravitee APIM with Helm, complete the following steps:

1. Add the Gravitee Helm chart repository to your Kubernetes environment using the following command:

    ```bash
    helm repo add gravitee https://helm.gravitee.io
    ```

2. Update the Helm repository with the following command:

    ```bash
    helm repo update
    ```

3. Install the Helm chart with the Gravitee values.yaml file into the namespace using the following command:

    ```bash
    helm install gravitee-apim gravitee/apim \
      --namespace gravitee-apim \
      -f ./values.yaml \
      --wait \
      --timeout 10m
    ```

### Verify installation

Verify the installation was successful. The command output should be similar to the following:

```
NAME: gravitee-apim
LAST DEPLOYED: [DATE]
NAMESPACE: gravitee-apim
STATUS: deployed
REVISION: 1
```

### Uninstall

To uninstall Gravitee APIM, use the following command:

```bash
helm uninstall gravitee-apim --namespace gravitee-apim
```

## Configure DNS records

After the load balancer is provisioned, configure your DNS records in Cloud DNS (or your DNS provider):

1. Get your load balancer IP address:

    ```bash
    kubectl get ingress -n gravitee-apim
    ```

2. Create A records pointing to the load balancer IP:
    * `api.yourdomain.com` → Load Balancer IP
    * `gateway.yourdomain.com` → Load Balancer IP
    * `console.yourdomain.com` → Load Balancer IP
    * `portal.yourdomain.com` → Load Balancer IP

If using Cloud DNS:

```bash
# Create DNS zone (if not exists)
gcloud dns managed-zones create gravitee-zone \
  --dns-name="yourdomain.com." \
  --description="DNS zone for Gravitee APIM"

# Add A records
gcloud dns record-sets create api.yourdomain.com. \
  --zone=gravitee-zone \
  --type=A \
  --ttl=300 \
  --rrdatas=<LOAD_BALANCER_IP>

gcloud dns record-sets create gateway.yourdomain.com. \
  --zone=gravitee-zone \
  --type=A \
  --ttl=300 \
  --rrdatas=<LOAD_BALANCER_IP>

gcloud dns record-sets create console.yourdomain.com. \
  --zone=gravitee-zone \
  --type=A \
  --ttl=300 \
  --rrdatas=<LOAD_BALANCER_IP>

gcloud dns record-sets create portal.yourdomain.com. \
  --zone=gravitee-zone \
  --type=A \
  --ttl=300 \
  --rrdatas=<LOAD_BALANCER_IP>
```

## Verification

To verify that your Gravitee APIM platform is up and running on GKE, complete the following steps.

### Access Gravitee APIM web interface

Access the Gravitee APIM web interface using the following steps.

#### Management Console

Open your browser and navigate to: `https://console.yourdomain.com/console`

The interface allows you to configure APIs, policies, and monitor your API platform.

#### Developer Portal

Open your browser and navigate to: `https://portal.yourdomain.com/`

The self-service portal allows developers to discover and consume APIs.

### Validate the pods

A healthy deployment displays all pods with the Running status, 1/1 ready containers, and zero or minimal restart counts.

To validate the pods, complete the following steps:

1. Use the following command to query the pod status:

    ```bash
    kubectl get pods --namespace=gravitee-apim
    ```

2. Verify that the deployment was successful. The output should show all Gravitee components ready and running:

    ```
    NAME                                    READY   STATUS    RESTARTS   AGE
    gravitee-apim-api-xxx-xxx               1/1     Running   0          23m
    gravitee-apim-gateway-xxx-xxx           1/1     Running   0          23m
    gravitee-apim-portal-xxx-xxx            1/1     Running   0          23m
    gravitee-apim-ui-xxx-xxx                1/1     Running   0          23m
    elasticsearch-master-0                  1/1     Running   0          23m
    gravitee-mongodb-0                      1/1     Running   0          23m
    gravitee-postgresql-0                   1/1     Running   0          23m
    gravitee-redis-master-0                 1/1     Running   0          23m
    ```

### Validate the services

To verify service configuration, run the following command:

```bash
kubectl get services -n gravitee-apim
```

Verify that all services are properly configured. The output should show all required services:

```
NAME                              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)
gravitee-apim-api                 ClusterIP   10.x.x.x        <none>        83/TCP
gravitee-apim-gateway             ClusterIP   10.x.x.x        <none>        82/TCP
gravitee-apim-ui                  ClusterIP   10.x.x.x        <none>        8002/TCP
gravitee-apim-portal              ClusterIP   10.x.x.x        <none>        8003/TCP
gravitee-mongodb                  ClusterIP   10.x.x.x        <none>        27017/TCP
elasticsearch-master              ClusterIP   10.x.x.x        <none>        9200/TCP,9300/TCP
gravitee-postgresql               ClusterIP   10.x.x.x        <none>        5432/TCP
gravitee-redis-master             ClusterIP   10.x.x.x        <none>        6379/TCP
```

### Validate the Gateway logs

To validate the Gateway logs, complete the following steps:

1. List the Gateway pod using the following command:

    ```bash
    kubectl get pods -n gravitee-apim | grep gateway
    ```

2. Verify that the Gateway is running properly. The output should show the Gateway ready and running:

    ```
    gravitee-apim-gateway-xxxxxxxxxx  1/1     Running   0          23m
    ```

3. View the Gateway logs using the following command:

    ```bash
    kubectl logs -f gravitee-apim-gateway-xxxxxxxxxxxx -n gravitee-apim
    ```

### Validate Ingress

Verify ingress is working with the following command:

```bash
kubectl get ingress -n gravitee-apim
```

The output should show the hosts and load balancer addresses:

```
NAME                           CLASS   HOSTS                      ADDRESS          PORTS     AGE
gravitee-apim-api-management   gce     api.yourdomain.com         x.x.x.x          80, 443   1h
gravitee-apim-api-portal       gce     api.yourdomain.com         x.x.x.x          80, 443   1h
gravitee-apim-gateway          gce     gateway.yourdomain.com     x.x.x.x          80, 443   1h
gravitee-apim-portal           gce     portal.yourdomain.com      x.x.x.x          80, 443   1h
gravitee-apim-ui               gce     console.yourdomain.com     x.x.x.x          80, 443   1h
```

### Validate the Gateway URL

Validate your Gateway URL using the following steps.

#### Validate Gateway URL using Ingress

The Gateway URL is determined by the ingress configuration in your values.yaml file and Cloud DNS settings pointing to the load balancer endpoints.

To validate the Gateway URL, complete the following steps:

1. Get the load balancer IP from ingress: