# Performing OAuth 2.0 Token Exchange: Request Parameters, Response Fields, and Restrictions

## User Binding Criteria

Define how to resolve external subjects to domain users:

| Property | Description | Example |
|:---------|:------------|:--------|
| `attribute` | User attribute to match | `email` |
| `expression` | SpEL expression evaluated against token claims | `{#token['email']}` |

The EL context includes `token` (JWT claims map) and `issuer` (trusted issuer URL). Multiple criteria are combined with AND logic. User lookup must return exactly one user or the exchange fails.

## Client-Level Scope Handling

Override scope handling mode per client:

| Property | Description | Example |
|:---------|:------------|:--------|
| `scopeHandling` | `DOWNSCOPING` or `PERMISSIVE` | `PERMISSIVE` |
| `inherited` | Inherit from domain settings | `false` |

## Creating a Token Exchange Request

To exchange a token, send a POST request to the `/oauth/token` endpoint:

1. Set `grant_type` to `urn:ietf:params:oauth:grant-type:token-exchange`.
2. Include the `subject_token` and `subject_token_type` parameters with the token to be exchanged and its type URN.
3. Optionally specify `requested_token_type` to request a specific token type. Defaults to access token if allowed.
4. Optionally include `scope` to request a subset of allowed scopes. If omitted, all allowed scopes are granted.
5. For delegation, include `actor_token` and `actor_token_type` to document the actor performing the exchange.
6. Authenticate the client using standard OAuth 2.0 client authentication (e.g., `client_id` and `client_secret` in the request body or HTTP Basic authentication).

The response includes the issued token in the `access_token` field, `issued_token_type` indicating the token type, and `expires_in` for token lifetime.

## End-User Configuration

### Token Exchange Request Parameters

| Parameter | Required | Description |
|:----------|:---------|:------------|
| `grant_type` | Yes | Must be `urn:ietf:params:oauth:grant-type:token-exchange` |
| `subject_token` | Yes | The security token representing the subject |
| `subject_token_type` | Yes | Type URN (e.g., `urn:ietf:params:oauth:token-type:access_token`) |
| `requested_token_type` | No | Type URN for requested token (defaults to `access_token` if allowed) |
| `scope` | No | Requested scopes (subset of allowed scopes) |
| `resource` | No | Target resource URIs |
| `actor_token` | No | Token representing the actor (delegation only) |
| `actor_token_type` | Conditional | Required when `actor_token` is provided |

If the `scope` parameter is omitted, all allowed scopes are granted. If provided, requested scopes must be a subset of allowed scopes or the request fails with `invalid_scope`.

For impersonation, base scopes equal subject token scopes. For delegation, base scopes equal subject token scopes intersected with actor token scopes.

### Token Exchange Response Fields

| Field | Description |
|:------|:------------|
| `access_token` | The issued token (access token or ID token) |
| `token_type` | `Bearer` for access tokens, `N_A` for ID tokens |
| `expires_in` | Token lifetime in seconds |
| `issued_token_type` | Type URN of the issued token |
| `scope` | Granted scopes (omitted for ID tokens) |

## Restrictions

- Token exchange must be explicitly enabled at the domain level (`enabled: true`)
- Impersonation requires `allowImpersonation: true`; delegation requires `allowDelegation: true`
- `subject_token_type` must be in `allowedSubjectTokenTypes`
- `requested_token_type` must be in `allowedRequestedTokenTypes`
- `actor_token_type` must be in `allowedActorTokenTypes` (when delegation is used)
- Delegation depth cannot exceed `maxDelegationDepth` (default: 25, range: 1-100)
- Requested scopes must be a subset of allowed scopes (computed per scope handling mode)
- Domain-issued tokens are validated against the token repository; revoked tokens are rejected
- External tokens from trusted issuers are validated using JWKS or PEM certificates; signature verification failures result in `invalid_grant` errors
- User binding requires exactly one matching user; zero or multiple matches result in `invalid_grant` errors
- No refresh tokens are issued via token exchange
- When `requested_token_type` is `id_token`, the ID token is returned in the `access_token` field with `token_type` set to `"N_A"`; no `scope` or `refresh_token` is included
- SpEL expression evaluation errors in user binding criteria result in `invalid_grant` errors
- Temporal validation (`exp`, `nbf`) is enforced for all subject and actor tokens

## Related Changes

The token exchange feature introduces new audit events logging `SUBJECT_TOKEN`, `SUBJECT_TOKEN_TYPE`, `ACTOR_TOKEN`, `ACTOR_TOKEN_TYPE`, and `REQUESTED_TOKEN_TYPE` parameters. The OAuth settings UI includes a new "Token Exchange" section with toggles for impersonation and delegation, multi-select fields for allowed token types, and a numeric input for maximum delegation depth. A new "Trusted Issuers" UI allows administrators to configure external JWT issuers with JWKS or PEM key resolution, scope mappings, and user binding criteria; the domain scopes field includes autocomplete for valid scopes. Client settings include a new "Scope Handling" dropdown to override the domain-level mode. The grant type architecture was refactored to use a strategy pattern, with `TokenExchangeGrantTypeHandler` implementing the RFC 8693 flow. Token repository interfaces were unified to support both V2 and V4 domains. Temporal validation logic was centralized in `TokenValidationUtils.validateTemporalClaims()` for consistent `exp` and `nbf` checking across all token types.
