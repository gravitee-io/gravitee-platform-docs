# Migrate from Redis Cache Resource 4.x to 5.x

## Overview

Gravitee Gateway now shares Redis client connections across resources and APIs that target the same Redis endpoint, reducing connection overhead and improving resource utilization. This release also introduces Redis Cluster support for rate limiting and cache resources, enabling horizontal scaling of Redis deployments. Connection pool sizing and timeout configuration have moved from per-API resource definitions to gateway-wide settings in `gravitee.yml`.

## Key Concepts

### Shared Connection Pooling

When multiple APIs or resources connect to the same Redis endpoint (matching host, port, credentials, and topology), the gateway creates a single shared Vert.x Redis client with a reference-counted connection pool. The first resource to acquire a connection establishes the pool; subsequent resources reuse it. When the last resource releases its reference, the pool is closed. Pool sizing parameters are configured gateway-wide in `gravitee.yml` under `resources.cacheRedis.*` or `resources.aiVectorStoreRedis.*`, not per-API.

### Redis Cluster Topology

Redis Cluster distributes data across multiple master nodes using hash slots. The gateway now supports cluster mode for rate limiting and cache resources. When cluster mode is enabled, the client automatically routes commands to the correct master based on key hash. Replica read policies control whether read operations can be served by replica nodes (`NEVER`, `SHARE`, or `ALWAYS`). For rate limiting, replica reads are disabled (`NEVER`) to ensure master-consistent counters and avoid stale-read race conditions.

### Deployment Mode Selection

Redis resources support three mutually exclusive deployment modes: **Standalone** (single host/port), **Sentinel** (high-availability master discovery), and **Cluster** (horizontal sharding). Sentinel and Cluster modes cannot be enabled simultaneously; the configuration mapper throws an error if both are active. Standalone mode is the default when neither Sentinel nor Cluster options are configured.

## Creating Redis Cache Resources

Configure a cache-redis resource in the API definition. Pool sizing and timeout parameters are now sourced from gateway-wide settings in `gravitee.yml` under `resources.cacheRedis.*`, not from the per-API resource configuration. Specify the Redis endpoint (host, port, credentials), deployment mode (Standalone, Sentinel, or Cluster), and SSL/TLS options. When multiple APIs or resources target the same Redis endpoint, the gateway automatically shares a single connection pool.

**Standalone mode example**:

```json
{
  "type": "cache-redis",
  "configuration": {
    "host": "redis.example.com",
    "port": 6379,
    "password": "secret",
    "useSsl": true,
    "ssl": {
      "trustAll": false,
      "trustStore": {
        "type": "pem",
        "path": "/etc/gravitee/truststore.pem"
      }
    }
  }
}
```

**Sentinel mode example**:

```json
{
  "type": "cache-redis",
  "configuration": {
    "sentinel": {
      "enabled": true,
      "masterId": "mymaster",
      "nodes": [
        {"host": "sentinel1.example.com", "port": 26379},
        {"host": "sentinel2.example.com", "port": 26379},
        {"host": "sentinel3.example.com", "port": 26379}
      ]
    },
    "password": "secret"
  }
}
```

**Cluster mode example**:

```json
{
  "type": "cache-redis",
  "configuration": {
    "cluster": {
      "enabled": true,
      "nodes": [
        {"host": "redis-node1.example.com", "port": 6379},
        {"host": "redis-node2.example.com", "port": 6379},
        {"host": "redis-node3.example.com", "port": 6379}
      ],
      "useReplicas": "NEVER"
    },
    "password": "secret"
  }
}
```

## Configuring Rate Limit Redis Cluster

Enable Redis Cluster mode for rate limiting by adding cluster node configuration to `gravitee.yml`. Cluster mode is mutually exclusive with Sentinel mode; configure cluster nodes **or** sentinel nodes, not both. Replica reads are disabled (`useReplicas=NEVER`) to ensure master-consistent rate-limit counters and avoid stale-read race conditions. When a rate-limit operation is routed to a Redis master that does not have the Lua script cached, the gateway automatically falls back from `EVALSHA` to `EVAL` with the script source, then retries the operation. This NOSCRIPT recovery is transparent to API consumers.

**gravitee.yml example**:

```yaml
repositories:
  ratelimit:
    redis:
      cluster:
        nodes:
          - host: redis-node1
            port: 6379
          - host: redis-node2
            port: 6379
          - host: redis-node3
            port: 6379
      username: myuser
      password: secret
      ssl: true
      hostnameVerificationAlgorithm: HTTPS
      truststore:
        type: pem
        path: /etc/gravitee/truststore.pem
```

**Helm chart example**:

```yaml
gateway:
  ratelimit:
    redis:
      cluster:
        nodes:
          - host: redis-node1
            port: 6379
          - host: redis-node2
            port: 6379
          - host: redis-node3
            port: 6379
```

{% hint style="info" %}
**Cluster-safe Lua script**: The rate-limit Lua script now declares `numkeys=1` (only the rate-limit key) and passes the weight parameter as `ARGV[1]` instead of `KEYS[2]`. This ensures all keys in the command hash to the same slot, avoiding `CROSSSLOT` errors on Redis Cluster.
{% endhint %}

**EVALSHA command structure**:

```bash
EVALSHA <sha> 1 <key> <weight> <counter> <limit> <reset> <subscription>
```

* `numkeys` is `1` (only the rate-limit key)
* `weight` is passed as `ARGV[1]`
* Remaining arguments are `ARGV[2]` (counter), `ARGV[3]` (limit), `ARGV[4]` (reset), `ARGV[5]` (subscription)
