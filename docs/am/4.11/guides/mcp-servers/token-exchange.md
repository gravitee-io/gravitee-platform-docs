### Exchanging Tokens with MCP Servers

To exchange a token for a new access token:

1. Authenticate the MCP server at the token endpoint using `client_secret_basic`, `client_secret_post`, or `client_secret_jwt`.
2. Include the following parameters in the request body:
   * `grant_type=urn:ietf:params:oauth:grant-type:token-exchange`
   * `subject_token` (the token to exchange)
   * `subject_token_type` (the type of the subject token)
3. Optionally specify `requested_token_type=urn:ietf:params:oauth:token-type:access_token`.
4. The system validates the request:
   * Verifies the subject token type is in the domain's allowed list
   * Confirms the MCP server has the token exchange grant type
   * Decodes and verifies the subject token
5. A new access token is issued with:
   * `client_id` and `aud` set to the MCP server's `clientId`
   * `gis` claim copied from the subject token
   * Expiration capped by the subject token's remaining lifetime

The response includes only `access_token`, `issued_token_type`, `token_type`, and `expires_in`. The token exchange flow never issues refresh tokens or ID tokens.

{% hint style="info" %}
The token exchange grant type must be explicitly enabled in domain settings. Subject token types must be in the domain's `allowedSubjectTokenTypes` list. The requested token type must be `urn:ietf:params:oauth:token-type:access_token` or omitted.
{% endhint %}

#### MCP Server Grant Type Restrictions

MCP servers can only use the following grant types:

* `client_credentials`
* `urn:ietf:params:oauth:grant-type:token-exchange`

MCP servers cannot use `authorization_code`, `implicit`, `password`, or `refresh_token` grant types.

#### MCP Server Authentication Method Restrictions

MCP servers can only use the following token endpoint authentication methods:

* `client_secret_basic`
* `client_secret_post`
* `client_secret_jwt`

MCP servers cannot use `private_key_jwt`, `tls_client_auth`, `self_signed_tls_client_auth`, or `none` authentication methods.

## Renewing Protected Resource Secrets

To renew an existing secret:

1. Send a POST request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/secrets/{secretId}/_renew`.
2. The system generates a new secret value while preserving the secret's settings identifier.
3. The response includes the new plaintext secret.
4. The system unregisters the old expiration notification and registers a new one if the renewed secret has an `expiresAt` value.

{% hint style="warning" %}
The old secret value is immediately invalidated upon renewal.
{% endhint %}

## Protected Resource Membership

Membership endpoints enable role-based access control for protected resources.

To add a member:

1. Send a POST request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/members` with the following parameters:
   * `memberId` — The identifier of the user or group
   * `memberType` — Either `USER` or `GROUP`
   * `role` — The role to assign to the member
2. The system creates the membership.

