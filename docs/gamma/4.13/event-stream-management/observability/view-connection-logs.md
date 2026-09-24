---
hidden: false
noIndex: false
description: List what the gateway recorded for your Kafka Services and Message APIs, narrow it with filters, and find the connections that failed.
---

# View connection logs

The **Logs** page lists the connections and requests the gateway recorded for your Kafka Services and Message APIs, newest first. A Kafka row is one client connection, and a Message API row is one request that opened a stream. Your HTTP proxies, LLM proxies, and other APIs never appear here.

<figure><img src="../../.gitbook/assets/esm-observability-logs.png" alt="The Logs page of Observability, with a connection chart above a table whose rows carry the Timestamp, Error Key, API, API Type, Application, and Plan columns of the Common column set"><figcaption><p>The Logs page lists connections and requests across the environment</p></figcaption></figure>

## Open the logs

1. From the Gamma console sidebar, select **Event Stream Management**.
2. Open **Observability**.
3. Click **Logs**.

To open the logs for one API, open the API from **Kafka Services** or **Message APIs** and click its logs link. The logs open filtered to that API over the last 24 hours.

## Find failed Kafka connections

Switch the column set from **Common** to **Kafka** to add each connection's status, failure origin, client ID, and duration. For Message APIs, **Message** adds the entrypoint, the HTTP status, the request URI, and the gateway response time.

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

A row with an error key is a failure even when its status reads **Connected** or **Disconnected**.

Filter on **Failure Origin** to narrow the list to one hop, or on **Kafka Client ID** to follow one client. Topic and Kafka operation filters are on the dashboards, not here.

Open a row for the full diagnosis. See [Diagnose a failed Kafka connection](diagnose-a-failed-kafka-connection.md).

## Why an API shows nothing

An API records nothing until reporting is switched on for it, and its own page shows a warning until then. Both warnings link to the API's **Reporter Settings**.

* A Kafka Service shows **Connection metrics are disabled** until both analytics and reporter metrics are on. Either one alone records nothing.
* A Message API shows **Runtime logs are disabled** until analytics is on and it captures at least one mode, the entrypoint or the endpoint, and at least one phase, the request or the response. A mode without a phase records nothing, and so does a phase without a mode.

<figure><img src="../../.gitbook/assets/esm-observability-metrics-disabled.png" alt="The Overview page of a Kafka Service showing the Connection metrics are disabled warning, which links to Reporter Settings"><figcaption><p>A Kafka Service that reports nothing says so on its own page</p></figcaption></figure>
