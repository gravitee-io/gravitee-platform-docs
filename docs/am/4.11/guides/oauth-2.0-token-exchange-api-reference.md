# OAuth 2.0 Token Exchange - API Reference

## Client-Level Scope Handling

Override scope handling mode at the client level.

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `inherited` | boolean | `true` | Inherit scope handling from domain settings |
| `scopeHandling` | Enum | `DOWNSCOPING` | `DOWNSCOPING` or `PERMISSIVE` |

## Restrictions

- `subject_token` and `subject_token_type` are required; omitting either returns `subject_token is required` or `subject_token_type is required`
- `subject_token_type` must be in `allowedSubjectTokenTypes`; unsupported types return `Unsupported subject_token_type: <type>`
- `requested_token_type` must be `ACCESS_TOKEN` or `ID_TOKEN` and in `allowedRequestedTokenTypes`; unsupported types return `Unsupported requested_token_type: <type>` or `requested_token_type not allowed: <type>`
- If `requested_token_type` is omitted and `ACCESS_TOKEN` is not allowed, the error is `requested_token_type is required when access_token is not allowed`
- Impersonation requires `allowImpersonation` enabled; otherwise returns `Impersonation is not allowed`
- Delegation requires `allowDelegation` enabled and `actor_token` + `actor_token_type` provided; otherwise returns `Delegation is not allowed`
- `actor_token_type` must be in `allowedActorTokenTypes` when delegation is used
- Delegation depth is capped at `maxDelegationDepth` (1-100, default 25); exceeding this returns `Delegation depth exceeds maximum allowed depth of <maxDelegationDepth>`
- Requested scopes must be a subset of allowed scopes; otherwise returns `Requested scope is not allowed`
- Expired tokens (`exp` claim in the past) return `<tokenType> has expired`
- Tokens not yet valid (`nbf` claim in the future) return `<tokenType> is not yet valid`
- Domain-issued tokens are checked for revocation; revoked tokens return `token has been revoked`
- Trusted issuer validation requires `jwksUri` for `JWKS_URL` method or `certificate` for `PEM` method; missing values throw `JWKS URI is required for JWKS_URL method` or `Certificate is required for PEM method`
- User binding with zero matches returns `No user found matching binding criteria`; multiple matches return `Multiple users found matching binding criteria`

## Related Changes

Token exchange introduces audit logging for all token exchange parameters, including `GRANT_TYPE`, `REQUESTED_TOKEN_TYPE`, `SUBJECT_TOKEN`, `SUBJECT_TOKEN_TYPE`, `ACTOR_TOKEN`, `ACTOR_TOKEN_TYPE`, `SCOPE`, and `RESOURCE`. The token repository has been unified into a single `TokenRepository` interface, replacing separate access and refresh token repositories, with a backward-compatible adapter for existing code. The UI includes a Token Exchange settings page for enabling the feature and configuring allowed token types, impersonation, delegation, and delegation depth. A Trusted Issuers management page allows administrators to add, edit, and delete trusted issuers, configure key resolution methods, map external scopes to domain scopes (with autocomplete), and define user binding criteria via EL expressions. The grant type architecture has been refactored to use a `GrantStrategy` interface with a `StrategyGranterAdapter` for backward compatibility, and `TokenCreationRequest` and `GrantData` types encapsulate token creation data.
