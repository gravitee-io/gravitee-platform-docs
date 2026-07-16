# Configure Cache Policies to Use Redis Cache Resources

## Configuring Cache Policies

### Cache Policy

The Cache policy caches HTTP responses for a configurable time-to-live (TTL). Configure the policy to reference a Redis cache resource by name. The policy uses asynchronous cache operations to avoid blocking the event loop.

**Binary Cache Storage Format**:

Responses are stored as binary frames (version byte `0x01`) to preserve byte-for-byte fidelity for non-text content. Legacy JSON-format entries (policy version <= 3.0.1) remain readable during rolling upgrades but are not written by 4.12+ gateways.

**Cache Frame Deserialization Failure Handling**:

If the gateway cannot deserialize a cache frame, it logs `"Cannot decode cache frame for key <key>, evicting and refetching"` and evicts the corrupted entry.

### Data Cache Policy

The Data Cache policy performs `SET`, `GET`, or `EVICT` operations on a cache resource. Use it to share state across API executions or implement custom caching logic.

{% hint style="warning" %}
The migration to the AsyncAPI in version 2.0.0+ is a breaking change.
{% endhint %}

**Configuration Fields**:

| Property | Description | Default |
|:---------|:------------|:--------|
| **Cache Key** | Cache key (supports EL) | — |
| **Value** | Value to store (SET only; supports EL) | — |
| Default Operation | Default operation: `SET`, `GET`, or `EVICT` | — |
| Resource | Cache resource name | — |
| **Time To Live** | TTL in seconds (SET only) | `3600` |
| Cache Miss Attribute Key | Attribute key set to `true` on cache miss | `cache_miss` |

**Operation-Specific Behavior**:

| Operation | Value Field | Cache Miss Behavior |
|:----------|:------------|:--------------------|
| `SET` | **Required**. Provides the value to store. | N/A |
| `GET` | **Ignored**. Cached value is stored on execution context under attribute named after resolved **Cache Key**. | Sets **Cache Miss Attribute Key** to `true` if key not found. |
| `EVICT` | **Ignored**. Cached value is stored on execution context under attribute named after resolved **Cache Key** before eviction. | Sets **Cache Miss Attribute Key** to `true` if key not found; eviction proceeds regardless. |

**Validation Rules**:

* **Time To Live** must be greater than 0 for `SET` operations.
* **Value** must be non-empty for `SET` operations.
* **Cache Key** must be non-empty for all operations.
