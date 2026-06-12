# Managing Topics, Partitions, Configurations, and Admin Operations

## Managing Topics and Partitions

### CreateTopics

`CREATE_TOPICS` requests are routed to the first backend cluster (configuration order, index 0). If the first cluster fails, the gateway falls back to the next configured backend (index 1, 2, …) until a structured Kafka response is received. Any structured Kafka response—including per-topic errors such as `TOPIC_ALREADY_EXISTS`—stops the fallback. After a successful response, the gateway refreshes the metadata cache.

### DeleteTopics

`DELETE_TOPICS` requests are routed per topic using the topic-to-cluster index. If a topic is not in the cache, the gateway performs a single metadata refresh and retries. Unresolved topics receive a synthesized `UNKNOWN_TOPIC_OR_PARTITION` result. After a successful response, the gateway refreshes the metadata cache.

### CreatePartitions

`CREATE_PARTITIONS` requests are routed per topic using the topic-to-cluster index (name only). If a topic is not in the cache, the gateway performs a single metadata refresh and retries. Unresolved topics receive a synthesized `UNKNOWN_TOPIC_OR_PARTITION` result. If `validateOnly=false` and any topic succeeded, the gateway refreshes the metadata cache before responding.

### DeleteRecords

`DELETE_RECORDS` requests are routed per topic using the topic-to-cluster index (name only). If a topic is not in the cache, the gateway performs a single metadata refresh and retries. Unresolved topics receive a synthesized `UNKNOWN_TOPIC_OR_PARTITION` per partition. The gateway does not refresh the metadata cache after success because log start offset changes do not affect topic structure.

## Managing Configurations

### DescribeConfigs

`DESCRIBE_CONFIGS` requests are routed based on resource type:

| Resource Type | Routing Rule |
|:--------------|:-------------|
| `TOPIC` | Owning backend via topic-to-cluster index; cache miss triggers refresh + retry. |
| `BROKER` / `BROKER_LOGGER` | Virtual broker ID → cluster index via virtual broker ID mapper. Resource name is rewritten virtual→real on send, real→virtual on response. |
| `CLIENT_METRICS`, `GROUP`, `UNKNOWN`, empty broker name | Backend index 0 (documented MESH limitation). |

### AlterConfigs / IncrementalAlterConfigs

`ALTER_CONFIGS` and `INCREMENTAL_ALTER_CONFIGS` requests share routing semantics with `DESCRIBE_CONFIGS`. The `validateOnly` flag is forwarded as-is to every sub-cluster.

## Managing Consumer Groups (Admin Operations)

### DescribeGroups

`DESCRIBE_GROUPS` requests are routed based on group type:

| Group Type | Routing Rule |
|:-----------|:-------------|
| Multiplexed (in `GroupMultiplexStore`) | Fan-out to every cluster the group spans; address per-cluster shadow `<groupId>__shadow-c<N>`; merge results into single `DescribedGroup` with union of members. |
| Other | Forward to cluster cached by `GroupClusterRouter`, or connection's bound cluster as fallback. |

### ConsumerGroupDescribe

`CONSUMER_GROUP_DESCRIBE` requests share routing semantics with `DESCRIBE_GROUPS`, applied to next-gen consumer protocol (`group.protocol=consumer`, KIP-848).

### ListGroups

`LIST_GROUPS` requests are fanned out to every backend cluster. Shadow groups (`<clientId>__shadow-c<N>`) are remapped to `clientId` and deduplicated. Failed backends contribute an empty list plus a non-NONE error code; the merged response carries the first non-NONE error but includes rows from healthy backends.

### DeleteGroups

`DELETE_GROUPS` requests are routed based on group type:

| Group Type | Routing Rule |
|:-----------|:-------------|
| Multiplexed (in `GroupMultiplexStore`) | Fan-out to every cluster the group spans; address per-cluster shadow `<groupId>__shadow-c<N>`. |
| Other | Forward to cluster cached by `GroupClusterRouter`, or connection's bound cluster as fallback. |

On `NONE` merged result per group, the gateway invalidates the group in `GroupClusterRouter` and removes the group from `GroupMultiplexStore`.

## Managing ACLs

All ACL operations (`DESCRIBE_ACLS`, `CREATE_ACLS`, `DELETE_ACLS`) are refused with `SECURITY_DISABLED` and the message:

```
MESH virtual cluster does not multiplex ACL operations; manage ACLs directly on each backend cluster.
```
