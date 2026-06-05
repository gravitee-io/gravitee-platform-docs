# SPIFFE Workload Identity Restrictions and Related Changes

## Restrictions

- **SPIFFE Prefix Match** is only allowed for Hosted Delegated and Autonomous agent applications. User-Embedded agents must use Exact Match.
- SPIFFE subjects using Prefix Match must end with `/` to ensure prefix matching occurs at path boundaries.
- CIMD clients cannot use secret-based token endpoint authentication methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`). Only public clients or certificate-based authentication are supported.
- CIMD document fetches are bounded by `fetchTimeoutMs` (domain-level setting). Large documents may fail if the timeout is too low.
- CIMD responses are capped at `maxResponseSizeKb` (domain-level setting). Documents exceeding this limit are rejected.
- SPIFFE JWT-SVID lifetime (`exp - iat`) must not exceed `maxJwtLifetimeSeconds` (domain-level setting). SVIDs exceeding this value are rejected.
- JWKS URLs resolving to private, loopback, link-local, or any-local addresses are rejected unless the domain sets `allowPrivateIpAddress=true`.
- Agent applications forbid `implicit`, `password`, and `urn:ietf:params:oauth:grant-type:uma-ticket` grant types.
- User-Embedded agents cannot use the `client_credentials` grant type.
- Autonomous agents cannot use the `authorization_code` or `refresh_token` grant types.
- User-Embedded and Hosted Delegated agents require at least one redirect URI.
- The SPIRE local-stack overlay (`docker-compose.spire.yml`) uses HTTP for the OIDC provider. Production deployments must serve over TLS.

## Related Changes

The following changes apply to AM 4.12:

### Management Console Updates

The Management Console now includes a dedicated **Agents** navigation entry with its own list view and creation wizard, separate from the standard Applications area. The Applications list excludes agent applications.

Agent applications can now be marked as DCR/CIMD registration templates. The earlier restriction preventing this has been removed.

### Token Claims

The `act.sub` claim in issued tokens now carries the agent instance ID for User-Embedded and Hosted Delegated agents when an instance ID is known. This enables downstream systems to track the acting agent instance in delegation chains.

### Database Migration

{% hint style="warning" %}
Database migration is required when upgrading to AM 4.12.
{% endhint %}

The following database changes are applied during migration:

* A new `sub_type` column is added to the `applications` table
* A new `trust_domains` table is created to store trust domain configurations

