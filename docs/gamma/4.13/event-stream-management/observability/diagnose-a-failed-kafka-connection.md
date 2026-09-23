---
hidden: false
noIndex: false
description: Open a failed Kafka connection from the logs and read the verdict that names what broke, which hop it broke on, and what to do about it.
---

# Diagnose a failed Kafka connection

Opening a Kafka row on the **Logs** page of **Observability** leads with a verdict. One plain sentence says what happened, a badge says which hop it happened on, and an error the gateway recognizes also gets a next step.

<figure><img src="../../../.gitbook/assets/esm-observability-log-detail.png" alt="A failed Kafka connection detail opening on a Connection error verdict labelled Gateway and Broker, above the collapsed Client to Gateway, Gateway to Broker, Error, Service activity, and Raw record sections"><figcaption><p>A failed connection opens on the verdict rather than on raw fields</p></figcaption></figure>

## Open a connection

1. From the Gamma console sidebar, select **Event Stream Management**.
2. Open **Observability**.
3. Click **Logs**.
4. Click the row you want to inspect.

The detail opens beside the table, and you can step through neighboring rows without closing it.

## Read the verdict

The sentence at the top says what failed, and the badge next to it says where. The sentence never repeats the hop, so read the two together.

A connection that didn't fail gets a plain statement instead: that it was established, that the client disconnected, or that its status is unknown for the request.

A connection counts as failed when its status is **Connection error**, **Session error**, or **Internal error**, or when it carries an error key at all. A row that reads **Connected** and still carries an error key is a failure, and the verdict treats it as one.

## Read the sections

Below the verdict, the detail separates the two hops so you can see which side holds the evidence.

<table>
    <thead>
        <tr>
            <th width="200">Section</th>
            <th>What it holds</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>The client-to-gateway section</td>
            <td>What the Kafka client presented to the gateway, and how the gateway saw it.</td>
        </tr>
        <tr>
            <td>The gateway-to-broker section</td>
            <td>What the gateway did toward the broker on the other side.</td>
        </tr>
        <tr>
            <td><strong>Error</strong></td>
            <td>The error fields, badged with the error key, plus the message the gateway recorded. Shown only on a failed connection.</td>
        </tr>
        <tr>
            <td><strong>Service activity</strong></td>
            <td>What the Kafka Service was doing around the time of this connection.</td>
        </tr>
        <tr>
            <td><strong>Raw record</strong></td>
            <td>The stored record behind the view.</td>
        </tr>
    </tbody>
</table>

The table row and the detail word the hop differently. The row badge reads **Client ↔ Gateway** and **Gateway ↔ Broker**. The detail's two hop headings pair the same names with a one-way arrow instead, because each describes a single direction.

## What each error key means

An error the gateway recognizes gets a sentence and a next step. An error it doesn't recognize is shown with its key turned into readable words, and no next step.

### Client to gateway

These fail before the gateway ever reaches a broker, and the fix is on the client or the plan.

<table>
    <thead>
        <tr>
            <th width="290">Error key</th>
            <th width="330">What happened</th>
            <th>What to do</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>SASL_AUTHENTICATION_FAILED</code></td>
            <td>SASL authentication failed.</td>
            <td>Check the application's subscription credentials.</td>
        </tr>
        <tr>
            <td><code>UNSUPPORTED_SASL_MECHANISM</code></td>
            <td>The client requested an unsupported SASL mechanism.</td>
            <td>Align the client's security protocol and SASL mechanism with what the plan enables.</td>
        </tr>
        <tr>
            <td><code>ILLEGAL_SASL_STATE</code></td>
            <td>The SASL handshake reached an illegal state.</td>
            <td>Review the client's security configuration, because SASL frames were sent out of order.</td>
        </tr>
        <tr>
            <td><code>SECURITY_DISABLED</code></td>
            <td>The client attempted SASL but security is disabled.</td>
            <td>Use a keyless client, or a secured plan.</td>
        </tr>
    </tbody>
</table>

### Gateway to broker

These mean the gateway reached the broker and the broker refused, or couldn't answer.

<table>
    <thead>
        <tr>
            <th width="290">Error key</th>
            <th width="330">What happened</th>
            <th>What to do</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>BROKER_NOT_AVAILABLE</code></td>
            <td>The Kafka broker wasn't reachable.</td>
            <td>Check the cluster endpoint and broker health, and that the gateway can reach the bootstrap servers.</td>
        </tr>
        <tr>
            <td><code>UNKNOWN_TOPIC_OR_PARTITION</code></td>
            <td>The requested topic or partition was unknown.</td>
            <td>Check the topic mapping, and that the topic exists on the target cluster.</td>
        </tr>
        <tr>
            <td><code>TOPIC_AUTHORIZATION_FAILED</code></td>
            <td>Access to the topic wasn't authorized.</td>
            <td>Check the broker-side ACLs granting this principal access to the topic.</td>
        </tr>
        <tr>
            <td><code>GROUP_AUTHORIZATION_FAILED</code></td>
            <td>Access to the consumer group wasn't authorized.</td>
            <td>Check the broker-side ACLs granting this principal access to the consumer group.</td>
        </tr>
        <tr>
            <td><code>CLUSTER_AUTHORIZATION_FAILED</code></td>
            <td>Access to the cluster wasn't authorized.</td>
            <td>Check the broker-side cluster ACLs for this principal.</td>
        </tr>
        <tr>
            <td><code>COORDINATOR_NOT_AVAILABLE</code></td>
            <td>The group coordinator wasn't available.</td>
            <td>Check broker health, then retry.</td>
        </tr>
        <tr>
            <td><code>NOT_COORDINATOR</code></td>
            <td>The broker isn't the coordinator for this group.</td>
            <td>Transient. The client refreshes coordinator metadata and retries.</td>
        </tr>
        <tr>
            <td><code>COORDINATOR_LOAD_IN_PROGRESS</code></td>
            <td>The group coordinator is still loading.</td>
            <td>Transient. The client retries shortly.</td>
        </tr>
    </tbody>
</table>

### Consumer group and producer state

These are usually transient, and they resolve without intervention.

<table>
    <thead>
        <tr>
            <th width="290">Error key</th>
            <th width="330">What happened</th>
            <th>What to do</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>REBALANCE_IN_PROGRESS</code></td>
            <td>The consumer group is redistributing its partitions.</td>
            <td>Transient. It resolves once the group settles.</td>
        </tr>
        <tr>
            <td><code>ILLEGAL_GENERATION</code></td>
            <td>The consumer sent an illegal generation id.</td>
            <td>Transient. The consumer rejoins with a fresh generation.</td>
        </tr>
        <tr>
            <td><code>MEMBER_ID_REQUIRED</code></td>
            <td>The consumer must rejoin the group with a member id.</td>
            <td>Transient. The consumer rejoins with the assigned member id.</td>
        </tr>
        <tr>
            <td><code>INVALID_TXN_STATE</code></td>
            <td>The producer transaction was in an invalid state.</td>
            <td>Review the producer's transactional workflow.</td>
        </tr>
        <tr>
            <td><code>UNKNOWN_SERVER_ERROR</code></td>
            <td>An unexpected server error occurred.</td>
            <td>Inspect the gateway logs around this request id.</td>
        </tr>
    </tbody>
</table>

## Verification

To verify a diagnosis points where you expect, follow these steps:

1. Connect a Kafka client with an incorrect password to a Kafka Service on a secured plan.
2. Open **Observability**, then click **Logs**.
3. Open the new row.
4. Confirm the verdict reads that SASL authentication failed, and that the badge places the failure between the client and the gateway.
