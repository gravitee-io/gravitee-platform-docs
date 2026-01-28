---
description: Configure webhook entrypoints for v4 APIs
---

# Webhook

## Overview

The webhook entrypoint allows you to expose v4 message APIs via webhook. When a client subscribes to a webhook entrypoint, the Gateway establishes a persistent connection and pushes messages to the client's callback URL in real-time.

## Configuration

To configure a webhook entrypoint:

1. Log in to your APIM Console.
2. Select **APIs** from the left nav.
3. Select your API.
4. Select **Configuration** from the inner left nav.
5. Select the **Entrypoints** tab.
6. Click **+ Add entrypoint** or select an existing webhook entrypoint to modify.
7. Configure the webhook settings:
   * **Context path**: The path on which the webhook entrypoint will be exposed
   * **Callback URL**: The URL to which the Gateway will send HTTP POST requests
   * **HTTP method**: The HTTP method to use (typically POST)
   * **Headers**: Optional headers to include in webhook requests
   * **Retry configuration**: Configure retry behavior for failed webhook deliveries
   * **Dead Letter Queue (DLQ)**: Configure DLQ settings for messages that fail after all retries

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
   * **Request headers**
   * **Request body**
   * **Response headers**
   * **Response body**

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
   * **Request headers**
   * **Request body**
   * **Response headers**
   * **Response body**
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

Click on a timestamp to view the details of a specific call. The details include:

* **Request**
  * Date
  * Method (always POST)
  * Callback URL
* **Response**
  * Status (can be 0 in case of connection issues)
  * Duration
* **Error information** (if applicable)
  * Last message error received
* **Retry information** (if retry is configured)
  * Attempts with status, date, and duration
* **Dead Letter Queue (DLQ) information** (if applicable)
  * Indicates if the message was sent to the DLQ
* **Logged data** (if enabled)
  * Request headers
  * Request body
  * Response headers
  * Response body