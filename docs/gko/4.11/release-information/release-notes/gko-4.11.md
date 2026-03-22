# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2025 -->
#### **MCP Analytics and Dashboard Template**

* Adds four new analytics facets and filters for Model Context Protocol (MCP) traffic: MCP Method, MCP Tool, MCP Resource, and MCP Prompt, enabling granular analysis of MCP API usage patterns.
* Introduces a pre-built MCP dashboard template with 12 widgets covering latency statistics, method distribution, resource/tool/prompt usage, and response status breakdowns for immediate visibility into MCP API performance.
* Supports time-series and categorical chart types (`time-series-line`, `time-series-bar`, `vertical-bar`, `horizontal-bar`) for flexible data visualization across all HTTP-based metrics.
* Requires Elasticsearch backend with analytics enabled and at least one deployed API with `API_TYPE = MCP` receiving traffic to populate MCP-specific metrics.
<!-- /PIPELINE:GKO-2025 -->

## Improvements

## Bug Fixes
