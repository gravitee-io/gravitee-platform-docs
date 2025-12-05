---
description: An overview about vanilla kubernetes.
---

# Vanilla Kubernetes

{% hint style="warning" %}
This installation guide is for only development and quick start purposes. Do not use it for production environments. For more information about best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Overview

This guide explains how to install a complete self-hosted Gravitee API Management (APIM) platform on Kubernetes using Helm charts.

## Prerequisites

Before you install the Gravitee APIM, complete the following steps:

* Install [helm](https://helm.sh/docs/intro/install/).
* Install [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl).
* Ensure you have access to the self-hosted Kubernetes cluster where you want to install Gravitee APIM.
* **(Enterprise Edition only)** Obtain a license key. For more information about obtaining a license key, see [Enterprise Edition Licensing.](../../../readme/enterprise-edition.md)

## Components Overview

This self-hosted APIM deployment includes several components that work together to provide a complete API management platform:

* Management API: Handles API configuration, policies, and administrative operations
* Gateway: Processes API requests, applies policies, and routes traffic to backend services
* Management Console UI: Web interface for API administrators to configure and monitor APIs
* Developer Portal UI: Self-service portal for developers to discover and consume APIs

The Gravitee APIM platform requires several external dependencies and services to provide complete functionality. Here are the required and optional dependencies and services:

*   Required dependencies and services:

    <div data-gb-custom-block data-tag="hint" data-style="danger" class="hint hint-danger"><p>The minimum installation of APIM requires MongoDB and Elasticsearch.</p></div>

    * MongoDB: Stores API definitions, configurations, and rate limiting data.
    * Elasticsearch: Provides analytics, logging, and search capabilities for API metrics.
* (Optional) Dependencies and services for enhanced functionality:
  * Redis: Supports advanced caching and distributed rate limiting.
  * PostgreSQL: Alternative database for management data.
  * Ingress Controller: Routes external traffic to APIM services and enables web access.

## Install the Gravitee APIM

To install the Gravitee APIM, complete the following steps:

1. [#create-namespace](./#create-namespace "mention")
2. [#install-mongodb](./#install-mongodb "mention")
3. [#install-elasticsearch](./#install-elasticsearch "mention")
4. [#optional-install-redis](./#optional-install-redis "mention")
5. [#optional-install-postgresql](./#optional-install-postgresql "mention")
6. [#enterprise-edition-only-create-secret](./#enterprise-edition-only-create-secret "mention")
7. [#install-ingress-controller](./#install-ingress-controller "mention")
8. [#configure-dns-resolution](./#configure-dns-resolution "mention")
9. [#prepare-values.yaml-for-helm](./#prepare-values.yaml-for-helm "mention")
10. [#install-with-helm](./#install-with-helm "mention")

### Create Namespace

Kubernetes namespaces provide logical isolation and organization within a cluster. Creating a dedicated namespace for Gravitee APIM has the following benefits: Isolates resources, Separates APIM components from other applications and Simplifies management by grouping related services, pods, and configurations together.

*   Create the namespace using the following command:

    ```bash
    kubectl create namespace gravitee-apim
    ```

#### Verification

*   Ensure that you created the namespace using the following command:

    ```bash
    kubectl get namespaces
    ```

    \
    The command generates an output similar to the following output:

    ```bash
    NAME              STATUS   AGE
    default           Active   12m
    gravitee-apim     Active   60s
    kube-node-lease   Active   12m
    kube-public       Active   12m
    kube-system       Active   12m
    ```

### Install MongoDB

{% hint style="info" %}
You can use PostgreSQL instead of MongoDB. For more information about installing PostgreSQL, see [#optional-install-postgresql](./#optional-install-postgresql "mention").
{% endhint %}

To support API definitions and configuration, you must install MongoDB into your Kubernetes cluster. For more information about installing MongoDB, see the [official chart documentation](https://artifacthub.io/packages/helm/bitnami/mongodb)

1.  Install MongoDB with Helm using the following command:

    ```bash
    helm install gravitee-mongodb oci://registry-1.docker.io/cloudpirates/mongodb \
      -n gravitee-apim \
      --set auth.enabled=false \
      --set persistence.enabled=false \
      --set resources.requests.memory=512Mi \
      --set resources.requests.cpu=250m
    ```

#### Verification

1.  To verify that your MongoDB deployment succeeded, check pod status using the following command:

    ```bash
    kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-mongodb -w
    ```

    \
    After a few minutes, the command generates the following output:

    ```bash
    NAME                  READY   STATUS    RESTARTS   AGE
    gravitee-mongodb-0    1/1     Running   0          2m
    ```

### Install Elasticsearch

To support analytics and logging, you must install Elasticsearch into your Kubernetes cluster. For more information on installing Elasticsearch, see the [official chart documentation.](https://artifacthub.io/packages/helm/elastic/elasticsearch)

1.  Install Elasticsearch using the following command:

    ```bash
    helm repo add elastic https://helm.elastic.co

    helm repo update

    helm -n gravitee-apim install elasticsearch elastic/elasticsearch \
      --set persistence.enabled=false \
      --set replicas=1 \
      --set minimumMasterNodes=1
    ```
2.  Follow the instructions that appear in your terminal, and retrieve Elastic user's password.

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

*   To verify that your Elasticsearch deployment succeeded, check pod status using the following command:

    ```bash
    kubectl get pods --namespace=gravitee-apim -l app=elasticsearch-master -w 
    ```

    \
    After a few minutes, the command generates the following output:

    ```purebasic
    NAME                     READY   STATUS    RESTARTS   AGE
    elasticsearch-master-0   1/1     Running   0          55m
    ```

### (Optional) Install Redis

To support caching and rate-limiting, you must install Redis into your Kubernetes cluster. For more information about installing Redis, see the [official chart documentation.](https://artifacthub.io/packages/helm/cloudpirates-redis/redis)

*   Install Redis with Helm using the following command:

    ```bash
    helm install gravitee-redis oci://registry-1.docker.io/cloudpirates/redis \
      -n gravitee-apim \
      --set auth.enabled=true \
      --set auth.password=redis-password
    ```

#### Verification

1.  To verify that your Redis deployment succeeded, check pod status using the following command:

    ```bash
    kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-redis
    ```

    \
    After a few minutes, the command generates the following output:

    ```bash
    NAME                      READY   STATUS    RESTARTS   AGE
    gravitee-redis-0          1/1     Running     0        2m
    ```

### (Optional) Install PostgreSQL

To support management data, you can install PostgreSQL into your Kubernetes cluster. For more information on installing PostgreSQL, see the [official chart documentation.](https://artifacthub.io/packages/helm/bitnami/postgresql)

1.  Install PostgreSQL with Helm using the following command:

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

#### Verification

1.  To verify that your PostgreSQL deployment succeeded, retrieve the password using the following command:

    ```bash
    kubectl -n gravitee-apim get secret gravitee-postgresql -o jsonpath="{.data.postgres-password}" | base64 -d
    ```
2.  Check pod status using the following command:

    ```bash
    kubectl -n gravitee-apim get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-postgresql
    ```

    \
    The command generates the following output:

    ```bash
    NAME                    READY   STATUS    RESTARTS   AGE
    gravitee-postgresql-0   1/1     Running    0          2m
    ```

### (Enterprise Edition Only) Create Secret

Before you install the Enterprise Edition of Gravitee APIM, you need to create a Kubernetes secret for your license key.

1.  Create the secret using the following command:

    ```bash
    kubectl create secret generic gravitee-license \
      --from-file=license.key=./license.key \
      --namespace gravitee-apim
    ```

{% hint style="info" %}
* Ensure your license key file is named `license.key` and located in your current directory.
* The secret will be named `gravitee-license` and referenced in your Helm configuration.
* If you do not have a license key, you can still proceed with community features.
{% endhint %}

### Install Ingress Controller

{% hint style="info" %}
If you have installed the Ingress Controller, you can skip this section.
{% endhint %}

An ingress controller is required to route external traffic to your Gravitee APIM services. Choose the installation method based on your Kubernetes environment:

* [#install-nginx-ingress-controller-with-helm](./#install-nginx-ingress-controller-with-helm "mention")
* [#minikube-users-only-install-ingress-controller](./#minikube-users-only-install-ingress-controller "mention")

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

#### Verification

When you install the NGINX Ingress Controller, you receive the following message:

```
NAME: nginx-ingress
LAST DEPLOYED: Tue Oct 28 09:44:42 2025
NAMESPACE: ingress-nginx
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
The ingress-nginx controller has been installed.
It may take a few minutes for the load balancer IP to be available.
```

#### (Minikube users only) Install Ingress Controller

1.  Enable the built-in ingress addon using the following command:

    ```bash
    minikube addons enable ingress
    ```
2.  In a separate terminal, enable the network tunnel using the following command:

    <div data-gb-custom-block data-tag="hint" data-style="danger" class="hint hint-danger"><p>Keep the tunnel command running in a separate terminal window. The tunnel must remain active for ingress to function properly.</p></div>

    ```bash
    sudo minikube tunnel
    ```

#### Verification

*   Verify the ingress controller is running using the following command:

    ```bash
    kubectl get pods -n ingress-nginx
    ```

    \
    The output should show the ingress controller pod in Running status:

    ```bash
    NAME                                       READY   STATUS    RESTARTS   AGE
    ingress-nginx-controller-xxx-xxx           1/1     Running   0          2
    ```

### Configure DNS Resolution

For local development with custom hostnames, you must add DNS entries to your system's hosts file.

1.  Add the required DNS entries using the following commands:

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
    The output shows the three localhost entries:

    ```bash
    127.0.0.1 apim.localhost
    127.0.0.1 api.localhost
    127.0.0.1 dev.localhost
    ```

### Prepare the `values.yaml` for Helm

{% hint style="info" %}
Ensure that you have the following sections complete:

* [#install-ingress-controller](./#install-ingress-controller "mention")
* [#configure-dns-resolution](./#configure-dns-resolution "mention")
{% endhint %}

1.  Create a `values.yaml` file in your working directory, and then copy the following Gravitee configuration into the file. This is the base configuration for your self-hosted APIM platform:

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
          value: "Authorization,Content-Type,X-Requested-With,Accept,Origin,Access-Control-Request-Method,Access-Control-Request-Headers,Cookie"
        - name: gravitee_http_cors_allow-methods
          value: "GET,POST,PUT,DELETE,OPTIONS"
        - name: gravitee_http_cors_exposed-headers
          value: "X-Total-Count,Set-Cookie"
        - name: gravitee_http_cors_allow-credentials
          value: "true"

        # Cookie Configuration - Set SameSite to None for cross-site requests
        - name: gravitee_http_cookie_sameSite
          value: "Lax"
        - name: gravitee_http_cookie_secure
          value: "false"

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
            nginx.ingress.kubernetes.io/cors-allow-origin: "http://dev.localhost"
            nginx.ingress.kubernetes.io/cors-allow-methods: "GET, POST, PUT, DELETE, OPTIONS, PATCH"
            nginx.ingress.kubernetes.io/cors-allow-headers: "DNT,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization,Accept,Origin,Cookie"
            nginx.ingress.kubernetes.io/cors-expose-headers: "Content-Length,Content-Range,Set-Cookie"
            nginx.ingress.kubernetes.io/cors-allow-credentials: "true"

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
      
    # # Uncomment to use Redis Configuration for caching and rate limiting
    # ratelimit:
    #   redis:
    #     download: false
    #     host: gravitee-redis.gravitee-apim.svc.cluster.local
    #     port: 6379
    #     password: redis-password
    #     ssl: false

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
        annotations: {}

      resources:
        requests:
          memory: "256Mi"
          cpu: "100m"
        limits:
          memory: "512Mi"
          cpu: "250m"
      
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

    # Current configuration: MongoDB for management and for rate limiting
    # Ensure you have Mongo and Elasticsearch services running in your cluster
    ```

    1. Replace `[ELASTIC PASSWORD FROM ES INSTALLATION]` with your Elasticsearch password.
    2. If your Kubernetes cluster does not support IPV6 networking, both the UI and Portal deployments must set the `IPV4_ONLY` environment variable to `true`.
2.  **(Enterprise Edition only)** Navigate to the following section, and then uncomment the following configuration:

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
3. Save your Gravitee `values.yaml` file in your working directory.

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

1.  Add the Gravitee Helm chart repository to your Kubernetes environment using the following command:

    ```bash
    helm repo add gravitee https://helm.gravitee.io

    helm repo update
    ```
2.  Install the Helm chart with the Gravitee `values.yaml` file into the namespace using the following command:

    ```bash
    helm install gravitee-apim gravitee/apim \
      --namespace gravitee-apim \
      -f ./values.yaml \
      --set 'portal.ingress.annotations.nginx\.ingress\.kubernetes\.io/rewrite-target=null' \
      --wait \
      --timeout 5m
    ```

#### Verification

* Verify that the installation was successful with the following command:

```bash
kubectl get pods --namespace=gravitee-apim -l app.kubernetes.io/instance=gravitee-apim -w
```

Verify the installation was successful. The command output should be similar to the following:

```bash
NAME: gravitee-apim
LAST DEPLOYED: [DATE]
NAMESPACE: gravitee-apim
STATUS: deployed
REVISION: 1
```

## Verification

To verify that your Gravitee APIM platform is up and running, complete the following steps:

1. [#access-gravitee-apim-web-interface](./#access-gravitee-apim-web-interface "mention")
2. [#validate-the-pods](./#validate-the-pods "mention")
3. [#validate-the-services](./#validate-the-services "mention")
4. [#validate-the-gateway-logs](./#validate-the-gateway-logs "mention")
5. [#validate-ingress](./#validate-ingress "mention")
6. [#validate-the-gateway-url](./#validate-the-gateway-url "mention")

### Access Gravitee APIM web interface

* To open the APIM Console, go to `http://apim.localhost/console` The default username and password are both `admin`.
* To open the Developer Portal, go to `http://dev.localhost/`. The default username and password are both `admin`.

### Validate the pods

A healthy deployment displays the pods with the Running status, `1/1` ready containers, and zero or minimal restart counts.

*   To validate the pods, query the pods status using the following command:

    ```bash
    kubectl get pods --namespace=gravitee-apim
    ```

    \
    The output shows all Gravitee components ready and running:

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

1.  Verify that all services are properly configured using the following command:

    ```bash
    kubectl get services -n gravitee-apim
    ```

    \
    The output shows all required services:

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

*   Validate the Gateway logs using the following command:

    ```bash
    kubectl get pods -n gravitee-apim | grep gateway
    ```

    \
    The output shows the Gateway ready and running:

    <pre class="language-bash"><code class="lang-bash"><strong>gravitee-apim-gateway-xxx-xxx        1/1     Running   0          5m
    </strong></code></pre>

### Validate Ingress

*   Verify ingress is working using the following command:

    ```bash
    kubectl get ingress -n gravitee-apim
    ```

    \
    The output shows the hosts and address:

    ```bash
    NAME                           CLASS   HOSTS            ADDRESS     PORTS   AGE
    gravitee-apim-api-management   nginx   apim.localhost   localhost   80      27h
    gravitee-apim-api-portal       nginx   apim.localhost   localhost   80      27h
    gravitee-apim-gateway          nginx   api.localhost    localhost   80      27h
    gravitee-apim-portal           nginx   dev.localhost    localhost   80      27h
    gravitee-apim-ui               nginx   apim.localhost   localhost   80      27h
    ```

### Validate the Gateway URL

Validate your Gateway URL by completing the following steps:

1. [#validate-gateway-url-using-ingress](./#validate-gateway-url-using-ingress "mention")
2. [#validate-gateway-url-using-port-forwarding](./#validate-gateway-url-using-port-forwarding "mention")

The Gateway URL is determined by the ingress configuration in your `values.yaml` file. This setup uses localhost hostnames for local development.

#### Validate Gateway URL using Ingress

To validate the Gateway URL, complete the following steps:

1.  Verify the Gateway endpoint directly using the following command:

    ```bash
    curl http://api.localhost/
    ```

    \
    The output should show the following message, which confirms that no API is deployed yet for this URL.

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

    \
    The output shows the following message, which confirms that no API is deployed yet for this URL:

    ```bash
    No context-path matches the request URI.
    ```

## Next steps

* Create your first API. For more information about creating your first API, see [create-and-publish-your-first-api](../../../how-to-guides/create-and-publish-your-first-api/ "mention").
* Add native Kafka capabilities. For more information about adding native Kafka capabilities, see [configure-the-kafka-client-and-gateway.md](../../../kafka-gateway/configure-the-kafka-client-and-gateway.md "mention").
