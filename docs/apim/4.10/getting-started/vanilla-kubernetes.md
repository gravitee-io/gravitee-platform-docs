### Create Namespace

Kubernetes namespaces provide logical isolation and organization within a cluster. Creating a dedicated namespace for Gravitee APIM isolates resources, separates APIM components from other applications, and simplifies management by grouping related services, pods, and configurations together.

Create the namespace:

```bash
kubectl create namespace gravitee-apim
```

#### Verification

Verify the namespace was created:

```bash
kubectl get namespaces
```

The command output should include the `gravitee-apim` namespace:

```bash
NAME              STATUS   AGE
default           Active   12m
gravitee-apim     Active   60s
kube-node-lease   Active   12m
kube-public       Active   12m
kube-system       Active   12m
```

### Install MongoDB

MongoDB stores API definitions, configurations, and rate limiting data. For more information about installing MongoDB, see the [official chart documentation](https://artifacthub.io/packages/helm/bitnami/mongodb).

Install MongoDB with Helm:

```bash
helm install gravitee-mongodb oci://registry-1.docker.io/cloudpirates/mongodb \
  -n gravitee-apim \
  --set auth.enabled=false \
  --set persistence.enabled=false \
  --set resources.requests.memory=512Mi \
  --set resources.requests.cpu=250m
```

#### Verification

Check pod status:

```bash
kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-mongodb -w
```

After a few minutes, the pod should be running:

```bash
NAME                  READY   STATUS    RESTARTS   AGE
gravitee-mongodb-0    1/1     Running   0          2m
```

### Install Elasticsearch

Elasticsearch provides analytics, logging, and search capabilities for API metrics. For more information about installing Elasticsearch, see the [official chart documentation](https://artifacthub.io/packages/helm/elastic/elasticsearch).

1. Add the Elastic Helm repository and install Elasticsearch:

    ```bash
    helm repo add elastic https://helm.elastic.co
    helm repo update

    helm -n gravitee-apim install elasticsearch elastic/elasticsearch \
      --set persistence.enabled=false \
      --set replicas=1 \
      --set minimumMasterNodes=1
    ```

2. Retrieve the Elasticsearch password from the installation output:

    ```bash
    kubectl get secrets --namespace=gravitee-apim elasticsearch-master-credentials -ojsonpath='{.data.password}' | base64 -d
    ```

#### Verification

Check pod status:

```bash
kubectl get pods --namespace=gravitee-apim -l app=elasticsearch-master -w
```

After a few minutes, the pod should be running:

```bash
NAME                     READY   STATUS    RESTARTS   AGE
elasticsearch-master-0   1/1     Running   0          55m
```

### (Enterprise Edition Only) Create Secret

Before installing the Enterprise Edition of Gravitee APIM, create a Kubernetes secret for your license key.

Create the secret:

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
If you have already installed an ingress controller, skip this section.
{% endhint %}

An ingress controller routes external traffic to your Gravitee APIM services. Choose the installation method based on your Kubernetes environment:

* [Install NGINX Ingress Controller with Helm](#install-nginx-ingress-controller-with-helm)
* [(Minikube users only) Install Ingress Controller](#minikube-users-only-install-ingress-controller)

#### Install NGINX Ingress Controller with Helm

1. Add the `ingress-nginx` Helm repository:

    ```bash
    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm repo update
    ```

2. Install the NGINX Ingress Controller:

    ```bash
    helm install nginx-ingress ingress-nginx/ingress-nginx \
      --namespace ingress-nginx \
      --create-namespace \
      --set controller.service.type=LoadBalancer \
      --set controller.admissionWebhooks.enabled=false
    ```

##### Verification

Verify the ingress controller is running:

```bash
kubectl get pods -n ingress-nginx
```

The output should show the ingress controller pod in Running status:

```bash
NAME                                       READY   STATUS    RESTARTS   AGE
ingress-nginx-controller-xxx-xxx           1/1     Running   0          2m
```

#### (Minikube users only) Install Ingress Controller

1. Enable the built-in ingress addon:

    ```bash
    minikube addons enable ingress
    ```

2. In a separate terminal, enable the network tunnel:

    {% hint style="danger" %}
    Keep the tunnel command running in a separate terminal window. The tunnel must remain active for ingress to function properly.
    {% endhint %}

    ```bash
    sudo minikube tunnel
    ```

##### Verification

Verify the ingress controller is running:

```bash
kubectl get pods -n ingress-nginx
```

The output should show the ingress controller pod in Running status:

```bash
NAME                                       READY   STATUS    RESTARTS   AGE
ingress-nginx-controller-xxx-xxx           1/1     Running   0          2m
```

### Configure DNS Resolution

For local development with custom hostnames, add DNS entries to your system's hosts file.

Add the required DNS entries:

```bash
echo "127.0.0.1 apim.localhost" | sudo tee -a /etc/hosts
echo "127.0.0.1 api.localhost" | sudo tee -a /etc/hosts  
echo "127.0.0.1 dev.localhost" | sudo tee -a /etc/hosts
```

#### Verification

Verify the DNS entries were added:

```bash
cat /etc/hosts | tail -5
```

The output should show the three localhost entries:

```bash
127.0.0.1 apim.localhost
127.0.0.1 api.localhost
127.0.0.1 dev.localhost
```

### Prepare the `values.yaml` for Helm

{% hint style="info" %}
Ensure you have completed the following sections:
* [Install Ingress Controller](#install-ingress-controller)
* [Configure DNS Resolution](#configure-dns-resolution)
{% endhint %}

1. Create a `values.yaml` file in your working directory and copy the following Gravitee configuration into the file:

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

2. Replace `[ELASTIC PASSWORD FROM ES INSTALLATION]` with your Elasticsearch password.

3. If your Kubernetes cluster does not support IPv6 networking, both the UI and Portal deployments must set the `IPV4_ONLY` environment variable to `true`.

4. **(Enterprise Edition only)** Navigate to the license volume configuration section and uncomment the following configuration:

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

5. Save your Gravitee `values.yaml` file in your working directory.

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

1. Add the Gravitee Helm chart repository to your Kubernetes environment:

    ```bash
    helm repo add gravitee https://helm.gravitee.io
    helm repo update
    ```

2. Install the Helm chart with the Gravitee `values.yaml` file into the namespace:

    ```bash
    helm install gravitee-apim gravitee/apim \
      --namespace gravitee-apim \
      -f ./values.yaml \
      --set 'portal.ingress.annotations.nginx\.ingress\.kubernetes\.io/rewrite-target=null' \
      --wait \
      --timeout 5m
    ```

#### Verification

Verify the installation was successful:

```bash
kubectl get pods --namespace=gravitee-apim -l app.kubernetes.io/instance=gravitee-apim -w
```

The command output should be similar to the following:

```bash
NAME: gravitee-apim
LAST DEPLOYED: [DATE]
NAMESPACE: gravitee-apim
STATUS: deployed
REVISION: 1
```