# MCP Analytics Support

## Overview

MCP Analytics Support enables monitoring and visualization of Model Context Protocol (MCP) API usage through dedicated facets, filters, and dashboard templates. Platform administrators can track MCP method distribution, tool invocations, resource access, and prompt usage alongside standard gateway performance metrics.

## Key Concepts

### MCP Facets and Filters


MCP Analytics adds four facets and filters for segmenting analytics data by MCP protocol elements.
 Each facet maps to an Elasticsearch field capturing MCP-specific metadata from API requests.

| Facet/Filter Name | Elasticsearch Field | Purpose |
|:------------------|:--------------------|:--------|
| `MCP_PROXY_METHOD` | `additional-metrics.keyword_mcp-proxy_method` | MCP method name (e.g., `initialize`, `tools/call`) |
| `MCP_PROXY_TOOL` | `additional-metrics.keyword_mcp-proxy_tools/call` | MCP tool identifier |
| `MCP_PROXY_RESOURCE` | `additional-metrics.keyword_mcp-proxy_resources/read` | MCP resource identifier |
| `MCP_PROXY_PROMPT` | `additional-metrics.keyword_mcp-proxy_prompts/get` | MCP prompt identifier |

### Dashboard Widgets

The MCP dashboard template includes 12 pre-configured widgets covering request volume, average response time, latency percentiles (P90, P99), method distribution over time, and top-5 rankings for resources, prompts, and tools. Widgets use the `vertical-bar`, `time-series-line`, and `doughnut` chart types.

### Widget Types

Analytics dashboards support eight widget types for visualizing MCP data:

| Widget Type | Description |
|:------------|:------------|
| `stats` | Single numeric value (e.g., total requests, average latency) |
| `doughnut` | Proportional data with center cutout |
| `pie` | Proportional data as full circle |
| `polarArea` | Proportional data with varying radii |
| `time-series-line` | Line chart for temporal trends |
| `time-series-bar` | Stacked bar chart for temporal data |
| `vertical-bar` | Vertical bar chart for category comparisons |
| `horizontal-bar` | Horizontal bar chart for category comparisons |

{% hint style="warning" %}
**Breaking Change**: Widget types `top`, `bar`, and `line` have been removed. Use `time-series-line`, `time-series-bar`, `vertical-bar`, or `horizontal-bar` instead.
{% endhint %}

## Prerequisites

Before creating MCP dashboards, ensure the following:

* Elasticsearch analytics backend configured and operational
* MCP APIs deployed with `API_TYPE = MCP` metadata
* Gateway configured to capture MCP protocol metadata in analytics events

Required permissions:

* `Environment-dashboard-r`: View dashboards
* `Environment-dashboard-c`: Create dashboards
* `Environment-dashboard-u`: Update dashboards
* `Environment-dashboard-d`: Delete dashboards

## Gateway Configuration

## Creating MCP Dashboards

1. Navigate to **Observability** > **Dashboards** in the Gravitee console.
2. Click **Create dashboard** > **Create from template**.
3. Select the **MCP** template from the left panel and click **Use template**.

The template provisions 11 widgets covering request volume (`mcp-requests`), latency statistics (`mcp-average-latency`, `mcp-max-latency`, `mcp-p90-latency`, `mcp-p99-latency`), method usage distribution (`mcp-method-usage`, `mcp-method-usage-over-time`), top resources (`mcp-most-used-resources`), response status breakdown (`mcp-response-status-repartition`), and top prompts and tools (`mcp-most-used-prompts`, `mcp-most-used-tools`). Each widget receives a unique UUID and a default time range during creation. Customize widget filters, metrics, or chart types after creation to focus on specific MCP methods, tools, or resources.

## Filtering and Segmenting MCP Data

Apply MCP facets and filters in analytics queries to segment data by protocol element:

* Use `MCP_PROXY_METHOD` to compare usage across MCP methods (e.g., `initialize` vs. `tools/call`)
* Use `MCP_PROXY_TOOL` to identify the most-invoked tools
* Use `MCP_PROXY_RESOURCE` to track resource access patterns
* Use `MCP_PROXY_PROMPT` to analyze prompt usage

Combine MCP filters with standard filters like `HTTP_STATUS_CODE_GROUP` or `API_TYPE` to isolate error rates or latency for specific MCP operations. All MCP facets and filters are available in the Analytics API and console UI for custom dashboard creation.

## End-User Configuration

No end-user configuration is required beyond dashboard creation and filter customization.

## Restrictions

* MCP analytics require an Elasticsearch backend; other analytics engines are not supported.
* MCP facets and filters apply only to APIs with `API_TYPE = MCP`.
* Widget type migration from `top`, `bar`, and `line` to new types is not automated; existing dashboards must be manually updated.
* The `gd-category-chart` component does not support time-series data; use `time-series-line` or `time-series-bar` for temporal visualizations.

## Related Changes

Dashboard widgets created from templates now receive unique UUIDs via `crypto.randomUUID()` instead of static IDs. Widgets without explicit time ranges receive a default range during dashboard creation. The `gd-line-chart` and `gd-bar-chart` components have been unified into `gd-time-series-chart` with a `type` input (`time-series-line` or `time-series-bar`). A new `gd-category-chart` component supports vertical and horizontal bar charts for facets data, assigning distinct colors per bar from the `CHART_COLORS` palette.
