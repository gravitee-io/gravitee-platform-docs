# Configure MCP Analytics Queries

## Prerequisites

Before you configure MCP analytics queries, ensure the following:

* MCP-type APIs are configured to emit analytics events with `additional-metrics` fields
* Analytics data ingestion pipeline is configured to index MCP proxy fields
* You have the `Environment-dashboard-r` permission to view dashboards
* You have the `Environment-dashboard-c` permission to create dashboards

## Gateway Configuration

No gateway-specific configuration is required. MCP analytics queries operate on data already indexed by the analytics backend.

## Creating MCP Analytics Queries

To analyze MCP API traffic, configure analytics queries using MCP facets and filters:

1. Select a supported HTTP metric:
   * `HTTP_REQUESTS`
   * `HTTP_ERRORS`
   * `HTTP_REQUEST_CONTENT_LENGTH`
   * `HTTP_RESPONSE_CONTENT_LENGTH`
   * `HTTP_ENDPOINT_RESPONSE_TIME`
   * `HTTP_GATEWAY_RESPONSE_TIME`
   * `HTTP_GATEWAY_LATENCY`
2. Add facets to group results by MCP dimension:
   * `MCP_PROXY_METHOD`
   * `MCP_PROXY_TOOL`
   * `MCP_PROXY_RESOURCE`
   * `MCP_PROXY_PROMPT`
3. Add filters to restrict results to specific MCP dimension values. For example, filter by `MCP_PROXY_METHOD=tools/call` to analyze tool invocations.
4. Combine MCP filters with standard filters for multi-dimensional analysis:
   * `API_TYPE=MCP`
   * `HTTP_STATUS_CODE_GROUP`

All MCP facets and filters are keyword-based and support exact-match queries only.


To deploy the pre-built MCP dashboard, see [Deploy the MCP Dashboard Template](../dashboards/deploy-the-mcp-dashboard-template.md).
