### Protected Resource Secrets

Protected Resources can maintain multiple client secrets with independent lifecycle management. Each secret inherits domain-level expiration settings and triggers notification events on creation, renewal, and deletion. When a secret is deleted, its associated OAuth settings are automatically removed if no other secrets reference them. At least one secret must exist per Protected Resource.

### MCP Server Context Restrictions

When operating in MCP Server context, Protected Resources are restricted to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types. Token endpoint authentication methods are limited to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`. These restrictions are enforced in the UI and do not apply to standard Application contexts.

### Prerequisites

* Domain with configured OAuth settings
* `PROTECTED_RESOURCE[CREATE]` permission for resource creation
* `PROTECTED_RESOURCE[UPDATE]` permission for secret renewal
* `PROTECTED_RESOURCE_MEMBER[CREATE]` permission for membership management
* Certificate uploaded to domain (optional, for certificate-based authentication)

### Gateway Configuration

#### OAuth Default Settings

When a Protected Resource is created or updated, the following defaults are applied if not explicitly set:

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `grantTypes` | `["client_credentials"]` | Allowed OAuth grant types |
| `responseTypes` | `["code"]` | Allowed OAuth response types |
| `tokenEndpointAuthMethod` | `"client_secret_basic"` | Client authentication method |
| `clientId` | (copied from resource) | OAuth client identifier |
| `clientSecret` | (preserved or generated) | Client secret value |

#### Event Configuration

| Event Type | Actions | Description |
|:-----------|:--------|:------------|
| `PROTECTED_RESOURCE_SECRET` | `CREATE`, `RENEW`, `DELETE` | Lifecycle events for Protected Resource secrets |

### Creating a Protected Resource with Secrets

Create a Protected Resource via `POST /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources`. The system automatically generates an initial secret and applies default OAuth settings (`client_credentials` grant, `client_secret_basic` auth method). To add additional secrets, call `POST /protected-resources/{id}/secrets` with a `name` property—the response includes the plaintext secret value (visible only on creation). Renew an existing secret via `POST /secrets/{secretId}/_renew`, which invalidates the old secret and returns a new value. Delete secrets via `DELETE /secrets/{secretId}`; the system prevents deletion if it would leave the resource with no secrets.

### Associating a Certificate with a Protected Resource

Protected Resources support certificate-based authentication for JWT verification during token introspection. Upload a certificate to the domain, then reference it in the Protected Resource configuration via the `certificate` field (stores certificate ID as `nvarchar(64)` in JDBC, string in MongoDB). When introspecting tokens with an audience matching the Protected Resource's `clientId`, the system uses the associated certificate for signature validation. If no certificate is configured, the system assumes HMAC-signed tokens. Attempting to delete a certificate referenced by any Protected Resource returns `400 Bad Request` with message "You can't delete a certificate with existing protected resources."

### Managing Protected Resource Memberships

Assign users or groups to Protected Resources via `POST /protected-resources/{id}/members` with `memberId`, `memberType` (USER or GROUP), and `role`. List memberships via `GET /members` (requires `PROTECTED_RESOURCE_MEMBER[LIST]`). Remove memberships via `DELETE /members/{member}`. Retrieve flattened permission maps for the current user via `GET /members/permissions`. All membership operations follow hierarchical permission checks: resource-level, domain-level, environment-level, then organization-level.

### Client Configuration

#### Token Exchange Parameters

| Parameter | Allowed Values | Description |
|:----------|:---------------|:------------|
| `subject_token_type` | `urn:ietf:params:oauth:token-type:access_token`, `urn:ietf:params:oauth:token-type:refresh_token`, `urn:ietf:params:oauth:token-type:id_token`, `urn:ietf:params:oauth:token-type:jwt` | Type of subject token for exchange |
| `resource` | (resource identifier URI) | Target Protected Resource identifier |

### Restrictions

* MCP Server contexts allow only `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types
* MCP Server contexts restrict token endpoint auth methods to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`
* At least one secret must exist per Protected Resource (enforced on deletion)
* Certificates referenced by Protected Resources cannot be deleted
* Multi-audience tokens always validate via RFC 8707 resource identifiers (no direct client ID matching)
* Search queries with wildcards use prefix matching only (e.g., `^query.*`)

### Related Changes

The UI's Grant Flows component now filters available grant types and authentication methods when `context === 'McpServer'`, hiding Refresh Token and PKCE configuration sections. Client secret expiration notifications now support Protected Resources alongside Applications, with notification messages formatted as "Client Secret {id} of {resourceType} {name} in domain {domain} expires on {date}". The permission system extends hierarchical checks (resource → domain → environment → organization) to all Protected Resource secret and membership endpoints. Database schemas add a nullable `certificate` column (JDBC: `nvarchar(64)`, MongoDB: string field) to the `protected_resources` table/collection.
