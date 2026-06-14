# Redis Cache and Cluster Support — Gateway Configuration Reference

## Overview

Gravitee API Management 4.12 introduces Redis Cluster support for rate limiting and distributed synchronization, alongside enhanced SSL/TLS configuration options for all Redis-backed resources. The Redis cache resource has been rewritten to use asynchronous operations and binary-safe storage, improving performance and reliability for high-throughput API gateways. Pool and timeout settings for Redis cache resources are now configured globally in `gravitee.yml` to ensure consistency across shared connections.

## Key Concepts

### Redis Cluster Topology

Redis Cluster distributes data across multiple master nodes using hash slots. Gravitee's rate limiting and distributed synchronization features now support Redis Cluster deployments, automatically routing commands to the correct node and handling CROSSSLOT constraints. Cluster mode is mutually exclusive with Sentinel mode — you must configure one or the other, not both. For rate limiting, the replica read policy is pinned to `NEVER` to ensure write consistency across all cluster operations. When a Redis Cluster EVALSHA command returns a `NOSCRIPT` error, the gateway automatically falls back to `EVAL` with the full script source and caches the script on the target node for subsequent requests.

### Shared Connection Pooling

Multiple APIs using the same Redis endpoint (host, port, credentials, and topology) share a single connection pool. Pool size, timeout, and recycling parameters are configured once in `gravitee.yml` under `resources.cacheRedis.*` or `resources.aiVectorStoreRedis.*` and apply to all resources sharing that endpoint. The first resource to acquire a connection establishes the pool configuration; subsequent resources reuse the existing pool. Shared clients are deduplicated by a key that includes host, port, **Use Ssl**, username, password (never logged), Sentinel master ID and sorted nodes and enabled flag, and Cluster `useReplicas` and sorted nodes and enabled flag.

### Binary Cache Storage

Cache entries are now stored as binary frames (version `0x01`) instead of JSON envelopes. This format preserves exact byte sequences for response bodies, headers, and metadata, eliminating serialization overhead and supporting non-UTF-8 content. Legacy JSON-format entries (from policy versions ≤ 4.0.0-alpha.2) remain readable during rolling upgrades but are not rewritten to avoid thundering-herd refetches; they migrate to binary format naturally when their TTL expires. If a cache entry is unrecognized (neither binary frame nor valid JSON), it is evicted and refetched.

### SSL/TLS Hardening

Redis resources support advanced SSL options including hostname verification algorithms (`HTTPS`, `LDAPS`), custom TLS protocol and cipher suite selection, OpenSSL engine acceleration, and ALPN. PEM keystores now accept multiple certificate/key pairs for multi-domain scenarios. When `useSsl=true` but no `ssl` configuration is provided, the resource falls back to `trustAll=true` and logs a warning recommending explicit truststore and hostname verification configuration. Credentials are applied to Redis client options only when password is non-empty; otherwise both username and password are null. TLS is enabled for `rediss://` scheme with `useSsl(true)` and default system-CA validation (`trustAll=false`). Hostname verification is disabled by default when `hostnameVerificationAlgorithm` is `NONE`, and enabled when `hostnameVerificationAlgorithm` is `HTTPS` or `LDAPS`.

## Prerequisites

* Gravitee API Management 4.12 or later
* Java 21 runtime
* Redis 6.0 or later (standalone, Sentinel, or Cluster)
* For Redis Cluster: all cluster nodes must share the same authentication credentials
* For SSL/TLS: valid certificates and keys in PEM, PKCS12, or JKS format
* For Sentinel mode: at least one sentinel node must be declared and `sentinel.master` parameter must be configured

## Gateway Configuration

### Redis Cache Resource Pool Settings

Configure these properties in `gravitee.yml` under `resources.cacheRedis.*`. They apply gateway-wide to all Redis cache resources sharing the same endpoint.

| Property | Description | Default |
|:---------|:------------|:--------|
| `resources.cacheRedis.maxPoolSize` | Maximum number of connections in the Redis pool | `6` |
| `resources.cacheRedis.maxPoolWaiting` | Maximum number of requests waiting for a connection from the pool | `1024` |
| `resources.cacheRedis.poolCleanerInterval` | Interval in milliseconds between pool cleaner runs | `30000` |
| `resources.cacheRedis.poolRecycleTimeout` | Timeout in milliseconds for recycling idle connections | `180000` |
| `resources.cacheRedis.maxWaitingHandlers` | Maximum number of waiting handlers for the Redis client | `1024` |
| `resources.cacheRedis.connectTimeout` | Maximum time in milliseconds to establish a connection | `2000` |

**Example:**

```yaml
resources:
  cacheRedis:
    maxPoolSize: 60
    maxPoolWaiting: 1024
    poolCleanerInterval: 30000
    poolRecycleTimeout: 180000
    maxWaitingHandlers: 1024
    connectTimeout: 2000
```

### AI Vector Store Redis Resource Pool Settings

Configure these properties in `gravitee.yml` under `resources.aiVectorStoreRedis.*`. They apply gateway-wide to all AI vector store Redis resources sharing the same endpoint (APIM 4.12+).

| Property | Description | Default |
|:---------|:------------|:--------|
| `resources.aiVectorStoreRedis.maxPoolSize` | Maximum number of connections in the Redis pool | `6` |
| `resources.aiVectorStoreRedis.maxPoolWaiting` | Maximum number of requests waiting for a connection from the pool | `1024` |
| `resources.aiVectorStoreRedis.poolCleanerInterval` | Interval in milliseconds between pool cleaner runs | `30000` |
| `resources.aiVectorStoreRedis.poolRecycleTimeout` | Timeout in milliseconds for recycling idle connections | `180000` |
| `resources.aiVectorStoreRedis.maxWaitingHandlers` | Maximum number of waiting handlers for the Redis client | `1024` |
| `resources.aiVectorStoreRedis.connectTimeout` | Maximum time in milliseconds to establish a connection | `2000` |

### Redis Cluster Configuration

Configure Redis Cluster nodes in `gravitee.yml` for rate limiting and distributed synchronization. Cluster mode is mutually exclusive with Sentinel mode.

| Property | Description | Example |
|:---------|:------------|:--------|
| `ratelimit.redis.cluster.nodes[N].host` | Redis Cluster node host | `redis-node-1.example.com` |
| `ratelimit.redis.cluster.nodes[N].port` | Redis Cluster node port | `6379` |

**Example:**

```yaml
ratelimit:
  redis:
    cluster:
      nodes:
        - host: redis-node-1.example.com
          port: 6379
        - host: redis-node-2.example.com
          port: 6379
        - host: redis-node-3.example.com
          port: 6379
```

### Redis Repository Configuration

Configure Redis repository settings in `gravitee.yml` using prefix-based properties for multiple Redis instances. The prefix identifies the repository type (e.g., `ratelimit`, `management`).

| Property | Description | Default |
|:---------|:------------|:--------|
| `<prefix>.redis.host` | Redis standalone host | `localhost` |
| `<prefix>.redis.port` | Redis standalone port | `6379` |
| `<prefix>.redis.username` | Redis username (optional) | `null` |
| `<prefix>.redis.password` | Redis password | `null` |
| `<prefix>.redis.ssl` | Enable TLS | `false` |
| `<prefix>.redis.trustAll` | Trust all certificates (when SSL enabled) | `true` |
| `<prefix>.redis.hostnameVerificationAlgorithm` | Hostname verification algorithm (`NONE`, `HTTPS`, `LDAPS`) | `NONE` |
| `<prefix>.redis.tlsProtocols` | Enabled TLS protocols (comma-delimited) | `""` |
| `<prefix>.redis.tlsCiphers` | Enabled TLS cipher suites (comma-delimited) | `""` |
| `<prefix>.redis.alpn` | Enable ALPN | `false` |
| `<prefix>.redis.openssl` | Use OpenSSL engine | `false` |
| `<prefix>.redis.tcp.connectTimeout` | TCP connect timeout (ms) | `5000` |
| `<prefix>.redis.tcp.idleTimeout` | TCP idle timeout (ms) | `0` |
| `<prefix>.redis.sentinel.master` | Sentinel master name (required when sentinel enabled) | N/A |
| `<prefix>.redis.sentinel.nodes[N].host` | Sentinel node host | N/A |
| `<prefix>.redis.sentinel.nodes[N].port` | Sentinel node port | N/A |
| `<prefix>.redis.sentinel.password` | Sentinel password | `null` |
| `<prefix>.redis.cluster.nodes[N].host` | Redis Cluster node host | N/A |
| `<prefix>.redis.cluster.nodes[N].port` | Redis Cluster node port | N/A |
| `<prefix>.redis.truststore.type` | Truststore type (`PEM`, `PKCS12`, `JKS`) | N/A |
| `<prefix>.redis.truststore.path` | Truststore file path | N/A |
| `<prefix>.redis.truststore.password` | Truststore password (PKCS12/JKS) | N/A |
| `<prefix>.redis.truststore.alias` | Truststore alias (PKCS12/JKS) | N/A |
| `<prefix>.redis.keystore.type` | Keystore type (`PEM`, `PKCS12`, `JKS`) | N/A |
| `<prefix>.redis.keystore.path` | Keystore file path (PKCS12/JKS) | N/A |
| `<prefix>.redis.keystore.certificates[N].cert` | PEM certificate path (PEM keystore) | N/A |
| `<prefix>.redis.keystore.certificates[N].key` | PEM key path (PEM keystore) | N/A |
| `<prefix>.redis.keystore.password` | Keystore password (PKCS12/JKS) | N/A |
| `<prefix>.redis.keystore.alias` | Keystore alias (PKCS12/JKS) | N/A |
| `<prefix>.redis.keystore.keyPassword` | Key password (PKCS12/JKS) | N/A |

When Sentinel configuration is enabled, the `sentinel.master` parameter is required. If missing or empty, the repository throws an `IllegalStateException` at startup.

### SSL/TLS Options

Configure SSL/TLS settings for Redis connections. These options apply to cache resources, rate limiting, and distributed synchronization.

| Property | Description | Default |
|:---------|:------------|:--------|
| `ssl.trustAll` | Trust all certificates (disables validation) | `false` |
| `ssl.hostnameVerifier` | Enable hostname verification | `true` |
| `ssl.hostnameVerificationAlgorithm` | Hostname verification algorithm (`HTTPS`, `LDAPS`, or `NONE`); overrides **Hostname Verifier** when set | `null` |
| `ssl.openSsl` | Use OpenSSL engine for TLS | `false` |
| `ssl.alpn` | Enable Application-Layer Protocol Negotiation | `false` |
| `ssl.tlsProtocols` | Enabled TLS protocols (e.g., `TLSv1.2`, `TLSv1.3`) | System default |
| `ssl.tlsCiphers` | Enabled TLS cipher suites | System default |

**Hostname Verification Algorithm Resolution:**

1. If `hostnameVerificationAlgorithm` is set and not `NONE`, use the specified algorithm (`HTTPS` or `LDAPS`).
2. Otherwise, if **Hostname Verifier** is `true`, use `HTTPS`.
3. Otherwise, hostname verification is disabled.

### PEM Keystore (Multi-Certificate Support)

PEM keystores now support multiple certificate/key pairs for multi-domain scenarios. Pair each certificate path with its corresponding key path at the same index. Both **Cert Paths** and **Key Paths** must be the same size. The constructor validates that **Cert Paths** and **Key Paths** are either both null or both the same size, throwing `IllegalArgumentException` if mismatched.

| Property | Description | Example |
|:---------|:------------|:--------|
| `ssl.keyStore.certPaths` | List of certificate file paths (paired with **Key Paths**) | `["/etc/certs/domain1.crt", "/etc/certs/domain2.crt"]` |
| `ssl.keyStore.keyPaths` | List of private key file paths (paired with **Cert Paths**) | `["/etc/keys/domain1.key", "/etc/keys/domain2.key"]` |
| `ssl.keyStore.certPath` | Single certificate file path (fallback when **Cert Paths** is null) | `/etc/certs/redis.crt` |
| `ssl.keyStore.keyPath` | Single private key file path (fallback when **Key Paths** is null) | `/etc/keys/redis.key` |

When populated, **Cert Paths** and **Key Paths** take precedence over singular `certPath` and `keyPath`.

### Helm Chart Configuration

Configure Redis cache and cluster settings via Helm values.

| Property | Description | Default |
|:---------|:------------|:--------|
| `gateway.ratelimit.redis.cluster.nodes` | List of `{host, port}` objects for Redis Cluster nodes (mutually exclusive with `sentinel`) | `unset` |
| `gateway.cacheRedis.maxPoolSize` | Redis cache resource max connections per endpoint (gateway-wide) | `6` |
| `gateway.cacheRedis.maxPoolWaiting` | Redis cache resource max queued requests waiting for a connection | `1024` |
| `gateway.cacheRedis.poolCleanerInterval` | Redis cache resource idle-connection cleaner interval (ms) | `30000` |
| `gateway.cacheRedis.poolRecycleTimeout` | Redis cache resource idle connection recycle timeout (ms) | `180000` |
| `gateway.cacheRedis.maxWaitingHandlers` | Redis cache resource max queued commands on a connection | `1024` |
| `gateway.cacheRedis.connectTimeout` | Redis cache resource TCP connect timeout (ms) | `2000` |
| `gateway.aiVectorStoreRedis.maxPoolSize` | AI vector store Redis resource max connections per endpoint (gateway-wide, APIM 4.12+) | `6` |
| `gateway.aiVectorStoreRedis.maxPoolWaiting` | AI vector store Redis resource max queued requests waiting for a connection | `1024` |
| `gateway.aiVectorStoreRedis.poolCleanerInterval` | AI vector store Redis resource idle-connection cleaner interval (ms) | `30000` |
| `gateway.aiVectorStoreRedis.poolRecycleTimeout` | AI vector store Redis resource idle connection recycle timeout (ms) | `180000` |
| `gateway.aiVectorStoreRedis.maxWaitingHandlers` | AI vector store Redis resource max queued commands on a connection | `1024` |
| `gateway.aiVectorStoreRedis.connectTimeout` | AI vector store Redis resource TCP connect timeout (ms) | `2000` |
