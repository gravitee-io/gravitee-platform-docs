# Create and Configure Redis Cache Resources

## Creating a Redis Cache Resource

Configure a Redis cache resource for use with Cache or Data Cache policies. Pool settings are sourced from `gravitee.yml` and apply gateway-wide to all resources sharing the same endpoint.

### Per-Resource Configuration

Configure the following properties in the API definition or Management Console:

| Property | Description | Default |
|:---------|:------------|:--------|
| **Host** | Redis instance host (supports EL) | `localhost` |
| **Port** | Redis instance port (supports EL) | `6379` |
| **Username** | Username for Redis ACL authentication (supports EL and secrets) | — |
| **Password** | Redis instance password (supports EL and secrets) | — |
| **Use SSL** | Enable SSL connections to Redis | `true` |
| **Timeout** | Command timeout in milliseconds | `2000` |
| **Time To Live Seconds** | Default TTL for cached entries (0 = no expiration) | `0` |
| **Release Cache** | When enabled, `clear()` deletes keys matching `gravitee:*:<deployAt>` pattern; when disabled, `clear()` is a no-op | `false` |
| **Idle Timeout** | Time in milliseconds after which an idle connection is closed; 0 disables idle timeout (supports EL) | `0` |

### Sentinel Configuration

The following properties are displayed when Sentinel mode is enabled:

| Property | Description | Default |
|:---------|:------------|:--------|
| **Enabled** | Enable Sentinel mode | `true` |
| **Master Id** | Sentinel master id (supports EL) | `sentinel-master` |
| **Password** | Sentinel password (supports EL and secrets) | — |
| **Nodes** | Sentinel nodes (each with `host` and `port`, both support EL) | `[{host: "localhost", port: 26379}]` |

### Cluster Configuration

The following properties are displayed when Cluster mode is enabled:

| Property | Description | Default |
|:---------|:------------|:--------|
| **Enabled** | Enable Cluster mode | `true` |
| **Nodes** | Cluster nodes (each with `host` and `port`, both support EL) | `[]` |
| **Use Replicas** | Read-from-replica policy: `NEVER`, `SHARE`, or `ALWAYS` | `NEVER` |

### SSL Options

The following properties are displayed when **Use SSL** is enabled:

| Property | Description | Example |
|:---------|:------------|:--------|
| **Trust All** | Trust all certificates | `false` |
| **Hostname Verifier** | Enable hostname verification | `true` |
| **Hostname Verification Algorithm** | Hostname verification algorithm (`HTTPS`, `LDAPS`, `NONE`); takes precedence over **Hostname Verifier** | `HTTPS` |
| **Open SSL** | Use OpenSSL engine | `false` |
| **ALPN** | Enable ALPN | `false` |
| **TLS Protocols** | Enabled TLS protocols | `TLSv1.2,TLSv1.3` |
| **TLS Ciphers** | Enabled TLS cipher suites | `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256` |

### Backward Compatibility

* API definitions created before 4.12 with a nested `standalone` object are automatically migrated to flat `host`/`port` fields.

* The legacy **Sentinel Mode** boolean (top-level) is honored regardless of JSON property order. Sentinel mode is detected when `sentinel.enabled=true` AND `sentinel.nodes` is non-empty, OR when the legacy **Sentinel Mode** (top-level) AND `sentinel.nodes` is non-empty.
* The legacy **Max Total** pool setting and per-resource pool settings (**Max Pool Size**, **Max Pool Waiting**, **Pool Cleaner Interval**, **Pool Recycle Timeout**, **Max Waiting Handlers**, **Connect Timeout**) are silently ignored. Pool configuration is sourced from `gravitee.yml`.

### Credential Handling

* When `password` is `null` or blank, both `username` and `password` are set to `null` in `RedisClientOptions`.
* When `password` is not `null`/blank, `username` (may be `null`) and `password` are both applied to `RedisClientOptions`.

### Index Creation Failure

If index creation throws an exception, the error is logged and the resource is marked as started. Redeploy the resource to retry index creation.

### Client Release Logging

When releasing a non-existent registry key, the gateway logs `"Attempted to release unknown Redis client for key [<key>] (double-release bug)"`.
