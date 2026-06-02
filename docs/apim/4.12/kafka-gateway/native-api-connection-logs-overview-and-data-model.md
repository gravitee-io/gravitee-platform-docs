# Native API Connection Logs: Overview and Data Model

## Overview

Native API Connection Logs & Reporting provides visibility into connection-level events for native Kafka APIs. Administrators can view connection attempts, track connection status, analyze connection duration, and troubleshoot errors through a dedicated logs interface. Connection metrics are reported to Elasticsearch or OpenSearch when enabled in the API's analytics configuration.

## Key Concepts

### Connection Metrics

Connection metrics capture lifecycle events for native Kafka API connections. Each log entry records the timestamp, client identity, connection status, duration, and error details when applicable. Metrics are stored in Elasticsearch or OpenSearch and are queryable through the Management Console and Management API.

| Field | Description |
|:------|:------------|
| Timestamp | Connection event time |
| Application ID | Consuming application identifier |
| Plan ID | Subscription plan identifier |
| Subscription ID | Active subscription identifier |
| Client Identifier | Kafka client identifier |
| Client ID | Kafka client ID |
| Connection Status | Lifecycle status (CONNECTED, CONNECTION_ERROR, SESSION_ERROR, INTERNAL_ERROR) |
| Connection Duration | Duration in milliseconds (available only on connection close) |
| Error Key | Error classification key (when status is not CONNECTED) |
| Error Message | Detailed error description (when status is not CONNECTED) |

### Connection Status

Connection status reflects the lifecycle state of a native Kafka connection. Four statuses are tracked:

| Status | Label | Trigger | Description |
|:-------|:------|:--------|:------------|
| CONNECTED | Connected | Successful connection open | Healthy connection established |
| CONNECTION_ERROR | Failed | Connection setup failure | Connection initialization or entrypoint-connect failed |
| SESSION_ERROR | Disconnected | Policy failure during request flow | Post-connection session error |
| INTERNAL_ERROR | Unknown | Backend unreachable | Infrastructure failure (e.g., broker stopped mid-session) |

### Reporter Metrics Toggle

The **Enable connection metrics reporting** toggle controls whether connection-level metrics are sent to Elasticsearch or OpenSearch. This setting is independent of the **Enable event-metrics reporting** toggle, which controls message-level metrics. Both can be enabled simultaneously or separately. When analytics configuration is absent, connection metrics reporting defaults to enabled.


## Prerequisites

Before viewing or configuring native API connection logs, ensure the following requirements are met:

* Native Kafka API (API type must be `NATIVE`)
* Elasticsearch or OpenSearch repository configured for metrics storage
* User permission `api-native_log-r` to view connection logs
* User permission `api-definition-u` to modify reporter settings
* Time range (`from` and `to` parameters) required for all log queries
