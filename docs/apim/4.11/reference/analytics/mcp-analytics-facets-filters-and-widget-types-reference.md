# MCP Analytics Facets, Filters, and Widget Types Reference

## Overview

MCP Analytics & Dashboard Enhancements extends the Gravitee analytics platform with dedicated tracking for Model Context Protocol (MCP) traffic. It introduces four new facets and filters for MCP-specific dimensions (method, tool, resource, prompt) and a pre-built dashboard template for monitoring MCP API usage, latency, and protocol-level activity. This feature is designed for API administrators managing MCP-enabled APIs and developers integrating MCP analytics into custom dashboards.

## Key Concepts

### MCP Facets and Filters

Four new analytics dimensions enable granular analysis of MCP protocol traffic. Each facet and filter operates on keyword-type fields extracted from request metadata and supports equality (`EQ`) and set membership (`IN`) operators.

| Facet/Filter Name | Label | Elasticsearch Field | Description |
|:------------------|:------|:--------------------|:------------|
| `MCP_PROXY_METHOD` | MCP Method | `additional-metrics.keyword_mcp-proxy_method` | MCP protocol method (e.g., `initialize`, `tools/call`, `resources/read`, `prompts/get`) |
| `MCP_PROXY_TOOL` | MCP Tool | `additional-metrics.keyword_mcp-proxy_tools/call` | Tool invoked via `tools/call` method (e.g., `search`, `fetch`) |
| `MCP_PROXY_RESOURCE` | MCP Resource | `additional-metrics.keyword_mcp-proxy_resources/read` | Resource accessed via `resources/read` method (e.g., `file:///docs/readme.md`) |
| `MCP_PROXY_PROMPT` | MCP Prompt | `additional-metrics.keyword_mcp-proxy_prompts/get` | Prompt retrieved via `prompts/get` method (e.g., `summarize`) |

All four dimensions are available on HTTP-based metrics: `HTTP_REQUESTS`, `HTTP_ERRORS`, `HTTP_REQUEST_CONTENT_LENGTH`, `HTTP_RESPONSE_CONTENT_LENGTH`, `HTTP_ENDPOINT_RESPONSE_TIME`, `HTTP_GATEWAY_RESPONSE_TIME`, and `HTTP_GATEWAY_LATENCY`.

### Widget Types

The analytics platform now supports time-series and categorical chart types. Widget type enumeration has been refactored to distinguish temporal visualizations from category-based comparisons.

| Widget Type | Chart.js Type | Description |
|:------------|:--------------|:------------|
| `time-series-line` | `line` | Line chart for time-series data; applies curved lines (`tension: 0.4`), area fill, and 1px borders |
| `time-series-bar` | `bar` | Stacked bar chart for time-series data |
| `vertical-bar` | `bar` (indexAxis: `x`) | Vertical bar chart for categorical comparisons |
| `horizontal-bar` | `bar` (indexAxis: `y`) | Horizontal bar chart for categorical comparisons |

Legacy widget types (`line`, `bar`) have been replaced by the above types.

### MCP Dashboard Template

A pre-configured dashboard template (`mcp`) provides immediate visibility into MCP API performance and usage patterns. The template includes 12 widgets organized into latency statistics, method distribution, resource/tool/prompt usage, and response status breakdowns. Template labels (`Focus: MCP`, `Theme: AI`) enable filtering in the dashboard gallery.

## Prerequisites

- Gravitee API Management platform with analytics enabled
- Elasticsearch backend configured for analytics storage
- At least one API with `API_TYPE = MCP` deployed and receiving traffic
- MCP proxy configured to populate `additional-metrics` fields (`keyword_mcp-proxy_method`, `keyword_mcp-proxy_tools/call`, `keyword_mcp-proxy_resources/read`, `keyword_mcp-proxy_prompts/get`)

## Gateway Configuration


## Creating MCP Analytics Queries

To analyze MCP traffic, construct analytics queries using the new facets and filters:

1. Select a supported metric (e.g., `HTTP_REQUESTS` with `COUNT` aggregation).
2. Apply the `API_TYPE = MCP` filter to isolate MCP traffic.
3. Add MCP-specific filters (e.g., `MCP_PROXY_METHOD IN [tools/call, resources/read]`) to narrow results.
4. Group results by an MCP facet (e.g., `MCP_PROXY_TOOL`) to break down usage by tool name.
5. Configure time range and interval for time-series queries.

The platform resolves facet and filter names to Elasticsearch field paths automatically.
 
