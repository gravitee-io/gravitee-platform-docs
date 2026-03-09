---
description: This article walks through how to configure Alert Engine
---

# Configure Alert Engine

## Introduction

There are three different methods to configure Alert Engine (AE):

* environment variables
* system properties
* `gravitee.yml`

Environment variables overrride system properties, and  environement variables override the `gravitee.yml` file.

## Configure AE via the `gravitee.yml` file

The `gravitee.yml` file is the default way to configure AE.

{% hint style="info" %}
The YAML (`yml`) format is sensitive to indentation. Ensure you include the correct number of spaces for each line.
{% endhint %}

Here is an example with the correct indentation:

```
############################################################################################################
################################## Gravitee Alert Engine - Configuration ################################
############################################################################################################

############################################################################################################
# This file is the general configuration of Gravitee Alert Engine:
# - Properties (and respective default values) in comment are provided for information.
# - You can reference other property by using ${property.name} syntax
# - gravitee.home property is automatically set-up by launcher and refers to the installation path. Do not override it !
#
############################################################################################################

# Ingesters
ingesters:
  ws:
#    instances: 0
#    port: 8072
#    host: 0.0.0.0
#    secured: false
#    alpn: false
#    ssl:
#      clientAuth: false
#      keystore:
#        path: ${gravitee.home}/security/keystore.jks
#        password: secret
#      truststore:
#        path: ${gravitee.home}/security/truststore.jks
#        password: secret
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

## System properties

You can override the default `gravitee.yml` configuration by defining system properties.

To override the following property:

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

By defining environment variables, you can override the default `gravitee.yml` configuration and system properties.

To override the following property:

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

* Some properties are case sensitive and cannot be written in upper case. For example, `gravitee_security_providers_0_tokenIntrospectionEndpoint`. To avoid this issue, define environment variables in lower case and ensure you use the correct syntax for each property.

* In some systems, hyphens are not allowed in variable names. You can replace hyphens with another character such as an underscore. For example, `gravitee_policy_apikey_header` instead of `gravitee_policy_api-key_header`).
{% endhint %}

## Cluster deployment

Alert Engine supports cluster deployment with Hazelcast-based synchronization. Cluster mode enables multi-tenant deployments where each alert maintains an independent, predictable evaluation schedule.

{% hint style="info" %}
Cluster mode requires a valid Gravitee Enterprise Edition license.
{% endhint %}

### Prerequisites

Before configuring cluster mode, ensure you meet the following requirements:

* You have a Gravitee Enterprise Edition license key.
* Your Hazelcast configuration file at `${gravitee.home}/config/hazelcast.xml` or a custom path.
* For production clusters, you have a static IP addresses or hostnames for all Alert Engine nodes.
* For default filters, Alert Engine Connectors WS version 2.3.0 or later.
* For for schedule anchoring, Alert API version 3.0.0 or later.

### Cluster synchronization

Alert Engine nodes form a Hazelcast cluster with one PRIMARY node and zero or more REPLICA nodes. Nodes synchronize trigger state every 30 seconds by default. The cluster uses multicast discovery by default. Production deployments should configure TCP-IP with explicit member addresses. Each node logs its role (PRIMARY or REPLICA) at startup and when cluster membership changes.

Configure cluster synchronization behavior in `gravitee.yml`:

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `cluster.sync.time.value` | integer | `30` | Interval between cluster node synchronization |
| `cluster.sync.time.unit` | string | `SECONDS` | Time unit for sync interval |
| `cluster.hazelcast.config.path` | string | `${gravitee.home}/config/hazelcast.xml` | Path to Hazelcast XML configuration |

**Example configuration:**

```yaml
cluster:
  sync:
    time:
      value: 30
      unit: SECONDS
  hazelcast:
    config:
      path: ${gravitee.home}/config/hazelcast.xml
```

### Hazelcast cluster configuration

Alert Engine uses Hazelcast for cluster coordination. The cluster name is `graviteeio-ae`.

**Discovery modes:**

* **Multicast (default):** Works out-of-box on same network
* **TCP-IP (production):** Requires explicit member IP addresses

**Example TCP-IP configuration** (`hazelcast.xml`):

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

### Cluster role logging

Alert Engine logs cluster role information at startup and when cluster membership changes:

```
INFO  c.g.a.c.hz.HazelcastClusterManager - Local node [[172.25.0.2]:5701] role is PRIMARY (cluster size: 1)
INFO  c.g.a.c.hz.HazelcastClusterManager - A node has joined the cluster: MembershipEvent {...}
INFO  c.g.a.c.hz.HazelcastClusterManager - Local node [[172.25.0.2]:5701] role is PRIMARY (cluster size: 2)
INFO  c.g.a.c.hz.HazelcastClusterManager - Local node [[172.25.0.3]:5701] role is REPLICA (cluster size: 2)
```

### Docker Compose environment variables

Configure Docker Compose deployments using the following environment variables:

| Variable | Description | Example |
|:---------|:------------|:--------|
| `LICENCE_KEY_PATH` | Absolute path to Gravitee license key file | `/path/to/license.key` |
| `AE_VERSION` | Alert Engine Docker image version | `latest` |
| `AE_REPLICAS` | Number of Alert Engine nodes in cluster | `2` |
| `CONTAINER_CPUS` | CPU limit per container | `1` |
| `CONTAINER_MEMORY` | Memory limit per container | `768M` |
| `GIO_MIN_MEM` | JVM minimum heap size | `256m` |
| `GIO_MAX_MEM` | JVM maximum heap size | `512m` |

## Default filters

When enabled, the Alert Engine WebSocket connector automatically adds an installation ID filter to all triggers. This ensures triggers only evaluate events from their originating Gravitee installation in multi-tenant environments. The filter is applied transparently during trigger registration if an installation ID is available in the context.

Configure default filter behavior in `gravitee.yml`:

**Alert Engine WebSocket connector:**

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `alerts.alert-engine.ws.defaultFilters.enabled` | boolean | `true` | Enable/disable automatic installation ID filter on triggers |

**APIM REST API (Helm chart):**

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `alerts.api.ws.defaultFilters.enabled` | boolean | `true` | Enable/disable Alert Engine default filters through APIM REST API |
