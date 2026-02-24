## Token exchange workflow

MCP Servers (Protected Resources in MCP context) can exchange subject tokens for new access tokens using the OAuth 2.0 Token Exchange grant type.

### Prerequisites

Before configuring token exchange, ensure the following requirements are met:

- Token exchange enabled at domain level (`tokenExchangeSettings.enabled = true`)
- Domain configured with `allowedSubjectTokenTypes` (e.g., `urn:ietf:params:oauth:token-type:access_token`, `urn:ietf:params:oauth:token-type:id_token`)
- MCP Server configured with `client_credentials` grant type
- Valid subject token (access, refresh, or ID token) obtained via standard OAuth2 flows

### Exchange process

The token exchange workflow follows these steps:

1. The application obtains a subject token using standard OAuth2 flows (authorization code, client credentials, etc.).

2. The MCP Server submits a token exchange request to the token endpoint with the following parameters:

   | Parameter | Value | Description |
   |:----------|:------|:------------|
   | `grant_type` | `urn:ietf:params:oauth:grant-type:token-exchange` | Token exchange grant type |
   | `subject_token` | Subject token value | The token to be exchanged |
   | `subject_token_type` | Token type URI | Type of the subject token (e.g., `urn:ietf:params:oauth:token-type:access_token`) |

3. The system validates the request:
   - Verifies the `subject_token_type` is in the domain's `allowedSubjectTokenTypes` list
   - Validates the subject token signature and expiration
   - Extracts the `gis` claim from the subject token

4. If validation succeeds, the system issues a new access token with:
   - MCP Server's `clientId` as both the client and audience
   - Lifetime that cannot exceed the subject token's remaining validity
   - No refresh token or ID token (even if `openid` scope is requested)

### Error responses

The following error codes may be returned during token exchange:

| Error Code | Description |
|:-----------|:------------|
| `invalid_request` | Subject token type not in `allowedSubjectTokenTypes` |
| `invalid_grant` | Subject token signature invalid or expired |

### Restrictions

Token exchange for MCP Servers has the following limitations:

- MCP Servers in token exchange flows support only `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grants
- Token exchange does not issue refresh tokens or ID tokens
- New token lifetime is constrained by subject token remaining validity

