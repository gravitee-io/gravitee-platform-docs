# View and manage portal analytics dashboards

The New Developer Portal presents pre-configured analytics dashboards that API consumers and administrators can browse, pin, and filter. Dashboards are read-only in the portal. Administrators create and manage them from **Observability** > **Dashboards** in the APIM Console. For prerequisites and enablement, see [Portal analytics configuration reference](portal-analytics-configuration-reference.md). For the Console workflow, see [Create portal analytics dashboards](../../analyze-and-monitor-apis/dashboards/creating-portal-analytics-dashboards.md).

## View dashboards

You must be signed in to the New Developer Portal. To open analytics, click **Analytics** in the user avatar menu on desktop, or in the mobile menu. The analytics list page displays the available dashboards in a paginated grid of 20 per page. Pinned dashboards appear in a separate **Pinned** section at the top, marked with an accent border. Each dashboard card shows the title, the widget count, the last modified date, and the dashboard's labels. When the labels don't all fit, the card shows as many as fit and adds a `+N` badge for the rest.

<!-- SME-REQUIRED: Screenshot of the analytics list page with the Pinned section at the top -->

## Pin and unpin dashboards

To pin a dashboard, click the pin icon in the top-right corner of its card. You can pin up to 4 dashboards. When 4 are already pinned, the pin icon is disabled and shows a **Pin limit reached** tooltip. Pinned dashboard IDs are stored in the browser under the `analytics-pinned-dashboards` `localStorage` key, so clearing browser data or switching devices resets which dashboards are pinned. To unpin a dashboard, click the pin icon again.

## Open a dashboard and adjust the view

Click a dashboard card to open its detail page, where the dashboard renders with all of its configured widgets. The detail page includes a timeframe selector with preset periods (Last minute, Last 5 minutes, Last hour, Last day, Last week, and Last month) and a custom range. The default is Last 5 minutes.

A filter bar lets you add global filters for **API**, **APPLICATION**, **HTTP_STATUS_CODE_GROUP**, and **HTTP_STATUS**. Filters apply across all widgets in the dashboard. You can edit or remove each filter individually, or clear them all at once. The dashboard refreshes automatically when the timeframe, interval, or filters change. Dashboards support dynamic filtering by API, application, plan, status code, and custom time ranges with URL-based state persistence. For details, see [Dashboard Filtering and Time Range Controls](../../analyze-and-monitor-apis/dashboards/dashboard-filtering-and-time-range-controls.md).

You can only filter by APIs you're authorized to view and applications you own. If a dashboard's name is empty, the breadcrumb label uses the dashboard ID.

## See also

* [Portal analytics dashboards overview](../../analyze-and-monitor-apis/dashboards/portal-analytics-dashboards-overview.md)
* [Create portal analytics dashboards](../../analyze-and-monitor-apis/dashboards/creating-portal-analytics-dashboards.md)
* [Portal analytics API reference](../../configure-and-manage-the-platform/management-api/portal-analytics-management-api-reference.md)
