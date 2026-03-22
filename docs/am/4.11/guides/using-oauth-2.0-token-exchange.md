# Using OAuth 2.0 Token Exchange

## Client-Level Scope Handling

Configure at **Application Settings > OAuth 2.0 > Token Exchange**.

| Property | Description | Example |
|:---------|:------------|:--------|
| `inherited` | Inherit scope handling mode from domain | `true` |
| `scopeHandling` | Override with `DOWNSCOPING` or `PERMISSIVE` | `PERMISSIVE` |

## Creating a Token Exchange Request

To exchange a token, the client sends a POST request to the token endpoint (`/oauth/token`) with `grant_type=urn:ietf:params:oauth:grant-type:token-exchange`. Include `subject_token` (the token to exchange) and `subject_token_type` (its type URN). Optionally include `requested_token_type` (defaults to `ACCESS_TOKEN` if allowed) and `scope` (space-delimited scopes). For delegation, include `actor_token` and `actor_token_type`. Optionally include `resource` (target resource URIs).

The gateway validates token types against domain settings, verifies token signatures and temporal claims, resolves the user (via binding criteria or virtual user creation), computes granted scopes per the configured mode, and returns a new token with `issued_token_type` indicating the result type.

**Example Impersonation Request:**

```http
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=urn:ietf:params:oauth:grant-type:token-exchange
&subject_token=eyJhbGc...
&subject_token_type=urn:ietf:params:oauth:token-type:access_token
&requested_token_type=urn:ietf:params:oauth:token-type:access_token
&scope=openid profile
&client_id=my-client
&client_secret=my-secret
```

**Example Delegation Request:**

```http
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=urn:ietf:params:oauth:grant-type:token-exchange
&subject_token=eyJhbGc...
&subject_token_type=urn:ietf:params:oauth:token-type:access_token
&actor_token=eyJhbGc...
&actor_token_type=urn:ietf:params:oauth:token-type:access_token
&requested_token_type=urn:ietf:params:oauth:token-type:access_token
&client_id=my-client
&client_secret=my-secret
```

## Managing Delegation Chains

When delegation is enabled, the gateway builds an `act` claim in the new access token to record the actor's identity and prior delegation chains. The `act.sub` field contains the actor user ID. If the subject token contains an `act` claim, it is nested under the new token's `act` claim to preserve the prior chain. If the actor token contains an `act` claim, it is nested as `act.actor_act` to preserve the actor's own delegation history. The gateway calculates the resulting delegation depth as `max(subjectDepth, actorDepth) + 1` and rejects the request if it exceeds `maxDelegationDepth`.

**Example Access Token with Delegation:**

```json
{
  "sub": "subject-user-id",
  "client_id": "requesting-client-id",
  "act": {
    "sub": "actor-user-id",
    "gis": "actor-gis-claim",
    "act": { "sub": "prior-actor-1" },
    "actor_act": { "sub": "prior-actor-2" }
  }
}
```

## Token Exchange Responses

### Access Token Response

When `requested_token_type` is `urn:ietf:params:oauth:token-type:access_token` (or defaults to it), the response includes an access token JWT, expiration, and granted scopes.

```json
{
  "access_token": "eyJhbGc...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
  "scope": "openid profile"
}
```

### ID Token Response

When `requested_token_type` is `urn:ietf:params:oauth:token-type:id_token`, the response places the ID token JWT in the `access_token` field, sets `token_type` to `N_A`, and omits the `scope` field. No refresh token is issued.

```json
{
  "access_token": "eyJhbGc...",
  "token_type": "N_A",
  "expires_in": 3600,
  "issued_token_type": "urn:ietf:params:oauth:token-type:id_token"
}
```

## Restrictions

- Token exchange is disabled by default; `TokenExchangeSettings.enabled` must be set to `true`
- Delegation is disabled by default; `allowDelegation` must be set to `true` to use `actor_token`
- Impersonation is enabled by default; set `allowImpersonation=false` to require `actor_token`
- `maxDelegationDepth` must be between 1 and 100
- No refresh token is issued for token exchange requests
- Requested scopes must be a subset of allowed scopes (per DOWNSCOPING or PERMISSIVE mode) or the request fails with `"Requested scope is not allowed"`
- If `requested_token_type` is omitted and `ACCESS_TOKEN` is not in `allowedRequestedTokenTypes`, the request fails with `"requested_token_type is required when access_token is not allowed"`
- Subject and actor tokens from trusted issuers must have `iss` claims matching the configured issuer URL
- User binding requires exactly one matching user; zero or multiple matches cause the exchange to fail
- Revoked domain tokens are rejected during validation
- Trusted issuer tokens are not checked for revocation (external revocation endpoints are not supported)

## Related Changes

The token exchange feature introduces the following changes:

- New grant type `urn:ietf:params:oauth:grant-type:token-exchange` available for client applications
- New domain-level settings at **Domain Settings > OAuth 2.0 > Token Exchange**
- New client-level settings at **Application Settings > OAuth 2.0 > Token Exchange**
- New trusted issuer configuration at **Domain Settings > OAuth 2.0 > Token Exchange > Trusted Issuers**
- New audit events for token exchange requests with subject/actor token parameters
- New token repository fields `parentSubjectJti` and `parentActorJti` to track token lineage
