---
hidden: false
noIndex: true
---

# Monitor API usage
<!-- GAP-STRUCTURAL: Missing procedural content source -->
The API usage dashboard provides real-time and historical metrics for your API proxies, including request volume, latency distribution, error rates, and consumer-level analytics.

## Dashboard overview

To access the analytics dashboard for your HTTP Proxy APIs:
1. From the Gamma console sidebar, select **API Management**.
2. Navigate to your API proxy.
3. In the sidebar under **Monitoring**, select **Observability**.

By default, the dashboard displays metrics for the last **7 days** using a relative time range. You can adjust the time window using the time-range selector.

## Key metrics

The Observability dashboard for HTTP proxies includes several specialized widgets:

### Key Performance Indicators (KPIs)
* **Total Requests**: The absolute volume of requests handled by the Gateway.
* **Error Rate**: Percentage of requests resulting in error responses.
* **Response Time**: The Average, P95, and Max response times observed by consumers.

### Traffic Analysis
* **Requests by HTTP Method**: A stacked bar chart of request volume per method overlaid with the P95 response time.
* **Status Distribution**: A doughnut chart visualizing the share of responses by HTTP status code group (e.g., 2xx, 4xx, 5xx).
* **Status Over Time**: Response status groups stacked over time to identify temporal error spikes.

### Performance & Latency
* **Gateway Latency Percentiles**: P90, P95, and P99 charts showing internal gateway processing time.
* **Endpoint vs Gateway Response Time**: Compares average backend response time with the total gateway response time.
* **Requests vs Avg Response Time**: Correlates request volume with average gateway response time.

### Top Consumers
* **Top 5 APIs**: The most-used APIs by request count (useful when viewing platform-wide dashboards).
* **Top 5 Applications**: The most active consumer applications calling your proxy.
* **Top 5 Plans**: The most heavily used subscription plans.
* **Top 5 Paths**: The most-requested API path mappings.

### Data Volume
* **Request / Response Content Length**: Average request and response payload size in bytes over time.

## Filtering and Drill-down

All dashboard widgets support native dynamic filtering. You can filter data streams by:
* Time range
* Subscription plan
* Consumer application
* Response status code

Selecting segments on doughnut charts or bar charts automatically applies filters to the entire dashboard view.

* [View API logs](view-api-logs.md) — Inspect individual request logs for debugging and audit.
