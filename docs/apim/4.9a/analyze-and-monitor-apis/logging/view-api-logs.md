# View API Logs

## Overview

Gravitee lets you collect runtime logs for v4 proxy APIs and v4 message APIs, and webhook logs for v4 message APIs that use a webhook entrypoint. The following sections describe how to view the logs for v4 APIs.

## View runtime logs

Comprehensive connection logs let you analyze the usage of your v4 message APIs or v4 proxy APIs. To view the logs associated with calls to your API, complete the following steps:

1. Select **APIs** from your APIM Console's navigation menu.
2. Select the API for which you want to enable or modify logging.
3. Navigate to the desired logs applicable to your API.
   1.  To view v4 API runtime logs, click the **Logs** menu item:

       <figure><img src="../../.gitbook/assets/67DC788E-B000-4F17-8547-2D34EE35FB89_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
   2.  To view the webhook logs for a v4 message API with a webhook entrypoint, click the **Webhook** menu item:

       <figure><img src="../../.gitbook/assets/logging-webhook-view3.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
If logging is disabled, existing logs are displayed with a banner that indicates that the record is not current.
{% endhint %}

### Filter API logs

The list of logs associated with an API contains logs for all of the API's subscriptions. The filters above the list let you search records based on API logging information. Different filters apply to the runtime logs for v4 proxy APIs and v4 message APIs and the webhook logs for v4 message APIs.

You can filter v4 proxy API and v4 message API runtime logs based on the following information:

* **Period:** The time period for which you want to view logs.
* **Entrypoints:** The Entrypoint used to interact with the API.
* **HTTP methods:** The method used to interact with the API.
* **Plan:** The plan used to interact with the API.

The **More** button offers additional filtering options.

<figure><img src="../../.gitbook/assets/image (363) (1).png" alt=""><figcaption></figcaption></figure>

You can filter v4 message webhook logs based on time period, HTTP status, and application. The **More** button lets you filter by callback URL and a customized timeframe.&#x20;

<figure><img src="../../.gitbook/assets/logging-webhook-filters.png" alt=""><figcaption></figcaption></figure>

## View log details

You can view runtime logs for all v4 proxy APIs and v4 message APIs. You can view webhook logs for v4 message APIs that use the webhook entrypoint.

#### v4 proxy API runtime logs

To view the details of any entry in the list of runtime logs, select **Logs** from your API's menu, and then click the eye symbol next to the log whose details you want to view.

<figure><img src="../../.gitbook/assets/321F6892-812F-4DAA-AEE6-0CA0C44BEFF4_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

The logs screen shows the following API-level logging information:

<figure><img src="../../.gitbook/assets/image (1) (1).png" alt=""><figcaption></figcaption></figure>

The **Overview** section provides information about the request and response phases of the API.&#x20;

The **More details** drop-down menu shows information about the application, plan, endpoint, Gateway host, and Gateway IP associated with the API.

<figure><img src="../../.gitbook/assets/E28EB0D9-6405-4876-8730-BFA28645A4D5_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

The **Details** menu shows the details of the API request and response phases.

The **Request** panel shows the HTTP method and URI for the Gateway and consumer, the headers sent by the user or the backend in the request phase, and the request body.

<figure><img src="../../.gitbook/assets/image (369) (1) (1).png" alt=""><figcaption></figcaption></figure>

The **Response** panel shows the status of the Gateway and consumer, the headers sent by the user or the backend in the response phase, and the body returned in the response.

<figure><img src="../../.gitbook/assets/2421DA4C-35BB-4DAD-A6FA-642B70A17486_4_5005_c (1).jpeg" alt=""><figcaption></figcaption></figure>

### v4 message API runtime logs

To view the details of any entry in the list of v4 message API runtime logs, select **Logs** from your API's menu, and then click the eye symbol next to the log whose details you want to view.

<figure><img src="../../.gitbook/assets/logging-webhook-view4.png" alt=""><figcaption></figcaption></figure>

Under the **Connection Logs** tab, logs for the entry are grouped by **Entrypoint Request**, **Endpoint Request**, **Entrypoint Response**, and **Endpoint Response**:

<figure><img src="../../.gitbook/assets/connection details_CROP (1).png" alt=""><figcaption><p>View log details</p></figcaption></figure>

Under the **Messages** header, entrypoint and endpoint message details are grouped by date code:

<figure><img src="../../.gitbook/assets/message details_CROP (1).png" alt=""><figcaption><p>View message details</p></figcaption></figure>

Each message record includes placeholder tabs for raw content, headers, and metadata. If the corresponding data was recorded, it appears under the tab. If no data was recorded, the field is empty.

### v4 message API webhook logs

Webhook logs contain specific metrics related to the HTTP call performed by the callback URL. Gravitee stores call metrics when the message sent to the webhook URL is sampled.

To view the details of any entry in the list of webhook logs, select **Webhooks** from your API's menu, and then click the eye symbol next to the log whose details you want to view.

<figure><img src="../../.gitbook/assets/logging-webhook-view2.png" alt=""><figcaption></figcaption></figure>

The **Overview** section shows general information about the request and response phases.&#x20;

The request information includes the date of the request, number of delivery attempts, and the callback URL. The response information includes the HTTP status, response duration, and payload size.

<figure><img src="../../.gitbook/assets/logging-webhook-overview.png" alt=""><figcaption></figcaption></figure>

If there are connection issues, the response status can be 0. If an HTTP error occurred, the following information is recorded:

* Last error message received
* If retry is configured:
  * The count, status, date, and duration of attempts
* If the message was sent to the DLQ

The **Delivery attempts** section records the number of retry attempts, the timestamp of the delivery, its duration, and its HTTP status.

<figure><img src="../../.gitbook/assets/logging-webhook-delivery.png" alt=""><figcaption></figcaption></figure>

Optionally, you can [enable logging for each of the following](configure-api-level-logs.md):

* Request headers
* Request body
* Response headers
* Response body

<figure><img src="../../.gitbook/assets/logging-webhook.png" alt=""><figcaption></figcaption></figure>
