# Consumer Group Routing: Classic Protocol (Pre-KIP-848)

## Coordinator Discovery

When a client sends `FIND_COORDINATOR` for a consumer group, the gateway probes all backend clusters to determine which cluster hosts the group:

1. The gateway sends `DESCRIBE_GROUPS` to every backend cluster.
2. The first cluster that reports the group as alive wins — the gateway returns that cluster's coordinator address to the client.
3. If no cluster reports the group as alive, the gateway falls back to deterministic hash routing: `hash % clusterCount` selects the target cluster.
4. If all backends are unreachable, the gateway hashes across all configured backends (including unreachable ones) to maintain consistent routing.

## Cross-Cluster Subscription Rejection

If a consumer group's subscription spans topics hosted on multiple backend clusters, the gateway rejects the `JOIN_GROUP` request with `INVALID_REQUEST` and the following error message:

```
Cross-cluster subscription is not supported in MESH mode (group '{groupId}' subscribes to topics that span clusters {clusters}). Split the subscription into per-cluster groups, mirror the topics, or use single-cluster routing.
```

The gateway enforces single-cluster membership to prevent split-brain scenarios where different members of the same group operate on different backends.

## Offset Operations

### OFFSET_COMMIT and OFFSET_FETCH with memberId

When a consumer commits or fetches offsets with a non-empty `memberId`, the gateway decomposes the request by cluster:

1. The gateway identifies which backend cluster hosts each topic in the request.
2. For each cluster, the gateway creates a shadow member ID and forwards the request to that cluster.
3. Partitions for unknown topics are stamped with `UNKNOWN_TOPIC_OR_PARTITION` in the response.
4. Admin tools (empty `memberId`) bypass multiplex and are forwarded to the cluster determined by coordinator discovery.

### OFFSET_FETCH with topics=null

For `OFFSET_FETCH` requests with `topics=null` (v0–v7 all-topics form) or v8+ requests where `group.topics() == null`:

1. The gateway fans out the request to every cluster the group spans, using the group→clusters reverse index.
2. Groups that were never multiplexed (single-cluster groups) receive an empty reply.
3. The gateway merges per-cluster responses into a single client response.

## Classic Protocol Multiplexing

{% hint style="info" %}
Classic protocol multiplexing support status is pending verification. The following section documents the multiplexing behavior if supported.
{% endhint %}

If classic protocol multiplexing is supported, the gateway maintains shadow groups on each backend cluster to enable cross-cluster consumer group operation.

### Shadow Group Naming

The gateway creates one shadow group per backend cluster using the naming convention:

```xml
<clientGroupId>__shadow-c<clusterIndex>
```

For example, a client group `analytics` spanning two clusters becomes:
- `analytics__shadow-c0` on cluster 0
- `analytics__shadow-c1` on cluster 1

### Membership Lifecycle

| Event | Client State | Gateway Action | Backend State |
|:------|:-------------|:---------------|:--------------|
| JOIN_GROUP (first call) | No memberId | Allocate virtual memberId, create shadow groups on all clusters, forward JOIN_GROUP to each cluster with shadow memberId | Each cluster assigns shadow memberId |
| Re-join with known memberId | Has memberId | Look up shadow memberId mapping, forward to each cluster | Each cluster recognizes shadow memberId |
| Re-join with unknown memberId | Has memberId but gateway lost mapping | Treat as first join, reallocate virtual memberId | Each cluster assigns new shadow memberId |
| LEAVE_GROUP | Has memberId | Forward LEAVE_GROUP to each cluster with shadow memberId | Each cluster removes shadow member |
| HEARTBEAT error | Has memberId | Merge error responses from all clusters, return highest-priority error to client | Each cluster tracks shadow member liveness |

### Generation ID Synthesis

The gateway synthesizes a single generation ID for the client by summing the `generationId` values from all shadow groups:

```
virtualGenerationId = sum(shadowGenerationId[0], shadowGenerationId[1], ..., shadowGenerationId[N])
```

If any shadow group returns an error, the gateway falls back to incrementing the previous virtual generation ID. The virtual generation ID wraps at `Integer.MAX_VALUE`.

### Protocol Negotiation

All shadow groups must agree on the same `protocolName` (e.g., `range`, `roundrobin`). If shadow groups report different protocols, the gateway returns `INCONSISTENT_GROUP_PROTOCOL` to the client.

### Error Priority for HEARTBEAT and SYNC_GROUP

When merging error responses from multiple shadow groups, the gateway applies the following priority order (highest to lowest):

1. `REBALANCE_IN_PROGRESS`
2. `UNKNOWN_MEMBER_ID` or `ILLEGAL_GENERATION`
3. Other errors

The gateway returns the highest-priority error to the client.

### Partial Failure Handling for JOIN_GROUP

| Scenario | Gateway Behavior |
|:---------|:-----------------|
| All clusters return success | Merge assignments, return success to client |
| One or more clusters return non-success (excluding `MEMBER_ID_REQUIRED`) | Return first non-success error to client |
| All clusters return `MEMBER_ID_REQUIRED` | Return `MEMBER_ID_REQUIRED` to client |
| Mixed success and `MEMBER_ID_REQUIRED` | Retry with member IDs from successful clusters |
| Any cluster returns `INCONSISTENT_GROUP_PROTOCOL` | Return `INCONSISTENT_GROUP_PROTOCOL` to client |

### Subscription Scoping

The gateway filters each shadow group's subscription to include only topics hosted on that cluster:

1. For each shadow group, the gateway extracts the subset of `topics` and `ownedPartitions` that belong to that cluster.
2. The gateway forwards the filtered subscription to the shadow group.
3. The gateway forwards `userData` verbatim to all shadow groups without modification.

### SyncGroup Assignment Decomposition

When the leader sends `SYNC_GROUP` with assignments:

1. The gateway decomposes the assignment by cluster, routing each member's partitions to the appropriate shadow group.
2. If the assignment includes partitions from a cluster where the member has no shadow membership, the gateway returns `REBALANCE_IN_PROGRESS`.
3. The gateway skips assignment entries for unknown member IDs.
4. The gateway picks the first non-empty `Assignment.userData` from any shadow group and returns it to the client.

### Cooperative-Sticky Assignor Restriction

The gateway refuses consumer groups using the `cooperative-sticky` assignor with `INCONSISTENT_GROUP_PROTOCOL`.

**Rationale**: The cooperative-sticky assignor stores sticky state in the per-member `Subscription.userData` field. This state breaks across shadow groups because each shadow group sees only a subset of the client's subscription. Multiplexing cooperative-sticky would require the gateway to parse and rewrite the sticky state, which is not supported.
