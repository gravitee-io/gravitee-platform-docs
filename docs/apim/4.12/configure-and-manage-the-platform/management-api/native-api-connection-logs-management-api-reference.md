---
hidden: true
noIndex: true
---

# Native API Connection Logs Management API Reference

## Management API

The Management API v2 exposes three endpoints for programmatic access to native API connection logs:

| Endpoint | Method | Purpose |
|:---------|:-------|:--------|
| `/apis/{apiId}/logs/native` | GET | Search native API connection logs |
| `/apis/{apiId}/logs/native/{requestId}` | GET | Find a single native API connection log by request ID |
| `/apis/{apiId}/logs/native/summary` | GET | Retrieve connection status summary counts |

### Search Query Parameters

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `page` | number | Page number (must be ≥ 1) |
| `perPage` | number | Page size (must be ≥ 1) |
| `from` | number | Start timestamp (must be ≤ `to`) |
| `to` | number | End timestamp (must be ≥ `from`) |
| `applicationIds` | string | Comma-separated application IDs |
| `planIds` | string | Comma-separated plan IDs |
| `connectionStatuses` | string | Comma-separated connection statuses |

### Connection Log Response Schema

| Field | Type | Description |
|:------|:-----|:------------|
| `timestamp` | string | Connection lifecycle event time |
| `apiId` | string | API identifier |
| `requestId` | string | Unique request identifier |
| `transactionId` | string | Transaction identifier |
| `applicationId` | string | Application identifier |
| `planId` | string | Plan identifier |
| `clientIdentifier` | string | Free-form client identifier |
| `subscriptionId` | string | Subscription identifier |
| `entrypointId` | string | Entrypoint identifier |
| `gateway` | string | Gateway node identifier |
| `remoteAddress` | string | Client remote address |
| `localAddress` | string | Gateway local address |
| `host` | string | Host header value |
| `errorKey` | string | Error classification key |
| `errorMessage` | string | Human-readable error message |
| `connectionStatus` | string | `CONNECTED`, `CONNECTION_ERROR`, `SESSION_ERROR`, or `INTERNAL_ERROR` |
| `clientId` | string | Kafka client ID |
| `brokerId` | string | Broker node identifier |
| `connectionDurationMs` | number | Connection duration in milliseconds |

### Summary Response Schema

| Field | Type | Description |
|:------|:-----|:------------|
| `countByConnectionStatus` | object | Map of connection status to count |

### Query Validation Rules

Invalid query parameters are rejected with HTTP 400 and a descriptive error message:

| Rule | Response |
|:-----|:---------|
| `page` < 1 | HTTP 400 — `page must be >= 1` |
| `perPage` < 1 | HTTP 400 — `perPage must be >= 1` |
| `from` > `to` | HTTP 400 — `from must be <= to` |
| `from` or `to` missing | HTTP 400 |
