### Configuring Token Exchange for MCP Servers

MCP Servers support the OAuth 2.0 Token Exchange grant type (`urn:ietf:params:oauth:grant-type:token-exchange`) as defined in RFC 8693. This grant type allows an MCP Server to exchange a subject token (access token, refresh token, ID token, or JWT) for a new access token with restricted scope and audience.

#### Grant Type Configuration

When creating an MCP Server, set `grantTypes` to include both `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange`:

```json
{
  "grantTypes": [
    "client_credentials",
    "urn:ietf:params:oauth:grant-type:token-exchange"
  ]
}
```

#### Token Endpoint Authentication Methods

MCP Servers support the following token endpoint authentication methods:

* `client_secret_basic`
* `client_secret_post`
* `client_secret_jwt`
* `null` (based on incoming request)

#### Subject Token Types

Configure allowed subject token types at the domain level via `domain.tokenExchangeSettings.allowedSubjectTokenTypes`. The default allowed types are:

* `access_token`
* `refresh_token`
* `id_token`
* `jwt`

#### Exchanged Token Behavior

The exchanged token has the following characteristics:

* **Expiration:** The `expires_in` value never exceeds the subject token's expiration.
* **Claims:** The `client_id` and `aud` claims are set to the MCP Server's client ID. The `gis` claim is preserved from the subject token.
* **Token Type:** The issued token type is always `urn:ietf:params:oauth:token-type:access_token`.
* **Refresh and ID Tokens:** The response never includes refresh tokens or ID tokens, even if the subject token has `offline_access` or `openid` scopes.

