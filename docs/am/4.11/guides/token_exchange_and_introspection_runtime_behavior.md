### Token Exchange with MCP Servers

Token exchange allows an MCP Server to exchange a subject token for a new access token. The exchange flow requires domain-level configuration and MCP Server grant type support.

#### Prerequisites

Before using token exchange:

* Enable token exchange in the domain settings by setting `tokenExchangeSettings.enabled` to `true`.
* Configure the MCP Server with grant type `urn:ietf:params:oauth:grant-type:token-exchange`.

#### Token Exchange Request

To exchange a token, send a POST request to `/oauth/token` with the following parameters:

| Parameter | Value | Description |
|:----------|:------|:------------|
| `grant_type` | `urn:ietf:params:oauth:grant-type:token-exchange` | Token exchange grant type |
| `subject_token` | `<token>` | The token to exchange |
| `subject_token_type` | `<type>` | Token type identifier (e.g., `urn:ietf:params:oauth:token-type:access_token`) |
| `Authorization` | `Basic <credentials>` | MCP Server client credentials |

**Example Request:**

```http
POST /oauth/token
Content-Type: application/x-www-form-urlencoded
Authorization: Basic <mcpServerBasicAuth>

grant_type=urn:ietf:params:oauth:grant-type:token-exchange
&subject_token=<subjectToken>
&subject_token_type=urn:ietf:params:oauth:token-type:access_token
```

#### Token Exchange Response

The response includes an access token with the following characteristics:

```json
{
  "access_token": "<exchangedToken>",
  "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
  "token_type": "bearer",
  "expires_in": 3600
}
```

**Token Claims:**

* `client_id` and `aud` claims are set to the MCP Server's client ID
* `gis` claim is preserved from the subject token
* `expires_in` is capped by the subject token's expiration

**Excluded Tokens:**

* No `refresh_token` is issued
* No `id_token` is issued

#### Subject Token Type Validation

If the domain restricts `allowedSubjectTokenTypes`, only listed token types are accepted. When a token type is not allowed, the request fails with:

```json
{
  "error": "invalid_request",
  "error_description": "subject_token_type not allowed"
}
```
