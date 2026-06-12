
# Consumer Group Routing: KIP-848 Protocol (Multiplexing)

KIP-848 introduces the consumer group protocol, enabling clients to join groups and coordinate partition assignments across Kafka clusters. When a consumer group subscription spans multiple backend clusters, the gateway multiplexes group operations by creating shadow groups on each backend and synthesizing unified responses to the client.

## Classic Protocol Multiplexing


Consumer groups using the classic protocol can be multiplexed across backends when the subscription spans multiple clusters.
 The gateway creates one shadow group per backend cluster, each named `<clientGroupId>__shadow-c<clusterIndex>`.

#### Membership Lifecycle

The gateway manages membership state across shadow groups according to the following rules:

| Event | Action |
|:------|:-------|
| `JOIN_GROUP` (first call) | Mint synthetic `clientMemberId = "gw-" + UUID`, persist mapping to shadow member IDs. |
| `JOIN_GROUP` (re-join with known memberId) | Reuse existing `clientMemberId` and per-shadow `shadowMemberId` from store. |
| `JOIN_GROUP` (re-join with unknown memberId) | Mint new synthetic `clientMemberId`. |
| `LEAVE_GROUP` | Evict membership from store after fan-out completes, regardless of shadow errors. |
| `HEARTBEAT` (`UNKNOWN_MEMBER_ID` or `ILLEGAL_GENERATION` from any shadow) | Evict membership from store. |

#### Generation ID Synthesis

The gateway synthesizes a `clientGenerationId` by summing per-shadow `generationId` values. If the sum fits in int32 and exceeds the previous generation, the sum is used. Otherwise, the gateway increments the previous generation by 1. If the previous generation is `Integer.MAX_VALUE`, the gateway wraps to `1`.

#### Protocol Negotiation

If all shadows agree on `protocolName`, the merged response carries that protocol. If shadows return different `protocolName` values, the gateway returns `INCONSISTENT_GROUP_PROTOCOL` and sends best-effort `LEAVE_GROUP` to accepted shadows.

#### Error Priority

For `HEARTBEAT` and `SYNC_GROUP` responses, the gateway applies the following error priority:

1. `REBALANCE_IN_PROGRESS`
2. `UNKNOWN_MEMBER_ID` / `ILLEGAL_GENERATION`
3. Other errors (first non-success in result order)

#### Partial Failure Handling

For `JOIN_GROUP` requests, the gateway handles partial failures as follows:

| Condition | Action |
|:----------|:-------|
| Any shadow returns non-success (excluding `MEMBER_ID_REQUIRED`) | Best-effort `LEAVE_GROUP` to successful shadows, reply `NOT_COORDINATOR` to client. |
| All shadows return `MEMBER_ID_REQUIRED` | Persist pending membership with assigned shadow member IDs, reply `MEMBER_ID_REQUIRED` with synthetic `clientMemberId`. |
| Mixed `MEMBER_ID_REQUIRED` + `NONE` | Best-effort `LEAVE_GROUP` to accepted shadows, reply `MEMBER_ID_REQUIRED`. |
| Shadows return `INCONSISTENT_GROUP_PROTOCOL` | Best-effort `LEAVE_GROUP` to accepted shadows, reply `INCONSISTENT_GROUP_PROTOCOL` (fatal, not remapped to `NOT_COORDINATOR`). |

#### Subscription Scoping

The gateway filters the `topics` and `ownedPartitions` fields per shadow to include only topics and partitions on that cluster. The `userData` field is forwarded verbatim to every shadow.

#### SyncGroup Assignment Decomposition

If the client assignment touches a cluster outside the membership, the gateway replies `REBALANCE_IN_PROGRESS` to force re-join. Assignment entries for unknown `memberId` values are skipped (the shadow's real leader will assign). If multiple shadows return non-empty `Assignment.userData`, the gateway picks the first non-empty value and logs a warning about degraded per-member assignor state.

#### Cooperative-Sticky Assignor Restriction

Cross-cluster `JOIN_GROUP` requests selecting the `cooperative-sticky` protocol are refused with `INCONSISTENT_GROUP_PROTOCOL`. The gateway cleans up successful shadows before responding.

{% hint style="info" %}
**Rationale:** Sticky state lives in per-member Subscription userData. With one shadow per backend, each shadow rebuilds sticky state in isolation, breaking the assignor's stickiness guarantee.
{% endhint %}
