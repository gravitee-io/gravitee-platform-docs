# Idempotent Producer Routing in Kafka Virtual Clusters

## Idempotent Producer Routing

When a producer enables idempotence (`enable.idempotence=true`), the gateway intercepts the `INIT_PRODUCER_ID` request, fans it out to all backend clusters, and stores a session mapping the virtual producer ID to per-backend real producer IDs.

For subsequent `PRODUCE` requests, the gateway rewrites the producer ID and epoch in-place to match the backend's session before forwarding. If the session is missing (due to cache eviction or pod failover), the gateway returns a synthetic `PRODUCER_FENCED` error to force the client to reinitialize its producer ID. Configuring a distributed cache (`DistributedStoreFactory`) makes the `PRODUCER_FENCED` fatal path negligible for idempotent producers.

Non-idempotent producers (`producerId == NO_PRODUCER_ID`) are forwarded unchanged without session management.

### Error Handling

| Condition | Error Code | Message |
|:----------|:-----------|:--------|
| Virtual PID session missing (cache eviction, pod failover) | `PRODUCER_FENCED` | `"No producer id session for api={} virtualPid={} cluster={}, replying with PRODUCER_FENCED"` |
| Session exists but no mapping for target cluster | `PRODUCER_FENCED` | `"No producer id session for api={} virtualPid={} cluster={}, replying with PRODUCER_FENCED"` |

The gateway uses `PRODUCER_FENCED` rather than `UNKNOWN_PRODUCER_ID` because Kafka clients only re-initialize their producer ID on epoch exhaustion, never on `UNKNOWN_PRODUCER_ID` alone. An idempotent producer would stay stuck in retry loops with stale virtual-PID/sequence state that the gateway can no longer rewrite. `PRODUCER_FENCED` surfaces the failure immediately and forces the application path that re-creates the producer.
