# Message and Webhook Logging Overview

## Overview

Gravitee message logging and webhook logging provide detailed observability into the data transmitted between the Gateway, backend systems, and API consumers. These capabilities enable operational monitoring and troubleshooting by recording message metadata, delivery statuses, and performance metrics.

Message logging captures the details of individual messages as they pass through the Gateway. Webhook logging specifically observes HTTP callback calls performed by the Webhook entrypoint. These logs integrate with Gravitee Lens to provide AI-powered analytics and self-service insights for both API publishers and consumers.

## Key features

### Webhook delivery observability
Webhook logging enhances standard message logging by capturing critical delivery metadata.
* **Deferred reporting**: The Gateway reports logs after the outgoing webhook call completes to ensure the response status and latency are captured accurately.
* **Retry handling**: For deliveries configured with a retry policy, Gravitee generates a single log entry after the final attempt. This entry records the final status, the total number of attempts, and the details of the last error received.
* **Consolidated views**: Detailed logs are accessible in both the API Management (APIM) Console and the Developer Portal. This allows consumers to verify delivery and debug issues independently without contacting the API publisher.

### Volume management and sampling
Gravitee uses sampling strategies to manage log volume and protect system performance in high-traffic scenarios.
* **Count per time window**: Samples a maximum count of consecutive messages during a sliding time window that conforms to an ISO-8601 duration. When the count is reached, the Gateway stops logging until the window closes.
* **Temporal**: Logs messages at regular time intervals based on a specified duration.
* **Probabilistic**: Logs a random percentage of messages.
* **Windowed count**: Logs a specified number of messages within a sliding time window.

## How it works

As messages pass through the Gateway, they are sampled according to the configured strategy. Sampled messages are logged along with metrics and, if enabled, the request and response headers and bodies.

Webhook logs contain specific metrics related to the HTTP call performed by the callback URL. Although all messages are sent to the Webhook URL, Gravitee only stores metrics on the call when the message is sampled. Webhook logging is separate from general message sampling and must be enabled explicitly in the entrypoint configuration or the Webhook logs section.

---

# Configure Gateway Message Logging

## Overview

This guide explains how to configure global message logging settings on the Gravitee Gateway. Administrators can define these limits in the `gravitee.yml` file or via Helm charts to control log volume and resource consumption across the environment.

## Configuration settings

Configure message logging in the `reporting.logging` section of your `gravitee.yml` file.

### Message body size
The `max_size` setting controls the maximum size of the message body stored in the logs and the size of logged webhook request bodies.

{% code title="gravitee.yml" overflow="wrap" %}
```yaml
reporting:
  logging:
    max_size: 10KB
```
{% endcode %}

### Sampling strategies
Sampling strategies determine the frequency and volume of logged messages. 

{% hint style="info" %}
If these settings are configured in `gravitee.yml` with any value other than the default, they appear as read-only in the APIM Console.
{% endhint %}

| Strategy | Default Value | Limit |
| :--- | :--- | :--- |
| **Count** | 100 | 10 |
| **Temporal** | PT10S | PT1S |
| **Probabilistic** | 0.01 | 0.5 |
| **Windowed Count** | 1/PT10S | 1/PT1S |

---

# Configure Webhook Logging

## Overview

This guide explains how to enable and configure webhook logging for an API. By default, Gravitee does not enable HTTP callback logging for webhooks, even if general message logging is active. Webhook logging is specific to the Webhook entrypoint.

## Enable webhook logging

You can enable webhook logging directly within the entrypoint configuration of a message API.

1. Log in to your APIM Console.
2. Select your message API from the **APIs** menu.
3. Select **Entrypoints** from the left nav.
4. Click the edit icon for the Webhook entrypoint.
5. In the **Logging** section, configure the following:
   * **Enable Webhook Logging**: Toggle this setting ON to begin capturing HTTP callback metrics.
   * **Include Headers**: Toggle ON to include request and response headers in the logs.
   * **Include Body**: Toggle ON to include request and response bodies in the logs.
6. Click **Save Changes**.

<!-- TODO: Add screenshot of the Webhook entrypoint logging configuration section -->

## Configure from the Webhook logs page

You can also access logging configuration from the **Webhook logs** view by clicking the settings button in the top right corner of the page.

<!-- TODO: Add screenshot of the Webhook log page with the settings button highlighted -->

---

# Explore Message and Webhook Logs

## Overview

Gravitee provides a dedicated view for exploring webhook delivery attempts and message logs. These logs allow publishers and consumers to verify event delivery and troubleshoot errors.

## View webhook logs

On a message API using a Webhook entrypoint, a dedicated **Webhook logs** entry is available in the side menu.

<!-- TODO: Add screenshot of the APIM Console side menu showing the Webhook logs entry -->

The log list contains records for all subscriptions to the API. You can search and filter the list using the following criteria:
* **Status**: Filter by the HTTP status of the delivery (e.g., Succeeded, Failed).
* **Callback URL**: Filter by the destination destination URL.
* **Application**: Filter by the consumer application.
* **Time range**: Filter by the date and time of the delivery attempt.

## Interpret log details

Click on a log entry timestamp to view the full details of a specific delivery attempt.

### Delivery information
The log view always includes the following metrics:
* **Request**: The attempt date, the HTTP method (always POST), and the callback URL.
* **Response**: The HTTP status code and the call duration.

{% hint style="info" %}
The status code may be `0` in cases of connection issues or timeouts.
{% endhint %}

### Troubleshooting errors
If an HTTP error occurs, the log provides additional troubleshooting data:
* **Last message error received**: The error message returned by the callback URL or Gateway.
* **Retry attempts**: If a retry policy is configured, a timeline displays the status, date, and duration for each attempt.
* **Dead Letter Queue (DLQ)**: Indicates if the message was ultimately sent to a DLQ.

### Payload and header details
If enabled in the entrypoint configuration, the log also displays:
* **Request headers and body**
* **Response headers and body**

<!-- TODO: Add screenshot of the log detail view showing all options (retry, request, response) -->
