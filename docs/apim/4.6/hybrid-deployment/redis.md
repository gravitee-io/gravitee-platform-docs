# Redis

## Kubernetes

1. Install Redis. To install Redis, go to [Bitnami Helm charts](https://artifacthub.io/packages/helm/bitnami/redis).
2. Configure Redis by copying the following file:

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

## Docker

1. Install Docker by copying the following file:

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

2. Configure Redis by copying the following file:

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

## .ZIP

1. Install Redis. To install Redis, go to[ redis.io](https://redis.io/docs/getting-started/installation/).
2. Configure Redis by copying the following file:

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
