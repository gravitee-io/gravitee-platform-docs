---
description: Overview of Slack.
---

# Notification Channels

## Overview

AM provides the most common notification channels out of the box, including SMTP, webhooks, and Slack. These notification channels are called _notifiers_.

### Create a notification channel

To create a notification channel:

1. Log in to AM Console.
2. Click **Alerts > Notifiers**.
3. In the Notifiers page, click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Choose your notifier type and click **Next**.
5. Configure your notifier and click **Save**.

## Email

You can notify and alert administrators using the SMTP server.

### Create an email notification channel

1. Log in to AM Console.
2. Click **Settings > Alerts > Notifiers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **Email** as your notifier type and click **Next**.
5. Give your notifier a name.
6. Configure the settings.
7. Click **Create**.

{% hint style="info" %}
You can customize the default `body` text with notification properties.
{% endhint %}

#### Custom messages

When an alert triggers a notification, Alert Engine returns various properties to build the most informative notification possible. These properties are accessible through the FreeMarker language using the following syntax: `${my.property}`.

**Common properties**

These properties are available for all alert types.

| Key                             | Description                                                                                                                                       |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `alert.id`                      | The UUID of the alert.                                                                                                                            |
| `alert.name`                    | The name of the alert.                                                                                                                            |
| `alert.severity`                | The severity of the alert. Values: `info`, `warning`, `critical`. =                                                                               |
| `alert.source`                  | The source of the alert. Values: `NODE_HEARTBEAT`, `NODE_HEALTHCHECK`, `ENDPOINT_HEALTH_CHECK`, `REQUEST`.                                        |
| `alert.description`             | The description of the alert.                                                                                                                     |
| `notification.timestamp`        | The timestamp (long value) of the trigger.                                                                                                        |
| `notification.message`          | When defining an aggregation-based condition (such as rate or aggregation), displays a human readable message in relation to the alert condition. |
| `notification.result.value`     | When defining an aggregation-based condition (such as rate or aggregation), you can retrieve the computed value using this property.              |
| `notification.result.threshold` | When defining an aggregation-based condition (such as rate or aggregation), you can retrieve the defined threshold value using this property.     |
| `notification.properties`       | Notification properties (map). Values: `user`.                                                                                                    |

**Specific properties**

These properties vary depending on the rules configured and the type of event being processed by Alert Engine.

| Key                              | Description                                              |
| -------------------------------- | -------------------------------------------------------- |
| `environment`                    | Current environment with property `id`.                  |
| `organization`                   | Current organization with property `id`.                 |
| `domain`                         | Current security domain with properties `id` and `name`. |
| `application`                    | Current application with properties `id` and `name`.     |
| `user`                           | Current user principal `username`                        |
| `risk_assessment.unknownDevices` | Current assessment returned when a device is unknown.    |
| `risk_assessment.ipReputation`   | Current assessment for the IP reputation.                |
| `risk_assessment.geoVelocity`    | Current assessment for the geo velocity.                 |

## Webhook

You can notify and alert administrators using a webhook.

### Create a webhook notification channel

1. Log in to AM Console.
2. Click **Settings > Alerts > Notifiers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **Webhook** as your notifier type and click **Next**.
5. Give your notifier a name.
6. Configure the settings.
7. Click **Create**.

{% hint style="info" %}
You can customize the `request body` input text with notification properties.
{% endhint %}

#### Custom messages

When an alert triggers a notification, Alert Engine returns various properties to build the most informative notification possible. These properties are accessible through the FreeMarker language using the following syntax: `${my.property}`.

**Common properties**

These properties are available for all alert types.

| Key                             | Description                                                                                                                                       |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `alert.id`                      | The UUID of the alert.                                                                                                                            |
| `alert.name`                    | The name of the alert.                                                                                                                            |
| `alert.severity`                | The severity of the alert. Values: `info`, `warning`, `critical`. =                                                                               |
| `alert.source`                  | The source of the alert. Values: `NODE_HEARTBEAT`, `NODE_HEALTHCHECK`, `ENDPOINT_HEALTH_CHECK`, `REQUEST`.                                        |
| `alert.description`             | The description of the alert.                                                                                                                     |
| `notification.timestamp`        | The timestamp (long value) of the trigger.                                                                                                        |
| `notification.message`          | When defining an aggregation-based condition (such as rate or aggregation), displays a human readable message in relation to the alert condition. |
| `notification.result.value`     | When defining an aggregation-based condition (such as rate or aggregation), you can retrieve the computed value using this property.              |
| `notification.result.threshold` | When defining an aggregation-based condition (such as rate or aggregation), you can retrieve the defined threshold value using this property.     |
| `notification.properties`       | Notification properties (map). Values: `user`.                                                                                                    |

**Specific properties**

These properties vary depending on the rules configured and the type of event being processed by Alert Engine.

| Key                              | Description                                              |
| -------------------------------- | -------------------------------------------------------- |
| `environment`                    | Current environment with property `id`.                  |
| `organization`                   | Current organization with property `id`.                 |
| `domain`                         | Current security domain with properties `id` and `name`. |
| `application`                    | Current application with properties `id` and `name`.     |
| `user`                           | Current user principal `username`                        |
| `risk_assessment.unknownDevices` | Current assessment returned when a device is unknown.    |
| `risk_assessment.ipReputation`   | Current assessment for the IP reputation.                |
| `risk_assessment.geoVelocity`    | Current assessment for the geo velocity.                 |

## Slack

You can notify and alert administrators using [Slack](https://slack.com/).

### Register a new application in Slack

[Create and regenerate API tokens](https://slack.com/help/articles/215770388-Create-and-regenerate-API-tokens).

1. Open your [Slack apps](https://api.slack.com/apps).
2. Click an app or create a new one.
3. In the **Install App** section, click **Reinstall App**. Your new tokens appear at the top of the page.
4. Slack generates a token. Make a note of it for later use.

{% hint style="info" %}
For more information about Slack integration, see the Alert Engine Slack notifier documentation.
{% endhint %}

### Create a Slack notification channel

1. Log in to AM Console.
2. Click **Settings > Alerts > Notifiers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **Slack** as your notifier type and click **Next**.
5. Give your notifier a name.
6. Configure the settings (slack channel and slack token).
7. Click **Create**.

{% hint style="info" %}
You can customize the `message` input text with notification properties.
{% endhint %}

#### Custom messages

When an alert triggers a notification, Alert Engine returns various properties to build the most informative notification possible. These properties are accessible through the FreeMarker language using the following syntax: `${my.property}`.

**Common properties**

These properties are available for all alert types.

| Key                             | Description                                                                                                                                       |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `alert.id`                      | The UUID of the alert.                                                                                                                            |
| `alert.name`                    | The name of the alert.                                                                                                                            |
| `alert.severity`                | The severity of the alert. Values: `info`, `warning`, `critical`. =                                                                               |
| `alert.source`                  | The source of the alert. Values: `NODE_HEARTBEAT`, `NODE_HEALTHCHECK`, `ENDPOINT_HEALTH_CHECK`, `REQUEST`.                                        |
| `alert.description`             | The description of the alert.                                                                                                                     |
| `notification.timestamp`        | The timestamp (long value) of the trigger.                                                                                                        |
| `notification.message`          | When defining an aggregation-based condition (such as rate or aggregation), displays a human readable message in relation to the alert condition. |
| `notification.result.value`     | When defining an aggregation-based condition (such as rate or aggregation), you can retrieve the computed value using this property.              |
| `notification.result.threshold` | When defining an aggregation-based condition (such as rate or aggregation), you can retrieve the defined threshold value using this property.     |
| `notification.properties`       | Notification properties (map). Values: `user`.                                                                                                    |

**Specific properties**

These properties vary depending on the rules configured and the type of event being processed by Alert Engine.

| Key                              | Description                                              |
| -------------------------------- | -------------------------------------------------------- |
| `environment`                    | Current environment with property `id`.                  |
| `organization`                   | Current organization with property `id`.                 |
| `domain`                         | Current security domain with properties `id` and `name`. |
| `application`                    | Current application with properties `id` and `name`.     |
| `user`                           | Current user principal `username`                        |
| `risk_assessment.unknownDevices` | Current assessment returned when a device is unknown.    |
| `risk_assessment.ipReputation`   | Current assessment for the IP reputation.                |
| `risk_assessment.geoVelocity`    | Current assessment for the geo velocity.                 |
