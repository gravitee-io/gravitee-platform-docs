### Searching Logs

To search logs, send a POST request to `/environments/{envId}/logs/search` with a JSON body containing a required `timeRange` and optional `filters` array.

The `timeRange` object must include `from` and `to` timestamps in ISO 8601 format. Filters are applied as an array of objects, each specifying a `name`, `operator`, and `value`.

**Example:** To find all 5xx errors for a specific API in the last hour, include a filter with `name: "API"`, `operator: "EQ"`, `value: "<api-id>"` and another with `name: "HTTP_STATUS"`, `operator: "GTE"`, `value: 500`.

Pagination is controlled via `page` (default 1, min 1) and `perPage` (default 10, min 1, max 100) query parameters.

The response includes a `data` array of log entries, `pagination` metadata, and HATEOAS `links` for navigation.

### Retrieving Filter Definitions

To discover available filters and their supported operators, send a GET request to `/environments/{envId}/logs/definition/filters`.

The response returns a `LogsFilterSpecsResponse` containing an array of `LogsFilterSpec` objects. Each spec includes:

* `name` — The filter name
* `operators` — Array of supported operators (e.g., `["EQ", "IN"]`)
* `type` — Data type (e.g., `"string"`, `"integer"`)
* `enumValues` — Optional array of allowed values for constrained fields
* `range` — Optional object with `min` and `max` values for numeric filters

Use this endpoint to dynamically build filter UIs or validate filter configurations before submitting search requests.

### Filter Reference

| Filter Name | Operators | Value Type | Description |
|:------------|:----------|:-----------|:------------|
| API | EQ, IN | String/Array | Limits results to specified API ID(s) |
| APPLICATION | EQ, IN | String/Array | Limits results to specified application ID(s) |
| PLAN | EQ, IN | String/Array | Limits results to specified plan ID(s) |
| HTTP_METHOD | EQ, IN | String/Array | Limits results to specified HTTP method(s) |
| HTTP_STATUS | EQ, IN | Integer/Array | Limits results to specified HTTP status code(s) |
| ENTRYPOINT | EQ, IN | String/Array | Limits results to specified entrypoint ID(s) |
| MCP_METHOD | EQ, IN | String/Array | Limits results to specified MCP method(s) |
| TRANSACTION_ID | EQ, IN | String/Array | Limits results to specified transaction ID(s) |
| REQUEST_ID | EQ, IN | String/Array | Limits results to specified request ID(s) |
| URI | EQ | String | Limits results to URIs matching pattern (supports wildcard `*`) |
| RESPONSE_TIME | GTE, LTE | Integer | Limits results to response times within range (milliseconds) |

Filters with the same name are combined using AND logic. The `RESPONSE_TIME` filter supports range queries by combining `GTE` and `LTE` operators. The `URI` filter supports wildcard matching with a trailing `*` for prefix searches.

### Validation Rules

The API enforces the following validation rules:

**Time Range:**
* `from` must be before `to`

**Response Time:**
* Filter values must be non-negative integers
* When both `GTE` and `LTE` are used for `RESPONSE_TIME`, the `GTE` value must not exceed the `LTE` value

**Pagination:**
* `page` must be ≥ 1
* `perPage` must be between 1 and 100

**URI Filter:**
* Wildcard (`*`) only supported as a trailing character for prefix matching

**Permissions:**
* Users only see logs for APIs they have permission to access

**Application Display:**
* Application ID `1` is treated as the default keyless application and displayed as "Unknown application (keyless)"
