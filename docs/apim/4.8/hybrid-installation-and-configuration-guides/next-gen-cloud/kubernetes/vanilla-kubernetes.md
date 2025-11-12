# Vanilla Kubernetes

## Overview

This guide explains how to install a Hybrid Gateway and connect it to Gravitee Next-Gen Cloud using Kubernetes.

{% include "../../../../4.6/.gitbook/includes/installation-guide-note (1).md" %}

## Prerequisites

Before you install a Hybrid Gateway, complete the following steps:

* Install [helm](https://helm.sh/docs/intro/install/).
* Install [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl).
* Ensure you have access to [Gravitee Cloud](https://cloud.gravitee.io/), with permissions to install new Gateways.
* Ensure you have access to the self-hosted Kubernetes cluster where you want to install the Gateway.
* Ensure the self-hosted target environment has outbound Internet connectivity to Gravitee Cloud using HTTPS/443.
* Complete the steps in [#prepare-your-installation](../#prepare-your-installation "mention").

## Install the Gateway

To install the Gravitee Gateway, complete the following steps:

1. [#install-redis](vanilla-kubernetes.md#install-redis "mention")
2. [#prepare-values.yaml-for-helm](vanilla-kubernetes.md#prepare-values.yaml-for-helm "mention")
3. [#ingress-configuration-with-custom-domain-and-kubernetes-secrets](vanilla-kubernetes.md#ingress-configuration-with-custom-domain-and-kubernetes-secrets "mention")
4. [#install-with-helm](vanilla-kubernetes.md#install-with-helm "mention")

### Install Redis

To support caching and rate-limiting, you must install Redis into your Kubernetes cluster. For more information, see [Bitnami package for Redis®](https://artifacthub.io/packages/helm/bitnami/redis).

1.  Install Redis with Helm using the following command, which also creates a new `gravitee-apim` namespace:

    ```bash
    helm install gravitee-apim-redis oci://registry-1.docker.io/bitnamicharts/redis \
      --version 19.6.4 \
      --create-namespace \
      --namespace gravitee-apim \
      --set image.repository=bitnamilegacy/redis
    ```
2.  Extract the Redis hostname from the command output and save it for future use. The following sample output lists `gravitee-apim-redis-master.gravitee-apim.svc.cluster.local` as the Redis hostname:

    ```sh
    Pulled: registry-1.docker.io/bitnamicharts/redis:19.6.4
    Digest: sha256:[hash_will_vary]
    NAME: gravitee-apim-redis
    LAST DEPLOYED: DDD MMM DD HH:MM:SS YYYY
    NAMESPACE: gravitee-apim
    STATUS: deployed
    REVISION: 1
    TEST SUITE: None
    NOTES:
    CHART NAME: redis
    CHART VERSION: 19.6.4
    APP VERSION: 7.2.5

    ** Please be patient while the chart is being deployed **

    Redis can be accessed on the following DNS names from within your cluster:

        gravitee-apim-redis-master.gravitee-apim.svc.cluster.local for read/write operations (port 6379)
        gravitee-apim-redis-replicas.gravitee-apim.svc.cluster.local for read-only operations (port 6379)

    To get your password run:
        export REDIS_PASSWORD=$(kubectl get secret --namespace gravitee-apim gravitee-apim-redis -o jsonpath="{.data.redis-password}" | base64 -d)
    ```
3.  Use the following command to output the Redis password. Save this password for future use.

    ```bash
    kubectl get secret --namespace gravitee-apim gravitee-apim-redis -o jsonpath="{.data.redis-password}" | base64 -d

    ```
4.  To verify that your Redis deployment succeeded, check pod status using the following command:

    ```bash
    kubectl get pods -n gravitee-apim -l app.kubernetes.io/instance=gravitee-apim-redis
    ```

    The command generates the following output:

    ```sh
    NAME                            READY   STATUS    RESTARTS   AGE
    gravitee-apim-redis-master-0    1/1     Running   0          2m
    gravitee-apim-redis-replicas-0  1/1     Running   0          2m
    gravitee-apim-redis-replicas-1  1/1     Running   0          2m
    gravitee-apim-redis-replicas-2  1/1     Running   0          2m
    ```

### Prepare `values.yaml` for Helm

To prepare your Gravitee `values.yaml` file for Helm, complete the following steps:

1.  Copy the following Gravitee `values.yaml` file. This is the base configuration for your new hybrid Gateway.

    \{% code title="values.yaml" %\}

    ```yaml
    #This is the license key provided in your Gravitee Cloud account 
    #example: Ic5OXgAAACAAAAACAAAADAAAAAhhbGVydC1lbmdpbmVpbmNsdWRlZAAAABsAAAACAAAABwAAAAhjb21wYW55R3Jhdml0ZWUAAAAxAAAAAgAAAAUAAAAgZW1haWxwbGF0Zm9ybS10ZWFtQGdyYXZpdGVlc291cmNlLmNvbQAAABoAAAALAAAACmV4cGlyeURhdGUAAAGhUXU7/wAAACAAAAACAAAACAAAAAxmZWF0dXJlc2FsZXJ0LWVuZ2luZQAAACEAAAAMAAAACWxpY2Vuc2VJZJTWw5qIQT4bEYqYFx9wSH4AAAEcAAAAAQAAABAAAAEAbGljZW5zZVNpZ25hdHVyZULCHNcIqMuFwEMkSCgE4Q/42YSVluW/vvMtaHZWJ5Xoh3rsWEjCMg8Ku2cTKuSP7FzR/b8GVedDJqxf+o2n8B/LV+WwzZjOAi09EBfLmTLOzzXFNp1KRDk3G4rrKznJ1Kqz9EXjyNAiT/c7en3om6Lx0A4BscZtu6k6i1pAnfHhotJkHMIdNkDqSU4fkyAH6FS+NYcLEcudaeeRr2Th/Dvyn0py7xOUNicgXdBjEXJXMF2vxyNkm0kML4ADG12++dZyG2kgGYg5+A8UdABGxCvIfNsl9uVuP2F5ACr8Uc73HytKpIaZqz71RMxQDuJtRzmkkGxHajJJeZWQZXtLdBoAAAARAAAAAgAAAAUAAAAAcGFja3MAAAAiAAAAAgAAAA8AAAAHc2lnbmF0dXJhfgzanZXN0U0hBLTI1NgAAABgAAAACAAAABAAAAAh0aWVydW5pdmVyc2U=
    license:
        key: "<license_key>"
    #This section controls the Management API component deployment of Gravitee. 
    #It is disabled for a hybrid gateway installation
    api:
        enabled: false
    #This section controls the Developer Portal API component deployment of Gravitee. 
    #It is disabled for a hybrid gateway installation
    portal:
        enabled: false
    #This section controls the API Management Console component deployment of Gravitee. 
    #It is disabled for a hybrid gateway installation
    ui:
        enabled: false
    #This section controls the Alert Engine component deployment of Gravitee. 
    #It is disabled for a hybrid gateway installation
    alerts:
        enabled: false
    #This section controls the Analytics Database component deployment of Gravitee based on ElasticSearch. 
    #It is disabled for a hybrid gateway installation
    es:
        enabled: false
        
    #This section has multiple parameters to configure the API Gateway deployment  
    gateway:
        replicaCount: 1 #number of replicas of the pod
        image:
            repository: graviteeio/apim-gateway
            tag: <add_the_gateway_tag> #The gateway version to install. It has to align with the control plane of your Gravitee Cloud
            pullPolicy: IfNotPresent
        autoscaling:
            enabled: false
        podAnnotations:
            prometheus.io/path: /_node/metrics/prometheus
            prometheus.io/port: "18082"
            prometheus.io/scrape: "true"
        #Sets environment variables.  
        env:
            #Gravitee Cloud Token. This is the value gathered in your Gravitee Cloud Account when you install a new Hybrid Gateway.
            - name: gravitee_cloud_token
              value: "<cloud_token>"
        
        #Configure the API Gateway internal API. 
        services:
            #The following sections enables the exposure of metrics to Prometheus. 
            metrics:
                enabled: true
                prometheus:
                    enabled: true

            #This enables the Gravitee APIM Gateway internal API for monitoring and retrieving technical information about the component.
            core:
                http:
                    enabled: true
            sync:
                kubernetes:
                    enabled: false
            #disables bridge mode. unnecessary for a hybrid gateway.
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
        #Reporter configuration section.
        #no additional reporter enabled for the hybrid gateway outside of the default Cloud Gateway reporter
        reporters:
            file:
                enabled: false
        terminationGracePeriod: 50
        gracefulShutdown:
            delay: 20
            unit: SECONDS
        ratelimit:
            redis:
                host: "<redis_hostname>"
                port: 6379
                password: "<redis_password>"
                ssl: false
            
    ratelimit:
        type: redis
    ```

    \{% endcode %\}
2. Make the following modifications to your `values.yaml` file:
   * Replace `<cloud_token>` with your Cloud Token.
   * Replace `<license_key>` with your License Key.
   * Replace `<redis_hostname>` with your extracted Redis hostname.
   * Replace `<redis_password>` with your extracted Redis password.
   *   Set the `tag` field in the `image` section to the value displayed in the Overview section of your Gravitee Cloud Dashboard. \\

       <figure><img src="../../../.gitbook/assets/gateway-cloud-version.png" alt=""><figcaption></figcaption></figure>

       \{% hint style="info" %\} The `tag` field specifies the version of your Gravitee Gateway. Your Gateway version must match your Gravitee Cloud Control Plane version to ensure compatibility between your hybrid Gateway and the Cloud Management platform. \{% endhint %\}
3. Save your Gravitee `values.yaml` file in your working directory.

<details>

<summary>Explanations of key predefined <code>values.yaml</code> parameter settings</summary>

**Service configuration**

The `LoadBalancer` type with `loadBalancerIP` set to `127.0.0.1` creates a local endpoint accessible at `localhost:8082`. This environment is suitable for test or development. You can modify this configuration for production deployments that use external load balancers, ingress controllers, or service mesh integration.

**Resource allocation**

The configured limits prevent excessive cluster resource consumption, but ensure adequate performance for API processing. These values support moderate traffic volumes and can be adjusted based on your expected load patterns and available cluster capacity.

**Deployment strategy**

The `RollingUpdate` strategy with `maxUnavailable` set to 0 ensures zero-downtime updates during configuration changes or version upgrades.

</details>

### Ingress Configuration with Custom Domain and Kubernetes Secrets

To configure Ingress and TLS rules, Copy the following `values.yaml` file to deploy the gateway and expose it via an Ingress controller. Fill in the required [placeholders](vanilla-kubernetes.md#prepare-values.yaml-for-helm) like your license key and domain. To enable HTTPS, uncomment and configure the optional TLS section.

```yaml
# Hybrid Gateway values.yaml with Ingress and Optional TLS
license:
  key: "<license_key>"

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
    tag: <add_the_gateway_tag>
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

  # Service configured to expose the gateway inside the cluster for the Ingress controller.
  service:
    type: ClusterIP
    externalPort: 80
    internalPort: 8082
    internalPortName: http

  # --- Ingress Configuration ---
  ingress:
    enabled: true
    pathType: Prefix
    path: /
    ingressClassName: "nginx"
    hosts:
      - gateway.customer.com
    annotations:
      nginx.ingress.kubernetes.io/ssl-redirect: "true"

      # ---- Optional: Uncomment to use cert-manager for automatic certificates ----
      # cert-manager.io/cluster-issuer: "letsencrypt-prod"

    # ---- Optional: Uncomment to enable TLS with a Kubernetes secret ----
    # tls:
    #   - hosts:
    #       - gateway.customer.com
    #     secretName: gravitee-gateway-tls

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
  ratelimit:
    redis:
      host: "<redis_hostname>"
      port: 6379
      password: "<redis_password>"
      ssl: false

ratelimit:
  type: redis
```

### Install with Helm

To install your Gravitee Gateway with Helm, complete the following steps:

1.  From your working directory, add the Gravitee Helm chart repository to your Kubernetes environment using the following command:

    ```bash
    helm repo add graviteeio https://helm.gravitee.io
    ```
2.  Install the Helm chart with the Gravitee `values.yaml` file into a dedicated namespace using the following command:

    ```bash
    helm install graviteeio-apim-gateway graviteeio/apim --namespace gravitee-apim -f ./values.yaml
    ```
3.  Verify the installation was successful. The command output should be similar to the following:

    ```sh
    NAME: graviteeio-apim-gateway
    LAST DEPLOYED: DDD MMM DD HH:MM:SS YYYY
    NAMESPACE: gravitee-apim
    STATUS: deployed
    REVISION: 1
    TEST SUITE: None
    NOTES:
    1. Watch all containers come up.
      $ kubectl get pods --namespace=gravitee-apim -l app.kubernetes.io/instance=graviteeio-apim-gateway -w
    ```

{% hint style="info" %}
To uninstall the Gravitee hybrid Gateway, use the following command:

```bash
helm uninstall graviteeio-apim-gateway --namespace gravitee-apim
```
{% endhint %}

## Verification

Your Gateway appears in the Gateways section of your Gravitee Cloud Dashboard.

<figure><img src="../../../.gitbook/assets/gravitee-gateway-cloud-verification (1).png" alt=""><figcaption></figcaption></figure>

To verify that your Gateway is up and running, complete the following steps:

1. [#validate-the-pods](vanilla-kubernetes.md#validate-the-pods "mention")
2. [#validate-the-gateway-logs](vanilla-kubernetes.md#validate-the-gateway-logs "mention")
3. [#validate-the-gateway-url](vanilla-kubernetes.md#validate-the-gateway-url "mention")

### Validate the pods

A healthy Gateway pod displays the `Running` status with `1/1` ready containers and zero or minimal restart counts. The pod startup process includes license validation, Cloud Token authentication, and Redis connectivity verification.

To validate your pods, complete the following steps:

1.  Use the following command to query the pod status:

    ```bash
    kubectl get pods --namespace=gravitee-apim -l app.kubernetes.io/instance=graviteeio-apim-gateway
    ```
2.  Verify that the deployment was successful. The output should show that a Gravitee Gateway is ready and running with no restarts.

    ```sh
    NAME                                               READY   STATUS    RESTARTS   AGE
    graviteeio-apim-gateway-gateway-6b77d4dd96-8k5l9   1/1     Running   0          6m17s
    ```

### Validate the Gateway logs

To validate the Gateway logs, complete the following steps:

1.  List all the pods in your deployment using the following command:

    ```bash
    kubectl get pods --namespace=gravitee-apim -l app.kubernetes.io/instance=graviteeio-apim-gateway
    ```
2.  In the output, navigate to the pod that you want to obtain logs for. For example, `graviteeio-apim-gateway-gateway-6b77d4dd96-8k5l9`.

    ```sh
    NAME                                               READY   STATUS    RESTARTS   AGE
    graviteeio-apim-gateway-gateway-6b77d4dd96-8k5l9   1/1     Running   0          6m17s
    ```
3.  To obtain the logs from a specific pod, use the following command. Replace `<NAME_OF_THE_POD>` with your pod name.

    ```bash
    kubectl logs --namespace=gravitee-apim <NAME_OF_THE_POD>
    ```
4.  Review the log file. The following example output shows the important log entries:

    ```sh
    =========================================================================
      Gravitee.IO Standalone Runtime Bootstrap Environment
      GRAVITEE_HOME: /opt/graviteeio-gateway
      GRAVITEE_OPTS: 
      JAVA: /opt/java/openjdk/bin/java
      JAVA_OPTS:  -Xms256m -Xmx256m -Djava.awt.headless=true -XX:+HeapDumpOnOutOfMemoryError -XX:+DisableExplicitGC -Dfile.encoding=UTF-8
      CLASSPATH: /opt/graviteeio-gateway/lib/gravitee-apim-gateway-standalone-bootstrap-<version>.jar
    =========================================================================
    14:01:39.318 [graviteeio-node] [] INFO  i.g.n.c.spring.SpringBasedContainer - Starting Boot phase.
    ...
    14:01:43.140 [graviteeio-node] [] INFO  i.g.n.license.LicenseLoaderService - License information: 
    	expiryDate: YYYY-MM-DD HH:MM:SS.mmm
    	features: alert-engine
    	tier: universe
    	alert-engine: included
    	company: Gravitee
    	signatureDigest: SHA-256
    	licenseId: [redacted]
    	packs: 
    	email: [redacted]
    	licenseSignature: [redacted]
    14:01:43.215 [graviteeio-node] [] INFO  i.g.common.service.AbstractService - Initializing service io.gravitee.plugin.core.internal.BootPluginEventListener
    14:01:43.338 [graviteeio-node] [] INFO  i.g.p.c.internal.PluginRegistryImpl - Loading plugins from /opt/graviteeio-gateway/plugins
    ...
    14:01:53.322 [graviteeio-node] [] INFO  i.g.node.container.AbstractContainer - Starting Gravitee.io - API Gateway...
    14:01:53.323 [graviteeio-node] [] INFO  i.g.node.container.AbstractNode - Gravitee.io - API Gateway is now starting...
    ...
    14:02:03.816 [graviteeio-node] [] INFO  i.g.node.container.AbstractNode - Gravitee.io - API Gateway id[95cb1eb8-ba65-42ad-8b1e-b8ba65b2adf7] version[4.7.6] pid[1] build[1093365#b33db62e676fad748d3ad09e3cbc139394b6da7a] jvm[Eclipse Adoptium/OpenJDK 64-Bit Server VM/21.0.7+6-LTS] started in 10400 ms.
    ...
    14:02:03.923 [vert.x-eventloop-thread-0] [] INFO  i.g.g.r.s.vertx.HttpProtocolVerticle - HTTP server [http] ready to accept requests on port 8082
    ...
    14:02:04.324 [gio.sync-deployer-0] [] INFO  i.g.g.p.o.m.DefaultOrganizationManager - Register organization ReactableOrganization(definition=Organization{id='[redacted]', name='Organization'}, enabled=true, deployedAt=Sat Oct 19 17:08:22 GMT 2024)
    ```
5.  To verify service configuration, run the following command:

    ```bash
    kubectl get services -n gravitee-apim
    ```

    The output should show TYPE `LoadBalancer` with EXTERNAL-IP `localhost` and PORT `8082`.

    ```bash
    NAME                              TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
    gravitee-apim-redis-headless      ClusterIP      None            <none>        6379/TCP         20m
    gravitee-apim-redis-master        ClusterIP      10.110.172.36   <none>        6379/TCP         20m
    gravitee-apim-redis-replicas      ClusterIP      10.96.207.194   <none>        6379/TCP         20m
    graviteeio-apim-gateway-gateway   LoadBalancer   10.107.188.66   localhost     8082:32738/TCP   5m
    ```

### Validate the Gateway URL

Your Gateway URL is determined by the networking settings you specify in the `service` section of your `values.yaml` file. This guide creates a `LoadBalancer` service that exposes your Gateway on your local machine at IP address 127.0.0.1 and port 8082, which is equivalent to port 8082 of localhost.

To validate the Gateway URL, complete the following steps:

1.  Make a GET request to the URL where you published the Gateway:

    ```bash
    curl http://localhost:8082/ # alternatively, you can use http://127.0.0.1:8082/
    ```
2.  Confirm that the Gateway replies with `No context-path matches the request URI.` This message informs you that an API isn't yet deployed for this URL.

    ```sh
    No context-path matches the request URI.
    ```

{% hint style="success" %}
You can now create and deploy APIs to your Hybrid Gateway.
{% endhint %}

## Next steps

* Access your API Management Console. To access your Console, complete the following steps:
  1. Log in to your [Gravitee Cloud](https://cloud.gravitee.io/).
  2. From the Dashboard, navigate to the Environment where you created your Gateway.
  3. Click on **APIM Console** to open the user interface where you can create and manage your APIs.
* Create your first API. For more information about creating your first API, see [create-and-publish-your-first-api](../../../how-to-guides/create-and-publish-your-first-api/ "mention").
* Add native Kafka capabilities. For more information about adding native Kafka capabilities, see [configure-the-kafka-client-and-gateway.md](../../../kafka-gateway/configure-the-kafka-client-and-gateway.md "mention").

{% hint style="warning" %}
To access your Gravitee Gateway from outside of your Kubernetes cluster, you must implement a load balancer or ingress.
{% endhint %}
