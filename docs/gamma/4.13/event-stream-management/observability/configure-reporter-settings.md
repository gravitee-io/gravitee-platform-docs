---
hidden: false
noIndex: false
description: >-
  Turn on what a Kafka Service or a Message API reports, and how much of it, so
  its traffic reaches the dashboards, the logs, and the traces.
---

# Configure reporter settings

Nothing in **Observability** shows an API until that API reports. **Reporter Settings** is where you turn reporting on, per API. The two families report different things, so each has its own version of the screen.

## Open Reporter Settings

1. Open the API from **Kafka Services** or **Message APIs**.
2. In the API's sidebar, under **Operations**, click **Reporter Settings**.

Changing a setting reveals **Save changes** and **Discard**. The controls are read-only for a role that can't update the API definition.

## Configure a Kafka Service

<table>
    <thead>
        <tr>
            <th width="300">Setting</th>
            <th>Turns on</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Enable event-metrics reporting</strong></td>
            <td>Per-event metrics, messages and offsets. The master switch: with it off the service reports nothing.</td>
        </tr>
        <tr>
            <td><strong>Enable connection-metrics reporting</strong></td>
            <td>Connection and client lifecycle metrics. This is what fills the connection logs.</td>
        </tr>
        <tr>
            <td><strong>OpenTelemetry tracing</strong></td>
            <td>Traces for this service. Needs event-metrics reporting on.</td>
        </tr>
        <tr>
            <td><strong>Verbose tracing</strong></td>
            <td>Detailed span events. Needs tracing on.</td>
        </tr>
    </tbody>
</table>

The four cascade: turning event-metrics reporting off takes tracing and verbose tracing down with it.

A Kafka Service reports connection logs only when the first two are both on. Turning on one of the two leaves the logs empty and leaves **Connection metrics are disabled** on the service's **Overview** page.

## Configure a Message API

The **Settings** card has one switch in its header, and the rest of the card applies underneath it.

**Logging mode** picks which leg to capture, **Entrypoint** for client to gateway or **Endpoint** for gateway to broker. **Logging phase** picks which phases, **Request** or **Response**. Both are required: a mode with no phase captures nothing, and so does a phase with no mode. They govern captured content only — the API's connections reach the logs as soon as the header switch is on.

**Content data** picks what to store alongside each logged event: **Message content** for the body itself, **Message headers**, **Message metadata**, and **Headers** for the transport headers of the request rather than of individual messages.

{% hint style="warning" %}
**Message content** writes message bodies to the log index as they are. Anything personal or secret they carry is stored there and searchable, and this is the option that grows the index fastest. Turn it on for an investigation, not by default.
{% endhint %}

**Message sampling** decides how many messages of a stream are kept: **Probabilistic** keeps a share given as a probability, **Count** keeps one message out of every N, **Temporal** keeps one per interval given as an ISO-8601 duration such as `PT1S`, and **Windowed Count** keeps a count over a sliding window such as `2/PT15S`. The bounds come from your environment, and the screen states the limit of whichever strategy you pick. A value outside them blocks the save.

**Display conditions** narrow what gets logged with an Expression Language expression, on the request phase and on the message. Both are optional, and an empty one logs everything. Your environment also caps how long runtime logging stays on: when it does, the platform adds a deadline to the request condition and the screen states the date this API stops logging. Saving again pushes it back.

The **OpenTelemetry** card turns on **OpenTelemetry tracing**, **Verbose tracing** for detailed span events with headers, context attributes, and policy execution details, and **OTel logs** to emit message payloads as OpenTelemetry log records correlated to the active trace. Span redaction rules sit below.

## What each setting unlocks

<table>
    <thead>
        <tr>
            <th width="330">To see</th>
            <th>Turn on</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>A Kafka Service in the logs and the dashboards</td>
            <td>Event-metrics reporting <strong>and</strong> connection-metrics reporting.</td>
        </tr>
        <tr>
            <td>A Message API in the logs and the dashboards</td>
            <td>The switch on the <strong>Settings</strong> card.</td>
        </tr>
        <tr>
            <td>Bodies and messages inside a Message API row</td>
            <td>A logging mode, a phase, and the matching content options.</td>
        </tr>
        <tr>
            <td>Traces for either family</td>
            <td>OpenTelemetry tracing, then redeploy the API.</td>
        </tr>
    </tbody>
</table>

## Verification

To verify an API is reporting, follow these steps:

1. Open the API.
2. Confirm its **Overview** page shows no reporting warning.
3. Send traffic through it.
4. Open **Logs** and set the time range to cover that traffic.
5. Confirm a row for that API appears.
