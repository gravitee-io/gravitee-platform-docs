# Consumer Group Routing in Kafka Virtual Clusters

## Consumer Group Routing

### Single-Cluster Consumer Groups

When a consumer group subscribes to topics that all reside on the same backend cluster, the gateway routes all group RPCs (JoinGroup, Heartbeat, SyncGroup, LeaveGroup, OffsetCommit, OffsetFetch) to that cluster. The gateway caches the group-to-cluster mapping after the first JoinGroup or ConsumerGroupHeartbeat request and uses the cache for subsequent requests.

If the cache indicates a different cluster than the one the client is connected to, the gateway returns a synthetic `NOT_COORDINATOR` error with the message:

```
"group '{groupId}' lives on a different backend cluster"
```

The client issues a FindCoordinator request, which the gateway routes to the correct cluster based on the cache.

LeaveGroup is forwarded without invalidating the cache. Other members of the same group still rely on the cached mapping, and a backend-side failure would otherwise drop routing information for a still-active group. The cache TTL evicts stale entries once the group is truly gone.

### Cross-Cluster Consumer Groups (Classic Protocol)

When a consumer group subscribes to topics that span multiple backend clusters, the gateway creates shadow consumer groups on each backend. Shadow groups are named `<groupId>__shadow-c<N>`, where `N` is the cluster index. The gateway fans out JoinGroup, Heartbeat, SyncGroup, and LeaveGroup requests to all shadow groups and merges their responses.

Cross-cluster subscriptions are supported only with the **range** or **round-robin** assignors. Subscriptions using the **cooperative-sticky** assignor are refused with `INCONSISTENT_GROUP_PROTOCOL` error and the message:

```
"Cross-cluster subscription is not supported with cooperative-sticky assignor"
```

OffsetCommit and OffsetFetch requests are routed per-partition based on topic ownership. The gateway splits the request into per-cluster sub-requests, forwards them to the appropriate backends, and merges the responses.

OFFSET_FETCH v0–v7 with `topics=null` (request for all topics) replies empty because no group-to-clusters index is available. OFFSET_FETCH v8+ multi-group requests run per-cluster decomposition once per requested group. OFFSET_FETCH v8+ multi-group requests are refused if any groupId collides with the reserved shadow suffix.

### Cross-Cluster Consumer Groups (Next-Generation Protocol)

When a consumer group uses the next-generation consumer protocol (KIP-848) and subscribes to topics that span multiple backend clusters, the gateway refuses the subscription with `INVALID_REQUEST` error and the message:

```
"Cross-cluster subscription is not supported in MESH mode (group '{groupId}' subscribes to topics that span clusters {clusters}). Split the subscription into per-cluster groups, mirror the topics, or use single-cluster routing."
```

Static membership (`group.instance.id`) on MESH KIP-848 is supported via `ShadowNamer.instanceId(client, clusterIndex)`.

Error priority for ConsumerGroupHeartbeat follows this chain:

```
FENCED_MEMBER_EPOCH > UNKNOWN_MEMBER_ID > UNRELEASED_INSTANCE_ID > 
coordinator-transient (NOT_COORDINATOR / COORDINATOR_NOT_AVAILABLE / COORDINATOR_LOAD_IN_PROGRESS) > 
other
```

The gateway returns `null` when every shadow reported `Errors.NONE`.

Virtual epoch bump rule: `virtualMemberEpoch` is bumped whenever the union of per-shadow assignments changes. Per-backend epoch churn unrelated to the merged view never reaches the client.

### Reserved Group ID Pattern

Consumer group IDs matching the pattern `.*__shadow-c\d+` are reserved for gateway multiplex internals. Requests using reserved group IDs are rejected with `INVALID_GROUP_ID` error and the message:

```
"group id '<groupId>' uses the reserved gateway suffix '__shadow-c<N>'"
```

### FindCoordinator Routing

For `GROUP` and `SHARE` key types, the gateway probes all backend clusters via DescribeGroups and caches the result. If at least one backend reports the group as alive (any state other than `Dead`), the gateway routes to that cluster. If multiple backends report the group, the first cluster in configuration order wins (with a warning logged).

If every backend denies knowledge of the group or fails to respond, the gateway falls back to deterministic hash routing.

For `TRANSACTION` key types, the gateway uses deterministic hash routing (transactions are single-cluster per MESH constraints).

Transient coordinator errors (`COORDINATOR_LOAD_IN_PROGRESS`, `COORDINATOR_NOT_AVAILABLE`, `NOT_COORDINATOR`) are retried up to 3 times with 300ms backoff.
