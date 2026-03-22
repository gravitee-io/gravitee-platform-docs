# MCP Dashboard Template

The MCP dashboard template (`mcp`) provides a pre-configured dashboard for monitoring MCP API usage. The template includes 12 widgets that track request volume, latency percentiles (average, max, P90, P99), method usage, resource/tool/prompt distribution, and response status. All widgets are pre-filtered to `API_TYPE = MCP`, and time-series widgets use 1-hour intervals.

The template is labeled with `Focus: 'MCP'` and `Theme: 'AI'` and uses the preview image `assets/images/templates/mcp-preview.png`. Widget IDs are generated using `crypto.randomUUID()` when a dashboard is created from the template.

### Widget Composition

The MCP dashboard template includes the following widgets:

| Widget Title | Type | Metric | Facet/Filter |
|:-------------|:-----|:-------|:-------------|
| MCP requests | stats | HTTP_REQUESTS | API_TYPE = MCP |
| Average latency | stats | HTTP_GATEWAY_LATENCY | API_TYPE = MCP |
| Max latency | stats | HTTP_GATEWAY_LATENCY (MAX) | API_TYPE = MCP |
| P90 latency | stats | HTTP_GATEWAY_LATENCY (P90) | API_TYPE = MCP |
| P99 latency | stats | HTTP_GATEWAY_LATENCY (P99) | API_TYPE = MCP |
| Method usage | vertical-bar | HTTP_REQUESTS by MCP_PROXY_METHOD | limit: 10 |
| Method usage over time | time-series-line | HTTP_REQUESTS by MCP_PROXY_METHOD | interval: 1h |
| Most used Resources | vertical-bar | HTTP_REQUESTS by MCP_PROXY_RESOURCE | limit: 5 |
| Response status repartition | doughnut | HTTP_REQUESTS by HTTP_STATUS_CODE_GROUP | API_TYPE = MCP |
| Most used Prompts | vertical-bar | HTTP_REQUESTS by MCP_PROXY_PROMPT | limit: 5 |
| Most used Tools | vertical-bar | HTTP_REQUESTS by MCP_PROXY_TOOL | limit: 5 |
| Average response time | time-series-line | HTTP_GATEWAY_RESPONSE_TIME | API_TYPE = MCP, interval: 1h |

## Gateway Configuration

