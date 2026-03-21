# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2025 -->
#### **MCP Analytics and Dashboard**

* Adds analytics support for Model Context Protocol (MCP) traffic, enabling monitoring of MCP method distribution, tool usage, resource access patterns, and prompt invocations.
* Introduces four MCP-specific facets (`MCP_PROXY_METHOD`, `MCP_PROXY_TOOL`, `MCP_PROXY_RESOURCE`, `MCP_PROXY_PROMPT`) and corresponding filters for grouping and querying analytics data by MCP dimensions.
* Includes a pre-built MCP dashboard template with 12 widgets tracking latency statistics, method/resource/tool usage, response status distribution, and response time trends.
* Requires MCP-enabled APIs to publish metrics to the `additional-metrics` field with MCP-specific keyword fields indexed in Elasticsearch.
<!-- /PIPELINE:GKO-2025 -->

## Improvements

## Bug Fixes
