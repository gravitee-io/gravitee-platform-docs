# Partial Updates for V4 HTTP Proxy APIs and Plans

## Overview

The Management API supports optimistic concurrency control for plan updates through ETag and Last-Modified headers. When retrieving a plan, the API returns version metadata that clients can use to detect and prevent conflicting concurrent modifications. This capability enables safe automation of plan configuration changes in multi-writer environments.

## Key Concepts

### ETag Header

The `ETag` header identifies a specific version of a plan resource. The value is an opaque quoted string derived from the plan's last-updated timestamp with millisecond precision. Clients should treat the ETag as a token—read it from the response and send it back verbatim in subsequent conditional requests. Do not parse, construct, or modify ETag values.

### Last-Modified Header

The `Last-Modified` header provides the plan's last-updated timestamp in RFC 7231 HTTP-date format (one-second resolution). This header is informational only. Because it loses millisecond precision from the underlying timestamp, clients must use the `ETag` header—not `Last-Modified`—for conditional update requests.

### Optimistic Concurrency Control

Optimistic concurrency control prevents lost updates when multiple clients modify the same plan. A client retrieves a plan and receives an ETag. When updating the plan, the client sends the ETag in an `If-Match` header. The server accepts the update only if the ETag matches the current version; if another writer has modified the plan in the interim, the server returns `412 Precondition Failed` and persists nothing. The client must re-fetch the plan to obtain the current ETag before retrying.

## Prerequisites

- Access to the Management API v2 (`/management/v2/environments/{envId}/apis/{apiId}/plans/{planId}`)
- A plan with a non-null `updatedAt` timestamp (plans without this field will not return ETag or Last-Modified headers)

## Managing Plan Updates

### Conditional Header Emission

The `GET /management/v2/environments/{envId}/apis/{apiId}/plans/{planId}` endpoint emits `ETag` and `Last-Modified` headers only when the plan's `updatedAt` field is non-null. Plans without an `updatedAt` timestamp return neither header, and conditional updates are not supported for those resources.

The header emission logic supports v2 plans, v4 plans, and native v4 plans. If the server encounters an unknown plan entity type, it logs a warning and omits both headers:

```
Cannot resolve updatedAt for unknown plan entity type: {className}
```

### Precision and Format Constraints

The `ETag` header preserves millisecond precision from the plan's `updatedAt` timestamp, making it suitable for detecting concurrent modifications. The `Last-Modified` header uses RFC 7231 HTTP-date format, which provides only one-second resolution and loses millisecond precision. Clients must use the `ETag` value—not `Last-Modified`—in `If-Match` requests to ensure accurate concurrency detection.

### Compatibility with Existing Operations

The ETag mechanism uses the same convention as existing PUT operations and lifecycle actions (`_start`, `_stop`). Clients already using conditional updates with PUT can apply the same pattern to PATCH operations without modification.
