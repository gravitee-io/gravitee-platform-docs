
# MCP Analytics and Dashboards

## Overview

This guide explains how to query MCP analytics data and create dashboards using the MCP template in Gravitee API Management.


## Creating Dashboards from the MCP Template

To create a dashboard from the MCP template:

1. Navigate to the dashboard creation interface.
2. Select the MCP template, labeled with `Focus: MCP` and `Theme: AI`.

The platform generates a new dashboard with 12 pre-configured widgets. Each widget receives a unique ID generated via `crypto.randomUUID()`, which differs from the template's static ID. This allows multiple dashboards created from the same template to coexist without ID conflicts.

The generated dashboard includes the following widgets, all filtered to `API_TYPE = MCP`:

| Widget | Type | Metrics | Description |
|:-------|:-----|:--------|:------------|
| MCP requests | `stats` | `HTTP_REQUESTS` | Total request count |
| Average latency | `stats` | `HTTP_GATEWAY_LATENCY` | Average gateway latency |
| Max latency | `stats` | `HTTP_GATEWAY_LATENCY` | Maximum gateway latency |
| P90 latency | `stats` | `HTTP_GATEWAY_LATENCY` (P90) | 90th percentile latency |
| P99 latency | `stats` | `HTTP_GATEWAY_LATENCY` (P99) | 99th percentile latency |
| Method usage | `vertical-bar` | `HTTP_REQUESTS` | Request count by MCP method (top 10) |
| Method usage over time | `time-series-line` | `HTTP_REQUESTS` | Request count by MCP method over time (1-hour intervals) |
| Most used Resources | `vertical-bar` | `HTTP_REQUESTS` | Request count by MCP resource (top 5) |
| Response status repartition | `doughnut` | `HTTP_REQUESTS` | Request count by HTTP status code group |
| Most used Prompts | `vertical-bar` | `HTTP_REQUESTS` | Request count by MCP prompt (top 5) |
| Most used Tools | `vertical-bar` | `HTTP_REQUESTS` | Request count by MCP tool (top 5) |
| Average response time | `time-series-line` | `HTTP_GATEWAY_RESPONSE_TIME` | Average gateway response time over time (1-hour intervals) |

## Restrictions

* MCP facets and filters are valid only for the seven HTTP metrics: `HTTP_REQUESTS`, `HTTP_ERRORS`, `HTTP_REQUEST_CONTENT_LENGTH`, `HTTP_RESPONSE_CONTENT_LENGTH`, `HTTP_ENDPOINT_RESPONSE_TIME`, `HTTP_GATEWAY_RESPONSE_TIME`, and `HTTP_GATEWAY_LATENCY`.
* Filter validation enforces the four MCP filter names (`MCP_PROXY_METHOD`, `MCP_PROXY_TOOL`, `MCP_PROXY_RESOURCE`, `MCP_PROXY_PROMPT`). Other filter names are rejected.
* MCP facets require Elasticsearch fields in the `additional-metrics` namespace with `keyword_` prefix.
* Widget types `line` and `bar` are deprecated and replaced by `time-series-line`, `time-series-bar`, `vertical-bar`, and `horizontal-bar`.
