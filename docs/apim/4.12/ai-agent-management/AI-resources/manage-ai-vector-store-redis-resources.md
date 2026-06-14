# Manage AI Vector Store Redis Resources

## Managing AI Vector Store Redis Resources

The AI vector store Redis resource connects to Redis Stack or RedisSearch to store and query vector embeddings. Configure the resource with a Redis URL, username, password, index name, prefix, query template, and score field. The resource uses a shared Redis client factory with gateway-wide pool and timeout settings. Configure these settings in [`gravitee.yml`](../../configure-and-manage-the-platform/gravitee-gateway/configure-gateway-wide-redis-resource-settings.md#ai-vector-store-redis-resource-pool-settings):

### Configuration

Configure the AI vector store Redis resource with the following properties:

| Property | Description | Example |
|:---------|:------------|:--------|
| **URL** | Redis connection URL (supports EL). Use scheme `rediss://` to enable TLS with default system-CA validation. | `rediss://localhost:6379` |
| **Username** | Redis username for authentication (supports EL and secrets) | `admin` |
| **Password** | Redis password (supports EL and secrets) | `secret` |
| **Index Name** | Name of the Redis vector index | `product-embeddings` |
| **Prefix** | Key prefix for stored vectors | `vec:` |
| **Query Template** | Template for vector search queries | `*=>[KNN 10 @embedding $BLOB AS score]` |
| **Score Field** | Field name for similarity scores | `score` |

### Restrictions

* Requires Gravitee API Management 4.12 or later and Java 21 or later.
* Invalid Redis URLs trigger `IllegalArgumentException` with message `"Invalid Redis URL in AI vector store configuration: [<url>]"`.
