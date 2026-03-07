---
description: This article walks through how to configure Alert Engine
---

# Configure Alert Engine

## Introduction

There are three different ways to configure AE:

* environment variables
* system properties
* `gravitee.yml`

The order in which they are listed above corresponds to their order of precedence. In other words, environment variables override the other two configuration types, and system properties override `gravitee.yml`.

## Prerequisites

Before configuring Alert Engine, ensure the following:

* Gravitee license key file (for cluster mode)
* Docker runtime (for cluster deployment and integration tests)
* Hazelcast configuration file at `${gravitee.home}/config/hazelcast.xml` (or custom path)
* Alert Engine version 3.0.0 or later (for timestamp-based scheduling)

## Configure AE via the `gravitee.yml` file

The `gravitee.yml` file, found in `GRAVITEE_HOME/config/`, is the default way to configure AE.

{% hint style="info" %}
Be aware of sensitivities

YAML (`yml`) format is very sensitive to indentation. Ensure you include the correct number of spaces and use spaces instead of tabs.
{% endhint %}

Please see the example below:

```
############################################################################################################
################################## Gravitee Alert Engine - Configuration ################################
############################################################################################################

############################################################################################################







ingesters:
  ws:













    authentication: # authentication type to be used for HTTP authentication
      type: basic # none to disable authentication / basic for basic authentication
      users:
        admin: adminadmin



services:
  core:
    http:
      enabled: true
      port: 18072
      host: localhost
      authentication:
        # authentication type to be used for the core services
        # - none : to disable authentication
        # - basic : to use basic authentication
        # default is "basic"
        type: basic
        users:
          admin: adminadmin
  metrics:
    enabled: false
    prometheus:
      enabled: true

cluster:
  # Frequency at which Alert Engine will register the latest state of dampenings and buckets
  sync:
    time:
      value: 30
      unit: SECONDS

  hazelcast:
    config:
      path: ${gravitee.home}/config/hazelcast.xml
```

### Cluster Synchronization

The following properties control cluster synchronization behavior:

| Property | Description | Example |
|:---------|:------------|:--------|
| `cluster.sync.time.value` | Sync interval between cluster nodes | `30` |
| `cluster.sync.time.unit` | Time unit for sync interval | `SECONDS` |
| `cluster.hazelcast.config.path` | Path to Hazelcast configuration file | `${gravitee.home}/config/hazelcast.xml` |
| `cluster.hazelcast.systemProperties` | Hazelcast system properties (without `hazelcast.` prefix) | _(optional map)_ |

### WebSocket Connector Filters

The WebSocket connector applies default filters (e.g., installation ID constraints) to alert events. Administrators can disable these filters via configuration to allow cross-installation alert routing or custom filtering logic.

{% hint style="warning" %}
Default filters are enabled by default. Disabling them may allow cross-installation alert routing.
{% endhint %}

| Property | Description | Example |
|:---------|:------------|:--------|
| `alerts.alert-engine.ws.defaultFilters.enabled` | Enable default filters (e.g., installation ID constraint) | `true` |

## System properties

You can override the default `gravitee.yml` configuration by defining system properties.

To override this property:

```
cluster:
  sync:
    time:
      value: 30
```

Add this property to the JVM:

```
-Dcluster.sync.time.value=50
```

## Environment variables

You can override the default `gravitee.yml` configuration and system properties by defining environment variables.

To override this property:

```
cluster:
  sync:
    time:
      value: 30
```

Define one of the following variables:

```
GRAVITEE_CLUSTER_SYNC_TIME_VALUE=30
GRAVITEE.CLUSTER.SYNC.TIME.VALUE=30
gravitee_cluster_sync_time_value=30
gravitee.cluster.sync.time.value=30
```

{% hint style="info" %}
**Case sensitivities**

Some properties are case sensitive and cannot be written in upper case (for example, `gravitee_security_providers_0_tokenIntrospectionEndpoint`). We advise you to define environment variables in lower case. Ensure you use the correct syntax for each property.
{% endhint %}

{% hint style="info" %}
**Hyphen sensitivities**

In some systems, hyphens are not allowed in variable names. You can replace them with another character such as an underscore (for example, `gravitee_policy_apikey_header` instead of `gravitee_policy_api-key_header`).
{% endhint %}

### Docker Compose Environment

The following environment variables control Docker Compose cluster deployments:

| Variable | Description | Example |
|:---------|:------------|:--------|
| `LICENCE_KEY_PATH` | Absolute path to the Gravitee license key file | `/path/to/license.key` |
| `AE_VERSION` | AE Docker image version | `latest` |
| `AE_REPLICAS` | Number of AE nodes in the cluster | `2` |
| `CONTAINER_CPUS` | CPU limit per container | `1` |
| `CONTAINER_MEMORY` | Memory limit per container | `768M` |
| `GIO_MIN_MEM` | JVM minimum heap size | `256m` |
| `GIO_MAX_MEM` | JVM maximum heap size | `512m` |

### Helm Chart Parameters

The following properties control Alert Engine behavior when deployed via Helm:

| Property | Description | Example |
|:---------|:------------|:--------|
| `alerts.api.ws.defaultFilters.enabled` | Enable or disable Alert Engine default filters through the APIM Rest API | `true` |

## Creating a Cluster Deployment

Deploy a cluster by configuring the Docker Compose environment variables in `.env` and running `docker-compose up`:

1. Set `LICENCE_KEY_PATH` to your license file location.
2. Define `AE_REPLICAS` to specify the number of nodes (default: 2).
3. Adjust `CONTAINER_CPUS`, `CONTAINER_MEMORY`, `GIO_MIN_MEM`, and `GIO_MAX_MEM` based on workload requirements.
4. Ensure the Hazelcast configuration file exists at the path specified in `cluster.hazelcast.config.path`.

On startup, each node logs its role (PRIMARY or REPLICA) and cluster size. Membership changes (joins/leaves) are logged with node addresses.

## Updating a Scheduled Alert

When updating a scheduled alert with a duration-based condition, the evaluation schedule resets. The next cycle starts from the moment you confirm the update. If the anchor timestamp (`updatedAt` or `createdAt`) is in the future, the engine falls back to scheduling from the current time. Negative initial delays result in immediate scheduling.
