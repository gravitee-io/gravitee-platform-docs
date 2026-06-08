# Create portal analytics dashboards

Portal analytics dashboards are environment-scoped dashboards that administrators create in the APIM Console. After you enable portal analytics, every dashboard in the environment appears in the New Developer Portal analytics list. Portal users can browse, pin, and filter those dashboards, but cannot edit their layout or widgets.

## Prerequisites

Before creating dashboards for the New Developer Portal:

* Turn on **Enable Analytics** in the Console. See [Enable analytics in the Console](../../developer-portal/new-developer-portal/portal-analytics-configuration-reference.md#enable-analytics-in-the-console).
* Make sure the New Developer Portal is enabled for the environment.

You need the following environment permissions:

* `ENVIRONMENT_DASHBOARD[READ]` to view dashboards
* `ENVIRONMENT_DASHBOARD[CREATE]` to create dashboards
* `ENVIRONMENT_DASHBOARD[UPDATE]` to edit dashboards
* `ENVIRONMENT_DASHBOARD[DELETE]` to delete dashboards

## Create a dashboard from a template

1. In the side navigation, click **Observability**.
2. Click **Dashboards**.
3. Click **Create dashboard**, and then click **Create from template**.
4. Pick a template that matches the metrics you want portal users to see:
   * **HTTP Proxy** — API traffic, errors, and latency for V4 proxy APIs
   * **LLM** — LLM token usage, cost, and request metrics
   * **MCP** — MCP request volume, latency, and error breakdown
5. Click **Use template**.

The Console opens the new dashboard in the editor. All environment dashboards are published to the New Developer Portal automatically. You do not need a separate publish step.

## Customize the dashboard

After the template is applied, you can adjust how the dashboard appears in the portal:

1. Click **Dashboard options**, and then click **Edit**.
2. Update the **Name** and **Labels**. Labels appear on dashboard cards in the New Developer Portal.
3. Click **Save**.

You can also change the default timeframe and widget layout from the dashboard editor. Portal users can override the timeframe and add filters when they open the dashboard, but they inherit the widget definitions you configure here.

## Verify in the New Developer Portal

1. Confirm **Enable Analytics** is turned on in **Settings** > **Portal** > **Settings**.
2. Sign in to the New Developer Portal as a user who should see the dashboard.
3. Open **Analytics** from the user avatar menu (desktop) or the mobile menu.
4. Confirm the dashboard appears in the list and opens with the expected widgets.

For end-user behavior (pinning, filters, and timeframes), see [View and manage portal analytics dashboards](../../developer-portal/new-developer-portal/viewing-and-managing-portal-analytics-dashboards.md).

## See also

* [Portal analytics dashboards overview](portal-analytics-dashboards-overview.md)
* [Portal analytics configuration reference](../../developer-portal/new-developer-portal/portal-analytics-configuration-reference.md)
* [Portal analytics API reference](../../configure-and-manage-the-platform/management-api/portal-analytics-management-api-reference.md)
