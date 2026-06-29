---
hidden: false
noIndex: false
---
# Install Gamma on Vanilla Kubernetes
<!-- GAP-STRUCTURAL: Missing procedural content source -->

{% hint style="warning" %}
This installation guide is for development and quick-start purposes only. Don't use it for production environments. For best practices for production environments, contact your Technical Account Manager.
{% endhint %}

## Overview

This guide explains how to install a self-hosted Gravitee Gamma platform on Kubernetes with Helm.

You deploy the standard `graviteeio/apim` Helm chart, turn on Gamma with `gamma.enabled`, and add the Gamma console (`gammaUi`). The Gamma console isn't a separate backend. It talks to the Management API, which runs with Gamma enabled.

The most important rule for this deployment is that **every user interface and the Management API share a single hostname** (`gamma.localhost`). This keeps every browser request same-origin so the login session cookie is sent with each API call. If you split the consoles and the API across different hostnames over HTTP, the browser drops the session cookie and login fails. For the full reason, see [Why a single hostname](#why-a-single-hostname).

By the end of this guide, you'll have the Gamma console, the APIM Console, the Developer Portal, and the API Gateway running locally, and you'll sign in to the Gamma console with `admin` / `admin`.

## Prerequisites

Before you install Gamma, complete the following steps:

* Install [helm](https://helm.sh/docs/intro/install/).
* Install [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl).
* Ensure you have access to the local Kubernetes cluster where you want to install Gamma. This guide covers both Docker Desktop and minikube. Where a step differs between them, follow the tab for your cluster.
* **(Enterprise Edition only)** To enable Agent Management, you need an enterprise license that includes the `agent-management` pack. To get one, contact your Technical Account Manager. For more information, see [Add your license key](#enterprise-edition-only-add-your-license-key).
* For Gravitee Enterprise Edition deployments, ensure that you have your license key. For more information about license keys, see [Gravitee Platform Pricing](https://www.gravitee.io/pricing).

## Components overview

This deployment includes the components that work together to provide Gamma:

* Management API: handles configuration and administrative operations, and runs with Gamma enabled.
* Gateway: processes API requests, applies policies, and routes traffic to backend services.
* APIM Console: the web interface for API administrators.
* Developer Portal: the self-service portal for API consumers.
* Gamma console: the Gamma user interface, served from the Management API.

The platform also requires two datastores:

* MongoDB: stores API definitions, configurations, and rate-limiting data.
* Elasticsearch: provides analytics, logging, and search.

{% hint style="info" %}
This guide doesn't deploy Access Management (AM). You don't need AM to run Gamma or to sign in. AM is required only for Gamma's agent-identity features in Agent Management. To add those features, deploy AM separately and wire it to Gamma after the platform is up.
{% endhint %}

## Install Gamma

To install Gamma, complete the following steps:

1. [#create-the-namespace](#create-the-namespace "mention")
2. [#deploy-mongodb-and-elasticsearch](#deploy-mongodb-and-elasticsearch "mention")
3. [#install-the-ingress-controller](#install-the-ingress-controller "mention")
4. [#configure-dns-resolution](#configure-dns-resolution "mention")
5. [#enterprise-edition-only-add-your-license-key](#enterprise-edition-only-add-your-license-key "mention")
6. [#prepare-the-values-yaml-for-helm](#prepare-the-values-yaml-for-helm "mention")
7. [#install-with-helm](#install-with-helm "mention")

### Create the namespace

A dedicated namespace isolates the Gamma resources from other applications in the cluster.

* Create the namespace using the following command:

  ```bash
  kubectl create namespace gravitee-gamma
  ```

### Deploy MongoDB and Elasticsearch

Gamma needs MongoDB and Elasticsearch. Install both into the `gravitee-gamma` namespace with Helm, then point the chart at them through the `mongo` and `es` settings in your `values.yaml`.

1. Install MongoDB using the following command. For more information, see the [official chart documentation](https://artifacthub.io/packages/helm/bitnami/mongodb).

   ```bash
   helm install gravitee-mongodb oci://registry-1.docker.io/cloudpirates/mongodb \
     --namespace gravitee-gamma \
     --set auth.enabled=false \
     --set persistence.enabled=false \
     --set resources.requests.memory=512Mi \
     --set resources.requests.cpu=250m
   ```

2. Install Elasticsearch using the following commands. For more information, see the [official chart documentation](https://artifacthub.io/packages/helm/elastic/elasticsearch).

   ```bash
   helm repo add elastic https://helm.elastic.co
   helm repo update

   helm install elasticsearch elastic/elasticsearch \
     --namespace gravitee-gamma \
     --set persistence.enabled=false \
     --set replicas=1 \
     --set minimumMasterNodes=1
   ```

3. Retrieve the `elastic` user password using the following command. You add it to your `values.yaml` in [Prepare the values.yaml for Helm](#prepare-the-values-yaml-for-helm):

   ```bash
   kubectl get secrets --namespace gravitee-gamma elasticsearch-master-credentials -o jsonpath='{.data.password}' | base64 -d
   ```

#### Verification

* Confirm both datastores report `Running` using the following commands:

  ```bash
  kubectl get pods -n gravitee-gamma -l app.kubernetes.io/instance=gravitee-mongodb
  kubectl get pods -n gravitee-gamma -l app=elasticsearch-master
  ```

  \
  After a few minutes, both pods report `Running`:

  ```bash
  NAME                     READY   STATUS    RESTARTS   AGE
  gravitee-mongodb-0       1/1     Running   0          2m
  elasticsearch-master-0   1/1     Running   0          3m
  ```

### Install the ingress controller

{% hint style="info" %}
If you already have the NGINX Ingress Controller installed, skip this section.
{% endhint %}

An ingress controller routes external traffic to the Gamma services and the consoles. The install step differs between Docker Desktop and minikube, so follow the section for your cluster.

#### Docker Desktop

* Install the NGINX Ingress Controller using the following command. Docker Desktop bridges the controller's `LoadBalancer` service to `localhost` automatically, so no tunnel is needed:

  ```bash
  kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.12.0/deploy/static/provider/cloud/deploy.yaml
  ```

#### minikube

On minikube, enable the built-in ingress addon instead of applying the manifest above. The addon installs the NGINX Ingress Controller and creates an `IngressClass` named `nginx`, which matches the `ingressClassName: nginx` in the `values.yaml`.

1. Enable the ingress addon using the following command:

   ```bash
   minikube addons enable ingress
   ```

2. minikube doesn't have a cloud load balancer, so the controller has no external IP until a tunnel runs. In a separate terminal, start the tunnel and keep it running for as long as you use Gamma:

   ```bash
   sudo minikube tunnel
   ```

{% hint style="info" %}
On macOS with the Docker driver, `minikube tunnel` can assign `127.0.0.1` as the external IP without binding port 80 on the host, so `gamma.localhost` stays unreachable. If that happens, stop the tunnel and port-forward the controller directly in a separate terminal instead, keeping it running:

```bash
sudo kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 80:80
```
{% endhint %}

#### Verification

1. Verify the controller is running using the following command:

   ```bash
   kubectl get pods -n ingress-nginx
   ```

   \
   The output shows the controller pod in `Running` status:

   ```bash
   NAME                                       READY   STATUS    RESTARTS   AGE
   ingress-nginx-controller-xxxxxxxxx-xxxxx   1/1     Running   0          2m
   ```

2. Confirm the `IngressClass` is named `nginx`, the value the `values.yaml` expects, using the following command:

   ```bash
   kubectl get ingressclass
   ```

   \
   The output lists `nginx`:

   ```bash
   NAME    CONTROLLER             PARAMETERS   AGE
   nginx   k8s.io/ingress-nginx   <none>       2m
   ```

### Configure DNS resolution

The deployment serves every console and the API on `gamma.localhost`, and the Gateway on `api.localhost`. Most browsers resolve `*.localhost` to `127.0.0.1` automatically. If yours doesn't, add the entries to your hosts file.

1. Add the DNS entries using the following commands:

   ```bash
   echo "127.0.0.1 gamma.localhost" | sudo tee -a /etc/hosts
   echo "127.0.0.1 api.localhost"   | sudo tee -a /etc/hosts
   ```

#### Verification

* Verify the entries using the following command:

  ```bash
  cat /etc/hosts | tail -2
  ```

  \
  The output shows both entries:

  ```bash
  127.0.0.1 gamma.localhost
  127.0.0.1 api.localhost
  ```

### (Enterprise Edition only) Add your license key

Agent Management is an enterprise feature. It only activates with an enterprise license that includes the `agent-management` pack. Without a license, the module loads but stays inactive and doesn't appear in the console. The other modules (API Management, Authorization Management, and Platform Management) work without a license.

To get a license, contact your Technical Account Manager. Your account manager sends you the license as a `license.key` file. On Kubernetes, you store the license in a Kubernetes secret that the Management API mounts.

{% hint style="info" %}
If your license is a base64-encoded text file (for example, `license.base64.txt`), decode it into `license.key` first. The `kubectl create secret` command in the next step references that exact name:

```bash
base64 -d < license.base64.txt > license.key
```

On macOS, use `base64 -D` (capital `D`) if `base64 -d` returns an error.
{% endhint %}

1. Save the `license.key` file your account manager sent you.
2. Create a Kubernetes secret named `gravitee-license` from that file, in the `gravitee-gamma` namespace:

   ```bash
   kubectl create secret generic gravitee-license \
     --from-file=license.key=./license.key \
     --namespace gravitee-gamma
   ```

   \
   The license now lives in the cluster as a secret. You can delete the `license.key` file afterward.
3. In your `values.yaml`, uncomment the license lines under the `api` service so the chart mounts the secret:

   ```yaml
   api:
     extraVolumes: |
       - name: gravitee-license
         secret:
           secretName: gravitee-license
     extraVolumeMounts: |
       - name: gravitee-license
         mountPath: "/opt/graviteeio-management-api/license/license.key"
         subPath: license.key
         readOnly: true
   ```

   \
   The [Install with Helm](#install-with-helm) step then mounts the secret automatically.

### Prepare the `values.yaml` for Helm

The Helm values consolidate every console and the API on `gamma.localhost`, point the platform at the datastores you deployed in [Deploy MongoDB and Elasticsearch](#deploy-mongodb-and-elasticsearch), and turn on Gamma.

1. Create a `values.yaml` file in your working directory, and then copy the following configuration into it:

   ```yaml
   # Gravitee Gamma - single-hostname Helm values for local Kubernetes
   #
   # Every console and the Management API are served on gamma.localhost so the
   # browser keeps each request same-origin and the login session cookie is
   # sent. The Gateway is the only component on its own hostname (api.localhost)
   # because it doesn't take part in console login.

   # MongoDB Configuration
   mongo:
     uri: mongodb://gravitee-mongodb.gravitee-gamma.svc.cluster.local:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000

   # # Uncomment to use PostgreSQL Configuration
   # jdbc:
   #   url: jdbc:postgresql://gravitee-postgresql.gravitee-gamma.svc.cluster.local:5432/gravitee
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

   # Disable the bundled MongoDB and Elasticsearch subcharts.
   # This guide installs MongoDB and Elasticsearch as separate Helm releases
   # (see Deploy MongoDB and Elasticsearch).
   mongodb:
     enabled: false
   elasticsearch:
     enabled: false

   # Installation - single origin for all UIs
   installation:
     type: standalone
     api:
       url: http://gamma.localhost/management
     standalone:
       console:
         urls:
           - orgId: DEFAULT
             url: http://gamma.localhost/console/
       portal:
         urls:
           - envId: DEFAULT
             url: http://gamma.localhost/dev/
       gamma-console:
         urls:
           - orgId: DEFAULT
             url: http://gamma.localhost/

   # Turn on Gamma
   gamma:
     enabled: true

   # Management API Configuration
   api:
     enabled: true
     replicaCount: 1
     image:
       repository: graviteeio/apim-management-api
       tag: 4.12.0
       pullPolicy: Always

     env:
       - name: gravitee_installation_api_url
         value: "http://gamma.localhost/management"

       # CORS Configuration - single origin, credentials allowed
       - name: gravitee_http_cors_enabled
         value: "true"
       - name: gravitee_http_cors_allow-origin
         value: "http://gamma.localhost"
       - name: gravitee_http_cors_allow-headers
         value: "Authorization,Content-Type,X-Requested-With,Accept,Origin,Access-Control-Request-Method,Access-Control-Request-Headers,Cookie"
       - name: gravitee_http_cors_allow-methods
         value: "GET,POST,PUT,DELETE,OPTIONS"
       - name: gravitee_http_cors_exposed-headers
         value: "X-Total-Count,Set-Cookie"
       - name: gravitee_http_cors_allow-credentials
         value: "true"

       # Cookie Configuration - same-origin session cookie over HTTP
       - name: gravitee_http_cookie_sameSite
         value: "Lax"
       - name: gravitee_http_cookie_secure
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
           - gamma.localhost
         annotations: {}
       portal:
         enabled: true
         ingressClassName: nginx
         scheme: http
         pathType: Prefix
         path: /portal
         hosts:
           - gamma.localhost
         annotations: {}
       gamma:
         enabled: true
         ingressClassName: nginx
         scheme: http
         pathType: Prefix
         path: /gamma
         hosts:
           - gamma.localhost
         annotations: {}

     resources:
       requests:
         memory: "1Gi"
         cpu: "500m"
       limits:
         memory: "2Gi"
         cpu: "1"

     # (Enterprise Edition) Agent Management needs a license. Create a Kubernetes
     # secret named gravitee-license (see "Add your license key"), then uncomment
     # the lines below to mount it into the Management API.
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
       tag: 4.12.0
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

   # # Uncomment to use Redis for caching and rate limiting
   # ratelimit:
   #   redis:
   #     download: false
   #     host: gravitee-redis.gravitee-gamma.svc.cluster.local
   #     port: 6379
   #     password: redis-password
   #     ssl: false

   # Management Console UI - gamma.localhost/console
   ui:
     enabled: true
     replicaCount: 1
     image:
       repository: graviteeio/apim-management-ui
       tag: 4.12.0
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
         - gamma.localhost
       annotations:
         nginx.ingress.kubernetes.io/rewrite-target: /$1

     resources:
       requests:
         memory: "256Mi"
         cpu: "100m"
       limits:
         memory: "512Mi"
         cpu: "250m"

   # Developer Portal UI - gamma.localhost/dev/
   portal:
     enabled: true
     defaultPortal: "classic"
     replicaCount: 1
     image:
       repository: graviteeio/apim-portal-ui
       tag: 4.12.0
       pullPolicy: Always

     env:
       - name: PORTAL_BASE_HREF
         value: /dev/

     service:
       type: ClusterIP
       externalPort: 8003
       internalPort: 8080

     ingress:
       enabled: true
       ingressClassName: nginx
       pathType: ImplementationSpecific
       path: /dev(/.*)?
       hosts:
         - gamma.localhost
       annotations:
         nginx.ingress.kubernetes.io/rewrite-target: /$1

     resources:
       requests:
         memory: "256Mi"
         cpu: "100m"
       limits:
         memory: "512Mi"
         cpu: "250m"

   # Gamma Console UI - gamma.localhost/ (catch-all)
   gammaUi:
     enabled: true
     image:
       repository: graviteeio/gamma-ui
       tag: 4.12.0
       pullPolicy: Always
     app:
       # URL the Gamma console uses to reach the Gamma API
       gammaBaseURL: "http://gamma.localhost/gamma"
     env:
       # Serve the Gamma console at the root path
       - name: GAMMA_CONSOLE_BASE_HREF
         value: /
     ingress:
       enabled: true
       ingressClassName: nginx
       pathType: ImplementationSpecific
       path: /(.*)
       hosts:
         - gamma.localhost
       annotations:
         nginx.ingress.kubernetes.io/rewrite-target: /$1

     resources:
       requests:
         memory: "64Mi"
         cpu: "50m"
       limits:
         memory: "128Mi"
         cpu: "100m"

   # Alternative configurations (to switch database types):

   # Option 1: MongoDB for both management and rate limiting (current configuration)
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

   # Current configuration: MongoDB for management and for rate limiting.
   # Ensure MongoDB and Elasticsearch are running in your cluster
   # (see Deploy MongoDB and Elasticsearch).
   ```

2. Replace `[ELASTIC PASSWORD FROM ES INSTALLATION]` with the password you retrieved in [Deploy MongoDB and Elasticsearch](#deploy-mongodb-and-elasticsearch).
3. Save the `values.yaml` file in your working directory.

<details>

<summary>Explanations of key <code>values.yaml</code> settings</summary>

**Turn on Gamma**

`gamma.enabled: true` turns on Gamma in the Management API configuration and unlocks the Gamma ingress and the Gamma console deployment. `gammaUi.enabled: true` deploys the Gamma console (`graviteeio/gamma-ui`).

**Single origin**

Every `hosts` entry for the consoles and the Management API ingresses is `gamma.localhost`. The Gateway is the only component on its own hostname (`api.localhost`) because it doesn't take part in console login. The `installation` block registers each console URL on `gamma.localhost`, and the CORS and cookie settings allow credentials on that origin with a `SameSite=Lax` cookie over HTTP.

**Gamma console wiring**

* `gammaUi.app.gammaBaseURL` is the URL the Gamma console uses to reach the Gamma API. It's written into the console's `constants.json`.
* `gammaUi.env GAMMA_CONSOLE_BASE_HREF: /` serves the Gamma console at the root path.
* `api.ingress.gamma.enabled: true` exposes the Gamma API on `gamma.localhost/gamma`.

**Datastores**

`mongodb.enabled` and `elasticsearch.enabled` are `false` because you installed MongoDB and Elasticsearch as separate Helm releases. The `mongo.uri` and `es.endpoints` values point at those services.

</details>

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

The chart that includes Gamma ships as a `4.12` pre-release build for the Gamma release.

1. Add the Gravitee Helm repository using the following commands:

   ```bash
   helm repo add graviteeio https://helm.gravitee.io
   helm repo update
   ```

2. List the available `4.12` pre-release chart versions using the following command:

   ```bash
   helm search repo graviteeio/apim --devel --versions
   ```

3. Install the chart with the release name `gamma` using the following command. Replace the version with the `4.12` pre-release you found in the previous step:

   ```bash
   helm install gamma graviteeio/apim \
     --version 4.12.0 \
     --devel \
     --namespace gravitee-gamma \
     -f values.yaml \
     --wait --timeout 10m
   ```

   \
   **(Enterprise Edition)** If you created the license secret in [Add your license key](#enterprise-edition-only-add-your-license-key) and uncommented the secret lines in your `values.yaml`, the chart mounts the license automatically. No extra flag is needed.

{% hint style="info" %}
Gamma ships in evolving `4.12` pre-release builds for the Gamma release, so the exact chart version and image tags move. The image tags in `values.yaml` (`4.12.0`) are the public Docker Hub builds. Pick the current `4.12` chart version from the `helm search` output, and keep the release name `gamma` so the service names in the next step match.
{% endhint %}

## Access the consoles

Wait about 60 seconds for the pods to become ready, then open the consoles in your browser. The default username and password for the Gamma console, the APIM Console, and the Developer Portal are both `admin`.

| Component | URL | Default credentials |
| --- | --- | --- |
| Gamma console | `http://gamma.localhost/` | `admin` / `admin` |
| APIM Console | `http://gamma.localhost/console` | `admin` / `admin` |
| Developer Portal | `http://gamma.localhost/dev/` | `admin` / `admin` |
| API Gateway | `http://api.localhost/` | Not applicable |

<!-- TODO: Screenshot of the Gamma console sign-in page at gamma.localhost -->
<figure><img src="../../../.gitbook/assets/gamma-console-sign-in.png" alt=""><figcaption><p>The Gamma console sign-in page</p></figcaption></figure>

## Verification

To verify that the platform is up and reachable, complete the following steps:

1. [#validate-the-pods](#validate-the-pods "mention")
2. [#validate-the-endpoints](#validate-the-endpoints "mention")
3. [#validate-the-gateway](#validate-the-gateway "mention")

### Validate the pods

A healthy deployment shows the pods with the `Running` status and `1/1` ready containers.

* Query the pod status using the following command:

  ```bash
  kubectl get pods --namespace=gravitee-gamma
  ```

  \
  The output shows the Gamma components ready and running:

  ```bash
  NAME                            READY   STATUS    RESTARTS   AGE
  gamma-apim-api-xxx              1/1     Running   0          3m
  gamma-apim-gateway-xxx          1/1     Running   0          3m
  gamma-apim-ui-xxx               1/1     Running   0          3m
  gamma-apim-portal-xxx           1/1     Running   0          3m
  gamma-gamma-xxx                 1/1     Running   0          3m
  ```

### Validate the endpoints

* Confirm each surface answers using the following commands:

  ```bash
  curl -s http://gamma.localhost/ | head -5          # Gamma console HTML
  curl -s http://gamma.localhost/console | head -5   # APIM Console HTML
  curl -s http://gamma.localhost/dev/ | head -5      # Developer Portal HTML
  curl -s -u admin:admin \
    http://gamma.localhost/management/organizations/DEFAULT/environments
  ```

  \
  The Management API call returns the default environment:

  ```json
  [{"id":"DEFAULT","name":"Default environment", ... }]
  ```

### Validate the Gateway

* Call the Gateway on its own hostname using the following command:

  ```bash
  curl -i http://api.localhost/
  ```

  \
  The output confirms the Gateway is running with no API deployed yet at the root path:

  ```bash
  No context-path matches the request URI.
  ```

## Why a single hostname

The Management API exposes a single installation API URL that bootstraps every user interface. When the consoles and the API live on different hostnames, the API calls become cross-origin. Over HTTP, browsers enforce `SameSite=Lax` on cookies and don't send the session cookie on cross-origin requests, which breaks the login flow. The failure surfaces in the Gamma console as a login error.

Consolidating every console and the Management API on `gamma.localhost` makes all requests same-origin, so the session cookie is sent with each call and login works. This is the same outcome the Docker Compose setup achieves with an NGINX reverse proxy that serves all components on one hostname.

If you need the consoles on separate subdomains (for example, `console.example.com` and `portal.example.com`), use HTTPS with `SameSite=None; Secure` cookies, or put a reverse proxy in front of each subdomain that forwards API requests to the backend.

## Next steps

* Create your first MCP server. For more information, see [Create your first MCP server](../../../agent-management/get-started/create-your-first-mcp-server.md).
* Add Gamma's agent-identity features. Deploy Access Management and wire it to Gamma. For more information, see [Configure your Access Management instance](../../../agent-management/build/configure-your-access-management-instance.md).
