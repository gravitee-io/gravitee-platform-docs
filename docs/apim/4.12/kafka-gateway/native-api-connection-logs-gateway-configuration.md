# Native API Connection Logs Gateway Configuration

## Overview

Native API Connection Logs and Reporting provides visibility into connection-level events for native Kafka APIs. Administrators can view connection attempts, session failures, and connection durations, and filter logs by application, plan, or connection status. A dedicated reporting toggle controls whether connection metrics are collected and stored.

## Key Concepts

### Connection Status

Each connection event is classified into one of four statuses:

| Status | Meaning | Badge |
|:-------|:--------|:------|
| **Connected** | Healthy connection established | Success (green) |
| **Disconnected** | Policy-driven session failure during request flow | Warning (orange) |
| **Failed** | Connection-level interruption before session establishment | Error (red) |
| **Unknown** | Backend unreachable or internal server error | Accent (purple) |

Connection status determines the badge color and icon displayed in the logs table and detail view.

### Connection Metrics

Connection metrics capture client and server details for each connection event:

- **Client context**: application, plan, subscription, client identifier, remote address
- **Server context**: gateway, entrypoint, local address, host, broker identifier
- **Timing**: timestamp, connection duration in milliseconds
- **Error details**: error key and message (when status is not Connected)

Connection duration is populated only on close-event metrics; open-event metrics (e.g., Connected status) may have null duration.

### Reporter Metrics Toggle

The **Enable connection metrics reporting** toggle controls whether connection-level metrics are collected and stored. When disabled, the logs page displays a banner indicating that reporting is off and data may be outdated or absent. This toggle is independent of the event-metrics reporting toggle and remains configurable even when analytics is disabled.

## Prerequisites

- Native Kafka API (API type `NATIVE`)
- `api-native_log-r` permission to view connection logs
- `from` and `to` query parameters (required for all native-log endpoints)

## Gateway Configuration

## Creating Native API Connection Logs

Navigate to **Logs** in the API v4 navigation menu (visible only for native APIs when the user has `api-native_log-r` permission). The connection logs page displays a filterable table of connection events and a summary widget showing counts by connection status.

<figure><img src="../.gitbook/assets/apim-native-api-connection-logs-and-reporting-step-01.png" alt="Connection logs table displaying timestamp, application, plan, client identifier, connection status, and duration columns"><figcaption></figcaption></figure>

1. Select one or more **Applications** from the multi-select dropdown to filter by application.
2. Select one or more **Plans** from the multi-select dropdown to filter by plan.
3. Select one or more **Connection status** values (Connected, Disconnected, Failed, Unknown) to filter by status.
4. Choose a **Timeframe** preset (e.g., Last 15 minutes, Last hour) or select a custom range and click **Apply**.

The table displays the following columns:

| Column | Description |
|:-------|:------------|
| **Timestamp** | Connection event timestamp in `dd/MM/yyyy HH:mm:ss.SSS` format |
| **Application** | Resolved application name or raw application ID |
| **Plan** | Resolved plan name or raw plan ID |
| **Client identifier** | Client identifier value |
| **Connection status** | Badge with icon and label (Connected, Disconnected, Failed, Unknown) |
| **Duration** | Connection duration in milliseconds (empty for open-event metrics) |
| **View** | Eye icon button to navigate to log detail page |

The summary widget displays four cards showing the count of connections for each status (Connected, Disconnected, Failed, Unknown). The widget is hidden when **Enable connection metrics reporting** is disabled.

**Reference Table:**

| Field | Type | Description |
|:------|:-----|:------------|
| **Applications** | Multi-select | Filter by one or more applications |
| **Plans** | Multi-select | Filter by one or more plans |
| **Connection status** | Multi-select | Filter by Connected, Disconnected, Failed, or Unknown |
| **Timeframe** | Preset or custom range | Filter by time window (requires explicit Apply for custom ranges) |

## Viewing Connection Log Details

Click the eye icon in the **View** column to navigate to the connection log detail page for a specific request ID. The detail page displays four cards:

<figure><img src="../.gitbook/assets/apim-native-api-connection-logs-and-reporting-step-02.png" alt="Connection detail view showing Connection, Client, Server, and Error details cards with failed authentication status"><figcaption></figcaption></figure>

### Connection Card

- Timestamp, API ID, Transaction ID, Request ID, Status (badge), Duration

### Client Card

- Application ID, Plan ID, Subscription ID, Client identifier, Client ID, Remote address

### Server Card

- Gateway, Entrypoint ID, Local address, Host, Broker ID

### Error Details Card

Displayed only when connection status is not Connected. Shows error key and error message.

**Error states:**

- **404 (not found)**: Banner displays "Log not found — No log was found for request id **{requestId}** within the selected time window. The window may be outside the configured retention."
- **Non-404 error**: Banner displays "Failed to load connection log — An unexpected error occurred while loading the log for request id **{requestId}**."
- **Missing `from`/`to` query params**: Renders load-failed banner without firing HTTP call.

### Management API

#### Search Native API Logs

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

**Response:** `NativeApiLogsResponse` with `data` (array of `NativeApiLog`), `pagination`, and `links`.

**Permissions:** Requires `api-native_log-r`. Missing permission returns HTTP 403. Missing `from` or `to` returns HTTP 400.

#### Get Native API Logs Summary

**Endpoint:** `GET /apis/{apiId}/logs/native/summary`

**Query Parameters:**

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `from` | number | Start timestamp (required) |
| `to` | number | End timestamp (required) |
| `applicationIds` | string | Comma-separated application IDs |
| `planIds` | string | Comma-separated plan IDs |
| `connectionStatuses` | string | Comma-separated statuses |

**Response:** `NativeApiLogsSummary` with `countByConnectionStatus` (partial record mapping status to count).

**Permissions:** Requires `api-native_log-r`. Missing permission returns HTTP 403. Missing `from` or `to` returns HTTP 400.

#### Find Native API Log by Request ID

**Endpoint:** `GET /apis/{apiId}/logs/native/{requestId}`

**Query Parameters:**

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `from` | number | Start timestamp (required) |
| `to` | number | End timestamp (required) |

**Response:** `NativeApiLog` object.

**Permissions:** Requires `api-native_log-r`. Missing permission returns HTTP 403. Missing `from` or `to` returns HTTP 400.

## Restrictions

- Connection duration (`connectionDurationMs`) is only populated on close-event metrics; open-event metrics (e.g., Connected status) may have null duration.
- Application name resolution degrades gracefully: if the `/applications/_paged` call fails, rows render with raw application IDs instead of names.
- Custom timeframe requires explicit "Apply" action; preset changes trigger immediate search.
- Changing filters resets pagination to page 1.
- Summary widget does not re-fetch when timeframe period switches to "custom" (waits for explicit Apply).
- `from` and `to` query parameters are required for all native-log endpoints; missing parameters return HTTP 400.
- `from` must be ≤ `to`; violating this constraint throws `IllegalArgumentException`.
- `page` and `size` must be ≥ 1; violating this constraint throws `IllegalArgumentException`.
- The following fields were removed from `MetricsQuery.Filter` and are now handled via `NativeApiMetricsQuery`: `nativeKafkaClientIds`, `nativeKafkaConnectionStatuses`. Use `applicationIds`, `planIds`, `connectionStatuses` instead.

## Related Changes

The **Enable connection metrics reporting** toggle is added to the Reporter Settings page for native APIs. When disabled, the connection logs page displays a banner ("Reporting is disabled — You're seeing outdated or no data because reporting is disabled. To view the latest data, please enable reporting.") with a "Configure Reporting" button that navigates to the reporter settings. The toggle defaults to `true` when `analytics` is `null` or undefined. The Elasticsearch schema is extended with four new keyword and long fields for native Kafka metrics: `keyword_native-kafka_client-id`, `keyword_native-kafka_broker-id`, `keyword_native-kafka_connection-status`, and `long_native-kafka_connection-duration-ms`. The repository layer introduces `NATIVE_CONNECTIONS_SUMMARY` metric, `NATIVE_CONNECTION_STATUS` facet, and two new methods (`searchNativeApiFacets`, `findNativeApiMetrics`, `searchNativeApiMetrics`) in `AnalyticsRepository` and `MetricsRepository`.
