# Create an MCP Dashboard from Template

## Overview

This guide explains how to create an MCP dashboard from the template library in the APIM Console. The MCP dashboard monitors Model Context Protocol usage for an environment, including method distribution, tool usage, and gateway performance.

Use this dashboard to identify unused tools, monitor abnormal behavior, or investigate increases in errors.

## Prerequisites

Before you create an MCP dashboard, ensure you have the following permissions:

* Environment-dashboard-r
* Environment-dashboard-c
* Environment-dashboard-u
* Environment-dashboard-d

## Create an MCP dashboard from template

1. Navigate to **Observability > Dashboards**.
2. Click **Create dashboard > Create from template**.
3. Select the **MCP** template from the left panel and click **Use template**.

    You are redirected to the new dashboard.

4. (Optional) Change filters or adjust the timeframe.

## Verification

To confirm the dashboard was created successfully, navigate to **Observability > Dashboards**. The new MCP dashboard appears in the list.

## Common pitfalls

If the dashboard displays no data or fails to load:

* Verify the analytics backend is running.
* Confirm MCP API requests have been processed and analytics data is available.

## Next steps

After creating the MCP dashboard, you can:

* Create custom dashboards
* Add filters to refine displayed data
* Investigate suspect behaviors identified in the dashboard
