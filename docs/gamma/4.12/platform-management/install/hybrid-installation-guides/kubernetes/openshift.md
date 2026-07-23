---
hidden: false
noIndex: false
---
# Install a hybrid Gamma Gateway on OpenShift
<!-- GAP-STRUCTURAL: Missing procedural content source -->

{% hint style="warning" %}
This installation guide is for development and quick-start purposes only. Don't use it for production environments. For best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Overview

Gravitee Gamma supports hybrid deployments, so you run the data plane in your own infrastructure while Gravitee hosts and manages the control plane. In a hybrid setup, the platform splits into two planes:

* **Control plane**: managed by Gravitee in the cloud. It runs the Management API with Gamma enabled, the Gamma console, the APIM Console, and the Developer Portal, and it handles design, publishing, configuration, analytics, and lifecycle management.
* **Data plane**: deployed and managed by you, close to your backend services. It enforces policies, applies security, and routes traffic.

This guide covers the data plane only. You deploy the Gravitee Gateway and Redis on OpenShift with Helm. OpenShift creates a Route from the Gateway ingress definition, with edge TLS termination. The Gateway connects to your Gravitee Cloud control plane with a Cloud Token and a License Key. Redis provides rate limiting at the edge.

## Prerequisites

Before you install the Gateway, complete the following steps:

* The Gravitee APIM Helm chart is compatible with OpenShift 3.10 and later.
* Install [oc or kubectl](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html).
* Install [helm](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/building_applications/working-with-helm-charts).
* Have access to a running OpenShift cluster with outbound Internet connectivity to Gravitee Cloud over HTTPS/443, and a project (namespace).
* A hostname served by the OpenShift router (for example, `gateway.apps.<cluster-domain>`). This guide uses `gateway.example.com` as a placeholder.
* Obtain a Gravitee Cloud account. To register for a Gravitee Cloud account, go to the [Gravitee Cloud sign in page](https://cloud.gravitee.io), and then click **Register**.
* Ensure you have access to Gravitee Cloud, with permissions to install new Gateways.
* From your Gravitee Cloud account, obtain your **Cloud Token** and **License Key** for the hybrid Gateway.

## Install the Gateway

To install the Gateway, complete the following steps:

1. [#create-the-project](#create-the-project "mention")
2. [#install-redis](#install-redis "mention")
3. [#prepare-the-values-yaml-for-helm](#prepare-the-values-yaml-for-helm "mention")
4. [#install-the-gravitee-helm-chart](#install-the-gravitee-helm-chart "mention")

### Create the project

```bash
oc new-project gravitee-gamma
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

### Prepare the `values.yaml` for Helm

The Helm values deploy the Gateway only. They set `openshift.enabled: true`, set `runAsUser: null` so OpenShift assigns the security context, disable the control-plane components, point the Gateway at Redis, and connect it to Gravitee Cloud. The Gateway ingress becomes an edge-terminated Route.

1. Create a `values.yaml` file. Replace `gateway.example.com` with your hostname, and the Cloud Token, License Key, Redis hostname, and Redis password with your values:

   ```yaml
   apim:
     managedServiceAccount: true

   openshift:
     enabled: true

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
     # OpenShift converts this ingress into an edge-terminated Route on the host.
     ingress:
       enabled: true
       pathType: Prefix
       path: /
       hosts:
         - gateway.example.com
       annotations:
         route.openshift.io/termination: edge
     deployment:
       revisionHistoryLimit: 1
       strategy:
         type: RollingUpdate
         rollingUpdate:
           maxUnavailable: 0
       securityContext:
         runAsUser: null
         runAsGroup: null
         allowPrivilegeEscalation: false
         capabilities:
           drop: ["ALL"]
         seccompProfile:
           type: RuntimeDefault
     resources:
       limits:
         cpu: 500m
         memory: 1024Mi
       requests:
         cpu: 200m
         memory: 512Mi
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

{% hint style="info" %}
Setting `runAsUser` to `null` lets OpenShift assign the correct user ID from the project's security context constraints when it deploys the chart.
{% endhint %}

### Install the Gravitee Helm chart

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
3. Confirm OpenShift created the Route:

   ```bash
   oc get routes -n gravitee-gamma
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
   oc get pods -n gravitee-gamma -l app.kubernetes.io/instance=graviteeio-gamma-gateway
   ```
2. Verify that the Gateway pod is ready and running with no restarts:

   ```sh
   NAME                                              READY   STATUS    RESTARTS   AGE
   graviteeio-gamma-gateway-gateway-6b77d4dd96-8k5l9 1/1     Running   0          6m17s
   ```

### Validate the Gateway URL

1. After your DNS records resolve to the OpenShift router, make a GET request to the Gateway:

   ```bash
   curl https://gateway.example.com/
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
