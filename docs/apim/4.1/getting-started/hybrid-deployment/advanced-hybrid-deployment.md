---
description: A detailed guide for installing and configuring a hybrid APIM deployment
---

# Advanced Hybrid Deployment

## Introduction

This page focuses on the installation of the Self-Hosted Data-Plane, which is part of the API Management platform in a hybrid architecture (SaaS Control-Plane + Self-Hosted Data-Plane).

<img src="../../.gitbook/assets/file.excalidraw (4).svg" alt="" class="gitbook-drawing">

### SaaS Control-Plane components <a href="#saas-components" id="saas-components"></a>

<table><thead><tr><th width="228" align="center">Component</th><th>Description</th></tr></thead><tbody><tr><td align="center">APIM Console<br>(for API producers)</td><td>This web UI gives easy access to some key APIM Management API services. <a href="../../#api-publisher">API publishers</a> can use it to publish APIs.<br>Administrators can also configure global platform settings and specific portal settings.</td></tr><tr><td align="center">APIM Management API</td><td>This RESTful API exposes services to manage and configure the APIM Console and APIM Developer Portal web UIs.<br>All exposed services are restricted by authentication and authorization rules. For more information, see the<a href="../../reference/management-api-reference.md"> Management API Reference</a> section.</td></tr><tr><td align="center"><a href="../../guides/developer-portal/">APIM Developer Portal</a><br>(for API consumers)</td><td>This web UI gives easy access to some key APIM API services. It allows <a href="../../#api-consumer">API Consumers</a> to <a href="../../guides/api-exposure-plans-applications-and-subscriptions/#applications">manage their applications</a> and search for, view, try out, and subscribe to a published API.</td></tr><tr><td align="center">APIM SaaS API Gateways</td><td>APIM Gateway is the core component of the APIM platform. You can think of it like a smart reverse proxy.<br>Unlike a traditional HTTP proxy, APIM Gateway has the capability to apply <a href="../../guides/policy-design/">policies</a> (i.e., rules or logic) to both the request and response phases of an API transaction. With these policies, you can transform, secure, monitor, etc., your APIs.</td></tr><tr><td align="center">Bridge Gateways</td><td>A <em>bridge</em> API Gateway exposes extra HTTP services for bridging HTTP calls to the underlying repository (which can be any of our supported repositories: MongoDB, JDBC, etc.)</td></tr><tr><td align="center">Config Database</td><td>All the API Management platform management data, such as API definitions, users, applications, and plans.</td></tr><tr><td align="center">S3 Bucket + Analytics Database</td><td>Analytics and logs data.</td></tr><tr><td align="center">Gravitee Cockpit</td><td>Gravitee Cockpit is a centralized, multi-environments / organizations tool for managing all your Gravitee API Management and Access Management installations in a single place.</td></tr><tr><td align="center">[Optional]<br>API Designer</td><td>Drag-and-Drop graphical (MindMap) API designer to quickly and intuitively design your APIs (Swagger / OAS) and deploy mocked APIs for quick testing.</td></tr><tr><td align="center">[Optional]<br>Alert Engine</td><td>Alert Engine (AE) provides APIM and AM users with efficient and flexible API platform monitoring, including advanced alerting configuration and notifications sent through their preferred channels, such as email, Slack and using Webhooks.<br>AE does not require any external components or a database as it does not store anything. It receives events and sends notifications under the conditions which have been pre-configured upstream with triggers.</td></tr></tbody></table>

### Self-Hosted Data-Plane components[¶](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#on-prem-private-cloud-components) <a href="#on-prem-private-cloud-components" id="on-prem-private-cloud-components"></a>

<table><thead><tr><th width="133" align="center">Component</th><th>Description</th></tr></thead><tbody><tr><td align="center">APIM Gateway</td><td>APIM Gateway is the core component of the APIM platform. You can think of it like a smart reverse proxy.<br><br>Unlike a traditional HTTP proxy, APIM Gateway has the capability to apply <a href="../../guides/policy-design/">policies</a> (i.e., rules or logic) to both the request and response phases of an API transaction. With these policies, you can transform, secure, monitor, etc., your APIs.</td></tr><tr><td align="center">Logstash</td><td>Collect and send local Gateway logs and metrics to the Gravitee APIM SaaS Control Plane.</td></tr><tr><td align="center">Redis</td><td>The database used locally for rate limit synchronized counters (RateLimit, Quota, Spike Arrest) and, optionally, as an external cache for the Cache policy.</td></tr></tbody></table>

<img src="../../.gitbook/assets/file.excalidraw (1) (1).svg" alt="Hybrid architecture connections" class="gitbook-drawing">

## Self-Hosted Hybrid Gateway <a href="#installation" id="installation"></a>

### Installation <a href="#installation" id="installation"></a>

{% hint style="danger" %}
Make sure the version you are installing aligns with the Control-Plane SaaS version.
{% endhint %}

{% hint style="info" %}
Don't forget to add the Gravitee.io License file.
{% endhint %}

{% tabs %}
{% tab title="Kubernetes (Helm)" %}
* Follow the APIM installation instructions in the [Install on Kubernetes](../install-guides/install-on-kubernetes/) guide.
* Install **only the Gateway** and disable the other components in your `values.yaml` configuration file.

{% hint style="info" %}
**Additional assets**

* [Hybrid Deployment on Kubernetes](hybrid-deployment-on-kubernetes.md)
* [Gravitee Helm charts](https://artifacthub.io/packages/helm/graviteeio/apim3)
{% endhint %}
{% endtab %}

{% tab title="Docker" %}
Follow the APIM installation instructions in the [Install on Docker](../install-guides/install-on-docker/) guide.

{% hint style="info" %}
**Download and mount the required plugins for the Gravitee.io Gateway:**

* [Redis Repository](https://download.gravitee.io/#graviteeio-apim/plugins/repositories/gravitee-apim-repository-redis): The database used locally for rate limits synchronized counters
* [TCP Reporter](https://download.gravitee.io/#graviteeio-ee/apim/plugins/reporters/gravitee-reporter-tcp/): To push events to Logstash
{% endhint %}
{% endtab %}

{% tab title="VM" %}
Follow the APIM installation instructions in the [Install with `.ZIP`](docs/apim/4.1/getting-started/install-guides/install-with-.zip.md) guide.

{% hint style="info" %}
**Download and mount the required plugins for the Gravitee.io Gateway:**

* [Redis Repository](https://download.gravitee.io/#graviteeio-apim/plugins/repositories/gravitee-apim-repository-redis): The database used locally for rate limits synchronized counters
* [TCP Reporter](https://download.gravitee.io/#graviteeio-ee/apim/plugins/reporters/gravitee-reporter-tcp/): To push events to Logstash
{% endhint %}
{% endtab %}
{% endtabs %}

### Configuration <a href="#configuration" id="configuration"></a>

There are at least 3 connections to configure:

* The connection to the SaaS Control-Plane via the Bridge Gateway.
* The connection to push Analytics and Logs using the file or TCP reporter to push data to Logstash and send to the SaaS storage.
* The connection to the local rate limits database (Redis).
* (Optional) The connection to the SaaS Alert Engine.

#### **Management (SaaS Control-Plane Bridge Gateway)**[**¶**](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#management)

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
      username: kubernetes://<namespace>/secrets/<my-secret-name>/<my-secret-key>
      password: kubernetes://<namespace>/secrets/<my-secret-name>/<my-secret-key>
      # ssl:
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

* [Hybrid deployment on Kubernetes](hybrid-deployment-on-kubernetes.md)
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
      basic:
        username: bridge-gateway-username
        password: bridge-gateway-password
    # ssl:
    #   trustAll: true
    #   verifyHostname: true
    #   keystore:
    #     type: # can be jks / pem / pkcs12
    #     path:
    #     password:
    #   truststore:
    #     type: # can be jks / pem / pkcs12
    #     path:
    #     password:
```
{% endcode %}
{% endtab %}
{% endtabs %}

#### **Analytics and Logs**

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

#### **Rate limits**

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

#### **Alert Engine**

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

### **Configuration: Full example**

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
      username: kubernetes://<namespace>/secrets/<my-secret-name>/<my-secret-key>
      password: kubernetes://<namespace>/secrets/<my-secret-name>/<my-secret-key>
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
    username: kubernetes://<namespace>/secrets/<my-secret-name>/<my-secret-key>
    password: kubernetes://<namespace>/secrets/<my-secret-name>/<my-secret-key>
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

## Redis <a href="#redis" id="redis"></a>

### Installation <a href="#redis" id="redis"></a>

{% tabs %}
{% tab title="Kubernetes (Helm)" %}
[Bitnami Helm charts](https://artifacthub.io/packages/helm/bitnami/redis)
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
[Installing Redis from redis.io](https://redis.io/docs/getting-started/installation/)
{% endtab %}
{% endtabs %}

## Logstash <a href="#logstash" id="logstash"></a>

### Installation <a href="#installation_2" id="installation_2"></a>

{% tabs %}
{% tab title="Kubernetes (Helm)" %}
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
[Download Logstash OSS](https://www.elastic.co/downloads/logstash-oss)
{% endtab %}
{% endtabs %}

### Configuration <a href="#configuration_2" id="configuration_2"></a>

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

{% hint style="info" %}
**Additional assets**

* [Configuring Logstash](https://www.elastic.co/guide/en/logstash/current/configuration.html)
{% endhint %}

## Fluentd <a href="#fluentd" id="fluentd"></a>

### Installation

{% tabs %}
{% tab title="Kubernetes (Helm)" %}
* [Official Helm charts](https://artifacthub.io/packages/helm/fluent/fluentd)
* [Bitnami Helm charts](https://bitnami.com/stack/fluentd/helm)
{% endtab %}

{% tab title="Docker" %}
You have to build your own docker image:

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
