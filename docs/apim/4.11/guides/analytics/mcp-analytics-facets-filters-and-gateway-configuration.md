# MCP Analytics Facets, Filters, and Gateway Configuration

## Overview

MCP Analytics & Dashboard Enhancements extend the Gravitee analytics platform to support Model Context Protocol (MCP) API monitoring. This feature introduces MCP-specific facets and filters for HTTP metrics, a pre-built dashboard template for MCP usage visualization, and widget visualization types for time-series and category-based data.

## Gateway Configuration

### Elasticsearch Field Mapping

MCP facets and filters map to Elasticsearch fields in the analytics index. Ensure the following field mappings are present:

| Filter/Facet Name | Elasticsearch Field |
|:------------------|:--------------------|
| `MCP_PROXY_METHOD` | `additional-metrics.keyword_mcp-proxy_method` |
| `MCP_PROXY_TOOL` | `additional-metrics.keyword_mcp-proxy_tools/call` |
| `MCP_PROXY_RESOURCE` | `additional-metrics.keyword_mcp-proxy_resources/read` |
| `MCP_PROXY_PROMPT` | `additional-metrics.keyword_mcp-proxy_prompts/get` |

## Querying MCP Analytics

To query MCP analytics programmatically:

1. Construct an analytics query targeting an HTTP metric (e.g., `HTTP_REQUESTS`).
2. Add one or more MCP filters using `MCP_PROXY_METHOD`, `MCP_PROXY_TOOL`, `MCP_PROXY_RESOURCE`, or `MCP_PROXY_PROMPT` with `EQ` or `IN` operators.
3. Submit the query via the analytics API.

<!-- GAP: Analytics API endpoint paths and request/response schemas not provided in manifest -->
