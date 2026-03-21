# MCP Analytics Concepts

## Overview

MCP Analytics & Dashboard Enhancements extend the Gravitee analytics platform to support Model Context Protocol (MCP) traffic analysis. This feature enables API administrators to monitor MCP method distribution, tool usage, resource access patterns, and prompt invocations through dedicated facets, filters, and a pre-built dashboard template. It is designed for teams managing MCP-enabled APIs who need visibility into protocol-specific metrics.

## Key Concepts

### MCP Analytics Facets

MCP facets enable grouping and aggregation of analytics data by MCP-specific dimensions. Four facets are available:

* `MCP_PROXY_METHOD`: Groups by MCP method name
* `MCP_PROXY_TOOL`: Groups by tool identifier
* `MCP_PROXY_RESOURCE`: Groups by resource URI
* `MCP_PROXY_PROMPT`: Groups by prompt name

All facets use keyword-type data and are supported across seven HTTP metrics: `HTTP_REQUESTS`, `HTTP_ERRORS`, `HTTP_REQUEST_CONTENT_LENGTH`, `HTTP_RESPONSE_CONTENT_LENGTH`, `HTTP_ENDPOINT_RESPONSE_TIME`, `HTTP_GATEWAY_RESPONSE_TIME`, and `HTTP_GATEWAY_LATENCY`.

| Facet Name | Label | Type | Elasticsearch Field |
|:-----------|:------|:-----|:--------------------|
| `MCP_PROXY_METHOD` | MCP Method | KEYWORD | `additional-metrics.keyword_mcp-proxy_method` |
| `MCP_PROXY_TOOL` | MCP Tool | KEYWORD | `additional-metrics.keyword_mcp-proxy_tools/call` |
| `MCP_PROXY_RESOURCE` | MCP Resource | KEYWORD | `additional-metrics.keyword_mcp-proxy_resources/read` |
| `MCP_PROXY_PROMPT` | MCP Prompt | KEYWORD | `additional-metrics.keyword_mcp-proxy_prompts/get` |

### MCP Analytics Filters

MCP filters restrict analytics queries to specific MCP method, tool, resource, or prompt values. Each filter supports two operators:

* `EQ`: Equals a single value
* `IN`: Matches any value in a list

Filters share the same names and Elasticsearch field mappings as their corresponding facets.

### Widget Types

The analytics platform supports eight widget types for dashboard visualization:

**New widget types:**

* `time-series-line`: Line chart for time-based data with stacked series and 0.4 tension curves
* `time-series-bar`: Stacked bar chart for time-based data
* `vertical-bar`: Vertical bar chart for categorical comparisons with per-bar coloring
* `horizontal-bar`: Horizontal bar chart for categorical comparisons

**Legacy widget types:**

* `stats`: Statistics display
* `doughnut`: Doughnut chart
* `pie`: Pie chart
* `polarArea`: Polar area chart

### MCP Dashboard Template

The MCP dashboard template (`mcp`) provides a pre-configured analytics view with 12 widgets monitoring MCP protocol usage:

**Latency statistics widgets (5):**

* Average latency
* Max latency
* P90 latency
* P99 latency
* Total requests

**Usage distribution widgets (7):**

* Method usage (vertical bar chart)
* Method usage over time (time-series line chart)
* Most used resources (vertical bar, top 5)
* Most used prompts (vertical bar, top 5)
* Most used tools (vertical bar, top 5)
* Response status distribution (doughnut chart)
* Average response time over time (time-series line chart)

All widgets filter to `API_TYPE = MCP` and use 1-hour intervals for time-series data.

## Prerequisites

Before using MCP analytics, ensure the following requirements are met:

* Gravitee API Management platform with analytics enabled
* Elasticsearch cluster configured for analytics storage
* MCP-enabled APIs publishing metrics to the `additional-metrics` field
* Analytics data indexed with MCP-specific keyword fields: `keyword_mcp-proxy_method`, `keyword_mcp-proxy_tools/call`, `keyword_mcp-proxy_resources/read`, `keyword_mcp-proxy_prompts/get`

## Gateway Configuration

## Creating MCP Analytics Queries

To query MCP analytics data, construct an analytics request using the standard HTTP metrics and add MCP facets or filters:

1. Select a metric from the supported list: `HTTP_REQUESTS`, `HTTP_ERRORS`, `HTTP_REQUEST_CONTENT_LENGTH`, `HTTP_RESPONSE_CONTENT_LENGTH`, `HTTP_ENDPOINT_RESPONSE_TIME`, `HTTP_GATEWAY_RESPONSE_TIME`, or `HTTP_GATEWAY_LATENCY`.
2. Add one or more MCP facets to group results by MCP dimensions: `MCP_PROXY_METHOD`, `MCP_PROXY_TOOL`, `MCP_PROXY_RESOURCE`, or `MCP_PROXY_PROMPT`.
3. Optionally add MCP filters with `EQ` or `IN` operators to restrict results to specific method, tool, resource, or prompt values.
