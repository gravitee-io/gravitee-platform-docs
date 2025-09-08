---
hidden: true
noIndex: true
---

# Vanilla Kubernetes

## Overview&#x20;

This guide deploys a complete self-hosted Gravitee APIM platform on Kubernetes using Helm charts.&#x20;

## Prerequisites

Before you install a Hybrid Gateway, complete the following steps:

* Install [helm](https://helm.sh/docs/intro/install/).
* Install [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl).
* Ensure you have access to the self-hosted Kubernetes cluster where you want to install the Gateway.
* Ensure the self-hosted target environment has outbound Internet connectivity to Gravitee Cloud using HTTPS/443.
* License key for Enterprise features (optional)

## Components Overview&#x20;

This self-hosted APIM deployment includes several components that work together to provide a complete API management platform:

* Management API: Handles API configuration, policies, and administrative operations
* Gateway: Processes API requests, applies policies, and routes traffic to backend services
* Management Console UI: Web interface for API administrators to configure and monitor APIs
* Developer Portal UI: Self-service portal for developers to discover and consume APIs

External dependencies:

* MongoDB: Stores API definitions, configurations, and rate limiting data
* Elasticsearch: Provides analytics, logging, and search capabilities for API metrics
* Redis: Supports advanced caching and distributed rate limiting (optional)
* PostgreSQL: Alternative database for management data (optional)

## Install the Gateway

To install the Gravitee Gateway, complete the following steps:

1. [#create-namespace](vanilla-kubernetes.md#create-namespace "mention")
2. [#install-mongodb](vanilla-kubernetes.md#install-mongodb "mention")
3. [#install-elasticsearch](vanilla-kubernetes.md#install-elasticsearch "mention")
4. [#install-redis](vanilla-kubernetes.md#install-redis "mention")
5. [#install-postgresql](vanilla-kubernetes.md#install-postgresql "mention")
6. [#prepare-values.yaml-for-helm](vanilla-kubernetes.md#prepare-values.yaml-for-helm "mention")
7. [#install-with-helm](vanilla-kubernetes.md#install-with-helm "mention")



### Create Namespace&#x20;

Kubernetes namespaces provide logical isolation and organization within a cluster. Creating a dedicated namespace for Gravitee APIM:

a. Isolates resources: Separates APIM components from other applications

b. Simplifies management: Groups related services, pods, and configurations together\


1.  Create the namespace using the following command:&#x20;

    ```bash
    kubectl create namespace gravitee-apim
    ```

{% hint style="info" %}
This guide requires **MongoDB** and **Elasticsearch** to be installed for the complete APIM platform to function.
{% endhint %}

### Install MongoDB

To support API definitions and configuration, you must install MongoDB into your Kubernetes cluster. For more information, see [Bitnami package for MongoDB](https://artifacthub.io/packages/helm/bitnami/mongodb)

1.  Install MongoDB with Helm using the following command: \


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
      --set resources.requests.memory=512Mi \
      --set resources.requests.cpu=250m
    ```



2.  Extract the MongoDB hostname from the command output and save it for future use. The following sample output lists `gravitee-mongodb.gravitee-apim.svc.cluster.local`  as the MongoDB hostname: \


    ```
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

    ```



3.  To verify that your MongoDB deployment succeeded, check pod status using the following command:

    ```bash
    kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-mongodb
    ```

    \
    The command generates the following output: \


    ```
    NAME                  READY   STATUS    RESTARTS   AGE
    gravitee-mongodb-0    1/1     Running   0          2m
    ```

    \


### Install Elasticsearch&#x20;

To support analytics and logging, you must install Elasticsearch into your Kubernetes cluster. For more information, see [Bitnami package for Elasticsearch.](https://artifacthub.io/packages/helm/bitnami/elasticsearch)

1.  Install Elasticsearch with Helm using the following command:\


    ```bash
    helm install gravitee-elasticsearch oci://registry-1.docker.io/bitnamicharts/elasticsearch \
      --version 19.13.14 \
      --namespace gravitee-apim \
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
2.  Extract the Elasticsearch hostname from the command output and save it for future use. The following sample output lists `http://gravitee-elasticsearch.gravitee-apim.svc.cluster.local:9200`as the Elasticsearch hostname:\


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



3.  To verify that your Elasticsearch deployment succeeded, check pod status using the following command:\


    ```bash
    kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-elasticsearch
    ```

    \
    The command generates the following output:\


    ```bash
    NAME                              READY   STATUS    RESTARTS   AGE
    gravitee-elasticsearch-master-0   1/1     Running   0          2m
    ```

### Install Redis

To support caching and rate-limiting, you must install Redis into your Kubernetes cluster. For more information, see [Bitnami package for Redis®](https://artifacthub.io/packages/helm/bitnami/redis).

1.  Install Redis with Helm using the following command: &#x20;

    ```bash
    helm install gravitee-redis oci://registry-1.docker.io/bitnamicharts/redis \
      --version 18.6.1 \
      --namespace gravitee-apim \
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
3.  To verify that your Redis deployment succeeded, check pod status using the following command:

    ```bash
    kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-redis
    ```

    The command generates the following output:&#x20;

    ```sh
    NAME                      READY   STATUS    RESTARTS   AGE
    gravitee-redis-master-0   1/1     Running   0          2m
    ```

### Install PostgreSQL&#x20;

To support management data, you can install PostgreSQL into your Kubernetes cluster. For more information, see [Bitnami package for PostgreSQL](https://artifacthub.io/packages/helm/bitnami/postgresql)

1.  Install PostgreSQL with Helm using the following command:\


    ```bash
    helm install gravitee-postgresql oci://registry-1.docker.io/bitnamicharts/postgresql \
      --version 13.2.24 \
      --namespace gravitee-apim \
      --set auth.database=gravitee \
      --set auth.username=gravitee \
      --set auth.password=changeme \
      --set persistence.enabled=true \
      --set persistence.size=8Gi \
      --set resources.requests.memory=512Mi \
      --set resources.requests.cpu=250m
    ```


2.  Extract the PostgreSQL hostname from the command output and save it for future use. The following sample output lists `gravitee-postgresql.gravitee-apim.svc.cluster.local`  as the PostgreSQL hostname:

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



3.  To verify that your PostgreSQL deployment succeeded, retrieve the password using the following command:\


    ```bash
    kubectl get secret --namespace gravitee-apim gravitee-postgresql -o jsonpath="{.data.postgres-password}" | base64 -d
    ```
4.  Check pod status using the following command:\


    ```bash
    kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-postgresql
    ```

    \
    The command generates the following output:&#x20;

    ```bash
    NAME                    READY   STATUS    RESTARTS   AGE
    gravitee-postgresql-0   1/1     Running   0          2m
    ```



### Create Secret (Enterprise Edition Only)

Before installing Gravitee APIM for enterprise edition, you need to create a Kubernetes secret for your license key.

1.  Create the secret with the following command:

    ```bash
    kubectl create secret generic gravitee-license \
      --from-file=license.key=./license.key \
      --namespace gravitee-apim
    ```

{% hint style="info" %}
* Ensure your license key file is named `license.key` and located in your current directory
* The secret will be named `gravitee-license` and referenced in your Helm configuration
* If you don't have a license key, you can still proceed with community features
{% endhint %}



### Prepare `values.yaml` for Helm&#x20;

To prepare your Gravitee values.yaml file for Helm, complete the following steps:

1.  Copy the following Gravitee values.yaml file. This is the base configuration for your self-hosted APIM platform:\


    ```yaml
    # Gravitee.io APIM Configuration using Helm Chart


    # MongoDB Configuration
    mongo:
      uri: mongodb://gravitee-mongodb.gravitee-apim.svc.cluster.local:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000

    # # PostgreSQL Configuration (alternative to MongoDB)
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

    # # Redis Configuration for caching and rate limiting
    # redis:
    #   download: true
    #   host: gravitee-redis-master.gravitee-apim.svc.cluster.local
    #   port: 6379
    #   password: redis-password
    #   ssl: false

    # Elasticsearch Configuration 
    es:
      enabled: true
      endpoints:
        - http://gravitee-elasticsearch.gravitee-apim.svc.cluster.local:9200

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

        # PostgreSQL Configuration
        - name: gravitee_management_repository_type
          value: "jdbc"
        - name: gravitee_management_jdbc_url
          value: "jdbc:postgresql://gravitee-postgresql.gravitee-apim.svc.cluster.local:5432/gravitee"
        - name: gravitee_management_jdbc_username
          value: "gravitee"
        - name: gravitee_management_jdbc_password
          value: "changeme"

      service:
        type: ClusterIP
        externalPort: 83
        internalPort: 8083

      ingress:
        management:
          enabled: true
          scheme: http
          pathType: Prefix
          path: /management
          hosts:
            - apim.localhost
          annotations:
            kubernetes.io/ingress.class: nginx
            nginx.ingress.kubernetes.io/enable-cors: "true"
            nginx.ingress.kubernetes.io/cors-allow-origin: "*"
            nginx.ingress.kubernetes.io/cors-allow-methods: "GET, POST, PUT, DELETE, OPTIONS"
            nginx.ingress.kubernetes.io/cors-allow-headers: "Authorization, Content-Type, X-Requested-With, Accept, Origin"
        portal:
          enabled: true
          scheme: http
          pathType: Prefix
          path: /portal
          hosts:
            - apim.localhost
          annotations:
            kubernetes.io/ingress.class: nginx
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

      # Uncomment out to add your license key using the enterprise editiion 
      # # License volume configuration for Management API
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

      env:
        # Redis configuration for Gateway caching and rate limiting
        - name: gravitee_ratelimit_repository_type
          value: "redis"
        - name: gravitee_ratelimit_redis_host
          value: "gravitee-redis-master.gravitee-apim.svc.cluster.local"
        - name: gravitee_ratelimit_redis_port
          value: "6379"
        - name: gravitee_ratelimit_redis_password
          value: "redis-password"

        # PostgreSQL for Gateway sync
        - name: gravitee_management_repository_type
          value: "jdbc"
        - name: gravitee_management_jdbc_url
          value: "jdbc:postgresql://gravitee-postgresql.gravitee-apim.svc.cluster.local:5432/gravitee"
        - name: gravitee_management_jdbc_username
          value: "gravitee"
        - name: gravitee_management_jdbc_password
          value: "changeme"

      service:
        type: ClusterIP
        externalPort: 82
        internalPort: 8082

      ingress:
        enabled: true
        pathType: Prefix
        path: /
        hosts:
          - api.localhost
        annotations:
          kubernetes.io/ingress.class: nginx

      resources:
        requests:
          memory: "1Gi"
          cpu: "500m"
        limits:
          memory: "2Gi"
          cpu: "1"

      # Redis rate limiting configuration
      ratelimit:
        redis:
          host: gravitee-redis-master.gravitee-apim.svc.cluster.local
          port: 6379
          password: redis-password
          ssl: false

    # Management Console UI
    ui:
      enabled: true
      replicaCount: 1
      image:
        repository: graviteeio/apim-management-ui
        tag: latest
        pullPolicy: Always

      # Fix the HTTPS issue by ensuring UI uses HTTP URLs
      env:
        - name: MGMT_API_URL
          value: "http://apim.localhost/management/organizations/DEFAULT/environments/DEFAULT/"

      service:
        type: ClusterIP
        externalPort: 8002
        internalPort: 8080

      ingress:
        enabled: true
        pathType: ImplementationSpecific
        path: /console(/.*)?
        hosts:
          - apim.localhost
        annotations:
          kubernetes.io/ingress.class: nginx
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
        pathType: Prefix
        path: /
        hosts:
          - dev.localhost
        annotations:
          kubernetes.io/ingress.class: nginx

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

    # Repository types - Using PostgreSQL and Redis
    management:
      type: mongodb

    ratelimit:
      type: mongodb

    # Alternative configurations (uncomment to use):

    # Option 1: PostgreSQL for management, MongoDB for rate limiting
    # management:
    #   type: jdbc
    # ratelimit:
    #   type: mongodb

    # Option 2: PostgreSQL for management, Redis for rate limiting  
    # management:
    #   type: jdbc
    # ratelimit:
    #   type: redis

    # Option 3: MongoDB for management, Redis for rate limiting
    # management:
    #   type: mongodb
    # ratelimit:
    #   type: redis

    # Note: When changing repository types, ensure you also:
    # 1. Uncomment the corresponding database configuration sections above
    # 2. Uncomment the relevant environment variables in the API and Gateway sections
    # 3. Install the required database services (MongoDB, PostgreSQL, Redis)
    ```



2. Make the following modifications to your values.yaml file:

* Replace `<elasticsearch_hostname>` with `http://gravitee-elasticsearch.gravitee-apim.svc.cluster.local:9200`&#x20;
* Replace `<mongodb_hostname>` with `mongodb://gravitee-mongodb.gravitee-apim.svc.cluster.local:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000`

3. Save your Gravitee `values.yaml` file in your working directory.

<details>

<summary>Explanations of key predefined <code>values.yaml</code> parameter settings</summary>

#### Service Configuration

The self-hosted setup uses `ClusterIP` services with ingress controllers for external access. This provides better production scalability compared to direct `LoadBalancer` services:

* **ClusterIP**: Internal cluster communication only
* **Ingress**: Routes external traffic through nginx ingress controller to internal services
* **Host-based routing**: Uses `apim.localhost`, `api.localhost`, and `dev.localhost` for different components

#### Resource Allocation

The configured resource limits ensure optimal performance while preventing resource exhaustion:

* **Management API/Gateway**: 1-2Gi memory, 500m-1 CPU (handles API processing and management operations)
* **UI Components**: 256-512Mi memory, 100-250m CPU (lightweight frontend serving)

#### Ingress Strategy

The ingress configuration enables external access with path-based and host-based routing:

* **CORS enabled**: Allows cross-origin requests for web UI functionality
* **Path rewriting**: Console UI uses regex path matching with URL rewriting
* **Multiple hosts**: Separates Gateway (`api.localhost`) from Management (`apim.localhost`) and Portal (`dev.localhost`)

</details>

### Install with Helm&#x20;

To install your Gravitee APIM with Helm, complete the following steps:

1.  Add the Gravitee Helm chart repository to your Kubernetes environment using the following command:

    ```bash
    helm repo add gravitee https://helm.gravitee.io
    ```
2.  Update the Helm repository with the following command:&#x20;

    ```bash
    helm repo update
    ```
3.  Install the Helm chart with the Gravitee `values.yaml` file into the namespace using the following command:

    ```bash
    helm install gravitee-apim gravitee/apim \
      --namespace gravitee-apim \
      -f ./values.yaml
    ```
4.  Verify the installation was successful. The command output should be similar to the following:

    ```bash
    NAME: gravitee-apim
    LAST DEPLOYED: [DATE]
    NAMESPACE: gravitee-apim
    STATUS: deployed
    REVISION: 1
    ```
5.  To uninstall Gravitee APIM, use the following command:

    ```bash
    helm uninstall gravitee-apim --namespace gravitee-apim
    ```

## Verification&#x20;

Your APIM platform components should now be running in your Kubernetes cluster.

To verify that your Gateway is up and running, complete the following steps:

1. [#validate-the-pods](vanilla-kubernetes.md#validate-the-pods "mention")
2. [#validate-the-services](vanilla-kubernetes.md#validate-the-services "mention")
3. [#validate-the-gateway-logs](vanilla-kubernetes.md#validate-the-gateway-logs "mention")
4. [#validate-ingress](vanilla-kubernetes.md#validate-ingress "mention")
5. [#access-gravitee-apim-web-interface](vanilla-kubernetes.md#access-gravitee-apim-web-interface "mention")
6. [#validate-the-gateway-url](vanilla-kubernetes.md#validate-the-gateway-url "mention")

### Validate the pods

A healthy deployment displays all pods with the Running status, `1/1` ready containers, and zero or minimal restart counts.

To validate the pods, complete the following steps:&#x20;

1.  Use the following command to query the pod status: \


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



### Validate the Services&#x20;

1.  To verify service configuration, run the following command:\


    ```bash
    kubectl get services -n gravitee-apim
    ```
2.  The output should show all required services:

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



### Validate the Gateway logs&#x20;

To validate the Gateway logs, complete the following steps:

1.  List the Gateway pod using the following command:

    ```bash
    kubectl get pods -n gravitee-apim | grep gateway
    ```


2.  The output should show the Gateway ready and running:

    ```bash
    gravitee-apim-gateway-xxx-xxx        1/1     Running   0          5m
    ```

### Validate Ingress&#x20;

1.  Verify ingress is working with the following command:&#x20;

    ```bash
    kubectl get ingress -n gravitee-apim
    ```
2.  The output should show the hosts and address.

    ```bash
    NAME                           CLASS    HOSTS            ADDRESS     PORTS   AGE
    gravitee-apim-api-management   <none>   apim.localhost   localhost   80      2d4h
    gravitee-apim-api-portal       <none>   apim.localhost   localhost   80      2d4h
    gravitee-apim-gateway          <none>   api.localhost    localhost   80      2d4h
    gravitee-apim-portal           <none>   dev.localhost    localhost   80      2d4h
    gravitee-apim-ui               <none>   apim.localhost   localhost   80      2d4h
    ```

### Access Gravitee APIM web interface

Access the Gravitee APIM web interface using the following steps:&#x20;

#### Management Console

1. Open your browser and navigate to: `http://apim.localhost/console` \
   &#x20;\
   \
   \
   \
   \
   \

2. Login with: `admin` / `admin`
3. The interface allows you to configure APIs, policies, and monitor your API platform

#### Developer Portal&#x20;

1. Open your browser and navigate to: `http://dev.localhost/`
2. This self-service portal allows developers to discover and consume APIs

### Validate the Gateway URL

Validate your Gateway URL using using the following steps:&#x20;

1. [#validate-gateway-url-using-ingress](vanilla-kubernetes.md#validate-gateway-url-using-ingress "mention")
2. [#validate-gateway-url-using-port-forwarding](vanilla-kubernetes.md#validate-gateway-url-using-port-forwarding "mention")

The Gateway URL is determined by the ingress configuration in your `values.yaml` file. This setup uses localhost hostnames for local development.

#### Validate Gateway URL using Ingress&#x20;

To validate the Gateway URL, complete the following steps:

1.  Test the Gateway endpoint directly:

    ```bash
    curl http://api.localhost/
    ```
2.  Confirm that the Gateway replies with `No context-path matches the request URI.` This message informs you that an API isn't yet deployed for this URL.

    ```bash
    No context-path matches the request URI.
    ```

#### Validate Gateway URL using Port Forwarding

1. Set up port forwarding for the Gateway:

```bash
kubectl port-forward svc/gravitee-apim-gateway 8082:82 -n gravitee-apim
```

2. Test via port forward:

```bash
curl http://localhost:8082/
```

3.  Confirm that the Gateway replies with `No context-path matches the request URI.` This message informs you that an API isn't yet deployed for this URL.\


    ```bash
    No context-path matches the request URI.
    ```



## Next steps

* Create your first API. For more information about creating your first API, see [create-and-publish-your-first-api](../../how-to-guides/create-and-publish-your-first-api/ "mention").
* Add native Kafka capabilities. For more information about adding native Kafka capabilities, see [configure-the-kafka-client-and-gateway.md](../../kafka-gateway/configure-the-kafka-client-and-gateway.md "mention").



