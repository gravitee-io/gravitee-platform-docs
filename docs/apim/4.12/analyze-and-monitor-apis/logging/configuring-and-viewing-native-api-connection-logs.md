# Configuring and Viewing Native API Connection Logs

## Gateway Configuration

## Configuring Connection Metrics Reporting

1. Navigate to a Native API → **Deployment** (left menu) → **Reporter Settings** tab.
2. Toggle **Enable connection metrics reporting** on or off.
3. Click **Save** in the form save bar at the bottom.

| Setting | Default | Description |
|:--------|:--------|:------------|
| **Enable Connection Metrics Reporting** | On (when `analytics.reporterMetricsEnabled` is absent) | Controls whether the gateway writes connection-lifecycle records to the configured reporter. When off, no new connection logs are produced — the Logs page is gated by a banner and the summary widget is hidden. |

The toggle is enabled only when the parent analytics module is enabled. Disabling the parent analytics toggle disables this one in the UI. When the toggle is turned off, the Logs page on the same API switches to a "Reporting is disabled" banner with guidance pointing back at this setting.

## Viewing Connection Logs

### Logs List Page

Navigate to a Native API → **Logs**. The page has three regions: a summary widget (top, conditional), a filter row, and a paginated logs table. A **Configure Reporting** button in the page header deep-links to Deployment → Reporter Settings for fast access to the connection-metrics toggle.

**Summary Widget**: Four cards (Connected, Disconnected, Failed, Unknown) show counts over the currently selected timeframe. The widget is hidden when connection metrics reporting is disabled; an inline info banner explains that reporting is disabled and data below may be stale. Cards show `—` until a timeframe is selected, then the live count. On a fetch error, the affected card displays a **Retry** button that re-runs the summary query without disturbing the table below.

**Filter Row**:

| Filter | Type | Notes |
|:-------|:-----|:------|
| **Period** | Predefined ranges + Custom | Custom requires explicit **Apply** click to fire (avoids triggering on every date-picker keystroke). |
| **Applications** | Server-paginated search-and-select | Resolves application names via the existing Applications endpoint. |
| **Plans** | Plan picker, scoped to this API | Lists all plans on the API. |
| **Connection Status** | Multi-select | Connected / Disconnected / Failed / Unknown |

The filter state is mirrored to the URL query string for shareable links. Refreshing the page rehydrates the filter values.

**Logs Table**:

| Column | Source | Notes |
|:-------|:-------|:------|
| **Timestamp** | `timestamp` | Connection lifecycle event time, formatted `dd/MM/yyyy HH:mm:ss.SSS`. |
| **Application** | Resolved name from `applicationId` | Renders empty when the application has been deleted or the resolution call fails. |
| **Plan** | Resolved name from `planId` | Same fallback behavior as Application. |
| **Client Identifier** | `clientIdentifier` | Free-form identifier the client provided. |
| **Connection Status** | `connectionStatus` | Rendered as a colored pill. |
| **Duration** | `connectionDurationMs` | Formatted with standard duration pipe. Empty when not reported. |
| (unlabeled) | — | Per-row eye icon (`gio:eye-empty`). Clicking it opens the detail page for that connection, preserving the current filter state via query params. |

The table is cleared if a filter request fails — the global HTTP error snackbar surfaces the failure. The user is never left looking at the previous result set under a new filter. When no data matches the filter, an empty state displays: "No data to display. More data may be available. Try widening your timeframe or adjusting your filters."

<figure><img src="../../.gitbook/assets/apim-native-connection-logs-list.png" alt="Native API connection logs list showing timestamp, application, plan, client identifier, connection status pills, and duration columns"><figcaption><p>Connection logs list with status indicators</p></figcaption></figure>

### Connection Log Detail Page

Click the eye icon (right-most column) on any row in the connection logs table. The URL pattern is `.../v4/runtime-logs-native/<requestId>?from=...&to=...&<filters>` — direct-linkable. The page has a back link top-left and four stacked cards:

<figure><img src="../../.gitbook/assets/apim-native-connection-log-detail.png" alt="Connection log detail page showing Connection, Client, and Server information cards for a connected session"><figcaption><p>Connection log detail for a successful connection</p></figcaption></figure>

**1. Connection** — outcome at a glance:

| Field | Source |
|:------|:-------|
| **Timestamp** | `timestamp` (formatted `yyyy-MM-dd HH:mm:ss.SSS`) |
| **API ID** | `apiId` |
| **Transaction ID** | `transactionId` |
| **Request ID** | `requestId` |
| **Status** | Connection status pill (same labels as Logs List Page) |
| **Duration** | `connectionDurationMs` (formatted; displays `—` when null) |

**2. Client** — who connected:

| Field | Source |
|:------|:-------|
| **Application ID** | `applicationId` |
| **Plan ID** | `planId` |
| **Subscription ID** | `subscriptionId` |
| **Client Identifier** | `clientIdentifier` |
| **Client ID** | `clientId` |
| **Remote Address** | `remoteAddress` |

**3. Server** — where the connection landed:

| Field | Source |
|:------|:-------|
| **Gateway** | `gateway` |
| **Entrypoint ID** | `entrypointId` |
| **Local Address** | `localAddress` |
| **Host** | `host` |
| **Broker ID** | `brokerId` |

**4. Error** (conditional) — visible only when `connectionStatus` is Disconnected, Failed, or Unknown:

| Field | Source |
|:------|:-------|
| **Error Key** | `errorKey` |
| **Error Message** | `errorMessage` |

<figure><img src="../../.gitbook/assets/apim-native-connection-log-detail-error.png" alt="Connection log detail page for a failed connection showing Connection, Client, Server, and Error details cards with AUTH_FAILED error"><figcaption><p>Connection log detail showing the Error details card for a failed connection</p></figcaption></figure>

**Not Found Banner**: "Log not found. No log was found for request id {requestId} within the selected time window. The window may be outside the configured retention."

**Load Failed Banner**: "Failed to load connection log. An unexpected error occurred while loading the log for request id {requestId}."
