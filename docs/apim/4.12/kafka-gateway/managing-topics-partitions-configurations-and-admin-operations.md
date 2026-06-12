# Managing Topics, Partitions, Configurations, and Admin Operations

## Overview

This guide explains how to manage topics, partitions, configurations, and admin operations on Native Kafka APIs. Admin operations include CreateTopics, DeleteTopics, CreatePartitions, DeleteRecords, DescribeConfigs, AlterConfigs, IncrementalAlterConfigs, DescribeGroups, ConsumerGroupDescribe, ListGroups, DeleteGroups, and ACL operations. Routing behavior differs between single-cluster endpoints (native-kafka, native-kafka-cluster) and Virtual Cluster endpoints (native-kafka-virtual-cluster).

## Prerequisites

- **Cluster management permission**: Cluster management is hidden from basic users by default. Grant the CLUSTER environment-scoped permission (READ + UPDATE) to roles that need cluster access. Navigate to **Organization → Roles → [Role Name]** and enable the CLUSTER row.
- **Native API permissions** (for API-scoped access): Grant NATIVE_LOG and NATIVE_ANALYTICS permissions on the API scope to roles that need to read native Kafka API logs and analytics. The system automatically backfills these permissions on built-in OWNER and PRIMARY_OWNER roles; custom roles require manual grants.
- **Default Kafka domain** (for HOST routing mode): Configure the default domain for SNI-based routing. Navigate to **Organization → Entrypoints & Sharding Tags** and set the **Default Kafka Domain** field. The gateway maps each API's host prefix to `<prefix>.<defaultDomain>:9092`.
- **Wildcard certificate** (for HOST routing mode): Provision a wildcard certificate covering `*.<defaultDomain>` to support SNI dispatch across multiple APIs on a single bootstrap port. PORT routing mode does not require wildcard certificates.

## Admin Operations on Virtual Clusters

Admin operations on Virtual Cluster endpoints follow MESH-specific routing rules. Single-cluster endpoints (native-kafka, native-kafka-cluster) forward admin operations unchanged to the backend.

### CreateTopics

CreateTopics is routed to the first backend cluster in the configuration order (index 0). If the first backend is unreachable, the gateway falls back to the next backend in sequence. Any structured Kafka response (including per-topic errors such as TOPIC_ALREADY_EXISTS) stops the fallback chain. After a successful response, the gateway refreshes its metadata cache to resolve the new topic to the correct cluster for follow-up operations.

{% hint style="warning" %}
The gateway does not provide a mechanism to select the hosting backend from the client side. The first reachable backend in the configuration order owns the new topic. Affinity-based routing (prefix/regex → backend) is a documented follow-up feature.
{% endhint %}

### DeleteTopics

DeleteTopics is routed per topic using the topic-to-cluster index. A cache miss triggers a single metadata refresh and retry. Topics that remain unresolved after the retry receive a synthesized UNKNOWN_TOPIC_OR_PARTITION error. A batch spanning topics on different backends is split, fanned out to the owning backends, and re-merged into a single client response. After a successful response, the gateway refreshes its metadata cache.

### CreatePartitions

CreatePartitions is routed per topic using the topic-to-cluster index (topic name only). A cache miss triggers a single metadata refresh and retry. Topics that remain unresolved after the retry receive a synthesized UNKNOWN_TOPIC_OR_PARTITION error. If `validateOnly=false` and any topic succeeded, the gateway refreshes its metadata cache before responding to the client.

### DeleteRecords

DeleteRecords is routed per topic using the topic-to-cluster index (topic name only). A cache miss triggers a single metadata refresh and retry. Topics that remain unresolved after the retry receive a synthesized UNKNOWN_TOPIC_OR_PARTITION error per partition. The gateway does not refresh its metadata cache after a successful response — log start offset changes do not affect topic structure.

### DescribeConfigs, AlterConfigs, IncrementalAlterConfigs

Configuration operations follow resource-type-specific routing rules:

| Resource Type | Routing Behavior |
|:--------------|:-----------------|
| TOPIC | Routed to the owning backend via the topic-to-cluster index. Cache miss triggers a single metadata refresh and retry. |
| BROKER, BROKER_LOGGER | Routed to the cluster index via the virtual broker ID mapper. Resource name is rewritten from virtual broker ID to real broker ID on send, and from real to virtual on response. |
| CLIENT_METRICS, GROUP, UNKNOWN, or empty broker name | Routed to backend index 0. This is a documented MESH limitation. |

AlterConfigs and IncrementalAlterConfigs share the same routing semantics as DescribeConfigs. The `validateOnly` flag is forwarded as-is to every sub-cluster.

### DescribeGroups and ConsumerGroupDescribe

DescribeGroups and ConsumerGroupDescribe follow group-type-specific routing rules:

| Group Type | Routing Behavior |
|:-----------|:-----------------|
| Multiplexed (in GroupMultiplexStore) | Fanned out to every cluster the group spans. Each backend is addressed using the per-cluster shadow group name `<groupId>__shadow-c<N>`. Results are merged into a single DescribedGroup with a union of members from all backends. |
| Other | Forwarded to the cluster cached by GroupClusterRouter, or the connection's bound cluster as fallback. |

ConsumerGroupDescribe applies the same routing semantics to the next-gen consumer protocol (group.protocol=consumer, KIP-848).

### ListGroups

ListGroups is fanned out to every backend cluster. Shadow groups (`<clientId>__shadow-c<N>`) are remapped to `clientId` and deduplicated. Failed backends contribute an empty list plus a non-NONE error code. The merged response carries the first non-NONE error but includes rows from healthy backends.

### DeleteGroups

DeleteGroups follows group-type-specific routing rules:

| Group Type | Routing Behavior |
|:-----------|:-----------------|
| Multiplexed (in GroupMultiplexStore) | Fanned out to every cluster the group spans. Each backend is addressed using the per-cluster shadow group name `<groupId>__shadow-c<N>`. |
| Other | Forwarded to the cluster cached by GroupClusterRouter, or the connection's bound cluster as fallback. |

On a NONE merged result per group, the gateway invalidates the group in GroupClusterRouter and removes the group from GroupMultiplexStore.

### ACL Operations

All ACL operations (DESCRIBE_ACLS, CREATE_ACLS, DELETE_ACLS) are refused with SECURITY_DISABLED and the message:

```
MESH virtual cluster does not multiplex ACL operations; manage ACLs directly on each backend cluster.
```

A virtual cluster fronts N independent authorizer stores. Forwarding ACL operations to a single backend would leave the remaining backends divergent. Operators must manage ACLs directly on each backend cluster until cross-cluster ACL coordination is in scope.
