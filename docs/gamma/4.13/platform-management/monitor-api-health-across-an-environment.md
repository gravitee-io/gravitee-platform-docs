---
hidden: false
noIndex: false
description: Review the health-check availability of the v4 HTTP proxy APIs of an environment from the API Health Check page of the Gamma console, and open the dashboard of any API.
---

# Monitor API health across an environment

The **API Health Check** page shows how available the backend of each API of the selected environment has been over a chosen window. The figures come from the health checks configured on the endpoints of the API. A banner counts the APIs that are in error or in warning, and the table gives the availability of each API and opens its own dashboard.

The page requests v4 HTTP proxy APIs only, so v2 APIs and the other API types never appear on it. An API is monitored only once a health check is enabled on at least one of its endpoint groups or endpoints and the API is deployed. See the health-check step in [Configure endpoints](../api-management/build/configure-your-api-proxy/configure-backend-security.md#step-3-health-check).

## Open the API Health Check page

The page sits in the **System & Security** group of the **Environment** section. It appears only when your role can read the APIs of the environment.

To open the page, complete the following steps:

1. From the Gamma console sidebar, select **Platform Management**.
2. Open the **Environment** section.
3. Under **System & Security**, select **API Health Check**.

While the environment has no v4 HTTP proxy API, the page explains health checks in place of the banner and the table.

<!-- TODO: Screenshot of the API Health Check page with the report banner and the table -->

<figure><img src=".gitbook/assets/PLACEHOLDER-gamma-platform-api-health-check.png" alt=""><figcaption><p>The API Health Check page of the <strong>Environment</strong> section</p></figcaption></figure>

## Choose the window

**Timeframe** sets the window that every availability figure on the page covers: **Last minute**, **Last hour**, **Last day**, **Last week**, or **Last month**. The page opens on **Last minute**. Availability is the share of health checks that succeeded in the window, averaged across the endpoints of the API.

**Refresh** reloads the banner and the availability figures for the window. The window isn't kept in the page URL, so a reopened page starts again on **Last minute**.

## Read the report

The **API Health Check Report** banner covers every API of the environment that has health check enabled, not only the APIs on the current page of the table:

* **All APIs are operational** when no API is degraded.
* Otherwise, how many APIs are in error, at 80% availability or less, and how many are in warning, above 80% and at 95% or less. An API whose checks all failed reports 0% and counts as in error.
* **Could not load health for N APIs.** when the availability of some APIs couldn't be read. Those APIs are left out of the counts.

When no availability at all can be read, the banner reads **Failed to load the API Health Check report.**

## Read the API list

Sort the table by **Name**, and search it with the query syntax shown in the field, for example `name:"My api *"` or `ownerName:admin`. **Filter to APIs with Health Check enabled** fills the search with `has_health_check:true`. The search, the page, the page size, and the sort order are kept in the page URL.

**State** carries the badges of the API: **Started** or **Stopped**, **Published** or **Unpublished**, **Kubernetes** for an API managed by the Kubernetes Operator, **Deprecated** for a deprecated API, and **Draft**, **In Review**, or **Need changes** for an API under review.

**API Availability** shows one of the following:

* The availability over the window, as a percentage.
* **Health check has not been configured** when no endpoint group or endpoint of the API has health check enabled. The row has no actions menu.
* **No data to display** when health check is enabled but no check ran during the window, for example right after the health check was enabled.
* **Failed to load** when the availability couldn't be read. Reading it needs read access to the health checks of that API, so an API you can't read shows this and is counted in **Could not load health for N APIs.**

## Open the dashboard of an API

To open the dashboard of an API, complete the following steps:

1. On the row of an API with health check enabled, open the actions menu.
2. Select **View API-level health check details**. The **Health Check Dashboard** of the API opens in API Management, under **Monitoring**, with its response times and failed checks. See [Monitor endpoint health](../api-management/observe/monitor-endpoint-health.md).

## Verification

To verify the page is working as expected, follow these steps:

1. Enable the health check on an endpoint group of a v4 HTTP proxy API, and deploy the API.
2. Open the **API Health Check** page, wait for a check to run, and select **Refresh**. The row of the API shows its availability, and the banner counts the API when it's in error or in warning.

<!-- TODO: Screenshot of an API row with its availability over the window -->

<figure><img src=".gitbook/assets/PLACEHOLDER-gamma-platform-api-health-check-row.png" alt=""><figcaption><p>An API with health check enabled, with its availability over the window</p></figcaption></figure>

## Next steps

* To be notified when the availability of an API drops, see [Configure environment alerts](configure-environment-alerts.md).
* To inspect the failed checks and response times of one API, see [Monitor endpoint health](../api-management/observe/monitor-endpoint-health.md).
