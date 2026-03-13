### Domain Token Exchange Settings

Configure token exchange at the security domain level by navigating to **Settings > OAuth 2.0 > Token Exchange**.

| Property | Description | Example |
|:---------|:------------|:--------|
| `enabled` | Enable RFC 8693 token exchange for this domain | `true` |
| `allowedSubjectTokenTypes` | Token types accepted as `subject_token` | `ACCESS_TOKEN`, `REFRESH_TOKEN`, `ID_TOKEN` |
| `allowedRequestedTokenTypes` | Token types that can be requested via `requested_token_type` | `ACCESS_TOKEN`, `ID_TOKEN` |
| `allowImpersonation` | Allow token exchange without `actor_token` | `true` |
| `allowDelegation` | Allow token exchange with `actor_token` (adds `act` claim) | `false` |
| `allowedActorTokenTypes` | Token types accepted as `actor_token` when delegation enabled | `ACCESS_TOKEN`, `REFRESH_TOKEN`, `ID_TOKEN` |
| `maxDelegationDepth` | Maximum depth of nested `act` claims (1-100) | `25` |

### Trusted Issuer Configuration

Navigate to **Settings > OAuth 2.0 > Token Exchange > Trusted Issuers** to add external identity providers whose tokens can be exchanged.

| Property | Description | Example |
|:---------|:------------|:--------|
| `issuer` | Issuer URL (must match JWT `iss` claim) | `https://accounts.google.com` |
| `keyResolutionMethod` | How to resolve signing keys | `JWKS_URL` or `PEM` |
| `jwksUri` | JWKS endpoint URL (when method is `JWKS_URL`) | `https://accounts.google.com/.well-known/jwks.json` |
| `certificate` | PEM-encoded certificate (when method is `PEM`) | `-----BEGIN CERTIFICATE-----...` |
| `scopeMappings` | Map external scopes to domain scopes | `{"https://www.googleapis.com/auth/userinfo.email": "email"}` |
| `userBindingEnabled` | Enable user binding via EL expressions | `true` |
| `userBindingCriteria` | EL expressions to resolve external subject to domain user | See below |

#### User Binding Criteria

| Property | Description | Example |
|:---------|:------------|:--------|
| `attribute` | User attribute to match | `email`, `username` |
| `expression` | EL expression evaluated against token claims | `{#token['email']}` |

User binding resolves external token subjects to domain users. If zero users match the criteria, the request fails with "No user found matching binding criteria". If multiple users match, the request fails with "Multiple users found matching binding criteria". If `userBindingEnabled=false` or no criteria are configured, a virtual user is created from token claims.

