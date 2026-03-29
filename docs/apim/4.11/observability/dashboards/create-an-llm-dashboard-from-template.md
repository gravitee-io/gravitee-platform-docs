# Create an LLM Dashboard from Template

## Overview

This guide explains how to create an LLM dashboard from the pre-configured template in the APIM Console. The LLM dashboard provides real-time visibility into token consumption, costs, and usage patterns across LLM providers and models.

Use the LLM dashboard to monitor abnormal behavior, track tool usage, and identify increases in errors.

## Prerequisites

Before you create an LLM dashboard, ensure you have the following permissions:

* `Environment-dashboard-r`: View dashboards
* `Environment-dashboard-c`: Create dashboards
* `Environment-dashboard-u`: Update dashboards
* `Environment-dashboard-d`: Delete dashboards

## Create an LLM dashboard from template

1. Navigate to **Observability > Dashboards**.
2. Click **Create dashboard > Create from template**.
3. Select the **LLM** template in the left panel, and then click **Use template**. The Console creates a new dashboard with a timestamp-based name (e.g., `LLM - 1234567890`) and redirects you to the dashboard view.
4. (Optional) Customize filters or adjust the timeframe using the dashboard controls.

## Verification

Navigate to **Observability > Dashboards**. The new LLM dashboard appears in the list.

## Common pitfalls

If the dashboard displays no data:

* Verify that the backend is running.
* Confirm that LLM requests have been processed and logged to Elasticsearch.


## Next steps

* Monitor LLM usage patterns using the dashboard widgets
* Review dashboard data for unusual activity
