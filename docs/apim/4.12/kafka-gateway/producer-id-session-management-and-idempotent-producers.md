# Producer ID Session Management and Idempotent Producers

## Overview

The gateway manages producer ID sessions for idempotent producers across multiple backend clusters in a Virtual Cluster. When a client enables idempotent production (`enable.idempotence=true`), the gateway fans out the `INIT_PRODUCER_ID` request to all backends, captures the per-cluster producer ID and epoch pairs, and returns a synthetic virtual producer ID to the client. Subsequent `PRODUCE` requests carrying this virtual producer ID are rewritten per backend before forwarding.

## Key Concepts

### Virtual Producer ID Assignment

When an idempotent producer initializes, the gateway:

1. Fans out the `INIT_PRODUCER_ID` request to every backend cluster in the Virtual Cluster.
2. Captures each backend's response: a real `(producerId, producerEpoch)` pair.
3. Synthesizes one virtual producer ID for the client.
4. Stores the mapping from virtual producer ID to per-cluster real producer IDs in `ProducerIdSessionStore` (a distributed cache).
5. Returns the virtual producer ID to the client.

The client uses this virtual producer ID in all subsequent `PRODUCE` requests.

### PRODUCE Request Rewriting

Every `PRODUCE` request carrying a producer ID is rewritten before forwarding to the target backend:

1. The gateway looks up the virtual producer ID in `ProducerIdSessionStore`.
2. The gateway translates the virtual producer ID to the real producer ID for the target cluster.
3. The gateway forwards the rewritten `PRODUCE` request to the backend.

Non-idempotent producers (producer ID = `-1`) are forwarded unchanged.

### PRODUCER_FENCED Error Handling

If the gateway cannot find the virtual producer ID in `ProducerIdSessionStore` (for example, after a pod restart with local-only cache or cache eviction), the gateway returns `PRODUCER_FENCED` to the client. Configuring a distributed cache (`DistributedStoreFactory`) makes this fatal path negligible.

### DELEGATE_TO_BROKER SASL Mechanism

The `DELEGATE_TO_BROKER` mechanism passes the client's SASL handshake through to the backend broker as-is. The gateway does not interpret or validate the SASL exchange—the backend broker handles authentication directly.

{% hint style="info" %}
This mechanism requires no additional configuration fields. When `DELEGATE_TO_BROKER` is selected, no JAAS config, credentials, or other fields are permitted.
{% endhint %}

The gateway forwards the client's SASL exchange to the backend broker without modification. All authentication logic is delegated to the broker.

## Prerequisites

- A Virtual Cluster with two or more backend Kafka clusters must be configured. See [Creating a Kafka Virtual Cluster](#managing-kafka-virtual-clusters).
- The client must enable idempotent production by setting `enable.idempotence=true` in the producer configuration.

## Verification

To verify that the gateway is managing producer ID sessions correctly:

1. Enable idempotent production in your Kafka producer configuration:

   ```properties
   enable.idempotence=true
   ```

2. Produce messages to a topic that spans multiple backend clusters in the Virtual Cluster.
3. Monitor the gateway logs for `INIT_PRODUCER_ID` fan-out and virtual producer ID assignment.
4. Verify that `PRODUCE` requests are rewritten with the correct per-cluster producer ID before forwarding to each backend.

If the gateway returns `PRODUCER_FENCED`, the client will automatically re-create the `KafkaProducer` and re-initialize the producer ID session.
