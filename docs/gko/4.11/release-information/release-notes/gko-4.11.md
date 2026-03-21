# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2025 -->
#### **MCP Analytics and Dashboard Template**

* Adds four new analytics dimensions for Model Context Protocol (MCP) APIs: MCP Method, MCP Tool, MCP Resource, and MCP Prompt, enabling segmentation and filtering of HTTP metrics by MCP protocol elements.
* Introduces eight widget types including time-series line/bar charts and category-based vertical/horizontal bar charts for visualizing MCP API usage patterns and trends.
* Provides a pre-built MCP dashboard template with 11 widgets for monitoring request volume, latency, method distribution, top resources/tools/prompts, and response status breakdowns.
* Requires MCP-type APIs configured to emit analytics events with `additional-metrics` fields and Elasticsearch analytics backend.
<!-- /PIPELINE:GKO-2025 -->

## Improvements

## Bug Fixes
