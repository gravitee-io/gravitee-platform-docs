# Admin API Routing in Kafka Virtual Clusters

## Admin API Routing

Admin API routing on a Virtual Cluster differs from single-cluster endpoints. Single-cluster endpoints (`native-kafka` or `native-kafka-cluster`) forward admin operations unchanged. The rules below apply only to Virtual Cluster endpoints.

### Create topics

All CreateTopics requests are routed to backend cluster index 0 (first in configuration order). If the first backend is unreachable, the gateway falls back to the next configured backend. On any successful per-topic result, the gateway refreshes its metadata cache.

{% hint style="warning" %}
Affinity-based topic-creation routing is not yet implemented. CreateTopics always goes to backend 0. Operators cannot pick the hosting backend from the client side.
{% endhint %}

### DeleteTopics / CreatePartitions / DeleteRecords

The gateway looks up each topic's owning cluster via the topic-to-cluster index (by name only; the `topicId` field is not used). If the topic is not found in the cache, the gateway refreshes the metadata cache once and retries the lookup. Unresolved topics receive a synthetic `UNKNOWN_TOPIC_OR_PARTITION` error.

DeleteTopics and CreatePartitions trigger a metadata cache refresh after successful completion. DeleteRecords does not trigger a refresh (it moves the log start offset but does not change topic structure).

### DescribeConfigs / AlterConfigs / IncrementalAlterConfigs

For `TOPIC` resources, the gateway routes to the owning backend via the topic-to-cluster index. If the topic is not found in the cache, the gateway refreshes the metadata cache once and retries the lookup.

For `BROKER` and `BROKER_LOGGER` resources, the gateway resolves the owning backend from the virtual broker ID and rewrites the resource name (virtual→real on send, real→virtual on response).

For other resource types (`CLIENT_METRICS`, `GROUP`, `UNKNOWN`, default broker config with empty name), the gateway routes to backend index 0. This is a documented MESH limitation.

### DeleteGroups

For multiplexed consumer groups, the gateway fans out the request to each cluster the group spans, addressing per-cluster shadow groups (`<groupId>__shadow-c<N>`). For non-multiplexed groups, the gateway forwards the request to the cached cluster with the original group ID.

When the same client group ID exists across multiple clusters, the first non-NONE error code wins (delete is atomic from the client's view). On a NONE merged result, the gateway invalidates the group-to-cluster cache and removes the group from the multiplex store.

### OffsetDelete

For multiplexed consumer groups, the gateway splits the request per-topic via the topic-to-cluster index and sends each topic to the owning cluster's shadow group. For non-multiplexed groups, the gateway forwards the request to the cached cluster with the original group ID. Unresolved topics receive a synthetic `UNKNOWN_TOPIC_OR_PARTITION` error per partition.

### ListGroups

The gateway fans out the request to every backend cluster, remaps shadow group IDs (`<clientId>__shadow-c<N>`) back to client group IDs, and deduplicates the results. Failed backends contribute an empty list and a non-NONE error code. The merged response carries the first non-NONE error code and the maximum observed throttle time.

### DescribeGroups / ConsumerGroupDescribe

For multiplexed consumer groups, the gateway fans out the request to each cluster the group spans, addressing per-cluster shadow groups. For non-multiplexed groups, the gateway forwards the request to the cached cluster with the original group ID.

When the same client group ID exists across multiple clusters, the gateway merges the results into one entry: the first non-NONE error code wins, group state and assignor name are taken from the first shadow, and members are concatenated.
