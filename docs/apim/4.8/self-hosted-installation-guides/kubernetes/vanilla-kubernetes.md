---
description: An overview about vanilla kubernetes.
---

# Vanilla Kubernetes

## Overview

This guide explains a complete self-hosted Gravitee APIM platform on Kubernetes using Helm charts.

## Prerequisites

Before you install the Gravitee APIM, complete the following steps:

* Install [helm](https://helm.sh/docs/intro/install/).
* Install [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl).
* Ensure you have access to the self-hosted Kubernetes cluster where you want to install Gravitee APIM.
* Ensure the self-hosted target environment has outbound Internet connectivity to Gravitee Cloud using HTTPS/443.
* (optional) [License key](https://documentation.gravitee.io/platform-overview/gravitee-platform/gravitee-offerings-ce-vs-ee/enterprise-edition-licensing) for Enterprise features

{% hint style="warning" %}
This installation guide is for only development and quick start purposes. Do not use it for production environments. For more information about best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Components Overview

This self-hosted APIM deployment includes several components that work together to provide a complete API management platform:

* Management API: Handles API configuration, policies, and administrative operations
* Gateway: Processes API requests, applies policies, and routes traffic to backend services
* Management Console UI: Web interface for API administrators to configure and monitor APIs
* Developer Portal UI: Self-service portal for developers to discover and consume APIs

The Gravitee APIM platform requires several external dependencies and services to provide complete functionality:

**Required:**

* MongoDB: Stores API definitions, configurations, and rate limiting data
* Elasticsearch: Provides analytics, logging, and search capabilities for API metrics

**(Enhanced functionality) Optional:**

* Redis: Supports advanced caching and distributed rate limiting
* PostgreSQL: Alternative database for management data
* Ingress Controller: Routes external traffic to APIM services and enables web access

## Install the Gravitee APIM

To install the Gravitee APIM, complete the following steps:

1. [#create-namespace](vanilla-kubernetes.md#create-namespace "mention")
2. [#install-mongodb](vanilla-kubernetes.md#install-mongodb "mention")
3. [#install-elasticsearch](vanilla-kubernetes.md#install-elasticsearch "mention")
4. [#install-redis](vanilla-kubernetes.md#install-redis "mention")
5. [#install-postgresql](vanilla-kubernetes.md#install-postgresql "mention")
6. [#create-secret-enterprise-edition-only](vanilla-kubernetes.md#create-secret-enterprise-edition-only "mention")
7. [#install-ingress-controller](vanilla-kubernetes.md#install-ingress-controller "mention")
8. [#prepare-values.yaml-for-helm](vanilla-kubernetes.md#prepare-values.yaml-for-helm "mention")
9. [#install-with-helm](vanilla-kubernetes.md#install-with-helm "mention")

### Create Namespace

Kubernetes namespaces provide logical isolation and organization within a cluster. Creating a dedicated namespace for Gravitee APIM:

* Isolates resources: Separates APIM components from other applications
* Simplifies management: Groups related services, pods, and configurations together

Create the namespace using the following command:

```bash
kubectl create namespace gravitee-apim
```

{% hint style="danger" %}
This guide requires MongoDB and Elasticsearch to be installed for the complete APIM platform to function.
{% endhint %}

### Install MongoDB

To support API definitions and configuration, you must install MongoDB into your Kubernetes cluster. For more information about installing MongoDB, see the [official chart documentation](https://artifacthub.io/packages/helm/bitnami/mongodb)

1.  Install MongoDB with Helm using the following command:

    ```bash
    helm install gravitee-mongodb oci://registry-1.docker.io/bitnamicharts/mongodb \
      --version 14.12.3 \
      --namespace gravitee-apim \
      --set image.registry=docker.io \
      --set image.repository=mongo \
      --set image.tag=5.0 \
      --set auth.enabled=false \
      --set architecture=standalone \
      --set persistence.enabled=false \
      --set podSecurityContext.enabled=false \
      --set containerSecurityContext.enabled=false \
      --set volumePermissions.enabled=true \
      --set volumePermissions.image.repository=bitnamilegacy/os-shell \
      --set resources.requests.memory=512Mi \
      --set resources.requests.cpu=250m
    ```
2.  Extract the MongoDB hostname from the command output, and then save it for future use. The following sample output lists `gravitee-mongodb.gravitee-apim.svc.cluster.local` as the MongoDB hostname:

    ```bash
    NAME: gravitee-mongodb
    LAST DEPLOYED: DDD MMM DD HH:MM:SS YYYY
    NAMESPACE: gravitee-apim
    STATUS: deployed
    REVISION: 1
    TEST SUITE: None
    NOTES:
    CHART NAME: mongodb
    CHART VERSION: 14.12.3
    APP VERSION: 7.0.11
    ...
    ** Please be patient while the chart is being deployed **

       gravitee-mongodb.gravitee-apim.svc.cluster.local

    To connect to your database, create a MongoDB&reg; client container:

        kubectl run --namespace gravitee-apim gravitee-mongodb-client --rm --tty -i --restart='Never' --env="MONGODB_ROOT_PASSWORD=$MONGODB_ROOT_PASSWORD" --image docker.io/bitnamilegacy/mongodb:5.0 --command -- bash

    Then, run the following command:
        mongosh admin --host "gravitee-mongodb"

    ```

#### Verification

1.  To verify that your MongoDB deployment succeeded, check pod status using the following command:

    ```bash
    kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-mongodb
    ```

    \
    The command generates the following output:

    ```bash
    NAME                  READY   STATUS    RESTARTS   AGE
    gravitee-mongodb-0    1/1     Running   0          2m
    ```

### Install Elasticsearch

To support analytics and logging, you must install Elasticsearch into your Kubernetes cluster. For more information on installing Elasticsearch, see the [official chart documentation.](https://artifacthub.io/packages/helm/bitnami/elasticsearch)

1.  Install Elasticsearch with Helm using the following command:

    ```bash
    helm install gravitee-elasticsearch oci://registry-1.docker.io/bitnamicharts/elasticsearch \
      --version 19.13.14 \
      --namespace gravitee-apim \
      --set image.repository=bitnamilegacy/elasticsearch \
      --set security.enabled=false \
      --set master.replicaCount=1 \
      --set data.replicaCount=0 \
      --set coordinating.replicaCount=0 \
      --set ingest.replicaCount=0 \
      --set master.persistence.enabled=true \
      --set master.persistence.size=20Gi \
      --set master.resources.requests.memory=1536Mi \
      --set master.resources.requests.cpu=500m
    ```
2.  Extract the Elasticsearch hostname from the command output and save it for future use. The following sample output lists `http://gravitee-elasticsearch.gravitee-apim.svc.cluster.local:9200`as the Elasticsearch hostname:

    ```bash
    Pulled: registry-1.docker.io/bitnamicharts/elasticsearch:19.13.14
    Digest: sha256:68e9602a61d0fbe171f9bc2df3893ad792e0f27f13731d8627a8e23b2b336
    NAME: gravitee-elasticsearch
    LAST DEPLOYED: DDD MMM DD HH:MM:SS YYYY
    NAMESPACE: gravitee-apim
    STATUS: deployed
    REVISION: 1
    TEST SUITE: None
    NOTES:
    CHART NAME: elasticsearch
    CHART VERSION: 19.13.14
    APP VERSION: 8.11.3

    -------------------------------------------------------------------------------

          https://www.elastic.co/guide/en/elasticsearch/reference/current/file-descriptors.html
          https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html

      To access from outside the cluster execute the following commands:

        kubectl port-forward --namespace gravitee-apim svc/gravitee-elasticsearch 9200:9200 &
        curl http://127.0.0.1:9200/
    ```

#### Verification

1.  To verify that your Elasticsearch deployment succeeded, check pod status using the following command:

    ```bash
    kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-elasticsearch
    ```

    \
    The command generates the following output:

    ```bash
    NAME                              READY   STATUS    RESTARTS   AGE
    gravitee-elasticsearch-master-0   1/1     Running   0          2m
    ```

### (Optional) Install Redis

To support caching and rate-limiting, you must install Redis into your Kubernetes cluster. For more information about installing Redis, see the [official chart documentation.](https://artifacthub.io/packages/helm/bitnami/redis)

1.  Install Redis with Helm using the following command:

    ```bash
    helm install gravitee-redis oci://registry-1.docker.io/bitnamicharts/redis \
      --version 18.6.1 \
      --namespace gravitee-apim \
      --set image.repository=bitnamilegacy/redis \
      --set architecture=standalone \
      --set auth.enabled=true \
      --set auth.password=redis-password \
      --set master.persistence.enabled=true \
      --set master.persistence.size=8Gi
    ```
2.  Extract the Redis hostname from the command output and save it for future use. The following sample output lists `gravitee-apim-redis-master.gravitee-apim.svc.cluster.local` as the Redis hostname:

    ```sh
    NAME: gravitee-redis
    LAST DEPLOYED:  DDD MMM DD HH:MM:SS YYYY
    NAMESPACE: gravitee-apim
    STATUS: deployed
    REVISION: 1
    TEST SUITE: None
    NOTES:
    CHART NAME: redis
    CHART VERSION: 18.6.1
    APP VERSION: 7.2.4
    ...
    ** Please be patient while the chart is being deployed **

    Redis(TM) can be accessed on the following DNS names from within your cluster:
        gravitee-redis-master.gravitee-apim.svc.cluster.local for read/write operations (port 6379)

    To get your password run:
        export REDIS_PASSWORD=$(kubectl get secret --namespace gravitee-apim gravitee-redis -o jsonpath="{.data.redis-password}" | base64 -d)
    ```

#### Verification

1.  To verify that your Redis deployment succeeded, check pod status using the following command:

    ```bash
    kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-redis
    ```

    \
    The command generates the following output:

    ```bash
    NAME                      READY   STATUS    RESTARTS   AGE
    gravitee-redis-master-0   1/1     Running   0          2m
    ```

### (Optional) Install PostgreSQL

To support management data, you can install PostgreSQL into your Kubernetes cluster. For more information on installing PostgreSQL, see the [official chart documentation.](https://artifacthub.io/packages/helm/bitnami/postgresql)

1.  Install PostgreSQL with Helm using the following command:

    ```bash
    helm install gravitee-postgresql oci://registry-1.docker.io/bitnamicharts/postgresql \
      --version 13.2.24 \
      --namespace gravitee-apim \
      --set image.repository=bitnamilegacy/postgresql \
      --set auth.database=gravitee \
      --set auth.username=gravitee \
      --set auth.password=changeme \
      --set persistence.enabled=true \
      --set persistence.size=8Gi \
      --set resources.requests.memory=512Mi \
      --set resources.requests.cpu=250m
    ```
2.  Extract the PostgreSQL hostname from the command output and save it for future use. The following sample output lists `gravitee-postgresql.gravitee-apim.svc.cluster.local` as the PostgreSQL hostname:

    ```bash
    NAME: gravitee-postgresql
    LAST DEPLOYED: DDD MMM DD HH:MM:SS YYYY
    NAMESPACE: gravitee-apim
    STATUS: deployed
    REVISION: 1
    TEST SUITE: None
    NOTES:
    CHART NAME: postgresql
    CHART VERSION: 13.2.24
    APP VERSION: 16.3.0
    ...
    ** Please be patient while the chart is being deployed **

    To get the password for "gravitee" run:
        export POSTGRES_PASSWORD=$(kubectl get secret --namespace gravitee-apim gravitee-postgresql -o jsonpath="{.data.postgres-password}" | base64 -d)
    ```

#### Verification

1.  To verify that your PostgreSQL deployment succeeded, retrieve the password using the following command:

    ```bash
    kubectl get secret --namespace gravitee-apim gravitee-postgresql -o jsonpath="{.data.postgres-password}" | base64 -d
    ```
2.  Check pod status using the following command:

    ```bash
    kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-postgresql
    ```

    \
    The command generates the following output:

    ```bash
    NAME                    READY   STATUS    RESTARTS   AGE
    gravitee-postgresql-0   1/1     Running   0          2m
    ```

### (Enterprise Edition Only) Create Secret

Before installing Gravitee APIM for [enterprise edition](../../readme/enterprise-edition.md), you need to create a Kubernetes secret for your license key.

1.  Create the secret using the following command:

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

### Install Ingress Controller

An ingress controller is required to route external traffic to your Gravitee APIM services. Choose the installation method based on your Kubernetes environment:

#### Install NGINX Ingress Controller with Helm

1.  Add the `ingress-nginx` Helm repository using the following command:

    ```bash
    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

    helm repo update
    ```
2.  Install the NGINX Ingress Controller using the following command:

    ```bash
    helm install nginx-ingress ingress-nginx/ingress-nginx \
      --namespace ingress-nginx \
      --create-namespace \
      --set controller.service.type=LoadBalancer \
      --set controller.admissionWebhooks.enabled=false
    ```

#### Configure DNS Resolution

For local development with custom hostnames, you must add DNS entries to your system's hosts file.

1.  In this guide, we are using DNS entries we defined in our [values.yaml](vanilla-kubernetes.md#prepare-the-values.yaml-for-helm) file, add the required DNS entries using the following commands:

    ```bash
    echo "127.0.0.1 apim.localhost" | sudo tee -a /etc/hosts
    echo "127.0.0.1 api.localhost" | sudo tee -a /etc/hosts  
    echo "127.0.0.1 dev.localhost" | sudo tee -a /etc/hosts
    ```

#### Verification

1.  Verify the DNS entries were added using the following command:

    ```bash
    cat /etc/hosts | tail -5
    ```

    \
    \
    The output should show the three localhost entries:

    ```bash
    127.0.0.1 apim.localhost
    127.0.0.1 api.localhost
    127.0.0.1 dev.localhost
    ```

#### Install Ingress Controller for Minikube Environments

1.  Enable the built-in ingress addon using the following command:

    ```bash
    minikube addons enable ingress
    ```
2.  Verify the ingress controller is running using the following command:

    ```bash
    kubectl get pods -n ingress-nginx
    ```

    The output should show the ingress controller pod in Running status:

    ```bash
    NAME                                       READY   STATUS    RESTARTS   AGE
    ingress-nginx-controller-xxx-xxx           1/1     Running   0          2m
    ```
3.  (Minikube users only), enable the network tunnel using the following command:

    ```bash
    minikube tunnel
    ```

{% hint style="danger" %}
Keep the tunnel command running in a separate terminal window. The tunnel must remain active for ingress to function properly.
{% endhint %}

### Prepare the `values.yaml` for Helm

> Ensure you have completed the[ ingress controller setup, DNS configuration, and (for Minikube) tunnel configuration from the previous sections](vanilla-kubernetes.md#install-ingress-controller) before proceeding.

1.  Create a `values.yaml` file in your working directory and copy the following Gravitee configuration into it. This is the base configuration for your self-hosted APIM platform:

    ```yaml
    # MongoDB Configuration
    mongo:
      uri: mongodb://gravitee-mongodb.gravitee-apim.svc.cluster.local:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000

    # # Uncomment to use PostgreSQL Configuration
    # jdbc:
    #   url: jdbc:postgresql://gravitee-postgresql.gravitee-apim.svc.cluster.local:5432/gravitee
    #   username: gravitee
    #   password: changeme
    #   driver: https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.2/postgresql-42.7.2.jar
    #   liquibase: true
    #   schema: public
    #   pool:
    #     autoCommit: true
    #     connectionTimeout: 10000
    #     idleTimeout: 600000
    #     maxLifetime: 1800000
    #     minIdle: 10
    #     maxPoolSize: 10
    #     registerMbeans: true

    # # Uncomment to us Redis Configuration for caching and rate limiting
    # redis:
    #   download: false
    #   host: gravitee-redis-master.gravitee-apim.svc.cluster.local
    #   port: 6379
    #   password: redis-password
    #   ssl: false

    # Elasticsearch Configuration
    es:
      enabled: true
      endpoints:
        - http://gravitee-elasticsearch.gravitee-apim.svc.cluster.local:9200

    # Repository types - Using PostgreSQL for management, Redis for rate limiting
    management:
      type: mongodb

    ratelimit:
      type: mongodb

    # Management API Configuration
    api:
      enabled: true
      replicaCount: 1
      image:
        repository: graviteeio/apim-management-api
        tag: latest
        pullPolicy: Always

      env:
        # CORS Configuration - Enable CORS at API level
        - name: gravitee_http_cors_enabled
          value: "true"
        - name: gravitee_http_cors_allow-origin
          value: "*"
        - name: gravitee_http_cors_allow-headers
          value: "Authorization,Content-Type,X-Requested-With,Accept,Origin,Access-Control-Request-Method,Access-Control-Request-Headers"
        - name: gravitee_http_cors_allow-methods
          value: "GET,POST,PUT,DELETE,OPTIONS"
        - name: gravitee_http_cors_exposed-headers
          value: "X-Total-Count"

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

      service:
        type: ClusterIP
        externalPort: 83
        internalPort: 8083

      ingress:
        management:
          enabled: true
          ingressClassName: nginx
          scheme: http
          pathType: Prefix
          path: /management
          hosts:
            - apim.localhost
          annotations:
            nginx.ingress.kubernetes.io/enable-cors: "true"
            nginx.ingress.kubernetes.io/cors-allow-origin: "*"
            nginx.ingress.kubernetes.io/cors-allow-methods: "GET, POST, PUT, DELETE, OPTIONS"
            nginx.ingress.kubernetes.io/cors-allow-headers: "Authorization, Content-Type, X-Requested-With, Accept, Origin"
        portal:
          enabled: true
          ingressClassName: nginx
          scheme: http
          pathType: Prefix
          path: /portal
          hosts:
            - apim.localhost
          annotations:
            nginx.ingress.kubernetes.io/enable-cors: "true"
            nginx.ingress.kubernetes.io/cors-allow-origin: "*"
            nginx.ingress.kubernetes.io/cors-allow-methods: "GET, POST, PUT, DELETE, OPTIONS"
            nginx.ingress.kubernetes.io/cors-allow-headers: "Authorization, Content-Type, X-Requested-With, Accept, Origin"

      resources:
        requests:
          memory: "1Gi"
          cpu: "500m"
        limits:
          memory: "2Gi"
          cpu: "1"

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
        ingressClassName: nginx
        pathType: Prefix
        path: /
        hosts:
          - api.localhost

      resources:
        requests:
          memory: "1Gi"
          cpu: "500m"
        limits:
          memory: "2Gi"
          cpu: "1"

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
          value: "http://apim.localhost/management/organizations/DEFAULT/environments/DEFAULT/"

      service:
        type: ClusterIP
        externalPort: 8002
        internalPort: 8080

      ingress:
        enabled: true
        ingressClassName: nginx
        pathType: ImplementationSpecific
        path: /console(/.*)?
        hosts:
          - apim.localhost
        annotations:
          nginx.ingress.kubernetes.io/rewrite-target: /$1

      resources:
        requests:
          memory: "256Mi"
          cpu: "100m"
        limits:
          memory: "512Mi"
          cpu: "250m"

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
          value: "http://apim.localhost/portal/environments/DEFAULT"

      service:
        type: ClusterIP
        externalPort: 8003
        internalPort: 8080

      ingress:
        enabled: true
        ingressClassName: nginx
        pathType: Prefix
        path: /
        hosts:
          - dev.localhost

      resources:
        requests:
          memory: "256Mi"
          cpu: "100m"
        limits:
          memory: "512Mi"
          cpu: "250m"

    # External dependencies (disabled, using external ones)
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

    # Ingress configuration
    ingress:
      enabled: false

    # Alternative configurations (to switch database types):

    # Option 1: MongoDB for both management and rate limiting
    # management:
    #   type: mongodb
    # ratelimit:
    #   type: mongodb

    # Option 2: PostgreSQL for management, MongoDB for rate limiting
    # management:
    #   type: jdbc
    # ratelimit:
    #   type: mongodb

    # Option 3: MongoDB for management, Redis for rate limiting
    # management:
    #   type: mongodb
    # ratelimit:
    #   type: redis

    # Current configuration: PostgreSQL for management, Redis for rate limiting
    # Ensure you have PostgreSQL, Redis, and Elasticsearch services running in your cluster
    ```

> If your Kubernetes cluster does not support IPV6 networking, both the UI and Portal deployments must set the `IPV4_ONLY` environment variable to `true`.

2. Save your Gravitee `values.yaml` file in your working directory.

<details>

<summary>Explanations of key predefined <code>values.yaml</code> parameter settings</summary>

**Service Configuration**

The self-hosted setup uses `ClusterIP` services with ingress controllers for external access. This provides better production scalability compared to direct `LoadBalancer` services:

* **ClusterIP**: Internal cluster communication only
* **Ingress**: Routes external traffic through nginx ingress controller to internal services
* **Host-based routing**: Uses `apim.localhost`, `api.localhost`, and `dev.localhost` for different components

**Resource Allocation**

The configured resource limits ensure optimal performance while preventing resource exhaustion:

* **Management API/Gateway**: 1-2Gi memory, 500m-1 CPU (handles API processing and management operations)
* **UI Components**: 256-512Mi memory, 100-250m CPU (lightweight frontend serving)

**Ingress Strategy**

The ingress configuration enables external access with path-based and host-based routing:

* **CORS enabled**: Allows cross-origin requests for web UI functionality
* **Path rewriting**: Console UI uses regex path matching with URL rewriting
* **Multiple hosts**: Separates Gateway (`api.localhost`) from Management (`apim.localhost`) and Portal (`dev.localhost`)

</details>

### Install with Helm

To install your Gravitee APIM with Helm, complete the following steps:

1.  Add the Gravitee Helm chart repository to your Kubernetes environment using the following command:

    ```bash
    helm repo add gravitee https://helm.gravitee.io
    ```
2.  Update the Helm repository with the following command:

    ```bash
    helm repo update
    ```
3.  Install the Helm chart with the Gravitee `values.yaml` file into the namespace using the following command:

    ```bash
    helm install gravitee-apim gravitee/apim \
      --namespace gravitee-apim \
      -f ./values.yaml
    ```

#### Verification

Verify the installation was successful. The command output should be similar to the following:

```bash
NAME: gravitee-apim
LAST DEPLOYED: [DATE]
NAMESPACE: gravitee-apim
STATUS: deployed
REVISION: 1
```

To uninstall Gravitee APIM, use the following command:

```bash
helm uninstall gravitee-apim --namespace gravitee-apim
```

## Verification

To verify that your Gravitee APIM platform is up and running, complete the following steps:

1. [#access-gravitee-apim-web-interface](vanilla-kubernetes.md#access-gravitee-apim-web-interface "mention")
2. [#validate-the-pods](vanilla-kubernetes.md#validate-the-pods "mention")
3. [#validate-the-services](vanilla-kubernetes.md#validate-the-services "mention")
4. [#validate-the-gateway-logs](vanilla-kubernetes.md#validate-the-gateway-logs "mention")
5. [#validate-ingress](vanilla-kubernetes.md#validate-ingress "mention")
6. [#validate-the-gateway-url](vanilla-kubernetes.md#validate-the-gateway-url "mention")

### Access Gravitee APIM web interface

Access the Gravitee APIM web interface using the following steps:

#### Management Console

1. Open your browser and navigate to: `http://apim.localhost/console`
2. Login with: `admin / admin` as your username and password

The interface allows you to configure APIs, policies, and monitor your API platform

#### Developer Portal

1. Open your browser and navigate to: `http://dev.localhost/`

This self-service portal allows developers to discover and consume APIs

### Validate the pods

A healthy deployment displays all pods with the Running status, `1/1` ready containers, and zero or minimal restart counts.

To validate the pods, complete the following steps:

1.  Use the following command to query the pod status:

    ```bash
    kubectl get pods --namespace=gravitee-apim
    ```
2.  Verify that the deployment was successful. The output should show all Gravitee components ready and running:

    ```bash
    NAME                                    READY   STATUS    RESTARTS   AGE
    gravitee-apim-api-xxx                   1/1     Running   0          5m
    gravitee-apim-gateway-xxx               1/1     Running   0          5m  
    gravitee-apim-ui-xxx                    1/1     Running   0          5m
    gravitee-apim-portal-xxx                1/1     Running   0          5m
    gravitee-elasticsearch-master-0         1/1     Running   0          10m
    gravitee-mongodb-0                      1/1     Running   0          10m
    ```

### Validate the Services

1.  To verify service configuration, run the following command:

    ```bash
    kubectl get services -n gravitee-apim
    ```
2.  Verify that all services are properly configured. The output should show all required services:

    ```bash
    NAME                              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)
    gravitee-apim-api                 ClusterIP   10.x.x.x        <none>        83/TCP
    gravitee-apim-gateway             ClusterIP   10.x.x.x        <none>        82/TCP
    gravitee-apim-ui                  ClusterIP   10.x.x.x        <none>        8002/TCP
    gravitee-apim-portal              ClusterIP   10.x.x.x        <none>        8003/TCP
    gravitee-mongodb                  ClusterIP   10.x.x.x        <none>        27017/TCP
    gravitee-elasticsearch            ClusterIP   10.x.x.x        <none>        9200/TCP,9300/TCP
    gravitee-redis-master             ClusterIP   10.x.x.x        <none>        6379/TCP
    ```

### Validate the Gateway logs

To validate the Gateway logs, complete the following steps:

1.  List the Gateway pod using the following command:

    ```bash
    kubectl get pods -n gravitee-apim | grep gateway
    ```
2.  Verify that the Gateway is running properly. The output should show the Gateway ready and running:

    ```bash
    gravitee-apim-gateway-xxx-xxx        1/1     Running   0          5m
    ```

### Validate Ingress

1.  Verify ingress is working with the following command:

    ```bash
    kubectl get ingress -n gravitee-apim
    ```
2.  The output should show the hosts and address.

    ```bash
    NAME                           CLASS   HOSTS            ADDRESS     PORTS   AGE
    gravitee-apim-api-management   nginx   apim.localhost   localhost   80      27h
    gravitee-apim-api-portal       nginx   apim.localhost   localhost   80      27h
    gravitee-apim-gateway          nginx   api.localhost    localhost   80      27h
    gravitee-apim-portal           nginx   dev.localhost    localhost   80      27h
    gravitee-apim-ui               nginx   apim.localhost   localhost   80      27h
    ```

### Validate the Gateway URL

Validate your Gateway URL using the following steps:

1. [#validate-gateway-url-using-ingress](vanilla-kubernetes.md#validate-gateway-url-using-ingress "mention")
2. [#validate-gateway-url-using-port-forwarding](vanilla-kubernetes.md#validate-gateway-url-using-port-forwarding "mention")

The Gateway URL is determined by the ingress configuration in your `values.yaml` file. This setup uses localhost hostnames for local development.

#### Validate Gateway URL using Ingress

To validate the Gateway URL, complete the following steps:

1.  Verify the Gateway endpoint directly using the following command:

    ```bash
    curl http://api.localhost/
    ```
2.  Verify that the Gateway is responding correctly. The output should show the following message, which confirms that no API is deployed yet for this URL.

    ```bash
    No context-path matches the request URI.
    ```

#### Validate Gateway URL using Port Forwarding

1.  Set up port forwarding for the Gateway using the following command:

    ```bash
    kubectl port-forward svc/gravitee-apim-gateway 8082:82 -n gravitee-apim
    ```
2.  Verify the Gateway URL using the following command:

    ```bash
    curl http://localhost:8082/
    ```
3.  Verify that the Gateway is responding correctly. The output should show the following message, which confirms that no API is deployed yet for this URL.

    ```bash
    No context-path matches the request URI.
    ```

## Next steps

* Create your first API. For more information about creating your first API, see [create-and-publish-your-first-api](../../how-to-guides/create-and-publish-your-first-api/ "mention").
* Add native Kafka capabilities. For more information about adding native Kafka capabilities, see [configure-the-kafka-client-and-gateway.md](../../kafka-gateway/configure-the-kafka-client-and-gateway.md "mention").
