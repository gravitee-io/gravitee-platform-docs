# Kafka Port-Based Routing: Restrictions and Schema Changes

## Restrictions

- Port routing mode is gateway-wide. The `kafka.routingMode` property applies to all APIs on the gateway. Mixed-mode deployments (some APIs using host routing, others using port routing) are not supported.
- Port routing is available only for native Kafka APIs. Proxy and message APIs do not support port-based routing.
- All port values must fall within the range 1024–65535.
- The bootstrap port must not fall within the broker port range.
- Port allocations must not conflict with other plans in the same environment (overlapping broker ranges, duplicate bootstrap ports, or bootstrap ports inside another plan's broker range).
- Broker slot assignment is deterministic but not configurable. Backend broker node IDs are sorted ascending and assigned sequential slots starting from `brokerRangeStart`. Administrators cannot manually map specific node IDs to specific ports.
- The default broker range size is fixed at 3 brokers (`bootstrapPort + 1` to `bootstrapPort + 3`) when auto-filled. This default cannot be customized via configuration.
- The console does not verify that OS-level ports are free at plan save time. A plan may save successfully but fail to deploy if the ports are already bound by another process.
- Broker range changes cause client reconnections. Modifying `brokerRangeStart` or `brokerRangeEnd` on a deployed plan reassigns broker slots, which breaks active connections. Clients automatically reconnect on their next metadata refresh, but in-flight requests may fail.
- MongoDB row-level locks: conflict detection degrades to non-locking queries on MongoDB unless multi-document transactions are enabled with a replica set or sharded cluster. Concurrent plan saves may bypass conflict detection in this configuration.

## Related Changes

### Console Changes

The console adds a **Kafka port routing** section to the plan General step form for native APIs, visible only when the environment toggle is enabled. Three new fields (**Bootstrap port**, **Broker range start**, **Broker range end**) enforce cross-field validation rules (range order, bootstrap exclusion from broker range) and check for port conflicts across all plans in the environment. A warning banner appears when editing broker ranges on deployed APIs, notifying administrators of client reconnection behavior:

"Changing the broker port range will cause a brief reconnection for active consumers. Clients will automatically reconnect on their next metadata refresh — no configuration change required on the client side."

### Schema Changes

The plan model and API schema extend to include `bootstrapPort`, `brokerRangeStart`, and `brokerRangeEnd` properties. A new `kafka_port_ranges` table (JDBC) or collection (MongoDB) stores port allocations indexed by environment and API, enabling conflict detection queries.

### Gateway Changes

The gateway introduces port-based acceptors and broker resolvers that open dedicated TCP listeners per plan and map client connections to backend broker slots based on local port numbers.
