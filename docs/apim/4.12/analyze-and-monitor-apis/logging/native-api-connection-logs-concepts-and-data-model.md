# Native API Connection Logs: Concepts and Data Model

## Overview

Native API Connection Logs and Reporting provides visibility into connection lifecycle events for native Kafka APIs. Administrators can view connection attempts, track session errors, and analyze connection duration metrics through a dedicated logs interface. The feature introduces a separate reporting toggle for connection metrics, independent of event-metrics reporting.

## Key Concepts

### Connection Lifecycle Status

Each connection attempt is classified by its outcome. The system tracks four distinct states: successful connections, policy-driven interruptions, request-phase policy failures, and infrastructure errors. Connection duration is measured from establishment to close, with null values indicating interrupted connections without a close event.

| Status | Description | Trigger |
|:-------|:------------|:--------|
| CONNECTED | Healthy connection established | Normal operation |
| CONNECTION_ERROR | Policy-driven connection interruption | `InterruptConnectionException` at connection/entrypoint-connect phase |
| SESSION_ERROR | Request-phase policy error | Policy failure during request flow (wrapped in `KafkaException`) |
| INTERNAL_ERROR | Infrastructure failure | Backend unreachable (e.g., broker stopped mid-session) |

### Connection Metrics Reporting

Connection metrics are stored in Elasticsearch or OpenSearch as additional metric keys. The `reporterMetricsEnabled` flag controls whether connection events are indexed. When enabled, the system records client identifiers, broker identifiers, connection status, and connection duration for each connection attempt. This setting is independent of event-metrics reporting and defaults to enabled for new native APIs.

### Log Data Model

Each connection log entry captures temporal, routing, client, and error context:

* **Temporal fields**: timestamp, request ID, transaction ID
* **Routing fields**: API, plan, subscription, entrypoint, gateway
* **Client fields**: application ID, client identifier, remote address, Kafka-specific client and broker IDs
* **Error fields**: error key and error message (populated only for errored connection statuses)

## Prerequisites

Before viewing native API connection logs, ensure the following requirements are met:

* Native Kafka API deployed and running
* Elasticsearch or OpenSearch configured as the analytics repository
* User permission `api-native_log-r` to view connection logs
* User permission `api-native_analytics-r` to view individual log details

{% hint style="warning" %}
Logs outside the configured Elasticsearch retention window return 404. If application or plan name resolution fails, the logs table renders raw IDs without error notification. The `connectionDurationMs` field is null for logs without a close event (e.g., interrupted connections). When a broker stops mid-session, the system emits `INTERNAL_ERROR` on the next connection attempt.
{% endhint %}
