---
hidden: true
---

# Deploy a Hybrid Gateway with Redis Sentinel

## Deploy Redis with Sentinel

Before installing the Gravitee Hybrid Gateway, a Redis instance with Sentinel for high availability must be running in your Kubernetes cluster. This setup ensures that the gateway's rate-limiting capabilities remain functional even if the primary Redis node fails.&#x20;

The following manifest will create a Redis master, three Sentinel replicas to monitor it, and the necessary service for the gateway to discover the Sentinels.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: gravitee-apim
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-config
  namespace: gravitee-apim
data:
  redis.conf: |
    dir /data
    port 6379
    bind 0.0.0.0
    appendonly yes
    protected-mode no
    requirepass myredispassword
    masterauth myredispassword
  sentinel.conf: |
    port 26379
    bind 0.0.0.0
    sentinel monitor mymaster redis-master 6379 2
    sentinel auth-pass mymaster myredispassword
    sentinel down-after-milliseconds mymaster 10000
    sentinel parallel-syncs mymaster 1
    sentinel failover-timeout mymaster 180000
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-master
  namespace: gravitee-apim
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis-master
  template:
    metadata:
      labels:
        app: redis-master
    spec:
      containers:
      - name: redis
        image: redis:7.2.0
        ports:
        - containerPort: 6379
        volumeMounts:
        - name: config
          mountPath: /usr/local/etc/redis/redis.conf
          subPath: redis.conf
        command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
      volumes:
      - name: config
        configMap:
          name: redis-config
---
apiVersion: v1
kind: Service
metadata:
  name: redis-master
  namespace: gravitee-apim
spec:
  selector:
    app: redis-master
  ports:
  - port: 6379
    targetPort: 6379
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-sentinel
  namespace: gravitee-apim
spec:
  replicas: 3
  selector:
    matchLabels:
      app: redis-sentinel
  template:
    metadata:
      labels:
        app: redis-sentinel
    spec:
      containers:
      - name: sentinel
        image: redis:7.2.0
        ports:
        - containerPort: 26379
        volumeMounts:
        - name: config
          mountPath: /usr/local/etc/redis/sentinel.conf
          subPath: sentinel.conf
        command: ["redis-sentinel", "/usr/local/etc/redis/sentinel.conf"]
      volumes:
      - name: config
        configMap:
          name: redis-config
---
apiVersion: v1
kind: Service
metadata:
  name: gravitee-apim-redis-headless
  namespace: gravitee-apim
spec:
  clusterIP: None
  selector:
    app: redis-sentinel
  ports:
  - port: 26379
    targetPort: 26379
```

Make the following modifications to the `yaml` file:&#x20;

* Replace all instances of `<redis_password>` (shown as `myredispassword` in the file) with a secure password for your Redis instance.&#x20;
* Replace all instances of `<redis_master_name>` (shown as `mymaster` in the file) with the desired name for your Redis master group.
* Apply this configuration to your cluster using `kubectl apply -f <filename>.yaml`.



## Configure the Gravitee Hybrid Gateway&#x20;

This `values.yaml` file configures the Gravitee Hybrid Gateway Helm chart. It is used to connect to the Redis Sentinel service for rate limiting and to download custom plugins from an internal S3 bucket, which is used for environments without internet access.

To configure the Gravitee hybrid gateway with custom plugins we support, copy and paste the following configuration:&#x20;

```yaml
  #This is the license key provided in your Gravitee Cloud account
  license:
      key: "LICENSE KEY"

  # The following components are disabled for a hybrid gateway installation
  api:
      enabled: false
  portal:
      enabled: false
  ui:
      enabled: false
  alerts:
      enabled: false
  es:
      enabled: false

  gateway:
      replicaCount: 1
      image:
          repository: graviteeio/apim-gateway
          tag: 4.9.0
          pullPolicy: IfNotPresent
      autoscaling:
          enabled: false
      podAnnotations:
          prometheus.io/path: /_node/metrics/prometheus
          prometheus.io/port: "18082"
          prometheus.io/scrape: "true"

      # Custom plugins with correct versions from pom.xml
      additionalPlugins:
        # Authentication & Security
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-policy-oauth2-4.0.1.zip"
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-policy-jwt-6.2.0.zip"
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-policy-basic-authentication-1.6.0.zip"
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-policy-apikey-5.1.0.zip"
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-policy-mtls-1.0.0.zip"

        # Request/Response Transformation
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-policy-transformheaders-4.1.2.zip"
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-policy-json-to-json-3.0.1.zip"
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-policy-xml-json-2.0.1.zip"
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-policy-assign-content-2.0.1.zip"
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-policy-assign-attributes-3.0.1.zip"

        # Traffic Management & Resilience
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-policy-ratelimit-3.0.0.zip"
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-policy-circuit-breaker-1.1.5.zip"
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-policy-retry-3.0.1.zip"
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-policy-cache-2.0.7.zip"

        # Integration & Connectivity
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-policy-aws-lambda-3.0.0.zip"
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-policy-callout-http-5.0.0.zip"
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-connector-http-5.0.5.zip"

        # Resources
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-resource-cache-redis-4.0.1.zip"
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-resource-oauth2-provider-generic-4.0.3.zip"
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-resource-auth-provider-ldap-2.0.0.zip"

        # Validation & Security
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-policy-json-validation-2.0.3.zip"
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-policy-request-validation-1.15.1.zip"
        - "https://internal-s3.company.com/gravitee-plugins/gravitee-policy-ipfiltering-1.19.1.zip"

      env:
          - name: gravitee_cloud_token
            value: "CLOUD TOKEN"

      services:
          metrics:
              enabled: true
              prometheus:
                  enabled: true
          core:
              http:
                  enabled: true
          sync:
              kubernetes:
                  enabled: false
          bridge:
              enabled: false

      service:
          type: LoadBalancer
          externalPort: 8082

      ingress:
          enabled: false

      resources:
          limits:
              cpu: 500m
              memory: 1024Mi
          requests:
              cpu: 200m
              memory: 512Mi

      deployment:
          revisionHistoryLimit: 1
          strategy:
              type: RollingUpdate
              rollingUpdate:
                  maxUnavailable: 0

      reporters:
          file:
              enabled: false

      terminationGracePeriod: 50
      gracefulShutdown:
          delay: 20
          unit: SECONDS

      # Rate limiting configuration using Redis with Sentinel
      ratelimit:
          type: redis
          redis:
              password: "myredispassword"
              sentinel:
                  master: "mymaster"
                  nodes:
                    - host: "gravitee-apim-redis-headless.gravitee-apim.svc.cluster.local"
                      port: 26379
```

{% hint style="info" %}
* `gateway.ratelimit`: This section is configured to use Redis in `sentinel` mode. The `host` value points to the headless Kubernetes service created in the previous step.
* `gateway.additionalPlugins`: This list contains URLs pointing to your internally-hosted plugin zip files. The gateway will download and install these plugins upon starting. Ensure the gateway pods have network access to these URLs.
{% endhint %}

Make the following modifications to your `values.yaml` file:&#x20;

* Replace `LICENSE KEY` with your Gravitee License Key.
* Replace `CLOUD TOKEN` with the token generated for your hybrid gateway in the Gravitee Cloud UI.
* Ensure the `tag` field (e.g., `4.8.0`) under `gateway.image` matches the version required by your Gravitee Cloud control plane.
* Replace the entire list under `gateway.additionalPlugins` with the actual URLs of your custom plugins hosted on your internal S3 bucket.
* Replace `"myredispassword"` under `gateway.ratelimit.redis.password` with the same `<redis_password>` you set in the Redis manifest.
* Replace `"mymaster"` under `gateway.ratelimit.redis.sentinel.master` with the same `<redis_master_name>` you set in the Redis manifest.

