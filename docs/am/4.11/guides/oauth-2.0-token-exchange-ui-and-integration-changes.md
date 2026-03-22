# OAuth 2.0 Token Exchange: UI and Integration Changes

## Related Changes

### OAuth 2.0 Client Configuration

The OAuth 2.0 client configuration UI includes a new grant type selection: `urn:ietf:params:oauth:grant-type:token-exchange`. Clients must enable this grant type to use token exchange.

### Domain Settings

Domain settings include a dedicated token exchange section with the following controls:

* **Impersonation and delegation mode toggles:** Enable or disable impersonation and delegation.
* **Token type multi-select dropdowns:** Configure allowed subject, requested, and actor token types.
* **Delegation depth input:** Set the maximum delegation depth (1-100).
* **Scope handling mode radio buttons:** Select between `DOWNSCOPING` and `PERMISSIVE` modes.

### Trusted Issuers UI

The trusted issuers UI provides a form for adding external JWT issuers. The form includes:

* **Autocomplete for domain scope selection:** Simplifies scope mapping configuration by suggesting available domain scopes.
* **User binding criteria:** Define EL expressions to resolve external subjects to domain users.

### Audit Logging

Audit logs capture the following parameters for all token exchange requests:

* `SUBJECT_TOKEN`
* `SUBJECT_TOKEN_TYPE`
* `REQUESTED_TOKEN_TYPE`
* `ACTOR_TOKEN`
* `ACTOR_TOKEN_TYPE`

### Policy Integration

Token exchange integrates with existing `PRE_TOKEN` and `POST_TOKEN` policy execution points. Administrators can apply custom logic during token issuance by configuring policies at these execution points.
