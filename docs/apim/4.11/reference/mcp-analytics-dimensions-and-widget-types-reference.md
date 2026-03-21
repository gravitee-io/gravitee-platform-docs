# MCP Analytics Dimensions and Widget Types Reference

## Overview

MCP Analytics & Dashboard Enhancements extends the Gravitee analytics platform to support Model Context Protocol (MCP) API monitoring. It introduces four keyword-based analytics dimensions for MCP-specific data (method, tool, resource, prompt), a pre-built MCP dashboard template with 11 widgets, and refactored chart components to support time-series and categorical visualizations. This feature is designed for API administrators and developers managing MCP integrations.

## Key Concepts

### MCP Analytics Dimensions

MCP Analytics introduces four keyword-based facets and filters that enable segmentation and filtering of HTTP metrics by MCP protocol elements. Each dimension maps to an Elasticsearch field in the `additional-metrics` namespace and supports all standard HTTP metrics.

| Dimension | UI Label | Elasticsearch Field | Description |
|:----------|:---------|:--------------------|:------------|
| `MCP_PROXY_METHOD` | MCP Method | `additional-metrics.keyword_mcp-proxy_method` | The MCP protocol method (e.g., `initialize`, `tools/call`, `resources/read`, `prompts/get`) |
| `MCP_PROXY_TOOL` | MCP Tool | `additional-metrics.keyword_mcp-proxy_tools/call` | The specific tool invoked in a `tools/call` request (e.g., `search`, `fetch`) |
| `MCP_PROXY_RESOURCE` | MCP Resource | `additional-metrics.keyword_mcp-proxy_resources/read` | The resource URI accessed in a `resources/read` request (e.g., `file:///docs/readme.md`) |
| `MCP_PROXY_PROMPT` | MCP Prompt | `additional-metrics.keyword_mcp-proxy_prompts/get` | The prompt name retrieved in a `prompts/get` request (e.g., `summarize`) |

All MCP dimensions are keyword-based and support the following HTTP metrics:

* `HTTP_REQUESTS`
* `HTTP_ERRORS`
* `HTTP_REQUEST_CONTENT_LENGTH`
* `HTTP_RESPONSE_CONTENT_LENGTH`
* `HTTP_ENDPOINT_RESPONSE_TIME`
* `HTTP_GATEWAY_RESPONSE_TIME`
* `HTTP_GATEWAY_LATENCY`

### Widget Types

The analytics platform supports eight widget types for visualizing MCP data. Time-series widgets display data over time with configurable intervals; category widgets display comparative data across discrete values.

| Widget Type | Description | Primary Use Case |
|:------------|:------------|:-----------------|
| `stats` | Single numeric value | Display aggregate metrics (count, average, max, percentiles) |
| `doughnut` | Circular segmented chart | Show proportional distribution (e.g., status code groups) |
| `pie` | Circular segmented chart | Show proportional distribution |
| `polarArea` | Radial segmented chart | Show proportional distribution with emphasis on magnitude |
| `time-series-line` | Line chart over time | Track metric trends (e.g., request volume, latency over time) |
| `time-series-bar` | Stacked bar chart over time | Track metric trends with categorical breakdown |
| `vertical-bar` | Vertical bar chart | Compare values across categories (e.g., top methods, tools) |
| `horizontal-bar` | Horizontal bar chart | Compare values across categories |

### MCP Dashboard Template

The MCP dashboard template (`mcp`) provides a pre-configured 11-widget layout for monitoring MCP API usage. It includes request volume and latency statistics, method distribution over time, top resources/tools/prompts, response status breakdown, and average response time trends.

**Template Metadata:**

* **Template ID:** `mcp`
* **Labels:** `Focus: MCP`, `Theme: AI`
* **Preview Image:** `assets/images/templates/mcp-preview.png`

When a dashboard is created from this template, each widget receives a unique ID generated via `crypto.randomUUID()` to prevent ID collisions.

## Gateway Configuration

