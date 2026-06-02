# Native API Connection Logs Management API Reference

## Management API

The Management API provides three endpoints for querying native API connection logs:

**GET** `/apis/{apiId}/logs/native` — Search connection logs with filters and pagination. Requires `from` and `to` query parameters; returns **400** if missing.

**GET** `/apis/{apiId}/logs/native/{requestId}` — Retrieve a single connection log by request ID. Requires `from` and `to` query parameters; returns **400** if missing.

**GET** `/apis/{apiId}/logs/native/summary` — Retrieve aggregated connection counts by status. Requires `from` and `to` query parameters; returns **400** if missing.

### Query Parameters

| Parameter | Type | Description | Required |
|:----------|:-----|:------------|:---------|
| `from` | number | Start of time range (timestamp) | Yes |
| `to` | number | End of time range (timestamp) | Yes |
| `page` | number | Page number (≥ 1) | No (default: 1) |
| `perPage` | number | Results per page (≥ 1) | No (default: 20) |
| `applicationIds` | string | Comma-separated application IDs | No |
| `planIds` | string | Comma-separated plan IDs | No |
| `connectionStatuses` | string | Comma-separated connection statuses | No |

## Restrictions

- Logs are subject to Elasticsearch or OpenSearch retention policies; the detail page warns when a log is not found within the selected time window.
- Application and plan names are resolved client-side; if resolution fails, raw IDs are displayed.
- Switching to a custom timeframe does not trigger search or summary refetch until the user clicks "Apply."
- Connection duration is emitted only on connection close; open connections do not have a duration value.
- The `from` and `to` query parameters are required for all log queries; omitting them returns **400**.
- Query validation enforces `page ≥ 1`, `size ≥ 1`, and `from ≤ to` (when both are present).
- The **Enable connection metrics reporting** toggle is disabled when the user lacks `api-definition-u` permission.
- Connection logs are available only for native Kafka APIs (API type `NATIVE`).
- The Logs menu entry appears only when the API type is `NATIVE` and the user has `api-native_log-r` permission.

## Related Changes

The Management Console adds a new **Logs** menu entry for native APIs, accessible to users with `api-native_log-r` permission. The connection logs list page includes a summary widget displaying connection counts by status and a filterable table with pagination. The detail page organizes connection metadata into four cards (Connection, Client, Server, Error Details). The Reporter settings page for native APIs now includes two toggles: **Enable connection metrics reporting** (new) and **Enable event-metrics reporting** (renamed from "Enable metrics reporting"). The connection-metrics toggle remains enabled even when event-metrics reporting is off. The Management API adds three new endpoints for querying native API connection logs. The Elasticsearch repository introduces new metric types (`NATIVE_CONNECTIONS_SUMMARY`), facets (`NATIVE_CONNECTION_STATUS`), and filters (`NATIVE_CONNECTION_STATUS`) to support connection-level analytics. The generic `MetricsQuery.Filter` no longer supports `nativeKafkaClientIds` and `nativeKafkaConnectionStatuses`; native-Kafka logs now use dedicated `NativeApiMetricsQuery` and `NativeApiMetrics` models.
