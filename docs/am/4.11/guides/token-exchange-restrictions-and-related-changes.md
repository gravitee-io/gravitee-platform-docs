# Token Exchange Restrictions and Related Changes

## Token Exchange Response

### Standard Access Token Response

```json
{
  "access_token": "eyJhbGc...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
  "scope": "openid profile"
}
```

### ID Token-Only Response

```json
{
  "access_token": "eyJhbGc...",
  "token_type": "N_A",
  "expires_in": 3600,
  "issued_token_type": "urn:ietf:params:oauth:token-type:id_token"
}
```

### Delegation Token Claims

When delegation is enabled and an actor token is provided, the issued access token includes an `act` claim:

```json
{
  "sub": "subject-user-id",
  "client_id": "requesting-client-id",
  "act": {
    "sub": "actor-user-id",
    "gis": "actor-gis-claim-if-present",
    "act": { /* nested act claim from subject token if present */ },
    "actor_act": { /* act claim from actor token if actor is also delegated */ }
  }
}
```

## Restrictions

* Token exchange must be enabled at the domain level (`enabled = true`)
* Refresh tokens are never issued during token exchange
* Subject token type must be in `allowedSubjectTokenTypes`
* Requested token type must be in `allowedRequestedTokenTypes` (or omitted if access token is allowed)
* Requested token type must be `ACCESS_TOKEN` or `ID_TOKEN`
* Impersonation requires `allowImpersonation = true`
* Delegation requires `allowDelegation = true`
* Actor token type must be in `allowedActorTokenTypes` when delegation is enabled
* Delegation depth cannot exceed `maxDelegationDepth` (calculated as 1 + max(subject depth, actor depth))
* Requested scopes must be a subset of allowed scopes (computed per scope handling mode)
* Domain-issued tokens are checked for revocation before exchange
* Trusted issuer JWT signatures must verify against configured key material
* Trusted issuer `iss` claim must match configured issuer URL
* User binding requires exactly one matching user (zero or multiple matches result in error)
* ID token-only responses omit the `scope` field per RFC 8693

## Related Changes

The token exchange feature introduces audit logging for all token exchange operations. Audit events include the following parameters: `REQUESTED_TOKEN_TYPE`, `SUBJECT_TOKEN`, `SUBJECT_TOKEN_TYPE`, `ACTOR_TOKEN`, `ACTOR_TOKEN_TYPE`.

The UI includes a trusted issuer management interface with autocomplete for domain scope selection when configuring scope mappings.

Token validation checks domain-issued tokens for revocation before exchange. The grant type architecture was refactored to use a strategy pattern, enabling modular token exchange logic.

<!-- GAP: Details on token revocation query mechanism pending -->
<!-- GAP: PRE_TOKEN and POST_TOKEN extension point interfaces and policy registration process pending -->

