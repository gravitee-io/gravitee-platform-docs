# MCP Analytics Elasticsearch Mappings and Restrictions

## Elasticsearch Field Mappings

| Facet/Filter Name | Elasticsearch Field Path |
|:------------------|:-------------------------|
| `MCP_PROXY_METHOD` | `additional-metrics.keyword_mcp-proxy_method` |
| `MCP_PROXY_TOOL` | `additional-metrics.keyword_mcp-proxy_tools/call` |
| `MCP_PROXY_RESOURCE` | `additional-metrics.keyword_mcp-proxy_resources/read` |
| `MCP_PROXY_PROMPT` | `additional-metrics.keyword_mcp-proxy_prompts/get` |

## Restrictions

- MCP facets and filters require Elasticsearch indices with `additional-metrics` mappings for MCP-specific keyword fields.
- Widget IDs in dashboard templates are replaced with UUIDs on instantiation. Original template IDs are not preserved.
- Time-series widgets without explicit intervals default to 5-minute buckets (10000ms / 30 buckets over 7 days).
- Category bar charts display a maximum of 10 items by default (configurable via widget limit property).
- Nested bucket detection in time-series converter now scans all buckets. Sparse data at the start of a time range no longer prevents nested facet rendering.
- Chart color assignment for category bars uses a fixed `CHART_COLORS` array. Datasets exceeding array length will cycle colors.
