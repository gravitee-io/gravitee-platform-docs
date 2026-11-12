---
noIndex: false
description: Track backend endpoint availability, response times, and failed health checks for an API. Follow the steps to open the Health Check Dashboard.
---

# Monitor endpoint health

The Endpoint Health Check Dashboard provides real-time visibility into the availability and performance of your API's backend endpoints. You can use this dashboard to monitor response times, track failed health checks, and diagnose connectivity issues.

## Prerequisites

* The API is an HTTP Proxy API. A TCP Proxy API has no health checks and no **Health Check Dashboard** item in its sidebar.
* Health checks are configured and enabled on the API's endpoint groups or endpoints. See the health-check step in [Configure endpoints](../build/configure-your-api-proxy/configure-backend-security.md#step-3-health-check).

## View the health check dashboard

1. From the Gamma console sidebar, select **API Management**.
2. Click **API Proxies**.
3. Select an API proxy from the list to view its detail page.
4. In the sidebar, under **Monitoring**, click **Health Check Dashboard**.

## Dashboard metrics

The dashboard covers the period selected in **Timeframe**: **Last minute**, **Last hour**, **Last day**, **Last week**, or **Last month**. The default is **Last day**. To reload the data for the same period, click **Refresh data**.

The following table describes each section of the dashboard:

| Section                                      | What it shows                                                                                                   |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Global availability over selected period** | The share of successful health checks across all endpoints.                                                     |
| **Global average response time**             | The average health check response time across all endpoints.                                                    |
| **Global response time trend**               | The response time of endpoints to health checks over the period. To change the chart, select **Line**, **Area**, or **Bar**. |
| **Availability per endpoint**                | The availability and response time of each endpoint that has health checks enabled.                            |
| **Availability per gateway**                 | The availability and response time recorded by each gateway that runs health checks.                          |
| **Failed health checks**                     | The health checks that failed during the period. See [View failed health checks](#view-failed-health-checks).   |

## View failed health checks

The **Failed health checks** table lists the health checks that failed during the selected period. The following table describes its columns:

| Column            | Description                                  |
| ----------------- | -------------------------------------------- |
| **Timestamp**     | When the health check ran.                   |
| **Endpoint**      | The endpoint that the health check called.   |
| **Gateway**       | The gateway that ran the health check.       |
| **Response Time** | How long the endpoint took to respond.       |

To find out why a health check failed, complete the following steps:

1. In the **Failed health checks** table, find the failed health check.
2. Click **View failure details**. The **Health check detail** panel opens.
3. Review the **Status**, **Endpoint**, **Gateway**, and **Response time** of the health check.
4. Review the request and response captured during each step of the health check to find the cause of the failure.

When a health check captured no details, **View failure details** is unavailable, and its tooltip reads **No details available for this probe**.


## Next steps

* [View API logs](view-api-logs.md)
