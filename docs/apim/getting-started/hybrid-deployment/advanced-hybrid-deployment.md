---
description: A detailed guide for installing and configuring a hybrid APIM deployment
---

# Advanced Hybrid Deployment

## Introduction

This documentation page relates to the installation of the client (On-Prem / Private Cloud) part of the API Management platform in a Hybrid architecture (SaaS + On-prem / Private cloud).

![Hybrid Architecture](https://dobl1.github.io/gravitee-se-docs/assets/hybrid-architecture.svg)

### SaaS Components <a href="#saas-components" id="saas-components"></a>

|                                             Component                                            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| :----------------------------------------------------------------------------------------------: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|                            <p>APIM Console<br>(for API producers)</p>                            | <p>This web UI gives easy access to some key APIM Management API services. <a href="../../#api-publisher">API publishers</a> can use it to publish APIs.<br>Administrators can also configure global platform settings and specific portal settings.</p>                                                                                                                                                                                                                |
|                                        APIM Management API                                       | <p>This RESTful API exposes services to manage and configure the APIM Console and APIM Developer Portal web UIs.<br>All exposed services are restricted by authentication and authorization rules. For more information, see the<a href="../../reference/management-api-reference.md"> Management API Reference</a> section.</p>                                                                                                                                        |
| <p><a href="../../guides/developer-portal/">APIM Developer Portal</a><br>(for API consumers)</p> | This web UI gives easy access to some key APIM API services. Allows [API Consumers](../../#api-consumer) to [manage their applications](../../guides/api-exposure-plans-applications-and-subscriptions/#applications) and search for, view, try out, and subscribe to a published API.                                                                                                                                                                                  |
|                                      APIM SaaS API Gateways                                      | <p>APIM Gateway is the core component of the APIM platform. You can think of it like a smart reverse proxy.<br><br>Unlike a traditional HTTP proxy, APIM Gateway has the capability to apply <a href="../../reference/policy-reference/">policies</a> (i.e., rules or logic) to both the request and response phases of an API transaction. With these policies, you can transform, secure, monitor, etc., your APIs.</p>                                               |
|                                          Bridge Gateways                                         | A _bridge_ API Gateway exposes extra HTTP services for bridging HTTP calls to the underlying repository (which can be any of our supported repositories: MongoDB, JDBC, etc.)                                                                                                                                                                                                                                                                                           |
|                                          Config Database                                         | All the API Management platform management data, such as API definitions, users, applications, and plans.                                                                                                                                                                                                                                                                                                                                                               |
|                                  S3 Bucket + Analytics Database                                  | Analytics and logs data                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|                                <p>[Optional]<br>Gravitee Cloud</p>                               | Gravitee Cloud is a centralized, multi-environments / organizations tool for managing all your Gravitee API Management and Access Management installations in a single place.                                                                                                                                                                                                                                                                                           |
|                                 <p>[Optional]<br>API Designer</p>                                | Drag-and-Drop graphical (MindMap) API designer to quickly and intuitively design your APIs (Swagger / OAS) and deploy mocked APIs for quick testing.                                                                                                                                                                                                                                                                                                                    |
|                                 <p>[Optional]<br>Alert Engine</p>                                | <p>Alert Engine (AE) provides APIM and AM users with efficient and flexible API platform monitoring, including advanced alerting configuration and notifications sent through their preferred channels, such as email, Slack and using Webhooks.<br>AE does not require any external components or a database as it does not store anything. It receives events and sends notifications under the conditions which have been pre-configured upstream with triggers.</p> |

### On-prem / Private cloud components[¶](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#on-prem-private-cloud-components) <a href="#on-prem-private-cloud-components" id="on-prem-private-cloud-components"></a>

|   Component  | Description                                                                                                                                                                                                                                                                                                                                                                                                               |
| :----------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| APIM Gateway | <p>APIM Gateway is the core component of the APIM platform. You can think of it like a smart reverse proxy.<br><br>Unlike a traditional HTTP proxy, APIM Gateway has the capability to apply <a href="../../reference/policy-reference/">policies</a> (i.e., rules or logic) to both the request and response phases of an API transaction. With these policies, you can transform, secure, monitor, etc., your APIs.</p> |
|   Logstash   | Collect and send local Gateways logs and metrics to the Gravitee APIM SaaS Control Plane.                                                                                                                                                                                                                                                                                                                                 |
|     Redis    | The database used locally for rate limits synchronized counters (RateLimit, Quota, Spike Arrest) and optionally, as an external cache for the Cache policy.                                                                                                                                                                                                                                                               |

![Hybrid Architecture Connections](https://dobl1.github.io/gravitee-se-docs/assets/hybrid-architecture-connections.svg)

## Self-hosted hybrid gateway installation[¶](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#installation) <a href="#installation" id="installation"></a>

{% tabs %}
{% tab title="Kubernetes (Helm)" %}
Please follow the APIM install instructions laid out in the [Install on Kubernetes](../install-guides/install-on-kubernetes/) guide.

{% hint style="info" %}
**Additional assets**

* [Hybrid Deployment on Kubernetes](hybrid-deployment-on-kubernetes.md)
* [Gravitee Helm charts](https://artifacthub.io/packages/helm/graviteeio/apim3)
{% endhint %}
{% endtab %}

{% tab title="Docker" %}
Please follow the APIM install instructions laid out in the [Install on Docker](../install-guides/install-on-docker/) guide.

#### **Local file structure**

```
.
├── config
│   ├── gateway
│   │   └── gravitee.yml 

│   └── logstash
│       └── logstash.conf

├── docker-compose.yml
├── logs
│   └── apim-gateway-dev
└── plugins
    ├── gravitee-apim-repository-hazelcast-3.18.3.zip
    └── gravitee-apim-repository-redis-3.18.3.zip
```

#### **Download**&#x20;

**Download plugins**

* [gravitee-apim-repository-redis-3.18.3.zip](https://download.gravitee.io/graviteeio-apim/plugins/repositories/gravitee-apim-repository-redis/gravitee-apim-repository-redis-3.18.3.zip)

#### **plugins**

**Download plugins**

*   [gravitee-apim-repository-redis-3.18.3.zip](https://download.gravitee.io/graviteeio-apim/plugins/repositories/gravitee-apim-repository-redis/gravitee-apim-repository-redis-3.18.3.zip)

    **Download plugins**

    *   [gravitee-apim-repository-redis-3.18.3.zip](https://download.gravitee.io/graviteeio-apim/plugins/repositories/gravitee-apim-repository-redis/gravitee-apim-repository-redis-3.18.3.zip)

        **Download plugins**

        * [gravitee-apim-repository-redis-3.18.3.zip](https://download.gravitee.io/graviteeio-apim/plugins/repositories/gravitee-apim-repository-redis/gravitee-apim-repository-redis-3.18.3.zip)
        *
* [gravitee-apim-repository-redis-3.18.3.zip](https://download.gravitee.io/graviteeio-apim/plugins/repositories/gravitee-apim-repository-redis/gravitee-apim-repository-redis-3.18.3.zip)
* [gravitee-apim-repository-hazelcast-3.18.3.zip](https://download.gravitee.io/graviteeio-apim/plugins/repositories/gravitee-apim-repository-hazelcast/gravitee-apim-repository-hazelcast-3.18.3.zip)
{% endtab %}

{% tab title="ZIP" %}
Please follow the APIM install instructions laid out in the [Install with `.ZIP`](../install-guides/install-with-.zip.md) guide.

**Download plugins**

* [gravitee-apim-repository-redis-3.18.3.zip](https://download.gravitee.io/graviteeio-apim/plugins/repositories/gravitee-apim-repository-redis/gravitee-apim-repository-redis-3.18.3.zip)
{% endtab %}
{% endtabs %}



## Configuration[¶](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#configuration) <a href="#configuration" id="configuration"></a>

There are at least 3 connections to configure:

* The connection to the SaaS Management plane with the Bridge Gateway.
* The connection to push Analytics and Logs using the file or TCP reporter to push data for Logstash and send to the SaaS storage.
* The connection to the local rate limits database (Redis).

Additionally, you can optionally configure a connection to Alert Engine and Gravitee Cloud.

* \[Optional] The connection to the SaaS Alert Engine.

### **Management**[**¶**](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#management)

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

* [Hybrid Deployment on Kubernetes](hybrid-deployment-on-kubernetes.md)
* [Gravitee Helm charts](https://artifacthub.io/packages/helm/graviteeio/apim3)
{% endhint %}
{% endtab %}

{% tab title="Docker" %}
{% code title="docker-compose.yaml" lineNumbers="true" %}
```yaml
version: '3.5'

services:
  gateway:
    image: graviteeio/apim-gateway:${APIM_VERSION:-3.18.3}
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

{% tab title="ZIP" %}
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
    ssl:
      trustAll: true
      verifyHostname: true
      keystore:
        type: # can be jks / pem / pkcs12
        path:
        password:
      trustore:
        type: # can be jks / pem / pkcs12
        path:
        password:

```
{% endcode %}
{% endtab %}
{% endtabs %}

### **Analytics and Logs**[**¶**](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#analytics-and-logs)

{% tabs %}
{% tab title="Kubernetes (Helm)" %}
{% code title="values.yaml" lineNumbers="true" %}
```yaml
gateway:
  reporters:
    tcp:
      enabled: true
      host: logstash
      port: 8379
      output: elasticsearch
```
{% endcode %}
{% endtab %}

{% tab title="Docker" %}
{% code title="docker-compose.yaml" overflow="wrap" %}
```yaml
version: '3.5'

services:
  gateway:
    image: graviteeio/apim-gateway:${APIM_VERSION:-3.18.3}
    container_name: gio_apim_gateway
    restart: always
    ports:
      - "8082:8082"
    environment:
      # --- LOGSTASH ---
      - gravitee_reporters_elasticsearch_enabled=false
      - gravitee_reportealert-engine-usernamers_tcp_enabled=true
      - gravitee_reporters_tcp_host=logstash
      - gravitee_reporters_tcp_port=8379
      - gravitee_reporters_tcp_output=elasticsearch
```
{% endcode %}
{% endtab %}

{% tab title="ZIP" %}
{% code title="gravitee.yaml" lineNumbers="true" %}
```yaml
reporters:
  elasticsearch:
    enabled: false # Is the reporter enabled or not (default to true)
  tcp:
    enabled: true
    host: logstash-host
    port: logstash-port
    output: elasticsearch
```
{% endcode %}
{% endtab %}
{% endtabs %}

### **Rate limits**

{% tabs %}
{% tab title="Kubernetes (Helm)" %}
{% code title="values.yaml" lineNumbers="true" %}
```yaml
ratelimit:
  type: redis
redis:
  host: 'redis-host'
  port: 6379
  password: 'redis-password'
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
version: '3.5'

services:
  gateway:
    image: graviteeio/apim-gateway:${APIM_VERSION:-3.18.3}
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

{% tab title="ZIP" %}
{% code title="gravitee.yaml" lineNumbers="true" %}
```yaml
ratelimit:
  # type: hazelcast
  type: redis
  redis:
    host: redis-host
    port: 6379
    password: redis-password
```
{% endcode %}
{% endtab %}
{% endtabs %}

### **Alert Engine**

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
    username: alert-engine-username
    password: alert-engine-password
```
{% endcode %}
{% endtab %}

{% tab title="Docker" %}
{% code title="docker-compose.yaml" lineNumbers="true" %}
```yaml
version: '3.5'

services:
  gateway:
    image: graviteeio/apim-gateway:${APIM_VERSION:-3.18.3}
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

{% tab title="ZIP" %}
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

### **Gravite Cloud**

Please head over to our Gravitee Cloud documentation to get started.

### **Full example**

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
    username: alert-engine-username
    password: alert-engine-password
```
{% endcode %}
{% endtab %}

{% tab title="Docker" %}
{% code title="docker-compose.yaml" lineNumbers="true" %}
```yaml
version: '3.5'

services:
  gateway:
    image: graviteeio/apim-gateway:${APIM_VERSION:-3.18.3}
    container_name: gio_apim_gateway
    restart: always
    ports:
      - "8082:8082"
    depends_on:
      - rate-limit
      - logstash
    volumes:
      # --- LOCAL LOG FILES ---
      - ./logs/apim-gateway-dev:/opt/graviteeio-gateway/logs
      # --- EE LICENSE FILE ---
      # - ${GIO_LICENSE}:/opt/graviteeio-gateway/license/license.key
      # --- ADDITIONAL PLUGINS ---
      - ./plugins:/opt/graviteeio-gateway/plugins-ext
      - ./config/gateway/gravitee.yml:/opt/graviteeio-gateway/config/gravitee.yml:ro
    environment:
      # --- PLUGINS LOCATIONS ---
      - gravitee_plugins_path_0=/opt/graviteeio-gateway/plugins
      - gravitee_plugins_path_1=/opt/graviteeio-gateway/plugins-ext
      # --- COCKPIT ORGS & ENVS ---
      - gravitee_organizations=dorian-se
      - gravitee_environments=dev
      # --- SHARDING TAGS & TENANTS ---
      - gravitee_tags=internal
      # - gravitee_tenant=xxx
      # --- BRIDGE GATEWAYS ---
      - gravitee_management_type=http
      - gravitee_management_http_url=https://bridge-gateway-url:bridge-gateway-port
      - gravitee_management_http_authentication_basic_username=bridge-gateway-username
      - gravitee_management_http_authentication_basic_password=bridge-gateway-password
      # --- RATE LIMIT REPO ---
      - gravitee_ratelimit_type=redis
      - gravitee_ratelimit_redis_host=rate-limit
      - gravitee_ratelimit_redis_port=6379
      - gravitee_ratelimit_redis_password=${REDIS_PASS:-redis-password}
      # - gravitee_ratelimit_type=hazelcast
      # --- LOGSTASH ---
      - gravitee_reporters_elasticsearch_enabled=false
      - gravitee_reportealert-engine-usernamers_tcp_enabled=true
      - gravitee_reporters_tcp_host=logstash
      - gravitee_reporters_tcp_port=8379
      - gravitee_reporters_tcp_output=elasticsearch
      # --- ALERT ENGINE ---
      # - gravitee_alerts_alertengine_enabled=true
      # - gravitee_alerts_alertengine_ws_discovery=true
      # - gravitee_alerts_alertengine_ws_endpoints_0=https://alert-engine-url:alert-engine-port
      # - gravitee_alerts_alertengine_ws_security_username=alert-engine-username
      # - gravitee_alerts_alertengine_ws_security_password=alert-engine-password
      # --- SECRETS ---
      - gravitee_api_properties_encryption_secret=your-own-api-32-caracters-secret

  rate-limit:
    # https://hub.docker.com/_/redis?tab=tags
    image: redis:${REDIS_VERSION:-7.0.4-alpine3.16}
    container_name: gio_ratelimit_redis
    hostname: redis
    restart: always
    ports:
      - '6379:6379'
    command: redis-server --requirepass ${REDIS_PASS:-redis-password}
    volumes: 
      - redis_data:/data

  logstash:
    # https://www.docker.elastic.co/r/logstash/logstash-oss 
    image: docker.elastic.co/logstash/logstash-oss:8.3.2
    ports:
      - "8379:8379"
    volumes:
      - ./config/logstash:/usr/share/logstash/pipeline:ro
    environment:
      LS_JAVA_OPTS: "-Xmx256m -Xms256m"

volumes:
  redis_data:
    driver: local
```
{% endcode %}
{% endtab %}

{% tab title="ZIP" %}
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
    distributed: false # By enabling this mode, data synchronization process is distributed over clustered API gateways.
    bulk_items: 100 # Defines the number of items to retrieve during synchronization (events, plans, api keys, ...).

  local:
    enabled: false
    path: ${gravitee.home}/apis # The path to API descriptors

  monitoring:
    delay: 5000
    unit: MILLISECONDS
    distributed: false # By enabling this mode, data monitoring gathering process is distributed over clustered API gateways.

  metrics:
    enabled: false
    prometheus:
      enabled: true

  tracing:
    enabled: false

api:
  properties:
    encryption:
      secret: your-own-api-32-caracters-secret

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

## Redis Installation <a href="#redis" id="redis"></a>

{% tabs %}
{% tab title="Kubernetes (Helm)" %}
[Bitnami helm charts](https://artifacthub.io/packages/helm/bitnami/redis)
{% endtab %}

{% tab title="Docker" %}
{% code title="docker-compose.yaml" lineNumbers="true" %}
```yaml
version: '3.5'

services:
  rate-limit:
    # https://hub.docker.com/_/redis?tab=tags
    image: redis:${REDIS_VERSION:-7.0.4-alpine3.16}
    container_name: gio_ratelimit_redis
    hostname: redis
    restart: always
    ports:
      - '6379:6379'
    command: redis-server --requirepass ${REDIS_PASS:-redis-password}
    volumes: 
      - redis_data:/data

volumes:
  redis_data:
    driver: local
```
{% endcode %}
{% endtab %}

{% tab title="ZIP" %}
[Installing Redis from redis.io](https://redis.io/docs/getting-started/installation/)
{% endtab %}
{% endtabs %}

## Logstash <a href="#logstash" id="logstash"></a>

### Installation <a href="#installation_2" id="installation_2"></a>

{% tabs %}
{% tab title="Kubernetes (Helm)" %}
* [Official helm charts](https://artifacthub.io/packages/helm/elastic/logstash#how-to-install-oss-version-of-logstash)
* [Bitnami helm charts](https://bitnami.com/stack/logstash/helm)
{% endtab %}

{% tab title="Docker" %}
{% code title="docker-compose.yaml" lineNumbers="true" %}
```yaml
version: '3.5'

services:
  logstash:
    # https://www.docker.elastic.co/r/logstash/logstash-oss 
    image: docker.elastic.co/logstash/logstash-oss:8.3.2
    ports:
      - "8379:8379"
    volumes:
      - ./config/logstash:/usr/share/logstash/pipeline:ro
    environment:
      LS_JAVA_OPTS: "-Xmx256m -Xms256m"Download Logstash OSS
```
{% endcode %}
{% endtab %}

{% tab title="ZIP" %}
[Download Logstash OSS](https://www.elastic.co/downloads/logstash-oss)
{% endtab %}
{% endtabs %}

### Configuration[¶](https://dobl1.github.io/gravitee-se-docs/api-management/install/hybrid/#configuration\_2) <a href="#configuration_2" id="configuration_2"></a>

{% code title="logstash.conf" lineNumbers="true" %}
```
input {
  tcp {
      port => 8379
      codec => "json"
  }
}

filter {
    if [type] != "request" {
        mutate { remove_field => ["path", "host"] }
    }
}

output {
  s3 {
    access_key_id => "${S3_ACEESS_KEY_ID}"
    secret_access_key => "${S3_SECRET_ACCESS_KEY}"
    region => "${S3_REGION}"
    bucket => "${S3_BUCKET_NAME}"
    size_file => 10485760
    codec => "json_lines"
  }
}
```
{% endcode %}

{% hint style="info" %}
**Additional assets**

* [Configuring Logstash](https://www.elastic.co/guide/en/logstash/current/configuration.html)
{% endhint %}
