---
hidden: false
noIndex: false
description: >-
  Choose what a Kafka Service or a Message API reports, and how much of it, so
  its traffic reaches the dashboards, the logs, and the traces. Pick the
  settings each one needs.
---

# Configure reporter settings

Nothing in **Observability** shows an API until that API reports. **Reporter Settings** is where you choose what each API reports. The two families report different things, so each has its own version of the screen.

## Open Reporter Settings

1. Open the API from **Kafka Services** or **Message APIs**.
2. In the API's sidebar, under **Operations**, click **Reporter Settings**.

As soon as the page holds an unsaved change, a bar at the bottom of the page shows **Unsaved changes** with **Discard** and **Save changes**. If you leave the page with unsaved changes, the console asks you to confirm. The controls are read-only for a role that can't update the API definition.

## Configure a Kafka Service

The **Settings** card holds two checkboxes, and the **OpenTelemetry** card holds two more.

<table>
    <thead>
        <tr>
            <th width="250">Setting</th>
            <th>What it reports</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Aggregated metrics</strong></td>
            <td>Periodic counters of messages, bytes, connections, and authentication, per topic and per Kafka operation. They feed the traffic and operation charts of the dashboards, the <strong>Kafka Service activity</strong> charts of a connection, and the runtime alerts on topic traffic, operations, policy rejections, and authentication.</td>
        </tr>
        <tr>
            <td><strong>Connection events</strong></td>
            <td>One record per connection lifecycle event. These records fill the logs. Clear it and the Kafka Service writes no connection record at all, whatever events are selected under it.</td>
        </tr>
        <tr>
            <td><strong>OpenTelemetry tracing</strong></td>
            <td>Traces for this Kafka Service. Needs <strong>Aggregated metrics</strong>.</td>
        </tr>
        <tr>
            <td><strong>Verbose tracing</strong></td>
            <td>Detailed span events. Needs <strong>OpenTelemetry tracing</strong>.</td>
        </tr>
    </tbody>
</table>

The tracing options cascade: with **Aggregated metrics** cleared, **OpenTelemetry tracing** and **Verbose tracing** can't be selected, and saving turns both off.

{% hint style="warning" %}
Clearing **Aggregated metrics** silences the runtime alerts on topic traffic, operations, policy rejections, and authentication, because those alerts are built from the aggregated counters. Alerts on connections are unaffected. The Kafka Service's **Alerts** page shows the **Aggregated metrics are off, so most rules here will not work** warning, which tells you to turn on **Aggregated metrics** in **Reporter Settings**.
{% endhint %}

The gateway reads these settings when it deploys the Kafka Service. After you save, click **Deploy** for the change to reach the gateway.

### Choose which connection events are reported

Under **Connection events**, three checkboxes choose which events write a record:

* **Connected**. A record when a client opens a connection: who connected, with which plan and credential.
* **Disconnected**. A record when a connection closes normally, with how long it lasted and how many requests it served. It isn't written for a connection that ends in an error. It roughly doubles the records a healthy Kafka Service writes.
* **Errors**. A record when a connection fails, with the status **Connection error**, **Session error**, or **Internal error**. A connection that survives an error and later fails writes one record for each.

A Kafka Service whose events were never chosen reports **Connected** and **Errors**, and the checkboxes show that selection. **Disconnected** is off until you select it.

The three checkboxes are unavailable while **Connection events** is cleared. The last selected checkbox can't be cleared. To stop reporting connections, clear **Connection events** instead.

{% hint style="info" %}
Keep **Errors** selected when you select **Disconnected**. Without **Errors**, a connection that fails writes no closing record, so its opening record reads as a connection that never ended.
{% endhint %}

### What a Kafka Service shows on its Overview page

The Kafka Service's **Overview** page shows **Connection events are disabled** while **Connection events** is cleared. The warning says that the logs stay empty for the Kafka Service, and links to **Reporter Settings**.

## Configure a Message API

The **Enable analytics** checkbox in the header of the **Settings** card turns reporting on. With it selected, the API's connections reach the logs and the dashboards. The rest of the page chooses what each logged connection carries:

* **Logging mode**, **Logging phase**, and **Content data** choose which legs, phases, and parts of each message are captured.
* **Message sampling** chooses how many messages of a stream are kept.
* **Display conditions** narrow what gets logged with Expression Language.
* The **OpenTelemetry** card turns on tracing, verbose tracing, and OTel logs, with span redaction rules.

For each option and its limits, see [Configure reporter settings for a Message API](../apis/message-apis/configure-reporter-settings.md).

The logs of webhook deliveries are set apart, on the webhook entrypoint. On the Message API's **Webhooks** page, **Settings** opens the **Webhook logs reporting settings** dialog, with **Enable webhook logs** and the request and response bodies and headers. The dialog also shows the API's message sampling, which you edit in **Reporter Settings**. See [View webhook delivery attempts](../apis/message-apis/view-webhook-delivery-attempts.md).

## What each setting unlocks

<table>
    <thead>
        <tr>
            <th width="330">To see</th>
            <th>Select</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>A Kafka Service in the logs</td>
            <td><strong>Connection events</strong>, with the events you want listed.</td>
        </tr>
        <tr>
            <td>A Kafka Service in the dashboards</td>
            <td><strong>Aggregated metrics</strong> for traffic and operations, and <strong>Connection events</strong> for the failed-connection charts.</td>
        </tr>
        <tr>
            <td>Runtime alerts on topic traffic, operations, policy rejections, and authentication for a Kafka Service</td>
            <td><strong>Aggregated metrics</strong>.</td>
        </tr>
        <tr>
            <td>A Message API in the logs and the dashboards</td>
            <td><strong>Enable analytics</strong> on the <strong>Settings</strong> card.</td>
        </tr>
        <tr>
            <td>Bodies and messages inside a Message API row</td>
            <td>A logging mode, a phase, and the matching content options.</td>
        </tr>
        <tr>
            <td>Traces for either family</td>
            <td><strong>OpenTelemetry tracing</strong>, then deploy the API again.</td>
        </tr>
    </tbody>
</table>

## Verification

To verify an API is reporting, follow these steps:

1. Open the API.
2. Confirm its **Overview** page shows no reporting warning.
3. Send traffic through it.
4. Open **Logs**.
5. Set the time range to cover that traffic.
6. Confirm a row for that API appears.
