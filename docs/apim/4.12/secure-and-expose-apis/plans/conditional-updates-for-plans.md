# Conditional Updates and Plan Management

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

The `GET /management/v2/environments/{envId}/apis/{apiId}/plans/{planId}` endpoint emits `ETag` and `Last-Modified` headers only when the plan's `updatedAt` field is non-null. Plans without an `updatedAt` timestamp return neither header, and conditional updates are not supported for those resources. If a resource has `null` `updatedAt`, any `If-Match` header (except wildcard `*`) is rejected with `412 Precondition Failed`.

The header emission logic supports v2 plans, v4 plans, and native v4 plans. If the server encounters an unknown plan entity type, it logs a warning and omits both headers:

```
Cannot resolve updatedAt for unknown plan entity type: {className}
```

### Precision and Format Constraints

The `ETag` header preserves millisecond precision from the plan's `updatedAt` timestamp, making it suitable for detecting concurrent modifications. The `Last-Modified` header uses RFC 7231 HTTP-date format, which provides only one-second resolution and loses millisecond precision. Clients must use the `ETag` value—not `Last-Modified`—in `If-Match` requests to ensure accurate concurrency detection.

### Compatibility with Existing Operations

The ETag mechanism uses the same convention as existing PUT operations and lifecycle actions (`_start`, `_stop`). Clients already using conditional updates with PUT can apply the same pattern to PATCH operations without modification.

### Creating Conditional Update Workflows

To implement conditional updates, retrieve the plan's current ETag, then include it in the `If-Match` header when performing mutating operations. The following example demonstrates the round-trip flow:

```http
# 1. Retrieve the plan and its ETag
GET /management/v2/environments/DEFAULT/apis/{apiId}/plans/{planId}
→ 200 OK
→ ETag: "1705314645123"
→ Last-Modified: Mon, 15 Jan 2024 10:30:45 GMT
```

```http
# 2. Update the plan with the retrieved ETag
PATCH /management/v2/environments/DEFAULT/apis/{apiId}/plans/{planId}
If-Match: "1705314645123"
Content-Type: application/merge-patch+json

{"description": "Updated description"}

→ 200 OK
→ ETag: "1705314678456"   # New ETag after successful update
```

If another client modifies the plan between steps 1 and 2, the server rejects the update:

```http
PATCH /management/v2/environments/DEFAULT/apis/{apiId}/plans/{planId}
If-Match: "1705314645123"   # Stale ETag
Content-Type: application/merge-patch+json

{"description": "Updated description"}

→ 412 Precondition Failed
```

A `412` response does not include a fresh ETag. The client must re-fetch the plan to obtain the current version before retrying.

Omitting the `If-Match` header (or sending `If-Match: *`) skips the concurrency check entirely, implementing last-write-wins behavior identical to PUT operations.

### Response Header Reference

| Header | Description | Example |
|:-------|:------------|:--------|
| **ETag** | Opaque quoted string identifying the plan version. Derived from the plan's `updatedAt` timestamp as epoch milliseconds. Use this value in `If-Match` headers for conditional requests. | `"1705314645123"` |
| **Last-Modified** | Plan's last-updated timestamp in RFC 7231 HTTP-date format (one-second resolution). Informational only; do not use for conditional requests due to precision loss. | `Mon, 15 Jan 2024 10:30:45 GMT` |

### Partial Plan Updates

To partially update a V4 HTTP Proxy API plan, send a PATCH request to `/management/v2/environments/{envId}/apis/{apiId}/plans/{planId}` with one of the supported content types. The request body format and headers follow the same rules as API PATCH operations.

**Query Parameters**:

| Parameter | Type    | Default | Description                                 |
| :-------- | :------ | :------ | :------------------------------------------ |
| `dryRun`  | Boolean | `false` | Preview the result without persisting       |

**Patchable Plan Fields**:

| Field              | Nullable | Description                                                                                                                                                                                                                                                |
| :----------------- | :------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`             | No       | Plan name                                                                                                                                                                                                                                                  |
| `description`      | Yes      | Plan description                                                                                                                                                                                                                                           |
| `security`         | No       | Security configuration; type is frozen, only `configuration` sub-fields are patchable; when patching `selectionRule` or `security` on a plan without an HTTP V4 definition (`planDefinitionHttpV4` is `null`), the operation is a no-op and does not throw an error |
| `validation`       | No       | Plan validation type (`AUTO`, `MANUAL`)                                                                                                                                                                                                                    |
| `selectionRule`    | Yes      | EL expression for plan selection; when patching `selectionRule` or `security` on a plan without an HTTP V4 definition (`planDefinitionHttpV4` is `null`), the operation is a no-op and does not throw an error                                             |
| `tags`             | Yes      | Plan tags                                                                                                                                                                                                                                                  |
| `excludedGroups`   | Yes      | Group IDs excluded from the plan                                                                                                                                                                                                                           |
| `characteristics`  | Yes      | Plan characteristics                                                                                                                                                                                                                                       |
| `commentRequired`  | No       | Whether subscription comments are required                                                                                                                                                                                                                 |
| `generalConditions`| Yes      | General conditions page reference                                                                                                                                                                                                                          |
| `flows`            | Yes      | Plan flows                                                                                                                                                                                                                                                 |

**Non-Patchable Plan Fields**:

| Field            | Reason                                                                   |
| :--------------- | :----------------------------------------------------------------------- |
| `status`         | Use plan lifecycle endpoints to change plan status                       |
| `id`             | Field is not patchable                                                   |
| `createdAt`      | Field is not patchable                                                   |
| `security.type`  | Type is frozen; only `security.configuration` is patchable               |

**Response**:

* `200 OK` — Returns the patched plan with `ETag` and `Last-Modified` headers
* `400 Bad Request` — Validation failure, disallowed field, or unsupported plan type
* `404 Not Found` — Plan not found or does not belong to specified API
* `412 Precondition Failed` — `If-Match` header mismatch

**Security Type Immutability**:

The `security.type` field is frozen and cannot be changed via PATCH. When patching `security`, the existing type is preserved and only `security.configuration` is updated.

**Excluded Groups Handling**:

* Omitting `excludedGroups` preserves existing excluded groups.
* Setting `excludedGroups` to `null` (Merge Patch) or using JSON Patch `remove` on `/excludedGroups` clears excluded groups.
* Unknown group IDs are rejected with `GroupNotFoundException`.
* Excluded groups are validated only when the patch targets the `excludedGroups` field. Patches that do not target `excludedGroups` do not re-validate existing group IDs, allowing stale group references to persist.

**Flow Validation**:

Plan flows are validated using the flow validation domain service. Invalid selectors (e.g., `channel` selector on HTTP Proxy plan) trigger `ValidationDomainException` with `flowName` and `invalidSelectors` parameters.
