# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2025 -->
#### **MCP Analytics and Dashboard Template**

* Adds MCP-specific facets and filters to HTTP analytics metrics, enabling segmentation by MCP method, tool, resource, and prompt dimensions.
* Introduces a pre-built MCP dashboard template with 12 widgets tracking request volume, latency percentiles, method distribution, and resource/tool/prompt usage.
* Refactors widget types for improved clarity: `line`, `bar`, and `top` are now `time-series-line`, `time-series-bar`, `vertical-bar`, and `horizontal-bar`.
* Requires MCP APIs to generate traffic with MCP-specific additional metrics fields in Elasticsearch.
<!-- /PIPELINE:GKO-2025 -->

## Improvements

## Bug Fixes
