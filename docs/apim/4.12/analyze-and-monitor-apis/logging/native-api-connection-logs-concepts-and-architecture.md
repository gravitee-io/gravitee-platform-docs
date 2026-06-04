# Native API Connection Logs: Concepts and Architecture

## Overview

Native API connection logs record every client connection lifecycle event for Kafka-protocol APIs. Operators can list, filter, and inspect connection logs from the Logs menu on a Native API, with a four-card summary showing at-a-glance counts by connection status. A detail page displays the full lifecycle entry for a single connection, including client identifiers, server metadata, and error details when applicable.

## Key Concepts

### Connection Lifecycle Statuses

Each connection log entry is tagged with one of four lifecycle outcomes:

| Status | API Value | Meaning | Trigger |
|:-------|:----------|:--------|:--------|
| **Connected** | `CONNECTED` | Handshake completed; session is active or ended cleanly | Healthy connection established |
| **Disconnected** | `SESSION_ERROR` | Connection terminated by transport-level error after successful handshake | Policy failure during interact flow (e.g., broken pipe mid-session) |
| **Failed** | `CONNECTION_ERROR` | Handshake or authentication failed | `InterruptConnectionException` during initialize or entrypointConnect (e.g., SASL handshake failure, invalid credentials) |
| **Unknown** | `INTERNAL_ERROR` | Gateway-side error, not attributable to client or transport | Backend broker becomes unreachable mid-session |

The **Status** column is the label shown in the console UI; the **API Value** is the raw `connectionStatus` enum returned by the Management API. Each status is paired with a fixed color palette and icon used consistently in summary cards, table pills, and detail page badges.

### Connection Metrics Reporting

The **Enable connection metrics reporting** toggle on the Reporter Settings page controls whether the gateway writes connection-lifecycle records to the configured reporter (Elasticsearch or OpenSearch). When disabled, no new connection logs are produced — the Logs page displays a "Reporting is disabled" banner and the summary widget is hidden. Historical data already in the reporter store is unaffected by the toggle. The toggle defaults to enabled when the API is created without an explicit `analytics.reporterMetricsEnabled` value.

### Permissions Model

Two distinct permissions govern access to connection logs:

| Permission | Scope | Grants Access To |
|:-----------|:------|:-----------------|
| `api-native_log-r` | Summary visibility | Logs menu, list view, summary widget |
| `api-native_analytics-r` | Per-connection inspection | Detail page with client identifiers and error details |

Users with only `api-native_log-r` can see the list and summary but cannot drill into individual connections — the per-row view icon is hidden.

## Prerequisites

- Native (Kafka-protocol) API deployed on the gateway
- Elasticsearch or OpenSearch reporter configured
- User role with `api-native_log-r` permission to view logs
- User role with `api-native_analytics-r` permission to view connection details
