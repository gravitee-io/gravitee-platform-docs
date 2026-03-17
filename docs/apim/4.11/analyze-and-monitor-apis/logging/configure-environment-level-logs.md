# Configure environment-level logs

## Overview

Environment-level logs provide cross-API visibility into the runtime logs for your v4 proxy APIs. You can view request logs across all v4 proxy APIs in a single, centralized page within the APIM Console.

Viewing the environment logs for v4 proxy APIs is provides you with the following benefits:

* You can monitor traffic patterns across multiple APIs.
* You can troubleshoot issues that span several APIs.
* You can audit API usage at the environment level.

{% hint style="info" %}
Environment-level logs are available for v4 proxy APIs only. To view logs for a specific API, including v4 message APIs and webhook logs, see [View API Logs](/docs/apim/4.11/analyze-and-monitor-apis/logging/view-api-logs.md).
{% endhint %}

## View environment-level logs

To view the logs for your v4 proxy APIs in your environment, complete the following steps:

1. From the **Dashboard**, click **Observability**. 
2. From the **Observability** dropdown menu, click **Logs**. 

The logs table displays a paginated list of log entries across all v4 proxy APIs in the current environment. Each entry shows the following information:

* **Timestamp:** The date and time of the request.
* **HTTP method:** The HTTP method used in the request.
* **Status:** The HTTP response status code.
* **API:** The name of the API that received the request.
* **Path:** The request path.
* **Application:** The application that made the request.
* **Plan:** The plan associated with the API call.
* **Gateway:** The Gateway instance that processed the request.
* **Response time:** The time taken to process the request.

<figure><img src="/.gitbook/assets/environment-_logs_nav.png" alt=" Logs screen showsing the logs highlighted in the navigation menu"><figcaption></figcaption></figure>

## Filter your logs

The **Logs** provides filters that refine the list of log entries. The quick filters filter information based on the following information:

* **Period:** Select a predefined time range to display only logs from that window.
* **API:** Search for and select one or more APIs to display only their logs.
* **Application:** Search for one or more applications, and then select one or more applications to display only their logs.&#x20;

The **More** button opens a panel with additional filtering options, which are organized into the following sections:&#x20;

**Date**

* **From:** Set the start of a custom date and time range.
* **To:** Set the end of a custom date and time range. The "To" value must be after the "From" value.&#x20;

**Response**

* **Status:** Enter one or more HTTP response status codes (for example, 200, 404, 500) to filter by.&#x20;

**Request**

* **Entrypoints:** Filter by the entrypoint type used to interact with the API (for example, HTTP Proxy, HTTP GET, SSE, WebSocket).
* **HTTP Methods:** Filter by the HTTP method used in the request (for example, GET, POST, PUT, DELETE).
* **Plan:** Filter by a specific plan. This option is only available when exactly one API is selected in the quick filters above.&#x20;

**Additional filters**

* **Transaction ID:** Filter by a transaction ID (UUID format) to find all requests associated with a specific transaction.
* **Request ID:** Filter by a specific request ID (UUID format) to locate an individual request.
* **URI:** Filter by request path. Dor example, `/api/v1/users`.
* **Response time (ms):** Filter for requests with a response time greater than or equal to the specified value, in milliseconds.
* **Error Types:** Filter by specific error types. The available options are dynamically populated based on errors observed within the selected date range.&#x20;

You can combine multiple filters to refine the results. Applied filters appear after the filter bar. Use the **Reset filters** button to clear all active filters.

<figure><img src="/.gitbook/assets/environment_logs_filters.png" alt=" Logs screen showing the logs highlighted in the navigation menu"><figcaption></figcaption></figure>

## View the details of your logs

To view the details of any entry in the list of logs, click the entry in the logs table.

<figure><img src="/.gitbook/assets/environment_logs_log_details.png" alt=" Logs screen showing detailed logs"><figcaption></figcaption></figure>

The log details page shows the following information:

* The **Overview** section provides general information about the request and response phases, including the timestamp, HTTP method, path, and response status.&#x20;

* The **More details** dropdown menu shows information about the application, plan, endpoint, Gateway host, and Gateway IP associated with the request.

* The **Request** panel shows the HTTP method and URI for the Gateway and consumer, the headers sent in the request phase, and the request body.

* The **Response** panel shows the status of the Gateway and consumer, the headers sent in the response phase, and the body returned in the response.

{% hint style="info" %}
The level of detail available in each log entry depends on the [API-level logging configuration](/docs/apim/4.11/analyze-and-monitor-apis/logging/configure-api-level-logs.md). To capture request and response headers and payloads, you must configure logging at the API level.
{% endhint %}