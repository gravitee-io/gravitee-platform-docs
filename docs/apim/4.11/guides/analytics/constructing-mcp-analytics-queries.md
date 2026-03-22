# Constructing MCP Analytics Queries

## Gateway Configuration

## Creating MCP Analytics Queries

To analyze MCP traffic, construct analytics queries using the MCP-specific facets and filters. Follow these steps:

1. **Select a metric and aggregation.** Choose a supported metric (e.g., `HTTP_REQUESTS`) and an aggregation function (e.g., `COUNT`).
2. **Apply the `API_TYPE = MCP` filter.** This isolates MCP traffic from other API types.

3. **Add MCP-specific filters.** Narrow results using filters such as `MCP_PROXY_METHOD IN [tools/call, resources/read]`.
4. **Group by an MCP facet.** Break down results by facets such as `MCP_PROXY_TOOL` to analyze usage by tool name.
5. **Configure time range and interval.** Set the time range and interval for time-series queries.
