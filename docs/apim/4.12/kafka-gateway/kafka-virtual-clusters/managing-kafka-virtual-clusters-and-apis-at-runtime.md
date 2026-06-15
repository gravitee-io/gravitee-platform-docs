# Managing Kafka Virtual Clusters and APIs at Runtime

## Managing Clusters and APIs

### Deploying and Undeploying Clusters

Clusters must be deployed to the gateway before they can serve traffic. Deploying a cluster increments its version number and sets the deployment timestamp. Undeploying a cluster removes it from the gateway but preserves the configuration.

**To deploy a cluster:**

1. Navigate to [Console → Kafka Clusters](create-and-configure-kafka-clusters.md) (or [Kafka Virtual Clusters](creating-and-managing-kafka-virtual-cluster-entities.md)).
2. Open the cluster.
3. Click **Deploy**. The lifecycle state transitions to DEPLOYED.

**To undeploy a cluster:**

1. Navigate to Console → Kafka Clusters (or Kafka Virtual Clusters).
2. Open the cluster.
3. Click **Undeploy**. The lifecycle state transitions to UNDEPLOYED.

**To delete a cluster:**

1. Ensure the cluster is in UNDEPLOYED state. Clusters in DEPLOYED or PENDING state cannot be deleted.
2. Navigate to Console → Kafka Clusters (or Kafka Virtual Clusters).
3. Open the cluster.
4. Click **Delete**.

### Updating Cluster Configuration

When you update a deployed cluster's configuration, the lifecycle state transitions to PENDING. Redeploy the cluster to apply the changes to the gateway.

1. Navigate to Console → Kafka Clusters (or Kafka Virtual Clusters).
2. Open the cluster.
3. Navigate to the **Configuration** tab.
4. Make your changes (add, edit, or remove connections or backends).
5. Click **Save**. The lifecycle state transitions to PENDING.
6. Click **Deploy** to apply the changes. The lifecycle state transitions to DEPLOYED and the version number increments.

### Creating Topics on Virtual Clusters

When you create topics on a virtual cluster using `CreateTopics`, the gateway routes the request to the first configured backend (cluster index 0) in configuration order. If the first backend is unreachable (transport failure), the gateway falls back to the next backend in sequence. Only a structured Kafka response (even with per-topic errors like `TOPIC_ALREADY_EXISTS`) is treated as authoritative and stops the fallback chain.

After a successful `CreateTopics` operation, the gateway refreshes its merged metadata cache so the new topic immediately resolves to the correct cluster for follow-up operations. Affinity-based routing (prefix or regex patterns to select a specific backend) is not yet implemented. The gateway cannot pick the hosting backend for new topics from the client side — the first reachable backend wins.

### Adding Partitions to Topics

`CreatePartitions` requests are resolved per-topic via the topic-cluster index and sent to the owning backend. If the topic is not found in the index, the gateway triggers a single metadata refresh and retries. Topics still unknown after the refresh surface as `UNKNOWN_TOPIC_OR_PARTITION`.

### Deleting Topics

`DeleteTopics` requests use per-topic routing. A batch spanning topics on different backends is split, fanned out to the appropriate backends, and re-merged into one client response.

### Managing Consumer Groups

#### Listing Consumer Groups

`ListGroups` requests fan out across all backends. The gateway returns the union of group IDs with shadow suffixes stripped. For example, `mygroup__shadow-c0` and `mygroup__shadow-c1` collapse back to `mygroup`. The client sees one logical group per consumer group, regardless of how many backends host it.

#### Describing Consumer Groups

`DescribeGroups` (classic protocol) and `ConsumerGroupDescribe` (KIP-848) requests fan out per-cluster and merge per-cluster results. The client sees one virtual group with members from every backend.

#### Deleting Consumer Groups

`DeleteGroups` requests are split per-cluster and fanned out. Results are merged into one client response.

#### Deleting Consumer Group Offsets

`OffsetDelete` requests are split per-topic (based on the topic-cluster index) and fanned out. Results are merged into one client response.

### Committing and Fetching Offsets

The gateway routes `OFFSET_COMMIT` and `OFFSET_FETCH` requests using the following logic:

**For v8+ multi-group `OFFSET_FETCH` requests** (where `data.groups[]` is populated):

1. The gateway refuses any group ID matching the reserved `__shadow-c<N>` suffix pattern.
2. If the request requires multiplexing (determined by `offsetFetchNeedsMultiplex`), the gateway routes through the multiplex path.
3. Otherwise, the gateway forwards the request to the connection's backend cluster.

**For single-group `OFFSET_COMMIT` and `OFFSET_FETCH` requests**:

1. The gateway refuses reserved group IDs.
2. The gateway attempts the multiplex path:
   - **OFFSET_COMMIT**: Multiplex when topics span multiple clusters AND (if `memberId` is non-empty) the member has a multiplex membership.
   - **OFFSET_FETCH**: Multiplex when the explicit topic list spans multiple clusters OR (for "all topics" form where `topics == null`) the group is multiplexed (has a group→clusters index entry written at `JoinGroup` time).
3. If multiplex does not apply:
   - The gateway consults the `GroupClusterRouter` cache.
   - If the cache misses, the gateway falls back to topic-hint routing.
   - If the resolved cluster does not match the client's bound cluster, the gateway emits `NOT_COORDINATOR`.

**Offset routing for topics unknown to the topic-cluster index**: The gateway stamps `UNKNOWN_TOPIC_OR_PARTITION` on every partition for that topic.

**Offset routing for topics on clusters outside the membership**: The gateway stamps `UNKNOWN_TOPIC_OR_PARTITION` (member path) or skips fan-out (admin path).

**Offset routing when member ID is provided but no membership exists in the store**: The gateway replies `UNKNOWN_MEMBER_ID` on every partition without a backend round-trip.

**Offset routing when generation ID mismatches**: The gateway replies `ILLEGAL_GENERATION` on every partition.

**OFFSET_FETCH v0–v7 with `topics=null`**: The gateway replies with an empty topics list. Fetch-all is unsupported because the gateway does not maintain a group→clusters index for offset fetch operations.

**OFFSET_FETCH v8+ multi-group with `topics=null`**: The gateway replies with an empty topics list per group.

### Finding Coordinators

The gateway routes `FindCoordinator` requests based on the coordinator type:

| Coordinator Type | Routing Strategy |
|:-----------------|:-----------------|
| `GROUP` | Probe via `MultiClusterDescribeGroupsHandler` + cache |
| `SHARE` | Probe via `MultiClusterDescribeGroupsHandler` + cache |
| `TRANSACTION` | Deterministic hash (transactions are single-cluster per virtual cluster constraints) |

**Probe result**:
- `OptionalInt.of(clusterIndex)` when at least one backend reports the group as alive (any state other than `Dead`).
- `OptionalInt.empty()` when every backend denies knowledge, returns a non-retriable error, or fails to respond. The gateway falls back to deterministic hash.

**Retriable errors during probe**:
- `COORDINATOR_LOAD_IN_PROGRESS`
- `COORDINATOR_NOT_AVAILABLE`
- `NOT_COORDINATOR`

**Retry configuration**: Default max retries: 3. Default retry backoff: 300ms.

### Shadow Coordinator Warm-Up

Before fanning a cross-cluster group request (`JoinGroup`, `ConsumerGroupHeartbeat`), the gateway sends `FIND_COORDINATOR` (v4) to each shadow group's backend to pre-load the `__consumer_offsets` partition. The gateway retries up to 5 times with 50ms backoff on transient coordinator errors (`COORDINATOR_LOAD_IN_PROGRESS`, `COORDINATOR_NOT_AVAILABLE`, `NOT_COORDINATOR`). Failures are logged but do not block the subsequent group request.

### Consumer Group Membership Lifecycle

The gateway manages consumer group memberships across shadow groups using the following rules:

| Event | Action |
|:------|:-------|
| **JoinGroup success (all shadows)** | Store `MultiplexMembership` keyed by `(apiId, clientGroupId, clientMemberId)` with `clientGenerationId = sum(shadowGenerationIds)` |
| **JoinGroup partial failure** | Issue best-effort `LeaveGroup` to accepted shadows; do NOT persist membership |
| **Heartbeat: `UNKNOWN_MEMBER_ID` or `ILLEGAL_GENERATION` from any shadow** | Evict membership from store; surface error to client |
| **Heartbeat: `REBALANCE_IN_PROGRESS` from any shadow** | Surface error to client; keep membership (re-Join rebuilds it) |
| **SyncGroup: `UNKNOWN_MEMBER_ID` or `ILLEGAL_GENERATION` from any shadow** | Evict membership; surface error |
| **SyncGroup: `REBALANCE_IN_PROGRESS` from any shadow** | Surface error; keep membership |
| **LeaveGroup** | Evict membership after fan-out completes (even if a shadow errors) |

### Error Priority for Heartbeat and SyncGroup

When the gateway receives errors from multiple shadow groups during `Heartbeat` or `SyncGroup` operations, it reduces them in the following priority order (highest to lowest):

1. `REBALANCE_IN_PROGRESS`
2. `UNKNOWN_MEMBER_ID` / `ILLEGAL_GENERATION`
3. Other errors (e.g., `NOT_COORDINATOR`, `COORDINATOR_NOT_AVAILABLE`)

### Generation ID Aggregation

The gateway aggregates generation IDs from shadow groups using the following rules:

| Scenario | Merged `clientGenerationId` |
|:---------|:----------------------------|
| Sum of shadow generations exceeds previous | `sum(shadowGenerationIds)` |
| Sum does not exceed previous (e.g., broker restart) | `previousClientGenerationId + 1` |
| Sum saturates at `Integer.MAX_VALUE` and previous is also `MAX_VALUE` | Wrap to `1` |

### SyncGroup Assignment Decomposition

The gateway decomposes client assignments into per-cluster shadow assignments using the following rules:

| Rule | Description |
|:-----|:------------|
| **Partition routing** | Each `(topic, partition)` in the client's assignment is routed to the shadow on the cluster that owns the topic (via the topic-cluster index) |
| **Unknown topic partitions** | Silently dropped (not forwarded to any shadow) |
| **userData forwarding** | Forwarded verbatim to every shadow; per-cluster assignors ignore entries for topics outside their subscription |
| **ownedPartitions filtering** | Filtered per cluster: each shadow receives only the owned partitions whose topic belongs to that cluster |
| **Assignment touching cluster outside membership** | Reply `REBALANCE_IN_PROGRESS` before fan-out; client re-Joins to rebuild membership |

### Managing Configurations

`DescribeConfigs`, `AlterConfigs`, and `IncrementalAlterConfigs` requests use the following routing rules:

| Resource Type | Routing Rule |
|:--------------|:-------------|
| `TOPIC` | Owning backend via topic-cluster index; refresh-on-miss |
| `BROKER` / `BROKER_LOGGER` | Virtual broker ID → cluster index via `VirtualBrokerIdMapper`; `resourceName` rewritten virtual→real on send, real→virtual on response |
| Other types (`CLIENT_METRICS`, `GROUP`, `UNKNOWN`) | Backend index 0 |
| Empty broker name | Backend index 0 |

Unparseable or unmapped broker IDs fail with `Errors.INVALID_REQUEST`.

### Kafka Topic Mapping Policy

The Kafka Topic Mapping policy (`gravitee-policy-kafka-topic-mapping`) is available as a separate plugin. It allows you to rewrite client-side topic names into broker-side topic names at the gateway level. The mapping is bidirectional — produce and consume operations both translate, and the gateway rewrites `listConsumerGroupOffsets` responses so the client sees its own names.

### Management API

#### Deploy Cluster

```
POST /clusters/{clusterId}/_deploy
```

Deploys the cluster to the gateway. Sets `lifecycleState` to DEPLOYED, increments the version number, and sets the deployment timestamp.

**Response:** `200 OK` with the updated Cluster object.

#### Undeploy Cluster

```
POST /clusters/{clusterId}/_undeploy
```

Undeploys the cluster from the gateway. Sets `lifecycleState` to UNDEPLOYED and sets the deployment timestamp.

**Response:** `200 OK` with the updated Cluster object.
