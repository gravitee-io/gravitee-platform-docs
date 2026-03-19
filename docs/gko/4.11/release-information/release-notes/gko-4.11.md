# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2025 -->
#### **MCP Analytics and Dashboard Template**

* Adds analytics dimensions for Model Context Protocol (MCP) APIs, enabling tracking of MCP methods, tool invocations, resource access, and prompt execution alongside standard HTTP metrics.
* Introduces a pre-built MCP dashboard template with 12 widgets monitoring request volume, latency percentiles (P90, P95, P99), method distribution, and top resources/prompts/tools.
* Supports eight widget types including time-series line/bar charts and category-based visualizations (doughnut, pie, polar area, vertical/horizontal bar).
* Requires Elasticsearch cluster with MCP API analytics data indexed under the `additional-metrics` namespace with keyword facet mappings.
* MCP facets and filters (`MCP_PROXY_METHOD`, `MCP_PROXY_TOOL`, `MCP_PROXY_RESOURCE`, `MCP_PROXY_PROMPT`) support `EQ` and `IN` operators for querying via the analytics API.
<!-- /PIPELINE:GKO-2025 -->

## Improvements

## Bug Fixes
