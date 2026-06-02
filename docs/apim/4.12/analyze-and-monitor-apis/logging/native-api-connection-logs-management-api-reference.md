# Native API Connection Logs Management API Reference

## Management API

### Search Native API Logs

**Endpoint:** `GET /apis/{apiId}/logs/native`

**Query Parameters:**

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `from` | number | Start timestamp (required) |
| `to` | number | End timestamp (required) |
| `page` | number | Page number (default: 1, must be ≥ 1) |
| `perPage` | number | Results per page (default: 10, must be ≥ 1) |
| `applicationIds` | string | Comma-separated application IDs |
| `planIds` | string | Comma-separated plan IDs |
| `connectionStatuses` | string | Comma-separated statuses (CONNECTED, SESSION_ERROR, CONNECTION_ERROR, INTERNAL_ERROR) |

**Response Schema:** `NativeApiLogsResponse`

The response contains:
- `data`: Array of `NativeApiLog` objects
- `pagination`: Pagination metadata
- `links`: Hypermedia links

**Permissions:** Requires `api-native_log-r` permission. Missing permission returns HTTP 403.

**Validation:**
- Missing `from` or `to` returns HTTP 400.
- `from` must be ≤ `to`. Violating this constraint throws `IllegalArgumentException`.
- `page` and `perPage` must be ≥ 1. Violating this constraint throws `IllegalArgumentException`.

### Get Native API Logs Summary

**Endpoint:** `GET /apis/{apiId}/logs/native/summary`

**Query Parameters:**

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `from` | number | Start timestamp (required) |
| `to` | number | End timestamp (required) |
| `applicationIds` | string | Comma-separated application IDs |
| `planIds` | string | Comma-separated plan IDs |
| `connectionStatuses` | string | Comma-separated statuses (CONNECTED, SESSION_ERROR, CONNECTION_ERROR, INTERNAL_ERROR) |

**Response Schema:** `NativeApiLogsSummary`

The response contains:
- `countByConnectionStatus`: Partial record mapping connection status to count

**Permissions:** Requires `api-native_log-r` permission. Missing permission returns HTTP 403.

**Validation:**
- Missing `from` or `to` returns HTTP 400.
- `from` must be ≤ `to`. Violating this constraint throws `IllegalArgumentException`.

### Find Native API Log by Request ID

**Endpoint:** `GET /apis/{apiId}/logs/native/{requestId}`

**Query Parameters:**

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `from` | number | Start timestamp (required) |
| `to` | number | End timestamp (required) |

**Response Schema:** `NativeApiLog`

**Permissions:** Requires `api-native_log-r` permission. Missing permission returns HTTP 403.

**Validation:**
- Missing `from` or `to` returns HTTP 400.
- `from` must be ≤ `to`. Violating this constraint throws `IllegalArgumentException`.
