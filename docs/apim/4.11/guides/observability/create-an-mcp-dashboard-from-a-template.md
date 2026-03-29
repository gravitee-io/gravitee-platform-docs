# Create an MCP Dashboard from a Template

## Overview

This guide explains how to create an MCP analytics dashboard from the built-in template. The MCP dashboard template provisions 12 pre-configured widgets that visualize MCP protocol usage, including request volume, latency metrics, method distribution, and top resources, prompts, and tools.

Use this dashboard to monitor MCP API usage in your environment, identify unused tools, detect abnormal behavior, and track error trends.

## Prerequisites

Before you create an MCP dashboard, ensure you have the following permissions:

* `Environment-dashboard-r`: View dashboards
* `Environment-dashboard-c`: Create dashboards
* `Environment-dashboard-u`: Update dashboards
* `Environment-dashboard-d`: Delete dashboards

## Create an MCP dashboard from template

1. Navigate to **Observability > Dashboards**.
2. Click **Create dashboard > Create from template**.
3. Select the **MCP** template in the left panel and click **Use template**.
4. (Optional) Adjust filters or the timeframe using the controls at the top of the dashboard.

## Verification

To confirm the dashboard was created successfully, navigate back to **Observability > Dashboards**. The new MCP dashboard appears in the list.

## Common pitfalls

If the dashboard displays no data or fails to load:

* **Backend not started**: Verify that the analytics backend is running.
* **No data available**: Confirm that MCP APIs are deployed and receiving traffic.

## Next steps

After creating the MCP dashboard, you can:

* Create custom dashboards tailored to specific monitoring requirements
* Add filters to segment data by API, application, or time range
* Analyze suspect behaviors such as error spikes or latency anomalies
