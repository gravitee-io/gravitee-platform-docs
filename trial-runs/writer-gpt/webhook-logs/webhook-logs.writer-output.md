# webhook logs.writer output

## Overview

Webhook logs provide observability for webhook deliveries performed by message APIs that use a Webhook entrypoint. Webhook logs help API publishers and API consumers verify delivery status and troubleshoot failed deliveries.

Webhook logs are distinct from message logs:

* **Message logs** capture sampled messages and message-level metadata as they pass through the Gateway.
* **Webhook logs** capture webhook delivery metadata (HTTP status, latency, and optional request/response details) for sampled messages delivered to a subscription callback URL.

{% hint style="info" %}
Webhook deliveries always occur, but webhook delivery data is only stored when the message is sampled for logging. Sampling reduces log volume and storage usage.
{% endhint %}

## What Gravitee logs

### Message logs

As messages go through the Gateway, Gravitee can sample and log messages along with message-level metrics. Sampling protects the platform from extreme-volume use cases while still providing representative visibility.

### Webhook logs

Webhook logs contain delivery metrics related to the HTTP call performed against the subscription callback URL.

Webhook logging uses **separate settings** from message sampling and must be enabled explicitly for the Webhook entrypoint.

## Configure message logging and sampling

### Sampling strategies

Message logging supports the following sampling strategies:

<table><thead><tr><th width="200">Strategy</th><th>How it works</th><th width="220">Defaults and limits</th></tr></thead><tbody><tr><td><strong>Count</strong></td><td>Logs a fixed number of messages, then stops logging.</td><td><p>Default: <code>100</code></p><p>Limit: <code>10</code></p></td></tr><tr><td><strong>Temporal</strong></td><td>Logs messages over a duration, then stops logging.</td><td><p>Default: <code>PT10S</code></p><p>Limit: <code>PT1S</code></p></td></tr><tr><td><strong>Probabilistic</strong></td><td>Logs each message with a probability.</td><td><p>Default: <code>0.01</code></p><p>Limit: <code>0.5</code></p></td></tr><tr><td><strong>Windowed count</strong></td><td>Logs up to a maximum number of consecutive messages during a sliding time window (ISO-8601 duration). When the count is reached within the window, no new messages are logged until the window closes, then logging resumes.</td><td><p>Default: <code>1/PT10S</code></p><p>Limit: <code>1/PT1S</code></p></td></tr></tbody></table>

### Read-only sampling settings

If an administrator configures sampling defaults and/or limits in `gravitee.yml` using non-default values, the corresponding sampling fields in the APIM Console become read-only. This prevents API publishers from configuring sampling values that conflict with platform-level safeguards.

## Configure webhook logging

By default, webhook HTTP callback logging is disabled, even if message logging is enabled. Webhook logging is specific to the Webhook entrypoint, so configuration depends on the entrypoint.

### Enable webhook logging at the entrypoint level

{% stepper %}
{% step %}
### Open the API

Open your message API in APIM Console.
{% endstep %}

{% step %}
### Navigate to Webhook entrypoint configuration

Navigate to the Webhook entrypoint configuration.
{% endstep %}

{% step %}
### Enable webhook logging

Enable webhook logging.
{% endstep %}

{% step %}
### Select stored data

Select which webhook data Gravitee stores for each sampled delivery.
{% endstep %}
{% endstepper %}

### Configure webhook logging from the Webhook logs page

You can also configure webhook logging directly from the Webhook logs page for your API.

## Control stored body size

The `reporting.logging.max_size` setting controls the maximum size of:

* The message body stored in message logs.
* The webhook request body stored in webhook logs (when request body logging is enabled).

{% stepper %}
{% step %}
### Set the maximum stored size in gravitee.yml

```yaml
reporting:
  logging:
    max_size: 0 # <!-- NEED CLARIFICATION: Provide unit (bytes/KB) and recommended default. -->
```
{% endstep %}

{% step %}
### Restart the Gateway

Restart the Gateway to apply the change.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
If you run APIM with Helm, configure the equivalent value in your `values.yaml`.
{% endhint %}

## View webhook logs

On a message API that includes a Webhook entrypoint, the API logs section includes a dedicated Webhook logs view.

### Filter and browse logs

The Webhook logs list contains logs for all subscriptions of the API. Each entry represents a webhook delivery for a sampled message and includes at least:

* Destination callback URL
* Delivery timestamp
* Final HTTP status
* Number of attempts (when retries are configured)

You can filter logs by:

* Delivery status
* Callback URL
* Application

### Inspect a delivery

Select a log entry by timestamp to open the delivery details.

The following fields are always present:

* **Date**
* **Method** (always `POST`)
* **Callback URL**
* **Status** (can be `0` in case of connection issues)
* **Duration**

If a retry policy is configured, Gravitee generates a single log entry after the final attempt. The log entry records the final status and exposes retry attempt details.

If the delivery results in an HTTP error, the detail view can also show:

* The last error received
* Retry attempt timeline (if a retry policy is configured)
* Whether the message was sent to the dead letter queue (DLQ)

### Log payload and header capture

If enabled, the detail view can include:

* Request headers
* Request body
* Response headers
* Response body

{% hint style="warning" %}
Webhook requests and responses can include sensitive data. Enable header/body logging only when necessary and use `reporting.logging.max_size` to limit stored payload size.
{% endhint %}

## View webhook logs in Developer Portal

API consumers can view webhook delivery history for their own webhook subscriptions in APIM Developer Portal.
