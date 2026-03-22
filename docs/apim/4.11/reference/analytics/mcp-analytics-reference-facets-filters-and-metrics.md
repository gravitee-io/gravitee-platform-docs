# MCP Analytics Reference: Facets, Filters, and Metrics

## Overview

MCP Analytics & Dashboard Enhancements extend the Gravitee analytics platform to support Model Context Protocol (MCP) APIs. This feature enables administrators to track MCP-specific request patterns — including method types, tool invocations, resource access, and prompt usage — alongside standard HTTP metrics. A pre-built dashboard template provides immediate visibility into MCP API performance and usage trends.

## Key Concepts

### MCP Facets and Filters

MCP facets and filters enable segmentation of analytics data by MCP-specific dimensions. All four facets and filters use the `KEYWORD` type and support `EQ` and `IN` operators.

| Name | Display Label | Purpose |
|:-----|:--------------|:--------|
| `MCP_PROXY_METHOD` | MCP Method | Segment by MCP protocol method (e.g., `initialize`, `tools/call`, `resources/read`, `prompts/get`) |
| `MCP_PROXY_TOOL` | MCP Tool | Segment by tool name invoked via `tools/call` |
| `MCP_PROXY_RESOURCE` | MCP Resource | Segment by resource URI accessed via `resources/read` |
| `MCP_PROXY_PROMPT` | MCP Prompt | Segment by prompt name requested via `prompts/get` |

#### Elasticsearch Field Mappings

MCP filter and facet names map to Elasticsearch fields under the `additional-metrics` namespace:

| Filter/Facet Name | Elasticsearch Field |
|:------------------|:--------------------|
| `MCP_PROXY_METHOD` | `additional-metrics.keyword_mcp-proxy_method` |
| `MCP_PROXY_TOOL` | `additional-metrics.keyword_mcp-proxy_tools/call` |
| `MCP_PROXY_RESOURCE` | `additional-metrics.keyword_mcp-proxy_resources/read` |
| `MCP_PROXY_PROMPT` | `additional-metrics.keyword_mcp-proxy_prompts/get` |

### Supported Metrics

All HTTP metrics support MCP facets and filters: `HTTP_REQUESTS`, `HTTP_ERRORS`, `HTTP_REQUEST_CONTENT_LENGTH`, `HTTP_RESPONSE_CONTENT_LENGTH`, `HTTP_ENDPOINT_RESPONSE_TIME`, `HTTP_GATEWAY_RESPONSE_TIME`, and `HTTP_GATEWAY_LATENCY`. Facets and filters apply identically across all metrics.

### Widget Types

The analytics platform supports seven widget types for visualizing MCP data:

| Type | Description |
|:-----|:------------|
| `doughnut` | Circular chart for proportional data |
| `pie` | Circular chart divided into slices |
| `polarArea` | Circular chart with variable radius |
| `time-series-line` | Line chart for data over time; supports stacked datasets |
| `time-series-bar` | Stacked bar chart for data over time |
| `vertical-bar` | Vertical bar chart for categorical comparisons |
| `horizontal-bar` | Horizontal bar chart for categorical comparisons |

{% hint style="warning" %}
The `top`, `bar`, and `line` widget types have been removed. Existing dashboards using these types must migrate to the time-series and category chart types.
{% endhint %}

{% hint style="info" %}
Widget IDs are generated using `crypto.randomUUID()` when creating a dashboard from a template. This requires a browser that supports the Web Crypto API.
{% endhint %}

## Prerequisites

Before using MCP analytics, ensure the following:

* Gravitee API Management platform with analytics enabled
* Elasticsearch cluster configured for analytics storage
* MCP APIs deployed and generating traffic
* User permissions:
  * `Environment-dashboard-r`
  * `Environment-dashboard-c`
  * `Environment-dashboard-u`
  * `Environment-dashboard-d`


<!-- GAP: Gateway configuration section is empty. Requires SME input on required Gateway settings for MCP analytics collection. -->

<!-- GAP: Query construction section lacks API endpoint, request format, and response structure. Requires SME input to provide actionable query examples with concrete API calls and expected responses. -->
