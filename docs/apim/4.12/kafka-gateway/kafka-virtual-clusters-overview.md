# Kafka Virtual Clusters Overview

## Overview

Kafka Virtual Clusters enable you to present multiple backend Kafka clusters as a single unified cluster to client applications. This capability allows you to distribute topics across multiple physical Kafka clusters while maintaining a single connection point for producers and consumers. Virtual clusters are designed for API platform administrators who need to scale beyond a single Kafka cluster or isolate workloads across multiple backend clusters without changing client configurations.

## Key Concepts

### Cluster Entities

The Gravitee Kafka Gateway manages three persistent entity types that work together to route Kafka traffic:

| Entity | Purpose | Configuration Scope |
|:-------|:--------|:-------------------|
| **Kafka Cluster** | Reusable connection profile to a real Kafka backend. Contains one or more named connections, each with bootstrap servers and security settings. | [Console → Kafka Clusters](create-and-configure-kafka-clusters.md) |
| **Kafka Virtual Cluster** | Fan-out wrapper that presents multiple backend Kafka clusters as one virtual cluster. References existing Kafka Cluster entities and their connections. | [Console → Kafka Virtual Clusters](creating-and-managing-kafka-virtual-cluster-entities.md) |
| **Kafka API** | Standard V4 API whose endpoint connector points at a raw bootstrap address, a Kafka Cluster entity, or a Kafka Virtual Cluster entity. | [Console → APIs](create-and-configure-kafka-apis/create-kafka-apis.md) |

Kafka Cluster and Virtual Cluster entities exist so the same backend configuration (bootstrap servers, SASL credentials, SSL trust material) can be shared across many APIs without duplication. Updating a Cluster entity propagates changes to every API that references it.

### Connections

A single Kafka Cluster entity can contain multiple connections. Each connection represents a distinct listener on the same backend cluster — for example, port 9091 with PLAINTEXT for internal traffic and port 9095 with SASL_SSL for partner integrations. Modeling them as siblings inside one Cluster entity lets you switch between authentication profiles per API without re-creating the entire cluster configuration.

### Virtual Cluster Backends

A Virtual Cluster backend is a reference pair consisting of a **Cluster Cross ID** (identifying a Kafka Cluster entity) and a **Connection Cross ID** (identifying one connection within that cluster). Each Virtual Cluster must reference at least two backends to enable cross-cluster fan-out. The practical ceiling is approximately 5–10 backends, as every consumer group RPC fans out across all configured backends.

### Cross IDs

Cross IDs are portable identifiers used for cross-environment references and configuration-as-code workflows. When you create a Kafka Cluster or Virtual Cluster, you can provide an explicit Cross ID or let the system auto-generate one from the entity name. Cross IDs are immutable after creation and must be unique within the environment.

### Lifecycle States

Clusters transition through three lifecycle states:

| State | Description | Badge |
|:------|:------------|:------|
| **UNDEPLOYED** | Cluster configuration exists but is not active on the gateway. | Neutral |
| **DEPLOYED** | Cluster is active and serving traffic. | Success |
| **PENDING** | Cluster configuration has been updated but not yet redeployed. | Warning |

Deploying a cluster increments its version number and sets the deployment timestamp. Clusters in DEPLOYED or PENDING state cannot be deleted until they are undeployed.

### Consumer Group Multiplexing

When a consumer group subscribes to topics that span multiple backend clusters, the gateway creates shadow groups on each backend cluster. Shadow group IDs follow the naming convention `{clientGroupId}__shadow-c{clusterIndex}`. When a client sets `group.instance.id` (static membership), each shadow receives `{clientInstanceId}__shadow-c{clusterIndex}`. The gateway aggregates responses from all shadow groups and presents a unified view to the client. Client group IDs matching the reserved pattern `__shadow-c\d+$` are rejected with `INVALID_GROUP_ID`.


The gateway supports both the classic consumer protocol and the [next-generation consumer protocol (KIP-848)](https://cwiki.apache.org/confluence/display/KAFKA/KIP-848%3A+The+Next+Generation+of+the+Consumer+Rebalance+Protocol), `group.protocol=consumer`.
 For KIP-848 groups, the gateway allocates a virtual member ID in the format `gw-<UUID>` during bootstrap and persists shadow memberships in the `ConsumerGroupMultiplexStore`. Steady-state heartbeats route via the virtual member ID fast path.

### Virtual Broker IDs

Each backend cluster is assigned a range of 10,000 virtual broker IDs. Cluster index 0 receives virtual IDs 10000–19999, cluster index 1 receives 20000–29999, and so on. Backend broker IDs must be less than 10,000. The maximum supported number of clusters is 214,748.

### Idempotent Producers

Idempotent producers (`enable.idempotence=true`) are supported on virtual clusters. When a producer sends `INIT_PRODUCER_ID`, the gateway fans out the request to every backend cluster. Each backend returns a real producer ID and epoch. The gateway synthesizes one virtual producer ID for the client and persists the mapping in the `ProducerIdSessionStore` (distributed cache). Every subsequent `PRODUCE` frame carries the virtual producer ID; the gateway rewrites it in place to the cluster-local real producer ID before forwarding.

If the gateway cannot find a session for a virtual producer ID (due to pod restart with local-only cache or cache eviction), it returns `PRODUCER_FENCED`. This is a fatal error for Kafka clients — the `TransactionManager` transitions to a fatal state and the producer cannot recover automatically. The application must create a new `KafkaProducer` instance, which runs a fresh `INIT_PRODUCER_ID` and rebuilds the session. Configuring a distributed cache (via `DistributedStoreFactory`) makes this fatal path negligible. The gateway uses `PRODUCER_FENCED` instead of `UNKNOWN_PRODUCER_ID` because Kafka clients only re-initialize their producer ID on epoch exhaustion, not on `UNKNOWN_PRODUCER_ID` alone.

### Topic Name Collisions

When two different backend clusters in a Virtual Cluster have topics with the same name, the gateway collapses them to a single topic from the client's point of view. The gateway picks one owner based on the first cluster in configuration order. Operators must keep topic namespaces disjoint per backend to avoid unintended collisions.

### Topic-Cluster Index

The gateway maintains a topic-cluster index that maps each topic to its owning backend cluster. Topics are indexed by ID (primary) and by name (fallback). On name collision across clusters, the first cluster by configuration order wins for the name index. The ID index stores every topic without collision. Topics with error codes other than `NONE` are skipped during merge. Topics with names starting with `__` (internal topics) are skipped during merge.

### Metadata Cache

The gateway caches merged metadata from all backend clusters. The cache operates in the following states:

| State | Request Type | Action |
|:------|:-------------|:-------|
| Cache empty | Any | Wait for initial population |
| Cache populated, all topics present | Metadata request | Serve from cache directly |
| Cache populated, `allowAutoTopicCreation=true`, topic missing | Metadata request | Forward to first reachable backend for auto-create, then refresh cache |
| Cache populated, auto-create disabled, topic missing | Metadata request | Force refresh before responding; fallback to stale snapshot on refresh failure |

### Virtual Epoch Management

When the gateway merges consumer group assignments from shadow groups, it applies the following rules to determine the virtual epoch:

| Condition | Action |
|:----------|:-------|
| Merged assignment unchanged (backend-internal churn only) | Keep virtual epoch |
| Any shadow assignment changes | Bump virtual epoch |
| Partition list reordering only | Keep virtual epoch (not a real delta) |
