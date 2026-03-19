# Querying MCP Analytics via API

MCP filters and facets are available on all HTTP-based analytics metrics:

* `HTTP_REQUESTS`
* `HTTP_ERRORS`
* `HTTP_REQUEST_CONTENT_LENGTH`
* `HTTP_RESPONSE_CONTENT_LENGTH`
* `HTTP_ENDPOINT_RESPONSE_TIME`
* `HTTP_GATEWAY_RESPONSE_TIME`
* `HTTP_GATEWAY_LATENCY`

## Combining MCP Dimensions

Combine multiple MCP dimensions in a single query to analyze patterns such as:

* Which tools are called most frequently during `resources/read` operations
* Average latency by prompt identifier
