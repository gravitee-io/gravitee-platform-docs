# Portal Analytics Configuration Reference

## Prerequisites

Before using Portal Analytics Dashboards, ensure the following conditions are met:

- The `PORTAL_NEXT_ANALYTICS_ENABLED` environment parameter must be set to `true` by an administrator.
- The `portalNext.analytics.enabled` configuration flag must be `true` in the portal client configuration.
- Users must have at least one authorized API or application to view meaningful analytics data.
- For time-series and faceted queries, the analytics backend must support the requested interval and grouping dimensions.

## Gateway Configuration

### Environment Parameters

| Property | Description | Example |
|:---------|:------------|:--------|
| `PORTAL_NEXT_ANALYTICS_ENABLED` | Controls access to portal analytics endpoints and UI. When `false`, all analytics requests return 403. | `true` |

### Portal Client Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `portalNext.analytics.enabled` | Enables analytics features in the Next Gen Portal UI, including navigation links and route guards. | `true` |
