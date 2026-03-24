# Using OAuth 2.0 Token Exchange

## User Binding

User binding resolves domain users from external tokens using EL expressions. Each binding criterion specifies:

- **Attribute**: User attribute to match (e.g., `email`, `username`)
- **Expression**: EL expression evaluated against token claims (e.g., `{#context.attributes['token']['email']}`)

The gateway evaluates all criteria and looks up users by the resulting attribute values. If exactly one user matches, the token is bound to that user. If zero or multiple users match, an error is returned. If user binding is disabled or no criteria are configured, a virtual user is created from token claims.

## Delegation Depth

Delegation depth limits the number of nested `act` claims in the delegation chain. Each delegation adds one level to the depth. The gateway calculates depth by counting nested `act` claims in the subject and actor tokens, then validates against `maxDelegationDepth` (default: 25, range: 1-100). If depth exceeds the limit, the exchange is rejected with an `invalid_grant` error.

## Prerequisites

- OAuth2 client must have `urn:ietf:params:oauth:grant-type:token-exchange` grant type enabled
- Domain must have token exchange enabled via `TokenExchangeSettings.enabled = true`
- Subject token must be a valid JWT issued by the domain or a trusted issuer
- Actor token (if provided) must be a valid JWT issued by the domain or a trusted issuer
- Client must have `client_credentials` or equivalent authentication configured
- For trusted issuers: JWKS endpoint must be accessible or PEM certificate must be valid
