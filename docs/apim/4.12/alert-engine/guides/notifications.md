---
description: Choose the channel Alert Engine notifies you through when an alert fires in API Management 4.12. Compare the providers available.
---

# Notifications

## Introduction

When you create an alert in Alert Engine (AE), you can choose to be notified through your preferred channel via one of the provided _notifiers_.

Notifiers are plugins used to configure notifications for recipients. AE includes four notifiers:

* Email
* System email
* Slack
* Webhook

Please refer to the [alerts documentation](https://documentation.gravitee.io/apim/getting-started/configuration/notifications#configure-alerts) to learn how to configure AE-driven alerts and notifications.

This article describes how to configure notifications using these channels, as well as how to:

* Create custom messages
* Configure certain notification properties

## Create a custom message

AE includes custom properties to build the most informative notification possible. You can access these properties with the [Freemarker](https://freemarker.apache.org/docs/ref.html) language (with the notation `${my.property}`).

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

In `alert.conditions[]`, the `[]` only marks the value as a list. It isn't valid FreeMarker: a template that contains `${alert.conditions[]}` fails to render, and that notification isn't sent. Read a condition's fields by its position in the list instead:

```
${(alert.conditions[0].property)!}
${(alert.conditions[0].operator)!}
${(alert.conditions[0].threshold)!}
${(alert.conditions[0].pattern)!}
```

The fields depend on the condition's type: `property`, `operator`, and `threshold` for a threshold, `property`, `operator`, and `pattern` for a string match, and `threshold`, `duration`, and `timeUnit` for a rate or an aggregation. For a readable summary of the condition that triggered the alert, use `${(notification.message)!}`. Alerts on missing data don't have one.

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

There are different notification properties for different kinds of notification events. Please see the sections below for more details.

### NODE\_LIFECYCLE events

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

### Notification properties for REQUEST event

The following table lists the properties available in every alert triggered by a `REQUEST` event.

<table><thead><tr><th width="248.12109375">Key</th><th width="216.05859375">Description</th><th width="190.4375">Syntax</th><th>Processor</th></tr></thead><tbody><tr><td><code>node.hostname</code></td><td>Alerting node hostname</td><td>${notification.properties['node.hostname']}</td><td>-</td></tr><tr><td><code>node.application</code></td><td>Alerting node application(<code>gio-apim-gateway</code>, <code>gio-apim-management</code>, <code>gio-am-gateway</code>, <code>gio-am-management</code>)</td><td>${notification.properties['node.application']}</td><td>-</td></tr><tr><td><code>node.id</code></td><td>Alerting node UUID</td><td>${notification.properties['node.id']}</td><td>-</td></tr><tr><td><code>gateway.port</code></td><td>Gateway port</td><td>${notification.properties['gateway.port']}</td><td>-</td></tr><tr><td><code>tenant</code></td><td>Tenant of the node (if one exists)</td><td>${notification.properties['tenant']}</td><td>-</td></tr><tr><td><code>request.id</code></td><td>Request ID</td><td>${notification.properties['request.id']}</td><td>-</td></tr><tr><td><code>request.content_length</code></td><td>Request content length in bytes</td><td>${notification.properties['request.content_length']}</td><td>-</td></tr><tr><td><code>request.ip</code></td><td>Request IP address</td><td>${notification.properties['request.ip']}</td><td>-</td></tr><tr><td><code>request.ip.country_iso_code</code></td><td>Country ISO code associated with the IP address</td><td>${notification.properties['request.ip.country_iso_code']}</td><td>geoip</td></tr><tr><td><code>request.ip.country_name</code></td><td>Country name associated with the IP address</td><td>${notification.properties['request.ip.country_name']}</td><td>geoip</td></tr><tr><td><code>request.ip.continent_name</code></td><td>Continent name associated with the IP address</td><td>${notification.properties['request.ip.continent_name']}</td><td>geoip</td></tr><tr><td><code>request.ip.region_name</code></td><td>Region name associated with the IP address</td><td>${notification.properties['request.ip.region_name']}</td><td>geoip</td></tr><tr><td><code>request.ip.city_name</code></td><td>City name associated with the IP address</td><td>${notification.properties['request.ip.city_name']}</td><td>geoip</td></tr><tr><td><code>request.ip.timezone</code></td><td>Timezone associated with the IP address</td><td>${notification.properties['request.ip.timezone']}</td><td>geoip</td></tr><tr><td><code>request.ip.lat</code></td><td>Latitude associated with the IP address</td><td>${notification.properties['request.ip.lat']}</td><td>geoip</td></tr><tr><td><code>request.ip.lon</code></td><td>Longitude associated with the IP address</td><td>${notification.properties['request.ip.lon']}</td><td>geoip</td></tr><tr><td><code>request.user_agent</code></td><td>Request user agent</td><td>${notification.properties['request.user_agent']}</td><td>-</td></tr><tr><td><code>request.user_agent.device_class</code></td><td>Device class of the user agent</td><td>${notification.properties['request.user_agent.device_class']}</td><td>useragent</td></tr><tr><td><code>request.user_agent.device_brand</code></td><td>Device brand of the user agent</td><td>${notification.properties['request.user_agent.device_brand']}</td><td>useragent</td></tr><tr><td><code>request.user_agent.device_name</code></td><td>Device name of the user agent</td><td>${notification.properties['request.user_agent.device_name']}</td><td>useragent</td></tr><tr><td><code>request.user_agent.os_class</code></td><td>OS class of the user agent</td><td>${notification.properties['request.user_agent.os_class']}</td><td>useragent</td></tr><tr><td><code>request.user_agent.os_name</code></td><td>OS name of the user agent</td><td>${notification.properties['request.user_agent.os_name']}</td><td>useragent</td></tr><tr><td><code>request.user_agent.os_version</code></td><td>OS version of the user agent</td><td>${notification.properties['request.user_agent.os_version']}</td><td>useragent</td></tr><tr><td><code>request.user_agent.browser_name</code></td><td>Browser name of the user agent</td><td>${notification.properties['request.user_agent.browser_name']}</td><td>useragent</td></tr><tr><td><code>request.user_agent.browser_version</code></td><td>Browser version of the user agent</td><td>${notification.properties['request.user_agent.browser_version']}</td><td>useragent</td></tr><tr><td><code>user</code></td><td>Request user. JWT and OAuth2 plans set it from the token's user claim, and the Basic Authentication and WS-Security Authentication policies set it from the username. API Key and Keyless plans don't set it, so on those plans it's empty unless one of these policies runs in the API's flows.</td><td>${notification.properties['user']}</td><td>-</td></tr><tr><td><code>api</code></td><td>Request API</td><td>${notification.properties['api']}</td><td>-</td></tr><tr><td><code>application</code></td><td>Request application</td><td>${notification.properties['application']}</td><td>-</td></tr><tr><td><code>plan</code></td><td>Request plan</td><td>${notification.properties['plan']}</td><td>-</td></tr><tr><td><code>response.status</code></td><td>Response status</td><td>${notification.properties['response.status']}</td><td>-</td></tr><tr><td><code>response.latency</code></td><td>Response latency</td><td>${notification.properties['response.latency']}</td><td>-</td></tr><tr><td><code>response.response_time</code></td><td>Response time</td><td>${notification.properties['response.response_time']}</td><td>-</td></tr><tr><td><code>response.content_length</code></td><td>Response content length</td><td>${notification.properties['response.content_length']}</td><td>-</td></tr><tr><td><code>response.upstream_response_time</code></td><td>Upstream response time (between gateway and backend)</td><td>${notification.properties['response.upstream_response_time']}</td><td>-</td></tr><tr><td><code>quota.counter</code></td><td>Quota counter state. Only the Quota policy sets it. The Rate Limit policy doesn't.</td><td>${notification.properties['quota.counter']}</td><td>-</td></tr><tr><td><code>quota.limit</code></td><td>Quota limit. Only the Quota policy sets it, with the value of <strong>Max requests (static)</strong>, so it reads <code>0</code> when the policy uses <strong>Max requests (dynamic)</strong>. The Rate Limit policy doesn't set it.</td><td>${notification.properties['quota.limit']}</td><td>-</td></tr><tr><td><code>error.key</code></td><td>Key that identifies the root cause of an error the gateway records itself, for example a security or plan rejection, a policy interruption, a timeout, or a failed connection to the backend. It's never taken from the backend's HTTP status, so when the backend itself answers with a <code>4xx</code> or <code>5xx</code> status, <code>response.status</code> is set and <code>error.key</code> is empty. When a response template matches the error, <code>error.key</code> stays empty unless <strong>Add template key to logs</strong> is enabled on that template. The request's log details show the same key.</td><td>${notification.properties['error.key']}</td><td>-</td></tr></tbody></table>

#### Data

Data (or `resolved data`) consists of specific objects which have been resolved from the notification properties. For example, in the case of the `REQUEST` event, AE tries to resolve `api`, `app` and `plan` to provide more contextualized information to define your message templates.

**API data**

For the `api` data, you can access the following data:

| Key                        | Description                    | Syntax                             |
| -------------------------- | ------------------------------ | ---------------------------------- |
| `id`                       | API identifier                 | ${api.id}                          |
| `name`                     | API name                       | ${api.name}                        |
| `version`                  | API version                    | ${api.version}                     |
| `description`              | API description                | ${api.description}                 |
| `primaryOwner.email`       | API primary owner email        | ${api.primaryOwner.email}          |
| `primaryOwner.displayName` | API primary owner display name | ${api.primaryOwner.displayName}    |
| `tags`                     | API sharding tags              | ${api.tags}                        |
| `labels`                   | API labels                     | ${api.labels}                      |
| `views`                    | API views                      | ${api.views}                       |
| `metadata`                 | API metadata                   | ${api.metadata\['metadata\_name']} |

**Application data**

For the `application` data, you can access the following data:

| Key                        | Description                            | Syntax                                  |
| -------------------------- | -------------------------------------- | --------------------------------------- |
| `id`                       | Application identifier                 | ${application.id}                       |
| `name`                     | Application name                       | ${application.name}                     |
| `description`              | Application description                | ${application.description}              |
| `status`                   | Application status                     | ${application.status}                   |
| `type`                     | Application type                       | ${application.type}                     |
| `owner.email`              | Application primary owner email | ${application.owner.email}              |
| `owner.displayName`        | Application primary owner display name | ${application.owner.displayName}        |

These fields are only filled when the request comes through an application's subscription. On a Keyless plan, `${application.name}` reads `Unknown application (keyless)` and the other fields aren't set.

**Plan data**

For the `plan` data, you can access the following data:

| Key           | Description      | Syntax              |
| ------------- | ---------------- | ------------------- |
| `id`          | Plan identifier  | ${plan.id}          |
| `name`        | Plan name        | ${plan.name}        |
| `description` | Plan description | ${plan.description} |

### Notification properties for ENDPOINT\_HEALTHCHECK event

The following table lists the properties available in every alert triggered by an `ENDPOINT_HEALTHCHECK` event.

| Key                | Description                                                                                                  | Syntax                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------- |
| `node.hostname`    | Alerting node hostname                                                                                       | ${notification.properties\['node.hostname']}              |
| `node.application` | Alerting node application (`gio-apim-gateway`, `gio-apim-management`, `gio-am-gateway`, `gio-am-management`) | ${notification.properties\['node.application']}           |
| `node.id`          | Alerting node UUID                                                                                           | ${notification.properties\['node.id']}                    |
| `response_time`    | Endpoint response time in ms                                                                                 | ${notification.properties\['response\_time']}             |
| `tenant`           | Tenant of the node (if one exists)                                                                           | ${notification.properties\['tenant']}                     |
| `api`              | The API Id of the healthcheck                                                                                | ${notification.properties\['api']}                        |
| `endpoint.name`    | The endpoint name                                                                                            | ${notification.properties\['endpoint.name']}              |
| `status.old`       | Previous status: UP, DOWN, TRANSITIONALLY\_UP, TRANSITIONALLY\_DOWN                                          | ${notification.properties\['status.old']}                 |
| `status.new`       | New status: UP, DOWN, TRANSITIONALLY\_UP, TRANSITIONALLY\_DOWN                                               | ${notification.properties\['status.new']}                 |
| `success`          | Health check success, values: true or false                                                                  | ${notification.properties\['success']?string('yes','no')} |
| `message`          | Error message if success is false                                                                            | ${notification.properties\['message']}                    |

#### Data

Data (or `resolved data`) consists of specific objects which have been resolved from the notification properties. For example, in the case of the `ENDPOINT_HEALTHCHECK` event, AE tries to resolve `api` to provide more contextualized information to define your message templates.

**API**

For the `api` data, you can access the following data:

| Key                        | Description                    | Syntax                             |
| -------------------------- | ------------------------------ | ---------------------------------- |
| `id`                       | API identifier                 | ${api.id}                          |
| `name`                     | API name                       | ${api.name}                        |
| `version`                  | API version                    | ${api.version}                     |
| `description`              | API description                | ${api.description}                 |
| `primaryOwner.email`       | API primary owner email        | ${api.primaryOwner.email}          |
| `primaryOwner.displayName` | API primary owner display name | ${api.primaryOwner.displayName}    |
| `tags`                     | API sharding tags              | ${api.tags}                        |
| `labels`                   | API labels                     | ${api.labels}                      |
| `views`                    | API views                      | ${api.views}                       |
| `metadata`                 | API metadata                   | ${api.metadata\['metadata\_name']} |
