### Schedule Calculation

When a trigger has a window-based condition with a duration, the Alert Engine calculates the next evaluation time using an anchor timestamp. The anchor is either the `updated_at` or `created_at` timestamp. This ensures evaluations occur at consistent intervals. If the anchor timestamp is in the future or missing, the engine falls back to scheduling from the current time.

The schedule calculation formula:

```
nextIntervalNumber = floor(timeSinceAnchor / duration) + 1
nextEvalAt = anchorTime + (nextIntervalNumber * duration)
initialDelay = nextEvalAt - now
```

If the calculated delay is negative, the trigger evaluates immediately.

### Trigger Timestamps

The Trigger API includes `created_at` and `updated_at` fields, serialized as Unix epoch milliseconds. These timestamps enable schedule anchoring and are displayed in the UI. The `updated_at` field is set whenever a trigger configuration changes.

### Prerequisites

Before deploying Alert Engine in cluster mode, ensure the following:

* Docker is installed and running (required for integration tests using Testcontainers)
* A Gravitee license key file is available
* A Hazelcast configuration file exists at `${gravitee.home}/config/hazelcast.xml` (required for production TCP-IP discovery)

### Gateway Configuration

#### Cluster Synchronization

| Property | Description | Example |
|:---------|:------------|:--------|
| `cluster.sync.time.value` | Sync interval between cluster nodes | `30` |
| `cluster.sync.time.unit` | Time unit for sync interval | `SECONDS` |
| `cluster.hazelcast.config.path` | Path to Hazelcast configuration file | `${gravitee.home}/config/hazelcast.xml` |
| `cluster.hazelcast.systemProperties` | Hazelcast system properties (without `hazelcast.` prefix) | _(optional map)_ |

#### Alert Engine Connector

| Property | Description | Example |
|:---------|:------------|:--------|
| `alerts.alert-engine.ws.defaultFilters.enabled` | Automatically add default installation filters to triggers | `true` |

#### Helm Chart Parameters

| Property | Description | Example |
|:---------|:------------|:--------|
| `alerts.api.ws.defaultFilters.enabled` | Enable or disable Alert Engine default filters through the APIM Rest API | `true` |

#### Docker Compose Environment Variables

| Variable | Description | Example |
|:---------|:------------|:--------|
| `LICENCE_KEY_PATH` | Absolute path to the Gravitee license key file | `/path/to/license.key` |
| `AE_VERSION` | AE Docker image version | `latest` |
| `AE_REPLICAS` | Number of AE nodes in the cluster | `2` |
| `CONTAINER_CPUS` | CPU limit per container | `1` |
| `CONTAINER_MEMORY` | Memory limit per container | `768M` |
| `GIO_MIN_MEM` | JVM minimum heap size | `256m` |
| `GIO_MAX_MEM` | JVM maximum heap size | `512m` |

### Deploying a Cluster

1. Configure a `.env` file with the required environment variables. See `.env.example` in `docker/cluster/` for reference.
2. Set `LICENCE_KEY_PATH` to the absolute path of your license key file.
3. Adjust `AE_REPLICAS` to the desired number of nodes.
4. Start the cluster:

   

   The first node to join becomes the primary.

5. Verify cluster status by calling the `/_node` endpoint:

   

   Or check logs for messages like:

   

### Configuring Hazelcast Discovery

By default, the cluster uses multicast discovery, which works when nodes are on the same network. For production environments, configure TCP-IP discovery in `hazelcast.xml`:

```xml
<network>
    <join>
        <multicast enabled="false"/>
        <tcp-ip enabled="true">
            <member>192.168.1.10</member>
            <member>192.168.1.11</member>
            <member>192.168.1.12</member>
        </tcp-ip>
    </join>
</network>
```

The cluster name is `graviteeio-ae`. Distributed data structures include `IMap` for buckets, dampenings, and cached properties; `ITopic` for event broadcasting; and `ReliableTopic` for inter-node communication.

### Restrictions

* Duration for window-based triggers must be greater than 0. Validation error: `"Duration must be greater than 0 for trigger {triggerId}"`
* If the anchor timestamp (`updated_at` or `created_at`) is in the future, the engine falls back to scheduling from the current time and logs a warning.
