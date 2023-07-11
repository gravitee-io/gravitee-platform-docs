---
description: >-
  This article walks through how to configure alert Engine notifications in
  Gravitee API Management
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
| `user`                               | Request user                                                                                                 | ${notification.properties\['user']}                                 | -         |
| `api`                                | Request API                                                                                                  | ${notification.properties\['api']}                                  | -         |
| `application`                        | Request application                                                                                          | ${notification.properties\['application']}                          | -         |
| `plan`                               | Request plan                                                                                                 | ${notification.properties\['plan']}                                 | -         |
| `response.status`                    | Response status                                                                                              | ${notification.properties\['response.status']}                      | -         |
| `response.latency`                   | Response latency                                                                                             | ${notification.properties\['response.latency']}                     | -         |
| `response.response_time`             | Response time                                                                                                | ${notification.properties\['response.response\_time']}              | -         |
| `response.content_length`            | Response content length                                                                                      | ${notification.properties\['response.content\_length']}             | -         |
| `response.upstream_response_time`    | Upstream response time (the time between the gateway and the backend)                                        | ${notification.properties\['response.upstream\_response\_time']}    | -         |
| `quota.counter`                      | Quota counter state                                                                                          | ${notification.properties\['quota.counter']}                        | -         |
| `quota.limit`                        | Quota limit                                                                                                  | ${notification.properties\['quota.limit']}                          | -         |
| `error.key`                          | Key for identify the root cause of error                                                                     | ${notification.properties\['error.key']}                            | -         |

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
| `primaryOwner.email`       | Application description                | ${application.primaryOwner.email}       |
| `primaryOwner.displayName` | Application primary owner display name | ${application.primaryOwner.displayName} |

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

The notification properties are values which have been sent or computed while processing the event by AE. These are just the basic properties, you can’t use them to retrieve more information about a particular object like the `api` or the `application` (to achieve this, see the [data](https://docs.gravitee.io/ae/apim\_notification\_endpoint\_healthcheck.html#data) section).

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

\
