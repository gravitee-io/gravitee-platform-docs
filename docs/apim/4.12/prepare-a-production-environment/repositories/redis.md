---
description: An overview about redis.
metaLinks:
  alternates:
    - redis.md
---

# Redis

## Overview

The Redis repository plugin enables you to connect to Redis databases to use the Rate Limit feature. The Redis plugin is part of the default distribution of APIM.

Gravitee API Management 4.12 introduces Redis Cluster support for rate limiting and distributed synchronization, alongside a rewritten Redis cache resource that uses asynchronous operations and shared connection pooling. These changes enable horizontal scaling of Redis infrastructure, reduce connection overhead, and improve gateway performance under high load.

## Supported databases

| Database | Version tested        |
| -------- | --------------------- |
| Redis    | 6.2.x / 7.0.x / 7.2.x / 7.4.x/ 8.0.x |

## Key concepts

### Redis Cluster mode

Redis Cluster distributes data across multiple master nodes using hash slots. Gravitee's rate limiting and distributed synchronization repositories now support cluster topology, ensuring atomic counter operations and consistent state across sharded deployments. Cluster mode is mutually exclusive with Sentinel mode.

| Capability | Cluster Mode | Sentinel Mode |
|:-----------|:-------------|:--------------|
| Topology | Sharded masters with optional replicas | Single master with failover sentinels |
| Read policy | Masters only (rate limiting enforces `NEVER` to ensure consistency) | Master or replicas |
| Configuration | `cluster.nodes` array with `host`/`port` | `sentinel.nodes` array with `masterId` |
| Default enabled | `true` | `true` |
| Default nodes | `[]` (empty array) | `[{host: "localhost", port: 26379}]` |

### Shared connection pooling

The gateway deduplicates Redis clients across resources and repositories that connect to the same endpoint. A single Vert.x Redis client is shared when `host`, `port`, `username`, `password`, **Use SSL**, and topology settings (Sentinel or Cluster) match. The deduplication key includes Sentinel `masterId` and sorted `nodes` only when `sentinel.enabled=true`, and Cluster Use Replicas and sorted `nodes` only when `cluster.enabled=true`. Pool settings (Max Pool Size, Max Pool Waiting, etc.) are gateway-wide and configured in `gravitee.yml` under `resources.cacheRedis.*` or `resources.aiVectorStoreRedis.*`.

### Binary cache storage

Cache policies (Cache and Data Cache) now store response payloads and cached values as binary frames (version byte `0x01`) rather than JSON envelopes. This preserves byte-for-byte fidelity for non-text content and reduces serialization overhead. For policy version >= 4.0.0, entries are stored as binary frames; for policy version <= 3.0.1, entries are JSON envelopes served read-only during rolling upgrades. When frame deserialization fails, the gateway logs `"Cannot decode cache frame for key <key>, evicting and refetching"` and evicts the corrupted entry.

## Prerequisites

* Gravitee API Management 4.12 or later
* Java 21 runtime (required for Redis cache resource 2.0.0+)
* Redis 6.0+ (standalone, Sentinel, or Cluster)
* For Redis Cluster: all rate-limited APIs must use the same cluster configuration to avoid CROSSSLOT errors

## Configure the Rate Limit repository plugin

The following tables show the configuration options for different Redis implementations. All specific configurations are located under the `ratelimit.redis` attribute.

{% tabs %}
{% tab title="Standalone" %}
Redis Standalone options:

<table><thead><tr><th width="168">Parameter</th><th width="140">Default</th><th>Description</th></tr></thead><tbody><tr><td>host</td><td>localhost</td><td></td></tr><tr><td>port</td><td>6379</td><td></td></tr><tr><td>password</td><td></td><td></td></tr></tbody></table>
{% endtab %}

{% tab title="Sentinel" %}
Redis Sentinel options:

<table><thead><tr><th width="168.66666666666666">Parameter</th><th width="90">Default</th><th>Description</th></tr></thead><tbody><tr><td>sentinel.nodes</td><td></td><td>List of sentinels with host and port</td></tr><tr><td>sentinel.master</td><td></td><td>Mandatory when using Sentinel</td></tr><tr><td>password</td><td></td><td></td></tr></tbody></table>
{% endtab %}

{% tab title="Cluster" %}
Redis Cluster options:

<table><thead><tr><th width="168.66666666666666">Parameter</th><th width="90">Default</th><th>Description</th></tr></thead><tbody><tr><td>cluster.nodes</td><td>[]</td><td>List of cluster nodes with host and port</td></tr><tr><td>password</td><td></td><td></td></tr></tbody></table>

{% hint style="info" %}
The gateway enforces **Use Replicas**: `NEVER` for rate limiting to ensure atomic counter operations are always executed on master nodes.
{% endhint %}
{% endtab %}

{% tab title="SSL" %}
Redis SSL options:

<table><thead><tr><th width="140.66666666666666">Parameter</th><th width="146">Default</th><th>Description</th></tr></thead><tbody><tr><td>ssl</td><td>false</td><td></td></tr><tr><td>trustAll</td><td>true</td><td>Default value is true for backward compatibility but keep in mind that this is not a good practice and you should set to false and configure a truststore</td></tr><tr><td>hostnameVerificationAlgorithm</td><td>NONE</td><td>Hostname verification algorithm: <code>NONE</code>, <code>HTTPS</code>, or <code>LDAPS</code></td></tr><tr><td>tlsProtocols</td><td>See <a href="https://vertx.io/docs/vertx-core/java/#_configuring_tls_protocol_versions">Vert.x doc</a></td><td>List of TLS protocols to allow comma separated</td></tr><tr><td>tlsCiphers</td><td>See <a href="https://vertx.io/docs/vertx-core/java/#_configuring_tls_protocol_versions">Vert.x doc</a></td><td>List of TLS ciphers to allow comma separated</td></tr><tr><td>alpn</td><td>false</td><td></td></tr><tr><td>openssl</td><td>false</td><td>Used to rely on OpenSSL Engine instead of default JDK SSL Engine</td></tr><tr><td>keystore</td><td></td><td>Configuration for Mutual TLS. The keystore is used to select the client certificate to send to the backend server when connecting. See <a href="https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-repository/gravitee-apim-repository-redis/README.adoc#keystore-table">Redis SSL keystore options (client certificate, Mutual TLS)</a></td></tr><tr><td>truststore</td><td></td><td>Configuration for the truststore. The truststore is used to validate the server's certificate. See <a href="https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-repository/gravitee-apim-repository-redis/README.adoc#truststore-table">Redis SSL truststore options</a></td></tr></tbody></table>

{% hint style="warning" %}
When Use Ssl is `true` but the `ssl` object is `null`, the gateway defaults to **Trust All**: `true` and Hostname Verifier: `false` and logs a warning.
{% endhint %}

**Hostname Verification Precedence**:

1. If **Hostname Verification Algorithm** is set and not `NONE`, it is used verbatim (supports `HTTPS`, `LDAPS`, etc.).
2. Otherwise, the legacy **Hostname Verifier** boolean is resolved: `true` → `HTTPS`, `false` → disabled.

**URL Scheme-Based TLS**:

* For `rediss://` scheme: Use Ssl is `true` and default `SslOptions` with Trust All: `false`.
* For `redis://` scheme: Use Ssl is `false`.
{% endtab %}

{% tab title="SSL keystore" %}
Redis SSL keystore options (client certificate, Mutual TLS):

<table><thead><tr><th width="168.66666666666666">Parameter</th><th width="90">Default</th><th>Description</th></tr></thead><tbody><tr><td>type</td><td></td><td>Supports <code>jks</code>, <code>pem</code>, <code>pkcs12</code>, or <code>NONE</code></td></tr><tr><td>path</td><td></td><td>A path is required if certificate's type is <code>jks</code> or <code>pkcs12</code></td></tr><tr><td>password</td><td></td><td></td></tr><tr><td>alias</td><td></td><td></td></tr><tr><td>keyPassword</td><td></td><td>Key password (PKCS12, JKS)</td></tr><tr><td>certificates</td><td></td><td>List of certificates with cert and key. Certificates are required if keystore's type is <code>pem</code></td></tr></tbody></table>

{% hint style="warning" %}
**Breaking Change**: The `type` field for "None" keystore changed from `""` (empty string) to `"NONE"` in `schema-form-ssl.json`.
{% endhint %}

**Multi-Certificate PEM Keystore**: When `certificates` is populated, it takes precedence over singular Cert Path/Key Path. The `cert` and `key` arrays must both be set or both `null`, and if both are set they must be the same size. Certificates and keys are paired by index (e.g., RSA certificate + RSA key, ECDSA certificate + ECDSA key).
{% endtab %}

{% tab title="SSL truststore" %}
Redis SSL truststore options:

<table><thead><tr><th width="168.66666666666666">Parameter</th><th width="90">Default</th><th>Description</th></tr></thead><tbody><tr><td>type</td><td></td><td>Supports <code>jks</code>, <code>pem</code>, <code>pkcs12</code>, or <code>NONE</code></td></tr><tr><td>path</td><td></td><td></td></tr><tr><td>password</td><td></td><td></td></tr><tr><td>alias</td><td></td><td></td></tr></tbody></table>

{% hint style="warning" %}
**Breaking Change**: The `type` field for "None" truststore changed from `""` (empty string) to `"NONE"` in `schema-form-ssl.json`.
{% endhint %}
{% endtab %}

{% tab title="TCP" %}
TCP connection settings:

<table><thead><tr><th width="168.66666666666666">Parameter</th><th width="90">Default</th><th>Description</th></tr></thead><tbody><tr><td>tcp.connectTimeout</td><td>5000</td><td>TCP connect timeout (ms)</td></tr><tr><td>tcp.idleTimeout</td><td>0</td><td>TCP idle timeout (ms); 0 disables idle timeout</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

Below is the minimum configuration needed to get started with a Redis database.

```yaml

ratelimit:
  type: redis               # repository type
  redis:                    # redis repository
    host:                   # redis host (default localhost)
    port:                   # redis port (default 6379)
    password:               # redis password (default null)
    timeout:                # redis timeout (default -1)

    # Following properties are REQUIRED ONLY when running Redis in sentinel mode
    sentinel:
      master:               # redis sentinel master host
      password:             # redis sentinel master password
      nodes: [              # redis sentinel node(s) list
        {
          host : localhost, # redis sentinel node host
          port : 26379      # redis sentinel node port
        },
        {
          host : localhost,
          port : 26380
        },
        {
          host : localhost,
          port : 26381
        }
      ]

    # Following properties are REQUIRED ONLY when running Redis in cluster mode
    cluster:
      nodes: [              # redis cluster node(s) list
        {
          host : redis-node-1.example.com, # redis cluster node host
          port : 6379                       # redis cluster node port
        },
        {
          host : redis-node-2.example.com,
          port : 6379
        },
        {
          host : redis-node-3.example.com,
          port : 6379
        }
      ]

    # Following SSL settings are REQUIRED ONLY for Redis client SSL
    ssl: true                # redis ssl mode (default false)
    trustAll: false
    hostnameVerificationAlgorithm: HTTPS
    tlsProtocols: TLSv1.2, TLSv1.3
    tlsCiphers: TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384
    alpn: false
    openssl: false
    # Keystore for redis mTLS (client certificate)
    keystore:
      type: jks
      path: ${gravitee.home}/security/redis-keystore.jks
      password: secret
      keyPassword:
      alias:
      certificates: # Certificates are required if keystore's type is pem
      #      - cert: ${gravitee.home}/security/redis-mycompany.org.pem
      #        key: ${gravitee.home}/security/redis-mycompany.org.key
      #      - cert: ${gravitee.home}/security/redis-myothercompany.com.pem
      #        key: ${gravitee.home}/security/redis-myothercompany.com.key
    truststore:
      type: pem
      path: ${gravitee.home}/security/redis-truststore.jks
      password: secret
      alias:

    # TCP connection settings
    tcp:
      connectTimeout: 5000  # TCP connect timeout (ms)
      idleTimeout: 0        # TCP idle timeout (ms); 0 disables idle timeout
```

## Gateway configuration

### Redis cache resource pool settings

Configure gateway-wide connection pool limits for the Redis cache resource in `gravitee.yml`. These settings apply to all cache resources sharing the same Redis endpoint. Pool settings were removed from the per-resource configuration schema (`schema-form.json`) and moved to `gravitee.yml` in version 2.0.0+.

| Property | Description | Default |
|:---------|:------------|:--------|
| `resources.cacheRedis.maxPoolSize` | Maximum number of connections per Redis endpoint (gateway-wide) | `6` |
| `resources.cacheRedis.maxPoolWaiting` | Maximum number of requests waiting for a connection from the pool | `1024` |
| `resources.cacheRedis.poolCleanerInterval` | Interval in milliseconds between pool cleaner runs | `30000` |
| `resources.cacheRedis.poolRecycleTimeout` | Timeout in milliseconds for recycling idle connections | `180000` |
| `resources.cacheRedis.maxWaitingHandlers` | Maximum number of waiting handlers for the Redis client | `1024` |
| `resources.cacheRedis.connectTimeout` | Maximum time in milliseconds to establish a connection | `2000` |

**Example**:

```yaml
resources:
  cacheRedis:
    maxPoolSize: 10
    maxPoolWaiting: 2048
    poolCleanerInterval: 30000
    poolRecycleTimeout: 180000
    maxWaitingHandlers: 1024
    connectTimeout: 2000
```

### AI vector store Redis resource pool settings

Configure gateway-wide connection pool limits for the AI vector store Redis resource (APIM 4.12+). The migration to `VertxRedisClientFactory` in version 2.0.0+ is a breaking change.

| Property | Description | Default |
|:---------|:------------|:--------|
| `resources.aiVectorStoreRedis.maxPoolSize` | Maximum simultaneous connections per Redis endpoint (gateway-wide) | `6` |
| `resources.aiVectorStoreRedis.maxPoolWaiting` | Maximum queued requests waiting for a connection | `1024` |
| `resources.aiVectorStoreRedis.poolCleanerInterval` | Idle-connection cleaner interval (ms) | `30000` |
| `resources.aiVectorStoreRedis.poolRecycleTimeout` | Idle connection recycle timeout (ms) | `180000` |
| `resources.aiVectorStoreRedis.maxWaitingHandlers` | Maximum queued commands on a connection | `1024` |
| `resources.aiVectorStoreRedis.connectTimeout` | TCP connect timeout (ms) | `2000` |

### Node cache plugin Redis configuration

Configure the node-level Redis cache (used for distributed caching across gateway instances) in `gravitee.yml`.

| Property | Description | Default |
|:---------|:------------|:--------|
| `cache.redis.host` | Redis host | `localhost` |
| `cache.redis.port` | Redis port | `6379` |
| `cache.redis.password` | Redis password | — |
| `cache.redis.ssl` | Enable SSL | `false` |
| `cache.redis.trustAll` | Trust all certificates | `false` |
| `cache.redis.openssl` | Use OpenSSL | `false` |
| `cache.redis.hostnameVerificationAlgorithm` | Hostname verification algorithm; `NONE` disables verification | `NONE` |
| `cache.redis.sentinel.nodes[N].host` | Sentinel node host (indexed) | — |
| `cache.redis.sentinel.nodes[N].port` | Sentinel node port (indexed) | — |
| `cache.redis.sentinel.master` | Sentinel master id | `mymaster` |
| `cache.redis.sentinel.password` | Sentinel password | — |
| `cache.redis.keystore.type` | Keystore type: `JKS`, `PKCS12`, `PEM` | — |
| `cache.redis.keystore.path` | Keystore path | — |
| `cache.redis.keystore.password` | Keystore password | — |
| `cache.redis.keystore.alias` | Keystore alias (JKS only) | — |
| `cache.redis.keystore.keyPath` | PEM key path | — |
| `cache.redis.truststore.type` | Truststore type | — |
| `cache.redis.truststore.path` | Truststore path | — |
| `cache.redis.truststore.password` | Truststore password | — |
| `cache.redis.maxPoolSize` | Max pool size | — |
| `cache.redis.maxPoolWaiting` | Max pool waiting | — |
| `cache.redis.poolCleanerInterval` | Pool cleaner interval (ms) | — |
| `cache.redis.poolRecycleTimeout` | Pool recycle timeout (ms) | — |
| `cache.redis.maxWaitingHandlers` | Max waiting handlers | — |

### Helm chart configuration

Configure Redis resource pool settings and cluster nodes via Helm values.

| Property | Description | Default |
|:---------|:------------|:--------|
| `gateway.ratelimit.redis.cluster.nodes` | Redis Cluster nodes for rate limiting (array of `{host, port}`) | `unset` |
| `gateway.cacheRedis.maxPoolSize` | Redis cache resource max connections per endpoint (gateway-wide) | `6` |
| `gateway.cacheRedis.maxPoolWaiting` | Redis cache resource max queued requests waiting for a connection | `1024` |
| `gateway.cacheRedis.poolCleanerInterval` | Redis cache resource idle-connection cleaner interval (ms) | `30000` |
| `gateway.cacheRedis.poolRecycleTimeout` | Redis cache resource idle connection recycle timeout (ms) | `180000` |
| `gateway.cacheRedis.maxWaitingHandlers` | Redis cache resource max queued commands on a connection | `1024` |
| `gateway.cacheRedis.connectTimeout` | Redis cache resource TCP connect timeout (ms) | `2000` |
| `gateway.aiVectorStoreRedis.maxPoolSize` | AI vector store Redis resource max connections per endpoint (APIM 4.12+) | `6` |
| `gateway.aiVectorStoreRedis.maxPoolWaiting` | AI vector store Redis resource max queued requests waiting for a connection | `1024` |
| `gateway.aiVectorStoreRedis.poolCleanerInterval` | AI vector store Redis resource idle-connection cleaner interval (ms) | `30000` |
| `gateway.aiVectorStoreRedis.poolRecycleTimeout` | AI vector store Redis resource idle connection recycle timeout (ms) | `180000` |
| `gateway.aiVectorStoreRedis.maxWaitingHandlers` | AI vector store Redis resource max queued commands on a connection | `1024` |
| `gateway.aiVectorStoreRedis.connectTimeout` | AI vector store Redis resource TCP connect timeout (ms) | `2000` |

