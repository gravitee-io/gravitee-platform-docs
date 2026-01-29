# webhook logs.writer output

## Overview

This guide explains how to view and configure webhook logs for message APIs in Gravitee API Management (APIM). Webhook logs provide observability into the HTTP calls made by the Gateway when delivering messages to consumer webhook endpoints.

When messages flow through the Gateway to a webhook subscription, Gravitee samples and logs delivery attempts along with specific metrics. These logs enable you to monitor delivery status, troubleshoot failures, and verify successful message delivery.

## Prerequisites

Before you configure webhook logs, ensure the following:

* You have a message API with a webhook entrypoint configured
* You have appropriate permissions to access the API configuration in the Management Console
* Message logging is enabled for sampling (webhook logging is separate but works alongside message sampling)

## View webhook logs

Webhook logs display delivery attempt details for all subscriptions on a message API. You can filter logs by status, callback URL, and application.

{% stepper %}
{% step %}
### Open the APIs page

In the Management Console, select **APIs** from the left menu.
{% endstep %}

{% step %}
### Select the message API

Select the message API that has a webhook entrypoint configured.
{% endstep %}

{% step %}
### Open Webhooks

In the left sidebar, select **Webhooks**.
{% endstep %}

{% step %}
### Review the webhook delivery logs

Review the list of webhook delivery logs. Each entry displays the following information:

* **Timestamp**: When the delivery attempt occurred
* **Status**: HTTP response status code (a status of `0` indicates a connection issue)
* **Callback URL**: The webhook endpoint that received the message
* **Application**: The subscribing application
{% endstep %}

{% step %}
### View detailed log info

Click a timestamp to view detailed information about the delivery attempt.
{% endstep %}
{% endstepper %}

### Log details

Each webhook log entry contains the following information:

Request details (always present):

* Date of the request
* HTTP method (always POST)
* Callback URL

Response details (always present):

* HTTP status code
* Duration of the call

Error and retry information (when applicable):

* Last error message received (for HTTP errors)
* Number of retry attempts with individual status, date, and duration (if retry is configured)
* Dead Letter Queue (DLQ) delivery status (if the message was sent to a DLQ)

Optional logged content (when enabled):

* Request headers
* Request body
* Response headers
* Response body

## Configure webhook logging

By default, webhook HTTP callback logging is disabled, even when message logging is enabled. You must explicitly enable webhook logging in the entrypoint configuration.

{% hint style="warning" %}
Enable logging options carefully. Logging request and response headers or bodies requires extra storage and may affect API performance.
{% endhint %}

{% stepper %}
{% step %}
### Open your message API

Navigate to your message API in the Management Console.
{% endstep %}

{% step %}
### Open Webhooks

In the left sidebar, select **Webhooks**.
{% endstep %}

{% step %}
### Locate Callback reporting settings

Locate the **Callback reporting settings** section.
{% endstep %}

{% step %}
### Enable callback metrics

Enable **Enable callback metrics** to activate callback call reporting in your analytics databases (for example, Elasticsearch or OpenSearch).
{% endstep %}

{% step %}
### Configure logging options

Configure the logging options based on your requirements:

* **Request**:
  * **Headers**: Toggle to log request headers sent to the callback URL
  * **Body**: Toggle to log the request body sent to the callback URL
* **Response**:
  * **Headers**: Toggle to log response headers received from the callback URL
  * **Body**: Toggle to log the response body received from the callback URL
{% endstep %}

{% step %}
### Save

Click **Save** to apply the configuration.
{% endstep %}
{% endstepper %}

### Logging behavior

Webhook logs are reported after the outgoing webhook call completes, not before. This allows the system to capture the actual response status and latency.

For deliveries configured with a retry policy:

* A single log entry is generated after the final attempt
* The entry records the final status (success or failure)
* The total number of attempts is included
* Details of the last error are captured

{% hint style="info" %}
Webhook logging is governed by sampling to manage log volume. The sampling strategy determines how many messages are logged within a given time window.
{% endhint %}

## Verification

{% stepper %}
{% step %}
### Send a test message

Send a test message through your message API.
{% endstep %}

{% step %}
### Open the Webhooks section

Navigate to the **Webhooks** section of your API.
{% endstep %}

{% step %}
### Confirm log entry appears

Confirm that a new log entry appears with the expected delivery details.
{% endstep %}

{% step %}
### Inspect enabled content

Click the log entry to verify that the enabled content (headers, body) is captured.
{% endstep %}
{% endstepper %}

## Next steps

* Configure retry policies for webhook deliveries to handle transient failures
* Set up a Dead Letter Queue to capture messages that fail delivery after all retry attempts
* Review message logging configuration to adjust sampling strategies
