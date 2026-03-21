# MCP Analytics Restrictions and Implementation Notes

## Restrictions

MCP facets and filters apply only to HTTP metrics. They do not apply to message-based or v2 API metrics.

MCP dimension data must be present in the `additional-metrics` Elasticsearch field namespace. APIs that do not emit these fields will return empty facet results.

Existing dashboards using legacy widget types (`line`, `bar`) must migrate to the new enumeration values (`time-series-line`, `time-series-bar`).

The MCP dashboard template preview image must be present at `assets/images/templates/mcp-preview.png` for the template selection UI to render correctly.

## Related Changes

The analytics API schema (`openapi-analytics.yaml`) adds four MCP facet and filter enumerations: `MCP_PROXY_METHOD`, `MCP_PROXY_TOOL`, `MCP_PROXY_RESOURCE`, and `MCP_PROXY_PROMPT`. The schema replaces legacy widget types (`line`, `bar`, `top`) with four new types: `time-series-line`, `time-series-bar`, `vertical-bar`, and `horizontal-bar`.

The analytics definition YAML (`analytics-definition.yaml`) registers MCP facets and filters with keyword type and human-readable labels (MCP Method, MCP Tool, MCP Resource, MCP Prompt).

Chart components are refactored: `LineChartComponent` and `BarChartComponent` merge into `TimeSeriesChartComponent` with mode selection. A new `CategoryChartComponent` handles vertical and horizontal bar charts.

The dashboard service (`DashboardService.toCreateDashboard()`) generates unique widget IDs using `crypto.randomUUID()` instead of copying template IDs.

Test coverage includes five MCP-specific analytics query tests validating request counts, latency aggregations, faceting by method and tool, and filtering by method.
