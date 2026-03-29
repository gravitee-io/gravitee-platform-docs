# Create an LLM Dashboard from Template

## Overview

This guide explains how to create an LLM monitoring dashboard from a pre-configured template using the Console UI. The LLM dashboard provides a centralized view of LLM usage, token consumption, and costs across your environment.

Use this dashboard to:

* Monitor whether LLM tools are being used
* Detect abnormal behavior patterns
* Track increases in errors
* Analyze token consumption and associated costs

## Prerequisites

Before you create an LLM dashboard, ensure you have the following permissions:

* `Environment-dashboard-r`: View dashboards
* `Environment-dashboard-c`: Create dashboards
* `Environment-dashboard-u`: Update dashboards
* `Environment-dashboard-d`: Delete dashboards

## Create an LLM dashboard from template

1. Navigate to **Observability > Dashboards**.
2. Click **Create dashboard > Create from template**.
3. Select the **LLM** template in the left panel, and then click **Use template**. The Console redirects you to the new dashboard.
4. (Optional) Adjust the filters or timeframe to refine the displayed data.

## Verification

Navigate to **Observability > Dashboards**. The new LLM dashboard appears in the list of available dashboards.

## Common pitfalls

If the dashboard displays no data, verify the following:

* The backend is running
* LLM requests have been processed and analytics data is available

## Next steps

After creating the LLM dashboard, you can:

* Create a custom dashboard
* Add filters to refine displayed metrics
* Analyze suspect behaviors or usage patterns
