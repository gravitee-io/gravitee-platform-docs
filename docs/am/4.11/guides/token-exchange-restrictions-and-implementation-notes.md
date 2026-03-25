# Token Exchange Restrictions and Implementation Notes

## Restrictions

Token exchange in enforces the following constraints:

- **No refresh tokens**: Token exchange does not issue refresh tokens (`supportRefreshToken=false`).
- **Delegation depth limit**: Maximum delegation depth is configurable (range 1-100) with a default of 25 levels.
- **Allowed token types**: Requested token types are limited to `ACCESS_TOKEN` and `ID_TOKEN`.
- **JWT validation**: Subject and actor tokens must be valid JWTs with non-expired `exp` claims and valid `nbf` claims.
- **Impersonation control**: Impersonation requires `allowImpersonation=true` at the domain level.
- **Delegation control**: Delegation requires `allowDelegation=true` at the domain level.
- **Trusted issuer verification**: JWKS_URL resolution failures or PEM certificate parsing errors result in token verification exceptions.
- **User binding**: User binding requires exactly one matching domain user. Zero or multiple matches cause the request to fail.
- **Scope validation**: Scope validation in DOWNSCOPING mode rejects requests if requested scopes exceed allowed scopes.
- **Grant type requirement**: Clients must have the `TOKEN_EXCHANGE` grant type enabled.
- **Default state**: Token exchange is disabled by default at the domain level (`enabled=false`).
