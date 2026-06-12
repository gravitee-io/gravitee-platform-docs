# Configure Redis Cache Resource Global Settings

## Gateway configuration

### Global Redis pool settings

Configure these properties in `gravitee.yml` to control connection pooling and timeouts for all Redis cache resources:

| Property | Description | Default |
|:---------|:------------|:--------|
| `resources.cacheRedis.maxPoolSize` | Maximum number of connections in the pool | 6 |
| `resources.cacheRedis.maxPoolWaiting` | Maximum number of requests waiting for a connection from the pool | 1024 |
| `resources.cacheRedis.poolCleanerInterval` | Interval in milliseconds between pool cleaner runs | 30000 |
| `resources.cacheRedis.poolRecycleTimeout` | Timeout in milliseconds for recycling idle connections | 180000 |
| `resources.cacheRedis.maxWaitingHandlers` | Maximum number of waiting handlers for the Redis client | 1024 |
| `resources.cacheRedis.connectTimeout` | Maximum time in milliseconds to establish a connection | 2000 |

These settings apply to all Redis cache resources targeting the same endpoint. All cache resources sharing the same host, port, password, SSL configuration, and sentinel configuration share a single Redis client instance.

Example configuration:

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

### Per-Resource Connection Settings

Configure these properties in the Redis cache resource definition for each API:

| Property | Description | Example |
|:---------|:------------|:--------|
| `host` | Redis host (supports EL) | "redis.example.com" |
| `port` | Redis port (supports EL) | 6379 |
| `password` | Redis password (supports EL and secrets) | "{#secrets['redis-password']}" |
| **Use Ssl** | Use SSL connections | true |
| `ssl.trustStore.type` | Trust store type (JKS, PKCS12, PEM, None) | "PEM" |
| `ssl.trustStore.path` | Path to trust store file | "/etc/ssl/certs/ca.pem" |
| `ssl.hostnameVerificationAlgorithm` | Hostname verification algorithm (HTTPS, LDAPS, NONE) | "HTTPS" |
| `ssl.tlsProtocols` | Allowed TLS protocol versions | ["TLSv1.3"] |
| `ssl.tlsCiphers` | Allowed TLS cipher suites | ["TLS_AES_256_GCM_SHA384"] |
| `sentinel.enabled` | Enable Redis Sentinel mode | false |
| `sentinel.masterId` | Sentinel master ID (supports EL) | "mymaster" |
| `sentinel.password` | Sentinel password (supports EL and secrets) | "{#secrets['sentinel-password']}" |
| `sentinel.nodes` | Sentinel node list (host/port pairs) | [{"host": "sentinel1", "port": 26379}] |
| `cluster.enabled` | Enable Redis Cluster mode | false |
| `cluster.nodes` | Cluster node list (host/port pairs) | [{"host": "node1", "port": 6379}] |
| **Release Cache** | Release the cache when API is stopped | false |
| **Time To Live Seconds** | Maximum seconds an element can exist in cache (0 = infinite) | 600 |
| `timeout` | Command timeout in milliseconds. If a Redis command takes longer than this, it will fail. | 2000 |

{% hint style="warning" %}
When **Use Ssl** is true but no `ssl` options are configured, the resource falls back to `trustAll=true` and `hostnameVerificationAlgorithm=NONE` (bypasses TLS certificate validation). A warning is logged. Configure `ssl.trustStore` and `ssl.hostnameVerificationAlgorithm` to harden production deployments.
{% endhint %}

{% hint style="info" %}
Old API definitions with nested `"standalone": {"host": "...", "port": ...}` are deserialized into flat `host` and `port` fields. Serialization emits both flat fields and the nested `standalone` object for compatibility with old gateways. Old API definitions with top-level `sentinelMode=true` are treated as `sentinel.enabled=true`. Serialization emits both `sentinel.enabled` and top-level `sentinelMode` for compatibility. The **Max Total** property (legacy Lettuce pool setting) is silently ignored on deserialization.
{% endhint %}
