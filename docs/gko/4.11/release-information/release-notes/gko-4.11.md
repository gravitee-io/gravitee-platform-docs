# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2025 -->
#### **MCP Analytics and Dashboard Support**

* Adds analytics support for Model Context Protocol (MCP) APIs with four new facets: `MCP_PROXY_METHOD`, `MCP_PROXY_TOOL`, `MCP_PROXY_RESOURCE`, and `MCP_PROXY_PROMPT`.
* Includes a pre-built MCP dashboard template with 12 widgets covering request volume, latency percentiles, method distribution, and resource/tool/prompt usage.
* Supports all HTTP metrics (requests, errors, content length, response time, latency) with MCP-specific filtering and segmentation.
* Requires MCP APIs configured with `API_TYPE = MCP` and Elasticsearch backend storing `additional-metrics` fields.
<!-- /PIPELINE:GKO-2025 -->

## Improvements

## Bug Fixes
