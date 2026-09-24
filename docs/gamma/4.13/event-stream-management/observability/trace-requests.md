---
hidden: false
noIndex: false
description: Follow one Kafka Service or Message API through the gateway span by span, and narrow the traces to a Kafka operation or a client.
---

# Trace requests

The **Tracing** page follows one API's requests through the gateway. Where the logs tell you what happened to a connection, a trace shows the steps the gateway took inside it.

<figure><img src="../../.gitbook/assets/esm-observability-tracing.png" alt="The Tracing page of Observability with one Kafka Service selected, above a table of Start Time, Status, Service, Operation, and Duration columns"><figcaption><p>Tracing follows one API at a time</p></figcaption></figure>

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

## Verification

To verify tracing is working as expected, follow these steps:

1. Open **Tracing**.
2. In **Select an API**, pick a started Kafka Service that a client is using, with **OpenTelemetry tracing** on in its **Reporter Settings**.
3. Set the time range to cover recent traffic.
4. Confirm traces are listed.
5. Click a trace.
6. Confirm its spans are shown.
