### Token Exchange for MCP Servers

MCP Servers perform token exchange to obtain access tokens on behalf of users. The workflow involves creating an Application to issue subject tokens, creating a Protected Resource with type `MCP_SERVER`, and configuring the token exchange request.

#### Prerequisites for Token Exchange

Before configuring token exchange, complete the following steps:

1. Create an Application with `password` and `refresh_token` grant types to issue subject tokens.
2. Create a Protected Resource with type `MCP_SERVER`, enabling `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types.
3. Ensure Token Exchange is enabled in domain settings.

#### Token Exchange Request

The MCP Server exchanges the subject token by calling `POST /oauth/token` with the following parameters:

| Parameter | Required | Description |
|:----------|:---------|:------------|
| `grant_type` | Yes | Must be `urn:ietf:params:oauth:grant-type:token-exchange` |
| `subject_token` | Yes | The token to be exchanged (access, refresh, or ID token) |
| `subject_token_type` | Yes | URI identifying the token type (see table below) |
| `Authorization` header | Yes | Basic authentication using MCP Server credentials |

**Example Request:**

#### Supported Subject Token Types

| Token Type | URI |
|:-----------|:----|
| Access Token | `urn:ietf:params:oauth:token-type:access_token` |
| Refresh Token | `urn:ietf:params:oauth:token-type:refresh_token` |
| ID Token | `urn:ietf:params:oauth:token-type:id_token` |
| JWT | `urn:ietf:params:oauth:token-type:jwt` |

#### Token Exchange Response

The response includes a new access token with the following characteristics:

* `client_id` and `aud` claims are set to the MCP Server's `clientId`
* `expires_in` is capped at the subject token's remaining lifetime
* `gis` claim is preserved from the subject token
* No `refresh_token` is issued in the exchange response
* No `id_token` is issued even if `openid` scope is present
