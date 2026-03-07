### Trigger API Schema

The Trigger model now includes `created_at` and `updated_at` fields (JSON property names) to support schedule anchoring. These fields are populated automatically by the Alert Engine and returned in API responses. Clients should not set these fields when creating triggers; they are managed server-side.

| Field | Type | Description |
|:------|:-----|:------------|
| `created_at` | Date | Timestamp when the trigger was created |
| `updated_at` | Date | Timestamp when the trigger was last updated |

### Restrictions

- Cluster mode requires a valid Gravitee license key
- The primary node is always the oldest member in the Hazelcast cluster (first in member list)
- Window-based alert durations must be greater than 0 (throws `IllegalArgumentException` otherwise)
- If a trigger's anchor timestamp (`updatedAt` or `createdAt`) is in the future, the engine logs a warning and falls back to scheduling from the current time
- Negative initial delays are clamped to 0 (immediate scheduling)
- Default filters are enabled by default; disabling them may allow cross-installation alert routing
- Integration tests require Docker runtime (Testcontainers starts a Kafka container)

### Related Changes

The `gravitee-alert-api` dependency was upgraded from 2.0.0 to 3.0.0 to support the timestamp fields.
