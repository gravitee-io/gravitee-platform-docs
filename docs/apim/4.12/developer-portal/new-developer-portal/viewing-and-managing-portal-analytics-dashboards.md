# View and manage portal analytics dashboards

The New Developer Portal presents pre-configured analytics dashboards that API consumers and administrators can browse, pin, and filter. Dashboards are read-only in the portal. They're created and managed in the Console.

## View dashboards

To open analytics, click **Analytics** in the user avatar menu on desktop, or in the menu on mobile. The analytics list page displays the available dashboards in a paginated grid of 20 per page. Pinned dashboards appear in a separate **Pinned** section at the top, marked with an accent border. Each dashboard card shows the title, the widget count, the last modified date, and the dashboard's labels. When the labels don't all fit, the card shows as many as fit and adds a `+N` badge for the rest.

<!-- TODO: Screenshot of the analytics list page with the Pinned section at the top -->
<figure><img src="../../.gitbook/assets/PLACEHOLDER-portal-analytics-list.png" alt=""><figcaption><p>The analytics list page</p></figcaption></figure>

## Pin and unpin dashboards

To pin a dashboard, click the pin icon in the top-right corner of its card. You can pin up to 4 dashboards. When 4 are already pinned, the pin icon is disabled and shows a **Pin limit reached** tooltip. Pinned dashboard IDs are stored in the browser under the `analytics-pinned-dashboards` `localStorage` key, so clearing browser data or switching devices resets which dashboards are pinned. To unpin a dashboard, click the pin icon again.

## Open a dashboard and adjust the view

Click a dashboard card to open its detail page, where the dashboard renders with all of its configured widgets. The detail page includes a timeframe selector with preset periods (Last minute, Last 5 minutes, Last hour, Last day, Last week, and Last month) and a custom range. The default is Last 5 minutes.

<!-- TODO: Screenshot of a dashboard detail page showing widgets, the timeframe selector, and the filter bar -->
<figure><img src="../../.gitbook/assets/PLACEHOLDER-portal-analytics-detail.png" alt=""><figcaption><p>A dashboard detail page</p></figcaption></figure>

A filter bar lets you add global filters for **API**, **APPLICATION**, **HTTP_STATUS_CODE_GROUP**, and **HTTP_STATUS**. Filters apply across all widgets in the dashboard. You can edit or remove each filter individually, or clear them all at once. The dashboard refreshes automatically when the timeframe, interval, or filters change.

You can only filter by APIs you're authorized to view and applications you own. If a dashboard's name is empty, the breadcrumb label uses the dashboard ID.
