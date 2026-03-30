# Create an MCP Dashboard from Template

## Overview

This guide explains how to create an MCP dashboard from the pre-configured template in the Gravitee console. The MCP dashboard provides a centralized view of Model Context Protocol API usage, including request volume, latency, method distribution, and resource/tool/prompt usage.

Use this dashboard to monitor MCP API behavior, identify unused tools, detect abnormal usage patterns, and track error rates.

## Prerequisites

Before you create an MCP dashboard, ensure you have the following permissions:

* **Environment-dashboard-r**: View dashboards
* **Environment-dashboard-c**: Create dashboards
* **Environment-dashboard-u**: Update dashboards
* **Environment-dashboard-d**: Delete dashboards

## Create an MCP dashboard from template

1. Navigate to **Observability > Dashboards**.

    <figure><img src=".gitbook/assets/mcp-dashboard-step1.png" alt=""><figcaption></figcaption></figure>

2. Click **Create dashboard > Create from template**.

    Select the **MCP** template in the left panel, and then click **Use template**.

    <figure><img src=".gitbook/assets/mcp-dashboard-step2.png" alt=""><figcaption></figcaption></figure>

3. You are redirected to your new dashboard.

    <figure><img src=".gitbook/assets/mcp-dashboard-step3.png" alt=""><figcaption></figcaption></figure>

4. (Optional) Adjust filters or the timeframe.

    <figure><img src=".gitbook/assets/mcp-dashboard-step4.png" alt=""><figcaption></figcaption></figure>

## Verification

Navigate to **Observability > Dashboards**. Your new MCP dashboard appears in the list.

## Common pitfalls

If the dashboard displays no data:

* Verify that the analytics backend is running.
* Confirm that MCP API traffic has been recorded in the environment.


## Next steps

* Create additional dashboards from templates or customize existing dashboards
* Adjust dashboard filters and timeframes to focus on specific MCP API usage patterns
* Monitor dashboard widgets for unusual patterns in MCP API usage
