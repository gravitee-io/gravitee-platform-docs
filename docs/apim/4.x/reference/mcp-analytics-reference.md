## Overview

MCP Analytics Support enables monitoring and visualization of Model Context Protocol (MCP) API usage within the Gravitee API Management platform. Administrators can track request volume, latency, method distribution, and resource/tool/prompt usage through a dedicated dashboard template and new chart components.

## Key Concepts

### MCP Analytics Facets

MCP Analytics introduces four facets for filtering and grouping MCP protocol data: **MCP Proxy Method**, **MCP Proxy Tool**, **MCP Proxy Resource**, and **MCP Proxy Prompt**. Each facet maps to an Elasticsearch field in the `additional-metrics` namespace.

| Facet Name | Elasticsearch Field | Purpose |
|:-----------|:--------------------|:--------|
| `MCP_PROXY_METHOD` | `additional-metrics.keyword_mcp-proxy_method` | Tracks MCP method invocations |
| `MCP_PROXY_TOOL` | `additional-metrics.keyword_mcp-proxy_tools/call` | Tracks tool usage |
| `MCP_PROXY_RESOURCE` | `additional-metrics.keyword_mcp-proxy_resources/read` | Tracks resource access |
| `MCP_PROXY_PROMPT` | `additional-metrics.keyword_mcp-proxy_prompts/get` | Tracks prompt retrieval |

### Widget Types

The platform supports eight widget types for dashboard composition:

* **stats**: Single numeric values
* **doughnut**, **pie**, **polarArea**: Proportional data visualizations
* **time-series-line**: Line charts over time
* **time-series-bar**: Stacked bar charts over time
* **vertical-bar**: Category-based vertical bars
* **horizontal-bar**: Category-based horizontal bars

Time-series widgets display data with time-based x-axes. Category widgets display facets data with category-based axes.

### MCP Dashboard Template

The MCP dashboard template provides a pre-configured view of MCP API usage with 12 widgets:

* Request volume
* Latency percentiles (average, max, P90, P99)
* Method usage (bar chart and time series)
* Resource/tool/prompt usage (top 5 each)
* Response status distribution
* Average response time over time

All widgets filter by `API_TYPE=MCP` and use 1-hour intervals for time-series data. The template applies a 7-day default time range.

## Prerequisites

* Elasticsearch analytics backend configured and operational
* APIs with `API_TYPE=MCP` deployed and generating traffic
* Access to the Gravitee API Management console with dashboard creation permissions:
  * `Environment-dashboard-r`: View dashboards
  * `Environment-dashboard-c`: Create dashboards
  * `Environment-dashboard-u`: Update dashboards
  * `Environment-dashboard-d`: Delete dashboards

## Creating MCP Dashboards

1. Navigate to **Observability** > **Dashboards**.
2. Click **Create dashboard** > **Create from template**.
3. Select the **MCP** template in the left panel and click **Use template**.

The dashboard is created with auto-generated widget IDs and is immediately available for viewing and customization.

## Customizing MCP Dashboards

Administrators can add custom widgets to MCP dashboards by selecting widget types and configuring facets or filters using the four MCP-specific facet names (`MCP_PROXY_METHOD`, `MCP_PROXY_TOOL`, `MCP_PROXY_RESOURCE`, `MCP_PROXY_PROMPT`).

* **Time-series widgets** require an interval (default 10000ms / 5 minutes for 30 buckets).
* **Category widgets** (`vertical-bar`, `horizontal-bar`) require facets data and display a different color per bar with no legend.
* Widgets without an explicit time range inherit the dashboard's default 7-day range.

To adjust filters or timeframe, modify the dashboard settings after creation.

## Restrictions

* MCP analytics require an Elasticsearch backend. Other analytics engines are not supported.
* MCP facets and filters are only available for APIs with `API_TYPE=MCP`.
* Category charts (`vertical-bar`, `horizontal-bar`) require facets data and do not support time-series or measures requests.
* Time-series charts assume all metrics share identical time buckets (same timestamps and order). Mismatched timestamps may produce incorrect visualizations.
* Widget type values have changed: `line` is now `time-series-line`, `bar` is now `time-series-bar`, and `top` is removed (use `vertical-bar` or `horizontal-bar` with facets instead).

## Related Changes

* The MCP dashboard template is added to the template library alongside existing HTTP Proxy and LLM templates.
* Dashboards created from templates now generate unique widget IDs instead of preserving template IDs.
* Widgets without explicit time ranges or intervals receive defaults (7 days, 10000ms).
* Time-series charts replace separate line and bar chart components with a unified component supporting both visualizations.
* Category charts are introduced for facets-based bar charts with category axes.
