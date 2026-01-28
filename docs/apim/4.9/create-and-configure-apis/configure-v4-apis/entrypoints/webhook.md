---
description: Configure webhook entrypoints for v4 APIs
---

# Webhook

## Overview

The webhook entrypoint allows you to expose v4 message APIs via webhook. When a client subscribes to a webhook entrypoint, the Gateway calls the client's callback URL to push messages in real-time.

## Configuration

To configure a webhook entrypoint:

1. Log in to your APIM Console.
2. Select **APIs** from the left nav.
3. Select your API.
4. Select **Configuration** from the inner left nav.
5. Select the **Entrypoints** tab.
6. Click **+ Add entrypoint** or select an existing webhook entrypoint to edit.
7. Configure the webhook settings:
    * **Context path:** The path on which the webhook entrypoint will be exposed.
    * **HTTP methods:** Select which HTTP methods are allowed (typically POST).
    * **Quality of Service (QoS):** Choose the message delivery guarantee level.
    * **Dead Letter Queue (DLQ):** Configure a DLQ to handle failed message deliveries.
    * **Retry configuration:** Set retry attempts and delays for failed callbacks.
8. Click **Save**.

## Configure webhook logging

### Overview

This guide explains how to enable and configure HTTP callback logging for webhook entrypoints.

{% hint style="info" %}
Webhook logging is disabled by default, even when message logging is enabled. Webhook logging is specific to the webhook entrypoint and must be configured separately.
{% endhint %}

### Configure webhook logging at the entrypoint level

To configure webhook logging at the entrypoint level, complete the following steps:

1. Log in to your APIM Console.
2. Select **APIs** from the left nav.
3. Select your API.
4. Select **Configuration** from the inner left nav.
5. Select the **Entrypoints** tab.
6. Click the webhook entrypoint you want to configure.
7. In the **Logging** section, toggle ON the logging options you want to enable:
    * **Request headers:** Logs the headers sent in the HTTP callback request.
    * **Request body:** Logs the body content of the HTTP callback request.
    * **Response headers:** Logs the headers returned in the HTTP callback response.
    * **Response body:** Logs the body content of the HTTP callback response.

    <figure><img src=".gitbook/assets/1_image.png" alt=""><figcaption><p>Webhook entrypoint logging configuration</p></figcaption></figure>

8. Click **Save**.

### Configure webhook logging from the Webhook logs page

To configure webhook logging from the Webhook logs page, complete the following steps:

1. Log in to your APIM Console.
2. Select **APIs** from the left nav.
3. Select your API.
4. Select **Logs** from the inner left nav.
5. Select the **Webhook logs** tab.
6. Click the configuration button in the top right corner.

    <figure><img src=".gitbook/assets/2_image.png" alt=""><figcaption><p>Webhook logs configuration button</p></figcaption></figure>

7. In the **Logging** section, toggle ON the logging options you want to enable:
    * **Request headers:** Logs the headers sent in the HTTP callback request.
    * **Request body:** Logs the body content of the HTTP callback request.
    * **Response headers:** Logs the headers returned in the HTTP callback response.
    * **Response body:** Logs the body content of the HTTP callback response.
8. Click **Save**.

### View webhook logs

Webhook logs contain specific metrics related to the HTTP call performed by the callback URL. Although all messages are sent to the webhook URL, Gravitee stores metrics on the call when the message is being sampled.

To view webhook logs, complete the following steps:

1. Log in to your APIM Console.
2. Select **APIs** from the left nav.
3. Select your API.
4. Select **Logs** from the inner left nav.
5. Select the **Webhook logs** tab.

The list contains logs for all subscriptions of the API. You can filter logs by status, callback URL, and application.

Click the timestamp to view details for a specific call. The following information is always present:

* **Request**
    * Date
    * Method (always POST)
    * Callback URL
* **Response**
    * Status (can be 0 in case of connection issues)
    * Duration

If an HTTP error occurred, the last message error received is displayed.

If retry is configured, the log includes attempts with status, date, and duration.

If the message was sent to the DLQ, this information is displayed.

If logging is enabled, the following additional information is displayed:

* Request headers
* Request body
* Response headers
* Response body