# Partial Updates for V4 HTTP Proxy APIs and Plans + Partial Updates for V4 HTTP Proxy APIs

## Overview

V4 HTTP Proxy APIs and their plans support partial updates via PATCH endpoints, allowing you to modify individual fields without sending the entire resource representation. Both endpoints accept JSON Merge Patch (RFC 7396) and JSON Patch (RFC 6902) formats, and support optimistic concurrency control via ETag headers to detect concurrent modifications. Before this capability, plans could only be updated via PUT, which required sending the entire plan representation, and there was no concurrency control on plan updates.

## Key Concepts

### JSON Merge Patch

Send a partial object containing only the fields you want to change. Omitted fields remain untouched. Setting a field to `null` clears it (for nullable fields). This is the simpler format for most updates.

**Content-Type:** `application/merge-patch+json` or `application/json` (both are treated as JSON Merge Patch)

**Example:**

```json
{
  "description": "Updated description",
  "tags": ["production", "public"]
}
```

### JSON Patch

Send an array of operations (`add`, `remove`, `replace`, `move`, `copy`, `test`) with RFC 6901 JSON Pointer paths. Use this format for fine-grained edits, such as changing a single array element.

**Content-Type:** `application/json-patch+json`

**Example:**

```json
[
  {"op": "replace", "path": "/description", "value": "Updated description"},
  {"op": "add", "path": "/tags/-", "value": "public"}
]
```

**Limit:** JSON Patch requests are limited to 200 operations per request. Requests exceeding this limit are rejected with 400: `"JSON Patch request exceeds maximum of 200 operations"`.

### Optimistic Concurrency Control

The `GET` endpoints for APIs and plans return `ETag` and `Last-Modified` headers derived from the resource's `updatedAt` field. If `updatedAt` is `null`, both headers are omitted from the response. The ETag value is the `updatedAt` timestamp expressed as epoch milliseconds (e.g., `"1705314645123"`). Treat the ETag as an opaque token — don't parse or construct it; read it from the response and send it back verbatim. The ETag uses the same convention as the existing PUT and `_start`/`_stop` operations.

| Header | Description |
|:-------|:------------|
| **ETag** | Entity tag identifying the resource version (epoch milliseconds, quoted per RFC 7232). Example: `"1705314645123"` |
| **Last-Modified** | Resource's last-updated timestamp (RFC 7231 HTTP-date, one-second resolution). Informational only; use `ETag` for `If-Match` requests. Example: `"Mon, 15 Jan 2024 10:30:45 GMT"` |

Use the `ETag` value in an `If-Match` header on subsequent PATCH requests to detect concurrent modifications. If the resource was modified since you read the ETag, the request is rejected with 412 Precondition Failed. The following `If-Match` values are accepted:

| `If-Match` Value | Behavior |
|:-----------------|:---------|
| Absent | Proceed without precondition check (last-write-wins). |
| `*` | Proceed (wildcard matches any tag). |
| Quoted ETag matching resource's `updatedAt` | Proceed. |
| Weak validator `W/"<etag>"` matching resource's `updatedAt` | Proceed (weak validators are accepted). |
| ETag with `-gzip` suffix matching resource's `updatedAt` | Proceed (suffix is stripped during validation). |
| Malformed (not a valid entity-tag) | Reject with 412. |
| Empty tag set (e.g., `-gzip` only) | Reject with 412. |
| ETag not matching resource's `updatedAt` | Reject with 412. |
| Present when resource's `updatedAt` is `null` | Reject with 412 (unless `*`). |

**ETag Round-Trip Example:**

```http
# 1. Read the current ETag
GET /management/v2/environments/DEFAULT/apis/{apiId}
→ ETag: "<etag-a>"

# 2. Conditional PATCH with that ETag
PATCH /management/v2/environments/DEFAULT/apis/{apiId}
If-Match: "<etag-a>"
Content-Type: application/merge-patch+json

{"description": "New description"}

→ 200 OK
→ ETag: "<etag-b>"   # new ETag after the update

# If another writer changed the API between steps 1 and 2:
→ 412 Precondition Failed   # re-GET and retry with the new ETag
```

Omitting `If-Match` (or sending `If-Match: *`) skips the concurrency check (last-write-wins). A 412 response does not carry a fresh ETag; you must re-GET the resource to read the current version before retrying.

### Dry Run

Set the `dryRun=true` query parameter to validate the patch without persisting changes. The response shows the would-be result, but a subsequent GET still returns the pre-patch state. The `If-Match` precondition is still enforced on a dry run. Dry run still rejects disallowed patches (e.g., targeting `status` on plans) and malformed patch bodies.

**Dry-Run Caveats:**

- Flow IDs in the response are `null` because no IDs are assigned until the resource is persisted. Flow IDs are server-generated and returned in real PATCH responses. Read flow IDs from a real PATCH response or a GET, never from a dry-run preview.
- Encrypted properties remain encrypted in the response, with `encrypted: true` and ciphertext in the `value` field.

## Prerequisites

- The API must be a **V4 HTTP Proxy API**. PATCH is not supported for V2 APIs or V4 Message APIs.
- For plan PATCH, the plan must belong to the specified API. If a plan has `referenceType` = `API_PRODUCT` and `referenceId` ≠ `apiId`, it is rejected with 404.
- To use optimistic concurrency control with `If-Match` (other than `*`), the resource must have a non-null `updatedAt` timestamp. Resources without an `updatedAt` value can still be patched, but `If-Match` preconditions (other than `*`) will fail with 412.
- Any `Content-Type` other than `application/json`, `application/merge-patch+json`, or `application/json-patch+json` returns 415 Unsupported Media Type.

## Partial Plan Updates

To partially update a V4 HTTP Proxy API plan, send a PATCH request to `/management/v2/environments/{envId}/apis/{apiId}/plans/{planId}`. The request body format is determined by the `Content-Type` header:

* `application/merge-patch+json` or `application/json` for JSON Merge Patch
* `application/json-patch+json` for JSON Patch

Optionally include an `If-Match` header with the plan's current ETag to enforce optimistic concurrency control. Set `dryRun=true` as a query parameter to preview the result without persisting changes.

### Patchable fields

The following fields can be modified via PATCH:

| Field | Type | Nullable | Description |
|:------|:-----|:---------|:------------|
| `name` | string | No | Plan name. Cannot be blank. |
| `description` | string | Yes | Plan description. |
| `security` | object | No | Security configuration. Only the `configuration` sub-field is patchable; `type` is frozen. Attempts to patch `security.type` are silently ignored. |
| `validation` | enum | No | Plan validation type (`AUTO`, `MANUAL`). |
| `selectionRule` | string | Yes | Selection rule expression. |
| `tags` | array[string] | Yes | Plan tags. |
| `excludedGroups` | array[string] | Yes | Excluded group IDs. All group IDs are validated against the environment's group registry. |
| `characteristics` | array[string] | Yes | Plan characteristics. |
| `commentRequired` | boolean | No | Whether subscription comments are required. |
| `generalConditions` | string | Yes | General conditions page ID. |
| `flows` | array[Flow] | Yes | Plan flows. |

### Non-patchable fields

The following fields cannot be modified via PATCH:

* `status` — Use dedicated plan lifecycle endpoints (`_close`, `_publish`, `_deprecate`) to change plan status.
* All other fields not in the allow-list above.

### Response

**200 OK:** Returns the patched plan with updated `ETag` and `Last-Modified` headers.

### Error responses

| Status | Condition |
|:-------|:----------|
| 400 | Invalid patch request — targeting `status` or any non-allow-listed field, malformed patch body, plan is not a V4 HTTP Proxy plan, validation failure (e.g., blank `name`, unknown group IDs, invalid flow selectors), or JSON Patch request exceeds 200 operations. |
| 404 | No plan with the given identifier exists for this API (including a plan that belongs to a different API or has `referenceType` = `API_PRODUCT` with `referenceId` ≠ `apiId`). |
| 412 | The `If-Match` precondition failed — the plan was modified since the supplied ETag was read, or the ETag is malformed. |
| 415 | Unsupported media type. The request body must be sent with `application/json`, `application/merge-patch+json`, or `application/json-patch+json`. |

### Behavioral notes

{% hint style="info" %}
**Security type immutability:** The `security.type` field is frozen and cannot be changed via PATCH. Attempts to patch `security.type` are silently ignored (not rejected); only `security.configuration` is mutable.
{% endhint %}

* **Flow selector discriminator:** Flow selectors must use uppercase discriminator values (e.g., `"HTTP"`, not `"http"`). Lowercase or unknown discriminators are rejected with 400. The `CHANNEL` selector type is accepted in flow discriminators but rejected by the flow validator for HTTP Proxy plans.
* **Excluded groups validation:** When `excludedGroups` is patched, all group IDs are validated against the environment's group registry. Unknown group IDs cause the request to fail with 400. However, if `excludedGroups` is not targeted by the patch, stale group IDs in the existing plan are not re-validated.
* **Flow validation:** Flows are validated using `FlowValidationDomainService.validateAndSanitizeHttpV4`. Path parameters in flows are validated against API-level flows.
* **Flow sanitization:** Policy configurations in flows are sanitized by `PolicyValidationDomainService`. The sanitized configuration is returned in the response and persisted, which may differ from the input.
* **Backward compatibility:** Plans could only be updated via PUT before, which required sending the entire plan representation. The PATCH endpoint is additive and does not affect existing clients. Plans without an `updatedAt` value can still be patched, but `If-Match` preconditions (other than `*`) will fail with 412.

## Partial API Updates

To partially update a V4 HTTP Proxy API, send a PATCH request to `/management/v2/environments/{envId}/apis/{apiId}`. The request body format is determined by the `Content-Type` header: `application/merge-patch+json` or `application/json` for JSON Merge Patch, or `application/json-patch+json` for JSON Patch. Optionally include an `If-Match` header with the API's current ETag to enforce optimistic concurrency control. Set `dryRun=true` to preview the result without persisting changes.

### Patchable fields

The following fields can be modified via PATCH:

| Field | Type | Nullable | Description |
|:------|:-----|:---------|:------------|
| `name` | string | No | API name. Cannot be blank. |
| `apiVersion` | string | Yes | API version string. |
| `description` | string | Yes | API description. |
| `tags` | array[string] | Yes | API tags. |
| `listeners` | array[Listener] | Yes | Listener configurations (HTTP, TCP, Subscription, Kafka). Empty arrays are accepted. |
| `endpointGroups` | array[EndpointGroup] | Yes | Endpoint group configurations. |
| `analytics` | object | Yes | Analytics configuration. |
| `flowExecution` | object | Yes | Flow execution settings. |
| `flows` | array[Flow] | Yes | API-level flows. |
| `plans` | array[Plan] | Yes | Embedded plan definitions. |
| `responseTemplates` | map[string, ResponseTemplate] | Yes | Response templates by key. |
| `groups` | array[string] | Yes | Group IDs. |
| `visibility` | enum | No | API visibility (`PUBLIC`, `PRIVATE`). |
| `lifecycleState` | enum | No | Lifecycle state (`CREATED`, `PUBLISHED`, `UNPUBLISHED`, `DEPRECATED`, `ARCHIVED`). |
| `disableMembershipNotifications` | boolean | No | Whether membership notifications are disabled. |
| `background` | string | Yes | Background image URL. |
| `picture` | string | Yes | Picture URL. |
| `categories` | array[string] | Yes | Category IDs. |
| `labels` | array[string] | Yes | Labels. |
| `resources` | array[Resource] | Yes | Resource configurations. |
| `properties` | array[Property] | Yes | API properties. Send `{"properties": null}` to clear all properties. |
| `services` | object | Yes | Service configurations (e.g., health check, dynamic routing). |
| `metadata` | array[Metadata] | Yes | Metadata entries. |

### Non-patchable fields

The following fields are read-only or managed by lifecycle endpoints and cannot be modified via PATCH:
- `id`
- `crossId`
- `definitionVersion`
- `type`
- `state`
- `createdAt`
- `updatedAt`
- `deployedAt`
- `definitionContext`

### Response

A successful PATCH request returns a `200 OK` response with the patched API. The response includes updated `ETag` and `Last-Modified` headers. Flow IDs are assigned and returned in the response, except on dry runs where they are `null`. Encrypted properties remain encrypted in the response.

### Error responses

See [Error responses](#error-responses) above for details.
### Behavioral notes

See [Behavioral notes](#behavioral-notes) above for details.
