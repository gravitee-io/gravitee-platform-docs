---
hidden: false
noIndex: false
description: Follow one Kafka Service or Message API through the gateway span by span, and narrow the traces to a Kafka operation or a client.
---

# Trace requests

The **Tracing** page follows one API's requests through the gateway. Where the logs tell you what happened to a connection, a trace shows the steps the gateway took inside it.

<figure><img src="../../.gitbook/assets/esm-observability-tracing.png" alt="The Tracing page of Observability with one Kafka Service selected, above a table of Start Time, Status, Service, Operation, and Duration columns"><figcaption><p>Tracing follows one API at a time</p></figcaption></figure>

## Before you begin

Tracing is off until you turn it on for the API, and it takes effect only once the API is redeployed, because the gateway builds the tracer when the API starts.

1. Open the API and select **Reporter Settings**.
2. Turn **OpenTelemetry tracing** on. It needs the API's reporting on first.
3. Redeploy the API.

An API that traces nothing lists no traces here, whatever time range you set.

The spans also have to reach Gamma, which is a platform pipeline rather than an API setting. See [Configure OpenTelemetry tracing and logs](../../platform-management/configure-opentelemetry-tracing-and-logs.md).

## Open the traces for an API

1. From the Gamma console sidebar, select **Event Stream Management**.
2. Open **Observability**.
3. Click **Tracing**.
4. In **Select an API**, pick the API.

Nothing loads until you pick an API. The list offers the started Kafka Services and Message APIs of the environment.

To open the traces of one API from its own page, follow these steps:

1. Open the API from **Kafka Services** or **Message APIs**.
2. In the API's sidebar, under **Observability**, click **Tracing**.

The traces open in a new tab over the last 24 hours.

## Narrow the traces

Once you pick an API, two Kafka filters are available: **Kafka operation** and **Kafka client id**. Both match an exact value.

Consumer group, failure origin, and topic aren't trace filters. To narrow by failure origin, use the logs. To narrow by topic, use a dashboard.

## Read a trace

Each row is one trace. Click it to open the trace beside the list. The header states the service, the total duration, the number of spans, and when the trace started, above two views of the same spans.

* **Timeline** places the spans as a waterfall, each sized by how long it took. This is where a slow step stands out.
* **Lineage** shows the same spans as a graph of what called what.

On a Kafka Service, a trace is one client connection: a connection span at the root, then one span per Kafka protocol request under it, such as `API_VERSIONS`, `SASL_HANDSHAKE`, `METADATA`, `PRODUCE`, and `FETCH`. A trace with only the root span means the gateway isn't emitting the per-request ones.

## Read a span

Click any span, in either view, to open its panel.

<table>
    <thead>
        <tr>
            <th width="180">Section</th>
            <th>What it shows</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Overview</strong></td>
            <td>The service, the operation, the span and trace ids, the parent span, the kind, the start, and the duration.</td>
        </tr>
        <tr>
            <td><strong>Attributes</strong></td>
            <td>The attributes the gateway recorded on this span.</td>
        </tr>
        <tr>
            <td><strong>Policy Diff</strong></td>
            <td>What the policies of this step changed.</td>
        </tr>
        <tr>
            <td><strong>Events</strong></td>
            <td>The span events. A failure is usually recorded here.</td>
        </tr>
        <tr>
            <td><strong>Payload Logs</strong></td>
            <td>The payload records correlated to this span.</td>
        </tr>
    </tbody>
</table>

Each section shows its count, and a section with nothing to show is left out. **Verbose tracing** in **Reporter Settings** is what adds the detailed span events, and it multiplies what a trace stores, so turn it on for an investigation rather than leaving it on.

## Verification

To verify tracing is working as expected, follow these steps:

1. Open **Tracing**.
2. In **Select an API**, pick a started Kafka Service that a client is using, with **OpenTelemetry tracing** on in its **Reporter Settings**.
3. Set the time range to cover recent traffic.
4. Confirm traces are listed.
5. Click a trace.
6. Confirm its spans are shown.
