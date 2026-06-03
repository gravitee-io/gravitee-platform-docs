# Viewing and Managing Portal Analytics Dashboards

## Creating Portal Analytics Dashboards

Users access analytics dashboards by navigating to the **Analytics** section from the user avatar menu (desktop) or mobile menu. The analytics list page displays all available dashboards in a paginated grid (20 per page). Pinned dashboards appear in a separate **Pinned** section at the top with a 3px accent border. Each dashboard card shows the title, widget count, last modified date, and up to 2 labels (with a "+N" badge for additional labels).

Users can pin a dashboard by clicking the pin icon in the top-right corner of the card. The button is disabled with a "Pin limit reached" tooltip when 4 dashboards are already pinned. Pinned dashboard IDs are stored in browser `localStorage` under the key `analytics-pinned-dashboards`. Clearing browser data or switching devices resets the pinned state.

Clicking a dashboard card navigates to the detail page, where the dashboard renders with all configured widgets. The detail page includes a timeframe selector (preset periods: 5m, 15m, 1h, or custom range) and a filter bar for adding global filters (**API**, **APPLICATION**, **HTTP_STATUS_CODE_GROUP**, **HTTP_STATUS**). Filters are applied across all widgets in the dashboard and can be edited or removed individually, or cleared all at once. The dashboard automatically refreshes when the timeframe, interval, or filters change.

Users can only filter by APIs they are authorized to view and applications they own. If a dashboard's name is empty, the breadcrumb label uses the dashboard ID.
