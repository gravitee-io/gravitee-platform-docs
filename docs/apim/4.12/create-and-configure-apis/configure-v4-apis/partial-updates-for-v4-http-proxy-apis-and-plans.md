# Partial Updates for V4 HTTP Proxy APIs and Plans

## Overview

V4 HTTP Proxy APIs and plans support partial updates via PATCH endpoints, allowing you to modify specific fields without replacing the entire resource definition. PATCH operations accept two standard formats—JSON Merge Patch (RFC 7396) for simple field updates and JSON Patch (RFC 6902) for fine-grained array and object manipulation—and include optional dry-run validation and optimistic concurrency control.

## Key Concepts

### JSON Merge Patch (RFC 7396)

JSON Merge Patch sends a partial object containing only the fields you want to change. Omitted fields remain unchanged, and setting a field to `null` clears it. This format is the simpler choice for most updates.

**Content-Type**: `application/merge-patch+json` or `application/json`

**Example**: Update only the description and visibility:

```json
{
  "description": "Updated description",
  "visibility": "PUBLIC"
}
```

To clear all properties, send `{"properties": null}`.

### JSON Patch (RFC 6902)

JSON Patch sends an array of operations (`add`, `remove`, `replace`, `move`, `copy`, `test`) with RFC 6901 JSON Pointer paths. Use this format for fine-grained edits such as changing one element of an array or moving fields.

**Content-Type**: `application/json-patch+json`

**Example**: Replace a single endpoint group name and remove a tag:

```json
[
  {"op": "replace", "path": "/endpointGroups/0/name", "value": "Production"},
  {"op": "remove", "path": "/tags/2"}
]
```

**Operation Limit**: Maximum 200 operations per request.

### Dry-Run Validation

The `dryRun=true` query parameter runs the full validation chain and returns the projected result without persisting changes. Use it for pre-flight validation. A subsequent GET still returns the pre-patch state. The `If-Match` precondition is enforced on dry runs.

**Caveat**: On a dry run, every `flow.id` returns `null`. This signals "not yet persisted," not an error. Read flow IDs from a real PATCH response or a GET, never from a dry-run preview.

### Optimistic Concurrency Control

GET requests on APIs and plans return an `ETag` header. Send this value in the `If-Match` header on PATCH to ensure the resource has not changed since you read it. A successful update returns a new `ETag`. A stale or unparseable `If-Match` value returns `412 Precondition Failed` and persists nothing. A 412 response does not carry a fresh ETag; re-GET to read the current version before retrying.

Omitting `If-Match` or sending `If-Match: *` skips the check—last-write-wins, matching PUT behavior.

**ETag Round-Trip Example**:

```bash
# 1. Read the current ETag
GET /management/v2/environments/DEFAULT/apis/{apiId}
→ ETag: "<etag-a>"

# 2. Conditional PATCH with that ETag
PATCH /management/v2/environments/DEFAULT/apis/{apiId}
If-Match: "<etag-a>"
Content-Type: application/merge-patch+json

{"description": "New description"}

→ 200 OK
→ ETag: "<etag-b>"

# If another writer changed the API between step 1 and step 2:
→ 412 Precondition Failed
```

## Prerequisites

* The API must be a V4 HTTP Proxy API. V2 APIs, V4 Message APIs, Federated APIs, and Native APIs return `400 Bad Request`.
* For plan PATCH operations, the plan must belong to the specified API and must be a V4 HTTP Proxy API plan.
* The authenticated user must have `API_DEFINITION[UPDATE]` and `API_GATEWAY_DEFINITION[UPDATE]` permissions for API PATCH operations.

## Creating Partial API Updates

To partially update a V4 HTTP Proxy API, send a PATCH request to `/management/v2/environments/{envId}/apis/{apiId}` with one of the supported content types. The request body format depends on the `Content-Type` header:

* **JSON Merge Patch** (`application/merge-patch+json` or `application/json`): Send a partial object containing only the fields to change. Omitted fields remain unchanged. Setting a field to `null` clears it (for nullable fields).
* **JSON Patch** (`application/json-patch+json`): Send an array of operations with JSON Pointer paths.

**Query Parameters**:

| Parameter | Type    | Default | Description                                 |
| :-------- | :------ | :------ | :------------------------------------------- |
| `dryRun`  | Boolean | `false` | Preview the result without persisting       |

**Request Headers**:

| Header         | Required | Description                                                                                      |
| :------------- | :------- | :----------------------------------------------------------------------------------------------- |
| `Content-Type` | Yes      | `application/merge-patch+json`, `application/json-patch+json`, or `application/json`             |
| `If-Match`     | No       | ETag value for optimistic concurrency control; use `*` to bypass                                 |

**Patchable API Fields**:

| Field                                | Nullable | Description                                                                                                                                                  |
| :----------------------------------- | :------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                               | No       | API name                                                                                                                                                     |
| `description`                        | Yes      | API description                                                                                                                                              |
| `apiVersion`                         | No       | API version string                                                                                                                                           |
| `visibility`                         | No       | Visibility (`PUBLIC`, `PRIVATE`)                                                                                                                             |
| `labels`                             | Yes      | API labels; `null` coalesces to empty list                                                                                                                   |
| `tags`                               | Yes      | API tags; `null` coalesces to empty set                                                                                                                      |
| `lifecycleState`                     | No       | Lifecycle state (`CREATED`, `PUBLISHED`, `UNPUBLISHED`, `DEPRECATED`, `ARCHIVED`)                                                                            |
| `categories`                         | Yes      | Category IDs; `null` coalesces to empty set                                                                                                                  |
| `groups`                             | Yes      | Group IDs; `null` coalesces to empty set                                                                                                                     |
| `analytics`                          | Yes      | Analytics configuration                                                                                                                                      |
| `failover`                           | Yes      | Failover configuration                                                                                                                                       |
| `flowExecution`                      | Yes      | Flow execution configuration                                                                                                                                 |
| `flows`                              | Yes      | API flows; `null` clears flows                                                                                                                               |
| `services`                           | Yes      | Service configurations                                                                                                                                       |
| `resources`                          | Yes      | Resource configurations                                                                                                                                      |
| `endpointGroups`                     | Yes      | Endpoint group configurations                                                                                                                                |
| `listeners`                          | Yes      | Listener configurations; `null` clears to empty; empty arrays are accepted (no minimum-items enforcement), matching PUT                                      |
| `allowedInApiProducts`               | No       | Whether API can be included in API products; `null` in storage is rendered as `false` in API responses (but stored value remains `null` until explicitly set) |
| `allowMultiJwtOauth2Subscriptions`   | No       | Whether multiple JWT/OAuth2 subscriptions are allowed                                                                                                        |
| `disableMembershipNotifications`     | No       | Whether membership notifications are disabled                                                                                                                |
| `properties`                         | Yes      | API properties; supports encryption; send `{"properties": null}` to clear all properties                                                                     |
| `responseTemplates`                  | Yes      | Response template configurations                                                                                                                             |

**Non-Patchable API Fields**:

| Field               | Reason                      | Alternative                            |
| :------------------ | :-------------------------- | :------------------------------------- |
| `state`             | Runtime state management    | Use `/_start` or `/_stop` endpoints    |
| `definitionVersion` | Immutable                   | N/A                                    |
| `type`              | Immutable                   | N/A                                    |

**Response**:

* `200 OK` — Returns the patched API with `ETag` and `Last-Modified` headers
* `400 Bad Request` — Validation failure, disallowed field, or unsupported API type
* `403 Forbidden` — Missing required permissions
* `404 Not Found` — API not found
* `412 Precondition Failed` — `If-Match` header mismatch
* `415 Unsupported Media Type` — Invalid `Content-Type`

**Null Handling**:

* **Merge Patch**: Explicit `null` on required fields returns `400 Bad Request` with message: `"'{field}' cannot be null; omit the field to leave it unchanged, or send an explicit value"`. Explicit `null` on optional fields clears the field.
* **JSON Patch**: `remove` or `replace` with `null` on required fields returns `400 Bad Request`. `remove` or `replace` with `null` on optional fields clears the field.

**Flow Handling**:

* Omitting `flows` preserves existing flows (including IDs).
* Setting `flows` to `null` (Merge Patch) or using JSON Patch `remove` on `/flows` clears flows.
* Caller-supplied flow IDs are replaced with DB-generated UUIDs on persist.
* Dry-run responses strip flow IDs to `null`.
* When converting from repository `FlowHttpSelector` to domain `HttpSelector`, if `pathOperator` is `null`, it defaults to `STARTS_WITH`.

**Property Encryption**:

Properties with `"encryptable": true` are encrypted before persistence. Encrypted properties return with `"encrypted": true` and ciphertext in `value`, in both real and dry-run responses. Already-encrypted properties are not re-encrypted when patching unrelated fields.

**Groups Handling**:

* Omitting `groups` preserves existing groups.
* Setting `groups` to `null` (Merge Patch) or using JSON Patch `remove` on `/groups` clears groups.
* Unknown group IDs are rejected by the domain service.

**JSON Patch Path Restrictions**:

The following deep configuration paths are rejected with `400 Bad Request`:

* `/resources/N/configuration/...` (any depth under `configuration`) — Replace the full configuration object at `/resources/N/configuration` instead.
* `/endpointGroups/N/endpoints/M/configuration/...`
* `/endpointGroups/N/endpoints/M/sharedConfigurationOverride/...`
* `/endpointGroups/N/sharedConfiguration/...`
* `/endpointGroups/N/services/S/configuration/...`
* `/endpointGroups/N/endpoints/M/services/S/configuration/...`

Replace each configuration blob atomically at its top-level pointer (e.g., `/endpointGroups/0/endpoints/0/configuration`).

Root pointer paths (`""` or `"/"`) are rejected with message: `"does not target a specific field"`.

**Flow Selector Type Discriminators**:

Flow selector `type` values must be uppercase: `HTTP`, `CHANNEL`, `CONDITION`, `MCP`. Lowercase variants (`http`, `channel`, etc.) are rejected with `400 Bad Request`. Listener `type` values (`HTTP`, `TCP`, `SUBSCRIPTION`, `KAFKA`) must also be uppercase. The exception is `endpointGroups[*].type`, which is a plugin identifier (e.g., `http-proxy`) and remains lowercase.

## Managing Plans
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

## Restrictions

* **Scope**: PATCH is only supported for V4 HTTP Proxy APIs and plans. V2 APIs, V4 Message APIs, Federated APIs, and Native APIs return `400 Bad Request`.
* **Operation Limit**: JSON Patch requests are limited to 200 operations per request. Exceeding this limit returns `400 Bad Request` with message: `"JSON Patch request exceeds maximum of 200 operations"`.
* **Deep Path Restrictions**: JSON Patch operations cannot target paths under resource or endpoint group configuration fields. Replace the full configuration object at the parent path instead.
* **Validator Side Effects**: The domain service validator may modify submitted values (e.g., injecting plugin defaults, filtering tags, normalizing groups). The response reflects these sanitized values, not the raw patch input.
* **Concurrency Control**: `If-Match` header is optional. Without it, last-write-wins semantics apply.
* **Flow ID Persistence**: Caller-supplied flow IDs are always replaced with DB-generated UUIDs; clients cannot control flow IDs.
* **Dry-Run Flow IDs**: Dry-run responses strip flow IDs to `null`; clients must re-fetch to obtain server-assigned IDs.
* **Precondition on `null` `updatedAt`**: If a resource has `null` `updatedAt`, any `If-Match` header (except wildcard `*`) is rejected with `412 Precondition Failed`.
* **Nested Pointer Null Handling**: JSON Patch operations with `null` values on nested pointers (e.g., `/security/type`) do not clear the top-level field; the top-level field remains unchanged.
* **Plan Definition Absence**: When patching `selectionRule` or `security` on a plan without an HTTP V4 definition (`planDefinitionHttpV4` is `null`), the operation is a no-op and does not throw an error.

## Related Changes

**Before**: V4 HTTP Proxy APIs and plans could only be updated via `PUT /management/v2/environments/{envId}/apis/{apiId}` and `PUT /management/v2/environments/{envId}/apis/{apiId}/plans/{planId}`, requiring the full resource definition.

**After**: V4 HTTP Proxy APIs and plans can be partially updated via PATCH endpoints using RFC 7396 JSON Merge Patch or RFC 6902 JSON Patch.

**Flow Selector Type Discriminators**:

* **Before**: Lowercase selector types (e.g., `"type": "http"`) were accepted in some contexts.
* **After**: Only uppercase discriminators (e.g., `"type": "HTTP"`) are accepted in PATCH requests.
* **Migration**: Update client code to use uppercase selector types.

**Flow ID Handling**:

* **Before**: Caller-supplied flow IDs were persisted as-is.
* **After**: Caller-supplied IDs are replaced with DB-generated UUIDs; dry-run responses strip IDs.
* **Migration**: Do not rely on caller-supplied flow IDs; use server-returned IDs from responses.

**Precondition Evaluation**:

* **Before**: Malformed `If-Match` headers were silently ignored on non-strict paths.
* **After**: Malformed `If-Match` headers are rejected with `412 Precondition Failed` on PATCH endpoints.
* **Migration**: Ensure `If-Match` headers are well-formed quoted strings or wildcard `*`.

**Behavioral Changes**:

1. **Null Handling**: Setting a nullable field to `null` via PATCH clears the field; omitting the field leaves it unchanged. This differs from PUT, where omitted fields may be set to defaults.
2. **Dry-Run Mode**: `dryRun=true` invokes domain service validation and returns the projected result without persisting. Validation failures (e.g., tag restrictions, invalid selectors) surface as `400 Bad Request`. No audit entries are created in dry-run mode.
3. **Response Headers**: Successful PATCH responses include `ETag` and `Last-Modified` headers derived from the resource's `updatedAt` timestamp.
4. **Policy Configuration Sanitization**: Policy configurations in flows are sanitized via the policy validation domain service. Sanitized configurations are reflected in both the response and stored state.
5. **HTTP Selector Path Operator Default**: When converting from repository `FlowHttpSelector` to domain `HttpSelector`, if `pathOperator` is `null`, it defaults to `STARTS_WITH`.

**Compatibility Notes**:

* **V2 APIs**: PATCH requests to V2 APIs return `400 Bad Request` with message indicating invalid definition version.
* **V4 Message APIs**: PATCH requests to V4 Message APIs return `400 Bad Request` with message indicating invalid type.
* **Federated APIs**: PATCH requests to Federated APIs return `400 Bad Request` with message indicating invalid definition version.
* **Management-v1 REST API**: Plan PATCH is served only by management-v2 REST API; management-v1 throws `UnsupportedOperationException`.
* **Portal REST API**: Plan PATCH is served only by management-v2 REST API; portal REST API throws `UnsupportedOperationException`.