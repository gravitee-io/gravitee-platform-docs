# Configure Gateway-Wide Redis Resource Settings

## Gateway Configuration

### Redis Cache Resource Pool Settings

Configure gateway-wide connection pool and timeout settings in `gravitee.yml` under `resources.cacheRedis`. These settings apply to all Cache Redis resources across all APIs.

| Property | Description | Example |
|:---------|:------------|:--------|
| `resources.cacheRedis.maxPoolSize` | Maximum number of connections in the pool (gateway-wide) | `6` (default) |
| `resources.cacheRedis.maxPoolWaiting` | Maximum number of requests waiting for a connection from the pool | `1024` (default) |
| `resources.cacheRedis.poolCleanerInterval` | Interval in milliseconds between pool cleaner runs | `30000` (default) |
| `resources.cacheRedis.poolRecycleTimeout` | Timeout in milliseconds for recycling idle connections | `180000` (default) |
| `resources.cacheRedis.maxWaitingHandlers` | Maximum number of waiting handlers for the Redis client | `1024` (default) |
| `resources.cacheRedis.connectTimeout` | Maximum time in milliseconds to establish a connection | `2000` (default) |

### AI Vector Store Redis Resource Pool Settings

Configure gateway-wide connection pool and timeout settings for AI vector store Redis resources in `gravitee.yml` under `resources.aiVectorStoreRedis`.

| Property | Description | Example |
|:---------|:------------|:--------|
| `resources.aiVectorStoreRedis.maxPoolSize` | Maximum simultaneous connections per Redis endpoint | `6` (default) |
| `resources.aiVectorStoreRedis.maxPoolWaiting` | Maximum queued requests waiting for a connection | `1024` (default) |
| `resources.aiVectorStoreRedis.poolCleanerInterval` | Idle-connection cleaner interval in milliseconds | `30000` (default) |
| `resources.aiVectorStoreRedis.poolRecycleTimeout` | Idle connection recycle timeout in milliseconds | `180000` (default) |
| `resources.aiVectorStoreRedis.maxWaitingHandlers` | Maximum queued commands on a connection | `1024` (default) |
| `resources.aiVectorStoreRedis.connectTimeout` | TCP connect timeout in milliseconds | `2000` (default) |

### Redis Repository Configuration

Configure Redis for rate limiting and distributed synchronization in `gravitee.yml` under `repositories.ratelimit.redis`.

| Property | Description | Example |
|:---------|:------------|:--------|
| `repositories.ratelimit.redis.host` | Redis host | `localhost` (default) |
| `repositories.ratelimit.redis.port` | Redis port | `6379` (default) |
| `repositories.ratelimit.redis.username` | Redis username for ACL authentication | `admin` |
| `repositories.ratelimit.redis.password` | Redis password | `secret` |
| `repositories.ratelimit.redis.ssl` | Enable SSL/TLS | `false` (default) |
| `repositories.ratelimit.redis.trustAll` | Trust all certificates when SSL enabled | `true` (default) |
| `repositories.ratelimit.redis.hostnameVerificationAlgorithm` | Hostname verification algorithm: `NONE`, `HTTPS`, `LDAPS` | `NONE` (default) |
| `repositories.ratelimit.redis.tlsProtocols` | Enabled TLS protocols (comma-delimited) | `TLSv1.2,TLSv1.3` |
| `repositories.ratelimit.redis.tlsCiphers` | Enabled TLS cipher suites (comma-delimited) | `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256` |
| `repositories.ratelimit.redis.alpn` | Enable ALPN | `false` (default) |
| `repositories.ratelimit.redis.openssl` | Use OpenSSL engine | `false` (default) |
| `repositories.ratelimit.redis.tcp.connectTimeout` | TCP connect timeout in milliseconds | `5000` (default) |
| `repositories.ratelimit.redis.tcp.idleTimeout` | TCP idle timeout in milliseconds | `0` (default, disabled) |
| `repositories.ratelimit.redis.sentinel.master` | Sentinel master name (required when Sentinel enabled) | `sentinel-master` |
| `repositories.ratelimit.redis.sentinel.nodes[].host` | Sentinel node host | `sentinel1.example.com` |
| `repositories.ratelimit.redis.sentinel.nodes[].port` | Sentinel node port | `26379` |
| `repositories.ratelimit.redis.sentinel.password` | Sentinel password | `sentinel-secret` |
| `repositories.ratelimit.redis.cluster.nodes[].host` | Redis Cluster node host | `redis1.example.com` |
| `repositories.ratelimit.redis.cluster.nodes[].port` | Redis Cluster node port | `6379` |
| `repositories.ratelimit.redis.truststore.type` | Truststore type: `PEM`, `PKCS12`, `JKS` | `PEM` |
| `repositories.ratelimit.redis.truststore.path` | Truststore file path | `/etc/ssl/truststore.pem` |
| `repositories.ratelimit.redis.truststore.password` | Truststore password (PKCS12/JKS only) | `truststore-pass` |
| `repositories.ratelimit.redis.truststore.alias` | Truststore alias (PKCS12/JKS only) | `redis-ca` |
| `repositories.ratelimit.redis.keystore.type` | Keystore type: `PEM`, `PKCS12`, `JKS` | `PEM` |
| `repositories.ratelimit.redis.keystore.path` | Keystore file path (PKCS12/JKS only) | `/etc/ssl/keystore.p12` |
| `repositories.ratelimit.redis.keystore.password` | Keystore password (PKCS12/JKS only) | `keystore-pass` |
| `repositories.ratelimit.redis.keystore.alias` | Keystore alias (PKCS12/JKS only) | `redis-client` |
| `repositories.ratelimit.redis.keystore.certificates[].cert` | PEM certificate path (multi-cert PEM keystore) | `/etc/ssl/cert1.pem` |
| `repositories.ratelimit.redis.keystore.certificates[].key` | PEM key path (multi-cert PEM keystore) | `/etc/ssl/key1.pem` |

### Helm Chart Configuration

Configure Redis cache resource pool settings and Redis Cluster nodes for rate limiting in the Gravitee API Management gateway Helm chart under `gateway`.

| Property | Description | Example |
|:---------|:------------|:--------|
| `gateway.cacheRedis.maxPoolSize` | Redis cache resource max connections per endpoint | `60` (default) |
| `gateway.cacheRedis.maxPoolWaiting` | Redis cache resource max queued requests | `1024` (default) |
| `gateway.cacheRedis.poolCleanerInterval` | Redis cache resource idle-connection cleaner interval in milliseconds | `30000` (default) |
| `gateway.cacheRedis.poolRecycleTimeout` | Redis cache resource idle connection recycle timeout in milliseconds | `180000` (default) |
| `gateway.cacheRedis.maxWaitingHandlers` | Redis cache resource max queued commands on a connection | `1024` (default) |
| `gateway.cacheRedis.connectTimeout` | Redis cache resource TCP connect timeout in milliseconds | `2000` (default) |
| `gateway.aiVectorStoreRedis.maxPoolSize` | AI vector store Redis resource max connections per endpoint | `12` (default) |
| `gateway.aiVectorStoreRedis.maxPoolWaiting` | AI vector store Redis resource max queued requests | `1024` (default) |
| `gateway.aiVectorStoreRedis.poolCleanerInterval` | AI vector store Redis resource idle-connection cleaner interval in milliseconds | `30000` (default) |
| `gateway.aiVectorStoreRedis.poolRecycleTimeout` | AI vector store Redis resource idle connection recycle timeout in milliseconds | `180000` (default) |
| `gateway.aiVectorStoreRedis.maxWaitingHandlers` | AI vector store Redis resource max queued commands on a connection | `1024` (default) |
| `gateway.aiVectorStoreRedis.connectTimeout` | AI vector store Redis resource TCP connect timeout in milliseconds | `2000` (default) |
| `gateway.ratelimit.redis.cluster.nodes[].host` | Redis Cluster node host for rate limiting | `redis1.example.com` |
| `gateway.ratelimit.redis.cluster.nodes[].port` | Redis Cluster node port for rate limiting | `6379` |
