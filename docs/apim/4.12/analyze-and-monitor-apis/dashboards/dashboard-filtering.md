# Dashboard Filtering

## Overview

Dashboard filtering and time range selection enable API platform administrators to focus analytics dashboards on specific APIs, applications, plans, and time periods. Filters and time ranges are encoded in the URL, allowing users to share dashboard views and return to saved configurations. The feature supports both relative time periods (e.g., last 5 minutes, last 1 hour) and custom absolute date ranges.

## Key Concepts

### Filter Conditions

A filter condition narrows dashboard data to specific field values. Each condition consists of a field (e.g., API, Application, Status Code), an operator (e.g., equals, in, not in), and one or more values. Multiple values for the same field are automatically merged into array-based operators (`IN`, `NOT_IN`) when compatible. Filters are displayed as removable chips in the dashboard toolbar.

### Time Ranges

Time ranges define the temporal scope of dashboard data. Users can select from predefined relative periods (`1m`, `5m`, `1h`, `1d`, `1w`, `1M`) or specify a custom absolute range with start and end timestamps. The default period is 5 minutes. Time ranges are synchronized with the URL and persist across page reloads.

### Filter Label Resolution

Filter values for APIs, applications, and plans are stored as stable identifiers (UUIDs) but displayed with human-readable labels. The platform resolves these identifiers into display names via the `/environments/{envId}/observability/filters/resolve` endpoint. Label resolution requests are limited to 10 filter entries and 100 identifiers per entry.

## Prerequisites

Before creating dashboard filters, ensure the following requirements are met:

* User must have `ENVIRONMENT_DASHBOARD` read permission to view dashboards.
* User must have `environment-dashboard-u` permission to add, edit, or remove filters.
* Dashboard must be configured with filterable fields via the `FILTER_DEFINITION_PROVIDER` injection token.
* For keyword-based filters (API, Application, Plan), the `FILTER_VALUES_PROVIDER` must supply autocomplete values.

## Creating Dashboard Filters

1. Navigate to the dashboard page where the filter bar is displayed.
2. Click **Add filter** to open the filter dialog.
3. Select a field from the **Filter by** autocomplete dropdown (e.g., API, Application, Status Code).
4. Choose an operator from the **Choose operator** dropdown (e.g., `=`, `≠`, `In`, `Not in`, `≥`, `≤`).
5. Enter or select one or more values in the **Filter value** field. For keyword filters (API, Application, Plan), use the autocomplete chip grid with **Search by name** placeholder. For enum filters, select from the dropdown. For number or string filters, enter the value directly.
6. Click **Apply** to add the filter condition.

The filter appears as a chip in the filter bar. Click the chip to edit it, or click the remove icon (×) to delete it. Click **Clear all filters** to remove all active conditions at once.

| Field | Description | Example |
|:------|:------------|:--------|
| **Filter by** | The dashboard field to filter on (e.g., API, Application, Status Code, HTTP Path). Displays field label and optional API type badges. | `API`, `Status Code` |
| **Choose operator** | The comparison operator. Available operators depend on the field type. | `=`, `In`, `≥` |
| **Filter value** | The value(s) to match. Input type varies by field: autocomplete chip grid for keyword fields, dropdown for enums, text or number input for scalars. | `Public API`, `200`, `/api/v1` |

{% hint style="info" %}
**Filter merging behavior**: When adding a filter with the same field as an existing condition, the platform merges values if the operators are compatible. For example, adding `Status Code = 200` to an existing `Status Code = 404` condition produces `Status Code in [200, 404]`. Incompatible operators (e.g., `=` and `≥`) create separate conditions.
{% endhint %}

**Operator display rules**:
* Single-value filters with `EQ` display as `=` (e.g., `Status Code = 200`).
* Multi-value filters with `IN` display as `in` with a count badge (e.g., `Status Code in ⬤ 2`).
* Multi-value filters with `NOT_IN` display as `not in` with a count badge.
* Inequality operators display as symbols: `≠`, `≥`, `≤`.
