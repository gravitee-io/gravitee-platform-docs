
## Overview


Kafka Virtual Clusters enable you to present multiple backend Kafka clusters as a single unified cluster to client applications. This capability allows you to distribute topics across separate physical clusters while maintaining a single client connection point, simplifying multi-cluster architectures and enabling workload isolation without client-side complexity. Virtual clusters support consumer group multiplexing, idempotent producer session management, and SASL credential delegation across backends.

## Key Concepts

### Virtual Cluster Architecture

A Kafka Virtual Cluster is a fan-out wrapper that aggregates multiple backend Kafka clusters into one virtual cluster. The gateway merges metadata from all backend clusters, rewrites broker IDs into non-overlapping virtual ranges, and routes client requests to the appropriate backend based on topic ownership. Clients connect to a single bootstrap address and receive a unified view of all topics across the backends.

Each backend cluster is assigned a range of 10,000 virtual broker IDs. Cluster index 0 receives virtual IDs 10000–19999, cluster index 1 receives 20000–29999, and so on. The gateway rewrites broker IDs in metadata responses and routes subsequent client connections to the correct backend based on the virtual broker ID in the client's request.

**Virtual broker ID mapping formula:**

- `virtualBrokerId = (clusterIndex + 1) * 10000 + realBrokerId`
- `clusterIndex = virtualBrokerId / 10000 - 1`
- `realBrokerId = virtualBrokerId % 10000`

**Constraints:**

- Maximum clusters: 214,748 (`Integer.MAX_VALUE / 10000 - 1`)
- Maximum brokers per cluster: 9,999 (real broker IDs must be < 10,000)

### Cluster and Virtual Cluster Entities

The platform provides three persistent configuration entities for Kafka connectivity:

| Entity | Purpose | Configuration |
|:-------|:--------|:--------------|
| **Kafka Cluster** | Reusable connection profile to a single backend Kafka cluster | Name, one or more connections (each with bootstrap servers and security settings) |
| **Kafka Virtual Cluster** | Fan-out wrapper presenting multiple Kafka Clusters as one | List of backend references (each selecting one Cluster and one of its connections) |
| **Kafka API** | V4 native protocol API with endpoint connector | Points to a raw bootstrap address, a Kafka Cluster, or a Kafka Virtual Cluster |

Kafka Cluster and Virtual Cluster entities exist to share backend configuration across multiple APIs. Updating a Cluster entity propagates changes to every API that references it. A single backend often exposes multiple listeners (e.g., port 9091 PLAINTEXT for internal, port 9095 SASL_SSL for partners). Modelling them as siblings inside one Cluster lets you switch between auth profiles per API without re-creating the whole cluster.

Both Kafka Cluster and Virtual Cluster entities are governed by a single **CLUSTER** environment-scoped permission (mask 4000). There is no separate VIRTUAL_CLUSTER permission.

### Consumer Group Multiplexing

When a consumer group subscribes to topics that span multiple backend clusters, the gateway creates shadow consumer groups on each backend (named `<groupId>__shadow-c<N>`) and merges their assignments into a single response. The gateway maintains a membership store keyed by API ID, client group ID, and client member ID, and fans out heartbeats and offset commits to the appropriate backends based on topic ownership.

Cross-cluster subscriptions are supported only when using the classic consumer protocol with range or round-robin assignors. Subscriptions using the cooperative-sticky assignor or the next-generation consumer protocol (KIP-848) that span multiple clusters are refused with `INCONSISTENT_GROUP_PROTOCOL` or `INVALID_REQUEST` errors. Static membership (`group.instance.id`) on MESH KIP-848 is supported via `ShadowNamer.instanceId(client, clusterIndex)`.

### Idempotent Producer Session Management

The gateway maintains a session store mapping virtual producer IDs to per-backend real producer IDs. When an idempotent producer sends a PRODUCE request, the gateway rewrites the producer ID and epoch to match the backend's session before forwarding. If the session is missing (due to cache eviction or pod failover), the gateway returns a synthetic `PRODUCER_FENCED` error to force the client to reinitialize its producer ID. Configuring a distributed cache makes the `PRODUCER_FENCED` fatal path negligible for idempotent producers.

### SASL Delegate-to-Broker Authentication

When a backend cluster is configured with the **SASL Mechanism** set to **Delegate To Broker**, the gateway captures the client's SASL credentials during the initial handshake and replays them when opening connections to backend clusters. This mode allows the gateway to authenticate on behalf of the client without storing backend credentials, enabling per-user authorization at the backend level. In MESH, delegate replay opens a fresh per-RPC backend connection (does not touch the shared pool).

### Metadata Merging and Topic Routing

The gateway merges metadata from all backend clusters into a single unified response. Brokers are concatenated with remapped virtual IDs, topics are concatenated (excluding internal topics with prefix `__` and topics with `errorCode != 0`), and partition leaders/replicas/ISR are remapped to virtual broker IDs. The controller is taken from the first cluster and remapped to a virtual ID. The cluster ID is a stable UUID generated from the virtual cluster cross ID.

Topics are indexed by both ID (primary) and name (fallback). Lookup prefers topic ID when present to avoid ambiguity on name reuse. On name collision across clusters, the first cluster by configuration order wins for the name index, but all topics are indexed by ID. Topic name collisions across backends in a Virtual Cluster mean two different backends with the same topic name will be collapsed to a single topic from the client's point of view; the gateway picks one owner.
