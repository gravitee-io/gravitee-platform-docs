# Producer ID Session Management and Idempotent Producers

## Producer ID Session Management

The gateway manages producer ID sessions for idempotent producers across multiple backend clusters. When a client enables idempotency (`enable.idempotence=true`), the gateway assigns a synthetic virtual producer ID and maintains mappings to per-cluster real producer IDs.

### INIT_PRODUCER_ID

`INIT_PRODUCER_ID` requests are fanned out to all backend clusters. Each backend returns a real `(producerId, producerEpoch)` pair. The gateway captures these per-cluster pairs and stores them in the `ProducerIdSessionStore`, keyed by a synthetic virtual producer ID. The gateway returns the virtual producer ID to the client.

### Produce Requests

`PRODUCE` requests carrying a producer ID are rewritten per backend. The gateway looks up the virtual producer ID in the `ProducerIdSessionStore` and translates it to the real producer ID for the target cluster.

| Scenario | Gateway Behavior |
|:---------|:-----------------|
| Virtual producer ID found in store | Rewrite to real producer ID for target cluster; forward request |
| Virtual producer ID not found in store | Return `PRODUCER_FENCED` (fatal error; client must create new `KafkaProducer`) |
| Non-idempotent producer (PID = -1) | Forward unchanged |

**Rationale for PRODUCER_FENCED**: The gateway deliberately returns `PRODUCER_FENCED` instead of `UNKNOWN_PRODUCER_ID` because Kafka clients only re-initialize their producer ID on epoch exhaustion, never on `UNKNOWN_PRODUCER_ID` alone. An idempotent producer would stay stuck in retry loops with stale virtual-PID/sequence state that the gateway can no longer rewrite. `PRODUCER_FENCED` surfaces the failure immediately and forces the application path that re-creates the producer.
