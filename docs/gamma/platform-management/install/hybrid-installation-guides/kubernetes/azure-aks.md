---
hidden: false
noIndex: false
---
# Install a hybrid Gamma Gateway on Azure AKS
<!-- GAP-STRUCTURAL: Missing procedural content source -->

{% hint style="warning" %}
This installation guide is for development and quick-start purposes only. Don't use it for production environments. For best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Overview

Gravitee Gamma supports hybrid deployments, so you run the data plane in your own infrastructure while Gravitee hosts and manages the control plane. In a hybrid setup, the platform splits into two planes:

* **Control plane**: managed by Gravitee in the cloud. It runs the Management API with Gamma enabled, the Gamma console, the APIM Console, and the Developer Portal, and it handles design, publishing, configuration, analytics, and lifecycle management.
* **Data plane**: deployed and managed by you, close to your backend services. It enforces policies, applies security, and routes traffic.

This guide covers the data plane only. You deploy the Gravitee Gateway and Redis on Azure Kubernetes Service (AKS) with Helm, and you expose the Gateway through an NGINX Ingress Controller and an Azure Load Balancer. The Gateway connects to your Gravitee Cloud control plane with a Cloud Token and a License Key. Redis provides rate limiting at the edge.

## Prerequisites

Before you install the Gateway, complete the following steps:

* Install the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) and configure it with your credentials.
* Install [helm](https://helm.sh/docs/intro/install/) and [kubectl](https://kubernetes.io/docs/tasks/tools/).
* Have a valid [Azure subscription](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account) and a running AKS cluster with outbound Internet connectivity to Gravitee Cloud over HTTPS/443.
* A hostname you control (for example, `gateway.example.com`) that you can point at the ingress controller's external IP.
* Obtain a Gravitee Cloud account. To register for a Gravitee Cloud account, go to the [Gravitee Cloud sign in page](https://cloud.gravitee.io), and then click **Register**.
* Ensure you have access to Gravitee Cloud, with permissions to install new Gateways.
* From your Gravitee Cloud account, obtain your **Cloud Token** and **License Key** for the hybrid Gateway.

## Install the NGINX Ingress Controller

Install the NGINX Ingress Controller with Azure Load Balancer support:

```bash
kubectl create namespace ingress-nginx

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --set controller.service.type=LoadBalancer \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/azure-load-balancer-health-probe-request-path"=/healthz \
  --set controller.service.externalTrafficPolicy=Local \
  --set controller.admissionWebhooks.enabled=false
```

* Get the controller's external IP and point your DNS record (`gateway.example.com`) at it:

  ```bash
  kubectl get service -n ingress-nginx ingress-nginx-controller
  ```

## Install the Gateway

To install the Gateway, complete the following steps:

1. [#create-the-namespace](#create-the-namespace "mention")
2. [#install-redis](#install-redis "mention")
3. [#prepare-the-values-yaml-for-helm](#prepare-the-values-yaml-for-helm "mention")
4. [#install-with-helm](#install-with-helm "mention")

### Create the namespace

```bash
kubectl create namespace gravitee-gamma
```

### Install Redis

Redis is the rate-limit store for the data plane. Install it with Helm. For more information, see the [Bitnami package for Redis](https://artifacthub.io/packages/helm/bitnami/redis).

1. Install Redis using the following command:

   ```bash
   helm install gravitee-gamma-redis oci://registry-1.docker.io/bitnamicharts/redis \
     --version 19.6.4 \
     --namespace gravitee-gamma \
     --set image.repository=bitnamilegacy/redis
   ```
2. From the command output, save the Redis hostname (`gravitee-gamma-redis-master.gravitee-gamma.svc.cluster.local`).
3. Output the Redis password and save it for the next step:

   ```bash
   kubectl get secret --namespace gravitee-gamma gravitee-gamma-redis -o jsonpath="{.data.redis-password}" | base64 -d
   ```

{% hint style="info" %}
Redis requests a persistent volume. If the Redis pod stays `Pending`, ensure your cluster has a default storage class. AKS provides default storage classes (for example, `managed-csi`) out of the box.
{% endhint %}

### Prepare the `values.yaml` for Helm

The Helm values deploy the Gateway only. They disable the control-plane components, point the Gateway at Redis, connect it to Gravitee Cloud, and expose it through an NGINX ingress.

1. Create a `values.yaml` file. Replace `gateway.example.com` with your hostname, and the Cloud Token, License Key, Redis hostname, and Redis password with your values:

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

   gateway:
     replicaCount: 1
     image:
       # We recommend running the same Gateway version as your Gamma control plane, shown in Gravitee Cloud.
       repository: graviteeio/apim-gateway
       tag: 4.12.0
       pullPolicy: IfNotPresent
     autoscaling:
       enabled: false
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
       type: ClusterIP
       externalPort: 80
       internalPort: 8082
       internalPortName: http
     # Expose the Gateway through the NGINX Ingress Controller.
     ingress:
       enabled: true
       pathType: Prefix
       path: /
       ingressClassName: "nginx"
       hosts:
         - gateway.example.com
       annotations:
         nginx.ingress.kubernetes.io/ssl-redirect: "false"
         # ---- Optional: uncomment to use cert-manager for automatic certificates ----
         # cert-manager.io/cluster-issuer: "letsencrypt-prod"
       # ---- Optional: uncomment to enable TLS with a Kubernetes secret ----
       # tls:
       #   - hosts:
       #       - gateway.example.com
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
         host: "<redis-hostname>"
         port: 6379
         password: "<redis-password>"
         ssl: false

   ratelimit:
     type: redis
   ```

2. Save your `values.yaml` file in your working directory.

### Install with Helm

1. Add the Gravitee Helm repository:

   ```bash
   helm repo add graviteeio https://helm.gravitee.io
   helm repo update
   ```
2. Install the chart into the `gravitee-gamma` namespace:

   ```bash
   helm install graviteeio-gamma-gateway graviteeio/apim \
     --namespace gravitee-gamma \
     -f ./values.yaml
   ```
3. Confirm the ingress has the load balancer address:

   ```bash
   kubectl get ingress -n gravitee-gamma
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

A healthy Gateway pod displays the `Running` status with `1/1` ready containers.

1. Query the pod status using the following command:

   ```bash
   kubectl get pods --namespace=gravitee-gamma -l app.kubernetes.io/instance=graviteeio-gamma-gateway
   ```
2. Verify that the Gateway pod is ready and running with no restarts:

   ```sh
   NAME                                              READY   STATUS    RESTARTS   AGE
   graviteeio-gamma-gateway-gateway-6b77d4dd96-8k5l9 1/1     Running   0          6m17s
   ```

### Validate the Gateway URL

1. After DNS resolves to the ingress controller, make a GET request to the Gateway:

   ```bash
   curl http://gateway.example.com/
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

* Create your first MCP server. For more information, see [Create your first MCP server](../../../agent-management/get-started/create-your-first-mcp-server.md).
* Create your first API. For more information, see [Create your first API](../../../api-management/get-started/create-your-first-api.md).
