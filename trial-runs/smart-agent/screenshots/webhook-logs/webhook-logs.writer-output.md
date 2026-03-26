# webhook logs.writer output

## Overview

This guide explains how to configure and view webhook logs for message APIs with webhook entrypoints in Gravitee API Management (APIM).

Webhook logs provide observability into the HTTP calls made by the Gateway when delivering messages to webhook callback URLs. While all messages are sent to the webhook URL, Gravitee samples and logs specific metrics about each delivery attempt based on your configuration.

## Prerequisites

Before you configure webhook logs, complete the following:

* Deploy a message API with a webhook entrypoint
* Configure an analytics database (Elasticsearch or OpenSearch) for your environment

## Enable callback metrics

By default, webhook HTTP callback logging is disabled, even when message logging is enabled. Enable callback metrics to capture delivery data in your analytics database.

{% stepper %}
{% step %}
### Access the API

Log in to the API Management Console and select **APIs** from the left sidebar. Then select the message API with a webhook entrypoint that you want to configure.
{% endstep %}

{% step %}
### Open Webhooks settings

In the left menu, select **Webhooks**.
{% endstep %}

{% step %}
### Enable callback metrics

In the **Callback reporting settings** section, toggle **Enable callback metrics** to enable logging.

{% hint style="warning" %}
Opt for logging checkboxes carefully. Logging requires extra storage and may affect API performance.
{% endhint %}
{% endstep %}

{% step %}
### Configure request logging (optional)

Toggle the following options in the **Request** section to log callback request content:

* **Headers**: Log the HTTP headers sent in the callback request
* **Body**: Log the HTTP body sent in the callback request
{% endstep %}

{% step %}
### Configure response logging (optional)

Toggle the following options in the **Response** section to log callback response content:

* **Headers**: Log the HTTP headers received from the callback endpoint
* **Body**: Log the HTTP body received from the callback endpoint
{% endstep %}

{% step %}
### Save

Click **Save** to apply your changes.
{% endstep %}
{% endstepper %}

## View webhook logs

After you enable callback metrics, you can view logs for all webhook delivery attempts across subscriptions.

{% stepper %}
{% step %}
### Open the Webhooks page

In the API Management Console, navigate to your message API with a webhook entrypoint and select **Webhooks** in the left menu.
{% endstep %}

{% step %}
### Review the delivery logs

Review the list of webhook delivery logs. The list displays logs for all subscriptions of the API.
{% endstep %}

{% step %}
### Filter logs (optional)

Filter the logs by:

* **Status**: Filter by HTTP response status code
* **Callback URL**: Filter by the destination webhook URL
* **Application**: Filter by the subscribing application
{% endstep %}

{% step %}
### View log details

Click a timestamp to view the details of a specific delivery attempt.
{% endstep %}
{% endstepper %}

### Log details

Each log entry contains the following information:

Request details (always present):

* Date: Timestamp of the delivery attempt
* Method: HTTP method used (always POST)
* Callback URL: The webhook endpoint URL

Response details (always present):

* Status: HTTP response status code (returns 0 for connection issues)
* Duration: Time taken for the HTTP call

Error details (present for HTTP errors):

* Last message error received: The error message from the failed delivery
* Retry attempts: If retry is configured, displays each attempt with its status, date, and duration
* DLQ status: Indicates if the message was sent to the dead letter queue (DLQ)

Optional logged content (if enabled in callback reporting settings):

* Request headers
* Request body
* Response headers
* Response body

## Configure sampling strategies

Sampling strategies control how many messages are logged to protect system resources during high-volume scenarios. Configure sampling defaults and limits in the `gravitee.yml` file.

{% hint style="info" %}
When sampling settings are configured in `gravitee.yml` with values other than the defaults, the corresponding fields in the Management Console become read-only.
{% endhint %}

The following sampling strategies are available:

| Strategy       | Description                                                      | Default | Limit  |
| -------------- | ---------------------------------------------------------------- | ------- | ------ |
| Count          | Samples a maximum count of consecutive messages                  | 100     | 10     |
| Temporal       | Samples messages based on a time interval (ISO-8601 duration)    | PT10S   | PT1S   |
| Probabilistic  | Samples messages based on a probability value                    | 0.01    | 0.5    |
| Windowed Count | Samples a maximum count of messages during a sliding time window | 1/PT10S | 1/PT1S |

### Windowed count strategy

The windowed count strategy samples a maximum count of consecutive messages during a sliding time window that conforms to an ISO-8601 duration. When the count is reached during that time window, no new messages are logged until the window closes. After the window closes, message logging resumes.

## Configure maximum log size

Control the size of logged content by configuring the `reporting.logging.max_size` setting in `gravitee.yml`. This setting limits:

* The size of the message body stored in logs
* The size of logged webhook request body (when enabled)

## Next steps

* Configure retry policies for webhook delivery failures
* Set up dead letter queues for undeliverable messages
* Review message logging configuration for your message APIs
