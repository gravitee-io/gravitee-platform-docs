# Chart Component Architecture Refactoring

## Chart Component Architecture

The chart component architecture was refactored to consolidate legacy components and introduce new widget types for time-series and category data visualization.

### Removed Components

The following components were removed:

* `LineChartComponent` (selector: `gd-line-chart`)
* `BarChartComponent` (selector: `gd-bar-chart`)

### New Components

Two new components were introduced to replace the legacy chart components:

* **TimeSeriesChartComponent** (selector: `gd-time-series-chart`)
  * Supports widget types: `time-series-line`, `time-series-bar`
  * Uses `TimeSeriesConverterService` for data conversion
* **CategoryChartComponent** (selector: `gd-category-chart`)
  * Supports widget types: `vertical-bar`, `horizontal-bar`
  * Uses `CategoryConverterService` for data conversion

### Dashboard Template Updates

Existing dashboard templates were updated to use the new widget type names:

* **HTTP Proxy template**: Widget types changed from `line` to `time-series-line` and from `bar` to `time-series-bar`
* **LLM template**: Widget types changed from `line` to `time-series-line`

### Dashboard Service Enhancements

The dashboard service now injects default values for widgets created from templates:

* Widgets without an explicit `timeRange` receive a default 7-day range
* Time-series widgets without an explicit `interval` receive a default interval of 5 minutes (10000ms / 30 buckets)

### Public API Exports

Public API exports were updated to expose the new chart components:

* Removed: `export * from './lib/components/chart/line-chart/line-chart.component'`
* Added: `export * from './lib/components/chart/time-series-chart/time-series-chart.component'`
* Added: `export * from './lib/components/chart/category-chart/category-chart.component'`

### Analytics Definition Updates

Analytics definition YAML files now include MCP filter and facet labels for UI display:

* `MCP Method`
* `MCP Tool`
* `MCP Resource`
* `MCP Prompt`
