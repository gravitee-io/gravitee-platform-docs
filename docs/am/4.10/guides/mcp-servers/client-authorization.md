# Client Authorization

## Overview <a href="#how-mcp-servers-work" id="how-mcp-servers-work"></a>

The MCP Server authorization flow follows the official [MCP specification](https://modelcontextprotocol.io/specification/draft/basic/authorization). At a high level, it consists of the following criteria:

* The client includes the `resource` parameter on both `/authorize` and `/token`.
* On the first unauthenticated call, the MCP Server returns `401` with `resource_metadata` within the `WWW-Authenticate` header.
* The OAuth 2.1 flow returns an authorization code, not a token.
* The client exchanges `code → token` via `/token`.
* The MCP Server validates the token and scopes, and then executes the tool based on its decision.

The following diagram shows full MCP Server authorization flow with [AuthZen](../authorization-engines/authzen.md) and [OpenFGA](../authorization-engines/openfga.md) as the Authorization Engine.

<figure><img src="../../.gitbook/assets/Screenshot 2025-11-27 at 12.09.35.png" alt=""><figcaption></figcaption></figure>

## MCP Server authorization flow <a href="#how-mcp-servers-work" id="how-mcp-servers-work"></a>

The details of the MCP Server authorization flow are broken down into the following sequence of actions.

<details>

<summary>1. Administrator configures the MCP Server in Gravitee AM</summary>

In the AM Console:

* Create an MCP Server entry.
* Define the available tools.
* Assign the required scopes per tool.
* Ensure the resource identifier matches the MCP Server URL.

</details>

<details>

<summary>2. Client attempts to call MCP Server → receives 401 Unauthorized</summary>

When a client calls a protected MCP tool without a valid access token, the MCP Server must return a `401 Unauthorized` with a `WWW-Authenticate` header that includes a `resource_metadata` URL (Protected Resource Metadata document). This tells the client where and how to authorize.

Example response:

```http
401 Unauthorized
WWW-Authenticate: Bearer resource_metadata="https://mcp.example.com/.well-known/oauth-protected-resource"
```

</details>

<details>

<summary>3. Client discovers authorization information</summary>

The client first retrieves the Protected Resource Metadata from the MCP Server:

```http
GET https://mcp.example.com/.well-known/oauth-protected-resource
```

The response includes the MCP Server's resource identifier and one or more authorization servers. For example:

```json
{
  "resource": "https://mcp.example.com",
  "authorization_servers": [
    "https://am.gateway.io"
  ]
}
```

Using this information, the client retrieves the Authorization Server Metadata from Gravitee AM, as required by the OAuth 2.1 and MCP specifications:

```http
GET https://am.gateway.io/{{domain}}/.well-known/oauth-authorization-server
```

This endpoint points to the OIDC discovery document, which contains the full set of required authorization details:

```http
GET https://am.gateway.io/{{domain}}/oidc/.well-known/openid-configuration
```

The OpenID Connect discovery document provides all endpoints needed for the OAuth 2.1 flow, including:

* `authorization_endpoint`
* `token_endpoint`
* `issuer`
* `jwks_uri`
* Supported scopes, response types, and grant types

This ensures the MCP client has complete metadata about the Authorization Server.

</details>

<details>

<summary>4. Client starts OAuth 2.1 Authorization Code Flow (with PKCE)</summary>

The client initiates the `/authorize` request.

{% hint style="warning" %}
The `resource` parameter is mandatory and must match the MCP Server’s resource identifier.
{% endhint %}

Example `/authorize` request:

```http
GET /oauth/authorize
  ?response_type=code
  &client_id=abc123
  &redirect_uri=https://client.example.com/callback
  &scope=tool:get_weather
  &resource=https://mcp.example.com
  &code_challenge=xyz
  &code_challenge_method=S256
```

</details>

<details>

<summary>5. User authenticates in Gravitee AM</summary>

AM validates the following:

* User identity
* Requested scopes
* `resource` identifier
* PKCE parameters

If everything is valid → redirect with authorization code.

</details>

<details>

<summary>6. Client receives the authorization code</summary>

The redirect looks like the following:

```
https://client.example.com/callback?code=XYZ
```

According to the OAuth 2.1 specification, only the code is returned.

</details>

<details>

<summary>7. Client exchanges authorization code for access token</summary>

The client calls the `/token` endpoint.

{% hint style="warning" %}
The `resource` parameter is mandatory and must match the MCP Server’s resource identifier.
{% endhint %}

Example:

<pre><code><strong>POST /oauth/token
</strong>Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
code=XYZ
redirect_uri=https://client.example.com/callback
client_id=abc123
code_verifier=original_verifier
resource=https://mcp.example.com
</code></pre>

The Authorization Server returns the access token (and optionally the refresh token) with the `aud` claim equal to the resource identifier.

</details>

<details>

<summary>8. Client calls MCP Server with the access token</summary>

```
Authorization: Bearer <ACCESS_TOKEN>
```

</details>

<details>

<summary>9. MCP Server validates the access token</summary>

To check the validation, the MCP Server must:

*   Validate the token by calling the introspect endpoint:

    ```
    POST /{{domain}}/oauth/introspect HTTP/1.1
    Authorization: Basic {{base64(client_id:client_secret)}}
    Content-Type: application/x-www-form-urlencoded

    token={{access_token}}
    token_type_hint=access_token

    ```
* Check required scopes for the tool being requested.

Token validation triggers one of the following:

* If the token is missing or invalid → `401`.
* If the token is valid but has insufficient scopes → `403`.
* If the token is valid → execute tool.

</details>

<details>

<summary>10. Fine-grained permissions check</summary>

The permission check uses the Authorization Engine and AuthZen and is described in the [Authorization Engines](../authorization-engines/README.md) section.

</details>
