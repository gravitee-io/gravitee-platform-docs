# Kafka Virtual Clusters: Advanced Routing and Multiplex Reference

## Consumer Group Routing

Consumer groups are routed based on topic subscription topology. When a client joins a group and subscribes to topics that all reside on a single backend cluster, the gateway caches the group-to-cluster mapping and forwards all subsequent group RPCs (Heartbeat, SyncGroup, LeaveGroup, OffsetCommit, OffsetFetch) to that cluster. On JoinGroup with a single-cluster subscription, any existing multiplex membership for the group/member is purged. If the subscription spans multiple clusters, the gateway creates shadow groups (`<groupId>__shadow-c<N>`) on each backend and multiplexes the client's view into a single synthetic member ID (format: `gw-{uuid}`) and generation ID.

**LeaveGroup special case**: LeaveGroup requests are forwarded without invalidating the group-to-cluster cache; other group members still rely on the pin, and cache TTL evicts stale entries.

**Heartbeat and SyncGroup error handling**: On receiving `UNKNOWN_MEMBER_ID` or `ILLEGAL_GENERATION` errors, the membership is evicted from the store.

**Offset commit and fetch operations** fan out across all clusters that own the requested topics. The gateway merges per-partition offsets from each backend into a single response. For offset commits with a non-empty `memberId`, the gateway translates the client member ID and generation ID to the corresponding shadow group bindings on each cluster. OFFSET_COMMIT with topics spanning multiple clusters multiplexes when topics span multiple clusters AND (if `memberId` is non-empty) the member has a multiplex membership. OFFSET_FETCH with topics spanning multiple clusters multiplexes when the explicit topic list spans multiple clusters. OFFSET_FETCH "all topics" form (`topics == null`) multiplexes when the group is multiplexed (has a group→clusters index entry written at JoinGroup time). For OFFSET_FETCH v0–v7 with `topics=null` (fetch all form), the gateway replies with an empty response as this form is unsupported. For OFFSET_FETCH v8+ multi-group requests, the gateway runs single-group decomposition per requested group and reassembles into v8+ response shape.

**Cache miss handling for offset RPCs**: The gateway attempts topic-hint fallback using the cluster of the first topic in the request that exists in the topic index. If no topics resolve, it forwards to the connection's bound cluster.

**FindCoordinator requests** for consumer groups (coordinator type `GROUP`) and share groups (coordinator type `SHARE`) trigger a probe across all backends using DescribeGroups. If the group exists on at least one backend, the gateway routes to the first cluster in configuration order and caches the decision. If the group is unknown on all backends, the gateway falls back to deterministic hash routing; this fallback is **not cached**, allowing future probe-capable callers to discover the real cluster. For transaction coordinators (coordinator type `TRANSACTION`), the gateway uses deterministic hash routing (transactions are single-cluster per MESH constraints).

## Multiplex Membership Lifecycle

**Per-cluster subscription filtering**: Each shadow receives only the topics whose `TopicClusterIndexService` cluster index matches the shadow's cluster. Owned partitions are filtered per cluster — shadow-c0 sees only `ownedPartitions` whose topic lives on cluster 0. User data is forwarded verbatim to every shadow (assignor state is per-shadow; backends ignore entries for topics outside their subscription).

**Leader-side assignment decomposition (SyncGroup)**: The client assigns partitions to `clientMemberId`; the handler splits partitions by cluster via `TopicClusterIndexService` and re-encodes per-shadow with `shadowMemberId`. Partitions whose topic is not in the index are silently dropped (no shadow receives them).

**Follower-side assignment**: Empty `assignments` list forwarded as-is to every shadow.

**Assignment merge (SyncGroup)**: The gateway unions all shadow-returned partitions. The first non-empty `Assignment.userData` from shadow responses wins; subsequent non-empty payloads are discarded with a warning.

**Virtual epoch bump rule**: `virtualMemberEpoch` is bumped if and only if the merged assignment (union of per-shadow assignments) changes. Per-backend epoch churn unrelated to the merged view never reaches the client.

**Generation ID aggregation**: The merged `clientGenerationId` is the sum of shadow `generationId` values, with monotone bump logic: if the sum is less than or equal to the previous `clientGenerationId`, the gateway bumps to `previous + 1`. If the sum overflows `Integer.MAX_VALUE`, it saturates at `Integer.MAX_VALUE`. If the previous value is `Integer.MAX_VALUE` and the sum is greater than or equal to `MAX_VALUE`, the gateway wraps to `1` to avoid stall.

**Multiplex heartbeat error priority**: Per-shadow errors are reduced to a single client-facing code by priority chain: `FENCED_MEMBER_EPOCH` > `UNKNOWN_MEMBER_ID` > `UNRELEASED_INSTANCE_ID` > coordinator-transient (`NOT_COORDINATOR` / `COORDINATOR_NOT_AVAILABLE` / `COORDINATOR_LOAD_IN_PROGRESS`) > other. Returns `null` when every shadow reported `Errors.NONE`.

## Admin API Routing

**Topic operations** (CreateTopics, DeleteTopics, CreatePartitions, DeleteRecords) route to the owning backend cluster via the topic-to-cluster index. CreateTopics targets the first configured backend (index 0) by default; if the first backend is unreachable, the gateway tries the next configured backend in order. Only a structured Kafka response (even with per-topic errors) is treated as authoritative. If a topic is not found in the index, the gateway performs a single metadata cache refresh before synthesizing an `UNKNOWN_TOPIC_OR_PARTITION` error.

**Broker configuration operations** (DescribeConfigs, AlterConfigs, IncrementalAlterConfigs) route TOPIC resources to the owning cluster via `TopicClusterIndexService`, with metadata refresh retry on cache miss. BROKER and BROKER_LOGGER resources route to the owning backend via `VirtualBrokerIdMapper.toClusterIndex`; the `resourceName` is rewritten virtual→real on send and real→virtual on response. Other resource types (CLIENT_METRICS, GROUP, UNKNOWN) route to backend index 0. Empty broker names route to backend index 0.

**Group operations** (DescribeGroups, DeleteGroups, ListGroups, OffsetDelete, ConsumerGroupDescribe) route multiplexed groups to all clusters the group spans (addressing shadow groups `<groupId>__shadow-c<N>`) and non-multiplexed groups to the cached cluster or the connection's bound cluster.

**ACL operations** (DescribeAcls, CreateAcls, DeleteAcls) are refused with `SECURITY_DISABLED` and the message: "MESH virtual cluster does not multiplex ACL operations; manage ACLs directly on each backend cluster."

## Metadata Merging

The gateway fetches metadata from all backend clusters, excludes internal topics (names starting with `__`) and topics with error codes, and merges the results into a single response. On topic name collisions (same name, different IDs across clusters), the first cluster in configuration order wins for name-based routing, but all topics are indexed by ID for correct ID-based routing. Topic name collisions are logged once per topic name at DEBUG level with `apiId` in MDC. Broker IDs, partition leaders, replicas, ISR lists, and offline replicas are remapped to virtual IDs. The controller ID is taken from the first cluster with a valid controller. The virtual cluster ID is generated as `UUID.nameUUIDFromBytes(virtualClusterCrossId.getBytes())`.

**Metadata cache behavior**: If the cache is empty, the gateway waits for initial population before serving requests. If all requested topics are present in the cache, the gateway serves from cache directly. If `allowAutoTopicCreation=true` and at least one requested topic is missing, the gateway forwards the request to the first reachable backend for auto-creation and then refreshes the merged cache. If auto-creation is disabled and topics are missing, the gateway forces a cache refresh before responding; refresh failures fall back to the stale snapshot.

## Delegate-to-Broker SASL

When all backend clusters are configured with `security.sasl.mechanism.type = DELEGATE_TO_BROKER`, the gateway multiplexes the client's SASL handshake to all backends in parallel. If the metadata cache is empty, the gateway fans out SASL frames to every backend cluster; if the cache is populated, it fans out to one backend for credential validation only. Each backend authenticates the client's credentials independently. If any cluster rejects the authentication, the gateway forwards the error to the client and fails the connection. After all clusters authenticate, the gateway fetches metadata on each authenticated connection (first client only) and merges the responses into the cache. Subsequent bootstrap clients are served from cache without backend connections.

The gateway captures replay-safe credentials (PLAIN mechanism only) during the SASL exchange and stores them in the connection context. When opening sub-connections for cross-cluster operations (e.g., FindCoordinator probes), the gateway replays the captured SASL handshake and authenticate frames to the target backend before sending the application request. In delegate-to-broker mode, delegate replay opens a fresh per-RPC backend connection and does not touch the shared pool.

## Topic Name Rewriting

The Kafka Topic Mapping policy (`gravitee-policy-kafka-topic-mapping`) is available as a separate plugin for bidirectional topic name rewriting. This policy allows you to map client-visible topic names to backend topic names and vice versa, enabling namespace isolation or topic aliasing across virtual clusters.
