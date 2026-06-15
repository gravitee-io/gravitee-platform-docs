# Kafka Virtual Clusters Prerequisites and Gateway Configuration

## Prerequisites

Before configuring Kafka Virtual Clusters, complete the following steps:

* **Grant cluster management permissions**: Cluster management is hidden from basic users by default. Grant the **CLUSTER** environment-scoped permission (READ and UPDATE) to users who need to create or modify Kafka Cluster and Virtual Cluster entities.
   1. Navigate to [Console → Organization → Roles → USER](../configure-and-manage-the-platform/manage-organizations-and-environments/user-management.md).
   2. Enable the CLUSTER row.
* **Grant API-scoped permissions for native Kafka APIs**: Grant **NATIVE_LOG** and **NATIVE_ANALYTICS** permissions on the API scope to users who need to read native Kafka API logs and analytics. An automatic upgrader backfills these permissions on the built-in OWNER and PRIMARY_OWNER roles. Custom roles require manual grants.
* **Configure the default Kafka domain (HOST routing mode)**: When using HOST routing mode, configure the `gravitee_kafka_routingHostMode_defaultDomain` property so each API's host prefix maps to `<prefix>.<defaultDomain>:9092`.
   1. Navigate to [Console → Organization → Entrypoints & Sharding Tags](../configure-and-manage-the-platform/gravitee-gateway/).
   2. Set the **Default Kafka Domain** field.
* **Provision a wildcard TLS certificate (HOST routing mode)**: Provision a wildcard certificate covering `*.<defaultDomain>` to support SNI-based routing for all APIs on a single port.
* **Configure Kafka broker for next-generation consumer protocol**: If using Kafka 3.9 or later with the next-generation consumer protocol, set the following properties on the backend Kafka brokers:
   * `unstable.api.versions.enable=true`
   * `group.coordinator.rebalance.protocols=classic,consumer`
* **Configure distributed cache for producer ID sessions**: Configure a distributed cache (via `DistributedStoreFactory`) to persist producer ID sessions across gateway pod restarts. Without a distributed cache, pod restarts will cause idempotent producers to receive `PRODUCER_FENCED` errors and require application-level recovery.

## Gateway Configuration

### Routing Mode

| Property | Description | Example |
|:---------|:------------|:--------|
| `kafka.routingMode` | Global routing mode for all Kafka APIs. Valid values: `HOST`, `PORT`. | `HOST` |
| `gravitee_kafka_routingHostMode_defaultDomain` | Default domain suffix for HOST routing mode. The gateway constructs SNI hostnames as `<apiPrefix>.<defaultDomain>`. | `kafka.example.com` |

### Timeout and Retry Settings

| Property | Description | Default |
|:---------|:------------|:--------|
| `BACKEND_FORWARD_TIMEOUT` | Per-call timeout when forwarding gateway-internal requests (probe, FindCoordinator) to a backend. | 10 seconds |
| `SHADOW_HEARTBEAT_TIMEOUT` | Per-shadow timeout for cross-cluster ConsumerGroupHeartbeat fan-out. Must stay below the client heartbeat interval. | 3 seconds |
| `BACKEND_CALL_TIMEOUT` | Timeout for admin API fan-out calls (DeleteTopics, DescribeGroups). | 5 seconds |
| `METADATA_FETCH_TIMEOUT` | Timeout for metadata fetch during bootstrap. | 10 seconds |
| `RETRY_BACKOFF` | Default backoff duration for coordinator probe retries. | 300 milliseconds |
| `SHADOW_WARMUP_MAX_RETRIES` | Maximum retries for shadow coordinator warm-up. | 5 |

### Kafka Broker Configuration (Backend Clusters)

| Property | Description | Value |
|:---------|:------------|:------|
| `unstable.api.versions.enable` | Enables unstable Kafka API versions. Required for next-generation consumer protocol in Kafka 3.9. | `true` |
| `group.coordinator.rebalance.protocols` | Enables both classic and next-generation consumer rebalance protocols on the broker. | `classic,consumer` |
