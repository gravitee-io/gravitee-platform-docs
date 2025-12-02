# AuthZen

{% hint style="danger" %}
**Preview Feature:** The AuthZen Gateway Handler is currently in preview. Features and APIs may change in future releases. **This functionality is not production-ready and should be used with caution.**
{% endhint %}

{% hint style="warning" %}
The plugin is only available in the [Enterprise Edition (EE)](../../overview/open-source-vs-enterprise-am/) of Gravitee.
{% endhint %}

## Overview

[AuthZEN](https://openid.net/specs/authorization-api-1_0-01.html) is an OpenID Foundation initiative designed to standardize externalized authorization. Its goal is to define a uniform, interoperable way for applications acting as Policy Enforcement Points (PEPs) to request authorization decisions from Policy Decision Points (PDPs).

In Gravitee Access Management, AuthZen acts as the standardized interface used by MCP Servers and other applications to perform authorization checks against the configured Authorization Engine (e.g., OpenFGA).

The AuthZen Gateway Handler does the following:

* Integrates with the AM Gateway.
* Sends authorization requests to the active Authorization Engine per domain.
*   Exposes a dedicated evaluation endpoint. For example:

    ```
    POST https://{gateway}/{domain}/access/v1/evaluation
    ```

## Prerequisites

* Gravitee Access Management 4.10.0+.
* Valid Gravitee Enterprise license with `enterprise-authorization-engine` pack.
* A configured Authorization Engine plugin instance. For example, OpenFGA.

## Request format

AuthZen expects a JSON body with the following structure:

* `subject`: Represents the principal performing the action.
* `resource`: The resource being accessed.
* `action`: The action being evaluated.
* `context`: Additional environmental or request context passed to the Authorization Engine.

<table><thead><tr><th>Parameter</th><th data-type="checkbox">Required</th><th>Name/Type</th><th>ID</th><th>Properties</th></tr></thead><tbody><tr><td><code>subject</code></td><td>true</td><td>Entity type (e.g., <code>"user"</code>, <code>"service"</code>).</td><td>Unique identifier.</td><td>(Optional) Additional attributes.</td></tr><tr><td><code>resource</code></td><td>true</td><td>Resource type (e.g., <code>"tool"</code>, <code>"document"</code>, <code>"account"</code>).</td><td>Unique identifier.</td><td>(Optional) Metadata.</td></tr><tr><td><code>action</code></td><td>true</td><td>Action name (e.g., <code>"can_access"</code>, <code>"can_read"</code>, <code>"can_write"</code>).</td><td>N/A</td><td>(Optional) Additional metadata.</td></tr><tr><td><code>context</code></td><td>false</td><td>Arbitrary contextual information.</td><td>N/A</td><td>(Optional) Additional context fields.</td></tr></tbody></table>

<details>

<summary>Example request</summary>

```json
curl --location 'https://my-gateway/domain1/access/v1/evaluation' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'X-Request-ID: req123' \
--header 'Content-Type: application/json' \
--data '{
        "subject": { "type": "user", "id": "user123" },
        "resource": { "type": "tool", "id": "get_weather" },
        "action": { "name": "can_access" }
}'
```

</details>

## Response format

The evaluation endpoint returns a JSON object containing the following:

* **Decision**: Boolean value indicating whether access is allowed (`true`) or denied (`false`).
* **Context**: (Optional) Additional information for the PEP. For example, obligations, reasons, or expiry information.

<details>

<summary>Example response</summary>

```json
{
  "decision": true,
  "context": {
    "reason": "User has admin role",
    "expires_at": "2024-12-31T23:59:59Z"
  }
}
```

</details>

## Headers

### Request headers

| Header          | Description                                        |
| --------------- | -------------------------------------------------- |
| `Authorization` | Bearer token used to authenticate the request.     |
| `X-Request-ID`  | (Optional) Request identifier for logging/tracing. |
| `Content-Type`  | Must be `application/json`.                        |

### Response headers

| Header          | Description                         |
| --------------- | ----------------------------------- |
| `Cache-Control` | `no-store`.                         |
| `Pragma`        | `no-cache`.                         |
| `Content-Type`  | `application/json`.                 |
| `X-Request-ID`  | Echoed back if sent in the request. |

## Error responses

The following table includes examples of possible error responses returned by the AuthZen endpoint:

| Error                     | Description                                                                           | Example                                                          |
| ------------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `400 Bad Request`         | The request body is invalid or does not comply with the AuthZen schema.               | Missing required fields, wrong data types, malformed JSON.       |
| `401 Unauthorized`        | Authentication failed.                                                                | Missing or invalid Bearer token, expired access token.           |
| `503 Service Unavailable` | The Authorization Engine for the domain is not configured or temporarily unavailable. | Plugin not found, engine disabled, connection to OpenFGA failed. |
