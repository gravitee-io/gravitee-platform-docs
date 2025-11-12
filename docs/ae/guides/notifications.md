---
description: This article walks through how to configure Alert Engine notifications
---

# Notifications

## Introduction

When you create an alert in Alert Engine (AE), you can choose to be notified through your preferred channel with one of the provided _notifiers_.

Notifiers are a type of plugin used to configure a notification for a recipient. AE includes four notifiers:

* Email
* System email
* Slack
* Webhook

Please refer to the [alerts documentation](/apim/getting-started/configuration/notifications#configure-alerts) to learn how to configure AE-driven alerts and notifications.

This article walks through how to configure notifications via these channels as well as how to:

* Create custom messages
* Configure certain notification properties

## Create a custom message

AE includes a number of custom properties for building the most informative notification possible. You can access these properties with the [Freemarker](https://freemarker.apache.org/docs/ref.html) language (with the notation `${my.property}`).

### Common properties

These properties are available regardless of the alert type.

| Key                             | Description                                                                                                                   |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `alert.id`                      | UUID of the alert                                                                                                             |
| `alert.name`                    | Name of the alert                                                                                                             |
| `alert.severity`                | Severity of the alert: `info`, `warning`, `critical`                                                                          |
| `alert.source`                  | Source of the alert: `NODE_HEARTBEAT`, `NODE_HEALTHCHECK`, `ENDPOINT_HEALTH_CHECK`, `REQUEST`                                 |
| `alert.description`             | Description of the alert                                                                                                      |
| `alert.conditions[]`            | Array of conditions. Each condition contains specific fields.                                                                 |
| `notification.timestamp`        | Timestamp (long value) of the trigger                                                                                         |
| `notification.message`          | A human readable message relating to the alert condition                                                                      |
| `notification.result.value`     | Used for retrieving the computed value when defining an aggregation-based condition (for example, rate, aggregation)          |
| `notification.result.threshold` | Used for retrieving the defined threshold value when defining an aggregation-based condition (for example, rate, aggregation) |

### Specific properties

Depending on the rules you configure, you may have access to additional properties. These properties depend on the type of event being processed by AE.

You can access these properties using the following syntax: `${notification.properties['property_name\']}`.

| Scope    | Category     | Rules                                                                                                                                                                                                                                                                                                                                |
| -------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Platform | Node         | <ul><li>Alert when the lifecycle status of a node has changed</li><li>Alert when a metric of the node validates a condition</li><li>Alert when the aggregated value of a node metric passes a threshold</li><li>Alert when the rate of a given condition passes a threshold</li><li>Alert on the health status of the node</li></ul> |
| Platform | API Metrics  | <ul><li>Alert when a metric of the request validates a condition</li><li>Alert when the aggregated value of a request metric passes a threshold</li><li>Alert when the rate of a given condition passes a threshold</li></ul>                                                                                                        |
| API      | API Metrics  | <ul><li>Alert when a metric of the request validates a condition</li><li>Alert when the aggregated value of a request metric passes a threshold</li><li>Alert when the rate of a given condition passes a threshold</li></ul>                                                                                                        |
| API      | Health Check | <ul><li>Alert when the health status of an endpoint has changed</li></ul>                                                                                                                                                                                                                                                            |

## Notification properties

There are different notification properties based on the specific kind of notification events. Please see the below sections for more details.

### NODE\_LIFECYCLE events

2.1.2

The following table lists the properties available in every alert triggered by a `NODE_LIFECYCLE` event.

| Key                | Description                                                                                                  | Syntax                                          |
| ------------------ | ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------- |
| `node.hostname`    | Alerting node hostname                                                                                       | ${notification.properties\['node.hostname']}    |
| `node.application` | Alerting node application (`gio-apim-gateway`, `gio-apim-management`, `gio-am-gateway`, `gio-am-management`) | ${notification.properties\['node.application']} |
| `node.id`          | Alerting node UUID                                                                                           | ${notification.properties\['node.id']}          |
| `node.event`       | Lifecycle state, possible values: `NODE_START`, `NODE_STOP`                                                  | ${notification.properties\['node.event']}       |

### Notification properties for NODE\_HEARTBEAT event

The following table lists the properties available in every alert triggered by a `NODE_HEARTBEAT` event.

| Key                         | Description                                                                                                  | Syntax                                                   |
| --------------------------- | ------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------- |
| `node.hostname`             | Alerting node hostname                                                                                       | ${notification.properties\['node.hostname']}             |
| `node.application`          | Alerting node application (`gio-apim-gateway`, `gio-apim-management`, `gio-am-gateway`, `gio-am-management`) | ${notification.properties\['node.application']}          |
| `node.id`                   | Alerting note UUID                                                                                           | ${notification.properties\['node.id']}                   |
| `os.cpu.percent`            | CPU percentage used                                                                                          | ${notification.properties\['os.cpu.percent']}            |
| `os.cpu.average.0`          | CPU load average over 1 minute, if available                                                                 | ${notification.properties\['os.cpu.average.0']}          |
| `os.cpu.average.1`          | CPU load average over 5 minutes, if available                                                                | ${notification.properties\['os.cpu.average.1']}          |
| `os.cpu.average.2`          | CPU load average over 15 minutes, if available                                                               | ${notification.properties\['os.cpu.average.2']}          |
| `process.fd.open`           | Number of open file descriptors                                                                              | ${notification.properties\['process.fd.open']}           |
| `process.fd.max`            | Maximum number of open file descriptors                                                                      | ${notification.properties\['process.fd.max']}            |
| `process.cpu.percent`       | CPU percentage used by the process                                                                           | ${notification.properties\['process.cpu.percent']}       |
| `process.cpu.total`         | Total CPU time of the process                                                                                | ${notification.properties\['process.cpu.total']}         |
| `process.mem.virtual.total` | Total virtual memory of the process                                                                          | ${notification.properties\['process.mem.virtual.total']} |
| `jvm.uptime`                | Uptime of the Java Virtual Machine.                                                                          | ${notification.properties\['jvm.uptime']}                |
| `jvm.threads.count`         | Number of live threads of the Java process                                                                   | ${notification.properties\['jvm.threads.count']}         |
| `jvm.threads.peak`          | Peak number of live threads of the Java process                                                              | ${notification.properties\['jvm.threads.peak']}          |
| `jvm.mem.heap.used`         | Memory used, in bytes                                                                                        | ${notification.properties\['jvm.mem.heap.used']}         |
| `jvm.mem.heap.max`          | Maximum memory that can be used, in bytes                                                                    | ${notification.properties\['jvm.mem.heap.max']}          |
| `jvm.mem.heap.percent`      | Ratio between the used heap and the max heap                                                                 | ${notification.properties\['jvm.mem.heap.percent']}      |

### Notification properties for NODE\_HEALTHCHECK event

The following table lists the properties available in every alert triggered by a `NODE_HEALTHCHECK` event.

| Key                                        | Description                                                                                                  | Syntax                                                                             |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| `node.hostname`                            | Alerting node hostname                                                                                       | ${notification.properties\['node.hostname']}                                       |
| `node.application`                         | Alerting node application (`gio-apim-gateway`, `gio-apim-management`, `gio-am-gateway`, `gio-am-management`) | ${notification.properties\['node.application']}                                    |
| `node.id`                                  | Alerting node UUID                                                                                           | ${notification.properties\['node.id']}                                             |
| `node.healthy`                             | Global health of the node, possible values: `true` or `false`                                                | ${notification.properties\['node.healthy']?string('yes','no')}                     |
| `node.probe.repository-analytics`          | Health of a dedicated probe, possible values: `true` or `false`                                              | ${notification.properties\['node.probe.repository-analytics']?string('yes','no')}  |
| `node.probe.repository-analytics.message`  | If `node.probe.repository-analytics` is false, contains the error message                                    | ${notification.properties\['node.probe.repository-analytics.message']}             |
| `node.probe.management-repository`         | Health of a dedicated probe, possible values: `true` or `false`                                              | ${notification.properties\['node.probe.management-repository']?string('yes','no')} |
| `node.probe.management-repository.message` | If `node.probe.management-repository` is false, contains the error message                                   | ${notification.properties\['node.probe.management-repository.message']}            |
| `node.probe.management-api`                | Health of a dedicated probe, values: `true` or `false`                                                       | ${notification.properties\['node.probe.management-api']?string('yes','no')}        |
| `node.probe.management-api.message`        | If `node.probe.management-api` is false, contains the error message                                          | ${notification.properties\['node.probe.management-api.message']}                   |

\\
