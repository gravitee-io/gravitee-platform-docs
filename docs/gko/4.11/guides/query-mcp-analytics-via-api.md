# Querying MCP Analytics via API

MCP analytics use the standard analytics API with MCP-specific facets and filters.

## Supported Facets

MCP analytics support the following facets:

* `MCP_PROXY_METHOD`
* `MCP_PROXY_TOOL`
* `MCP_PROXY_RESOURCE`
* `MCP_PROXY_PROMPT`

## Supported Filters

MCP analytics support the following filters with `EQ` or `IN` operators:

* `MCP_PROXY_METHOD`
* `MCP_PROXY_TOOL`
* `MCP_PROXY_RESOURCE`
* `MCP_PROXY_PROMPT`

## Compatible HTTP Metrics

All HTTP metrics accept MCP filters and facets:

* `HTTP_REQUESTS`
* `HTTP_ERRORS`
* `HTTP_REQUEST_CONTENT_LENGTH`
* `HTTP_RESPONSE_CONTENT_LENGTH`
* `HTTP_ENDPOINT_RESPONSE_TIME`
* `HTTP_GATEWAY_RESPONSE_TIME`
* `HTTP_GATEWAY_LATENCY`

## Example Queries

Filter `HTTP_REQUESTS` by `MCP_PROXY_METHOD = 'tools/call'` to count tool invocations.

Facet by `MCP_PROXY_TOOL` to see tool distribution.
