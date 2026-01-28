---
description: An overview about viewing webhook logs.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/analyze-and-monitor-apis/view-webhook-logs
---

# View Webhook Logs

## Overview

This guide explains what webhook logs contain and provides step-by-step instructions for viewing and filtering webhook callback logs in the APIM Console.

## What is logged

As messages go through the Gateway, they are sampled and logged along with some metrics. Webhook logs contain specific metrics related to the HTTP call performed by the callback URL. Although all messages are sent to the webhook URL, Gravitee stores metrics on the call when the message is being sampled.

{% hint style="info" %}
Webhook logging is separate from message sampling and must be enabled explicitly in the entrypoint configuration or in the Webhook logs section.
{% endhint %}

## View webhook logs

To view webhook logs for a message API with a webhook entrypoint:

1. Log in to your APIM Console.
2. Select **APIs** from the left nav.
3. Select your API.
4.  Select **Logs** from the inner left nav.

    <figure><img src=".gitbook/assets/1_image.png" alt=""><figcaption><p>Webhook logs menu</p></figcaption></figure>

The list contains logs for all subscriptions of the API. You can filter on status, callback URL, and application.

### View log details

To view the details of a webhook log entry:

1.  Click the timestamp of the log entry you want to view.

    <figure><img src=".gitbook/assets/2_image.png" alt=""><figcaption><p>Webhook log details</p></figcaption></figure>

The log details include the following information:

**Always present**

* **Request**
  * Date
  * Method (always POST)
  * Callback URL
* **Response**
  * Status (can be 0 in case of connection issues)
  * Duration

**In case of HTTP error**

* Last message error received

**If retry is configured**

* Attempts with status, date, and duration

**If the message was sent to the DLQ**

* DLQ status

**If enabled in configuration**

* Request headers
* Request body
* Response headers
* Response body

## Configure webhook logging

By default, no webhook HTTP callback logging is enabled, even if message logging is enabled. Webhook logging is specific to the webhook entrypoint, so its configuration depends on it.

### Configure at the entrypoint level

To configure webhook logging at the entrypoint level:

1. Navigate to your API's entrypoint configuration.
2. Toggle the options to include what needs to be logged.

### Configure from the Webhook logs page

To configure webhook logging from the Webhook logs page:

1. Navigate to the Webhook logs page.
2. Click the configuration button in the top right.
3. Toggle the options to include what needs to be logged.