# Consumer Group Routing: KIP-848 Protocol (Multiplexing)

## Overview

Consumer Group Routing with the KIP-848 protocol enables consumer groups using `group.protocol=consumer` to span multiple backend clusters in a Kafka Virtual Cluster. The gateway multiplexes consumer group operations across backends by creating shadow groups on each cluster and merging responses into a single virtual view for the client.

## Bootstrap Flow

When a consumer joins a group for the first time, the gateway performs the following steps:

1. Client sends `CONSUMER_GROUP_HEARTBEAT` with `memberId=''` (bootstrap request).
2. Gateway generates a synthetic `virtualMemberId` using the pattern `gw-<UUID>`.
3. Gateway splits the subscription by owning cluster based on topic metadata and sends a shadow heartbeat with `memberId=''` to each touched cluster.
4. Gateway captures the per-cluster `shadowMemberId` values returned by each backend.
5. Gateway persists a `ConsumerGroupMembership` record mapping the virtual member ID to the per-cluster shadow member IDs.
6. Gateway merges per-shadow responses and returns the merged result with the synthetic `virtualMemberId` to the client.

## Steady-State Flow

After bootstrap, the client sends heartbeats with the cached `virtualMemberId`. The gateway performs the following steps:

1. Client sends `CONSUMER_GROUP_HEARTBEAT` with the cached `virtualMemberId`.
2. Gateway resolves the membership record from the `ConsumerGroupMultiplexStore` using the virtual member ID.
3. Gateway splits the subscription by topic name and current assignment by topic ID per cluster.
4. Gateway fans out each shadow heartbeat with the cached `(shadowMemberId, shadowMemberEpoch)` pair for that cluster.
5. Gateway merges per-shadow responses and persists the updated membership record.
6. Gateway increments the `virtualMemberEpoch` whenever the union of per-shadow assignments changes.

## Leave Flow

When a consumer leaves the group, the gateway performs the following steps:

1. Client sends `CONSUMER_GROUP_HEARTBEAT` with `memberEpoch=-1` (graceful leave) or `memberEpoch=-2` (forced leave).
2. Gateway propagates the leave request to every shadow group with the same epoch value.
3. Gateway evicts the membership record locally regardless of per-shadow outcomes.
4. Gateway returns success to the client.

## Error Handling

### Stale Epoch

If the client sends a heartbeat with an out-of-date `memberEpoch`, the gateway rejects the request with `FENCED_MEMBER_EPOCH` and evicts the membership record. The client must re-bootstrap by sending a heartbeat with `memberId=''`.

### Per-Shadow Error Reduction

When merging responses from multiple shadow groups, the gateway applies the following priority chain to determine the final error code returned to the client:

1. `FENCED_MEMBER_EPOCH` (highest priority)
2. `UNKNOWN_MEMBER_ID`
3. `UNRELEASED_INSTANCE_ID`
4. Transient coordinator errors (`NOT_COORDINATOR`, `COORDINATOR_NOT_AVAILABLE`, `COORDINATOR_LOAD_IN_PROGRESS`)
5. Other errors (lowest priority)

Transport-level failures (connection refused, timeout) are stamped as `COORDINATOR_NOT_AVAILABLE` before entering the reduction chain.

## Static Membership

When the client provides a `groupInstanceId` in the heartbeat request, the gateway appends `__shadow-c<clusterIndex>` to create per-cluster shadow instance IDs.

**Example**: A static member with `groupInstanceId=worker-1` spanning 2 backends creates:
- `worker-1__shadow-c0` on backend 0
- `worker-1__shadow-c1` on backend 1

If the client does not provide a `groupInstanceId` (dynamic membership), the shadow instance IDs are also null.
