---
hidden: false
noIndex: false
description: List what the gateway recorded for your Kafka Services and Message APIs on one screen, narrow it with filters, and choose the columns each family needs.
---

# View connection logs

The **Logs** page of **Observability** lists what the gateway recorded across every API in the environment, newest first, with a chart of the same rows above the table. One row is one Kafka connection, or one request that opened a Message API stream.

<figure><img src="../../../.gitbook/assets/esm-observability-logs.png" alt="The Logs page of Observability, with a connection chart above a table whose rows carry the Timestamp, Error Key, API, API Type, Application, and Plan columns of the Common column set"><figcaption><p>The Logs page lists connections and requests across the environment</p></figcaption></figure>

## Open the logs

1. From the Gamma console sidebar, select **Event Stream Management**.
2. Open **Observability**.
3. Click **Logs**.

To land on the logs already narrowed to one API, open that API instead and use its own link. See [Open the logs for one API](#open-the-logs-for-one-api).

## What the page lists

The page covers the two families Event Stream Management manages, and nothing else. A Kafka Service row and a Message API row sit in the same table, told apart by the **API Type** column, which reads **Kafka Service** or **Message API**.

Your HTTP proxies, LLM proxies, and other APIs never appear here, whatever the environment holds.

## Choose the columns

The two families barely share a useful column, so the page offers three column sets and opens on **Common**.

<table>
    <thead>
        <tr>
            <th width="150">Column set</th>
            <th>What it shows</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Common</strong></td>
            <td>What both families fill, so a mixed list opens with no empty cells. Timestamp, error key, API, API type, application, and plan.</td>
        </tr>
        <tr>
            <td><strong>Kafka</strong></td>
            <td>Where a connection failed. Adds the connection status, the failure origin, the Kafka client id, and the connection duration.</td>
        </tr>
        <tr>
            <td><strong>Message</strong></td>
            <td>What was called and how it answered. Adds the entrypoint, the HTTP status, the request URI, and the gateway response time.</td>
        </tr>
    </tbody>
</table>

A column set selects columns without reordering them, so all three share one order.

Further columns are available but hidden until you pick them, including the plan, the broker, the gateway, the client library, and the request id.

## Read a Kafka row

Two columns carry the diagnosis on a Kafka row.

**Native Connection Status** is one of **Connected**, **Disconnected**, **Connection error**, **Session error**, or **Internal error**.

**Failure Origin** names the hop that broke.

<table>
    <thead>
        <tr>
            <th width="210">Failure origin</th>
            <th>What it means</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Client ↔ Gateway</strong></td>
            <td>The connection broke between the Kafka client and the gateway, for example on the TLS or SASL handshake, or on the plan credentials.</td>
        </tr>
        <tr>
            <td><strong>Gateway ↔ Broker</strong></td>
            <td>The connection broke between the gateway and the broker, for example an unreachable broker, an unknown topic, or a broker ACL.</td>
        </tr>
        <tr>
            <td><strong>Gateway internal</strong></td>
            <td>The gateway itself failed.</td>
        </tr>
        <tr>
            <td><strong>Undetermined</strong></td>
            <td>Neither the gateway nor the error key placed the failure.</td>
        </tr>
    </tbody>
</table>

A row that didn't fail shows a dash instead of a badge.

A row with an error key counts as a failure even when its status reads **Connected** or **Disconnected**.

Open any row for the full diagnosis. See [Diagnose a failed Kafka connection](diagnose-a-failed-kafka-connection.md).

## Narrow the list

**Add filter** offers the filters grouped by the family they apply to. The ones both families answer, such as **API**, **Application**, **Plan**, and **Error Key**, sit under **Common**, and each family's own filters sit under their own group.

These filters apply to the Kafka rows.

<table>
    <thead>
        <tr>
            <th width="230">Filter</th>
            <th>Narrows to</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Native Connection Status</strong></td>
            <td>One or more of the five connection statuses.</td>
        </tr>
        <tr>
            <td><strong>Failure Origin</strong></td>
            <td>The hop that broke, or <strong>No failure</strong>.</td>
        </tr>
        <tr>
            <td><strong>Kafka Client ID</strong></td>
            <td>The <code>client.id</code> the Kafka client sent.</td>
        </tr>
    </tbody>
</table>

**Kafka Topic** and **Kafka Operation** narrow a dashboard rather than this table, so they aren't offered here. **Failure Origin** is the logs filter, and its dashboard counterpart is named **Failure Side**.

The chart above the table counts the same rows the table lists, so the total under it matches the table even in an environment that also serves other API families.

## Open the logs for one API

Each Kafka Service and each Message API links straight to its own logs.

1. Open the API from **Kafka Services** or **Message APIs**.
2. Click the observability link on the API's page.

The logs open filtered to that API over the last 24 hours. The same group links to that API's health dashboard and its traces, all three on the same 24-hour window.

The links appear only for a role that can read the APIs or the dashboards of the environment. The traces link needs to read the APIs.

## Why an API shows nothing

An API reports nothing until reporting is switched on for it, and the API's own page says so when it isn't.

A **Kafka Service** shows a **Connection metrics are disabled** warning, and it reports no connection logs until **both** the analytics switch and the reporter metrics flag are on for it. Turning on only one of the two leaves the logs empty and the banner in place.

A **Message API** shows a **Runtime logs are disabled** warning. It records nothing until analytics is on, it captures at least one mode, the entrypoint or the endpoint, and it captures at least one phase, the request or the response. A mode with no phase records nothing, and so does a phase with no mode.

Both banners link to the API's **Reporter Settings**, where you switch reporting on.

<figure><img src="../../../.gitbook/assets/esm-observability-metrics-disabled.png" alt="The Overview page of a Kafka Service showing the Connection metrics are disabled warning, which links to Reporter Settings"><figcaption><p>A Kafka Service that reports nothing says so on its own page</p></figcaption></figure>

## Verification

To verify the logs are reaching the page, follow these steps:

1. Open a Kafka Service and confirm no **Connection metrics are disabled** warning is shown.
2. Connect a Kafka client to that service, letting it succeed or fail.
3. Open **Observability**, then click **Logs**.
4. Set the time range to cover the connection, and confirm a row appears with the expected **Native Connection Status**.
