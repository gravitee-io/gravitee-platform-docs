---
hidden: false
noIndex: false
description: >-
  Open a Message API row from the logs and read the request that opened the
  stream, the two legs the gateway recorded, and the messages it carried.
---

# Inspect a Message API request

A Message API row opens on the request that opened the stream, what the gateway exchanged on each leg, and the messages that flowed afterwards. A Kafka row opens on a different panel. See [Diagnose a failed Kafka connection](diagnose-a-failed-kafka-connection.md).

## Open a request

1. From the Gamma console sidebar, select **Event Stream Management**.
2. Open **Observability**.
3. Click **Logs**.
4. Click a row whose **API Type** reads **Message API**.

## Read the sections

<table>
    <thead>
        <tr>
            <th width="210">Section</th>
            <th>What it shows</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Overview</strong></td>
            <td>The API, its type, the entrypoint, the plan, the application, and the transaction, request, and client ids.</td>
        </tr>
        <tr>
            <td><strong>Connection Logs</strong></td>
            <td>The four legs of the exchange, each with its headers and body.</td>
        </tr>
        <tr>
            <td><strong>Messages</strong></td>
            <td>The messages the connection carried.</td>
        </tr>
        <tr>
            <td><strong>Raw JSON</strong></td>
            <td>The stored record behind the panel.</td>
        </tr>
    </tbody>
</table>

## Read the four legs

**Connection Logs** shows the legs the gateway recorded, in the order it handled them: **Entrypoint Request**, what the client sent the gateway; **Endpoint Request**, what the gateway sent the broker; **Endpoint Response**, how the broker answered; **Entrypoint Response**, how the gateway answered the client. Each carries its method or status, its headers, and its body.

A leg the API doesn't capture is left out. When none was captured, the section reads **No connection log details captured**.

Which legs appear follows [Reporter Settings](configure-reporter-settings.md): the entrypoint legs need the **Entrypoint** logging mode, the endpoint legs need **Endpoint**, and each leg needs the matching phase, **Request** or **Response**.

## Read the messages

**Messages** lists one card per message, a page at a time. **Load more** fetches the next page.

Each card carries the time, the operation, either **PUBLISH** or **SUBSCRIBE**, and the correlation id when there is one, then the payload as the entrypoint saw it and as the endpoint saw it, each labelled with the connector that handled it.

## Why a section is empty

The connection is listed as soon as the switch on the API's **Settings** card is on. The bodies, headers, and messages need a **Logging mode**, a **Logging phase**, and the matching **Content data** options on top of it. Until then the row opens with **Connection Logs** and **Messages** empty, and the API's **Overview** page shows **Message content is not recorded**.

Message capture also follows the API's sampling strategy, so a busy stream stores a fraction of its messages by design.

## Verification

To verify a request and its messages reach the panel, follow these steps:

1. Open a Message API.
2. Confirm its **Overview** page shows no reporting warning.
3. Publish a message through the API's entrypoint.
4. Open **Logs** and set the time range to cover the request.
5. Open the new row.
6. Confirm **Connection Logs** shows the entrypoint request, and **Messages** lists the message.
