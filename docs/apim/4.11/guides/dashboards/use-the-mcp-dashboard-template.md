# Use the MCP Dashboard Template

## Using the MCP Dashboard Template

The MCP dashboard template provides a pre-configured view of MCP API usage and performance. To create a dashboard from the template:

1. Navigate to **Observability > Dashboards**.
2. Click **Create dashboard > Create from template**.
3. Select the **MCP** template from the left panel.
4. Click **Use template**.

The platform generates unique widget IDs and applies the template's initial configuration. The dashboard includes 12 widgets:

* **Five stats widgets:** Request count, average latency, max latency, P90 latency, and P99 latency
* **Four vertical bar charts:** Method usage (top 10 methods), resource usage (top 5 resources), tool usage (top 5 tools), and prompt usage (top 5 prompts)
* **One doughnut chart:** Response status distribution
* **Two time-series line charts:** Method usage over time and average response time

All widgets filter to `API_TYPE = MCP` where applicable.

### Widget Configuration

The following table describes the widgets included in the MCP dashboard template:

| Widget | Type | Metric | Facet/Filter | Display Limit |
|:-------|:-----|:-------|:-------------|:--------------|
| MCP requests | `stats` | `HTTP_REQUESTS` (COUNT) | `API_TYPE = MCP` | N/A |
| Average latency | `stats` | `HTTP_GATEWAY_LATENCY` | `API_TYPE = MCP` | N/A |
| Max latency | `stats` | `HTTP_GATEWAY_LATENCY` (MAX) | `API_TYPE = MCP` | N/A |
| P90 latency | `stats` | `HTTP_GATEWAY_LATENCY` (P90) | `API_TYPE = MCP` | N/A |
| P99 latency | `stats` | `HTTP_GATEWAY_LATENCY` (P99) | `API_TYPE = MCP` | N/A |
| Method usage | `vertical-bar` | `HTTP_REQUESTS` (COUNT) | `MCP_PROXY_METHOD` facet | Top 10 |
| Method usage over time | `time-series-line` | `HTTP_REQUESTS` (COUNT) | `MCP_PROXY_METHOD` facet | N/A |
| Most used Resources | `vertical-bar` | `HTTP_REQUESTS` (COUNT) | `MCP_PROXY_RESOURCE` facet | Top 5 |
| Response status repartition | `doughnut` | `HTTP_REQUESTS` (COUNT) | `HTTP_STATUS_CODE_GROUP` facet, `API_TYPE = MCP` filter | N/A |
| Most used Prompts | `vertical-bar` | `HTTP_REQUESTS` (COUNT) | `MCP_PROXY_PROMPT` facet | Top 5 |
| Most used Tools | `vertical-bar` | `HTTP_REQUESTS` (COUNT) | `MCP_PROXY_TOOL` facet | Top 5 |
| Average response time | `time-series-line` | `HTTP_GATEWAY_RESPONSE_TIME` | `API_TYPE = MCP` | N/A |

## End-User Configuration

<!-- GAP: No information about customizing the template after creation or modifying widget configurations -->

## Restrictions

* MCP facets and filters apply only to HTTP metrics.
* Widget ID generation uses `crypto.randomUUID()`, which requires a modern browser or Node.js environment.
* The `top`, `bar`, and `line` widget types are no longer supported. Existing dashboards using these types must migrate to `time-series-line`, `time-series-bar`, `vertical-bar`, or `horizontal-bar`.

## Related Changes

The analytics schema now includes four MCP-specific facet and filter names: `MCP_PROXY_METHOD`, `MCP_PROXY_TOOL`, `MCP_PROXY_RESOURCE`, and `MCP_PROXY_PROMPT`. These facets group results by dimension and map to Elasticsearch fields under the `additional-metrics` namespace:

| Facet/Filter Name | Elasticsearch Field |
|:------------------|:--------------------|
| `MCP_PROXY_METHOD` | `additional-metrics.keyword_mcp-proxy_method` |
| `MCP_PROXY_TOOL` | `additional-metrics.keyword_mcp-proxy_tools/call` |
| `MCP_PROXY_RESOURCE` | `additional-metrics.keyword_mcp-proxy_resources/read` |
| `MCP_PROXY_PROMPT` | `additional-metrics.keyword_mcp-proxy_prompts/get` |
