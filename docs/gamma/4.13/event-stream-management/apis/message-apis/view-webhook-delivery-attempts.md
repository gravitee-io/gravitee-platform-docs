---
hidden: false
noIndex: false
description: Review the calls that the gateway makes to the callback URLs of the webhook subscribers of a Message API in Event Stream Management, with their status, request, and response. Follow the steps to find a delivery attempt.
---

# View webhook delivery attempts

When a Message API has a **Webhook** entrypoint, the gateway pushes messages to the callback URL of each webhook subscription. Each call is a delivery attempt. The **Webhooks** page lists these attempts with their application, callback URL, and response status, and opens the request and the response of each one.

## Prerequisites

* A Message API with a **Webhook** entrypoint. Without one, the **Webhooks** item doesn't appear in the Message API sidebar. See [Configure entrypoints](configure-entrypoints.md).
* Permission to read the logs of the Message API. Without it, the **Webhooks** item doesn't appear in the Message API sidebar.
* Reporting enabled on the Message API. On the **Reporter Settings** page, **Enable analytics** must be selected. See [Configure reporter settings](configure-reporter-settings.md).
* Callback metrics enabled on the **Webhook** entrypoint. On the **Entrypoints** page, in the configuration of the **Webhook** entrypoint, under **Callback reporting settings**, select **Enable callback metrics**, then save and deploy the Message API. Without callback metrics, the gateway records no delivery attempt.

## Open the delivery attempts

1. From the Gamma console, open **Event Stream Management**.
2. In the sidebar, click **Message APIs**.
3. Click the name of the Message API.
4. In the **Monitoring** group of the Message API sidebar, click **Webhooks**.

The **Webhooks** card lists the delivery attempts, newest first, with the following columns:

* **Timestamp**. When the attempt happened.
* **Application**. The ID of the subscribing application.
* **Callback URL**. The URL that the gateway called.
* **Status**. The HTTP status code that the callback URL returned. `0` means that the call got no response.

Message sampling applies to delivery attempts too, so the list can hold fewer attempts than the messages that the gateway pushed. Messages in error are always recorded. See [Configure reporter settings](configure-reporter-settings.md).

## Filter the delivery attempts

Narrow the list with the following filters:

* **Application**. Type the name of an application, then select it in the list.
* **Status**. Enter a status code, for example `500`.
* **Callback URL**. Enter a callback URL, or part of one.

When no attempt matches, the list shows **No delivery attempts**. Clear a filter to widen the search.

## Inspect a delivery attempt

Click the application of an attempt. The **Delivery attempt details** panel opens with the following details:

* The **Application**, the **Callback URL**, and the **Timestamp** of the attempt.
* Under **Request**, the **Method**, **Headers**, and **Body** of the call to the callback URL.
* Under **Response**, the **Status**, **Headers**, and **Body** that the callback URL returned.

The headers and the bodies appear only when the callback reporting settings of the **Webhook** entrypoint include them. Under **Callback reporting settings**, select them under **Request** and under **Response**. Otherwise, the panel shows `—` for them.

## Verification

To verify that delivery attempts are recorded, follow these steps:

1. Publish a message to the topic or the queue that a webhook subscription of the Message API receives.
2. Open the **Webhooks** page of the Message API.
3. Check that a new attempt appears with the callback URL of the subscription and the status code it returned.
