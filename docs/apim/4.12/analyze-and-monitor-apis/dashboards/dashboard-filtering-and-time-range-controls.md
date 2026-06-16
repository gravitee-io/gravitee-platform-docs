# Dashboard Filtering and Time Range Controls

## Overview

Dashboard filtering and time range controls enable API platform administrators to scope observability dashboards to specific APIs, applications, plans, status codes, and custom time windows. Filters are applied dynamically across all dashboard widgets and persisted in the URL for sharing and bookmarking. The unified query parameter format (`q`) encodes both filter conditions and time ranges in a single, version-controlled structure.

## Key Concepts

### Filter Conditions

A filter condition consists of a field, an operator, and one or more values. Conditions are applied to all widgets in the dashboard. Multiple values for the same field are automatically merged using membership operators (`In`, `Not in`). Filters with incompatible operators on the same field are kept as separate conditions.

| Component | Description |
|-----------|-------------|
| **Field** | The dimension to filter (API, APPLICATION, PLAN, STATUS_CODE, HTTP_PATH, etc.) |
| **Operator** | Comparison logic (`=`, `≠`, `In`, `Not in`, `≥`, `≤`) |
| **Values** | One or more identifiers or literals. For ID-based fields (API, APPLICATION, PLAN), values are resolved to display labels via the backend. |
| **Value Labels** | Human-readable labels for ID-based values. Not persisted in the URL; resolved on load. |

### Filter Types

| Type | Input Behavior | Example Use Case |
|------|---------------|------------------|
| **ENUM** | Single or multi-select dropdown with predefined values | Selecting from a fixed list of status codes |
| **KEYWORD** | Autocomplete with backend search, chip-based multi-select, scroll pagination | Searching and selecting APIs or applications by name |
| **NUMBER** | Numeric input with optional range hint | Filtering by response time or request count |
| **STRING** | Free-text input | Filtering by HTTP path or custom string fields |

### Time Range

The time range defines the temporal scope for all dashboard widgets. It can be relative or absolute. The default period is `5m`. Changing the time range triggers a refresh of all widget data.

| Period | Description |
|--------|-------------|
| `1m` | Last 1 minute |
| `5m` | Last 5 minutes (default) |
| `1h` | Last 1 hour |
| `1d` | Last 1 day |
| `1w` | Last 1 week |
| `1M` | Last 1 month |
| `custom` | User-defined absolute range (from/to timestamps) |

## Prerequisites

- User must have `ENVIRONMENT_DASHBOARD` read permission to view dashboards.
- User must have `environment-dashboard-u` update permission to add, edit, or remove filters.
- For ID-based filters (API, APPLICATION, PLAN), the backend resolves identifiers to display labels.

## Creating Dashboard Filters

Navigate to the observability dashboard viewer. The filter bar is displayed below the dashboard title toolbar.

1. Click **Add filter** to open the filter dialog.
2. Select a **Filter by** field from the autocomplete dropdown. The list is searchable by field label, name, or API type. If the field definition includes API type badges, they are displayed next to the field name.
3. Choose an **operator** from the dropdown. If only one operator is available for the selected field, it is auto-selected. Operators are displayed with human-readable labels (`=`, `≠`, `In`, `Not in`, `≥`, `≤`).
4. Enter or select one or more **filter values**. The input type adapts to the field definition:
   - **ENUM fields**: Single or multi-select dropdown (mode switches automatically based on operator).
   - **KEYWORD fields**: Chip-based autocomplete with backend search. Selected values appear as removable chips. The autocomplete panel supports scroll pagination (default page size: 10 items, prefetch threshold: 7/8 of scroll range or 100px from bottom). For ID-based fields (API, APPLICATION, PLAN), the dialog displays resolved labels and falls back to the raw ID if resolution fails.
   - **NUMBER fields**: Numeric input. If the field definition includes a range, a hint is displayed.
   - **STRING fields**: Free-text input.
5. Click **Apply** (for new filters) or **Update** (when editing an existing filter).

The filter condition appears as a chip in the filter bar. If the operator is `In` or `Not in` with multiple values, the chip displays a circular count badge. Clicking a chip opens the edit dialog. Clicking the remove icon (×) deletes the filter. Clicking **Clear all** removes all filters.

### Filter Merging Behavior

| Existing Condition | New Condition | Result |
|--------------------|---------------|--------|
| `API = a` | `API = b` | Merged → `API In [a, b]` |
| `API In [a, b]` | `API = c` | Merged → `API In [a, b, c]` |
| `API = a` | `API = a` | Ignored (duplicate) |
| `STATUS_CODE ≥ 400` | `STATUS_CODE ≤ 499` | Both kept (incompatible operators) |
| `API = a` | `API ≠ b` | Both kept (EQ/NEQ not mergeable) |
| `API = a` | `APPLICATION = b` | Both kept (different fields) |

### Operator Normalization

When you select `=` and add multiple values, the operator is automatically upgraded to `In`. When you select `In` and provide only one value, the chip displays `=` for clarity. The same normalization applies to `≠` and `Not in`.

### Filter Condition Properties

| Property | Description | Example |
|----------|-------------|---------|
| **Field** | The dimension to filter | `API`, `APPLICATION`, `STATUS_CODE` |
| **Label** | Human-readable field name | `API`, `Application`, `Status Code` |
| **Operator** | Comparison logic | `EQ`, `IN`, `GTE` |
| **Values** | Array of identifiers or literals | `["67e246cb-ab02-4da4-8f47-f9fa3e061d6b"]` |
| **Value Labels** | Array of display labels (optional, not persisted in URL) | `["Public API"]` |

## Managing Time Ranges

The time range selector is displayed in the same control row as the filter bar.

1. Select a **relative period** from the dropdown (`1m`, `5m`, `1h`, `1d`, `1w`, `1M`) to scope the dashboard to a rolling time window. The default period is `5m`.
2. To define a **custom absolute range**, select `custom` from the dropdown, choose start and end dates/times in the date picker, and click **Apply**. The custom range is synced to the URL only after clicking Apply.
3. Click the **Refresh** icon to reload all widget data with the current filters and time range.

Changing the time range triggers a refresh of all dashboard widgets. The time range is encoded in the URL query parameter `q` under the `time_range` key.

### Time Range Encoding

| Timeframe Type | Condition | Encoded Format |
|----------------|-----------|:---------------|
| Relative | Period is not `5m` and is valid | `{ type: 'relative', period: '1h' }` |
| Absolute (custom) | Period is `custom` and `from`, `to` are non-null | `{ type: 'absolute', from: 1234567890000, to: 1234567999000 }` |
| Default (`5m`) | Period is `5m` | Omitted from payload (`time_range` undefined) |
