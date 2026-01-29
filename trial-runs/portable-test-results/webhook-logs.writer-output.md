# Webhook Logs

## Overview

This guide explains how to view and configure webhook logs for message APIs in Gravitee API Management (APIM).

Webhook logs provide observability for webhook deliveries. When a message is consumed from a backend system (such as Kafka) and pushed to a consumer's webhook endpoint, webhook logs capture metrics about each HTTP callback, including the response status, latency, and retry attempts.

{% hint style="info" %}
Webhook logging is specific to APIs with a Webhook entrypoint. This feature is separate from standard message logging and must be enabled explicitly.
{% endhint %}

## Prerequisites

Before you configure webhook logs, complete the following:

* Create a message API with a Webhook entrypoint
* Deploy the API to the Gateway

## View webhook logs

1.  In the APIM Console, select **APIs** from the left menu, and then select your API.

2.  In the API menu, select **Webhooks**.

    <figure><img src=".gitbook/assets/apim-webhook-logs-step-01.png" alt="API Configuration page with Webhooks menu item highlighted"><figcaption></figcaption></figure>

The webhook logs list displays logs for all subscriptions of the API. You can filter logs by:

* Status
* Callback URL
* Application

3. Click a timestamp to view the details of a specific webhook call.

### Log details

Each webhook log entry contains the following information:

**Request details (always present):**

| Field | Description |
|-------|-------------|
| Date | The timestamp of the webhook call |
| Method | The HTTP method (always POST) |
| Callback URL | The destination URL for the webhook |

**Response details (always present):**

| Field | Description |
|-------|-------------|
| Status | The HTTP response status code. A value of 0 indicates a connection error. |
| Duration | The time taken for the webhook call to complete |

**Error and retry details (when applicable):**

| Field | Description |
|-------|-------------|
| Last message error | The most recent error message received |
| Retry attempts | The number of retry attempts with status, date, and duration for each |
| DLQ status | Indicates if the message was sent to the dead letter queue (DLQ) |

**Optional logged content (when enabled):**

* Request headers
* Request body
* Response headers
* Response body

## Configure webhook logging

By default, webhook HTTP callback logging is disabled, even if message logging is enabled.

1. In the APIM Console, select **APIs** from the left menu, and then select your API.

2. In the API menu, select **Webhooks**.

3. Navigate to the **Callback reporting settings** section.

4.  Enable **Enable callback metrics** to report callback calls to your analytics databases.

    <figure><img src=".gitbook/assets/apim-webhook-logs-step-02.png" alt="Callback reporting settings with logging options for request and response"><figcaption></figcaption></figure>

5. Configure the logging options:
   * **Request**
     * **Headers**: Toggle to log request headers
     * **Body**: Toggle to log request body
   * **Response**
     * **Headers**: Toggle to log response headers
     * **Body**: Toggle to log response body

6. Click **Save** to apply the configuration.

{% hint style="warning" %}
Enabling detailed logging (headers and body) requires additional storage and may affect API performance. Enable these options selectively based on your troubleshooting needs.
{% endhint %}

<!-- NEED CLARIFICATION: The draft mentions configuring logging from the Webhook log page with a button in the top right. This UI flow is not shown in the provided screenshots. -->

## Sampling configuration

<!-- UNCERTAIN: The draft mentions sampling strategies but does not provide complete details on how to configure them in the UI. The following information is based on the draft notes. -->

Webhook logging supports sampling strategies to manage log volume. The following strategies are available:

| Strategy | Default | Limit |
|----------|---------|-------|
| Count | 100 | 10 |
| Temporal | PT10S | PT1S |
| Probabilistic | 0.01 | 0.5 |
| Windowed Count | 1/PT10S | 1/PT1S |

The **Windowed Count** strategy samples a maximum count of consecutive messages during a sliding time window (ISO-8601 duration format). When the count is reached during that time window, no new messages are logged until the window closes.

{% hint style="info" %}
Sampling settings configured in `gravitee.yml` take precedence and make the corresponding UI settings read-only.
{% endhint %}

### Configure message body size limit

To control the size of message bodies stored in logs, configure the `reporting.logging.max_size` property in `gravitee.yml`:

```yaml
reporting:
  logging:
    max_size: 8192
```

This setting controls the size limit for:
* Message body stored in logs
* Webhook request body (if logging is enabled)

<!-- NEED CLARIFICATION: The draft mentions providing Helm version of gravitee.yml settings, but specific Helm values were not provided in the source materials. -->

## Next steps

* Configure retry policies for webhook deliveries
* Set up alerts for webhook delivery failures
* Monitor webhook performance in the Analytics dashboard

<!-- ASSETS USED (copy/rename exactly):
- screenshots/image_1.png -> .gitbook/assets/apim-webhook-logs-step-01.png | alt: "API Configuration page with Webhooks menu item highlighted"
- screenshots/image_2.png -> .gitbook/assets/apim-webhook-logs-step-02.png | alt: "Callback reporting settings with logging options for request and response"
-->