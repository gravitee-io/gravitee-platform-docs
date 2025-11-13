# Azure AKS

{% hint style="warning" %}
This installation guide is for only development and quick start purposes. Do not use it for production environments. For more information about best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Overview&#x20;

This guide explains how to deploy a complete self-hosted Gravitee APIM platform on Azure Kubernetes Service (AKS) using Helm charts.

## Prerequisites <a href="#prerequisites" id="prerequisites"></a>

Before you install the Gravitee APIM, complete the following steps:

* Install [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-macos?view=azure-cli-latest) and configure it with your credentials
* Install [helm](https://helm.sh/docs/intro/install/)
* Install [kubectl](https://kubernetes.io/docs/tasks/tools/)
* Have a valid [Azure subscription](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account)
* (Optional) [License key](https://documentation.gravitee.io/platform-overview/gravitee-platform/gravitee-offerings-ce-vs-ee/enterprise-edition-licensing) for Enterprise features
* (Optional) Register a domain name in Azure DNS or have access to DNS management

## Components Overview

This deployment includes the following components:

* Management API: Handles API configuration, policies, and administrative operations.
* Gateway: Processes API requests, applies policies, and routes traffic to backend services.
* Management Console UI: Web interface for API administrators to configure and monitor APIs.
* Developer Portal UI: Self-service portal for developers to discover and consume APIs.

## Install NGINX Ingress Controller

* Install the NGINX ingress controller with Azure Load Balancer support using the following commands:

```bash
# Create namespace for ingress
kubectl create namespace ingress-nginx

# Add the nginx ingress helm repository
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# Install NGINX Ingress with Azure Load Balancer annotations
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --set controller.service.type=LoadBalancer \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/azure-load-balancer-health-probe-request-path"=/healthz \
  --set controller.service.externalTrafficPolicy=Local \
  --set controller.admissionWebhooks.enabled=false
```

#### Verification&#x20;

Complete the following steps to verify the NGINX Ingress Controller installation:

*   Verify the service is running using the following command:\


    ```bash
    kubectl get service -n ingress-nginx ingress-nginx-controller
    ```

    \
    The output shows the Ingress Nginx controller with the Cluster IP, and External IP address:\


    ```bash
    NAME                       TYPE           CLUSTER-IP    EXTERNAL-IP     PORT(S)                      AGE
    ingress-nginx-controller   LoadBalancer   10.0.x.x      20.x.x.x       80:30080/TCP,443:30443/TCP   2m
    ```



*   Verify the NGINX ingress controller pods are running using the following command:\


    ```bash
    kubectl get pods -n ingress-nginx
    ```

    \
    The output shows the Ingress Nginx controller pod in running status:\


    ```bash
    NAME                                        READY   STATUS    RESTARTS   AGE
    ingress-nginx-controller-xxxxx-xxxxx       1/1     Running   0          2m
    ```

## Install the Gravitee APIM <a href="#install-the-gravitee-apim" id="install-the-gravitee-apim"></a>

To install the Gravitee APIM, complete the following steps:

1. [#create-namespace](azure-aks.md#create-namespace "mention")
2. [#install-mongodb](azure-aks.md#install-mongodb "mention")
3. [#install-elasticsearch](azure-aks.md#install-elasticsearch "mention")
4. [#optional-install-redis](azure-aks.md#optional-install-redis "mention")
5. [#optional-install-postgresql](azure-aks.md#optional-install-postgresql "mention")
6. [#enterprise-edition-only-create-secret](azure-aks.md#enterprise-edition-only-create-secret "mention")
7. [#prepare-the-values.yamlfor-helm](azure-aks.md#prepare-the-values.yamlfor-helm "mention")
8. [#install-using-helm](azure-aks.md#install-using-helm "mention")

### Create Namespace&#x20;

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

1.  Install MongoDB with Helm using the following command:\


    ```bash
    helm install gravitee-mongodb oci://registry-1.docker.io/cloudpirates/mongodb \
      -n gravitee-apim \
      --set auth.enabled=false \
      --set persistence.enabled=false \
      --set resources.requests.memory=512Mi \
      --set resources.requests.cpu=250m
    ```

#### Verification&#x20;

*   To verify that your MongoDB deployment succeeded, check pod status using the following command:\


    ```bash
    kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-mongodb
    ```

    \
    \
    The command generates the following output:\


    ```bash
    NAME                  READY   STATUS    RESTARTS   AGE
    gravitee-mongodb-0    1/1     Running   0          2m
    ```

### Install Elasticsearch&#x20;

To support analytics and logging, you must install Elasticsearch into your Kubernetes cluster. For more information on installing Elasticsearch, see the [official chart documentation.](https://artifacthub.io/packages/helm/bitnami/elasticsearch)&#x20;

1.  Install Elasticsearch with Helm using the following command:\


    ```bash
    helm repo add elastic https://helm.elastic.co

    helm repo update

    helm -n gravitee-apim install elasticsearch elastic/elasticsearch \
      --set persistence.enabled=false \
      --set replicas=1 \
      --set minimumMasterNodes=1
    ```
2.  Follow the instructions that appear in your terminal, and retrieve the Elastic user's password.

    ```bash
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

#### Verification

*   To verify that your Elasticsearch deployment succeeded, check pod status using the following command:\


    ```bash
    kubectl get pods --namespace=gravitee-apim -l app=elasticsearch-master -w 
    ```

    \
    \
    The command generates the following output:\


    ```bash
    NAME                     READY   STATUS    RESTARTS   AGE
    elasticsearch-master-0   1/1     Running   0          55m
    ```

### (Optional) Install Redis

To support caching and rate-limiting, you must install Redis into your Kubernetes cluster. For more information about installing Redis, see the [official chart documentation. ](https://artifacthub.io/packages/helm/bitnami/redis)

1.  Install Redis with Helm using the following command: &#x20;

    ```bash
    helm install gravitee-redis oci://registry-1.docker.io/cloudpirates/redis \
      -n gravitee-apim \
      --set auth.enabled=true \
      --set auth.password=redis-password
    ```

#### Verification

*   To verify that your Redis deployment succeeded, check pod status using the following command:\


    ```bash
    kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-redis
    ```

    \
    \
    The command generates the following output: \


    ```bash
    NAME                      READY   STATUS    RESTARTS   AGE
    gravitee-redis-0          1/1     Running     0        2m
    ```

### (Optional) Install PostgreSQL&#x20;

To support management data, you can install PostgreSQL into your Kubernetes cluster. For more information on installing PostgreSQL, see the [official chart documentation.](https://artifacthub.io/packages/helm/bitnami/postgresql)&#x20;

1.  Install PostgreSQL with Helm using the following command:\


    ```bash
    helm install gravitee-postgresql oci://registry-1.docker.io/cloudpirates/postgres \
      -n gravitee-apim \
      --set auth.database=gravitee \
      --set auth.username=gravitee \
      --set auth.password=changeme \
      --set persistence.enabled=true \
      --set persistence.size=8Gi \
      --set resources.requests.memory=512Mi \
      --set resources.requests.cpu=250m
    ```

#### Verification&#x20;

1.  To verify that your PostgreSQL deployment succeeded, retrieve the password using the following command:

    ```bash
    kubectl get secret --namespace gravitee-apim gravitee-postgresql -o jsonpath="{.data.postgres-password}" | base64 -d
    ```


2.  Check pod status using the following command:

    ```bash
    kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-postgresql
    ```

    \
    The command generates the following output:&#x20;

    ```bash
    NAME                    READY   STATUS    RESTARTS   AGE
    gravitee-postgresql-0   1/1     Running   0          2m
    ```



### (Enterprise Edition Only) Create Secret&#x20;

Before installing Gravitee APIM for [enterprise edition](../../readme/enterprise-edition.md), you need to create a Kubernetes secret for your license key.

1.  Create the secret using the following command:

    ```bash
    kubectl create secret generic gravitee-license \
      --from-file=license.key=./license.key \
      --namespace gravitee-apim
    ```

{% hint style="info" %}
* Ensure your license key file is named `license.key` and located in your current directory.
* The secret is named `gravitee-license` and referenced in your Helm configuration.
* If you don't have a license key, you can still proceed with community features.
{% endhint %}

### Prepare the `values.yaml` for Helm&#x20;

1.  Create a `values.yaml` file in your working directory and copy the following Gravitee configuration into it. This is the base configuration for your self-hosted APIM platform:\


    ```yaml
    # MongoDB Configuration
    mongo:
      uri: mongodb://gravitee-mongodb.gravitee-apim.svc.cluster.local:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000

    # PostgreSQL Configuration (uncomment if using)
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

    # Redis Configuration (uncomment if using)
    # redis:
    #   download: false
    #   host: gravitee-redis.gravitee-apim.svc.cluster.local
    #   port: 6379
    #   password: redis-password
    #   ssl: false

    # Repository types
    management:
      type: mongodb

    ratelimit:
      type: mongodb

    # Analytics configuration
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

        # Security exclusions for public endpoints and portal
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

      # Ingress configuration for Management API
      ingress:
        management:
          enabled: true
          ingressClassName: nginx
          scheme: http
          pathType: Prefix
          path: /management(/.*)?
          hosts:
            - api.yourdomain.com  # Replace with your domain
          annotations:
            nginx.ingress.kubernetes.io/enable-cors: "true"
            nginx.ingress.kubernetes.io/cors-allow-origin: "*"
            nginx.ingress.kubernetes.io/cors-allow-methods: "GET,POST,PUT,DELETE,OPTIONS,PATCH"
            nginx.ingress.kubernetes.io/cors-allow-headers: "Authorization,Content-Type,X-Requested-With,Accept,Origin,Cookie"
            nginx.ingress.kubernetes.io/cors-expose-headers: "X-Total-Count,Set-Cookie"
            nginx.ingress.kubernetes.io/cors-allow-credentials: "true"
            nginx.ingress.kubernetes.io/ssl-redirect: "false"  # Set to "true" for HTTPS
            nginx.ingress.kubernetes.io/rewrite-target: /$1
            nginx.ingress.kubernetes.io/use-regex: "true"
            nginx.ingress.kubernetes.io/proxy-body-size: "50m"
            nginx.ingress.kubernetes.io/proxy-read-timeout: "600"
            nginx.ingress.kubernetes.io/proxy-send-timeout: "600"
          # Uncomment for HTTPS/Production:
          # tls:
          #   - secretName: api-tls-secret
          #     hosts:
          #       - api.yourdomain.com

        portal:
          enabled: true
          ingressClassName: nginx
          scheme: http
          pathType: Prefix
          path: /portal
          hosts:
            - api.yourdomain.com  # Same as management API
          annotations:
            nginx.ingress.kubernetes.io/enable-cors: "true"
            nginx.ingress.kubernetes.io/cors-allow-origin: "http://portal.yourdomain.com"  # Change to your portal domain
            nginx.ingress.kubernetes.io/cors-allow-methods: "GET,POST,PUT,DELETE,OPTIONS,PATCH"
            nginx.ingress.kubernetes.io/cors-allow-headers: "DNT,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization,Accept,Origin,Cookie"
            nginx.ingress.kubernetes.io/cors-expose-headers: "Content-Length,Content-Range,Set-Cookie"
            nginx.ingress.kubernetes.io/cors-allow-credentials: "true"
            nginx.ingress.kubernetes.io/ssl-redirect: "false"
            nginx.ingress.kubernetes.io/proxy-body-size: "50m"
          # tls:
          #   - secretName: api-tls-secret
          #     hosts:
          #       - api.yourdomain.com

      resources:
        requests:
          memory: "1Gi"
          cpu: "500m"
        limits:
          memory: "2Gi"
          cpu: "1"

      # Autoscaling configuration
      autoscaling:
        enabled: true
        minReplicas: 2
        maxReplicas: 5
        targetAverageUtilization: 70
        targetMemoryAverageUtilization: 80

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

      # Ingress configuration for Gateway
      ingress:
        enabled: true
        ingressClassName: nginx
        pathType: Prefix
        path: /
        hosts:
          - gateway.yourdomain.com  # Replace with your gateway domain
        annotations:
          nginx.ingress.kubernetes.io/ssl-redirect: "false"
          nginx.ingress.kubernetes.io/proxy-body-size: "50m"
          nginx.ingress.kubernetes.io/proxy-read-timeout: "600"
          nginx.ingress.kubernetes.io/proxy-send-timeout: "600"
          nginx.ingress.kubernetes.io/proxy-connect-timeout: "600"
        # tls:
        #   - secretName: gateway-tls-secret
        #     hosts:
        #       - gateway.yourdomain.com

      resources:
        requests:
          memory: "1Gi"
          cpu: "500m"
        limits:
          memory: "2Gi"
          cpu: "1"

      # Autoscaling configuration
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
          value: "http://api.yourdomain.com/management/organizations/DEFAULT/environments/DEFAULT/"
          # For HTTPS/Production, change to:
          # value: "https://api.yourdomain.com/management/organizations/DEFAULT/environments/DEFAULT/"

      service:
        type: ClusterIP
        externalPort: 8002
        internalPort: 8080

      # Ingress configuration for Management Console
      ingress:
        enabled: true
        ingressClassName: nginx
        pathType: ImplementationSpecific
        path: /console(/.*)?
        hosts:
          - console.yourdomain.com  # Replace with your console domain
        annotations:
          nginx.ingress.kubernetes.io/ssl-redirect: "false"
          nginx.ingress.kubernetes.io/rewrite-target: /$1
          nginx.ingress.kubernetes.io/use-regex: "true"
        # tls:
        #   - secretName: console-tls-secret
        #     hosts:
        #       - console.yourdomain.com

      resources:
        requests:
          memory: "256Mi"
          cpu: "100m"
        limits:
          memory: "512Mi"
          cpu: "250m"

      # Autoscaling configuration
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
          value: "http://api.yourdomain.com/portal/environments/DEFAULT"
          # For HTTPS/Production, change to:
          # value: "https://api.yourdomain.com/portal/environments/DEFAULT"

      service:
        type: ClusterIP
        externalPort: 8003
        internalPort: 8080

      # Ingress configuration for Developer Portal
      ingress:
        enabled: true
        ingressClassName: nginx
        pathType: Prefix
        path: /
        hosts:
          - portal.yourdomain.com  # Replace with your portal domain
        annotations:
          nginx.ingress.kubernetes.io/ssl-redirect: "false"
          nginx.ingress.kubernetes.io/proxy-body-size: "50m"
        # tls:
        #   - secretName: portal-tls-secret
        #     hosts:
        #       - portal.yourdomain.com

      resources:
        requests:
          memory: "256Mi"
          cpu: "100m"
        limits:
          memory: "512Mi"
          cpu: "250m"

      # Autoscaling configuration
      autoscaling:
        enabled: true
        minReplicas: 1
        maxReplicas: 3
        targetAverageUtilization: 70
        targetMemoryAverageUtilization: 80

    # External dependencies (disabled - using external deployments)
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

    # Main ingress disabled (using individual ingresses)
    ingress:
      enabled: false

    # Ratelimit configuration (uncomment to use Redis)
    # ratelimit:
    #   type: redis
    #   redis:
    #     download: false
    #     host: gravitee-redis.gravitee-apim.svc.cluster.local
    #     port: 6379
    #     password: redis-password
    #     ssl: false
    ```



2. Save your Gravitee `values.yaml` file in your working directory.

<details>

<summary>Explanations of key predefined <code>values.yaml</code> parameter settings</summary>

#### **Service Configuration**

The self-hosted setup uses `ClusterIP` services with **NGINX ingress controllers** for external access:

* **ClusterIP**: Internal cluster communication only - no direct external exposure
* **Ingress**: Routes external traffic through **NGINX Ingress Controller** to internal services
* **Domain-based routing**: Uses separate domains for Gateway, Management API, Console UI, and Portal UI
* **HTTPS enforcement**: All traffic can be redirected to HTTPS with SSL certificates from **Azure Key Vault** or **cert-manager**

#### **Resource Allocation**

The configured resource limits ensure optimal performance while preventing resource exhaustion:

* **Management API/Gateway**: 1-2Gi memory, 500m-1 CPU (handles API processing, gateway routing, and management operations)
* **UI Components (Console/Portal)**: 256-512Mi memory, 100-250m CPU (lightweight frontend serving)

#### **Ingress Strategy**

The ingress configuration enables external access with **NGINX-specific features**:

* **Multi-domain setup**: Separate domains for each component (gateway.yourdomain.com, api.yourdomain.com, console.yourdomain.com, portal.yourdomain.com)
* **Path-based routing**: Management API uses `/management` and `/portal` paths on the same domain
* **CORS enabled**: Comprehensive CORS headers configured at both application and NGINX ingress level for cross-origin requests
* **SSL/TLS**: TLS secrets (api-tls-secret, gateway-tls-secret, etc.) for HTTPS termination
* **NGINX annotations**: Proxy settings, timeouts, body size limits, and rewrite rules

#### **Autoscaling Configuration**

Horizontal Pod Autoscaling is enabled for all components to handle variable load with **Azure metrics**:

* **Management API/Gateway**: Scales 1-5/1-10 replicas based on 70% CPU and 80% memory utilization
* **UI Components**: Scales 1-3 replicas based on 70% CPU and 80% memory utilization
* **Dynamic scaling**: Automatically adjusts pod count based on actual resource consumption via **Azure Monitor metrics**

#### **Security Configuration**

Multiple security layers protect the deployment:

* **CORS policies**: Configured for all public-facing endpoints with specific allowed origins, methods, and headers
* **Security exclusions**: Public endpoints like `/auth/**`, `/_health`, and `/info`

</details>



### Install using Helm&#x20;

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

#### Verification&#x20;

Verify the installation was successful. The command output should be similar to the following:

```bash
NAME: gravitee-apim
LAST DEPLOYED: [DATE]
NAMESPACE: gravitee-apim
STATUS: deployed
REVISION: 1
```

To uninstall Gravitee APIM, use the following command:&#x20;

```bash
helm uninstall gravitee-apim --namespace gravitee-apim
```

## Verification&#x20;

To verify that your Gravitee APIM platform is up and running on AKS, complete the following steps:

1. [#access-gravitee-apim-web-interface](azure-aks.md#access-gravitee-apim-web-interface "mention")
2. [#validate-the-pods](azure-aks.md#validate-the-pods "mention")
3. [#validate-the-pods-2](azure-aks.md#validate-the-pods-2 "mention")
4. [#validate-the-gateway-logs](azure-aks.md#validate-the-gateway-logs "mention")
5. [#validate-ingress](azure-aks.md#validate-ingress "mention")
6. [#validate-the-gateway-url](azure-aks.md#validate-the-gateway-url "mention")

### Access Gravitee APIM Web Interface

Access the Gravitee APIM web interface using the following steps:

#### Management Console&#x20;

Open your browser and navigate to: `https://console.yourdomain.com/console`  The interface allows you to configure APIs, policies, and monitor your API platform.&#x20;

#### Developer Portal&#x20;

Open your browser and navigate to: `https://portal.yourdomain.com/`  The self-service portal allows developers to discover and consume APIs.&#x20;

### Validate the Pods&#x20;

A healthy deployment displays all pods with the `Running` status, `1/1` ready containers, and zero or minimal restart counts.

To validate the pods, complete the following steps:&#x20;

1.  Use the following command to query the pod status:

    ```bash
    kubectl get pods --namespace=gravitee-apim
    ```
2. Verify that the deployment was successful. The output should show all Gravitee components ready and running:

```bash
NAME                                    READY   STATUS    RESTARTS   AGE
gravitee-apim-api-xxx-xxx               1/1     Running   0          23m
gravitee-apim-gateway-xxx-xxx           1/1     Running   0          23m
gravitee-apim-portal-xxx-xxx            1/1     Running   0          23m
gravitee-apim-ui-xxx-xxx                1/1     Running   0          23m
gravitee-elasticsearch-master-0         1/1     Running   0          23m
gravitee-mongodb-xxx-xxx                1/1     Running   0          23m
gravitee-postgresql-0                   1/1     Running   0          23m
gravitee-redis-master-0                 1/1     Running   0          23m
```

### Validate the Services  <a href="#validate-the-pods" id="validate-the-pods"></a>

1.  To verify service configuration, run the following command:\


    ```bash
    kubectl get services -n gravitee-apim
    ```


2.  Verify that all services are properly configured. The output should show all required services:\


    ```bash
    NAME                              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)
    gravitee-apim-api                 ClusterIP   10.x.x.x        <none>        83/TCP
    gravitee-apim-gateway             ClusterIP   10.x.x.x        <none>        82/TCP
    gravitee-apim-ui                  ClusterIP   10.x.x.x        <none>        8002/TCP
    gravitee-apim-portal              ClusterIP   10.x.x.x        <none>        8003/TCP
    gravitee-mongodb                  ClusterIP   10.x.x.x        <none>        27017/TCP
    gravitee-elasticsearch            ClusterIP   10.x.x.x        <none>        9200/TCP,9300/TCP
    gravitee-postgresql               ClusterIP   10.x.x.x        <none>        5432/TCP
    gravitee-redis-master             ClusterIP   10.x.x.x        <none>        6379/TCP

    ```

### Validate the Gateway logs&#x20;

To validate the Gateway logs, complete the following steps:

1.  List the Gateway pod using the following command:\


    ```bash
    kubectl get pods -n gravitee-apim | grep gateway
    ```



2.  Verify that the Gateway is running properly. The output should show the Gateway ready and running:\


    ```bash
    gravitee-apim-gateway-xxxxxxxxxx  1/1     Running   0          23m
    ```


3.  View the Gateway logs using the following command: \


    ```bash
    kubectl logs -f gravitee-apim-gateway-xxxxxxxxxxxx -n gravitee-apim
    ```



### Validate Ingress&#x20;

1.  Verify ingress is working with the following command:\


    ```bash
    kubectl get ingress -n gravitee-apim
    ```
2.  The output should show the hosts and Azure Load Balancer IP addresses: \


    ```bash
    NAME                              CLASS   HOSTS                    ADDRESS          PORTS     AGE
    gravitee-apim-api-management      nginx   api.yourdomain.com       20.x.x.x         80, 443   23m
    gravitee-apim-api-portal          nginx   api.yourdomain.com       20.x.x.x         80, 443   23m
    gravitee-apim-gateway             nginx   gateway.yourdomain.com   20.x.x.x         80, 443   23m
    gravitee-apim-ui                  nginx   console.yourdomain.com   20.x.x.x         80, 443   23m
    gravitee-apim-portal              nginx   portal.yourdomain.com    20.x.x.x         80, 443   23m
    ```

### Validate the Gateway URL&#x20;

Validate your Gateway URL using the following steps:

1. [Validate Gateway URL using Ingress ](azure-aks.md#validate-gateway-url-using-ingress)
2. [Validate Gateway URL using Port Forwarding](azure-aks.md#validate-gateway-url-using-port-forwarding)

The Gateway URL is determined by the ingress configuration in your `values.yaml` file and Azure DNS settings pointing to the Azure Load Balancer IP addresses.

#### Validate Gateway URL using Ingress&#x20;

To validate the Gateway URL, complete the following steps:

1.  Get the Load Balancer IP addresses from ingress:

    ```bash
    kubectl get ingress -n gravitee-apim -o wide
    ```
2.  Verify the Gateway endpoint directly using the Load Balancer IP address:

    ```bash
    # Test Gateway
    curl -H "Host: gateway.yourdomain.com" http://20.x.x.x/

    # Or if DNS is configured and SSL certificate is set up:
    curl https://gateway.yourdomain.com/
    ```
3.  Verify that the Gateway is responding correctly. The output should show the following message, which confirms that no API is deployed yet for this URL:

    ```bash
    No context-path matches the request URI.
    ```

#### Validate Gateway URL using Port Forwarding&#x20;

1.  Set up port forwarding for the Gateway using the following command:&#x20;

    ```bash
    kubectl port-forward svc/gravitee-apim-gateway 8082:82 -n gravitee-apim
    ```
2.  Verify via port forwarding using the following command:&#x20;

    ```bash
    curl http://localhost:8082/
    ```
3.  Verify that the Gateway is responding correctly. The output should show the following message, which confirms that no API is deployed yet for this URL.

    ```bash
    No context-path matches the request URI.
    ```

## Next steps <a href="#next-steps" id="next-steps"></a>

* Create your first API. For more information about creating your first API, see [Create & Publish Your First API](https://documentation.gravitee.io/apim/how-to-guides/create-and-publish-your-first-api).
* Add native Kafka capabilities. For more information about adding native Kafka capabilities, see [Configure the Kafka Client & Gateway](../../kafka-gateway/configure-the-kafka-client-and-gateway.md).
