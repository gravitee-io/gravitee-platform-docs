# Configure Lightweight JWT with the Management API

You can also set Lightweight JWT in the application's OAuth settings when you patch an application. When the Lightweight JWT settings are absent, Lightweight JWT is disabled.

The Lightweight JWT settings contain the following values:

- Whether Lightweight JWT is enabled. It's disabled by default.
- The claim names kept in the access and refresh tokens, in addition to the reserved claims.
- The claim names kept in the ID token, in addition to the reserved claims.

Both claim lists are empty by default. A listed claim is kept only if AM issues it.

### Behavior of the settings

A patch that carries Lightweight JWT settings behaves as follows:

- **Replacement:** allowlists sent in a patch replace the stored ones. - **Disabling:** a patch that disables Lightweight JWT keeps the allowlists it carries.
- **Duplicate names across lists:** the same claim name can appear in both lists.
- **Dynamic Client Registration:** Lightweight JWT settings aren't part of the Dynamic Client Registration (DCR) contract. Registration updates and client secret renewals keep the stored settings.

### Claim name validation

Claim names are validated even when Lightweight JWT is disabled. A claim name can be at most 128 characters.

An invalid list fails the request with HTTP `400`. Only the first error is reported, and the access and refresh token list is checked before the ID token list.

For the access and refresh token list, you receive one of the following messages:

- `lightweightJwtSettings.allowedAccessTokenClaims must not contain a blank claim name`
- `lightweightJwtSettings.allowedAccessTokenClaims claim names must be at most 128 characters`

For the ID token list, the messages are the same, with `allowedIdTokenClaims` in place of `allowedAccessTokenClaims`.

### Verify the settings

Get the application and confirm that the Lightweight JWT settings match the values you sent.
