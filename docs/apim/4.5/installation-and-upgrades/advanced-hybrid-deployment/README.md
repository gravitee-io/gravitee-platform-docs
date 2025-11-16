---
description: Installing and configuring a hybrid API Management deployment
---

# Installing a Gravitee Gateway with a Hybrid Deployment

## Introduction

Hybrid architecture is the deployment of a Gravitee Gateway using self-hosted and cloud deployments.

The Gravitee Gateway hybrid deployment uses hybrid components to provide flexibility when you define your architecture and deployment.&#x20;

This page explains how to install a Self-Hosted Data-Plane in a Hybrid deployment, which consists of a SaaS Control-Plane and a Self-Hosted Data-Plane. The control plane signifies the Bridge and the data-plane signifies the Gateway.&#x20;

The Gravitee Gateway needs the following two components:

* An HTTP _Bridge_ server that exposes extra HTTP services for bridging HTTP calls to the underlying repositories. For example, MongoDB and JDBC.
* A _standard_ API Management (APIM) Gateway. You must switch the default repository plugin to the bridge repository plugin.

## Before you begin

* Ensure that you understand the various components of a Hybrid deployment. Here are two tables that explains the components of a Hybrid deployment:

{% tabs %}
{% tab title="SaaS Control-Plane components" %}
<table><thead><tr><th width="225.37383177570098" align="center">Component</th><th>Description</th></tr></thead><tbody><tr><td align="center">APIM Console<br>(for API producers)</td><td>This web UI gives easy access to some key APIM Management API services. <a href="../../#api-publisher">API publishers</a> can use it to publish APIs.<br>Administrators can also configure global platform settings and specific portal settings.</td></tr><tr><td align="center">APIM Management API</td><td>This RESTful API exposes services to manage and configure the APIM Console and APIM Developer Portal web UIs.<br>All exposed services are restricted by authentication and authorization rules. For more information, see the<a href="../../reference/management-api-reference.md"> Management API Reference</a> section.</td></tr><tr><td align="center"><a href="../../using-the-product/using-the-gravitee-api-management-components/developer-portal/">APIM Developer Portal</a><br>(for API consumers)</td><td>This web UI gives easy access to some key APIM API services. It allows <a href="../../#api-consumer">API Consumers</a> to managed their applications and search for, view, try out, and subscribe to a published API.</td></tr><tr><td align="center"><p>[Optional]</p><p>APIM SaaS API Gateways</p></td><td>APIM Gateway is the core component of the APIM platform. You can think of it like a smart reverse proxy.<br>Unlike a traditional HTTP proxy, APIM Gateway has the capability to apply <a href="../../using-the-product/managing-your-apis/policy-studio/">policies</a> (i.e., rules or logic) to both the request and response phases of an API transaction. With these policies, you can transform, secure, monitor, etc., your APIs.</td></tr><tr><td align="center">Bridge Server</td><td>A <em>bridge</em> API Gateway exposes extra HTTP services for bridging HTTP calls to the underlying repository (which can be any of our supported repositories: MongoDB, JDBC, etc.)</td></tr><tr><td align="center">Config Database</td><td>All the API Management platform management data, such as API definitions, users, applications, and plans.</td></tr><tr><td align="center">S3 Bucket + Analytics Database</td><td>Analytics and logs data.</td></tr><tr><td align="center">Gravitee Cockpit</td><td>Gravitee Cockpit is a centralized, multi-environments / organizations tool for managing all your Gravitee API Management and Access Management installations in a single place.</td></tr><tr><td align="center">[Optional]<br>API Designer</td><td>Drag-and-Drop graphical (MindMap) API designer to quickly and intuitively design your APIs (Swagger / OAS) and deploy mocked APIs for quick testing.</td></tr><tr><td align="center">[Optional]<br>Alert Engine</td><td>Alert Engine (AE) provides APIM and AM users with efficient and flexible API platform monitoring, including advanced alerting configuration and notifications sent through their preferred channels, such as email, Slack and using Webhooks.<br>AE does not require any external components or a database as it does not store anything. It receives events and sends notifications under the conditions which have been pre-configured upstream with triggers.</td></tr></tbody></table>
{% endtab %}

{% tab title="Self-Hosted Data-Plane components" %}
<table><thead><tr><th width="172.18918918918916" align="center">Component</th><th>Description</th></tr></thead><tbody><tr><td align="center">APIM Gateway</td><td>APIM Gateway is the core component of the APIM platform. You can think of it like a smart reverse proxy.<br><br>Unlike a traditional HTTP proxy, APIM Gateway has the capability to apply <a href="../../using-the-product/managing-your-apis/policy-studio/">policies</a> (i.e., rules or logic) to both the request and response phases of an API transaction. With these policies, you can transform, secure, monitor, etc., your APIs.</td></tr><tr><td align="center">Logstash</td><td>Collect and send local Gateway logs and metrics to the Gravitee APIM SaaS Control Plane.</td></tr><tr><td align="center">Redis</td><td>The database used locally for rate limit synchronized counters (RateLimit, Quota, Spike Arrest) and, optionally, as an external cache for the Cache policy.</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

* Ensure that the Bridge and Gateway versions that you use for your Hybrid deployment are compatible. For more information about Gateway and Bridge compatibility versions, see [Gateway and Bridge compatibility versions](gateway-and-bridge-compatibility-versions.md).

<img src="../../.gitbook/assets/file.excalidraw (18).svg" alt="Hybrid deployment architecture" class="gitbook-drawing">

<figure><img src="../../.gitbook/assets/image (134).png" alt="Diagram showing the hybrid architecture"><figcaption><p>Hybrid architecture connections</p></figcaption></figure>

## Installing your Self-Hosted Hybrid Gateway <a href="#installation" id="installation"></a>

{% hint style="danger" %}
Make sure that the version you install is compatible with the Control-Plane SaaS version.
{% endhint %}

{% hint style="info" %}
Ensure that you add the Gravitee.io License file.
{% endhint %}

{% tabs %}
{% tab title="Kubernetes (Helm)" %}
To install a Gravitee Gateway on Kubernetes, complete the following steps:&#x20;

{% hint style="info" %}
You must be familiar with the following topics:

* Google Cloud Platform (GCP)
* Kubernetes (K8s)
* Helm
{% endhint %}

## Target architecture

In this example, we demonstrate how to deploy a Gravitee Gateway (APIM) in two different GCP regions. Also, we demonstrate how to deploy Gravitee APIM in the follow two different K8s clusters:

* A **Management cluster** that runs the following components:
  * &#x20;The management API
  * &#x20;The two APIM UI components
  * &#x20;A bridge gateway
* A **Gateway cluster** that runs the APIM gateway.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/hybrid/hybrid_deployment_k8s.png" alt=""><figcaption><p>Kubernetes hybrid deployment architecture diagram</p></figcaption></figure>

In this example, the deployment consists of the following components:

* MongoDB. MongoDB manages all the management data. For example,  API definitions, subscriptions, and API keys.
* ElasticSearch. ElasticSearch is deployed in the Management cluster.
* Redis. Redis manages the rate limits and quota counters within the Gateway cluster.

## Deploying a Hybrid architecture with Helm

* To deploy a Hybrid architecture with Kubernetes, go to [Gravitee's Helm charts](https://helm.gravitee.io/).

### Before you begin

* Ensure the two GCP clusters exist.
* Ensure that Helm is installed on the GCP clusters.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/hybrid/hybrid_k8s_clusters.png" alt=""><figcaption><p>Sample K8 clusters</p></figcaption></figure>

{% hint style="warning" %}
The following Hybrid architecture example use the following names:

* hybrid-gw-eu
* hybrid-mgmt-eu

You can replace these names with the name of your clusters.
{% endhint %}

### Deploying the management cluster

1. Initialize the cluster with some prerequisites using the following commands:

{% code overflow="wrap" %}
```sh
$ gcloud container clusters get-credentials hybrid-mgmt-eu --zone=europe-west1-b

// Create namespace
$ kubectl create namespace graviteeio

// Nginx ingress controller is required for Gravitee APIM chart
$ helm install --name nginx-ingress --namespace graviteeio stable/nginx-ingress --set rbac.create=true --set controller.publishService.enabled=true

// Add Gravitee Helm repository
$ helm repo add graviteeio https://helm.gravitee.io
```
{% endcode %}

2. Deploy the management APIM instance using the following command. The management APIM contains the follow components:&#x20;



* The Management Console
* The Developer Portal
* Management API
* The Bridge Gateway

```sh
$ helm install — name graviteeio-apim3 — namespace graviteeio \
 -f values-bridge-http-server.yaml \
 -f values-hybrid-management-eu.yaml \
 graviteeio/apim3
```

When you install the `values-hybrid-management-eu.yaml`, the file looks like this example:

{% code title="values-hybrid-management-eu.yaml" %}
```yaml
mongo:
    uri: mongodb+srv://xxxxxx:xxxxx@demo.xxxxx.gcp.mongodb.net/gio-apim-hybrid?retryWrites=true&w=majority

es:
    endpoints:
        - https://xxxxxxxxx-elasticsearch.services.elasticcloud.com/
    index: demo_hybrid_apim
    security:
        enabled: true
        username: xxxxxx
        password: xxxxxx

api:
    ingress:
        management:
            path: /management
            hosts:
                - demo-hybrid-apim-api.cloud.gravitee.io
            tls:
            -   hosts:
                    - demo-hybrid-apim-api.cloud.gravitee.io
                secretName: cloud-gravitee-cert
        portal:
            path: /portal
            hosts:
                - demo-hybrid-apim-api.cloud.gravitee.io
            tls:
            -   hosts:
                    - demo-hybrid-apim-api.cloud.gravitee.io
                secretName: cloud-gravitee-cert

gateway:
    ingress:
        enabled: false
    services:
        bridge:
            enabled: true
            authentication:
                type: basic
                basic:
                    username: xxxxxxxxx
                    password: xxxxxxxxx            
            service:
                externalPort: 92
                internalPort: 18092
            ingress:
                enabled: true
                path: /
                hosts:
                    - demo-hybrid-apim-bridge.cloud.gravitee.io
                annotations:
                    kubernetes.io/ingress.class: nginx
                    nginx.ingress.kubernetes.io/ssl-redirect: "false"
                    nginx.ingress.kubernetes.io/enable-rewrite-log: "true"
                    nginx.ingress.kubernetes.io/configuration-snippet: "etag on;\nproxy_pass_header ETag;\nproxy_set_header if-match \"\";\n"
                tls:
                -   secretName: cloud-gravitee-cert
                    hosts:
                        - demo-hybrid-apim-bridge.cloud.gravitee.io

ui:
    ingress:
        path: /
        hosts:
            - demo-hybrid-apim-console.cloud.gravitee.io
        annotations:
            nginx.ingress.kubernetes.io/rewrite-target: /
        tls:
        -   hosts:
                - demo-hybrid-apim-console.cloud.gravitee.io
            secretName: cloud-gravitee-cert

portal:
    ingress:
        path: /
        hosts:
            - demo-hybrid-apim-portal.cloud.gravitee.io
        tls:
        -   hosts:
                - demo-hybrid-apim-portal.cloud.gravitee.io
            secretName: cloud-gravitee-cert
```
{% endcode %}

The file shows the following elements:

* The Gateway is not exposed through the ingress controller.
* You enabled the bridge service for the Gateway.
* Declared a new ingress to expose it to remote clusters.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/hybrid/hybrid_deployment_ingress.png" alt=""><figcaption><p>APIM management cluster</p></figcaption></figure>

### Deploy the Gateway cluster

1. Initialize the cluster with some prerequisites using the following commands:

{% code overflow="wrap" %}
```sh
$ gcloud container clusters get-credentials hybrid-gw-eu --zone=europe-west2-b

// Create namespace
$ kubectl create namespace graviteeio

// Nginx ingress controller is required for Gravitee APIM chart
$ helm install --name nginx-ingress --namespace graviteeio stable/nginx-ingress --set rbac.create=true --set controller.publishService.enabled=true

// Add Gravitee Helm repository
$ helm repo add graviteeio https://helm.gravitee.io
```
{% endcode %}

2. Deploy only the APIM Gateway component using the following command:

```sh
$ helm install — name graviteeio-apim3 — namespace graviteeio \
 -f values-bridge-http-client.yaml \
 -f values-hybrid-gw-eu.yaml \
 graviteeio/apim3
```

When you deploy the Gravitee APIM Gateway, the `values-hybrid-management-gw-eu.yaml` file looks like the following example:

{% code title="values-hybrid-management-gw-eu.yaml" %}
```yaml
mongo:
    uri: mongodb+srv://xxxxxx:xxxxx@demo.xxxxx.gcp.mongodb.net/gio-apim-hybrid?retryWrites=true&w=majority
es:
    endpoints:
        - https://xxxxxxxxx-elasticsearch.services.elasticcloud.com/
    index: demo_hybrid_apim
    security:
        enabled: true
        username: xxxxxx
        password: xxxxxx
management:
    type: http
api:
    enabled: false
gateway:
    management:
        http:
            url: https://demo-hybrid-apim-bridge.cloud.gravitee.io/
            authentication:
                type: basic
                basic:
                    username: xxxxxxxxx
                    password: xxxxxxxxx
            ssl:
                ### beware: since 4.4 default is false
                trustAll: false
    ingress:
        path: /
        hosts:
            - demo-hybrid-apim-gw.cloud.gravitee.io
        tls:
        -   hosts:
                - demo-hybrid-apim-gw.cloud.gravitee.io
            secretName: cloud-gravitee-cert
ui:
    enabled: false
portal:
    enabled: false
```
{% endcode %}

`values-hybrid-management-gw-eu.yaml` shows the following elements:

* You have disabled all the management components to prevent their deployment.
* You have enabled `http` management mode for the gateway, and you use this link to mount all the required information in the Gateway to process API calls.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/hybrid/hybrid_deployment_http.png" alt=""><figcaption><p>APIM gatewaye cluster</p></figcaption></figure>

### Verification

To verify that you deployed this architecture correctly, complete the following steps:

#### Examine the Gateway pod logs

* Examine the Gateway pod logs. You should see an output like this example:

```sh
08:27:29.394 [graviteeio-node] [] INFO  i.g.g.r.p.RepositoryPluginHandler - Register a new repository plugin: repository-bridge-http-client [io.gravitee.repository.bridge.client.HttpBridgeRepository]
08:27:29.402 [graviteeio-node] [] INFO  i.g.g.r.p.RepositoryPluginHandler - Repository [MANAGEMENT] loaded by http
08:27:30.999 [graviteeio-node] [] INFO  i.g.r.b.client.http.WebClientFactory - Validate Bridge Server connection ...
08:27:32.888 [vert.x-eventloop-thread-1] [] INFO  i.g.r.b.client.http.WebClientFactory - Bridge Server connection successful.
```

#### Check the Management Gateway

* Open the Management Console. You should see two gateways.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/hybrid/hybrid_deployment_gateways.png" alt=""><figcaption><p>Hybrid K8 deployment</p></figcaption></figure>

{% hint style="info" %}
**Additional assets**

* [Gravitee Helm charts](https://artifacthub.io/packages/helm/graviteeio/apim3)
{% endhint %}
{% endtab %}

{% tab title="Docker" %}
* Install Gravitee API Management (APIM). For more information about installing Gravitee APIM, see [Install on Docker](../install-on-docker/README.md).
* Download, and then mount the following plugins for the Gravitee Gateway:
  * Redis Repository. This repository is used for the rate limits' synchronized counters. To download this repository, go to [Gravitee.io Downloads](https://download.gravitee.io/#graviteeio-apim/plugins/repositories/gravitee-apim-repository-redis).
  * TCP Reporter. This repository is used to push events to Logstash. To download this repository, go to [Gravitee.io Downloads.](https://download.gravitee.io/#graviteeio-ee/apim/plugins/reporters/gravitee-reporter-tcp/)
{% endtab %}

{% tab title="VM" %}
* Install Gravitee API Management (APIM). For more information about installing Gravitee APIM, see [Install with .ZIP](../install-with-.zip.md).
* Download, and then mount the following plugins for the Gravitee Gateway:
  * Redis Repository. This repository is used for the rate limits' synchronized counters. To download this repository, go to [Gravitee.io Downloads](https://download.gravitee.io/#graviteeio-apim/plugins/repositories/gravitee-apim-repository-redis).
  * TCP Reporter. This repository is used to push events to Logstash. To download this repository, go to [Gravitee.io Downloads.](https://download.gravitee.io/#graviteeio-ee/apim/plugins/reporters/gravitee-reporter-tcp/)
{% endtab %}
{% endtabs %}

## Configuring your Self-Hosted Hybrid Gateway <a href="#configuration" id="configuration"></a>

Here are the following configurations for your self-hosted Gateway:

* The connection between the SaaS Control-Plane and the Bridge Gateway.
* The connection between the push analytics and logs to Logstash and the SaaS storage.
* The connection to the local rate limits database (Redis).
* (Optional) The connection to the SaaS Alert Engine.

### **Configuring the connection between the SaaS Control-Plane and the Bridge Gateway**

{% tabs %}
{% tab title="Kubernetes (Helm)" %}
{% code title="values.yaml" lineNumbers="true" %}
```yaml
management:
  type: http
gateway:
  management:
    http:
      url: https://bridge-gateway-url:bridge-gateway-port
      # the following still works but is deprecated 
      # username: kubernetes://<namespace>/secrets/<my-secret-name>/<my-secret-key>
      # password: kubernetes://<namespace>/secrets/<my-secret-name>/<my-secret-key>
      authentication:
        type: basic
        basic:
          username: secret://kubernetes/<my-secret-name>:<my-secret-key>
          password: secret://kubernetes/<my-secret-name>:<my-secret-key>
      # ssl:
      #   ### beware: since 4.4 default is false (see upgrade guide) 
      #   trustall: true
      #   verifyHostname: true
      #   keystore:
      #     type: jks # Supports jks, pem, pkcs12
      #     path: ${gravitee.home}/security/keystore.jks
      #     password: secret
      #   truststore:
      #     type: jks # Supports jks, pem, pkcs12
      #     path: ${gravitee.home}/security/truststore.jks
      #     password: secret
      # proxy:
      #   host:
      #   port:
      #   type: http
      #   username:
      #   password:
```
{% endcode %}

{% hint style="info" %}
**Additional assets**

* [Gravitee Helm charts](https://artifacthub.io/packages/helm/graviteeio/apim3)
{% endhint %}
{% endtab %}

{% tab title="Docker" %}
{% code title="docker-compose.yaml" lineNumbers="true" %}
```yaml
version: '3'

services:
  gateway:
    image: graviteeio/apim-gateway:<VERSION-ALIGNED-WITH-CONTROL-PLANE>
    container_name: gio_apim_gateway
    restart: always
    ports:
      - "8082:8082"
    environment:
      # --- BRIDGE GATEWAYS ---
      - gravitee_management_type=http
      - gravitee_management_http_url=https://bridge-gateway-url:bridge-gateway-port
      - gravitee_management_http_authentication_type=basic
      - gravitee_management_http_authentication_basic_username=bridge-gateway-username
      - gravitee_management_http_authentication_basic_password=bridge-gateway-password
```
{% endcode %}
{% endtab %}

{% tab title="VM" %}
{% code title="gravitee.yaml" lineNumbers="true" %}
```yaml
management:
  type: http
  http:
    url: https://bridge-gateway-url:bridge-gateway-port
    keepAlive: true
    idleTimeout: 30000
    connectTimeout: 10000
    authentication:
      type: basic
      basic:
        username: bridge-gateway-username
        password: bridge-gateway-password
      # ssl:
      #   ###beware: since 4.4 default is false (see upgrade guide) 
      #   trustall: true
      #   verifyHostname: true
      #   keystore:
      #     type: jks # Supports jks, pem, pkcs12
      #     path: ${gravitee.home}/security/keystore.jks
      #     password: secret
      #   truststore:
      #     type: jks # Supports jks, pem, pkcs12
      #     path: ${gravitee.home}/security/truststore.jks
      #     password: secret
```
{% endcode %}
{% endtab %}
{% endtabs %}

### **Configuring the connection between Analytics and Logs to Logstash and SaaS storage**

{% tabs %}
{% tab title="Kubernetes (Helm)" %}
{% code title="values.yaml" lineNumbers="true" %}
```yaml
gateway:
  reporters:
    elasticsearch:
      enabled: false
    tcp:
      enabled: true
      host: logstash-host
      port: 8379
      output: elasticsearch
```
{% endcode %}
{% endtab %}

{% tab title="Docker" %}
{% code title="docker-compose.yaml" overflow="wrap" %}
```yaml
version: '3'

services:
  gateway:
    image: graviteeio/apim-gateway:<VERSION-ALIGNED-WITH-CONTROL-PLANE>
    container_name: gio_apim_gateway
    restart: always
    ports:
      - "8082:8082"
    environment:
      # --- LOGSTASH ---
      - gravitee_reporters_elasticsearch_enabled=false
      - gravitee_reporters_tcp_enabled=true
      - gravitee_reporters_tcp_host=logstash-host
      - gravitee_reporters_tcp_port=8379
      - gravitee_reporters_tcp_output=elasticsearch
```
{% endcode %}
{% endtab %}

{% tab title="VM" %}
{% code title="gravitee.yaml" lineNumbers="true" %}
```yaml
reporters:
  elasticsearch:
    enabled: false
  tcp:
    enabled: true
    host: logstash-host
    port: 8379
    output: elasticsearch
```
{% endcode %}
{% endtab %}
{% endtabs %}

### Configuring the connection to the local rate limits database (Redis)

{% tabs %}
{% tab title="Kubernetes (Helm)" %}
{% code title="values.yaml" lineNumbers="true" %}
```yaml
ratelimit:
  type: redis
redis:
  host: redis-host
  port: 6379
  password: kubernetes://<namespace>/secrets/<my-secret-name>/<my-secret-key>
  download: true
```
{% endcode %}

{% hint style="info" %}
**Additional assets**

* [Full `values.yaml` example](https://artifacthub.io/packages/helm/graviteeio/apim3?modal=values)
{% endhint %}
{% endtab %}

{% tab title="Docker" %}
{% code title="docker-compose.yaml" overflow="wrap" %}
```yaml
version: '3'

services:
  gateway:
    image: graviteeio/apim-gateway:<VERSION-ALIGNED-WITH-CONTROL-PLANE>
    container_name: gio_apim_gateway
    restart: always
    ports:
      - "8082:8082"
    environment:
      # --- RATE LIMIT REPO ---
      - gravitee_ratelimit_type=redis
      - gravitee_ratelimit_redis_host=redis-host
      - gravitee_ratelimit_redis_port=6379
      - gravitee_ratelimit_redis_password=${REDIS_PASS:-redis-password}
```
{% endcode %}
{% endtab %}

{% tab title="VM" %}
{% code title="gravitee.yaml" lineNumbers="true" %}
```yaml
ratelimit:
  type: redis
  redis:
    host: redis-host
    port: 6379
    password: redis-password
```
{% endcode %}
{% endtab %}
{% endtabs %}

### **Configuring the connection to the SaaS Alert Engine**

{% tabs %}
{% tab title="Kubernetes (Helm)" %}
{% code title="values.yaml" lineNumbers="true" %}
```yaml
alerts:
  enabled: true
  endpoints:
    - https://alert-engine-url:alert-engine-port
  security:
    enabled: true
    username: kubernetes://<namespace>/secrets/<my-secret-name>/<my-secret-key>
    password: kubernetes://<namespace>/secrets/<my-secret-name>/<my-secret-key>
```
{% endcode %}
{% endtab %}

{% tab title="Docker" %}
{% code title="docker-compose.yaml" lineNumbers="true" %}
```yaml
version: '3'

services:
  gateway:
    image: graviteeio/apim-gateway:<VERSION-ALIGNED-WITH-CONTROL-PLANE>
    container_name: gio_apim_gateway
    restart: always
    ports:
      - "8082:8082"
    environment:
      # --- ALERT ENGINE ---
      - gravitee_alerts_alertengine_enabled=true
      - gravitee_alerts_alertengine_ws_discovery=true
      - gravitee_alerts_alertengine_ws_endpoints_0=https://alert-engine-url:alert-engine-port
      - gravitee_alerts_alertengine_ws_security_username=alert-engine-username
      - gravitee_alerts_alertengine_ws_security_password=alert-engine-password
```
{% endcode %}
{% endtab %}

{% tab title="VM" %}
{% code title="gravitee.yaml" lineNumbers="true" %}
```yaml
alerts:
  alert-engine:
    enabled: true
    ws:
      discovery: true
      endpoints:
        - https://alert-engine-url:alert-engine-port
      security:
        username: alert-engine-username
        password: alert-engine-password
```
{% endcode %}
{% endtab %}
{% endtabs %}

### **An example of a Self-Hosted Gateway configuration**

{% tabs %}
{% tab title="Kubernetes (Helm)" %}
{% code title="values.yaml" lineNumbers="true" %}
```yaml
management:
  type: http
gateway:
  management:
    http:
      url: https://bridge-gateway-url:bridge-gateway-port
      authentication:
        type: basic
        basic:
          username: secrets://kubernetes/<my-secret-name>:<my-secret-key>
          password: secrets://kubernetes/<my-secret-name>:<my-secret-key>
  reporters:
    elasticsearch:
      enabled: false
    tcp:
      enabled: true
      host: logstash
      port: 8379
      output: elasticsearch
alerts:
  enabled: true
  endpoints:
    - https://alert-engine-url:alert-engine-port
  security:
    enabled: true
    username: secrets://kubernetes/<my-secret-name>:<my-secret-key>
    password: secrets://kubernetes/<my-secret-name>:<my-secret-key>
```
{% endcode %}
{% endtab %}

{% tab title="Docker" %}
{% code title="docker-compose.yaml" lineNumbers="true" %}
```yaml
version: '3'

volumes:
  data-redis:

services:
  gateway:
    image: graviteeio/apim-gateway:<VERSION-ALIGNED-WITH-CONTROL-PLANE>
    container_name: gio_apim_hybrid_gateway
    restart: always
    ports:
      - "8082:8082"
    depends_on:
      redis:
        condition: service_healthy
      logstash:
        condition: service_healthy
    volumes:
      # --- LOCAL LOG FILES ---
      - ./logs/apim-gateway-dev:/opt/graviteeio-gateway/logs
      # --- EE LICENSE FILE ---
      - ${GIO_LICENSE}:/opt/graviteeio-gateway/license/license.key
      # --- ADDITIONAL PLUGINS ---
      - ./plugins:/opt/graviteeio-gateway/plugins-ext
    environment:
      # --- PLUGINS LOCATIONS ---
      - gravitee_plugins_path_0=/opt/graviteeio-gateway/plugins
      - gravitee_plugins_path_1=/opt/graviteeio-gateway/plugins-ext
      # --- COCKPIT ORGS & ENVS ---
      - gravitee_organizations=<YOUR-COCKPIT-ORG-HRID>,<YOUR-COCKPIT-ORG-HRID>
      - gravitee_environments=<YOUR-COCKPIT-ENV-HRID>,<YOUR-COCKPIT-ENV-HRID>
      # --- SHARDING TAGS & TENANTS ---
      # - gravitee_tags=internal
      # - gravitee_tenant=xxx
      # --- BRIDGE GATEWAYS ---
      - gravitee_management_type=http
      - gravitee_management_http_url=https://bridge-gateway-url:bridge-gateway-port
      - gravitee_management_http_authentication_type=basic
      - gravitee_management_http_authentication_basic_username=bridge-gateway-username
      - gravitee_management_http_authentication_basic_password=bridge-gateway-password
      # --- RATE LIMIT REPO ---
      - gravitee_ratelimit_type=redis
      - gravitee_ratelimit_redis_host=redis
      - gravitee_ratelimit_redis_port=6379
      - gravitee_ratelimit_redis_password=${REDIS_PASS:-redis-password}
      # - gravitee_ratelimit_type=hazelcast
      # --- LOGSTASH ---
      - gravitee_reporters_elasticsearch_enabled=false
      - gravitee_reporters_tcp_enabled=true
      - gravitee_reporters_tcp_host=logstash
      - gravitee_reporters_tcp_port=8379
      - gravitee_reporters_tcp_output=elasticsearch
      # --- ALERT ENGINE ---
      - gravitee_alerts_alertengine_enabled=true
      - gravitee_alerts_alertengine_ws_discovery=true
      - gravitee_alerts_alertengine_ws_endpoints_0=https://alert-engine-url:alert-engine-port
      - gravitee_alerts_alertengine_ws_security_username=alert-engine-username
      - gravitee_alerts_alertengine_ws_security_password=alert-engine-password
      # --- SECRETS ---
      - gravitee_api_properties_encryption_secret=your-own-api-32-characters-secret

  redis:
    # https://hub.docker.com/_/redis?tab=tags
    image: redis:${REDIS_VERSION:-7.2.1-alpine}
    container_name: gio_apim_hybrid_redis
    hostname: redis
    restart: always
    ports:
      - '6379:6379'
    command: redis-server --requirepass ${REDIS_PASS:-28kjzEGquZYrztGyPMofR8eWuNbn4YqR}
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 1s
      timeout: 3s
      retries: 30
    volumes: 
      - data-redis:/data
  
  logstash:
    # https://www.docker.elastic.co/r/logstash/logstash-oss 
    image: docker.elastic.co/logstash/logstash-oss:${LOGSTASH_VERSION:-8.10.2}
    container_name: gio_apim_hybrid_logstash
    hostname: logstash
    ports:
      - "8379:8379"
    healthcheck:
      test: curl -f -I http://localhost:9600/_node/pipelines/main || exit 1
      start_period: 20s
      interval: 3s
      timeout: 5s
      retries: 30
    volumes:
      - ./config/logstash:/usr/share/logstash/pipeline:ro
    environment:
      LS_JAVA_OPTS: "-Xmx256m -Xms256m"
```
{% endcode %}
{% endtab %}

{% tab title="VM" %}
{% code title="gravitee.yaml" lineNumbers="true" %}
```yaml
############################################################################################################
#################################### Gravitee.IO Gateway - Configuration ###################################
############################################################################################################

############################################################################################################
# This file is the general configuration of Gravitee.IO Gateway:
# - Properties (and respective default values) in comment are provided for information.
# - You can reference other property by using ${property.name} syntax
# - gravitee.home property is automatically set-up by launcher and refers to the installation path. Do not override it !
#
# Please have a look to http://docs.gravitee.io/ for more options and fine-grained granularity
############################################################################################################

organizations: cockpit-org-hrid
environments: cockpit-env-hrid
tags: your, sharding, tags #example: internal

plugins:
  path:
    - /opt/graviteeio-gateway/plugins
    - /opt/graviteeio-gateway/plugins-ext

management:
  type: http
  http:
    url: https://bridge-gateway-url:bridge-gateway-port
    authentication:
      basic:
        username: bridge-gateway-username
        password: bridge-gateway-password

ratelimit:
  # type: hazelcast
  type: redis
  redis:
    host: redis-host
    port: 6379
    password: redis-password

cache:
  type: ehcache

reporters:
  elasticsearch:
    enabled: false # Is the reporter enabled or not (default to true)
  tcp:
    enabled: true
    host: logstash-host
    port: logstash-port
    output: elasticsearch

services:
  core:
    http:
      enabled: true
      port: 18082
      host: localhost
      authentication:
        type: basic
        users:
          admin: internal-api-password

  sync:
    delay: 5000
    unit: MILLISECONDS
    distributed: false # By enabling this mode, data synchronization process is distributed over clustered API Gateways.
    bulk_items: 100 # Defines the number of items to retrieve during synchronization (events, plans, api keys, ...).

  local:
    enabled: false
    path: ${gravitee.home}/apis # The path to API descriptors

  monitoring:
    delay: 5000
    unit: MILLISECONDS
    distributed: false # By enabling this mode, data monitoring gathering process is distributed over clustered API Gateways.

  metrics:
    enabled: false
    prometheus:
      enabled: true

  tracing:
    enabled: false

api:
  properties:
    encryption:
      secret: your-own-api-32-characters-secret

alerts:
  alert-engine:
    enabled: true
    ws:
      discovery: true
      endpoints:
        - https://alert-engine-url:alert-engine-port
      security:
        username: alert-engine-username
        password: alert-engine-password

classloader:
  legacy:
    enabled: false
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Installing Redis to use with your Hybrid Deployment <a href="#redis" id="redis"></a>

{% tabs %}
{% tab title="Kubernetes (Helm)" %}
* To install Redis, go to [Bitnami Helm charts](https://artifacthub.io/packages/helm/bitnami/redis).
{% endtab %}

{% tab title="Docker" %}
{% code title="docker-compose.yaml" lineNumbers="true" %}
```yaml
version: '3'

volumes:
  data-redis:

services:
  redis:
    # https://hub.docker.com/_/redis?tab=tags
    image: redis:${REDIS_VERSION:-7.2.1-alpine}
    container_name: gio_apim_hybrid_redis
    hostname: redis
    restart: always
    ports:
      - '6379:6379'
    command: redis-server --requirepass ${REDIS_PASS:-28kjzEGquZYrztGyPMofR8eWuNbn4YqR}
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 1s
      timeout: 3s
      retries: 30
    volumes: 
      - data-redis:/data
```
{% endcode %}
{% endtab %}

{% tab title="VM" %}
* To install Redis, go to [redis.io](https://redis.io/docs/latest/get-started/).
{% endtab %}
{% endtabs %}

## Downloading Logstash to use with your Hybrid deployment <a href="#logstash" id="logstash"></a>

{% tabs %}
{% tab title="Kubernetes (Helm)" %}
* To install Logstash, go to either of the following websites:
  * [Official Helm charts](https://artifacthub.io/packages/helm/elastic/logstash#how-to-install-oss-version-of-logstash)
  * [Bitnami Helm charts](https://bitnami.com/stack/logstash/helm)
{% endtab %}

{% tab title="Docker" %}
{% code title="docker-compose.yaml" lineNumbers="true" %}
```yaml
version: '3'

services:
  logstash:
    # https://www.docker.elastic.co/r/logstash/logstash-oss 
    image: docker.elastic.co/logstash/logstash-oss:${LOGSTASH_VERSION:-8.10.2}
    container_name: gio_apim_hybrid_logstash
    hostname: logstash
    ports:
      - "8379:8379"
    healthcheck:
      test: curl -f -I http://localhost:9600/_node/pipelines/main || exit 1
      start_period: 20s
      interval: 3s
      timeout: 5s
      retries: 30
    volumes:
      - ./config/logstash:/usr/share/logstash/pipeline:ro
    environment:
      LS_JAVA_OPTS: "-Xmx256m -Xms256m"
```
{% endcode %}
{% endtab %}

{% tab title="VM" %}
* To install Logstash, go to [Download Logstash - OSS only](https://www.elastic.co/downloads/logstash-oss).
{% endtab %}
{% endtabs %}

### Configuring Logstash <a href="#configuration_2" id="configuration_2"></a>

{% hint style="info" %}
* For more information about configuring logstash, see [Configuring Logstash](https://www.elastic.co/guide/en/logstash/current/configuration.html).
{% endhint %}

To configure logstash for you environment, copy the following example:

{% code title="logstash.conf" lineNumbers="true" %}
```
input {
  tcp {
      port => 8379
      codec => "json_lines"
  }
}

filter {
    if [type] != "request" or [type] != "v4-metrics" {
        mutate { remove_field => ["path", "host"] }
    }
}

output {
  s3 {
    access_key_id => "${S3_ACEESS_KEY_ID}"
    secret_access_key => "${S3_SECRET_ACCESS_KEY}"
    region => "${S3_REGION}"
    bucket => "${S3_BUCKET_NAME}"
    rotation_strategy => time
    time_file => 1
    codec => "json_lines"
  }
}
```
{% endcode %}

## Installing Fluentd to use with your Hybrid deployment <a href="#fluentd" id="fluentd"></a>

{% tabs %}
{% tab title="Kubernetes (Helm)" %}
* To install Fluentd, go to either of the following sites:
  * [Official Helm charts](https://artifacthub.io/packages/helm/fluent/fluentd)
  * [Bitnami Helm charts](https://bitnami.com/stack/fluentd/helm)
{% endtab %}

{% tab title="Docker" %}
To install Fluentd using Docker, you must build a docker image.&#x20;

{% code title="Dockerfile" lineNumbers="true" %}
```
FROM fluent/fluentd:v1.16.2-1.0
USER root
RUN ["gem", "install", "fluent-plugin-s3"]
USER fluent
```
{% endcode %}

{% code title="docker-compose.yaml" lineNumbers="true" %}
```yaml
version: '3'

services:
  fluentd:
    image: fluentd:s3
    container_name: gio_apim_fluentd
    hostname: fluentd
    restart: always
    ports:
      - "9000:9000"
    volumes:
      - ./fluentd_conf:/fluentd/etc
```
{% endcode %}
{% endtab %}

{% tab title="VM" %}
[Download Fluentd](https://www.fluentd.org/download)
{% endtab %}
{% endtabs %}

### Configuration

{% code title="fluentd.conf" lineNumbers="true" %}
```
<source>
  @type tcp
  tag tcp
  <parse>
    @type json
  </parse>
  port 9000
</source>

<match *.**>
  @type s3
  aws_key_id "xxxxxxxxxxxxxxx"
  aws_sec_key "xxxxxxxxxxxxxxx"
  s3_bucket "my-s3-bucket"
  s3_region "my-s3-region"
  
  path /
  time_slice_format %Y%m%d%H
  time_slice_wait 10m
  time_format %Y%m%d%H%M

  buffer_type file
  buffer_path /fluentd/log
  buffer_chunk_limit 256m
  buffer_queue_limit 512
  flush_interval 10s
  flush_at_shutdown true
  
  <format>
    @type json
  </format>
</match>
```
{% endcode %}

{% hint style="info" %}
**Additional assets**

* [Configuring Fluentd](https://docs.fluentd.org/)
{% endhint %}
