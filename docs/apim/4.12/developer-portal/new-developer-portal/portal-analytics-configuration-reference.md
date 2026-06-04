# Portal analytics configuration reference

## Prerequisites

Before using portal analytics dashboards, make sure these conditions are met:

* An administrator has set the `portal.next.analytics.enabled` environment parameter to `true`. The New Developer Portal reads the same parameter (surfaced as `portalNext.analytics.enabled` in the portal configuration) to show the **Analytics** navigation and route guards, so this single parameter controls both the API and the UI.
* The user has at least one authorized API or application, so the dashboards have data to display.

## Environment parameter

Portal analytics is controlled by one environment-scoped parameter.

| Property | Description | Default | Required |
|:---------|:------------|:--------|:---------|
| `portal.next.analytics.enabled` | Controls access to portal analytics endpoints and the New Developer Portal analytics UI. When it's `false`, all analytics requests return `403`. | `false` | Yes |
