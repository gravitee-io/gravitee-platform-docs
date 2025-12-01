# AuthZen

{% hint style="warning" %}
Preview Feature: The AuthZen Gateway Handler is currently in preview. Features and APIs may change in future releases. This functionality is not production-ready and should be used with caution.
{% endhint %}

{% hint style="info" %}
The plugin is only available in the Enterprise Edition (EE) of Gravitee.
{% endhint %}

## Overview

AuthZEN is an OpenID Foundation initiative designed to standardize externalized authorization. Its goal is to define a uniform, interoperable way for applications acting as Policy Enforcement Points (PEPs) to request authorization decisions from Policy Decision Points (PDPs).

In Gravitee Access Management, AuthZen acts as the standardized interface used by MCP Servers and other applications to perform authorization checks against the configured Authorization Engine (for example, OpenFGA).

The AuthZen Gateway Handler does the following:

- Integrates with the AM Gateway.
- Sends authorization requests to the active Authorization Engine per domain.
- Exposes a dedicated evaluation endpoint. For example:

```text
POST https://{gateway}/{domain}/access/v1/evaluation
```

## Prerequisites

- Gravitee Access Management **4.10.0+**.
- Valid Gravitee Enterprise license with `enterprise-authorization-engine` pack.
- A configured Authorization Engine plugin instance (for example, OpenFGA).

### Request format

AuthZen expects a JSON body with the following structure:

- `subject`: Represents the principal performing the action.
- `resource`: The resource being accessed.
- `action`: The action being evaluated.
- `context`: Additional environmental or request context passed to the Authorization Engine.

#### Parameters

| Parameter | Required | Name/Type                                                                 | ID                          | Properties                             |
| --------- | -------- | ------------------------------------------------------------------------- | --------------------------- | -------------------------------------- |
| `subject` | Yes      | Entity type (for example, `"user"`, `"service"`).                     | Unique identifier.          | (Optional) Additional attributes.      |
| `resource`| Yes      | Resource type (for example, `"tool"`, `"document"`, `"account"`).   | Unique identifier.          | (Optional) Metadata.                   |
| `action`  | Yes      | Action name (for example, `"can_access"`, `"can_read"`, `"can_write"`). | N/A                         | (Optional) Additional metadata.        |
| `context` | No       | Arbitrary contextual information.                                         | N/A                         | (Optional) Additional context fields.  |

## Response format

The evaluation endpoint returns a JSON object containing the following:

- **decision**: Boolean value indicating whether access is allowed (`true`) or denied (`false`).
- **context**: (Optional) Additional information for the PEP. For example, obligations, reasons, or expiry information.

#### Example request

```bash
curl --location 'https://my-gateway/domain1/access/v1/evaluation'   --header 'Authorization: Bearer <TOKEN>'   --header 'X-Request-ID: req123'   --header 'Content-Type: application/json'   --data '{
  "subject": { "type": "user", "id": "user123" },
  "resource": { "type": "tool", "id": "get_weather" },
  "action": { "name": "can_access" }
}'
```

#### Example response

```json
{
  "decision": true,
  "context": {
    "reason": "User has admin role",
    "expires_at": "2024-12-31T23:59:59Z"
  }
}
```

## Headers

### Request headers

| Header         | Description                                                |
| ------------- | ---------------------------------------------------------- |
| `Authorization` | Bearer token used to authenticate the request.          |
| `X-Request-ID`  | (Optional) Request identifier for logging/tracing.      |
| `Content-Type`  | Must be `application/json`.                             |

### Response headers

| Header         | Description                                           |
| ------------- | ----------------------------------------------------- |
| `Cache-Control` | `no-store`.                                         |
| `Pragma`        | `no-cache`.                                         |
| `Content-Type`  | `application/json`.                                 |
| `X-Request-ID`  | Echoed back if sent in the request.                 |

## Error responses

The following table includes examples of possible error responses returned by the AuthZen endpoint:

| Error                  | Description                                                                 | Example                                                          |
| ---------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `400 Bad Request`      | The request body is invalid or does not comply with the AuthZen schema.    | Missing required fields, wrong data types, malformed JSON.       |
| `401 Unauthorized`     | Authentication failed.                                                      | Missing or invalid Bearer token, expired access token.           |
| `503 Service Unavailable` | The Authorization Engine for the domain is not configured or temporarily unavailable. | Plugin not found, engine disabled, connection to OpenFGA failed. |