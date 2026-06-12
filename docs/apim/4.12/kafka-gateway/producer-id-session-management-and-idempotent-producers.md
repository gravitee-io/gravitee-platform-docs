# Producer ID Session Management and Idempotent Producers

## Overview

Producer ID session management enables idempotent producers to operate across multiple backend clusters in a Kafka Virtual Cluster. When a client initializes an idempotent producer, the gateway fans out the `INIT_PRODUCER_ID` request to all backend clusters, captures the per-cluster producer ID and epoch pairs, and synthesizes a single virtual producer ID for the client. Subsequent `PRODUCE` requests carrying the virtual producer ID are rewritten per backend before forwarding.

## INIT_PRODUCER_ID Handling

When a client sends `INIT_PRODUCER_ID` to initialize an idempotent producer, the gateway performs the following steps:

1. Fan out the `INIT_PRODUCER_ID` request to all backend clusters in the virtual cluster.
2. Capture the `(producerId, producerEpoch)` pair returned by each backend cluster.
3. Generate a synthetic virtual producer ID for the client.
4. Store the mapping from the virtual producer ID to the set of backend-specific `(producerId, producerEpoch)` pairs in the `ProducerIdSessionStore`.
5. Return the virtual producer ID to the client in the `INIT_PRODUCER_ID` response.

The client uses the virtual producer ID in all subsequent `PRODUCE` requests. The gateway translates the virtual producer ID to the appropriate backend-specific producer ID before forwarding each request.

## PRODUCE Request Handling

When a `PRODUCE` request arrives, the gateway inspects the producer ID field:

- **Idempotent producer (producer ID ≠ -1)**: The gateway looks up the producer ID in the `ProducerIdSessionStore`. If the virtual producer ID is found, the gateway rewrites the request with the real producer ID for the target backend cluster and forwards the request. If the virtual producer ID is not found, the gateway returns `PRODUCER_FENCED` to the client.
- **Non-idempotent producer (producer ID = -1)**: The gateway forwards the request unchanged without session lookup.

## Cache Miss Behavior

If the gateway cannot find the virtual producer ID in the `ProducerIdSessionStore`, it returns `PRODUCER_FENCED` to the client. This error is fatal for the producer — the client must create a new `KafkaProducer` instance and re-run the bootstrap sequence to obtain a new virtual producer ID.

Cache misses occur when:

- The gateway pod restarts and the session store is not backed by a distributed cache.
- The session entry is evicted from the cache due to memory pressure or TTL expiration.

Configuring a distributed cache via `DistributedStoreFactory` minimizes the occurrence of cache misses by persisting session state across gateway pod restarts.

## PRODUCER_FENCED Rationale

The gateway deliberately returns `PRODUCER_FENCED` instead of `UNKNOWN_PRODUCER_ID` when the virtual producer ID is not found in the session store. Kafka clients only re-initialize the producer ID on epoch exhaustion, never on `UNKNOWN_PRODUCER_ID` alone. If the gateway returned `UNKNOWN_PRODUCER_ID`, the idempotent producer would remain stuck in retry loops with stale virtual producer ID and sequence state that the gateway can no longer rewrite. `PRODUCER_FENCED` surfaces the failure immediately and forces the application path that re-creates the producer.
