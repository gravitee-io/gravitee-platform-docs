# MCP Analytics Dimensions and Widget Types

## MCP Analytics Dimensions

MCP APIs expose four analytics dimensions for filtering and faceting:

* **MCP_PROXY_METHOD**: Protocol operations such as `initialize`, `tools/call`, `resources/read`, and `prompts/get`
* **MCP_PROXY_TOOL**: Specific tools invoked via `tools/call`
* **MCP_PROXY_RESOURCE**: Resources accessed via `resources/read`
* **MCP_PROXY_PROMPT**: Prompts retrieved via `prompts/get`

All dimensions support `EQ` and `IN` operators and are indexed as keyword facets in Elasticsearch under the `additional-metrics` namespace.

### Elasticsearch Field Mappings

| Dimension | Elasticsearch Field |
|:----------|:-------------------|
| `MCP_PROXY_METHOD` | `additional-metrics.keyword_mcp-proxy_method` |
| `MCP_PROXY_TOOL` | `additional-metrics.keyword_mcp-proxy_tools/call` |
| `MCP_PROXY_RESOURCE` | `additional-metrics.keyword_mcp-proxy_resources/read` |
| `MCP_PROXY_PROMPT` | `additional-metrics.keyword_mcp-proxy_prompts/get` |

## Widget Types

The platform supports eight widget types for visualizing analytics data:

### Time-Series Widgets

Time-series widgets display data over time and default to a 7-day time range with 5-minute intervals.

* **time-series-line**: Line chart for displaying data over time
* **time-series-bar**: Stacked bar chart for displaying data over time

### Category Widgets

Category widgets display proportional or comparative distributions and default to displaying up to 10 items.

* **stats**: Single metric value
* **doughnut**: Proportional distribution (doughnut chart)
* **pie**: Proportional distribution (pie chart)
* **polarArea**: Proportional distribution (polar area chart)
* **vertical-bar**: Comparative data across categories (vertical bars)
* **horizontal-bar**: Comparative data across categories (horizontal bars)

### MCP Dashboard Template

The `mcp` template provides 12 pre-configured widgets that monitor MCP request volume, latency percentiles (P90, P99), method distribution over time, top resources/prompts/tools, and response status breakdown. All widgets filter on `API_TYPE = MCP` and use the new time-series and category chart components.

