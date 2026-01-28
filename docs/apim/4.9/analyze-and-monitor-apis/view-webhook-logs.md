---
description: An overview about viewing webhook logs.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/analyze-and-monitor-apis/view-webhook-logs
---

# View Webhook Logs

## Overview

This guide explains how to view and filter webhook callback logs in the APIM Console. Webhook logs contain metrics on HTTP callbacks when messages are sampled.

{% hint style="info" %}
Message sampling and webhook logging are separate settings. Webhook logging must be enabled explicitly in the entrypoint configuration or in the Webhook logs section.
{% endhint %}

## What is logged

As messages go through the Gateway, they are sampled and logged. Webhook logs contain specific metrics related to the HTTP call performed by the callback URL. Although all messages are sent to the Webhook URL, Gravitee stores metrics on the call when the message is being sampled.

## View logs

To view webhook logs:

1. Log in to your APIM Console.
2. Select **APIs** from the left nav.
3. Select the message API with a Webhook entrypoint.
4. Select **Logs** from the inner left nav.
5. A new **Webhook logs** menu item appears for message APIs with webhook entrypoints.

    <figure><img src=".gitbook/assets/1_image.png" alt=""><figcaption><p>Webhook logs menu</p></figcaption></figure>

The list contains logs for all subscriptions of the API. You can filter logs by:

* Status
* Callback URL
* Application

To view details of a specific log entry, click the timestamp.

### Log fields

Each log entry contains the following information:

**Always present:**

* **Request**
  * Date
  * Method (always POST)
  * Callback URL
* **Response**
  * Status (can be 0 in case of connection issues)
  * Duration

**Conditional fields:**

* **HTTP error:** Last message error received
* **Retry attempts:** If retry is configured, displays status, date, and duration for each attempt
* **DLQ status:** If the message was sent to the Dead Letter Queue

**Optional logged data (when enabled):**

* Request headers
* Request body
* Response headers
* Response body

<figure><img src=".gitbook/assets/2_image.png" alt=""><figcaption><p>Webhook log details with all options</p></figcaption></figure>

## Configure webhook logging

By default, no Webhook HTTP callback logging is enabled, even if message logging is enabled. Webhook logging is specific to the Webhook entrypoint and must be configured separately.

### Configure at the entrypoint level

1. Navigate to your API's entrypoint configuration.
2. Toggle the options to include what needs to be logged.

### Configure from the Webhook logs page

1. Navigate to the Webhook logs page.
2. Click the configuration button in the top right corner.
3. Toggle the options to include what needs to be logged.