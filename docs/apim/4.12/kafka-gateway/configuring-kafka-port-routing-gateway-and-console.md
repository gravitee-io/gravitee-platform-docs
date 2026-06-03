# Configuring Kafka Port Routing (Gateway and Console)

## Prerequisites

Before configuring Kafka port routing, ensure the following requirements are met:

* Gateway version 4.12.0 or later
* Console version 4.12.0 or later
* Native Kafka API type (port routing does not apply to proxy or message APIs)
* `kafka.routingMode=port` configured in gateway settings
* `console.kafka.portRouting.enabled=true` configured in console settings

## Gateway Configuration

### Routing Mode

The `kafka.routingMode` property controls the routing strategy for Kafka APIs at the gateway level.

| Property | Description | Example |
|:---------|:------------|:--------|
| `kafka.routingMode` | Routing strategy: `host` for SNI-based routing or `port` for port-based routing. Defaults to `host` when unset or unrecognized. | `port` |

{% hint style="warning" %}
Plans without a configured bootstrap port are skipped in port routing mode and logged at WARN level. Port routing applies only to native Kafka APIs.
{% endhint %}

### Console Port Routing Toggle

The `console.kafka.portRouting.enabled` property controls the visibility of port routing fields in the Console UI.

| Property | Description | Example |
|:---------|:------------|:--------|
| `console.kafka.portRouting.enabled` | Environment-level toggle for Kafka port routing UI fields. When `false`, port fields are hidden even for native APIs. | `true` |

### Metrics Labels

The `services.metrics.labels` property configures user-defined labels for Vert.x metrics.

| Property | Description | Example |
|:---------|:------------|:--------|
| `services.metrics.labels` | User-configured Vert.x metrics labels passed to the metrics subsystem. | `["local", "remote"]` |

{% hint style="info" %}
When switching from port routing mode to host routing mode, clear the port fields on all plans (set to `null` or leave empty). The gateway reverts to SNI-based routing. Existing `kafka_port_ranges` data remains in the database but is unused.
{% endhint %}

{% hint style="danger" %}
**MongoDB Concurrency Limitation:** Without multi-document transactions enabled (requires a replica set or sharded cluster), two concurrent plan saves with overlapping port ranges may both succeed, leaving conflicting allocations. JDBC deployments prevent this via `SELECT ... FOR UPDATE` row-level locking.
{% endhint %}

{% hint style="danger" %}
**Broker Slot Overflow:** If the backend Kafka cluster has more brokers than the plan's port range supports, excess brokers are unmappable and logged as ERROR. Clients cannot reach those brokers.
{% endhint %}
