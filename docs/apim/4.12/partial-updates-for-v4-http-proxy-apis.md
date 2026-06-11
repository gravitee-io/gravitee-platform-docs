# Partial Updates for V4 HTTP Proxy APIs

## Overview

The PATCH endpoint enables partial updates to V4 HTTP Proxy APIs without requiring a full resource replacement. Use JSON Merge Patch (RFC 7396) for simple field updates or JSON Patch (RFC 6902) for fine-grained array and object modifications. This endpoint supports optimistic concurrency control via ETag headers (using the same convention as existing PUT and `_start`/`_stop` operations) and dry-run validation for pre-flight checks.

## Key Concepts

### JSON Patch

JSON Patch (RFC 6902) applies an ordered sequence of operations (`add`, `remove`, `replace`, `move`, `copy`, `test`) using JSON Pointer (RFC 6901) paths. Use this format for precise edits such as inserting a single flow or reordering endpoint groups. The endpoint accepts `application/json-patch+json` as the content type for JSON Patch operations.

**Example:**

```json
[
  {"op": "add", "path": "/labels/-", "value": "new-label"},
  {"op": "remove", "path": "/tags/0"}
]
```

### Optimistic Concurrency Control

The `If-Match` request header and `ETag` response header implement optimistic locking using the same convention as existing PUT and `_start`/`_stop` operations. Retrieve the current ETag from a GET response, include it in the `If-Match` header when patching, and receive a new ETag after a successful update. Treat the ETag as an opaque token—do not parse or construct it; read it from the response and send it back verbatim.

**Concurrency Control Behavior:**

| Condition | Behavior |
|:----------|:---------|
| `If-Match` header matches current ETag | Request proceeds |
| `If-Match` header is `*` (wildcard) | Request proceeds (skips validation) |
| `If-Match` header is omitted | Request proceeds (last-write-wins) |
| `If-Match` header mismatches | 412 Precondition Failed (no fresh ETag in response; re-GET required) |
| `updatedAt` is null | `If-Match` validation skipped entirely |

A 412 Precondition Failed response indicates the resource was modified by another client. The 412 response does not carry a fresh ETag, so the caller must re-GET to read the current version before retrying.

### Dry Run Validation

Set the `dryRun=true` query parameter to validate a patch without persisting changes. The response reflects the would-be result, including validator-sanitized values and plugin defaults. Flow `id` fields return `null` in dry-run responses because no database IDs are assigned. The `If-Match` precondition is still enforced on a dry run.

## Prerequisites

- API must be a V4 HTTP Proxy API (not V2, V4 Message, or Federated)
- User must have `API_DEFINITION[UPDATE]` or `API_GATEWAY_DEFINITION[UPDATE]` permission
- For conditional updates, retrieve the current ETag via GET before patching

## Creating Partial API Updates

Send a PATCH request to `/management/v2/environments/{envId}/apis/{apiId}` with one of the supported content types. Include the `If-Match` header with the current ETag to enforce concurrency control, send `If-Match: *` to skip validation, or omit the header to allow last-write-wins semantics. Set `dryRun=true` to preview the result without persisting changes.

**Request Headers:**

| Header | Required | Description |
|:-------|:---------|:------------|
| `Content-Type` | Yes | `application/merge-patch+json`, `application/json-patch+json`, or `application/json` (treated as merge patch) |
| `If-Match` | No | ETag value from a prior GET response (e.g., `"1234567890"`), or `*` to skip validation |

**Query Parameters:**

| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `dryRun` | boolean | `false` | Preview the result without persisting changes |

**Patchable Fields:**

```
name, description, apiVersion, visibility, labels, tags, lifecycleState, categories, groups,
analytics, failover, flowExecution, flows, services, resources, endpointGroups, listeners,
allowedInApiProducts, allowMultiJwtOauth2Subscriptions, disableMembershipNotifications,
properties, responseTemplates
```

**Blocked Fields:**

| Field | Reason |
|:------|:-------|
| `state` | Use `/_start` or `/_stop` endpoints to change runtime state |
| `definitionVersion` | Field is not patchable |
| `type` | Field is not patchable |

**Null Handling:**

Required fields (`name`, `apiVersion`, `visibility`, `lifecycleState`, `allowedInApiProducts`, `allowMultiJwtOauth2Subscriptions`, `disableMembershipNotifications`) reject `null` values with a 400 error. Optional fields accept `null` to clear the value. To clear all properties, send `{"properties": null}`. Omit a field entirely to leave it unchanged.

**Response:**

- **200 OK:** Returns the patched API with `ETag` and `Last-Modified` headers
- **400 Bad Request:** Validation failure, disallowed field, malformed patch, or out-of-bounds array index
- **403 Forbidden:** Missing required permission
- **404 Not Found:** API does not exist
- **412 Precondition Failed:** `If-Match` header validation failed (no fresh ETag in response; re-GET required)
- **415 Unsupported Media Type:** Invalid `Content-Type` header

**Example (Merge Patch):**

```bash
PATCH /management/v2/environments/DEFAULT/apis/my-api-id
Content-Type: application/merge-patch+json
If-Match: "1234567890"

{
  "description": "Updated via merge patch",
  "labels": ["production"]
}
```

**Example (JSON Patch):**

```bash
PATCH /management/v2/environments/DEFAULT/apis/my-api-id
Content-Type: application/json-patch+json
If-Match: "1234567890"

[
  {"op": "replace", "path": "/description", "value": "Updated via JSON Patch"},
  {"op": "add", "path": "/labels/-", "value": "production"}
]
```

### JSON Patch Constraints

| Constraint | Value | Error |
|:-----------|:------|:------|
| Maximum operations | 200 | "JSON Patch request exceeds maximum of 200 operations" |
| `path` field required | Yes | "JSON Patch operation at index {N} is missing required 'path' field" |
| `from` field required for `move`/`copy` | Yes | "JSON Patch operation at index {N} is missing required 'from' field" |
| JSON Pointer format | Must start with `/` | "not a valid JSON Pointer: must start with '/'" |
| Root pointer paths | `""` or `"/"` | Rejected with validation error |
| Out-of-bounds array index | N/A | Wrapped as `ValidationDomainException` |

**Deep Configuration Path Restrictions:**

JSON Patch operations targeting nested configuration objects are rejected. Replace the full configuration object at its top-level pointer instead:

- `/resources/N/configuration/...` → Replace at `/resources/N/configuration`
- `/endpointGroups/N/endpoints/M/configuration/...` → Replace at `/endpointGroups/N/endpoints/M/configuration`
- `/endpointGroups/N/endpoints/M/sharedConfigurationOverride/...` → Replace at `/endpointGroups/N/endpoints/M/sharedConfigurationOverride`
- `/endpointGroups/N/sharedConfiguration/...` → Replace at `/endpointGroups/N/sharedConfiguration`
- `/endpointGroups/N/services/S/configuration/...` → Replace at `/endpointGroups/N/services/S/configuration`
- `/endpointGroups/N/endpoints/M/services/S/configuration/...` → Replace at `/endpointGroups/N/endpoints/M/services/S/configuration`

### Polymorphic Type Validation

Discriminator fields require uppercase values. Lowercase values are rejected with an `invalidValue` error.

| Field | Accepted Values | Rejected Values |
|:------|:----------------|:----------------|
| `flows[].selectors[].type` | `HTTP`, `CHANNEL`, `CONDITION`, `MCP` | `http`, `channel`, `condition`, `mcp` |
| `listeners[].type` | `HTTP`, `TCP`, `SUBSCRIPTION`, `KAFKA` | `http`, `tcp`, `subscription`, `kafka` |
| `endpointGroups[].type` | `http-proxy` (lowercase accepted) | N/A |

### Flow ID Handling

Caller-supplied flow `id` values are replaced with server-generated UUIDs during persistence. Dry-run responses return `null` for flow `id` fields because no database IDs are assigned. Read flow IDs from a real PATCH response or a GET request.

### Groups Field

Setting `groups` to `null` or removing it via JSON Patch clears the groups set. Omitting `groups` preserves existing groups. Invalid group IDs are rejected with error code `data.invalid`.

### Listeners Field

Empty `listeners` arrays are accepted on PATCH with no minimum-items enforcement, matching PUT behavior.

### Validator Sanitization

The domain service validator may mutate the patched API. The response reflects validator-sanitized values, including plugin-default-injected resource configuration, sanitized flows, and sanitized properties. If the validator returns `null` for a field, the original value is preserved.

