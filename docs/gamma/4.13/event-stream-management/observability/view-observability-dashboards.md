---
hidden: false
noIndex: false
description: Open a prebuilt board for the health or the traffic of your Kafka Services and Message APIs, and narrow it to the APIs, applications, or topics you care about.
---

# View observability dashboards

The **Dashboards** page of **Observability** opens on a prebuilt board. Event Stream Management ships four, two per family, and they read the same reported data the logs do.

<!-- TODO: Screenshot of the Observability Dashboards page showing a Kafka Service board -->
<figure><img src="../../../.gitbook/assets/PLACEHOLDER-esm-observability-dashboards.png" alt=""><figcaption><p>The Dashboards page opens on a prebuilt board</p></figcaption></figure>

## Open a dashboard

1. From the Gamma console sidebar, select **Event Stream Management**.
2. Open **Observability**.
3. Click **Dashboards**.
4. Select the board you want.

**Dashboards** is the first item in the group, so opening **Observability** without picking an item lands here rather than on the logs.

## The boards

<table>
    <thead>
        <tr>
            <th width="150">Family</th>
            <th width="120">Board</th>
            <th>What it answers</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Kafka Service</td>
            <td><strong>Health</strong></td>
            <td>Connection health, availability, and latency of the Kafka Services: what is failing, where, and for whom.</td>
        </tr>
        <tr>
            <td>Kafka Service</td>
            <td><strong>Traffic</strong></td>
            <td>Volumes, throughput, and usage of the Kafka Services exposed by the gateway: who produces and who consumes.</td>
        </tr>
        <tr>
            <td>Message API</td>
            <td><strong>Health</strong></td>
            <td>Where Message APIs fail: refused connections, message errors, and how long the gateway holds a message.</td>
        </tr>
        <tr>
            <td>Message API</td>
            <td><strong>Traffic</strong></td>
            <td>Volumes, direction, and connectors of the Message APIs exposed by the gateway: what flows, and through what.</td>
        </tr>
    </tbody>
</table>

Each board's title on screen joins the two, as in the health board for Kafka Services.

The Kafka health board breaks failures down by the side that caused them, and ranks the Kafka Services in error alongside the failing clients and client libraries. The Kafka traffic board reports messages and data volume per interval. It also ranks the services, topics, and applications that produce and consume the most.

## Narrow a board

The filters work like the ones on the logs, grouped by the family they apply to. A few are specific to a board rather than to the logs.

<table>
    <thead>
        <tr>
            <th width="230">Filter</th>
            <th>Narrows to</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Failure Side</strong></td>
            <td>The hop that broke. This is the dashboard counterpart of the logs filter named <strong>Failure Origin</strong>.</td>
        </tr>
        <tr>
            <td><strong>Kafka Topic</strong></td>
            <td>One or more topics. Offered on a board only.</td>
        </tr>
        <tr>
            <td><strong>Kafka Operation</strong></td>
            <td>One or more Kafka operations. Offered on a board only.</td>
        </tr>
        <tr>
            <td><strong>Native Connection Status</strong></td>
            <td>One or more of the five connection statuses. Offered on a board and on the logs.</td>
        </tr>
    </tbody>
</table>

**Kafka Topic** and **Kafka Operation** don't offer a list of values to pick from, so type the value you want.

## Open the dashboard for one API

Each Kafka Service and each Message API links to its own health board.

1. Open the API from **Kafka Services** or **Message APIs**.
2. Click the dashboard link on the API's page.

The board opens filtered to that API over the last 24 hours, on the health board for that API's family.

## What you can't do here

Event Stream Management ships these four boards read-only. The **Dashboards** page of this module doesn't create, edit, or delete a board, so there's no way to save a custom one alongside the templates.

A board carries no link back to the matching logs. To go from a board to the rows behind it, open **Logs** and apply the same filters.

## Verification

To verify a board is reading your traffic, follow these steps:

1. Open **Observability**, then click **Dashboards**.
2. Select the traffic board for Kafka Services.
3. Set the time range to a period when a client was producing or consuming.
4. Confirm the messages per interval chart is populated rather than empty.
