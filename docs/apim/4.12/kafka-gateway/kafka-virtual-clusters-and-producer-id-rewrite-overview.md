# Kafka Virtual Clusters and Producer ID Rewrite Overview

## Overview

Kafka Virtual Clusters enable API administrators to present multiple backend Kafka clusters as a single unified cluster to client applications. This feature introduces three persistent entities: Kafka Clusters (reusable connection profiles), Kafka Virtual Clusters (fan-out wrappers), and Kafka APIs (V4 native protocol endpoints). Producer ID rewrite ensures idempotent producers function correctly when routing through virtual clusters by translating producer IDs and epochs in-place.

## Key Concepts

### Kafka Cluster

A Kafka Cluster is a reusable connection profile to one or more real Kafka backends. Each Kafka Cluster entity stores a name and one or more connections, where each connection defines bootstrap servers and security configuration (PLAINTEXT, SSL, SASL_PLAINTEXT, or SASL_SSL). Multiple APIs can reference the same Kafka Cluster entity; updates to the cluster propagate to all referencing APIs. Kafka Clusters are managed in the Console under **Kafka Clusters**.

### Kafka Virtual Cluster

A Kafka Virtual Cluster is a fan-out wrapper that presents multiple backend Kafka clusters as a single virtual cluster to clients. Each Virtual Cluster entity stores a list of backends, where each backend is a `(clusterCrossId, connectionCrossId)` pair referencing one connection from an underlying Kafka Cluster entity. Virtual Clusters are meaningful only when two or more Kafka Cluster entities exist; with one backend, a direct Cluster reference is sufficient. Virtual Clusters are managed in the Console under **Kafka Virtual Clusters**.

### Kafka API (V4 Native Protocol)

A Kafka API is a standard V4 API whose endpoint connector points at either (a) a raw bootstrap address, (b) one Kafka Cluster entity plus connection, or (c) one Kafka Virtual Cluster entity. The endpoint connector type determines the routing behavior:

* `native-kafka` for inline broker configuration
* `native-kafka-cluster` for Kafka Cluster entity references
* `native-kafka-virtual-cluster` for Kafka Virtual Cluster entity references

### Producer ID Session Rewrite

When a client uses an idempotent producer against a virtual cluster, the gateway maintains a mapping between the client's virtual producer ID and the real producer IDs assigned by each backend cluster. On each `PRODUCE` request, the gateway rewrites the producer ID and epoch in the record batches in-place, recalculates the CRC32C checksum, and forwards the mutated batch to the target backend. If the virtual producer ID session is missing or no cluster mapping exists, the gateway returns a synthetic `PRODUCER_FENCED` error response, forcing the client to reinitialize the producer.

### Lifecycle States

Kafka Cluster and Kafka Virtual Cluster entities support three lifecycle states:

* `UNDEPLOYED`: created but not active on the gateway
* `PENDING`: deployment in progress
* `DEPLOYED`: active on the gateway

Users deploy clusters via the Console; deployed clusters are synchronized to the gateway and become available for API endpoint references. Deleting a deployed cluster automatically undeploys it first.

### Delegate SASL Replay

When a client connects to the gateway with SASL PLAIN credentials and the gateway must open a sub-connection to a backend cluster (e.g., for cross-cluster fan-out of `FIND_COORDINATOR` or `DescribeGroups` requests), the gateway captures the client's SASL authentication bytes and replays the `SASL_HANDSHAKE` and `SASL_AUTHENTICATE` sequence on the sub-connection. This ensures the sub-connection is authenticated with the same credentials as the primary connection. Only SASL PLAIN is replay-safe; AWS_MSK_IAM, SCRAM, and GSSAPI mechanisms are not captured.
