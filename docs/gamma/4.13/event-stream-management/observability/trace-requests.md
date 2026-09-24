---
hidden: false
noIndex: false
description: Follow one Kafka Service or Message API through the gateway span by span, and narrow the traces to a Kafka operation or a client.
---

# Trace requests

The **Tracing** page follows one API's requests through the gateway. Where the logs tell you what happened to a connection, a trace shows the steps the gateway took inside it.

<figure><img src="../../.gitbook/assets/esm-observability-tracing.png" alt="The Tracing page of Observability with one Kafka Service chosen in the required API picker, above a table of Start Time, Status, Service, Operation, and Duration columns"><figcaption><p>Tracing follows one API at a time</p></figcaption></figure>

## Open the traces for an API

1. From the Gamma console sidebar, select **Event Stream Management**.
2. Open **Observability**.
3. Click **Tracing**.
4. Select an API.

Nothing loads until you select an API. The selector offers the started Kafka Services and Message APIs of the environment.

To open the traces for one API directly, open it from **Kafka Services** or **Message APIs** and click its traces link. The traces open over the last 24 hours.

## Narrow the traces

Once you select an API, two Kafka filters are available: **Kafka operation** and **Kafka client id**. Both match an exact value.

Consumer group, failure origin, and topic aren't trace filters. To narrow by failure origin, use the logs. To narrow by topic, use a dashboard.
