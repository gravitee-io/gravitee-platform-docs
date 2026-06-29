---
noIndex: true
---

# Monitor endpoint health

The Endpoint Health Check Dashboard provides real-time visibility into the availability and performance of your API's backend endpoints. You can use this dashboard to monitor response times, track failed health checks, and diagnose connectivity issues.

## Prerequisites

* Your API must have endpoint health checks configured and enabled.

## View the health check dashboard

1. From the Gamma console sidebar, select **API Management**, then navigate to **APIs**.
2. Select an API from the list to view its detail page.
3. In the API sub-navigation menu, select **Endpoints**, then select the **Health Check Dashboard** tab.
   <!-- Source: ApiDetailSidebarNav.tsx L20-L30, gravitee-gamma-module-apim @ d1bb5f8af7 -->

## Dashboard metrics

The dashboard displays several key metrics and visualizations:

* **Global Metrics**: High-level summary of availability, average response time, and total failures over the selected timeframe.
* **Availability by Field**: A table breaking down availability statistics by specific endpoint or group.
  <!-- Source: AvailabilityByFieldTable.tsx L15-L45, gravitee-gamma-module-apim @ d1bb5f8af7 -->
* **Response Time Trend**: A chart displaying the historical trend of endpoint response times.
  <!-- Source: ResponseTimeTrendChart.tsx L15-L50, gravitee-gamma-module-apim @ d1bb5f8af7 -->

Use the timeframe filter at the top of the dashboard to adjust the monitoring window (e.g., last hour, last 24 hours).

## View failed health checks

The **Failed Health Checks** table lists all unsuccessful endpoint verification attempts within the selected timeframe.

1. Locate the **Failed Health Checks** table at the bottom of the dashboard.
   <!-- Source: FailedHealthChecksTable.tsx L20-L60, gravitee-gamma-module-apim @ d1bb5f8af7 -->
2. Review the list of failures, which includes the timestamp, endpoint name, HTTP status, and error message.
3. Select the **Details** icon next to a failed check to open the log detail sheet.
4. Review the raw request and response data in the log detail sheet to diagnose the root cause of the failure.
   <!-- Source: HealthCheckLogDetailSheet.tsx L30-L80, gravitee-gamma-module-apim @ d1bb5f8af7 -->

<!-- GAP: 128 · Confirmable · Confirm if the health check dashboard supports exporting logs or metrics to external monitoring systems. Needs: UI verification -->

## Next steps

* [View API logs](view-api-logs.md)
