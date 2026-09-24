---
hidden: false
noIndex: false
description: Read the requests, errors, latency, tokens, and cost of an AI Workspace by model and by user on the AI Workspace Overview dashboard.
---

# Monitor your AI workspaces

The AI Workspace Overview dashboard charts the LLM traffic of AI Workspaces: requests, error rate, response time, tokens, and cost, broken down by model and by user. Each breakdown keeps the top five models or users. For the full ranking of one workspace and a CSV export, use its **Spend** page. See [Track AI workspace spend](../build/track-ai-workspace-spend.md).

## Open the dashboard from a workspace

To open the dashboard for one workspace, complete the following steps:

1. From the Gamma console sidebar, open **Agent Management**.
2. Under **Secure**, open **AI Workspaces**.
3. Select the workspace.
4. Under **Observability**, click **Dashboard**.

    <!-- TODO: Screenshot of the AI Workspace Overview dashboard opened from a workspace, with the AI Workspace filter set to the workspace -->

The dashboard opens in a new tab, filtered to the workspace, on the last 7 days. The **Logs** item under **Observability** opens the logs in a new tab, filtered to the same workspace, on the last 5 minutes.

The **Open in dashboard** button of the **Spend** page opens the same dashboard on the time range the **Spend** page shows.

## Open the dashboard from the Dashboards list

To open the dashboard from the **Dashboards** list, complete the following steps:

1. From the Gamma console sidebar, open **Agent Management**.
2. Under **Observability**, click **Dashboards**.
3. Click the AI Workspace Overview dashboard. The list marks it as a **Template**.

Opened this way, the dashboard covers the LLM traffic of every LLM Proxy you can view in the environment, including LLM Proxies that don't belong to a workspace. To read one workspace, pick it in the **AI Workspace** filter.

## Filter the dashboard

The dashboard carries three filters for you to fill: **AI Workspace**, **Model**, and **User**. A filter you set applies to every widget. Clicking a row of the **Models (top 5 by requests)** table or the **Users (top 5 by cost)** table sets the matching filter. The whole dashboard then narrows to that model or user, and clicking the same row again clears the filter.

## Read the widgets

Note the following points before you read the charts:

* The dashboard counts only traffic on APIs you can view.
* In **Top 5 Models by Requests + P95** and **Errors & Latency by Top 5 Models**, the bars are per model, but the P95 line covers all the traffic the dashboard is filtered to.
* Cost is the token cost the gateway records for each call. For how the gateway computes it, see [Where cost comes from](monitor-your-llm-proxy.md#where-cost-comes-from).

The dashboard is a template and can't be edited. If you can create dashboards, duplicate it as a custom dashboard to change it. See [Build a custom dashboard](dashboards/build-a-custom-dashboard.md).

## Verification

To verify the AI Workspace Overview dashboard is working as expected, follow these steps:

1. Call the workspace entrypoint with a user's API key. See [Assign users to an AI workspace](../build/assign-users-to-an-ai-workspace.md).
2. Open the workspace, and under **Observability**, click **Dashboard**.
3. Confirm the **AI Workspace** filter is set to the workspace, and that **Requests** under **Key Metrics** counts the call.

    <!-- TODO: Screenshot of the AI Workspace Overview dashboard after a call, with the Key Metrics row counting the request -->
