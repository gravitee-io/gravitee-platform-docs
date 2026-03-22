# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2025 -->
#### **MCP Analytics and Dashboard Support**

* Track Model Context Protocol (MCP) API usage with dedicated facets for method types, tool invocations, resource access, and prompt requests alongside standard HTTP metrics.
* Query MCP analytics data using four new facets (`MCP_PROXY_METHOD`, `MCP_PROXY_TOOL`, `MCP_PROXY_RESOURCE`, `MCP_PROXY_PROMPT`) with all existing HTTP metrics and widget types.
* Deploy pre-built MCP dashboard template with 12 widgets including request counts, latency percentiles, method/tool/resource/prompt usage charts, and time-series visualizations.
* Requires Elasticsearch cluster configured for analytics storage and MCP APIs generating traffic.
<!-- /PIPELINE:GKO-2025 -->

## Improvements

## Bug Fixes
