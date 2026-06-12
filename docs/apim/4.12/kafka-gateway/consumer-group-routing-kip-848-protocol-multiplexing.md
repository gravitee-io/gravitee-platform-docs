# Consumer Group Routing: KIP-848 Protocol (Multiplexing)

## Overview

Consumer groups using the KIP-848 protocol (`group.protocol=consumer`) can span multiple backend clusters in a Kafka Virtual Cluster. The gateway multiplexes each logical consumer group across backends by creating shadow groups, managing synthetic member identities, and merging per-cluster responses into a single virtual view for the client.

## Key Concepts

### Shadow Group Naming

For each backend cluster in a Virtual Cluster, the gateway creates a shadow group with the naming pattern:

```xml
<clientGroupId>__shadow-c<clusterIndex>
```

Where `<clusterIndex>` is the zero-based position of the backend in the Virtual Cluster configuration.

**Example**: A client group `analytics` spanning two backends produces:
- `analytics__shadow-c0` on the first backend
- `analytics__shadow-c1` on the second backend

### Client Group ID Collision Prevention

The gateway rejects client group IDs matching the reserved pattern `.*__shadow-c\d+$` with `INVALID_GROUP_ID`. This prevents clients from creating groups that collide with gateway-managed shadow groups.

Group IDs containing `__shadow-c` without a trailing digit are permitted. For example, `orders__shadow-counter` is a valid client group ID.

### Virtual Member Identity

When a client joins a KIP-848 consumer group on a Virtual Cluster, the gateway generates a synthetic `virtualMemberId` in the format `gw-<UUID>`. The gateway persists the mapping between this virtual identity and the per-cluster shadow member identities in the `ConsumerGroupMembership` store.

The client never sees the shadow member IDs — all responses use the virtual identity.

### Virtual Member Epoch

The gateway maintains a `virtualMemberEpoch` that increments whenever the union of per-shadow partition assignments changes. This epoch is independent of the per-cluster shadow epochs and ensures the client sees a consistent view of its assignment across backends.

### DELEGATE_TO_BROKER SASL Mechanism

The `DELEGATE_TO_BROKER` mechanism passes the client's SASL handshake through to the backend broker as-is. The gateway does not interpret or validate the SASL exchange—the backend broker handles authentication directly.

{% hint style="info" %}
This mechanism requires no additional configuration fields. When `DELEGATE_TO_BROKER` is selected, no JAAS config, credentials, or other fields are permitted.
{% endhint %}

The gateway forwards the client's SASL exchange to the backend broker without modification. All authentication logic and credential validation occur on the broker side.

## Prerequisites

Before configuring Kafka cluster references, ensure the following permissions are granted:

* **CLUSTER environment-scoped permission (READ + UPDATE)**: Must be granted to users who will create or modify Kafka cluster configurations.
  1. Navigate to **Console → Organization → Roles → USER**.
  2. Enable the **CLUSTER** row.

* **NATIVE_LOG and NATIVE_ANALYTICS API-scoped permissions**: Must be granted to roles that need to view native Kafka API logs and analytics for APIs using Kafka cluster references.

{% hint style="info" %}
The built-in **OWNER** and **PRIMARY_OWNER** roles receive the NATIVE_LOG and NATIVE_ANALYTICS permissions automatically via an upgrader. Custom roles require manual grants.
{% endhint %}

## Bootstrap Flow

When a client joins a KIP-848 consumer group on a Virtual Cluster, the gateway generates a synthetic `virtualMemberId` in the format `gw-<UUID>`. The gateway splits the client's subscription by owning cluster and sends a shadow heartbeat to each touched backend. Each backend returns a real `shadowMemberId` and `shadowMemberEpoch`. The gateway persists a `ConsumerGroupMembership` record mapping the `virtualMemberId` to the per-cluster shadow identities and returns the merged result to the client.

## Steady-State Flow

The client sends `CONSUMER_GROUP_HEARTBEAT` with the cached `virtualMemberId`. The gateway resolves the membership from the store, splits the subscription and current assignment per cluster, and fans out each shadow heartbeat. Each backend returns an updated `shadowMemberEpoch` and assignment. The gateway merges the per-shadow responses, persists the updated membership, and bumps the `virtualMemberEpoch` whenever the union of per-shadow assignments changes.

## Leave Flow

The client sends `CONSUMER_GROUP_HEARTBEAT` with `memberEpoch=-1` or `memberEpoch=-2` (leave request). The gateway propagates the leave request to every shadow group and evicts the membership locally regardless of per-shadow outcomes.

## Error Handling

### Stale Epoch

If the client sends a heartbeat with an out-of-date `memberEpoch`, the gateway rejects the request with `FENCED_MEMBER_EPOCH` and evicts the membership from the store. The client must restart the bootstrap flow.

### Per-Shadow Error Reduction

When merging responses from multiple backends, the gateway applies a priority chain to determine the error code returned to the client. `FENCED_MEMBER_EPOCH` takes precedence over `UNKNOWN_MEMBER_ID`, which takes precedence over transient coordinator errors. Transport-level failures are stamped as `COORDINATOR_NOT_AVAILABLE`.

## Static Membership

When the client provides a `groupInstanceId`, the gateway appends `__shadow-c<clusterIndex>` to create per-cluster shadow instance IDs.

**Example**: A client with `groupInstanceId=analytics-worker-1` spanning two backends produces:
- `analytics-worker-1__shadow-c0` on the first backend
- `analytics-worker-1__shadow-c1` on the second backend

If `groupInstanceId` is `null`, the shadow instance IDs are also `null` (dynamic membership).

<figure><img src="../.gitbook/assets/kafka-virtual-cluster-add-dialog.png" alt="Add virtual cluster dialog with fields for name, description, and backend cluster selection"><figcaption></figcaption></figure>
