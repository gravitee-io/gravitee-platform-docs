# How-To: Create an LLM Dashboard from Template

## Overview

This guide explains how to create an LLM analytics dashboard from the pre-configured template in the APIM Console. The LLM dashboard provides a centralized view of token consumption, costs, and usage patterns for Large Language Model integrations.

Use this dashboard to monitor LLM usage across your environment, identify underutilized tools, detect abnormal behavior, and track error trends.

## Prerequisites

Before you create an LLM dashboard, ensure you have the following permissions:

* **Environment-dashboard-r**: View dashboards
* **Environment-dashboard-c**: Create dashboards
* **Environment-dashboard-u**: Update dashboards
* **Environment-dashboard-d**: Delete dashboards

## Create an LLM dashboard from template

1. Navigate to **Observability** > **Dashboards**.



2. Click **Create dashboard** > **Create from template**.

3. Select the **LLM** template in the left panel, and then click **Use template**.



4. The Console redirects you to your new dashboard.



5. (Optional) Adjust filters or the timeframe to refine the displayed data.



## Verification

To confirm the dashboard was created successfully, navigate to **Observability** > **Dashboards**. Your new LLM dashboard appears in the list.

## Common pitfalls

If the dashboard displays no data or fails to load:

* **Backend not started**: Ensure the analytics backend is running and accessible.
* **No data available**: Verify that LLM requests have been processed and that analytics data has been ingested into Elasticsearch.

## Next steps

After creating your LLM dashboard, you can:

* [Create custom dashboards](../dashboards/create-a-dashboard.md) tailored to specific use cases
* Add filters to focus on particular models, providers, or time periods
* Analyze suspect behaviors by reviewing response status distributions and cost trends
