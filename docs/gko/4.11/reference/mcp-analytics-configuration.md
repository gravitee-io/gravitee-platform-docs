# MCP Analytics Configuration Reference

## Chart Widget Types

Four chart widget types support MCP analytics visualization. Time-series widgets (`time-series-line`, `time-series-bar`) display data evolution over time. Category widgets (`vertical-bar`, `horizontal-bar`) display comparative data across discrete categories like method names or tool identifiers.

## Prerequisites

Before configuring MCP analytics, ensure the following requirements are met:

* Gravitee API Management platform with analytics enabled
* Elasticsearch backend configured for metrics storage
* APIs configured to proxy MCP protocol traffic

## Analytics Facets

MCP proxy facets enable grouping and aggregation in analytics queries. All facets use `KEYWORD` type for exact-match indexing.

| Facet Name | Label | Elasticsearch Field |
|:-----------|:------|:--------------------|
| `MCP_PROXY_METHOD` | MCP Method | `additional-metrics.keyword_mcp-proxy_method` |
| `MCP_PROXY_TOOL` | MCP Tool | `additional-metrics.keyword_mcp-proxy_tools/call` |
| `MCP_PROXY_RESOURCE` | MCP Resource | `additional-metrics.keyword_mcp-proxy_resources/read` |
| `MCP_PROXY_PROMPT` | MCP Prompt | `additional-metrics.keyword_mcp-proxy_prompts/get` |

## Analytics Filters

MCP proxy filters enable query-time filtering in analytics requests. All filters support `EQ` (equals) and `IN` (set membership) operators.

| Filter Name | Label | Elasticsearch Field |
|:------------|:------|:--------------------|
| `MCP_PROXY_METHOD` | MCP Method | `additional-metrics.keyword_mcp-proxy_method` |
| `MCP_PROXY_TOOL` | MCP Tool | `additional-metrics.keyword_mcp-proxy_tools/call` |
| `MCP_PROXY_RESOURCE` | MCP Resource | `additional-metrics.keyword_mcp-proxy_resources/read` |
| `MCP_PROXY_PROMPT` | MCP Prompt | `additional-metrics.keyword_mcp-proxy_prompts/get` |
