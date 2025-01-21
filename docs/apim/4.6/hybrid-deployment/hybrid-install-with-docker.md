# Hybrid Install with Docker

1. Install Gravitee API Management (APIM). For more information about installing Gravitee APIM, see the [Docker](../install-and-upgrade/docker/) install guide.
2. Download the redis respository, and then mount the Redis Repository. This repository is used for the rate limits' synchronized counters. To download this repository, go to [Gravitee.io Downloads](https://download.gravitee.io/#graviteeio-apim/plugins/repositories/gravitee-apim-repository-redis).
3. Download, and then mount TCP Reporter. This repository is used to push events to Logstash. To download this repository, go to [Gravitee.io Downloads.](https://download.gravitee.io/#graviteeio-ee/apim/plugins/reporters/gravitee-reporter-tcp/)

### **Configuring the connection between the SaaS Control-Plane and the Bridge Gateway**

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

### **An example of a Self-Hosted Gateway configuration**

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
      - gravitee_api_properties_encryption_secret=your-own-api-32-caracters-secret

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
