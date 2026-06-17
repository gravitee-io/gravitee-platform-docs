# Kafka Virtual Clusters Overview

## Overview

Kafka Virtual Clusters enable you to present multiple independent Kafka backends as a single unified cluster to client applications. This capability allows you to distribute topics across separate Kafka clusters while maintaining a single client connection point, simplifying multi-cluster architectures and enabling cross-cluster consumer groups without client-side coordination.

## Key Concepts

### Kafka Cluster

A reusable connection profile to a real Kafka backend. Each Kafka Cluster entity stores one or more named connections, each with bootstrap servers and security configuration (PLAINTEXT, SSL, SASL_PLAINTEXT, or SASL_SSL). Multiple APIs can reference the same Kafka Cluster entity, allowing centralized configuration management — updates to the cluster propagate automatically to all referencing APIs.

**Connection Properties:**

| Property | Description | Example |
|:---------|:------------|:--------|
| Name | Identifier for this connection within the cluster | `eu-prod-internal` |
| Cross ID | Portable identifier for cross-environment references (auto-generated from name if not provided) | `eu-prod-internal` |
| Bootstrap Servers | Comma-separated list of broker addresses | `kafka1.example.com:9092,kafka2.example.com:9092` |
| Security Protocol | Connection security mode | `SASL_SSL` |

A single backend often exposes multiple listeners — for example, port 9091 PLAINTEXT for internal traffic and port 9095 SASL_SSL for external partners. Modeling them as sibling connections within one Kafka Cluster entity lets you switch between authentication profiles per API without re-creating the entire cluster configuration. Connection names within a Kafka Cluster must be unique; duplicate names will trigger a validation error. The connections array can be empty (minimum 0 items allowed).

### Kafka Virtual Cluster (MESH)

A fan-out wrapper that presents N backend Kafka clusters as one virtual cluster to clients. Each virtual cluster stores a list of backend references — pairs of `(clusterCrossId, connectionCrossId)` that select one connection from each underlying Kafka Cluster entity. Virtual clusters require at least two backend clusters to provide value; with a single backend, use a direct Kafka Cluster reference instead.

**Backend Reference Properties:**

| Property | Description |
|:---------|:------------|
| Cluster Cross ID | The cross ID of the referenced Kafka Cluster entity |
| Connection Cross ID | The cross ID of the connection within that cluster |

The gateway fans out metadata requests across all backends, merges topic lists, and remaps broker IDs into non-overlapping virtual ranges. Consumer group operations are routed based on topic subscription — single-cluster subscriptions forward directly to the owning backend, while cross-cluster subscriptions create shadow groups on each backend and synthesize a unified client-facing membership. Topics with names starting with `__` (internal topics) are skipped during metadata merge. Topics with `errorCode != NONE` are also skipped. On name collision during metadata merge, the first cluster wins in the merged response, but all clusters are indexed by topic ID. The controller ID in merged metadata is set from the first cluster with a valid controller ID. The cluster ID in merged metadata is generated as a UUID from the virtual cluster cross ID.

Topic name collisions across backends in a Virtual Cluster will be collapsed to a single topic from the client's point of view — the gateway picks one owner. Operators must keep topic namespaces disjoint per backend to avoid ambiguity.

### Cluster Lifecycle States

| State | Description |
|:------|:------------|
| `UNDEPLOYED` | Cluster configuration exists but is not active on the gateway |
| `DEPLOYED` | Cluster is active and serving traffic |
| `PENDING` | Cluster configuration has been updated but not yet deployed |

Each deployment increments the cluster's version number and updates the `deployedAt` timestamp.

### Virtual Broker ID Mapping

Each backend cluster in a virtual cluster is assigned a range of 10,000 broker IDs. Cluster index 0 receives virtual IDs 10000–19999, cluster index 1 receives 20000–29999, and so on. Backend broker IDs must be less than 10,000. The maximum number of clusters supported in a single virtual cluster is 214,748. All broker IDs (leader, replicas, ISR, offline) are remapped to virtual IDs during metadata merge.

### Cross-Cluster Consumer Groups

When a consumer subscribes to topics spanning multiple backend clusters in a virtual cluster, the gateway creates shadow groups on each backend (named `<groupId>__shadow-c<N>`) and synthesizes a single client-facing member ID and generation ID. The gateway fans out heartbeats, offset commits, and offset fetches to the appropriate shadow groups based on the cached membership.

**Protocol support:**

| Protocol | Multiplexed Support | Notes |
|:---------|:-------------------|:------|
| Classic (`JoinGroup` / `SyncGroup`) | ✅ Supported | Single-cluster and cross-cluster subscriptions |
| Next-gen (`CONSUMER_GROUP_HEARTBEAT`, `group.protocol=consumer`) | ✅ Supported | KIP-848 protocol with virtual epoch management |
| Cooperative-sticky assignor | ❌ Refused | Returns `INCONSISTENT_GROUP_PROTOCOL` — sticky state cannot be coordinated across shadow groups |

Consumer group IDs matching `.*__shadow-c\d+` are reserved for gateway multiplex internals and will be rejected with `INVALID_GROUP_ID` and the error message `"group id '<groupId>' uses the reserved gateway suffix '__shadow-c<N>'"`. Client group IDs containing the `__shadow-c` substring without a trailing digit are forwarded normally (not reserved).

JoinGroup subscriptions spanning multiple clusters are refused with `INVALID_REQUEST` and the error message `"Cross-cluster subscription is not supported in MESH mode (group '{groupId}' subscribes to topics that span clusters {clusters}). Split the subscription into per-cluster groups, mirror the topics, or use single-cluster routing."` Single-cluster subscriptions forward directly to the backend without multiplex.

Any shadow returning `UNKNOWN_MEMBER_ID` or `ILLEGAL_GENERATION` removes the membership from the store. Shadows returning `REBALANCE_IN_PROGRESS` keep the membership in the store (client re-Joins). LeaveGroup completes (success or error) evict the membership from the store.

If the sum of shadow generations is less than or equal to the previous client generation, the gateway bumps the generation to `previous + 1` to maintain monotonicity. If the sum exceeds `Integer.MAX_VALUE`, the gateway saturates at `Integer.MAX_VALUE`. If the previous generation is `Integer.MAX_VALUE` and the sum does not exceed it, the gateway wraps to `1`.

If shadows negotiate different protocol names (e.g., `"range"` vs `"roundrobin"`), the gateway replies with `INCONSISTENT_GROUP_PROTOCOL` and releases all shadows.

If one shadow fails and others succeed, the gateway replies with `NOT_COORDINATOR` and performs a best-effort LeaveGroup on successful shadows.

If a SyncGroup assignment references a topic on a cluster outside the membership, the gateway replies with `REBALANCE_IN_PROGRESS`.

Static membership (`group.instance.id`) on MESH KIP-848 is supported via per-shadow instance ID generation.

### Consumer Group Membership Schema

Per-client membership in a multiplexed consumer group using the next-gen protocol (`group.protocol=consumer`).

**Fields:**

| Field | Type | Description |
|:------|:-----|:------------|
| `virtualMemberId` | `String` | Gateway-allocated member ID (prefix: `"gw-"`) |
| `virtualMemberEpoch` | `int` | Gateway-managed epoch, bumped when merged assignment changes |
| `shadowsByCluster` | `Map<Integer, ShadowBinding>` | Per-cluster shadow bindings (cluster index → shadow state) |

**ShadowBinding Fields:**

| Field | Type | Description |
|:------|:-----|:------------|
| `shadowMemberId` | `String` | Backend-assigned member ID for this shadow |
| `shadowMemberEpoch` | `int` | Backend's last-returned member epoch |
| `assignment` | `Map<Uuid, List<Integer>>` | Per-shadow assignment (topic ID → partition list) |

The virtual member epoch field (`virtualMemberEpoch`) is incremented only when the union of per-shadow assignments changes. If merged assignments are equal, the epoch is preserved.

Per-shadow errors are reduced to a single client-facing code by priority: `FENCED_MEMBER_EPOCH` > `UNKNOWN_MEMBER_ID` > `UNRELEASED_INSTANCE_ID` > transient coordinator errors (`NOT_COORDINATOR`, `COORDINATOR_NOT_AVAILABLE`, `COORDINATOR_LOAD_IN_PROGRESS`) > other errors. Returns `null` when every shadow reported `NONE`.

### SASL Delegate-to-Broker

The `DELEGATE_TO_BROKER` SASL mechanism forwards the client's SASL exchange directly to the backend broker without gateway-side credential validation. This mode is useful when the backend requires custom SASL mechanisms or when you want the gateway to remain credential-agnostic. In MESH mode, delegate replay opens a fresh per-RPC backend connection and does not touch the shared pool.

### Gateway-to-Broker Authentication Modes

Gateway-to-broker authentication has two modes:

- **Gateway-managed:** The gateway holds SASL/SSL credentials in the Cluster entity and authenticates to the backend on behalf of the client.
- **Delegate:** Pass-through SASL where client credentials are forwarded to the broker without gateway-side validation.

### Idempotent Producer Support

Virtual clusters support idempotent producers by maintaining a session store that maps virtual producer IDs to per-cluster backend producer IDs. When a client initializes an idempotent producer, the gateway fans out `INIT_PRODUCER_ID` requests to all backends, caches the mappings, and rewrites producer IDs in `PRODUCE` requests on a per-batch basis. If a virtual producer ID session is missing or lacks a mapping for the target cluster, the gateway returns `PRODUCER_FENCED` with the error message `"No producer id session for api={apiId} virtualPid={virtualPid} cluster={clusterIndex}, replying with PRODUCER_FENCED"`, forcing the client to create a new `KafkaProducer` instance.

### Transactional Producer Support

Kafka transactions (`INIT_PRODUCER_ID` with `transactional.id`, `ADD_PARTITIONS_TO_TXN`, `END_TXN`, `TXN_OFFSET_COMMIT`, `ADD_OFFSETS_TO_TXN`, `WRITE_TXN_MARKERS`) are not supported on MESH virtual clusters. Transactional APIs have no multiplex handler and would fall through to whichever backend the broker-connect session is bound to, resulting in undefined behavior.

### ACL Operations

All ACL CRUD operations (`DESCRIBE_ACLS`, `CREATE_ACLS`, `DELETE_ACLS`) on a MESH virtual cluster are refused with `SECURITY_DISABLED` and the error message `"MESH virtual cluster does not multiplex ACL operations; manage ACLs directly on each backend cluster."` A MESH virtual cluster fronts N independent Kafka backends, each with its own authorizer store — forwarding ACL operations to a single backend would leave the others divergent.

### Supported API Keys in MESH Mode

The gateway strips unsupported API keys from the intersected `ApiVersionsResponse` before caching/returning to clients:

| API Key | Name | Status | Notes |
|:--------|:-----|:-------|:------|
| 78 | `SHARE_GROUP_HEARTBEAT` | **Removed** | KIP-932; not supported by multiplex layer |
| 68 | `CONSUMER_GROUP_HEARTBEAT` | **Advertised** | KIP-848; supported via `MultiplexConsumerGroupHeartbeatHandler` |
| 69 | `CONSUMER_GROUP_DESCRIBE` | **Advertised** | KIP-848; supported via `ConsumerGroupDescribeRouter` |

### Topic Cluster Index Lookup

Topics are indexed by both UUID and name. The ID index is primary; the name index is fallback. On name collision, the first cluster by configuration order wins for the name index. The ID index stores every topic (no collision possible). Topic must have at least an ID or a name (validation enforced in `Topic` record constructor).

**Lookup Priority:**
1. If topic has valid ID → use ID index
2. If ID lookup fails or ID is absent → use name index
3. If both fail → return empty

### Topic Mapping Policy

The Kafka Topic Mapping policy (`gravitee-policy-kafka-topic-mapping`) is available as a separate plugin to rewrite client-side topic names into broker-side topic names bidirectionally.

### Mixed Plan Security Restriction

Mixed Keyless + secure plans on one API causes the API to fail at start with `KafkaServerUnsupportedSecureAndUnsecurePlansException`.

## Prerequisites

- **Cluster management permission:** Cluster management is hidden from basic users by default. Grant the `CLUSTER` environment-scoped permission (READ + UPDATE) to users who need to create or edit Kafka Cluster and Virtual Cluster entities. Navigate to **Organization → Roles → USER** and check the `CLUSTER` row.
- **Native API log and analytics permissions:** Grant `NATIVE_LOG` and `NATIVE_ANALYTICS` API-scoped permissions to roles that need to read native Kafka API logs and analytics. The built-in `OWNER` and `PRIMARY_OWNER` roles receive these permissions automatically via an upgrader; custom roles require manual grants.
- **Default Kafka domain (HOST routing mode):** If using HOST routing mode (the default), configure the `gravitee_kafka_routingHostMode_defaultDomain` property so each API's host prefix maps to `<prefix>.<defaultDomain>:9092`. Set this via **Console → Organization → Entrypoints & Sharding Tags → Default Kafka Domain**.
- **Wildcard certificate (HOST routing mode):** HOST routing mode requires a wildcard certificate covering `*.<defaultDomain>` to support SNI-based routing. PORT routing mode does not require a wildcard certificate.
- **Minimum two Kafka Cluster entities (for virtual clusters):** A Kafka Virtual Cluster requires at least two Kafka Cluster entities to provide value. With a single backend, use a direct Kafka Cluster reference instead.
