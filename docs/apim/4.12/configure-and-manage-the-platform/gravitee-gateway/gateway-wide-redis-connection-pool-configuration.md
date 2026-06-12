# Gateway-Wide Redis Connection Pool Configuration

## Gateway Configuration

### Cache Redis Resource Pool Settings

Configure gateway-wide connection pool parameters for [cache-redis resources](../../upgrade-guides/migrate-from-redis-cache-resource-4.x-to-5.x.md#creating-redis-cache-resources) in `gravitee.yml`:

| Property | Description | Default |
|:---------|:------------|:--------|
| `resources.cacheRedis.maxPoolSize` | Maximum simultaneous connections per Redis endpoint | `6` |
| `resources.cacheRedis.maxPoolWaiting` | Maximum queued requests waiting for a connection | `1024` |
| `resources.cacheRedis.poolCleanerInterval` | Idle-connection cleaner interval (milliseconds) | `30000` |
| `resources.cacheRedis.poolRecycleTimeout` | Idle connection recycle timeout (milliseconds) | `180000` |
| `resources.cacheRedis.maxWaitingHandlers` | Maximum queued commands on a connection | `1024` |
| `resources.cacheRedis.connectTimeout` | TCP connect timeout (milliseconds) | `2000` |

### AI Vector Store Redis Pool Settings

Configure gateway-wide connection pool parameters for AI vector store Redis resources in `gravitee.yml`:

| Property | Description | Default |
|:---------|:------------|:--------|
| `resources.aiVectorStoreRedis.maxPoolSize` | Maximum simultaneous connections per Redis endpoint | `6` |
| `resources.aiVectorStoreRedis.maxPoolWaiting` | Maximum queued requests waiting for a connection | `1024` |
| `resources.aiVectorStoreRedis.poolCleanerInterval` | Idle-connection cleaner interval (milliseconds) | `30000` |
| `resources.aiVectorStoreRedis.poolRecycleTimeout` | Idle connection recycle timeout (milliseconds) | `180000` |
| `resources.aiVectorStoreRedis.maxWaitingHandlers` | Maximum queued commands on a connection | `1024` |
| `resources.aiVectorStoreRedis.connectTimeout` | TCP connect timeout (milliseconds) | `2000` |

### Rate Limit Redis Cluster Configuration

Enable Redis Cluster mode for rate limiting by configuring cluster nodes in `gravitee.yml`:

| Property | Description | Example |
|:---------|:------------|:--------|
| `repositories.ratelimit.redis.cluster.nodes[N].host` | Redis Cluster node hostname | `redis-node1` |
| `repositories.ratelimit.redis.cluster.nodes[N].port` | Redis Cluster node port | `6379` |
| `repositories.ratelimit.redis.cluster.useReplicas` | Replica read policy (hardcoded to `NEVER` for rate limiting) | `NEVER` |

Cluster mode is mutually exclusive with Sentinel mode. Configure cluster nodes **or** sentinel nodes, not both.

### Redis Client Options

Configure Redis connection parameters for cache and AI vector store resources:

| Property | Description | Default |
|:---------|:------------|:--------|
| `host` | Redis host | `localhost` |
| `port` | Redis port | `6379` |
| `username` | Redis ACL username | (none) |
| `password` | Redis password | (none) |
| **Use Ssl** | Enable SSL/TLS connections | `false` |
| **Max Pool Size** | Maximum connections in the pool (deprecated; use gateway-wide setting) | `6` |
| **Max Pool Waiting** | Maximum requests waiting for a connection (deprecated; use gateway-wide setting) | `1024` |
| **Pool Cleaner Interval** | Pool cleaner interval in milliseconds (deprecated; use gateway-wide setting) | `30000` |
| **Pool Recycle Timeout** | Idle connection recycle timeout in milliseconds (deprecated; use gateway-wide setting) | `180000` |
| **Max Waiting Handlers** | Maximum waiting handlers (deprecated; use gateway-wide setting) | `1024` |
| **Connect Timeout** | TCP connect timeout in milliseconds (deprecated; use gateway-wide setting) | `2000` |
| **Idle Timeout** | Idle connection timeout in milliseconds; 0 disables idle timeout | `0` |

### Redis Sentinel Options

Configure Sentinel mode for high-availability master discovery:

| Property | Description | Default |
|:---------|:------------|:--------|
| `sentinel.enabled` | Enable Sentinel mode | `true` |
| `sentinel.masterId` | Sentinel master ID | (required when Sentinel enabled) |
| `sentinel.password` | Sentinel password for AUTH to sentinel nodes | (none) |
| `sentinel.nodes[N].host` | Sentinel node hostname | (required when Sentinel enabled) |
| `sentinel.nodes[N].port` | Sentinel node port | (required when Sentinel enabled) |

### Redis Cluster Options

Configure Cluster mode for horizontal sharding:

| Property | Description | Default |
|:---------|:------------|:--------|
| `cluster.enabled` | Enable Cluster mode | `true` |
| `cluster.nodes[N].host` | Cluster node hostname | (required when Cluster enabled) |
| `cluster.nodes[N].port` | Cluster node port | (required when Cluster enabled) |
| `cluster.useReplicas` | Replica read policy: `NEVER`, `SHARE`, or `ALWAYS` | `NEVER` |

### SSL/TLS Options

Configure SSL/TLS encryption for Redis connections:

| Property | Description | Default |
|:---------|:------------|:--------|
| `ssl.trustAll` | Trust all server certificates (disables validation) | `false` (defaults to `true` when SSL enabled without explicit truststore) |
| `ssl.hostnameVerifier` | Enable hostname verification (deprecated; use **Hostname Verification Algorithm**) | `true` |
| `ssl.hostnameVerificationAlgorithm` | Hostname verification algorithm: `HTTPS`, `LDAPS`, or `NONE` | (none; falls back to **Hostname Verifier** boolean) |
| `ssl.openSsl` | Use OpenSSL engine | `false` |
| `ssl.alpn` | Enable ALPN (Application-Layer Protocol Negotiation) | `false` |
| `ssl.tlsProtocols` | Enabled TLS protocol versions (e.g., `TLSv1.2`, `TLSv1.3`) | (none; uses JVM defaults) |
| `ssl.tlsCiphers` | Enabled TLS cipher suites | (none; uses JVM defaults) |
| `ssl.trustStore.type` | Truststore type: `pem`, `pkcs12`, `jks`, or `NONE` | `NONE` |
| `ssl.trustStore.path` | Path to truststore file | (required when truststore type is not `NONE`) |
| `ssl.keyStore.type` | Keystore type: `pem`, `pkcs12`, `jks`, or `NONE` | `NONE` |
| `ssl.keyStore.path` | Path to PKCS12 or JKS keystore file | (required for `pkcs12` or `jks` types) |
| `ssl.keyStore.certPath` | Path to PEM certificate file (singular) | (required for `pem` type when **Cert Paths** not used) |
| `ssl.keyStore.keyPath` | Path to PEM private key file (singular) | (required for `pem` type when **Key Paths** not used) |
| `ssl.keyStore.certPaths` | Paths to multiple PEM certificate files (for multi-certificate keystores) | (optional; takes precedence over **Cert Path**) |
| `ssl.keyStore.keyPaths` | Paths to multiple PEM private key files (for multi-certificate keystores) | (optional; takes precedence over **Key Path**) |

{% hint style="info" %}
**Multi-certificate PEM keystores**: When **Cert Paths** and **Key Paths** are populated, they must be the same size and both non-null. Index `i` of **Cert Paths** pairs with index `i` of **Key Paths**. Use this configuration to present multiple keypairs (e.g., RSA + ECDSA) for TLS negotiation.
{% endhint %}

{% hint style="warning" %}
**Hostname verification precedence**: When **Hostname Verification Algorithm** is set to a non-`NONE` value, it takes precedence over the **Hostname Verifier** boolean. If `hostnameVerifier=false` but `hostnameVerificationAlgorithm=HTTPS`, verification is **enabled**.
{% endhint %}

### Rate Limit Redis SSL Configuration

Configure SSL/TLS encryption for rate-limit Redis connections in `gravitee.yml`:

| Property | Description | Example |
|:---------|:------------|:--------|
| `repositories.ratelimit.redis.hostnameVerificationAlgorithm` | Hostname verification algorithm: `NONE`, `HTTPS`, or `LDAPS` | `NONE` |
| `repositories.ratelimit.redis.trustAll` | Trust all certificates when SSL enabled without explicit truststore | `true` |
| `repositories.ratelimit.redis.keystore.type` | Keystore type: `pem`, `pkcs12`, or `jks` | `pem` |
| `repositories.ratelimit.redis.keystore.certificates[N].cert` | Path to PEM certificate file (supports multiple certificates) | `/path/to/cert.pem` |
| `repositories.ratelimit.redis.keystore.certificates[N].key` | Path to PEM private key file (supports multiple keys) | `/path/to/key.pem` |
| `repositories.ratelimit.redis.keystore.path` | Path to PKCS12 or JKS keystore file | `/path/to/keystore.p12` |
| `repositories.ratelimit.redis.truststore.type` | Truststore type: `pem`, `pkcs12`, or `jks` | `pem` |
| `repositories.ratelimit.redis.truststore.path` | Path to truststore file | `/path/to/truststore.pem` |

{% hint style="warning" %}
**SSL validation rules**:
* When `ssl=true` and **Trust All** is unset, **Trust All** defaults to `true` (backward compatibility)
* When `ssl=true` and `trustAll=false`, a truststore must be configured
* When `ssl=true` and `keystore.type=pem`, both `keystore.certificates[0].cert` and `keystore.certificates[0].key` are required
* When `ssl=true` and `keystore.type=pkcs12` or `jks`, `keystore.path` is required
{% endhint %}

### Helm Chart Configuration

Configure Redis resource pools and cluster topology via Helm values:

| Property | Description | Default |
|:---------|:------------|:--------|
| `gateway.ratelimit.redis.cluster.nodes` | Array of `{host, port}` objects for Redis Cluster nodes (mutually exclusive with `sentinel`) | (unset) |
| `gateway.cacheRedis.maxPoolSize` | Rendered to `resources.cacheRedis.maxPoolSize` in gravitee.yml | `6` |
| `gateway.cacheRedis.maxPoolWaiting` | Rendered to `resources.cacheRedis.maxPoolWaiting` | `1024` |
| `gateway.cacheRedis.poolCleanerInterval` | Rendered to `resources.cacheRedis.poolCleanerInterval` | `30000` |
| `gateway.cacheRedis.poolRecycleTimeout` | Rendered to `resources.cacheRedis.poolRecycleTimeout` | `180000` |
| `gateway.cacheRedis.maxWaitingHandlers` | Rendered to `resources.cacheRedis.maxWaitingHandlers` | `1024` |
| `gateway.cacheRedis.connectTimeout` | Rendered to `resources.cacheRedis.connectTimeout` | `2000` |
| `gateway.aiVectorStoreRedis.maxPoolSize` | Rendered to `resources.aiVectorStoreRedis.maxPoolSize` (APIM 4.12+) | `6` |
| `gateway.aiVectorStoreRedis.maxPoolWaiting` | Rendered to `resources.aiVectorStoreRedis.maxPoolWaiting` | `1024` |
| `gateway.aiVectorStoreRedis.poolCleanerInterval` | Rendered to `resources.aiVectorStoreRedis.poolCleanerInterval` | `30000` |
| `gateway.aiVectorStoreRedis.poolRecycleTimeout` | Rendered to `resources.aiVectorStoreRedis.poolRecycleTimeout` | `180000` |
| `gateway.aiVectorStoreRedis.maxWaitingHandlers` | Rendered to `resources.aiVectorStoreRedis.maxWaitingHandlers` | `1024` |
| `gateway.aiVectorStoreRedis.connectTimeout` | Rendered to `resources.aiVectorStoreRedis.connectTimeout` | `2000` |
