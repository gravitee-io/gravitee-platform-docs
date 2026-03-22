# Querying MCP Analytics and Using the MCP Dashboard Template

## Gateway Configuration

## Using the MCP Dashboard Template

The MCP dashboard template provides a pre-configured dashboard for monitoring MCP API usage. It includes 12 widgets tracking request volume, latency percentiles (average, max, P90, P99), method usage, resource/tool/prompt distribution, and response status.

To create a dashboard from the MCP template:

1. Navigate to **Observability** > **Dashboards**.
2. Click **Create dashboard** > **Create from template**.
3. Select the **MCP** template from the left panel.
4. Click **Use template**.

The platform generates a new dashboard with 12 pre-configured widgets, each assigned a unique ID. All widgets are pre-filtered to `API_TYPE = MCP` and use 1-hour intervals for time-series data.

### MCP Dashboard Widgets

| Widget Title | Type | Metrics | Filters |
|:-------------|:-----|:--------|:--------|
| MCP requests | stats | HTTP_REQUESTS (COUNT) | API_TYPE = MCP |
| Average latency | stats | HTTP_GATEWAY_LATENCY | API_TYPE = MCP |
| Max latency | stats | HTTP_GATEWAY_LATENCY (MAX) | API_TYPE = MCP |
| P90 latency | stats | HTTP_GATEWAY_LATENCY (P90) | API_TYPE = MCP |
| P99 latency | stats | HTTP_GATEWAY_LATENCY (P99) | API_TYPE = MCP |
| Method usage | vertical-bar | HTTP_REQUESTS (COUNT) by MCP_PROXY_METHOD | limit: 10 |
| Method usage over time | time-series-line | HTTP_REQUESTS (COUNT) by MCP_PROXY_METHOD | interval: 1h |
| Most used Resources | vertical-bar | HTTP_REQUESTS (COUNT) by MCP_PROXY_RESOURCE | limit: 5 |
| Response status repartition | doughnut | HTTP_REQUESTS (COUNT) by HTTP_STATUS_CODE_GROUP | API_TYPE = MCP |
| Most used Prompts | vertical-bar | HTTP_REQUESTS (COUNT) by MCP_PROXY_PROMPT | limit: 5 |
| Most used Tools | vertical-bar | HTTP_REQUESTS (COUNT) by MCP_PROXY_TOOL | limit: 5 |
| Average response time | time-series-line | HTTP_GATEWAY_RESPONSE_TIME | API_TYPE = MCP, interval: 1h |

### Customizing the Dashboard

After creating the dashboard, you can customize it by:

* Adjusting the timeframe to view data for a specific period
* Modifying filters to focus on specific MCP methods, tools, resources, or prompts
* Adding or removing widgets to match your monitoring requirements

## End-User Configuration

## Restrictions

* Widget type renames (`line` → `time-series-line`, `bar` → `time-series-bar`, `top` → `vertical-bar`/`horizontal-bar`) are backward-incompatible. Existing dashboards using legacy widget types require migration.
* MCP facets and filters are only available for HTTP metrics. Other metric types don't support MCP dimensions.
* MCP filters support only `EQ` and `IN` operators. Range or pattern-based filtering isn't available.
* MCP-specific Elasticsearch fields must be populated by the gateway at request time. Missing fields result in empty facet results.

## Related Changes

The following dashboard templates have been updated with new widget types:

* **HTTP Proxy template**: Widget type `line` renamed to `time-series-line`, widget type `bar` renamed to `time-series-bar`. Filters now applied at request level instead of metric level.
* **LLM template**: Widget type `line` renamed to `time-series-line`. Filters now applied at request level instead of metric level.
