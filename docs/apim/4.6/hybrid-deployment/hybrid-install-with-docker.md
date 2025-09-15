# Hybrid Install with Docker

{% include "../.gitbook/includes/installation-guide-note.md" %}

## Architecture

The hybrid installation consists of installing the data plane on your infrastructure and connecting it as shown in the following diagram:&#x20;

<figure><img src="../.gitbook/assets/image (135).png" alt="Diagram showing the hybrid architecture"><figcaption><p>Hybrid architecture connections</p></figcaption></figure>

## Configuration

The sample `docker-compose.yml` below sets up a hybrid configuration.

{% hint style="info" %}
All optional services have been commented out. Please uncomment them as needed to activate the Alert Engine or activate Redis for rate limiting at the Gateway level.
{% endhint %}

```yaml
version: '3.8'

volumes:
  data-redis:

services:

  gateway:
    image: graviteeio/apim-gateway:4.4.4
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
      - ./.logs/apim-gateway:/opt/graviteeio-gateway/logs
      - ./.license:/opt/graviteeio-gateway/license
      - ./.plugins:/opt/graviteeio-gateway/plugins-ext
    environment:
      # gravitee_tags=UK
      
      # --- GRAVITEE CLOUD ORGS & ENVS ---
      - gravitee_organizations=xxx
      - gravitee_environments=xxx
     
      # --- BRIDGE GATEWAYS ---
      - gravitee_management_type=http
      - gravitee_management_http_url=xxx
      - gravitee_management_http_authentication_type=basic
      - gravitee_management_http_authentication_basic_username=xxx
      - gravitee_management_http_authentication_basic_password=xxx
      - gravitee_plugins_path_0=$${gravitee.home}/plugins
      - gravitee_plugins_path_1=$${gravitee.home}/plugins-ext
     
      # --- LOGSTASH ---
      - gravitee_reporters_elasticsearch_enabled=false
      - gravitee_reporters_tcp_enabled=true
      - gravitee_reporters_tcp_host=logstash
      - gravitee_reporters_tcp_port=8379
      - gravitee_reporters_tcp_output=elasticsearch
      - gravitee_api_properties_encryption_secret=xxx
     
       # --- RATE LIMIT REPO (OPTIONAL)---
      # - gravitee_ratelimit_type=redis
      # - gravitee_ratelimit_redis_host=redis
      # - gravitee_ratelimit_redis_port=6379
      # - gravitee_ratelimit_redis_password=${REDIS_PASS:-xxx}
      # - gravitee_ratelimit_redis_ssl=false
      # - gravitee_redis_download=true

      # --- ALERT ENGINE (OPTIONAL) ---
      # - gravitee_alerts_alert-engine_enabled=true
      # - gravitee_alerts_alert-engine_ws_discovery=true
      # - gravitee_alerts_alert-engine_ws_endpoints[0]=http://host.docker.internal:8072/
      # - gravitee_alerts_alert-engine_ws_security_username=xxx
      # - gravitee_alerts_alert-engine_ws_security_password=xxx

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
         - ./config/logstash/:/usr/share/logstash/pipeline/:ro
     environment:
         LS_JAVA_OPTS: "-Xmx256m -Xms256m"

#   redis: 
#     # https://hub.docker.com/_/redis?tab=tags
#     image: redis:${REDIS_VERSION:-7.2.1-alpine}
#     container_name: gio_apim_hybrid_redis
#     hostname: redis
#     restart: always
#     ports:
#       - '6379:6379'
#     command: redis-server --requirepass ${REDIS_PASS:-xxx} --maxmemory 256mb --maxmemory-policy allkeys-lru
#     healthcheck:
#       test: ["CMD", "redis-cli", "ping"]
#       interval: 1s
#       timeout: 3s
#       retries: 30
#     volumes:
#      - data-redis:/data
```

This `docker-compose.yml` contains multiple services:&#x20;

* Gateway(s): Each Gateway declares the component used to route traffic and applies policies (one service per Gateway).
* The TCP reporter, Logstash: Centralizes logs from the Gateway(s), processes them, and forwards them to an S3 bucket in the control plane. These logs are then stored for persistence and can be used by Elasticsearch to enable log analytics and monitoring.
* Optional: To set up rate limiting at the Gateway level, you need to declare a Redis service.

## Before you begin

{% hint style="warning" %}
The following sections of this article assume you are using the `docker-compose.yml` above, with some modifications.
{% endhint %}

* All `xxx` values in the sample `docker-compose.yml` above must be replaced by the credentials appropriate to your environment. These can be provided by your Technical Account Manager.
* Ensure the version of your Gravitee Cloud environment corresponds to the Gateway version used by your `docker-compose.yml`, e.g., `image: graviteeio/apim-gateway:4.4.4` in the sample `docker-compose.yml`.
* Ensure the Logstash and Redis versions used by your `docker-compose.yml` are supported by Gravitee:
  * For supported version of Redis, refer to [Supported databases](../configure-apim/repositories/redis.md#supported-databases).
  * For supported version of Logstash, refer to [Compatibility with Elasticsearch](logstash.md#compatibility-with-elasticsearch).
  * For the installed version of Elasticsearch on the control plane, which Logstash will interact with via an S3 bucket, please reach out to your Technical Account Manager.

## **Gateway service configuration**&#x20;

As shown in the [architecture diagram](hybrid-install-with-docker.md#architecture), the Gateway(s) connect to the Bridge Gateway to allow the decoupling of the API Gateway functionality from the underlying data storage layer. Instead of directly interacting with a repository, the Gateway uses the Bridge Gateway to route requests and data through to the control plane.

First, you need to upload the `license.key` file sent by your Technical Account Manager, then refer to it in the `volumes` of the Gateway services section of your `docker-compose.yml`:&#x20;

```yaml
    volumes:
      - ./.license:/opt/graviteeio-gateway/license
```

You must update the path on the left of this command with the path where you will host the `license.key` file on your system.

To link your Gateway to a specific environment defined in Gravitee Cloud, update the following values:&#x20;

```yaml
  # --- GRAVITEE CLOUD ORGS & ENVS ---
  - gravitee_organizations=mycompany
  - gravitee_environments=myenv
```

For example:&#x20;

```yaml
  - gravitee_organizations=Company
  - gravitee_environments=DEV
```

{% hint style="info" %}
You can connect to Gravitee Cloud with your credentials to find these values. The name of the organization and the environment will appear in the Topology menu. Alternatively, they can be provided by your Technical Account Manager.
{% endhint %}

To initiate this connection, the following credentials must be added to each of the Gateway services in your `docket-compose.yml`:&#x20;

```yaml
 # --- BRIDGE GATEWAYS ---
      - gravitee_management_type=http
      - gravitee_management_http_url=xxx
      - gravitee_management_http_authentication_type=basic
      - gravitee_management_http_authentication_basic_username=xxx
      - gravitee_management_http_authentication_basic_password=xxx
```

{% hint style="info" %}
Please reach out to your Technical Account Manager for the Bridge Gateway credentials if you don't have them already.
{% endhint %}

## **Logstash service configuration**

To connect Logstash to the S3 bucket as shown in the [architecture diagram](hybrid-install-with-docker.md#architecture), you need to link the Docker Compose service to a configuration file called `logstash.conf` so it knows which S3 bucket to connect to. This link is done via the `volumes` command in the `docker-compose.yml`:&#x20;

```yaml
  volumes:
 - ./config/logstash/:/usr/share/logstash/pipeline/:ro
```

You must update the path on the left of this command with the path where you will host the `logstash.conf` file on your system.

You also need to set up an encryption key to make sure all communication between the Gateway and Logstash are encrypted. In your `docker-compose.yml`, go to the Logstash variables in the environment part of the Gateway service and provide the encryption secret:

```yaml
  - gravitee_api_properties_encryption_secret=xxx
```

{% hint style="info" %}
Please reach out to your Technical Account Manager for this encryption secret if you don't have it already.
{% endhint %}

Below is an example of `logstash.conf`. You need to provide this file with the S3 credentials.

```bash
input {
  tcp {
      port => 8379
      codec => "json"
      add_field => { "source" => "tcp" }
  }
}

filter {
  if ![type] {
      mutate { add_field => { "type" => "default" } }
  }
  if [type] != "request" {
      mutate { remove_field => ["path", "host"] }
  }
}

output {
  s3 {
    access_key_id => "xxx"
    secret_access_key => "xxx"
    region => "xxx"
    bucket => "xxx"
    size_file => 10485760
    codec => "json_lines"
    time_file => 5
  }
}
```

{% hint style="info" %}
Please reach out to your Technical Account Manager for the S3 credentials  if you don't have them already.
{% endhint %}

## **Redis service configuration (optional)**

To activate Redis, you need to generate a password and include it in your `docker-compose.yml`, in both the environment part of the Gateway configuration and the Redis service section:&#x20;

The following command generates a random and secured password using bash/sh:

```bash
openssl rand -base64 32
```

This password then needs to be updated here:

```yaml
    command: redis-server --requirepass ${REDIS_PASS:-xxx} --maxmemory 256mb --maxmemory-policy allkeys-lru
```

and here:&#x20;

```yaml
      - gravitee_ratelimit_redis_password=${REDIS_PASS:-xxx}
```

## **Alert Engine configuration (optional)**&#x20;

To configure the Alert Engine, you must provide the Alert Engine credentials in the environment part of the Gateway service in the `docker-compose.yml`:

```yaml
      - gravitee_alerts_alert-engine_ws_security_username=xxx
      - gravitee_alerts_alert-engine_ws_security_password=xxx
```

{% hint style="info" %}
Please reach out to your Technical Account Manager for the Alert Engine credentials if you don't have them already.
{% endhint %}

## Initiating the connection

Once the services are started, connect to the APIM Console of the environment you linked the hybrid Gateway(s) with. You should see them appear as having started in the Gateways menu.

You can test if your Gateway is accessible in a specific network by opening the Gateway URL in your browser. If the test is successful, you should see the following message: &#x20;

```
No context-path matches the request URI.
```
