---
hidden: true
noIndex: true
---

# Deploy APIM with Kubernetes Manifest

## Overview

This page describes how to install and deploy a complete Gravitee API Management (APIM) platform on any Kubernetes environment using kubectl and Kubernetes manifests. This guide provides a deployment configuration suitable for self-hosted installations, whether on-premises or in cloud-based Kubernetes clusters.

This deployment method gives you full control over your APIM infrastructure, allowing you to customize configurations, resource allocations, and networking to meet your specific requirements.&#x20;

In this guide, we will configure and deploy the following components:

* APIM Management API
* APIM Management Console
* APIM Developer Portal
* APIM Gateway
* MongoDB replica set&#x20;
* PostgreSQL
* Elasticsearch Cluster
* Redis for rate limiting and caching

## Environment Setup

Before deploying Gravitee APIM components, complete the following initial setup steps to prepare your Kubernetes environment:

* [#prerequisites](deploy-apim-with-kubernetes-manifest.md#prerequisites "mention")
* [#create-namespace](deploy-apim-with-kubernetes-manifest.md#create-namespace "mention")
* [#create-license-secret-enterprise-edition-only](deploy-apim-with-kubernetes-manifest.md#create-license-secret-enterprise-edition-only "mention")

### Prerequisites

You must install the following command line tools:

* [Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
* [Helm v3](https://helm.sh/docs/intro/install/)
* Ensure you have access to the self-hosted Kubernetes cluster where you want to install the Gateway.
* Ensure the self-hosted target environment has outbound Internet connectivity to Gravitee Cloud using HTTPS/443.

### Create Namespace&#x20;

Create a dedicated namespace for Gravitee APIM components to maintain isolation and organization with the following configuration: \


1.  Create the `namespace.yaml` file with the following configuration:\


    ```yaml
    apiVersion: v1
    kind: Namespace
    metadata:
      name: gravitee-apim
      labels:
        name: gravitee-apim
    ```
2.  Apply the namespace configuration using the following command:\


    ```bash
    kubectl apply -f namespace.yaml
    ```



### Create License Secret (Enterprise edition only)

Gravitee APIM requires a valid license key for enterprise features. Store this license as a Kubernetes Secret that will be mounted by the [Gateway](deploy-apim-with-kubernetes-manifest.md#configure-gravitee-gateway) and [Management API](deploy-apim-with-kubernetes-manifest.md#configure-management-api-and-ui) components. Create a license key with the following steps:

1. Ensure you have your `license.key` file in the current directory
2.  Create the secret using the following command:\


    ```bash
    kubectl create secret generic gravitee-license \
      --from-file=license.key=./license.key \
      -n gravitee-apim
    ```
3.  Verify the secret was created using the following command: \


    ```yaml
    kubectl get secret gravitee-license -n gravitee-apim
    ```

{% hint style="info" %}
For Community Edition, skip the license secret creation and remove the volumeMounts and volumes sections referencing gravitee-license from all deployments.&#x20;
{% endhint %}

## Deploy Components&#x20;

To install and deploy the self-host APIM in your Kubernetes cluster, complete the following steps:&#x20;

1. [#configure-your-database-options](deploy-apim-with-kubernetes-manifest.md#configure-your-database-options "mention")
2. [#configure-gravitee-gateway](deploy-apim-with-kubernetes-manifest.md#configure-gravitee-gateway "mention")
3. [#configure-management-api-and-ui](deploy-apim-with-kubernetes-manifest.md#configure-management-api-and-ui "mention")
4. [#configure-the-portal-ui](deploy-apim-with-kubernetes-manifest.md#configure-the-portal-ui "mention")

## **Configure your database options**

{% tabs %}
{% tab title="MongoDB" %}
MongoDB serves as the database for API definitions, users, and configuration data. This deployment uses MongoDB 7.0 with proper resource allocation and health monitoring.

1.  Create the `mongodb.yaml` file and then copy the following configuration: \


    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: gravitee-mongodb
      namespace: gravitee-apim
      labels:
        app: gravitee-mongodb
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: gravitee-mongodb
      template:
        metadata:
          labels:
            app: gravitee-mongodb
        spec:
          containers:
          - name: mongodb
            image: mongo:7.0
            ports:
            - containerPort: 27017
              name: mongodb
            env:
            - name: MONGO_INITDB_DATABASE
              value: "gravitee"
            volumeMounts:
            - name: mongodb-data
              mountPath: /data/db
            resources:
              requests:
                memory: "512Mi"
                cpu: "250m"
              limits:
                memory: "1Gi"
                cpu: "500m"
            readinessProbe:
              tcpSocket:
                port: 27017
              initialDelaySeconds: 10
              periodSeconds: 10
            livenessProbe:
              tcpSocket:
                port: 27017
              initialDelaySeconds: 30
              periodSeconds: 30
          volumes:
          - name: mongodb-data
            emptyDir: {}
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: gravitee-mongodb
      namespace: gravitee-apim
      labels:
        app: gravitee-mongodb
    spec:
      selector:
        app: gravitee-mongodb
      ports:
      - port: 27017
        targetPort: 27017
        name: mongodb
      type: ClusterIP
    ```



2. Apply and deploy mongodb using the command: `kubectl apply -f mongodb.yaml` &#x20;


{% endtab %}

{% tab title="PostgreSQL" %}
PostgreSQL is used to store the management and configuration data for Gravitee APIM.

1.  Create the `postgresql.yaml` file and copy the following configuration:

    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: gravitee-postgresql
      namespace: gravitee-apim
      labels:
        app: gravitee-postgresql
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: gravitee-postgresql
      template:
        metadata:
          labels:
            app: gravitee-postgresql
        spec:
          containers:
          - name: postgresql
            image: postgres:16-alpine
            ports:
            - containerPort: 5432
              name: postgresql
            env:
            # NOTE: Change the password to a secure value.
            # These variables are used to initialize the database on the first run.
            - name: POSTGRES_DB
              value: "gravitee"
            - name: POSTGRES_USER
              value: "gravitee"
            - name: POSTGRES_PASSWORD
              value: "changeme" 
            volumeMounts:
            - name: postgresql-data
              mountPath: /var/lib/postgresql/data
            resources:
              requests:
                memory: "512Mi"
                cpu: "250m"
              limits:
                memory: "1Gi"
                cpu: "500m"
            # Readiness and Liveness probes use 'pg_isready' to ensure the database
            # is actually ready to accept connections, not just that the port is open.
            readinessProbe:
              exec:
                command: ["pg_isready", "-U", "gravitee", "-d", "gravitee"]
              initialDelaySeconds: 15
              periodSeconds: 10
              timeoutSeconds: 5
            livenessProbe:
              exec:
                command: ["pg_isready", "-U", "gravitee", "-d", "gravitee"]
              initialDelaySeconds: 45
              periodSeconds: 30
              timeoutSeconds: 5
          volumes:
          # For production, you should use a PersistentVolumeClaim.
          - name: postgresql-data
            emptyDir: {}
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: gravitee-postgresql
      namespace: gravitee-apim
      labels:
        app: gravitee-postgresql
    spec:
      selector:
        app: gravitee-postgresql
      ports:
      - port: 5432
        targetPort: 5432
        name: postgresql
      type: ClusterIP
    ```



2. Deploy the file using the following command `kubectl apply -f postgresql.yaml` \

{% endtab %}

{% tab title="Elasticsearch" %}
Elasticsearch stores analytics data, logs, and metrics.&#x20;

1.  Create the `elasticsearch.yaml`  file and copy the following configuration: \


    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: gravitee-elasticsearch
      namespace: gravitee-apim
      labels:
        app: gravitee-elasticsearch
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: gravitee-elasticsearch
      template:
        metadata:
          labels:
            app: gravitee-elasticsearch
        spec:
          initContainers:
          - name: sysctl
            image: busybox:1.35
            command: ['sysctl', '-w', 'vm.max_map_count=262144']
            securityContext:
              privileged: true
          containers:
          - name: elasticsearch
            image: docker.elastic.co/elasticsearch/elasticsearch:7.17.15
            ports:
            - containerPort: 9200
            env:
            - name: discovery.type
              value: "single-node"
            - name: ES_JAVA_OPTS
              value: "-Xms1g -Xmx1g"
            - name: xpack.security.enabled
              value: "false"
            resources:
              requests:
                memory: "1.5Gi"
                cpu: "500m"
              limits:
                memory: "2.5Gi"
                cpu: "1"
            readinessProbe:
              httpGet:
                path: /_cluster/health
                port: 9200
              initialDelaySeconds: 30
              periodSeconds: 10
            livenessProbe:
              httpGet:
                path: /_cluster/health
                port: 9200
              initialDelaySeconds: 60
              periodSeconds: 30
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: gravitee-elasticsearch
      namespace: gravitee-apim
      labels:
        app: gravitee-elasticsearch
    spec:
      selector:
        app: gravitee-elasticsearch
      ports:
      - port: 9200
        targetPort: 9200
        name: http
      type: ClusterIP
    ```

    \

2. Deploy it using the following command: `kubectl apply -f elasticsearch.yaml`&#x20;
{% endtab %}

{% tab title="Redis" %}
Redis provides high-performance caching and rate limiting capabilities. This lightweight deployment is optimized for API management workloads.

1.  Create the `redis.yaml`  file and copy the following configuration: \


    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: gravitee-redis
      namespace: gravitee-apim
      labels:
        app: gravitee-redis
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: gravitee-redis
      template:
        metadata:
          labels:
            app: gravitee-redis
        spec:
          containers:
          - name: redis
            image: redis:7.2-alpine
            ports:
            - containerPort: 6379
              name: redis
            command:
            - redis-server
            - --appendonly
            - "yes"
            - --maxmemory
            - "256mb"
            - --maxmemory-policy
            - "allkeys-lru"
            volumeMounts:
            - name: redis-data
              mountPath: /data
            resources:
              requests:
                memory: "256Mi"
                cpu: "100m"
              limits:
                memory: "512Mi"
                cpu: "250m"
            readinessProbe:
              tcpSocket:
                port: 6379
              initialDelaySeconds: 10
              periodSeconds: 10
            livenessProbe:
              tcpSocket:
                port: 6379
              initialDelaySeconds: 30
              periodSeconds: 30
          volumes:
          - name: redis-data
            emptyDir: {}
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: gravitee-redis
      namespace: gravitee-apim
      labels:
        app: gravitee-redis
    spec:
      selector:
        app: gravitee-redis
      ports:
      - port: 6379
        targetPort: 6379
        name: redis
      type: ClusterIP
    ```



2. Apply and deploy the file using the command `kubectl apply -f redis.yaml` \

{% endtab %}
{% endtabs %}

### **Configure Gravitee Gateway**

The following tables list the configuration, and deployment parameters for the Gravitee Gateway

{% tabs %}
{% tab title="Gravitee Gateway" %}
The Gateway component handles all API traffic, applying policies, transformations, and routing requests to backend services. This configuration includes integration with MongoDB for configuration sync and Elasticsearch for analytics.

1.  Create the `gateway.yaml` file, and then copy the following configuration: \


    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: gravitee-gateway
      namespace: gravitee-apim
      labels:
        app: gravitee-gateway
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: gravitee-gateway
      template:
        metadata:
          labels:
            app: gravitee-gateway
        spec:
          containers:
          - name: gravitee-gateway
            image: graviteeio/apim-gateway:latest
            ports:
            - containerPort: 8082
            env:
            - name: gravitee_ratelimit_repository_type
              value: "mongodb"
            - name: gravitee_ratelimit_mongodb_uri
              value: "mongodb://gravitee-mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000"
            - name: gravitee_reporters_elasticsearch_endpoints_0
              value: "http://gravitee-elasticsearch:9200"
            - name: gravitee_services_sync_type
              value: "http"
            - name: gravitee_services_sync_endpoints_0
              value: "http://gravitee-management-api:8083/management/organizations/DEFAULT/environments/DEFAULT"
            resources:
              requests:
                memory: "1Gi"
                cpu: "500m"
              limits:
                memory: "2Gi"
                cpu: "1"
            volumeMounts:
            - name: gravitee-license
              mountPath: "/opt/graviteeio-gateway/license/license.key"
              subPath: license.key
              readOnly: true
            startupProbe:
              tcpSocket:
                port: 8082
              failureThreshold: 30
              periodSeconds: 10
            livenessProbe:
              tcpSocket:
                port: 8082
              initialDelaySeconds: 30
              periodSeconds: 30
              failureThreshold: 3
            readinessProbe:
              tcpSocket:
                port: 8082
              initialDelaySeconds: 30
              periodSeconds: 30
              failureThreshold: 3
          volumes:
          - name: gravitee-license
            secret:
              secretName: gravitee-license
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: gravitee-gateway
      namespace: gravitee-apim
      labels:
        app: gravitee-gateway
    spec:
      selector:
        app: gravitee-gateway
      ports:
      - port: 8082
        targetPort: 8082
        name: http
      type: ClusterIP
    ```

    \

2. Apply and deploy the configuration using the following command: `kubectl apply -f gateway.yaml`&#x20;

\

{% endtab %}
{% endtabs %}

### Configure Management API and UI&#x20;

Configure and deploy the management API and UI with the following configurations:&#x20;

{% tabs %}
{% tab title="Management API" %}
The Management API serves as the central control plane for Gravitee APIM, handling all administrative operations, API lifecycle management, and configuration synchronization.

1.  Create the `managementapi.yaml` file, and then deploy the Management API using the following configuration: \


    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: gravitee-management-api
      namespace: gravitee-apim
      labels:
        app: gravitee-management-api
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: gravitee-management-api
      template:
        metadata:
          labels:
            app: gravitee-management-api
        spec:
          containers:
          - name: gravitee-management-api
            image: graviteeio/apim-management-api:latest
            ports:
            - containerPort: 8083
              name: http
            - containerPort: 8072  # ADDED FOR FEDERATION WEBSOCKET
              name: federation-ws
            env:
            - name: gravitee_management_repository_type
              value: "mongodb"
            - name: gravitee_management_mongodb_uri
              value: "mongodb://gravitee-mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000"
            - name: gravitee_analytics_elasticsearch_endpoints_0
              value: "http://gravitee-elasticsearch:9200"
            - name: gravitee_http_host
              value: "0.0.0.0"
            - name: gravitee_http_cors_allow-origin
              value: "*"
            - name: gravitee_management_security_exclude_0
              value: "/management/apis/_health"
            # --- FEDERATION CONFIGURATION ---
            - name: gravitee_integration_enabled
              value: "true"
            - name: gravitee_exchange_controller_enabled
              value: "true"
            - name: gravitee_exchange_controller_ws_enabled
              value: "true"
            - name: gravitee_exchange_controller_ws_port
              value: "8072"
            - name: gravitee_exchange_controller_ws_host
              value: "0.0.0.0"
            - name: gravitee_federation_agent_enabled
              value: "true"
            resources:
              requests:
                memory: "1Gi"
                cpu: "500m"
              limits:
                memory: "2Gi"
                cpu: "1"
            volumeMounts:
            - name: gravitee-license
              mountPath: "/opt/graviteeio-management-api/license/license.key"
              subPath: license.key
              readOnly: true
            startupProbe:
              tcpSocket:
                port: 8083
              failureThreshold: 30
              periodSeconds: 10
            livenessProbe:
              tcpSocket:
                port: 8083
              initialDelaySeconds: 30
              periodSeconds: 30
              failureThreshold: 3
            readinessProbe:
              tcpSocket:
                port: 8083
              initialDelaySeconds: 30
              periodSeconds: 30
              failureThreshold: 3
          volumes:
          - name: gravitee-license
            secret:
              secretName: gravitee-license
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: gravitee-management-api
      namespace: gravitee-apim
      labels:
        app: gravitee-management-api
    spec:
      selector:
        app: gravitee-management-api
      ports:
      - port: 8083
        targetPort: 8083
        name: http
      - port: 8072  # ADDED FOR FEDERATION WEBSOCKET
        targetPort: 8072
        name: federation-ws
      type: ClusterIP
    ```


2. Apply the file using the command `kubectl apply -f managementapi.yaml`
{% endtab %}

{% tab title="Management UI" %}
The Management Console provides the administrative interface to manage APIs, applications, and settings.

1.  Create the `managementui.yaml` file, and then copy the following configuration: \


    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: gravitee-management-ui
      namespace: gravitee-apim
      labels:
        app: gravitee-management-ui
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: gravitee-management-ui
      template:
        metadata:
          labels:
            app: gravitee-management-ui
        spec:
          containers:
          - name: gravitee-management-ui
            image: graviteeio/apim-management-ui:latest
            ports:
            - containerPort: 8080
              name: http
            env:
            - name: MGMT_API_URL
              value: "http://localhost:30083/management/organizations/DEFAULT/environments/DEFAULT/"
            volumeMounts:
            - name: gravitee-management-ui-logs
              mountPath: /var/log/nginx
            resources:
              requests:
                memory: "256Mi"
                cpu: "100m"
              limits:
                memory: "512Mi"
                cpu: "250m"
            readinessProbe:
              httpGet:
                path: /
                port: 8080
              initialDelaySeconds: 10
              periodSeconds: 5
              timeoutSeconds: 3
            livenessProbe:
              httpGet:
                path: /
                port: 8080
              initialDelaySeconds: 30
              periodSeconds: 10
              timeoutSeconds: 5
          volumes:
          - name: gravitee-management-ui-logs
            emptyDir: {}
          restartPolicy: Always
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: gravitee-management-ui
      namespace: gravitee-apim
      labels:
        app: gravitee-management-ui
    spec:
      selector:
        app: gravitee-management-ui
      ports:
      - port: 8084
        targetPort: 8080
        name: http
      type: ClusterIP
    ```

    \

2. Apply the file using the command `kubectl apply -f managementui.yaml`
{% endtab %}
{% endtabs %}

### Configure the Portal UI&#x20;

The Developer Portal provides API consumers with documentation, testing tools, and application management capabilities.

1.  Create the `portalui.yaml` file, and then deploy the Portal UI using the following configuration: \


    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: gravitee-portal-ui
      namespace: gravitee-apim
      labels:
        app: gravitee-portal-ui
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: gravitee-portal-ui
      template:
        metadata:
          labels:
            app: gravitee-portal-ui
        spec:
          containers:
          - name: gravitee-portal-ui
            image: graviteeio/apim-portal-ui:latest
            ports:
            - containerPort: 8080
              name: http
            env:
            - name: PORTAL_API_URL
              value: "http://localhost:8083/portal/environments/DEFAULT"
            volumeMounts:
            - name: gravitee-portal-ui-logs
              mountPath: /var/log/nginx
            resources:
              requests:
                memory: "256Mi"
                cpu: "100m"
              limits:
                memory: "512Mi"
                cpu: "250m"
            readinessProbe:
              httpGet:
                path: /
                port: 8080
              initialDelaySeconds: 10
              periodSeconds: 5
              timeoutSeconds: 3
            livenessProbe:
              httpGet:
                path: /
                port: 8080
              initialDelaySeconds: 30
              periodSeconds: 10
              timeoutSeconds: 5
          volumes:
          - name: gravitee-portal-ui-logs
            emptyDir: {}
          restartPolicy: Always
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: gravitee-portal-ui
      namespace: gravitee-apim
      labels:
        app: gravitee-portal-ui
    spec:
      selector:
        app: gravitee-portal-ui
      ports:
      - port: 8085
        targetPort: 8080
        name: http
      type: ClusterIP
    ```

    \

2. Apply, and deploy the file using the command `kubectl apply -f portalui.yaml` &#x20;



### Configure Ingress&#x20;

The Ingress configuration provides a single entry point for all Gravitee APIM services, routing traffic based on URL paths. This setup uses NGINX Ingress Controller with path-based routing.

Configure your ingress route using the following steps:&#x20;

1.  Create the `ingress.yaml` file with the following configuration:\


    ```yaml
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: gravitee-ingress
      namespace: gravitee-apim
      annotations:
        nginx.ingress.kubernetes.io/ssl-redirect: "false"
        nginx.ingress.kubernetes.io/proxy-read-timeout: "3600"
        nginx.ingress.kubernetes.io/proxy-send-timeout: "3600"
        nginx.ingress.kubernetes.io/rewrite-target: /$2
    spec:
      ingressClassName: nginx
      rules:
      - host: localhost
        http:
          paths:
          # Gateway
          - path: /gateway(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: gravitee-gateway
                port:
                  number: 8082
          # Management API
          - path: /management(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: gravitee-management-api
                port:
                  number: 8083
          # Management UI
          - path: /console(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: gravitee-management-ui
                port:
                  number: 8084
          # Portal UI
          - path: /portal(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: gravitee-portal-ui
                port:
                  number: 8085
    ---
    # NodePort services for direct access during development
    apiVersion: v1
    kind: Service
    metadata:
      name: gravitee-gateway-nodeport
      namespace: gravitee-apim
      labels:
        app: gravitee-gateway
    spec:
      selector:
        app: gravitee-gateway
      ports:
      - port: 8082
        targetPort: 8082
        nodePort: 30082
        name: http
      type: NodePort
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: gravitee-management-api-nodeport
      namespace: gravitee-apim
      labels:
        app: gravitee-management-api
    spec:
      selector:
        app: gravitee-management-api
      ports:
      - port: 8083
        targetPort: 8083
        nodePort: 30083
        name: http
      - port: 8072
        targetPort: 8072
        nodePort: 30072
        name: federation
      type: NodePort
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: gravitee-management-ui-nodeport
      namespace: gravitee-apim
      labels:
        app: gravitee-management-ui
    spec:
      selector:
        app: gravitee-management-ui
      ports:
      - port: 8084
        targetPort: 8080
        nodePort: 30084
        name: http
      type: NodePort
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: gravitee-portal-ui-nodeport
      namespace: gravitee-apim
      labels:
        app: gravitee-portal-ui
    spec:
      selector:
        app: gravitee-portal-ui
      ports:
      - port: 8085
        targetPort: 8080
        nodePort: 30085
        name: http
      type: NodePort
    ```



2.  Apply, and deploy the ingress configuration using the command: \


    ```bash
    kubectl apply -f ingress.yaml
    ```

### Access Gravitee Components

Based on the [Ingress configuration above](deploy-apim-with-kubernetes-manifest.md#configure-ingress), you can access the following URLs:

* **APIM Console**: `http://localhost/console`
  * Default credentials: Username: `admin`, Password: `admin`
  * Use this interface to manage APIs, applications, and platform settings
* **Developer Portal**: `http://localhost/portal`
  * Default credentials: Username: `admin`, Password: `admin`
  * API consumers use this portal to discover and subscribe to APIs
* **Management API**: `http://localhost/management`
  * REST API endpoint for programmatic access
  * Test with: `curl http://localhost/management/organizations/DEFAULT/console`
* **Gateway**: `http://localhost/gateway`
  * API gateway endpoint where your APIs will be exposed

**Alternative Access via NodePort**

If Ingress is not configured or for development access, use the NodePort services:

* APIM Console: `http://localhost:30084`
* Developer Portal: `http://localhost:30085`
* Management API: `http://localhost:30083`
* Gateway: `http://localhost:30082`
* Federation WebSocket: `http://localhost:30072`



## **Configuration type**

{% tabs %}
{% tab title="External configuration" %}
To use external configuration files (like custom `gravitee.yml`), create ConfigMaps:

1. Create a ConfigMap from your configuration file:

```bash
kubectl create configmap gravitee-gateway-config \
  --from-file=gravitee.yml=./custom-gravitee.yml \
  -n gravitee-apim
```

2.  Mount the ConfigMap in your deployment:\


    ```yaml
    volumeMounts:
    - name: config
      mountPath: /opt/graviteeio-gateway/config
    volumes:
    - name: config
      configMap:
        name: gravitee-gateway-config
    ```
{% endtab %}
{% endtabs %}



## Verification&#x20;

After deploying all components, verify that your Gravitee APIM installation is functioning correctly by checking pod status, logs, and service endpoints.

### Validate the Pods&#x20;

All Gravitee APIM components should be running with healthy status. A healthy pod displays `Running` status with `1/1` ready containers and minimal restart counts.&#x20;

To validate your pods, complete the following steps:&#x20;

1.  Check all pods in the namespace using the following command:\


    ```bash
    kubectl get pods --namespace=gravitee-apim
    ```
2.  The output will be similar to the following:\


    ```bash
    NAME                                       READY   STATUS    RESTARTS   AGE
    gravitee-mongodb-7d9b8c6f5-xk9j2         1/1     Running   0          10m
    gravitee-postgresql-6c8d677c9b-h3k4l     1/1     Running   0          10m
    gravitee-elasticsearch-6b8d9f7c4-p2l8m   1/1     Running   0          9m
    gravitee-redis-5c7d6b8f9-m3n4k            1/1     Running   0          8m
    gravitee-gateway-8f7c9d6b5-w2r3t         1/1     Running   0          7m
    gravitee-management-api-7c8f9d6b4-k5l6m  1/1     Running   0          6m
    gravitee-management-ui-6d8c7f9b5-n3p2q   1/1     Running   0          5m
    gravitee-portal-ui-8b7d6c9f4-r4s5t      1/1     Running   0          4m
    gravitee-federation-agent-5d8f7c6b9-v2w3x 1/1     Running   0          3m
    ```



3.  Check specific components using the following command:\


    ```bash
    # Gateway pods
    kubectl get pods -n gravitee-apim -l app=gravitee-gateway

    # Management API pods
    kubectl get pods -n gravitee-apim -l app=gravitee-management-api

    # Federation Agent pods (if configured)
    kubectl get pods -n gravitee-apim -l app=gravitee-federation-agent
    ```



### Validate Services&#x20;

1.  Verify all services are configured using the following command:\


    ```bash
    kubectl get services -n gravitee-apim
    ```
2.  The output should show your `TYPE`, `NAME` and `PORT` :\


    ```bash
    NAME                              TYPE        CLUSTER-IP       PORT(S)
    gravitee-mongodb                  ClusterIP   10.96.x.x       27017/TCP
    gravitee-elasticsearch            ClusterIP   10.96.x.x       9200/TCP
    gravitee-redis                    ClusterIP   10.96.x.x       6379/TCP
    gravitee-gateway                  ClusterIP   10.96.x.x       8082/TCP
    gravitee-management-api           ClusterIP   10.96.x.x       8083/TCP,8072/TCP
    gravitee-management-ui            ClusterIP   10.96.x.x       8084/TCP
    gravitee-portal-ui                ClusterIP   10.96.x.x       8085/TCP
    gravitee-federation-agent         ClusterIP   10.96.x.x       8080/TCP
    gravitee-gateway-nodeport         NodePort    10.96.x.x       8082:30082/TCP
    gravitee-management-api-nodeport  NodePort    10.96.x.x       8083:30083/TCP,8072:30072/TCP
    gravitee-management-ui-nodeport   NodePort    10.96.x.x       8084:30084/TCP
    gravitee-portal-ui-nodeport       NodePort    10.96.x.x       8085:30085/TCP
    ```



### Validate the Gateway URL

The Gateway is exposed via NodePort service on port 30082. To validate the Gateway is running correctly, complete the following steps:

1.  Make a GET request to the Gateway endpoint:

    ```bash
    curl http://localhost:30082/
    ```
2.  Confirm that the Gateway replies with `No context-path matches the request URI.` This message informs you that an API isn't yet deployed for this URL.

    ```bash
    No context-path matches the request URI.
    ```

{% hint style="success" %}
You can now create and deploy APIs to your Gateway
{% endhint %}

## Federation

To use Federation, you need to enable specific environment variables in the Management API deployment, which activates the WebSocket endpoints required for federation agents to connect.

**Kubernetes-specific requirements for Federation:**

* **Service naming**: Ensure consistent service names across your deployments. Federation agents will connect to the Management API service using its Kubernetes service name (e.g., `gravitee-management-api`).
* **Port exposure**: The Management API must expose port 8072 for federation agent WebSocket connections. This port must be accessible to federation agents running in the same Kubernetes namespace or cluster.
* **Network policies**: If using network policies, ensure that federation agents can reach the Management API on port 8072.

To enable Federation, complete the following steps:

1. Update your existing [Management API deployment](deploy-apim-with-kubernetes-manifest.md#configure-management-api-and-ui) to include the Federation configuration. If you haven't deployed the Management API yet, use this configuration. If it's already deployed, update it with `kubectl apply -f`.
2. Create or update the `management-api.yaml` file with Federation environment variables enabled:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gravitee-management-api
  namespace: gravitee-apim
  labels:
    app: gravitee-management-api
spec:
  replicas: 1
  selector:
    matchLabels:
      app: gravitee-management-api
  template:
    metadata:
      labels:
        app: gravitee-management-api
    spec:
      containers:
      - name: gravitee-management-api
        image: graviteeio/apim-management-api:latest
        ports:
        - containerPort: 8083
          name: http
        - containerPort: 8072  # Federation WebSocket port for agents
          name: federation-ws
        env:
        - name: gravitee_management_repository_type
          value: "mongodb"
        - name: gravitee_management_mongodb_uri
          value: "mongodb://gravitee-mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000"
        - name: gravitee_analytics_elasticsearch_endpoints_0
          value: "http://gravitee-elasticsearch:9200"
        - name: gravitee_http_host
          value: "0.0.0.0"
        - name: gravitee_http_cors_allow-origin
          value: "*"
        - name: gravitee_management_security_exclude_0
          value: "/management/apis/_health"
        ## Federation is enabled
        - name: gravitee_integration_enabled
          value: "true"
        - name: gravitee_exchange_controller_enabled
          value: "true"
        - name: gravitee_exchange_controller_ws_enabled
          value: "true"
        - name: gravitee_exchange_controller_ws_port
          value: "8072"
        - name: gravitee_exchange_controller_ws_host
          value: "0.0.0.0"
        - name: gravitee_federation_agent_enabled
          value: "true"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1"
        volumeMounts:
        - name: gravitee-license
          mountPath: "/opt/graviteeio-management-api/license/license.key"
          subPath: license.key
          readOnly: true
        startupProbe:
          tcpSocket:
            port: 8083
          failureThreshold: 30
          periodSeconds: 10
        livenessProbe:
          tcpSocket:
            port: 8083
          initialDelaySeconds: 30
          periodSeconds: 30
          failureThreshold: 3
        readinessProbe:
          tcpSocket:
            port: 8083
          initialDelaySeconds: 30
          periodSeconds: 30
          failureThreshold: 3
      volumes:
      - name: gravitee-license
        secret:
          secretName: gravitee-license
---
apiVersion: v1
kind: Service
metadata:
  name: gravitee-management-api
  namespace: gravitee-apim
  labels:
    app: gravitee-management-api
spec:
  selector:
    app: gravitee-management-api
  ports:
  - port: 8083
    targetPort: 8083
    name: http
  - port: 8072  # Federation WebSocket port
    targetPort: 8072
    name: federation-ws
  type: ClusterIP
```

3.  Apply the Management API configuration using the following command:\


    ```bash
    kubectl apply -f management-api.yaml
    ```



### Configure Federation Agent&#x20;

The Federation Agent continuously synchronizes APIs from AWS API Gateway, Confluent, etc into Gravitee APIM, automatically creating API definitions and maintaining synchronization.

1.  Create the `federation-agent.yaml` file with the following configuration:\


    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: gravitee-federation-agent
      namespace: gravitee-apim
      labels:
        app: gravitee-federation-agent
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: gravitee-federation-agent
      template:
        metadata:
          labels:
            app: gravitee-federation-agent
        spec:
          containers:
          - name: federation-agent
            # Federation Agent Configuration
            # Select the correct agent image for your integration type:
            # * AWS API Gateway: graviteeio/federation-agent-aws-api-gateway:latest
            # * Confluent Platform: graviteeio/federation-agent-confluent-platform:latest
            # * Solace: graviteeio/federation-agent-solace:latest
            image: graviteeio/federation-agent-aws-api-gateway:latest
            env:
            # WebSocket connection configuration
            - name: gravitee_integration_connector_ws_endpoints_0
              value: "http://gravitee-management-api:8072"
            - name: gravitee_integration_connector_ws_headers_0_name
              value: "Authorization"
            - name: gravitee_integration_connector_ws_headers_0_value
              value: "bearer YOUR_ACCESS_TOKEN"  # Replace with your actual token
            
            # Provider configuration for AWS API Gateway
            # Update these environment variables based on your selected integration type
            - name: gravitee_integration_providers_0_type
              value: "aws-api-gateway"
            - name: gravitee_integration_providers_0_integrationId
              value: "YOUR_INTEGRATION_ID"  # Replace with your integration ID
            - name: gravitee_integration_providers_0_configuration_accessKeyId
              value: "YOUR_AWS_ACCESS_KEY"  # Consider using Secrets for production
            - name: gravitee_integration_providers_0_configuration_secretAccessKey
              value: "YOUR_AWS_SECRET_KEY"  # Consider using Secrets for production
            - name: gravitee_integration_providers_0_configuration_region
              value: "eu-west-2"
            - name: gravitee_integration_providers_0_configuration_acceptApiWithoutUsagePlan
              value: "true"
            
            # Logging configuration
            - name: GRAVITEE_LOG_LEVEL
              value: "DEBUG"
            resources:
              requests:
                memory: "256Mi"
                cpu: "100m"
              limits:
                memory: "512Mi"
                cpu: "250m"
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: gravitee-federation-agent
      namespace: gravitee-apim
      labels:
        app: gravitee-federation-agent
    spec:
      selector:
        app: gravitee-federation-agent
      ports:
      - port: 8080
        targetPort: 8080
        name: http
      type: ClusterIP
    ```



2.  Apply the Federation Agent deployment using the following command:\


    ```bash
    kubectl apply -f federation-agent.yaml
    ```



### Set up cluster mode

* APIM cluster mode is activated. Federation can work correctly in a highly available APIM deployment. Also, Hazelcast is configured and runs in memory as a library inside APIM.
* The default ingress used is the host used for the management API. Here is the default path: `/integration-controller`. The default ingress can be overridden in the federation ingress section with a dedicated host for the integration controller.

If you run a single replica of APIM, you can deactivate cluster mode by specifying the following environment variables and values:

```yaml
# To deactivate cluster mode for single replica deployments,
# add these environment variables to the Management API deployment:
        env:
        # ... other environment variables ...
        - name: GRAVITEE_CLUSTER_TYPE
          value: "standalone"
        - name: GRAVITEE_CACHE_TYPE
          value: "standalone"
```

