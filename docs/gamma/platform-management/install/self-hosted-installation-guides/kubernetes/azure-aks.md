---
hidden: false
noIndex: false
---
# Install Gamma on Azure AKS
<!-- GAP-STRUCTURAL: Missing procedural content source -->

{% hint style="warning" %}
This installation guide is for development and quick-start purposes only. Don't use it for production environments. For best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Overview

This guide explains how to deploy a self-hosted Gravitee Gamma platform on Azure Kubernetes Service (AKS) with Helm, fronted by a single NGINX Ingress Controller and an Azure Load Balancer.

You deploy the standard `graviteeio/apim` Helm chart, turn on Gamma with `gamma.enabled`, and add the Gamma console (`gammaUi`). This guide uses the `4.12.0` images, which include the Agent Management module.

Every component is served on **one hostname** through one NGINX ingress: the Gamma console at `/`, and the Management API at `/management`, `/portal`, and `/gamma`. Keeping everything on a single host makes the browser requests same-origin, so the login session cookie is sent and the consoles log in. The whole platform, including the ingress, is defined in a single `values.yaml`.

## Prerequisites

Before you install Gamma, complete the following steps:

* Install the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) and configure it with your credentials.
* Install [helm](https://helm.sh/docs/intro/install/) and [kubectl](https://kubernetes.io/docs/tasks/tools/).
* Have a valid [Azure subscription](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account) and a running AKS cluster.
* A hostname you control (for example, `gamma.example.com`) that you can point at the ingress controller's external IP.
* **(Enterprise Edition only)** To enable Agent Management, you need an enterprise license that includes the `agent-management` pack. To get one, contact your Technical Account Manager. For more information, see [Add your license key](#enterprise-edition-only-add-your-license-key).
* For Gravitee Enterprise Edition deployments, ensure that you have your license key. For more information about license keys, see [Gravitee Platform Pricing](https://www.gravitee.io/pricing).

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

* Get the controller's external IP and point your DNS record (`gamma.example.com`) at it:

  ```bash
  kubectl get service -n ingress-nginx ingress-nginx-controller
  ```

## Install Gamma

To install Gamma, complete the following steps:

1. [#create-the-namespace](#create-the-namespace "mention")
2. [#deploy-mongodb-and-elasticsearch](#deploy-mongodb-and-elasticsearch "mention")
3. [#enterprise-edition-only-add-your-license-key](#enterprise-edition-only-add-your-license-key "mention")
4. [#prepare-the-values-yaml-for-helm](#prepare-the-values-yaml-for-helm "mention")
5. [#install-with-helm](#install-with-helm "mention")

### Create the namespace

```bash
kubectl create namespace gravitee-gamma
```

### Deploy MongoDB and Elasticsearch

1. Install MongoDB:

   ```bash
   helm install gravitee-mongodb oci://registry-1.docker.io/cloudpirates/mongodb \
     --namespace gravitee-gamma --set auth.enabled=false --set persistence.enabled=false \
     --set resources.requests.memory=512Mi --set resources.requests.cpu=250m
   ```
2. Install Elasticsearch:

   ```bash
   helm repo add elastic https://helm.elastic.co
   helm repo update
   helm install elasticsearch elastic/elasticsearch \
     --namespace gravitee-gamma --set persistence.enabled=false --set replicas=1 --set minimumMasterNodes=1
   ```
3. Retrieve the `elastic` user password:

   ```bash
   kubectl get secrets --namespace gravitee-gamma elasticsearch-master-credentials -o jsonpath='{.data.password}' | base64 -d
   ```

### (Enterprise Edition only) Add your license key

Agent Management is an enterprise feature. It only activates with an enterprise license that includes the `agent-management` pack. To get one, contact your Technical Account Manager. Your account manager sends you the license as a `license.key` file. The other modules work without a license.

{% hint style="info" %}
If your license is a base64-encoded text file (for example, `license.base64.txt`), decode it into `license.key` first:

```bash
base64 -d < license.base64.txt > license.key
```

On macOS, use `base64 -D` (capital `D`) if `base64 -d` returns an error.
{% endhint %}

1. Save the `license.key` file your account manager sent you.
2. Create the secret:

   ```bash
   kubectl create secret generic gravitee-license --from-file=license.key=./license.key --namespace gravitee-gamma
   ```
3. Uncomment the license lines under the `api` service in `values.yaml` (in the next step).

### Prepare the `values.yaml` for Helm

The Gamma components run as `ClusterIP` services, and the single NGINX ingress is defined in the chart's `extraObjects`, so the whole platform ships from one `values.yaml`.

1. Create a `values.yaml` file. Replace `gamma.example.com` with your hostname and the Elasticsearch password:

   ```yaml
   # MongoDB Configuration
   mongo:
     uri: mongodb://gravitee-mongodb.gravitee-gamma.svc.cluster.local:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000

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

   management:
     type: mongodb
   ratelimit:
     type: mongodb
   analytics:
     type: elasticsearch

   elasticsearch:
     enabled: false
   mongodb:
     enabled: false

   # Single host for all components
   installation:
     type: standalone
     api:
       url: http://gamma.example.com/management
     standalone:
       gamma-console:
         urls:
           - orgId: DEFAULT
             url: http://gamma.example.com/

   gamma:
     enabled: true

   api:
     enabled: true
     image:
       repository: graviteeio/apim-management-api
       tag: 4.12.0
       pullPolicy: IfNotPresent
     env:
       - name: gravitee_installation_api_url
         value: "http://gamma.example.com/management"
       # CORS - single origin, credentials allowed
       - name: gravitee_http_cors_enabled
         value: "true"
       - name: gravitee_http_cors_allow-origin
         value: "http://gamma.example.com"
       - name: gravitee_http_cors_allow-credentials
         value: "true"
       # Cookie - same-origin. Over plain HTTP, secure must be false.
       # For HTTPS, add a TLS block to the ingress and set secure to "true".
       - name: gravitee_http_cookie_sameSite
         value: "Lax"
       - name: gravitee_http_cookie_secure
         value: "false"
     ingress:
       management:
         enabled: false
       portal:
         enabled: false
       gamma:
         enabled: false
     resources:
       requests:
         memory: "1Gi"
         cpu: "500m"
       limits:
         memory: "2Gi"
         cpu: "1"
     # (Enterprise Edition) Mount the license secret for Agent Management.
     # Create the gravitee-license secret (see "Add your license key"), then uncomment:
     # extraVolumes: |
     #   - name: gravitee-license
     #     secret:
     #       secretName: gravitee-license
     # extraVolumeMounts: |
     #   - name: gravitee-license
     #     mountPath: "/opt/graviteeio-management-api/license/license.key"
     #     subPath: license.key
     #     readOnly: true

   gateway:
     enabled: true
     image:
       repository: graviteeio/apim-gateway
       tag: 4.12.0
       pullPolicy: IfNotPresent
     ingress:
       enabled: false

   ui:
     enabled: true
     image:
       repository: graviteeio/apim-management-ui
       tag: 4.12.0
       pullPolicy: IfNotPresent
     ingress:
       enabled: false

   portal:
     enabled: true
     defaultPortal: "classic"
     image:
       repository: graviteeio/apim-portal-ui
       tag: 4.12.0
       pullPolicy: IfNotPresent
     env:
       - name: PORTAL_BASE_HREF
         value: /dev/
     ingress:
       enabled: false

   gammaUi:
     enabled: true
     image:
       repository: graviteeio/gamma-ui
       tag: 4.12.0
       pullPolicy: IfNotPresent
     app:
       gammaBaseURL: "http://gamma.example.com/gamma"
     env:
       - name: GAMMA_CONSOLE_BASE_HREF
         value: /
     ingress:
       enabled: false

   ingress:
     enabled: false

   # One NGINX ingress for all paths on the single host, shipped with the release.
   # NGINX matches the longest prefix first, so the specific API paths win over the / catch-all (the console).
   extraObjects:
     - apiVersion: networking.k8s.io/v1
       kind: Ingress
       metadata:
         name: gamma
         namespace: gravitee-gamma
         annotations:
           nginx.ingress.kubernetes.io/proxy-body-size: "50m"
       spec:
         ingressClassName: nginx
         rules:
           - host: gamma.example.com
             http:
               paths:
                 - path: /gamma
                   pathType: Prefix
                   backend:
                     service:
                       name: gamma-apim-api
                       port:
                         number: 83
                 - path: /management
                   pathType: Prefix
                   backend:
                     service:
                       name: gamma-apim-api
                       port:
                         number: 83
                 - path: /portal
                   pathType: Prefix
                   backend:
                     service:
                       name: gamma-apim-api
                       port:
                         number: 83
                 - path: /console
                   pathType: Prefix
                   backend:
                     service:
                       name: gamma-apim-ui
                       port:
                         number: 8002
                 - path: /dev
                   pathType: Prefix
                   backend:
                     service:
                       name: gamma-apim-portal
                       port:
                         number: 8003
                 - path: /
                   pathType: Prefix
                   backend:
                     service:
                       name: gamma-apim-gamma
                       port:
                         number: 8005
   ```
2. Replace `[ELASTIC PASSWORD FROM ES INSTALLATION]` with the password you retrieved.

{% hint style="warning" %}
**Gamma uses two Helm flags**

* `gamma.enabled` is the global master switch (default `false`). It turns Gamma on in the Management API and unlocks the Gamma ingress and the Gamma console deployment.
* `gammaUi.enabled` is the per-component switch for the Gamma console (default `false`). It deploys the `graviteeio/gamma-ui` console.

When `gamma.enabled` is `true`, you choose which components to deploy:

* `gamma.enabled: true` with `gammaUi.enabled: true` enables Gamma on the API and deploys the Gamma console.
* `gamma.enabled: true` with `gammaUi.enabled: false` enables Gamma on the API without the console.

If `gamma.enabled` is `false`, Gamma stays off everywhere, and the Gamma console doesn't deploy even when `gammaUi.enabled` is `true`.
{% endhint %}

### Install with Helm

1. Add the Gravitee Helm repository:

   ```bash
   helm repo add graviteeio https://helm.gravitee.io
   helm repo update
   ```
2. Install the chart with the release name `gamma`. This creates the components and the ingress together:

   ```bash
   helm install gamma graviteeio/apim \
     --version 4.12.0 --devel \
     --namespace gravitee-gamma \
     -f values.yaml \
     --wait --timeout 10m
   ```
3. Confirm the ingress has the load balancer address:

   ```bash
   kubectl get ingress gamma -n gravitee-gamma
   ```

## Access the consoles

After DNS resolves to the ingress controller, open the consoles. The default username and password for the Gamma console, the APIM Console, and the Developer Portal are both `admin`.

| Component | URL | Default credentials |
| --- | --- | --- |
| Gamma console | `http://gamma.example.com/` | `admin` / `admin` |
| APIM Console | `http://gamma.example.com/console` | `admin` / `admin` |
| Developer Portal | `http://gamma.example.com/dev/` | `admin` / `admin` |

## Verification

* Confirm the pods are running and the ingress serves the platform:

  ```bash
  kubectl get pods -n gravitee-gamma
  curl -s -o /dev/null -w "%{http_code}\n" http://gamma.example.com/management/v2/ui/bootstrap
  ```

  \
  The bootstrap call returns `200` once the platform is up.

## Why one hostname

The Gamma console (`/`) and the API (`/gamma`, `/management`) are on the same host, so the browser requests are same-origin and the login session cookie is sent with each call. If you instead put the console and the API on separate subdomains, the cookie becomes cross-site and you'd need `SameSite=None; Secure` cookies (and therefore HTTPS) plus per-origin CORS. Keeping everything on one host behind one ingress is simpler.

To serve the single host over HTTPS, add a `tls` block to the `extraObjects` ingress (referencing a Kubernetes TLS secret, for example one issued by [cert-manager](https://cert-manager.io/)), switch the URLs in `values.yaml` to `https://`, and set `gravitee_http_cookie_secure` to `"true"`.

## Next steps

* Create your first MCP server. For more information, see [Create your first MCP server](../../../../agent-management/get-started/create-your-first-mcp-server.md).
