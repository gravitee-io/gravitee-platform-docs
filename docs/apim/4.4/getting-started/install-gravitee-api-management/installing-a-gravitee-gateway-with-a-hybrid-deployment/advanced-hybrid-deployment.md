---
description: Installing and configuring a hybrid API Management deployment
---

# Installing a Gravitee Gateway with a standard Hybrid Deployment

## Installing your Self-Hosted Hybrid Gateway

{% hint style="danger" %}
Make sure that the version you install is compatible with the Control-Plane SaaS version. For more information about compatibility, see [Components of Hybrid Architecture](https://documentation.gravitee.io/apim/getting-started/install-gravitee-api-management/installing-a-gravitee-gateway-with-a-hybrid-deployment#components-of-hybrid-architecture).
{% endhint %}

{% hint style="info" %}
Ensure that you add the Gravitee.io License file.
{% endhint %}

{% tabs %}
{% tab title="Kubernetes (Helm)" %}
* Install Gravitee API Management (APIM). For more information about installing Gravitee APIM, see [Installing Gravitee API Management on Kubernetes](../../../installation-and-upgrades/install-gravitee-api-management/installing-gravitee-api-management-on-premise/install-on-kubernetes.md).
* Install **only the Gateway** and disable the other components in your `values.yaml` configuration file.

{% hint style="info" %}
**Additional assets**

* [Hybrid Deployment on Kubernetes](../../../installation-and-upgrades/install-gravitee-api-management/installing-a-gravitee-gateway-with-a-hybrid-deployment/hybrid-deployment-on-kubernetes.md)
* [Gravitee Helm charts](https://artifacthub.io/packages/helm/graviteeio/apim3)
{% endhint %}
{% endtab %}

{% tab title="Docker" %}
* Install Gravitee API Management (APIM). For more information about installing Gravitee APIM, see[ Installing Gravitee API Management with Docker](../../../installation-and-upgrades/install-gravitee-api-management/installing-gravitee-api-management-on-premise/install-on-docker/README.md).
* Download, and then mount the following plugins for the Gravitee Gateway:
  * Redis Repository. This repository is used for the rate limits' synchronized counters. To download this repository, go to [Gravitee.io Downloads](https://download.gravitee.io/#graviteeio-apim/plugins/repositories/gravitee-apim-repository-redis).
  * TCP Reporter. This repository is used to push events to Logstash. To download this repository, go to [Gravitee.io Downloads.](https://download.gravitee.io/#graviteeio-ee/apim/plugins/reporters/gravitee-reporter-tcp/)
{% endtab %}

{% tab title="VM" %}
* Install Gravitee API Management (APIM). For more information about installing Gravitee APIM, see [Installing Gravitee API Management with .ZIP](../../../installation-and-upgrades/install-gravitee-api-management/installing-gravitee-api-management-on-premise/install-with-.zip.md).
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

* Replace \<my-secret-name> with the name of the secret for your environment.
* Replace \<my-secret-key> with the secret's key for you environment.

{% hint style="info" %}
**Additional assets**

* [Hybrid deployment on Kubernetes](../../../installation-and-upgrades/install-gravitee-api-management/installing-a-gravitee-gateway-with-a-hybrid-deployment/hybrid-deployment-on-kubernetes.md)
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

* Replace \<VERSION-ALIGNED-WITH-CONTROL-PLANE> with the version of the gateway that aligns with your control plane. For more information about compatibility versions, see[ Components of Hybrid Architecture](https://documentation.gravitee.io/apim/getting-started/install-gravitee-api-management/installing-a-gravitee-gateway-with-a-hybrid-deployment#components-of-hybrid-architecture).
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
      # --- LOGSTASH ---
      - gravitee_reporters_elasticsearch_enabled=false
      - gravitee_reporters_tcp_enabled=true
      - gravitee_reporters_tcp_host=logstash-host
      - gravitee_reporters_tcp_port=8379
      - gravitee_reporters_tcp_output=elasticsearch
```
{% endcode %}

* Replace \<VERSION-ALIGNED-WITH-CONTROL-PLANE> with the version of the gateway that aligns with your control plane. For more information about compatibility versions, see[ Components of Hybrid Architecture](https://documentation.gravitee.io/apim/getting-started/install-gravitee-api-management/installing-a-gravitee-gateway-with-a-hybrid-deployment#components-of-hybrid-architecture).
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

* Replace \<my-secret-name> with the name of the secret for your environment.
* Replace \<my-secret-key> with the secret's key for you environment.

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
      - gravitee_ratelimit_redis_password=$<REDIS_PASS:-redis-password>
      
```
{% endcode %}

* Replace \<VERSION-ALIGNED-WITH-CONTROL-PLANE> with the version of the gateway that aligns with your control plane. For more information about compatibility versions, see[ Components of Hybrid Architecture](https://documentation.gravitee.io/apim/getting-started/install-gravitee-api-management/installing-a-gravitee-gateway-with-a-hybrid-deployment#components-of-hybrid-architecture).
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

* Replace \<my-secret-name> with the name of the secret for your environment.
* Replace \<my-secret-key> with the secret's key for you environment.
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

* Replace \<VERSION-ALIGNED-WITH-CONTROL-PLANE> with the version of the gateway that aligns with your control plane. For more information about compatibility versions, see[ Components of Hybrid Architecture](https://documentation.gravitee.io/apim/getting-started/install-gravitee-api-management/installing-a-gravitee-gateway-with-a-hybrid-deployment#components-of-hybrid-architecture).
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

* Replace \<my-secret-name> with the name of the secret for your environment.
* Replace \<my-secret-key> with the secret's key for you environment.
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
      - $<GIO_LICENSE>:/opt/graviteeio-gateway/license/license.key
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
      - gravitee_ratelimit_redis_password=${REDIS_PASS:-28kjzEGquZYrztGyPMofR8eWuNbn4Yq}
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

* Replace \<VERSION-ALIGNED-WITH-CONTROL-PLANE> with the version of the gateway that aligns with your control plane. For more information about compatibility versions, see[ Components of Hybrid Architecture](https://documentation.gravitee.io/apim/getting-started/install-gravitee-api-management/installing-a-gravitee-gateway-with-a-hybrid-deployment#components-of-hybrid-architecture).
* Replace \<GIO\_LICENSE> with your license key.
* Replace \<YOUR-COCKPIT-ENV-HRID>  with your cockpit ID.


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

To configure logstash for your environment, copy the following example:

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
    access_key_id => "$<S3_ACCESS_KEY_ID>"
    secret_access_key => "$<S3_SECRET_ACCESS_KEY>"
    region => "$<S3_REGION>"
    bucket => "$<S3_BUCKET_NAME>"
    rotation_strategy => time
    time_file => 1
    codec => "json_lines"
  }
}
```
{% endcode %}

* Replace the following S3 values with your S3 values:&#x20;
  * \<S3\_ACCESS\_KEY\_ID>
  * \<S3\_SECRET\_ACCESS\_KEY>
  * &#x20;\<S3\_REGION>
  * \<S3\_BUCKET\_NAME>

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

### Configuring Fluentd

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
