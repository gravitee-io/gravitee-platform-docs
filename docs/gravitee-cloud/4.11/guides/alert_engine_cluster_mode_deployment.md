### Cluster Role Election

The Alert Engine cluster uses Hazelcast to elect one node as PRIMARY and designate others as REPLICA. The primary node processes incoming events. If the primary node fails, another node is automatically promoted. The first member in the Hazelcast member list (oldest member) is always the primary.

On startup, each node logs its role and cluster size:

```
INFO c.g.a.c.hz.HazelcastClusterManager - Local node [<address>] role is PRIMARY (cluster size: N)
INFO c.g.a.c.hz.HazelcastClusterManager - Local node [<address>] role is REPLICA (cluster size: N)
```

When cluster membership changes, the Alert Engine logs node joins and leaves:

```
INFO c.g.a.c.hz.HazelcastClusterManager - A node has joined the cluster: <MembershipEvent>
INFO c.g.a.c.hz.HazelcastClusterManager - A node has left the cluster: <MembershipEvent>
```

### Helm Chart Parameters

The following table describes the Helm chart parameters for configuring Alert Engine default filters:

| Property | Description | Default |
|:---------|:------------|:--------|
| `alerts.api.ws.defaultFilters.enabled` | Enable or disable Alert Engine default filters through the APIM REST API | `true` |

{% hint style="info" %}
Set this parameter to `false` to disable Alert Engine default filters when using the APIM REST API.
{% endhint %}

### Cluster Configuration

Configure cluster synchronization and Hazelcast settings in `gravitee.yml`:

| Property | Type | Value/Default | Description |
|:---------|:-----|:--------------|:------------|
| `cluster.sync.time.value` | integer | `30` | Sync interval between cluster nodes |
| `cluster.sync.time.unit` | enum | `SECONDS` | Time unit for sync interval |
| `cluster.hazelcast.config.path` | string | `${gravitee.home}/config/hazelcast.xml` | Path to Hazelcast configuration file |
| `cluster.hazelcast.systemProperties` | map | _(optional)_ | Hazelcast system properties (without 'hazelcast.' prefix) |

### Docker Compose Environment Variables

Configure the Docker Compose deployment using the following environment variables in `.env`:

| Variable | Default | Description |
|:---------|:--------|:------------|
| `LICENCE_KEY_PATH` | __ | Absolute path to the Gravitee license key file |
| `AE_VERSION` | `latest` | AE Docker image version |
| `AE_REPLICAS` | `2` | Number of AE nodes in the cluster |
| `CONTAINER_CPUS` | `1` | CPU limit per container |
| `CONTAINER_MEMORY` | `768M` | Memory limit per container |
| `GIO_MIN_MEM` | `256m` | JVM minimum heap size |
| `GIO_MAX_MEM` | `512m` | JVM maximum heap size |
