# MCP Analytics Facets and Dashboard Templates

## Overview

MCP Analytics and Dashboard Enhancements extend the Gravitee analytics platform to support Model Context Protocol (MCP) APIs. This feature introduces MCP-specific analytics facets, filters, and a pre-built dashboard template for monitoring MCP protocol usage, method distribution, and gateway performance. It also refactors chart components to support time-series and categorical visualizations with improved widget type semantics.

## Key Concepts

### MCP Analytics Facets

MCP-specific facets enable aggregation and filtering of analytics data by MCP protocol dimensions. Four facets are available:

* **MCP_PROXY_METHOD**: MCP method invoked
* **MCP_PROXY_TOOL**: Tool called via MCP
* **MCP_PROXY_RESOURCE**: Resource read via MCP
* **MCP_PROXY_PROMPT**: Prompt retrieved via MCP

Each facet maps to an Elasticsearch field in the `additional-metrics` namespace:

| Facet/Filter Name | Elasticsearch Field |
|:------------------|:--------------------|
| `MCP_PROXY_METHOD` | `additional-metrics.keyword_mcp-proxy_method` |
| `MCP_PROXY_TOOL` | `additional-metrics.keyword_mcp-proxy_tools/call` |
| `MCP_PROXY_RESOURCE` | `additional-metrics.keyword_mcp-proxy_resources/read` |
| `MCP_PROXY_PROMPT` | `additional-metrics.keyword_mcp-proxy_prompts/get` |

### Widget Types

Widget types define how analytics data is visualized. This release introduces four new widget types and deprecates two legacy types:

| Widget Type | Description |
|:------------|:------------|
| `time-series-line` | Line chart for time-series data |
| `time-series-bar` | Stacked bar chart for time-series data |
| `vertical-bar` | Vertical bar chart for categorical data |
| `horizontal-bar` | Horizontal bar chart for categorical data |

Legacy widget types `line` and `bar` are deprecated in favor of `time-series-line` and `time-series-bar`. Widget type `top` has been removed with no replacement.

### MCP Dashboard Template

The MCP dashboard template provides a pre-configured analytics view for MCP APIs. It includes 12 widgets:

* Total requests
* Average latency
* Max latency
* P90 latency
* P99 latency
* Method usage distribution (vertical bar)
* Method usage over time (time-series line)
* Top 5 resources
* Response status distribution (doughnut)
* Top 5 prompts
* Top 5 tools
* Average response time over time (time-series line)

The template is labeled with `Focus: MCP` and `Theme: AI`.

## Prerequisites

Before creating MCP analytics dashboards, ensure the following:

* Elasticsearch backend configured with `additional-metrics` field support
* Gravitee API Management platform with analytics enabled
* MCP APIs deployed and generating analytics data

## Gateway Configuration

## Creating MCP Analytics Dashboards

To create an MCP analytics dashboard, select the MCP template from the template library. The template is identified by the label `Focus: MCP` and `Theme: AI`.

Upon creation, the platform generates unique widget IDs using `crypto.randomUUID()` and injects a default time range of `{ from: 'now-7d', to: 'now' }` with a 10000 ms interval (5 minutes per bucket, 30 buckets total). The dashboard includes 12 pre-configured widgets covering request volume, latency percentiles, method distribution, resource/prompt/tool usage, and response status distribution.

Customize widget filters, time ranges, and chart types as needed after creation.

## Filtering and Aggregating MCP Data

To filter or aggregate analytics data by MCP dimensions, use the four MCP-specific facet and filter names in analytics API requests: `MCP_PROXY_METHOD`, `MCP_PROXY_TOOL`, `MCP_PROXY_RESOURCE`, and `MCP_PROXY_PROMPT`. These names are available in the `FacetName` and `FilterName` enumerations in the analytics OpenAPI schema.

Apply filters at the request level (not metric level) to scope queries to specific MCP methods, tools, resources, or prompts. Facets return aggregated counts for each dimension value, enabling top-N queries (e.g., top 5 most-used tools).

## End-User Configuration

After creating a dashboard, you can customize widget filters, time ranges, and chart types. To verify successful dashboard creation, navigate back to **Dashboards**. Your new dashboard appears in the list.

Common issues:

* **Analytics backend not started**: Ensure the Elasticsearch backend is running.
* **No data displayed**: Verify that MCP APIs are deployed and generating analytics data.

## Restrictions

* MCP analytics require Elasticsearch backend with `additional-metrics` field support. Other analytics backends don't support MCP facets.
* Widget IDs from templates are replaced during dashboard creation. References to static template IDs will break.
* Time-series charts assume all metrics share the same time buckets (same timestamps and order).
* Nested bucket detection in time-series data requires at least one time bucket with a non-empty `buckets` array.
* Color palette cycles after 10 datasets. Datasets beyond index 9 reuse colors.

## Related Changes

The analytics OpenAPI schema now includes four MCP-specific facet and filter names and four new widget type enumerations. Chart components have been refactored: `LineChartComponent` and `BarChartComponent` are replaced by `TimeSeriesChartComponent` (selector `gd-time-series-chart`), and a new `CategoryChartComponent` (selector `gd-category-chart`) supports vertical and horizontal bar charts for categorical data.

The HTTP Proxy and LLM dashboard templates have been updated to use the new widget types and move filters from metric-level to request-level. Widget ID generation now uses `crypto.randomUUID()` instead of static IDs, and the dashboard service injects default time ranges and intervals into widget requests.

