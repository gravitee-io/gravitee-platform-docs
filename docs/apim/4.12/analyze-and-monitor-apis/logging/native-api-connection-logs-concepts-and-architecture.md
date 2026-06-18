---
description: Native Kafka API connection logs record every client connection lifecycle event.
hidden: true
noIndex: true
---

# Native Kafka API Connection Logs: Concepts and Architecture

## Overview

Native Kafka API connection logs record every client connection lifecycle event. You can list, filter, and inspect connection logs from the **Logs** menu on a Native Kafka API. A four-card summary shows at-a-glance counts by connection status. A detail page displays the full lifecycle entry for a single connection, including client identifiers, server metadata, and error details when applicable.

## Key Concepts

### Connection Lifecycle Statuses

Each connection log entry is tagged with one of the following four lifecycle outcomes:

| Status | API Value | Meaning | Trigger |
|:-------|:----------|:--------|:--------|
| **Connected** | `CONNECTED` | Handshake completed; session is active or ended cleanly. | Healthy connection established. |
| **Disconnected** | `SESSION_ERROR` | Connection terminated by transport-level error after successful handshake. | Policy failure during interact flow, for example, a broken pipe mid-session. |
| **Failed** | `CONNECTION_ERROR` | Handshake or authentication failed. | `InterruptConnectionException` during initialize or entrypointConnect, such as a SASL handshake failure or invalid credentials. |
| **Unknown** | `INTERNAL_ERROR` | API Gateway-side error, not attributable to client or transport. | Backend broker becomes unreachable mid-session. |

The **Status** column is the label shown in the **Management Console**. The **API Value** is the raw `connectionStatus` enum returned by the Management API (mAPI). Each status is paired with a fixed color palette and icon used consistently in summary cards, table pills, and detail page badges.

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