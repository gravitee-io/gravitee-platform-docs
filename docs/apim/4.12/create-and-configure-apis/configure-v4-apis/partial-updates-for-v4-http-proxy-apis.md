# Partial Updates for V4 HTTP Proxy APIs

## Overview

V4 HTTP Proxy APIs support partial updates via PATCH endpoints, allowing you to modify specific fields without replacing the entire resource definition. PATCH operations accept two standard formats—JSON Merge Patch (RFC 7396) for simple field updates and JSON Patch (RFC 6902) for fine-grained array and object manipulation—and include optional dry-run validation and optimistic concurrency control.

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

**Operation Limit**: Maximum 200 operations per request. Exceeding this limit returns `400 Bad Request`.

### Dry-Run Validation

The `dryRun=true` query parameter runs the full validation chain and returns the projected result without persisting changes. Use it for pre-flight validation. Validation failures (e.g., tag restrictions, invalid selectors) surface as `400 Bad Request`. No audit entries are created in dry-run mode. A subsequent GET still returns the pre-patch state. The `If-Match` precondition is enforced on dry runs.

**Caveat**: On a dry run, every `flow.id` returns `null`. This signals "not yet persisted," not an error. Read flow IDs from a real PATCH response or a GET, never from a dry-run preview.

### Optimistic Concurrency Control

GET requests on APIs return an `ETag` header. Send this value in the `If-Match` header on PATCH to ensure the resource has not changed since you read it. A successful update returns a new `ETag`. A stale or unparseable `If-Match` value returns `412 Precondition Failed` and persists nothing. Malformed `If-Match` headers are rejected with `412 Precondition Failed`. A 412 response does not carry a fresh ETag; re-GET to read the current version before retrying.

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
* The authenticated user must have `API_DEFINITION[UPDATE]` and `API_GATEWAY_DEFINITION[UPDATE]` permissions for API PATCH operations.

## Creating Partial API Updates

To partially update a V4 HTTP Proxy API, send a PATCH request to `/management/v2/environments/{envId}/apis/{apiId}` with one of the supported content types. The request body format depends on the `Content-Type` header:

* **JSON Merge Patch** (`application/merge-patch+json` or `application/json`): Send a partial object containing only the fields to change. Omitted fields remain unchanged. Setting a field to `null` clears it (for nullable fields).
* **JSON Patch** (`application/json-patch+json`): Send an array of operations with JSON Pointer paths.

{% hint style="info" %}
**Validator Side Effects**
The domain service validator may modify submitted values (e.g., injecting plugin defaults, filtering tags, normalizing groups). The response reflects these sanitized values, not the raw patch input.
{% endhint %}

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

* **Merge Patch**: Explicit `null` on required fields returns `400 Bad Request` with message: `"{field}' cannot be null; omit the field to leave it unchanged, or send an explicit value"`. Explicit `null` on optional fields clears the field.
* **JSON Patch**: `remove` or `replace` with `null` on required fields returns `400 Bad Request`. `remove` or `replace` with `null` on optional fields clears the field.
* **Nested Pointer**: JSON Patch operations with `null` values on nested pointers (e.g., `/security/type`) do not clear the top-level field; the top-level field remains unchanged.

**Flow Handling**:

* Omitting `flows` preserves existing flows (including IDs).
* Setting `flows` to `null` (Merge Patch) or using JSON Patch `remove` on `/flows` clears flows.
* Caller-supplied flow IDs are replaced with DB-generated UUIDs on persist.
* Dry-run responses strip flow IDs to `null`.
* When converting from repository `FlowHttpSelector` to domain `HttpSelector`, if `pathOperator` is `null`, it defaults to `STARTS_WITH`.
* Policy configurations in flows are sanitized via the policy validation domain service. Sanitized configurations are reflected in both the response and stored state.

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
