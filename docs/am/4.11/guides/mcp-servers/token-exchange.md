### Token Exchange for MCP Servers

An MCP Server can exchange a subject token for a new access token by sending a POST request to `/token` with the following parameters:

* `grant_type=urn:ietf:params:oauth:grant-type:token-exchange`
* `subject_token=<token>`
* `subject_token_type=urn:ietf:params:oauth:token-type:<access_token|refresh_token|id_token|jwt>`
* Client credentials (via `Authorization: Basic` header or request body)

#### Validation Steps

The gateway validates the token exchange request in the following order:

1. **Subject token validation**: The gateway validates the subject token's signature and expiration.
2. **Subject token type validation**: The gateway checks that `subject_token_type` is in the domain's `allowedSubjectTokenTypes`. If the type is not allowed, the gateway returns a 400 Bad Request response with `invalid_request` error.
3. **Grant type validation**: The gateway verifies that the MCP Server has the `token-exchange` grant type enabled.

#### Token Issuance

If validation succeeds, the gateway issues a new access token with the following properties:

* `client_id` and `aud` are set to the MCP Server's `clientId`
* The `gis` claim is preserved from the subject token
* `expires_in` is capped at the subject token's remaining lifetime

The response contains only an access token. No refresh token or ID token is included.

#### MCP Server Context Restrictions

MCP Servers have the following grant type and authentication method restrictions:

**Allowed Grant Types:**
* `client_credentials`
* `urn:ietf:params:oauth:grant-type:token-exchange`

**Allowed Token Endpoint Auth Methods:**
* `client_secret_basic`
* `client_secret_post`
* `client_secret_jwt`

**Excluded Token Endpoint Auth Methods:**
* `private_key_jwt`
* `tls_client_auth`
* `self_signed_tls_client_auth`
* `none`

{% hint style="info" %}
Token exchange requires the domain's `tokenExchangeSettings.enabled` to be set to `true` and `allowedSubjectTokenTypes` to be configured.
{% endhint %}
