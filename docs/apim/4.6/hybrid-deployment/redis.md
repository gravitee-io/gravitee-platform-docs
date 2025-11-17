---
description: Redis can be used by Gravitee for both caching and rate-limiting of your APIs.
---

# Redis

## Kubernetes

1.  To install Redis, use packages available from [Bitnami Helm charts](https://artifacthub.io/packages/helm/bitnami/redis).  The following example uses a standalone configuration.\


    ```bash
    helm repo add bitnami https://charts.bitnami.com/bitnami
    helm repo update
    helm install redis-apim bitnami/redis \
      --version 19.6.4 \
      --set image.repository=bitnamilegacy/redis \
      --set auth.password=p@ssw0rd
    ```
2. Configure your Gravitee Gateway to use Redis by using the following example `values.yaml` configuration:

{% code title="values.yaml" lineNumbers="true" %}
```yaml
gateway:
  ...
  ratelimit:
    type: redis
  redis:
    host: ${redis_hostname}
    port: ${redis_port_number}
    password: ${redis_password}
    #password: kubernetes://<namespace>/secrets/<my-secret-name>/<my-secret-key>
    download: true
```
{% endcode %}

## Docker

1. Install Redis by using the following `docker-compose.yaml` configuration example:

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
    command: redis-server --requirepass ${redis_password}
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 1s
      timeout: 3s
      retries: 30
    volumes: 
      - data-redis:/data
```
{% endcode %}

2. Now enable Gravitee to use the Redis service by using the following `docker-compose.yaml` example configuration:

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
      - gravitee_ratelimit_redis_host=${redis_hostname}
      - gravitee_ratelimit_redis_port=${redis_port_number}
      - gravitee_ratelimit_redis_password=${redis_password}
```
{% endcode %}

## .ZIP

1. Install Redis. To install Redis, go to [redis.io](https://redis.io/docs/latest/get-started/).
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
