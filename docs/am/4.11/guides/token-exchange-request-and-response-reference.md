# Token Exchange Request and Response Reference

## User Binding Criteria

Each user binding criterion specifies how to match external token claims to domain user attributes:

| Property | Type | Description |
|:---------|:-----|:------------|
| `attribute` | String | User attribute to match (e.g., `email`, `username`) |
| `expression` | String | EL expression evaluated against token claims (e.g., `{#context['email']}`) |

## Client-Level Scope Handling

Override domain-level scope handling for specific clients using `TokenExchangeOAuthSettings`:

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `inherited` | boolean | `true` | Inherit scope handling mode from domain settings |
| `scopeHandling` | Enum | `DOWNSCOPING` | `DOWNSCOPING` or `PERMISSIVE` (applies when `inherited = false`) |

## Creating a Token Exchange Request

To exchange a token, send a POST request to the token endpoint with `grant_type` set to `urn:ietf:params:oauth:grant-type:token-exchange`:

1. Include the `subject_token` and `subject_token_type` parameters with the token to be exchanged and its type URN.
2. Optionally specify `requested_token_type` to request a specific token type (defaults to access token if allowed).
3. For delegation scenarios, include `actor_token` and `actor_token_type` to identify the intermediary actor.
4. Optionally include `scope` to request a subset of allowed scopes (space-delimited).
5. Optionally include `resource` to specify target resource URIs.

The response includes the new token in the `access_token` field, with `issued_token_type` indicating the actual token type issued. No refresh token is issued during token exchange.

## Managing Trusted Issuers

Trusted issuers are managed through the domain configuration UI:

1. Navigate to the domain's token exchange settings and add a new trusted issuer.
2. Enter the issuer URL exactly as it appears in external JWTs' `iss` claim.
3. Select the key resolution method: choose `JWKS_URL` to fetch keys dynamically from a JWKS endpoint, or `PEM` to embed a certificate directly.
4. Configure scope mappings to translate external scopes to domain scopes (e.g., map `external:admin` to `domain:admin`).
5. Enable user binding if external subjects should resolve to domain users, and define binding criteria using EL expressions that match token claims to user attributes.
6. Save the configuration.

The system validates external tokens against the trusted issuer's key material and applies scope mappings before granting scopes.

## End-User Configuration

### Token Exchange Request Parameters

| Parameter | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `grant_type` | String | Yes | Must be `urn:ietf:params:oauth:grant-type:token-exchange` |
| `subject_token` | String | Yes | The security token representing the subject |
| `subject_token_type` | String | Yes | Type URN (e.g., `urn:ietf:params:oauth:token-type:access_token`) |
| `requested_token_type` | String | No | Type URN for requested token (defaults to access token if allowed) |
| `actor_token` | String | No | Token representing the actor (delegation scenarios) |
| `actor_token_type` | String | Conditional | Required when `actor_token` is provided |
| `scope` | String | No | Space-delimited scopes (subset of allowed scopes) |
| `resource` | String | No | Target resource URIs |

### Token Exchange Response

**Standard Access Token Response:**

```json
{
  "access_token": "eyJhbGc...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
  "scope": "openid profile"
}
```

**ID Token-Only Response:**

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
    "act": {
      "sub": "prior-actor-id",
      "gis": "source:prior-actor"
    },
    "actor_act": {
      "sub": "actor-delegator-id",
      "gis": "source:actor-delegator"
    }
  }
}
```

## Related Changes

The token exchange feature introduces audit logging for all token exchange operations.
