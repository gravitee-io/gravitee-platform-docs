# Kafka Virtual Cluster Runtime Behavior and Restrictions

## Runtime Behavior

### Producer ID Session Management

When a Kafka client uses idempotent producers or transactions, the gateway maintains a `ProducerIdSession` cache that maps virtual producer IDs to real backend producer IDs per cluster. If the session is missing (due to cache eviction, gateway pod failover without distributed cache, or no mapping for the target cluster), the gateway returns a synthetic `PRODUCER_FENCED` error.

`PRODUCER_FENCED` is a fatal error for Kafka clients. The `TransactionManager` transitions to a fatal state and the producer cannot recover automatically. The application must detect the failure and create a new `KafkaProducer` instance, which will run a fresh `INIT_PRODUCER_ID` and rebuild the session.

Configure a distributed `CacheManager` (Hazelcast or Redis) to ensure sessions survive gateway restarts and round-robin client reconnections.

### SASL Delegate Replay

When a client connects to a virtual cluster and performs SASL authentication, the gateway captures the client's authentication payload (for replay-safe mechanisms only) and stores it as `DelegateSaslCredentials`. When cross-cluster operations (e.g., `FIND_COORDINATOR`, `DescribeGroups` probe) require opening a fresh connection to a backend cluster the client never directly connected to, the gateway replays the captured `SASL_HANDSHAKE` and `SASL_AUTHENTICATE` frames on the new connection.

Only the `PLAIN` mechanism is supported for SASL delegate replay. AWS_MSK_IAM (time-bound signatures), SCRAM (challenge-response), and GSSAPI (tickets) are not replay-safe. Credentials are cleared automatically when the client connection closes.

### Cluster Lifecycle States

Clusters of type `KAFKA_CLUSTER` and `KAFKA_VIRTUAL_CLUSTER` support lifecycle state transitions:

| From State | To State | Trigger | Validation |
|:-----------|:---------|:--------|:-----------|
| `UNDEPLOYED` | `DEPLOYED` | User clicks **Deploy** | Cluster type must be `KAFKA_CLUSTER` or `KAFKA_VIRTUAL_CLUSTER` |
| `DEPLOYED` | `UNDEPLOYED` | User clicks **Undeploy** | N/A |
| `DEPLOYED` | (deleted) | User clicks **Delete** | Cluster is undeployed first, then deleted |
| `UNDEPLOYED` | (deleted) | User clicks **Delete** | Direct deletion |

The console enforces these transitions via the Danger Zone actions in the cluster General tab.

## Gateway Configuration

## Creating a Kafka Cluster

Navigate to **Kafka > Clusters** in the console and click **Create a new Kafka Cluster**. Complete the following fields:

1. Enter a value in the **Cluster name** field.
2. Enter a value in the **Description** field (optional).
3. Add one or more connections in the **Connections** section. For each connection:
   - Enter a **Cross ID** (unique identifier for the connection).
   - Enter a **Name** for the connection.
   - Enter the **Bootstrap Servers** (comma-separated list of `host:port` pairs).
   - Configure **Security** settings (protocol, SASL mechanism, credentials).
4. Click **Save**.

After creation, the cluster is in the `UNDEPLOYED` state. Navigate to the cluster's **General** tab and click **Deploy** to transition it to `DEPLOYED`. Once deployed, the cluster can be referenced by APIs via its `crossId`.

**Cluster Connection Reference Table**:

| Field | Description | Example |
|:------|:------------|:--------|
| **Cross ID** | Unique identifier for the connection | `prod-us-east-1` |
| **Name** | Human-readable connection name | `Production US East` |
| **Bootstrap Servers** | Comma-separated list of broker addresses | `broker1:9092,broker2:9092` |
| **Security Protocol** | Protocol for broker communication | `SASL_SSL` |
| **SASL Mechanism** | Authentication mechanism | `PLAIN`, `SCRAM-SHA-512`, `DELEGATE_TO_BROKER` |

## Creating a Kafka Virtual Cluster

Navigate to **Kafka > Virtual Clusters** in the console and click **Create a new Kafka Virtual Cluster**. Complete the following fields:

1. Enter a value in the **Cluster name** field.
2. Enter a value in the **Description** field (optional).
3. Add one or more backend clusters in the **Backends** section. For each backend:
   - Enter the **Cluster Cross ID** (references a deployed `KAFKA_CLUSTER`).
   - Enter the **Connection Cross ID** (references a connection within that cluster).
4. Click **Save**.

After creation, the virtual cluster is in the `UNDEPLOYED` state. Navigate to the virtual cluster's **General** tab and click **Deploy** to transition it to `DEPLOYED`. Once deployed, the virtual cluster can be referenced by APIs via its `virtualClusterCrossId`.

**Virtual Cluster Backend Reference Table**:

| Field | Description | Example |
|:------|:------------|:--------|
| **Cluster Cross ID** | References a deployed `KAFKA_CLUSTER` | `prod-cluster` |
| **Connection Cross ID** | References a connection within that cluster | `prod-us-east-1` |

## Managing Cluster Lifecycle

### Deploying a Cluster

Navigate to the cluster's **General** tab. If the cluster is in the `UNDEPLOYED` state, click **Deploy**. The cluster transitions to `DEPLOYED` and becomes available for API endpoint configuration.

### Undeploying a Cluster

Navigate to the cluster's **General** tab. If the cluster is in the `DEPLOYED` or `PENDING` state, click **Undeploy**. The cluster transitions to `UNDEPLOYED` and is no longer available for API endpoint configuration.

### Deleting a Cluster

Navigate to the cluster's **General** tab and click **Delete**. If the cluster is deployed, the console triggers undeploy first, then deletes the cluster. If the cluster is already undeployed, it is deleted immediately.

### Deployed Clusters API

The gateway exposes a REST endpoint for querying deployed clusters:

**Endpoint**: `GET /_node/clusters/deployed`

**Response**:
```json
[
  {
    "crossId": "prod-cluster",
    "type": "KAFKA_CLUSTER",
    "connections": [
      {
        "crossId": "prod-us-east-1",
        "name": "Production US East",
        "bootstrapServers": "broker1:9092,broker2:9092"
      }
    ]
  },
  {
    "crossId": "virtual-prod",
    "type": "KAFKA_VIRTUAL_CLUSTER",
    "backends": [
      {
        "clusterCrossId": "prod-cluster",
        "connectionCrossId": "prod-us-east-1"
      }
    ]
  }
]
```

This endpoint is used by the gateway to resolve cluster references during API deployment.

## Restrictions

- Producer ID sessions are lost on gateway pod failover unless a distributed `CacheManager` (Hazelcast or Redis) is configured.
- SASL delegate replay supports only the `PLAIN` mechanism. AWS_MSK_IAM, SCRAM, and GSSAPI are not replay-safe.
- Virtual clusters strip KIP-848 / KIP-932 group APIs (`CONSUMER_GROUP_HEARTBEAT`, `CONSUMER_GROUP_DESCRIBE`, `SHARE_GROUP_HEARTBEAT`, `SHARE_GROUP_DESCRIBE`) from the API version intersection, forcing clients to use the classic group protocol.
- Deployed clusters must be undeployed before deletion. The console enforces this by triggering undeploy first.
- Callers must explicitly invoke `close()` on the `KafkaEndpointManager` during API stop. Failure to do so leaks file descriptors.
- The current implementation opens a fresh connection per cross-cluster request. Connection pooling is planned but not yet implemented.
- Response frame rewriter optimization skips re-serialization only for responses with empty `nodeEndpoints`. Other no-op cases (e.g., empty records) are not yet optimized.

## Related Changes

The console now displays cluster lifecycle state badges (`DEPLOYED`, `PENDING`, `UNDEPLOYED`) in the cluster list and General tab. Endpoint configuration forms validate that user-entered cluster and connection `crossId` values match deployed clusters. The cluster schema's `displayIf` logic for SASL fields was corrected to use relative path references (`../protocol` instead of `value.security.protocol`). The SASL mechanism enum now includes `DELEGATE_TO_BROKER` as a selectable option. Database migration is required: a new `type` column is added to the `clusters` table, and existing clusters are backfilled with `KAFKA_CLUSTER_STANDALONE`. The `KafkaServer` bind logic now retries up to 3 times with exponential backoff (50ms, 100ms, 200ms) when encountering "Address already in use" errors. The `gravitee-reactor-native-kafka` plugin is updated to version `7.0.0-alpha.9` to support virtual cluster routing and producer ID session management.
