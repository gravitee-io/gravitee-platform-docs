# Deploying the MCP Dashboard Template

## Creating Dashboards from the MCP Template

To deploy the MCP dashboard template:

1. Navigate to the dashboard gallery.
2. Select the **MCP** template.

The platform generates unique widget IDs using `crypto.randomUUID()` to ensure each dashboard instance has distinct identifiers, even when multiple dashboards are created from the same template.

The template includes 12 widgets:

* Five latency statistics (`stats` type showing average, max, P90, P99 latency and total requests)
* Method usage charts (`vertical-bar` for top 10 methods, `time-series-line` for method trends)
* Top-5 rankings for resources, prompts, and tools (`vertical-bar`)
* Response status distribution (`doughnut`)
* Average response time over time (`time-series-line`)

All widgets except method, resource, tool, and prompt breakdowns apply the `API_TYPE = MCP` filter.

## Restrictions

* MCP facets and filters require Elasticsearch field mappings in the `additional-metrics` namespace. APIs not populating these fields will return empty results.
* Widget type migration from legacy `line` and `bar` types to `time-series-line` and `time-series-bar` is not automatic.
* MCP dashboard template assumes `API_TYPE = MCP` filter is valid. APIs without this type classification will not appear in template widgets.
* Widget ID uniqueness is enforced only at dashboard creation time. Manual widget ID edits may cause collisions.

## Related Changes

The analytics OpenAPI schema (`openapi-analytics.yaml`) was updated to include MCP filter and facet enumerations and new widget type values (`time-series-line`, `time-series-bar`, `vertical-bar`, `horizontal-bar`).
