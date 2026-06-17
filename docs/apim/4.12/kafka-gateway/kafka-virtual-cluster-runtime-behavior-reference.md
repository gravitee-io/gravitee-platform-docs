# Kafka Virtual Cluster Runtime Behavior Reference

## Managing Clusters

### Deploying a Cluster

To activate a cluster on the gateway:

1. Navigate to **Console → Kafka Clusters** (or **Kafka Virtual Clusters**).
2. Open the cluster you want to deploy.
3. Click **Deploy**.
4. The cluster's lifecycle state changes to `DEPLOYED`, the version number increments (or is set to 1 if this is the first deployment), and the `deployedAt` timestamp is updated.

### Undeploying a Cluster

To deactivate a cluster on the gateway:

1. Navigate to **Console → Kafka Clusters** (or **Kafka Virtual Clusters**).
2. Open the cluster you want to undeploy.
3. Click **Undeploy**.
4. The cluster's lifecycle state changes to `UNDEPLOYED`. The version number does not change.

### Updating a Deployed Cluster

When you update the configuration of a deployed cluster (e.g., add a connection, change bootstrap servers), the cluster's lifecycle state changes to `PENDING`. To apply the changes to the gateway, click **Deploy** again. The version number increments and the state returns to `DEPLOYED`. The Cross ID is immutable after creation — update attempts return the error `"CrossId is immutable and cannot be changed after creation."`

### Searching and Filtering Clusters

The cluster list view supports filtering by cluster type and searching by name or description:

- **Type filter:** Select a cluster type (`KAFKA_CLUSTER_STANDALONE`, `KAFKA_CLUSTER`, or `KAFKA_VIRTUAL_CLUSTER`) from the dropdown to show only clusters of that type.
- **Search:** Enter a query in the search box to filter clusters by name or description (case-insensitive).

### Viewing Deployed Clusters

To retrieve a list of all deployed clusters with their connections via the REST API:

```
GET /clusters/deployed
```

**Response:**

```json
[
  {
    "crossId": "eu-prod",
    "name": "EU Production",
    "description": "Production Kafka cluster in EU region",
    "deployedAt": "2024-01-15T10:30:00Z",
    "version": 3,
    "type": "KAFKA_CLUSTER",
    "connections": [
      {
        "crossId": "internal-plaintext",
        "name": "Internal PLAINTEXT"
      },
      {
        "crossId": "external-sasl",
        "name": "External SASL_SSL"
      }
    ]
  }
]
```

### Consumer Group Operations

#### ListGroups

ListGroups fans out across backends, unions group IDs, and strips shadow suffixes (`<groupId>__shadow-c<N>` collapses back to `<groupId>`) so one client-visible group appears per logical group.

#### DescribeGroups

DescribeGroups (classic protocol) fans out per-cluster and merges results so the client sees one virtual group with members from every backend. ConsumerGroupDescribe (KIP-848) uses a dedicated router with the same merge behavior as classic DescribeGroups.

#### DeleteGroups

DeleteGroups splits per-cluster, fans out, and merges results.

#### OffsetFetch

OffsetFetch v8+ multi-group form (KIP-709) is supported, but multi-group requests are refused if any groupId collides with the reserved shadow suffix. OffsetFetch v0–v7 with `data.topics() == null` (all-topics request) replies with an empty topics list (no group→clusters index). OffsetFetch v8+ with `groups[i].topics == null` (all-topics request for that group) replies with an empty topics list for that group. Offset fetch requests for topics not in `TopicClusterIndexService` stamp `UNKNOWN_TOPIC_OR_PARTITION` on affected partitions. Offset fetch requests for topics on clusters not in the membership stamp `UNKNOWN_TOPIC_OR_PARTITION` on affected partitions.

#### OffsetCommit

Offset commit requests for topics not in `TopicClusterIndexService` stamp `UNKNOWN_TOPIC_OR_PARTITION` on affected partitions. Offset commit requests for topics on clusters not in the membership stamp `UNKNOWN_TOPIC_OR_PARTITION` on affected partitions.

#### OffsetDelete

OffsetDelete splits per-topic, fans out, and merges results.

### Topic Operations

#### CreateTopics

Every `CREATE_TOPICS` request on a MESH broker-connect session is routed to the first backend cluster (config order, index 0) until affinity rules are introduced. If the first backend is unreachable, the router tries the next configured backend in sequence. Only a structured Kafka response (even with per-topic errors) is treated as authoritative.

#### CreatePartitions

CreatePartitions is resolved per-topic via `TopicClusterIndexService` and sent to the owning backend. A miss triggers a single metadata refresh + retry.

#### DeleteTopics

DeleteTopics uses the same per-topic routing as CreatePartitions. A batch spanning topics on different backends is split, fanned out, and re-merged into one client response.

### Configuration Operations

#### DescribeConfigs / AlterConfigs / IncrementalAlterConfigs

DescribeConfigs, AlterConfigs, and IncrementalAlterConfigs use per-topic routing for topic resources and per-cluster fan-out + merge for broker/cluster resources.

**Resource routing:**

| Resource Type | Routing Rule | Name Rewrite |
|:--------------|:-------------|:-------------|
| `TOPIC` | Owning backend via `TopicClusterIndexService`; refresh-on-miss | None |
| `BROKER` / `BROKER_LOGGER` | Virtual broker ID → cluster index via `VirtualBrokerIdMapper` | Virtual→real on send; real→virtual on response |
| Other types (CLIENT_METRICS, GROUP, UNKNOWN) | Backend index 0 | None |
| Empty broker name | Backend index 0 | None |

**ConfigResourceResolver resolution outcome:**

Per-resource resolution for `DescribeConfigs` / `AlterConfigs` / `IncrementalAlterConfigs`.

**Record:** `Resolution(OptionalInt targetCluster, String sentResourceName, Errors failure)`

| Outcome | Target Cluster | Failure Code | Meaning |
|:--------|:---------------|:-------------|:--------|
| Dispatch | present | `null` | Send to that backend with `sentResourceName` on wire |
| TOPIC miss | empty | `null` | Caller should refresh metadata and retry; if still empty, synthesize `UNKNOWN_TOPIC_OR_PARTITION` |
| Structural error | empty | non-null | Surface `failure` directly to client |

### Management API

| Method | Path | Description |
|:-------|:-----|:------------|
| POST | `/clusters/{clusterId}/_deploy` | Deploy cluster to gateway (sets state to `DEPLOYED`, increments version) |
| POST | `/clusters/{clusterId}/_undeploy` | Undeploy cluster from gateway (sets state to `UNDEPLOYED`) |
| GET | `/clusters/deployed` | List all deployed clusters with connections |
| GET | `/clusters/schema/configuration?type={ClusterType}` | Get configuration schema for cluster type |

## Creating a Kafka API

1. Navigate to **Console → APIs → Add API → Create API**.
2. Select **Native Kafka** as the protocol.
3. Complete steps 1–4 of the wizard (name, version, entrypoint configuration). The entrypoint type is automatically set to `native-kafka` (Client).
4. In step 5 (**Configure Endpoint**), select an endpoint connector type:
   - **Broker** (`native-kafka`): Enter bootstrap servers directly. Use this for one-shot APIs where you don't expect to reuse the broker configuration.
   - **Cluster** (`native-kafka-cluster`): Select a Kafka Cluster entity and one of its connections from the dropdowns. Use this when you have a reusable cluster entity and want centralized configuration management.
   - **Virtual Cluster** (`native-kafka-virtual-cluster`): Select a Kafka Virtual Cluster entity from the dropdown. Use this to fan out across N backend clusters (MESH mode).
5. Complete the remaining wizard steps (plans, documentation, deployment).
6. Click **Create API**.

**Endpoint Connector Configuration Reference:**

| Connector Type | Configuration Fields |
|:---------------|:---------------------|
| Broker | Bootstrap Servers (inline, marked as secret) |
| Cluster | Cluster Cross ID, Connection Cross ID |
| Virtual Cluster | Virtual Cluster Cross ID |
