# MCP Dashboard Template Reference

## Widget Types

The platform supports eight widget visualization types:

| Type | Description |
|:-----|:------------|
| `stats` | Single numeric value display |
| `doughnut` | Proportional data with center cutout |
| `pie` | Proportional data as circular segments |
| `polarArea` | Proportional data with varying radii |
| `time-series-line` | Line chart for temporal data |
| `time-series-bar` | Stacked bar chart for temporal data |
| `vertical-bar` | Vertical bar chart for categorical comparison |
| `horizontal-bar` | Horizontal bar chart for categorical comparison |

## MCP Dashboard Template

<!-- GAP: Verify template name, widget count, filter configuration, and label values against source materials -->

A pre-built dashboard template named **"MCP"** provides centralized monitoring of MCP API usage. The template includes 12 widgets covering request volume, latency percentiles, method distribution, resource/tool/prompt usage, and response status distribution. All widgets filter by `API_TYPE = 'MCP'`. The template is labeled with `Focus: 'MCP'` and `Theme: 'AI'`.

### MCP Dashboard Widgets

The MCP template includes the following widgets:

| Widget ID | Title | Type | Metric | Description |
|:----------|:------|:-----|:-------|:------------|
| `mcp-requests` | MCP requests | stats | `HTTP_REQUESTS` | Total number of requests targeting MCP APIs |
| `mcp-average-latency` | Average latency | stats | `HTTP_GATEWAY_LATENCY` (avg) | Average gateway latency for MCP requests |
| `mcp-max-latency` | Max latency | stats | `HTTP_GATEWAY_LATENCY` (max) | Maximum gateway latency observed |
| `mcp-p90-latency` | P90 latency | stats | `HTTP_GATEWAY_LATENCY` (p90) | 90th percentile gateway latency |
| `mcp-p99-latency` | P99 latency | stats | `HTTP_GATEWAY_LATENCY` (p99) | 99th percentile gateway latency |
| `mcp-method-usage` | Method usage | vertical-bar | `HTTP_REQUESTS` by `MCP_PROXY_METHOD` | Top 10 MCP methods by request count |
| `mcp-method-usage-over-time` | Method usage over time | time-series-line | `HTTP_REQUESTS` by `MCP_PROXY_METHOD` | Evolution of method usage over time |
| `mcp-most-used-resources` | Most used Resources | vertical-bar | `HTTP_REQUESTS` by `MCP_PROXY_RESOURCE` | Top 5 most used MCP resources |
| `mcp-response-status-repartition` | Response status repartition | doughnut | `HTTP_REQUESTS` by status code | Distribution of HTTP response statuses |
| `mcp-most-used-prompts` | Most used Prompts | vertical-bar | `HTTP_REQUESTS` by `MCP_PROXY_PROMPT` | Top 5 most used MCP prompts |
| `mcp-most-used-tools` | Most used Tools | vertical-bar | `HTTP_REQUESTS` by `MCP_PROXY_TOOL` | Top 5 most used MCP tools |
| `mcp-average-response-time` | Average response time | time-series-line | `HTTP_GATEWAY_RESPONSE_TIME` (avg) | Average gateway response time over time |


## Restrictions

* MCP facets and filters apply only to HTTP metrics; they are not available for other metric types
* All MCP filters support only `EQ` and `IN` operators; range or pattern-matching operators are not supported
* Widget type values changed in this release: `'line'` → `'time-series-line'`, `'bar'` → `'time-series-bar'`; existing dashboards using legacy type values must be migrated

## Related Changes

Chart components were refactored to separate time-series visualizations (`TimeSeriesChartComponent` for `time-series-line` and `time-series-bar`) from category-based visualizations (`CategoryChartComponent` for `vertical-bar` and `horizontal-bar`). Widget type enumeration in the OpenAPI schema now includes eight distinct visualization types.
