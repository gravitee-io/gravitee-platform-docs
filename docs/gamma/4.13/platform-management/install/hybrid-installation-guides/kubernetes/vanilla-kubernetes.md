---
hidden: false
noIndex: false
---
# Install a hybrid Gamma Gateway on Vanilla Kubernetes
<!-- GAP-STRUCTURAL: Missing procedural content source -->

{% hint style="warning" %}
This installation guide is for development and quick-start purposes only. Don't use it for production environments. For best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Overview

Gravitee Gamma supports hybrid deployments, so you run the data plane in your own infrastructure while Gravitee hosts and manages the control plane. In a hybrid setup, the platform splits into two planes:

* **Control plane**: managed by Gravitee in the cloud. It runs the Management API with Gamma enabled, the Gamma console, the APIM Console, and the Developer Portal, and it handles design, publishing, configuration, analytics, and lifecycle management.
* **Data plane**: deployed and managed by you, close to your backend services. It enforces policies, applies security, and routes traffic.

This guide covers the data plane only. You deploy the Gravitee Gateway and Redis with Helm, and the Gateway connects to your Gravitee Cloud control plane with a Cloud Token and a License Key. The Management API, the consoles, and the databases stay disabled because they run in Gravitee Cloud. Redis provides rate limiting at the edge, because the data-plane Gateway doesn't reach the control-plane datastore.

## Prerequisites

Before you install the Gateway, complete the following steps:

* Install [helm](https://helm.sh/docs/intro/install/).
* Install [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl).
* Ensure you have access to the self-hosted Kubernetes cluster where you want to install the Gateway.
* Ensure the cluster has outbound Internet connectivity to Gravitee Cloud over HTTPS/443.
* Obtain a Gravitee Cloud account. To register for a Gravitee Cloud account, go to the [Gravitee Cloud sign in page](https://cloud.gravitee.io), and then click **Register**.
* Ensure you have access to Gravitee Cloud, with permissions to install new Gateways.
* From your Gravitee Cloud account, obtain your **Cloud Token** and **License Key** for the hybrid Gateway.

## Install the Gateway

To install the Gateway, complete the following steps:

1. [#install-redis](#install-redis "mention")
2. [#prepare-the-values-yaml-for-helm](#prepare-the-values-yaml-for-helm "mention")
3. [#install-with-helm](#install-with-helm "mention")

### Install Redis

Redis is the rate-limit store for the data plane. Install it into the cluster with Helm. For more information, see the [Bitnami package for Redis](https://artifacthub.io/packages/helm/bitnami/redis).

1. Install Redis with Helm using the following command, which also creates the `gravitee-gamma` namespace:

   ```bash
   helm install gravitee-gamma-redis oci://registry-1.docker.io/bitnamicharts/redis \
     --version 19.6.4 \
     --create-namespace \
     --namespace gravitee-gamma \
     --set image.repository=bitnamilegacy/redis
   ```

2. From the command output, save the Redis hostname. The following sample output lists `gravitee-gamma-redis-master.gravitee-gamma.svc.cluster.local` as the Redis hostname:

   ```sh
   Redis can be accessed on the following DNS names from within your cluster:

       gravitee-gamma-redis-master.gravitee-gamma.svc.cluster.local for read/write operations (port 6379)
       gravitee-gamma-redis-replicas.gravitee-gamma.svc.cluster.local for read-only operations (port 6379)
   ```

3. Output the Redis password and save it for the next step:

   ```bash
   kubectl get secret --namespace gravitee-gamma gravitee-gamma-redis -o jsonpath="{.data.redis-password}" | base64 -d
   ```

#### Verification

* Confirm the Redis pods report `Running` using the following command:

  ```bash
  kubectl get pods -n gravitee-gamma -l app.kubernetes.io/instance=gravitee-gamma-redis
  ```

### Prepare the `values.yaml` for Helm

The Helm values deploy the Gateway only. They disable the control-plane components, point the Gateway at Redis, and connect it to Gravitee Cloud.

1. Create a `values.yaml` file in your working directory, and then copy the following configuration into it:

   {% code title="values.yaml" %}

   ```yaml
   # The License Key from your Gravitee Cloud account
   license:
     key: "<license-key>"

   # The control-plane components run in Gravitee Cloud, so they stay disabled.
   api:
     enabled: false
   portal:
     enabled: false
   ui:
     enabled: false
   gammaUi:
     enabled: false
   alerts:
     enabled: false
   es:
     enabled: false

   # Turn on Gamma in the Gateway (required for AuthZ policy/PDP sync)
   gamma:
     enabled: true

   gateway:
     replicaCount: 1
     image:
       # We recommend running the same Gateway version as your Gamma control plane, shown in Gravitee Cloud.
       repository: graviteeio/apim-gateway
       tag: "4.12"
       pullPolicy: IfNotPresent
     autoscaling:
       enabled: false
     podAnnotations:
       prometheus.io/path: /_node/metrics/prometheus
       prometheus.io/port: "18082"
       prometheus.io/scrape: "true"
     # The Cloud Token registers the Gateway with your Gravitee Cloud control plane.
     env:
       - name: gravitee_cloud_token
         value: "<cloud-token>"
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
     ratelimit:
       redis:
         host: "<redis-hostname>"
         port: 6379
         password: "<redis-password>"
         ssl: false

   ratelimit:
     type: redis
   ```

   {% endcode %}

2. Make the following modifications to your `values.yaml` file:
   * Replace `<license-key>` with your License Key.
   * Replace `<cloud-token>` with your Cloud Token.
   * Replace `<redis-hostname>` with the Redis hostname you saved.
   * Replace `<redis-password>` with the Redis password you saved.

3. Save your `values.yaml` file in your working directory.

<details>

<summary>Explanations of key <code>values.yaml</code> settings</summary>

**Disabled control-plane components**

`api`, `portal`, `ui`, `gammaUi`, `alerts`, and `es` are disabled because the Management API, the consoles, the Gamma console, and the analytics database run in Gravitee Cloud. A hybrid install deploys the Gateway only.

**Turn on Gamma**

`gamma.enabled: true` turns on Gamma in the Gateway. It's required to sync Authorization Management (AuthZ) policies to the Gateway's policy decision point (PDP).

**Gravitee Cloud connection**

`license.key` activates the Gateway, and `gravitee_cloud_token` registers it with your Gravitee Cloud control plane. The Gateway pulls its API definitions from the control plane.

**Service configuration**

The `LoadBalancer` type with `loadBalancerIP` set to `127.0.0.1` creates a local endpoint at `localhost:8082`, which suits a test or development environment. For production, use an external load balancer, an ingress controller, or service mesh integration.

</details>

### Install with Helm

1. From your working directory, add the Gravitee Helm chart repository:

   ```bash
   helm repo add graviteeio https://helm.gravitee.io
   helm repo update
   ```

2. Install the chart with your `values.yaml` file into the `gravitee-gamma` namespace:

   ```bash
   helm install graviteeio-gamma-gateway graviteeio/apim \
     --namespace gravitee-gamma \
     -f ./values.yaml
   ```

{% hint style="info" %}
To uninstall the hybrid Gateway, use the following command:

```bash
helm uninstall graviteeio-gamma-gateway --namespace gravitee-gamma
```
{% endhint %}

## Verification

To verify that your Gateway is up and connected, complete the following steps:

1. [#ensure-the-gateway-registers-in-gravitee-cloud](#ensure-the-gateway-registers-in-gravitee-cloud "mention")
2. [#validate-the-pods](#validate-the-pods "mention")
3. [#validate-the-gateway-url](#validate-the-gateway-url "mention")

### Ensure the Gateway registers in Gravitee Cloud

* Sign in to [Gravitee Cloud](https://cloud.gravitee.io/). From the **Dashboard**, open the **Gateways** section. Your new hybrid Gateway appears here.

  
### Validate the pods

A healthy Gateway pod displays the `Running` status with `1/1` ready containers. The pod startup process includes license validation, Cloud Token authentication, and Redis connectivity verification.

1. Query the pod status using the following command:

   ```bash
   kubectl get pods --namespace=gravitee-gamma -l app.kubernetes.io/instance=graviteeio-gamma-gateway
   ```

2. Verify that the Gateway pod is ready and running with no restarts:

   ```sh
   NAME                                              READY   STATUS    RESTARTS   AGE
   graviteeio-gamma-gateway-gateway-6b77d4dd96-8k5l9 1/1     Running   0          6m17s
   ```

3. To review the Gateway logs, use the following command. Replace `<pod-name>` with your pod name:

   ```bash
   kubectl logs --namespace=gravitee-gamma <pod-name>
   ```

### Validate the Gateway URL

This guide creates a `LoadBalancer` service that exposes the Gateway on `127.0.0.1:8082`.

1. Make a GET request to the Gateway:

   ```bash
   curl http://localhost:8082/
   ```

2. Confirm that the Gateway replies with the following message, which informs you that no API is deployed yet for this URL:

   ```sh
   No context-path matches the request URI.
   ```

{% hint style="success" %}
You can now create and deploy APIs to your hybrid Gateway from the Gamma control plane.
{% endhint %}

## Proxy configuration

To route Gateway traffic through a corporate proxy (for example, for backend API calls or JWKS retrieval from external identity providers like Microsoft Entra ID), add the following `gravitee_system_proxy_*` environment variables to the `gateway.env` section of your `values.yaml`:

```yaml
gateway:
  env:
    - name: gravitee_system_proxy_enabled
      value: "true"
    - name: gravitee_system_proxy_type
      value: "HTTP"
    - name: gravitee_system_proxy_host
      value: "<proxy-host>"
    - name: gravitee_system_proxy_port
      value: "<proxy-port>"
    - name: gravitee_system_proxy_https_host
      value: "<proxy-host>"
    - name: gravitee_system_proxy_https_port
      value: "<proxy-port>"
```

## Next steps

* Create your first MCP server. For more information, see [Create your first MCP server](../../../../agent-management/get-started/create-your-first-mcp-server.md).
* Create your first API. For more information, see [Create your first API](../../../../api-management/get-started/create-your-first-api.md).

{% hint style="warning" %}
To access your Gateway from outside of your Kubernetes cluster, you must implement a load balancer or ingress.
{% endhint %}
