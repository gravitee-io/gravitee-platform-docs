---
description: Use Alert Engine and API Management 4.11 together to configure notifications for your alerts. Follow the steps to set them up.
---

# Configure Notifications

## Introduction

You can use Gravitee Alert Engine (AE) and Gravitee API Management (APIM) together to configure notifications for your AE alerts. This article explains:

* Request notifications
* Health check notifications

## Request notifications

This page lists the properties available in all alerts triggered by a `REQUEST` event.

### Properties

The notification properties are values which have been sent or computed while processing the event by AE. These are just the basic properties; you can’t use them to retrieve more information about a particular object like the `api` or the `application` .

| Key                                  | Description                                                                                                  | Syntax                                                              | Processor |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------- | --------- |
| `node.hostname`                      | Alerting node hostname                                                                                       | ${notification.properties\['node.hostname']}                        | -         |
| `node.application`                   | Alerting node application (`gio-apim-gateway`, `gio-apim-management`, `gio-am-gateway`, `gio-am-management`) | ${notification.properties\['node.application']}                     | -         |
| `node.id`                            | Alerting node UUID                                                                                           | ${notification.properties\['node.id']}                              | -         |
| `gateway.port`                       | Gateway port                                                                                                 | ${notification.properties\['gateway.port']}                         | -         |
| `tenant`                             | Tenant of the node (if one exists)                                                                           | ${notification.properties\['tenant']}                               | -         |
| `request.id`                         | Request ID                                                                                                   | ${notification.properties\['request.id']}                           | -         |
| `request.content_length`             | Request content length in bytes                                                                              | ${notification.properties\['request.content\_length']}              | -         |
| `request.ip`                         | Request IP address                                                                                           | ${notification.properties\['request.ip']}                           | -         |
| `request.ip.country_iso_code`        | Country ISO code associated with the IP address                                                              | ${notification.properties\['request.ip.country\_iso\_code']}        | geoip     |
| `request.ip.country_name`            | Country name associated with the IP address                                                                  | ${notification.properties\['request.ip.country\_name']}             | geoip     |
| `request.ip.continent_name`          | Continent name associated with the IP address                                                                | ${notification.properties\['request.ip.continent\_name']}           | geoip     |
| `request.ip.region_name`             | Region name associated with the IP address                                                                   | ${notification.properties\['request.ip.region\_name']}              | geoip     |
| `request.ip.city_name`               | City name associated with the IP address                                                                     | ${notification.properties\['request.ip.city\_name']}                | geoip     |
| `request.ip.timezone`                | Timezone associated with the IP address                                                                      | ${notification.properties\['request.ip.timezone']}                  | geoip     |
| `request.ip.lat`                     | Latitude associated with the IP address                                                                      | ${notification.properties\['request.ip.lat']}                       | geoip     |
| `request.ip.lon`                     | Longitude associated with the IP address                                                                     | ${notification.properties\['request.ip.lon']}                       | geoip     |
| `request.user_agent`                 | Request user agent                                                                                           | ${notification.properties\['request.user\_agent']}                  | -         |
| `request.user_agent.device_class`    | Device class of the user agent                                                                               | ${notification.properties\['request.user\_agent.device\_class']}    | useragent |
| `request.user_agent.device_brand`    | Device brand of the user agent                                                                               | ${notification.properties\['request.user\_agent.device\_brand']}    | useragent |
| `request.user_agent.device_name`     | Device name of the user agent                                                                                | ${notification.properties\['request.user\_agent.device\_name']}     | useragent |
| `request.user_agent.os_class`        | OS class of the user agent                                                                                   | ${notification.properties\['request.user\_agent.os\_class']}        | useragent |
| `request.user_agent.os_name`         | OS name of the user agent                                                                                    | ${notification.properties\['request.user\_agent.os\_name']}         | useragent |
| `request.user_agent.os_version`      | OS version of the user agent                                                                                 | ${notification.properties\['request.user\_agent.os\_version']}      | useragent |
| `request.user_agent.browser_name`    | Browser name of the user agent                                                                               | ${notification.properties\['request.user\_agent.browser\_name']}    | useragent |
| `request.user_agent.browser_version` | Browser version of the user agent                                                                            | ${notification.properties\['request.user\_agent.browser\_version']} | useragent |
| `user` | Request user. JWT and OAuth2 plans set it from the token's user claim, and the Basic Authentication and WS-Security Authentication policies set it from the username. API Key and Keyless plans don't set it, so on those plans it's empty unless one of these policies runs in the API's flows. | ${notification.properties\['user']}                                 | -         |
| `api`                                | Request API                                                                                                  | ${notification.properties\['api']}                                  | -         |
| `application`                        | Request application                                                                                          | ${notification.properties\['application']}                          | -         |
| `plan`                               | Request plan                                                                                                 | ${notification.properties\['plan']}                                 | -         |
| `response.status`                    | Response status                                                                                              | ${notification.properties\['response.status']}                      | -         |
| `response.latency`                   | Response latency                                                                                             | ${notification.properties\['response.latency']}                     | -         |
| `response.response_time`             | Response time                                                                                                | ${notification.properties\['response.response\_time']}              | -         |
| `response.content_length`            | Response content length                                                                                      | ${notification.properties\['response.content\_length']}             | -         |
| `response.upstream_response_time`    | Upstream response time (the time between the Gateway and the backend)                                        | ${notification.properties\['response.upstream\_response\_time']}    | -         |
| `quota.counter` | Quota counter state. Only the Quota policy sets it. The Rate Limit policy doesn't. | ${notification.properties\['quota.counter']}                        | -         |
| `quota.limit` | Quota limit. Only the Quota policy sets it, with the value of **Max requests (static)**, so it reads `0` when the policy uses **Max requests (dynamic)**. The Rate Limit policy doesn't set it. | ${notification.properties\['quota.limit']}                          | -         |
| `error.key` | Key that identifies the root cause of an error the gateway records itself, for example a security or plan rejection, a policy interruption, a timeout, or a failed connection to the backend. It's never taken from the backend's HTTP status, so when the backend itself answers with a `4xx` or `5xx` status, `response.status` is set and `error.key` is empty. When a response template matches the error, `error.key` stays empty unless **Add template key to logs** is enabled on that template. The request's log details show the same key. | ${notification.properties\['error.key']}                            | -         |

### Data

Data (or `resolved data`) consists of specific objects which have been resolved from the notification properties. For example, in the case of the `REQUEST` event, AE tries to resolve `api`, `app` , and `plan` to provide more contextualized information to define your message templates.

#### API data

For the `api`, you can access the following data:

| Key                        | Description                     | Syntax                             |
| -------------------------- | ------------------------------- | ---------------------------------- |
| `id`                       | API identifier                  | ${api.id}                          |
| `name`                     | API name                        | ${api.name}                        |
| `version`                  | API version                     | ${api.version}                     |
| `description`              | API description                 | ${api.description}                 |
| `primaryOwner.email`       | API primary owner email address | ${api.primaryOwner.email}          |
| `primaryOwner.displayName` | API primary owner display name  | ${api.primaryOwner.displayName}    |
| `tags`                     | API sharding tags               | ${api.tags}                        |
| `labels`                   | API labels                      | ${api.labels}                      |
| `views`                    | API views                       | ${api.views}                       |
| `metadata`                 | API metadata                    | ${api.metadata\['metadata\_name']} |

#### Application

For the `application`, you can access the following data:

| Key                        | Description                            | Syntax                                  |
| -------------------------- | -------------------------------------- | --------------------------------------- |
| `id`                       | Application identifier                 | ${application.id}                       |
| `name`                     | Application name                       | ${application.name}                     |
| `description`              | Application description                | ${application.description}              |
| `status`                   | Application status                     | ${application.status}                   |
| `type`                     | Application type                       | ${application.type}                     |
| `owner.email`              | Application primary owner email address | ${application.owner.email}              |
| `owner.displayName`        | Application primary owner display name | ${application.owner.displayName}        |

These fields are only filled when the request comes through an application's subscription. On a Keyless plan, `${application.name}` reads `Unknown application (keyless)` and the other fields aren't set.

#### Plan

For the `plan`, you can access the following data:

| Key           | Description      | Syntax              |
| ------------- | ---------------- | ------------------- |
| `id`          | Plan identifier  | ${plan.id}          |
| `name`        | Plan name        | ${plan.name}        |
| `description` | Plan description | ${plan.description} |

## Health-check notifications

This page lists the properties available in all alerts triggered by an `ENDPOINT_HEALTHCHECK` event.

### Properties

The notification properties are values which have been sent or computed while processing the event by AE. These are just the basic properties, you can’t use them to retrieve more information about a particular object like the `api` or the `application` (to achieve this, see the [data](configure-notifications.md#data-1) section).

| Key                | Description                                                                                                  | Syntax                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------- |
| `node.hostname`    | Alerting node hostname                                                                                       | ${notification.properties\['node.hostname']}              |
| `node.application` | Alerting node application (`gio-apim-gateway`, `gio-apim-management`, `gio-am-gateway`, `gio-am-management`) | ${notification.properties\['node.application']}           |
| `node.id`          | Alerting node UUID                                                                                           | ${notification.properties\['node.id']}                    |
| `response_time`    | Endpoint response time in ms                                                                                 | ${notification.properties\['response\_time']}             |
| `tenant`           | Tenant of the node (if one exists)                                                                           | ${notification.properties\['tenant']}                     |
| `api`              | The API Id of the healthcheck.                                                                               | ${notification.properties\['api']}                        |
| `endpoint.name`    | The endpoint name.                                                                                           | ${notification.properties\['endpoint.name']}              |
| `status.old`       | Values: `UP`, `DOWN`, `TRANSITIONALLY_UP`, `TRANSITIONALLY_DOWN`.                                            | ${notification.properties\['status.old']}                 |
| `status.new`       | Values: `UP`, `DOWN`, `TRANSITIONALLY_UP`, `TRANSITIONALLY_DOWN`.                                            | ${notification.properties\['status.new']}                 |
| `success`          | Values: `true` or `false`.                                                                                   | ${notification.properties\['success']?string('yes','no')} |
| `message`          | If `success` is `false`, contains the error message.                                                         | ${notification.properties\['message']}                    |

### Data

Data (or `resolved data`) consists of specific objects which have been resolved from the notification properties. For example, in the case of the `ENDPOINT_HEALTHCHECK` event, AE tries to resolve `api` to provide more contextualized information to define your message templates.

#### API

For the `api`, you can access the following data:

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
