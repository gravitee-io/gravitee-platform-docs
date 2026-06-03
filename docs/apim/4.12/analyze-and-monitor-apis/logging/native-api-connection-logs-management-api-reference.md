# Native API Connection Logs Management API Reference

## Management API

The Management API provides three endpoints for programmatically accessing native API connection logs, log details, and summary statistics.

### List Native API Logs

`GET /v2/apis/{apiId}/logs/native`

Retrieves a paginated list of connection logs for the specified native API.

**Query Parameters**

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `page` | integer | Page number (≥ 1) |
| `perPage` | integer | Results per page (≥ 1) |
| `from` | integer | Start timestamp (milliseconds) |
| `to` | integer | End timestamp (milliseconds, must be ≥ `from`) |
| `applicationIds` | string | Comma-separated application IDs |
| `planIds` | string | Comma-separated plan IDs |
| `connectionStatuses` | string | Comma-separated connection statuses. Valid values: `CONNECTED`, `CONNECTION_ERROR`, `SESSION_ERROR`, `INTERNAL_ERROR` |

**Response**

Returns a `NativeApiLogsResponse` object containing:

* `data`: Array of `NativeApiLog` objects
* `pagination`: Pagination metadata
* `links`: Navigation links for pagination

### Get Native API Log Details

`GET /v2/apis/{apiId}/logs/native/{requestId}`

Retrieves detailed information for a specific connection log identified by `requestId`.

**Query Parameters**

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `from` | integer | Start timestamp (milliseconds) |
| `to` | integer | End timestamp (milliseconds) |

**Response**

Returns a single `NativeApiLog` object. If the log is not found within the specified time window, the endpoint returns a 404 status code.

### Get Native API Logs Summary

`GET /v2/apis/{apiId}/logs/native/summary`

Retrieves summary statistics for connection logs, aggregated by connection status.

**Query Parameters**

Uses the same query parameters as the list endpoint: `page`, `perPage`, `from`, `to`, `applicationIds`, `planIds`, and `connectionStatuses`.

**Response**

Returns a `NativeApiLogsSummary` object containing:

* `countByConnectionStatus`: A map of connection status values to their respective counts
