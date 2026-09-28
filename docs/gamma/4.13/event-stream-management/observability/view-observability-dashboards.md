---
hidden: false
noIndex: false
description: Open the prebuilt health and traffic dashboards for your Kafka Services and Message APIs, and narrow them to the APIs, applications, or topics you care about.
---

# View observability dashboards

Event Stream Management ships four dashboards: a health dashboard and a traffic dashboard for Kafka Services, and the same pair for Message APIs. Open a health dashboard to see what's failing and where, or a traffic dashboard to see volumes.

<figure><img src="../../.gitbook/assets/esm-observability-dashboards.png" alt="The Dashboards page of Observability, listing a custom dashboard above the Health and Traffic templates for Kafka Services and for Message APIs"><figcaption><p>The Dashboards page lists the four templates and any custom dashboard saved in the environment</p></figcaption></figure>

## Open a dashboard

1. From the Gamma console sidebar, select **Event Stream Management**.
2. Open **Observability**.
3. Click **Dashboards**.
4. Select the dashboard you want.

To open the health dashboard of one API, follow these steps:

1. Open the API from **Kafka Services** or **Message APIs**.
2. In the API's sidebar, under **Observability**, click **Dashboard**.

The dashboard opens in a new tab, filtered to that API over the last 24 hours.

## Narrow a dashboard

Dashboards offer three Kafka filters that the logs don't: **Failure Side**, **Kafka Topic**, and **Kafka Operation**. **Failure Side** is the dashboard counterpart of the logs filter **Failure Origin**. **Kafka Topic** and **Kafka Operation** don't suggest values, so type the one you want.

## Custom dashboards

Event Stream Management doesn't create, edit, or delete dashboards. Custom dashboards saved in the same environment still appear in the list, marked **Custom**, and open here, for a role with read access to the environment's dashboards. Agent Management and the Gamma API both save custom dashboards. See [Build a custom dashboard](../../agent-management/observe/dashboards/build-a-custom-dashboard.md) and [Save observability dashboards with the Gamma API](../../platform-management/save-observability-dashboards.md).

The four templates don't link back to the logs behind them. To see those rows, open **Logs** and apply the same filters.

## Verification

To verify dashboards are working as expected, follow these steps:

1. Open the traffic dashboard for Kafka Services.
2. Set the time range to a period when a client was producing or consuming.
3. Confirm the charts show data.
