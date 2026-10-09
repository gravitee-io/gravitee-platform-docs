---
description: Native Kafka API connection logs record every client connection lifecycle event in API Management 4.13. Learn the architecture behind them.
---

# Native Kafka API Connection Logs: Concepts and Architecture

## Overview

Native Kafka API connection logs record client connection lifecycle events. You can list, filter, and inspect connection logs from the **Logs** menu on a Native Kafka API. A five-card summary shows at-a-glance counts by connection status. A detail page displays a single log entry, including client identifiers, server metadata, and error details when applicable.

## Key Concepts

### Log entries and connections

Each lifecycle event of a connection is its own log entry. Depending on the events the API reports, a connection writes an entry when it opens, when it fails, and when it closes cleanly. A connection can therefore have several entries:

* The entries of one connection share the same **Transaction ID**, which is the connection ID.
* The **Request ID** is unique to each entry. It's made of the connection ID, a sequence number, and the status, for example `<connection-id>:2:disconnected`.

### Connection Lifecycle Statuses

Each connection log entry is tagged with one of the following five statuses:

| Status | API Value | Meaning | Trigger |
|:-------|:----------|:--------|:--------|
| **Connected** | `CONNECTED` | The connection is established. | The client completed the handshake and authentication. |
| **Disconnected** | `DISCONNECTED` | The connection closed cleanly. The entry carries the connection duration and never carries an error. | The connection ended without a failure. Reported only when the API selects the Disconnected event. See [Which events are reported](#which-events-are-reported). |
| **Interrupted** | `SESSION_ERROR` | The connection was cut by a failure during the session. | A Kafka request failed while it was processed during the session. |
| **Failed** | `CONNECTION_ERROR` | The connection couldn't be established on the client side or on the broker side. | Client authentication failure, a rejection during the Entrypoint Connect phase, no endpoint found for the API, or the Gateway failing to connect or authenticate to the broker. |
| **Unknown** | `INTERNAL_ERROR` | An unexpected Gateway-side error. | Any failure that doesn't match the other statuses. |

The **Status** column is the label shown in the **Management Console**. The **API Value** is the raw `connectionStatus` enum returned by the Management API (mAPI). Each status is paired with a fixed color palette and icon used consistently in summary cards, table pills, and detail page badges.

Disconnected entries and error entries carry the connection duration. They also carry the number of Kafka requests the connection served, in total and per Kafka request type, when the connection served at least one request. The Management Console doesn't display these request counts. They're stored in the reporter as `long_native-kafka_request-count` and `long_native-kafka_requests_<REQUEST_TYPE>`, for example `long_native-kafka_requests_PRODUCE`.

### Which events are reported

The `analytics.connectionEvents` field of the API definition selects the lifecycle events the Gateway reports. It accepts `CONNECTED`, `DISCONNECTED`, and `ERROR`. `ERROR` covers the Interrupted, Failed, and Unknown statuses.

* When the field is absent or empty, the Gateway reports `CONNECTED` and `ERROR`. This is the default for every API, including new ones.
* `DISCONNECTED` is opt-in. Selecting it adds a closing entry to every connection, so it increases the volume of connection logs.
* If an API selects `DISCONNECTED` without `ERROR`, a connection that fails writes no closing entry.

The Management Console has no setting for `analytics.connectionEvents`. Set it through the Management API. Until you do, the **Disconnected** summary card stays at zero.

### Connection Metrics Reporting

The **Enable connection metrics reporting** toggle on the **Reporter Settings** page controls whether the API Gateway writes connection-lifecycle records to the configured reporter, such as Elasticsearch or OpenSearch. When disabled, no new connection logs are produced—the **Logs** page displays a "Reporting is disabled" banner and the summary widget is hidden. Historical data already in the reporter store is unaffected by the toggle. The toggle defaults to enabled when the API is created without an explicit `analytics.reporterMetricsEnabled` value.

### Permissions Model

Two distinct permissions govern access to connection logs:

| Permission | Scope | Grants Access To |
|:-----------|:------|:-----------------|
| `api-native_log-r` | Summary visibility. | **Logs** menu, list view, and summary widget. |
| `api-native_analytics-r` | Per-connection inspection. | Detail page with client identifiers and error details. |

If you only have the `api-native_log-r` permission, you can see the list and summary, but you cannot drill into individual connections—the per-row view icon is hidden.

## Prerequisites

To view connection logs, ensure you meet the following:

* A Native Kafka API deployed on the API Gateway.
* An Elasticsearch or OpenSearch reporter configured.
* A user role with the `api-native_log-r` permission to view logs.
* A user role with the `api-native_analytics-r` permission to view connection details.