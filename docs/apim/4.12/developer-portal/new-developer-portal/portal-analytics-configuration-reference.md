---
hidden: true
noIndex: true
---

# Portal analytics configuration reference

## Prerequisites

Before using portal analytics dashboards, make sure these conditions are met:

* An administrator has enabled analytics for the New Developer Portal (see [Enable analytics in the Console](#enable-analytics-in-the-console)).
* At least one analytics dashboard exists in the environment. See [Create portal analytics dashboards](../../analyze-and-monitor-apis/dashboards/creating-portal-analytics-dashboards.md).
* Users are signed in to the New Developer Portal and have at least one authorized API or application, so the dashboards have data to display.

## Enable analytics in the Console

1. From the **Settings** menu, navigate to the **Portal** section, and then click **Settings**.
2. In the **New Developer Portal** card, turn on **Enable Analytics**.
3. Click **Save**.

This sets the `portal.next.analytics.enabled` environment parameter to `true`. The New Developer Portal reads the same value (surfaced as `portalNext.analytics.enabled` in the portal configuration) to show the **Analytics** navigation entry and route guards, so this single parameter controls both the Portal API and the UI.

## Environment parameter

Portal analytics is controlled by one environment-scoped parameter.

| Property | Description | Default | Required |
|:---------|:------------|:--------|:---------|
| `portal.next.analytics.enabled` | Controls access to portal analytics endpoints and the New Developer Portal analytics UI. When it's `false`, all analytics requests return `403`. | `false` | Yes |

## See also

* [Portal analytics dashboards overview](../../analyze-and-monitor-apis/dashboards/portal-analytics-dashboards-overview.md)
* [Create portal analytics dashboards](../../analyze-and-monitor-apis/dashboards/creating-portal-analytics-dashboards.md)
* [View and manage portal analytics dashboards](viewing-and-managing-portal-analytics-dashboards.md)
* [Portal analytics API reference](../../configure-and-manage-the-platform/management-api/portal-analytics-management-api-reference.md)
