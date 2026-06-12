# Consumer Group Routing: Classic Protocol (Pre-KIP-848)

## Classic Protocol (Pre-KIP-848)

Consumer groups using the classic protocol (default for most Kafka clients) are routed to a single backend cluster based on the topics in the group's subscription. The gateway caches the `groupId → clusterIndex` mapping after the first successful `JOIN_GROUP` request. Subsequent requests (`HEARTBEAT`, `SYNC_GROUP`, `LEAVE_GROUP`, `OFFSET_COMMIT`, `OFFSET_FETCH`) are forwarded to the cached cluster.

When a subscription spans multiple clusters, the gateway rejects the request with `INVALID_REQUEST` and the message:

```
Cross-cluster subscription is not supported in MESH mode (group '{groupId}' subscribes to topics that span clusters {clusters}). Split the subscription into per-cluster groups, mirror the topics, or use single-cluster routing.
```

### Coordinator Discovery

When the gateway receives a `FIND_COORDINATOR` request for a group not in the cache, it probes all backend clusters using `DESCRIBE_GROUPS`. The first cluster reporting the group alive owns the group. If no cluster reports the group alive, the gateway falls back to a deterministic hash of the group ID across reachable clusters. If all clusters are unreachable, the gateway hashes across all configured backends.

### Offset Operations

`OFFSET_COMMIT` and `OFFSET_FETCH` requests carrying a `memberId` are decomposed by cluster. The gateway translates the client's `memberId` to per-cluster shadow member IDs and fans out the request. Partitions for topics unknown to the index are stamped with `UNKNOWN_TOPIC_OR_PARTITION`. Admin tools (empty `memberId`) bypass multiplex and are forwarded as-is.

For `OFFSET_FETCH` with `topics=null` (v0–v7 "all topics" form) or v8+ with `group.topics() == null`, the gateway fans out to every cluster the group spans, using the group→clusters reverse index populated at `JOIN_GROUP` time. Groups never multiplexed receive an empty reply.

