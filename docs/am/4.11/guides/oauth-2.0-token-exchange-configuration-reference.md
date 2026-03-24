# OAuth 2.0 Token Exchange Configuration Reference

## Gateway Configuration

### Token Exchange Settings

Configure token exchange behavior at the domain level. All properties are nested under `TokenExchangeSettings`.

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `enabled` | boolean | `false` | Enable RFC 8693 OAuth 2.0 Token Exchange |
| `allowedSubjectTokenTypes` | Set<String> | `[ACCESS_TOKEN, REFRESH_TOKEN, ID_TOKEN]` | Token types accepted as `subject_token` |
| `allowedRequestedTokenTypes` | Set<String> | `[ACCESS_TOKEN]` | Token types that can be requested via `requested_token_type` |
| `allowImpersonation` | boolean | `true` | Allow token exchange without `actor_token` |
| `allowDelegation` | boolean | `false` | Allow token exchange with `actor_token` |
| `allowedActorTokenTypes` | Set<String> | `[ACCESS_TOKEN, REFRESH_TOKEN, ID_TOKEN]` | Token types accepted as `actor_token` for delegation |
| `maxDelegationDepth` | int | `25` | Maximum depth of nested `act` claims (range: 1-100) |
| `trustedIssuers` | List<TrustedIssuer> | `[]` | External JWT issuers trusted for token exchange |
| `tokenExchangeOAuthSettings.scopeHandling` | enum | `DOWNSCOPING` | Scope handling mode: `DOWNSCOPING` or `PERMISSIVE` |

### Trusted Issuer Configuration

Each trusted issuer entry configures an external JWT issuer. Multiple issuers can be configured, but issuer URLs must be unique.

| Property | Type | Description |
|:---------|:-----|:------------|
| `issuer` | String | Issuer URL (must match JWT `iss` claim exactly) |
| `keyResolutionMethod` | enum | `JWKS_URL` or `PEM` |
| `jwksUri` | String | JWKS endpoint URL (required when method is `JWKS_URL`) |
| `certificate` | String | PEM-encoded certificate (required when method is `PEM`) |
| `scopeMappings` | Map\<String, String> | External scope → domain scope mappings |
| `userBindingEnabled` | boolean | Enable user binding via EL expressions |
| `userBindingCriteria` | List\<UserBindingCriterion> | EL expressions to resolve domain users |

### User Binding Criteria

Each criterion specifies how to resolve a domain user from token claims.

| Property | Type | Description |
|:---------|:-----|:------------|
| `attribute` | String | User attribute to match (e.g., `email`, `username`) |
| `expression` | String | EL expression evaluated against token claims (e.g., `{#context.attributes['token']['email']}`) |
