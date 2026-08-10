---
noIndex: false
---

# Monitor endpoint health

The Endpoint Health Check Dashboard provides real-time visibility into the availability and performance of your API's backend endpoints. You can use this dashboard to monitor response times, track failed health checks, and diagnose connectivity issues.

## Prerequisites

* Health checks are configured and enabled on the API's endpoint groups or endpoints. See the health-check step in [Configure endpoints](../build/configure-your-api-proxy/configure-backend-security.md#step-3-health-check).

## View the health check dashboard

1. From the Gamma console sidebar, select **API Management**, then navigate to **APIs**.
2. Select an API from the list to view its detail page.
3. In the API sub-navigation menu, select **Endpoints**, then select the **Health Check Dashboard** tab.

## Dashboard metrics

The dashboard displays several key metrics and visualizations:

* **Global Metrics**: High-level summary of availability, average response time, and total failures over the selected timeframe.
* **Availability by Field**: A table breaking down availability statistics by specific endpoint or group.
* **Response Time Trend**: A chart displaying the historical trend of endpoint response times.

Use the timeframe filter at the top of the dashboard to adjust the monitoring window (for example, last hour or last 24 hours).

## View failed health checks

The **Failed Health Checks** table lists all unsuccessful endpoint verification attempts within the selected timeframe.

1. Locate the **Failed Health Checks** table at the bottom of the dashboard.
2. Review the list of failures, which includes the timestamp, endpoint name, HTTP status, and error message.
3. Select the **Details** icon next to a failed check to open the log detail sheet.
4. Review the raw request and response data in the log detail sheet to diagnose the root cause of the failure.


## Next steps

* [View API logs](view-api-logs.md)
