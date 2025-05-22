# Kubernetes

## Prerequisites

* Follow the instructions to [#prepare-your-installation](../#prepare-your-installation "mention").
* You must install the following command line tools:
  * [Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
  * [Helm v3](https://helm.sh/docs/intro/install/)

## Install the Gateway

1.  To set up Helm, add the Gravitee Helm Chart repo using the following command:\


    <pre class="language-bash"><code class="lang-bash"><strong>helm repo add graviteeio https://helm.gravitee.io
    </strong></code></pre>


2.  On your local machine, copy the configuration below into a file called `values.yaml`:

    * Replace `<CONTROL_PLANE_VERSION>` with the version that is in the Environments section of your Gravitee Cloud dashboard.&#x20;
    * Replace `<cloud_token>` with your Cloud token.
    * Replace the `<license_key>` with your license key.



    ```yaml
    gateway:
        replicaCount: 1
        image:
            repository: graviteeio/apim-gateway
            tag: <CONTROL_PLANE_VERSION>
            pullPolicy: IfNotPresent
        autoscaling:
            enabled: false
        podAnnotations:
            prometheus.io/path: /_node/metrics/prometheus
            prometheus.io/port: "18082"
            prometheus.io/scrape: "true"
        env:
            - name: gravitee_cloud_token
              value: "<cloud_token>"
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
            loadBalancerIP: 127.0.0.1
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

    api:
        enabled: false

    ratelimit:
        type: none

    portal:
        enabled: false

    ui:
        enabled: false

    alerts:
        enabled: false

    es:
        enabled: false

    license:
        key: "<license_key>"
    ```


3.  Install the Helm Chart with the `values.yaml` file to a dedicated namespace using the  command below:\


    ```bash
    helm install graviteeio-apim4x graviteeio/apim --create-namespace --namespace gravitee-apim -f ./values.yaml
    ```

## Configure Redis

To enable API rate-limiting, configure your Gateway to use a rate-limiting repository, such as Redis.

To install Redis, use packages available from [Bitnami Helm charts](https://artifacthub.io/packages/helm/bitnami/redis).  The following example `values.yaml` is for a standalone configuration:

{% code title="values.yaml" lineNumbers="true" %}
```yaml
gateway:
  ...
  ratelimit:
    type: redis
  redis:
    host: ${redis_hostname}
    port: ${redis_port_number}
    password: ${redis_password}
    #password: kubernetes://<namespace>/secrets/<my-secret-name>/<my-secret-key>
    download: true
```
{% endcode %}

## Verification

From the Gravitee Cloud Dashboard, you can see your configured Gateway.

<figure><img src="../../../.gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>

To verify that the Gateway is running, make a GET request to the URL on which you have published the Gateway. The output is a default message similar to:

```
No context-path matches the request URI.
```

You can now create and deploy APIs to your hybrid Gateway.
