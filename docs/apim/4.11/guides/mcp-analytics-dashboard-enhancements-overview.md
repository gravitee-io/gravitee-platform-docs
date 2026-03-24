# MCP Analytics & Dashboard Enhancements Overview

## Overview

MCP Analytics & Dashboard Enhancements extend the Gravitee analytics platform to support Model Context Protocol (MCP) APIs. This feature enables API administrators to track MCP-specific operations—methods, tools, resources, and prompts—through dedicated facets, filters, and a pre-built dashboard template. It is designed for teams managing MCP integrations who need visibility into protocol-level usage patterns and performance metrics.

## Key Concepts

### MCP Facets and Filters

MCP facets and filters enable segmentation of analytics data by protocol-specific dimensions. Four new facets and filters are available:

* **MCP_PROXY_METHOD**: Tracks MCP proxy methods (e.g., `initialize`, `tools/call`, `resources/read`, `prompts/get`)
* **MCP_PROXY_TOOL**: Tracks MCP tool invocations (e.g., `search`, `fetch`)
* **MCP_PROXY_RESOURCE**: Tracks MCP resource access (e.g., `file:///docs/readme.md`)
* **MCP_PROXY_PROMPT**: Tracks MCP prompt usage (e.g., `summarize`)

Each facet and filter is a keyword-type field supporting `EQ` (equals) and `IN` (in list) operators. These dimensions apply to all HTTP metrics (requests, errors, content length, response time, latency) and map to Elasticsearch fields under the `additional-metrics` namespace:

| Facet/Filter | Elasticsearch Field |
|:-------------|:--------------------|
| MCP_PROXY_METHOD | `additional-metrics.keyword_mcp-proxy_method` |
| MCP_PROXY_TOOL | `additional-metrics.keyword_mcp-proxy_tools/call` |
| MCP_PROXY_RESOURCE | `additional-metrics.keyword_mcp-proxy_resources/read` |
| MCP_PROXY_PROMPT | `additional-metrics.keyword_mcp-proxy_prompts/get` |

### Widget Types

Four new widget types support MCP dashboard visualizations:

* **time-series-line**: Line chart for displaying data over time
* **time-series-bar**: Stacked bar chart for displaying data over time
* **vertical-bar**: Vertical bar chart for displaying comparative data across categories
* **horizontal-bar**: Horizontal bar chart for displaying comparative data across categories

These widget types replace the legacy `line` and `bar` types.

### MCP Dashboard Template

The MCP dashboard template provides a pre-configured analytics view with 12 widgets covering request volume, latency percentiles (average, max, P90, P99), method distribution, resource/tool/prompt usage, response status distribution, and response time trends. The template is labeled with `Focus: 'MCP'` and `Theme: 'AI'` and appears in the dashboard template library alongside HTTP Proxy and LLM templates. Dashboards created from this template receive unique widget IDs and a default 7-day time range.

## Prerequisites

Before using MCP Analytics & Dashboard Enhancements, ensure the following:

* Gravitee API Management platform with analytics enabled
* MCP APIs deployed and configured with `API_TYPE = MCP`
* Elasticsearch backend configured to store analytics data
* MCP proxy instrumentation capturing `additional-metrics` fields (`keyword_mcp-proxy_method`, `keyword_mcp-proxy_tools/call`, `keyword_mcp-proxy_resources/read`, `keyword_mcp-proxy_prompts/get`)

To create or manage MCP dashboards, you must have the following permissions:

* **Environment-dashboard-r**: View dashboards
* **Environment-dashboard-c**: Create dashboards
* **Environment-dashboard-u**: Update dashboards
* **Environment-dashboard-d**: Delete dashboards

## Creating MCP Dashboards

To create an MCP dashboard from the template:

1. Navigate to **Observability** > **Dashboards**.
2. Click **Create dashboard** > **Create from template**.
3. Select the **MCP** template in the left panel and click **Use template**.
4. The dashboard is created and you are redirected to the new dashboard view.
5. Adjust filters or the timeframe to customize the dashboard view.

### Verification

To verify the dashboard was created successfully, navigate back to **Observability** > **Dashboards**. The new MCP dashboard appears in the dashboard list.

{% hint style="warning" %}
If the dashboard displays no data, verify that:
* The Elasticsearch backend is running
* MCP APIs are generating traffic
* The MCP proxy instrumentation is capturing `additional-metrics` fields
{% endhint %}

### Next Steps

After creating an MCP dashboard, you can:

* Create additional custom dashboards
* Add filters to focus on specific MCP methods, tools, resources, or prompts
* Monitor for abnormal behavior, increased errors, or unused tools
