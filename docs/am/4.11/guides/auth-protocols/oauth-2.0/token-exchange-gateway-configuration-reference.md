# Token Exchange Gateway Configuration Reference

## Gateway Configuration

### Token Exchange Settings

Configure token exchange behavior at the domain level using the following properties:

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `enabled` | boolean | `false` | Enable RFC 8693 OAuth 2.0 Token Exchange |
| `allowedSubjectTokenTypes` | Set\<String> | `[ACCESS_TOKEN, REFRESH_TOKEN, ID_TOKEN]` | Token types accepted as `subject_token` |
| `allowedRequestedTokenTypes` | Set\<String> | `[ACCESS_TOKEN]` | Token types that can be requested via `requested_token_type` |
| `allowImpersonation` | boolean | `true` | Allow token exchange without `actor_token` (impersonation) |
| `allowDelegation` | boolean | `false` | Allow token exchange with `actor_token` (delegation) |
| `allowedActorTokenTypes` | Set\<String> | `[ACCESS_TOKEN, REFRESH_TOKEN, ID_TOKEN]` | Token types accepted as `actor_token` for delegation |
| `maxDelegationDepth` | int | `25` | Maximum depth of nested `act` claims (range: 1-100) |
| `trustedIssuers` | List\<TrustedIssuer> | `[]` | External JWT issuers trusted for token exchange |

### OAuth Settings

Configure scope handling mode under OAuth settings:

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `tokenExchangeOAuthSettings.scopeHandling` | enum | `DOWNSCOPING` | Scope handling mode: `DOWNSCOPING` or `PERMISSIVE` |

### Trusted Issuer Configuration

Each trusted issuer requires the following properties. See [Managing Trusted Issuers](../token-exchange/managing-trusted-issuers.md) for step-by-step configuration instructions.

| Property | Type | Description |
|:---------|:-----|:------------|
| `issuer` | String | Issuer URL (must match JWT `iss` claim) |
| `keyResolutionMethod` | enum | `JWKS_URL` or `PEM` |
| `jwksUri` | String | JWKS endpoint URL (required when method is `JWKS_URL`) |
| `certificate` | String | PEM-encoded certificate (required when method is `PEM`) |
| `scopeMappings` | Map\<String, String> | Map external scopes to domain scopes (e.g., `external:read` → `profile`) |
| `userBindingEnabled` | boolean | Enable user binding via EL expressions |
| `userBindingCriteria` | List\<UserBindingCriterion> | EL expressions to match external JWT to domain user |

User binding criteria consist of attribute/expression pairs:

| Property | Type | Description |
|:---------|:-----|:------------|
| `attribute` | String | User attribute to match (e.g., `email`, `username`) |
| `expression` | String | EL expression evaluated against JWT claims (e.g., `{#token['email']}`) |


### Delegation Chain Claims

See [Delegation Chain Claims](../token-exchange/oauth-2.0-token-exchange-overview.md#delegation-chain-claims) in the Token Exchange Overview for details on the `act` claim structure.
