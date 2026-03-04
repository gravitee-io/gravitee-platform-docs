### Prerequisites

Before configuring Protected Resources, ensure you have:

* Access Management 4.11.0 or later
* `PROTECTED_RESOURCE[CREATE]`, `PROTECTED_RESOURCE[UPDATE]`, `PROTECTED_RESOURCE[DELETE]` permissions for secret management
* `PROTECTED_RESOURCE_MEMBER[LIST]`, `PROTECTED_RESOURCE_MEMBER[CREATE]`, `PROTECTED_RESOURCE_MEMBER[DELETE]` permissions for membership operations
* Valid domain-scoped certificate if using certificate-based authentication

### OAuth 2.0 Default Settings

When creating or updating a Protected Resource, the system applies default OAuth settings if the `settings.oauth` field is null or incomplete. These defaults ensure functional client credentials flows without explicit configuration.

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `settings.oauth.grantTypes` | `["client_credentials"]` | Default grant types |
| `settings.oauth.responseTypes` | `["code"]` | Default response types |
| `settings.oauth.tokenEndpointAuthMethod` | `client_secret_basic` | Default authentication method |
| `settings.oauth.clientId` | (copied from `clientId`) | Synchronized with resource client ID |
| `settings.oauth.clientSecret` | (preserved if exists) | Retained from existing settings on update |

### Event Configuration

Secret lifecycle operations emit domain events for audit and synchronization purposes.

| Event Type | Action | Description |
|:-----------|:-------|:------------|
| `PROTECTED_RESOURCE_SECRET` | `CREATE` | Emitted when a new secret is generated |
| `PROTECTED_RESOURCE_SECRET` | `RENEW` | Emitted when an existing secret is renewed |
| `PROTECTED_RESOURCE_SECRET` | `DELETE` | Emitted when a secret is deleted |

### Creating a Protected Resource with Secrets

1. Create a Protected Resource via `POST /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources` with a JSON body containing `name`, `clientId`, `type`, and optional `certificate` field. The system validates certificate existence if provided and applies default OAuth settings.
2. Generate a secret via `POST /protected-resources/{id}/secrets` with `{"name": "secret-name"}`. The response includes the plaintext secret value, which is never returned again.
3. Configure the Protected Resource as an audience in token exchange or client credentials flows.
4. Use the `clientId` and secret for authentication at the token endpoint.

### Renewing or Deleting Secrets

To renew a secret, call `POST /protected-resources/{id}/secrets/{secretId}/_renew`. The response contains the new plaintext value. To delete a secret, call `DELETE /protected-resources/{id}/secrets/{secretId}`. The system removes the secret from `clientSecrets` and removes the associated `secretSettings` entry only if no other secret references it. List all secrets (without plaintext values) via `GET /protected-resources/{id}/secrets`.

### Managing Protected Resource Memberships

Add members via `POST /protected-resources/{id}/members` with `{"memberId": "user-or-group-id", "memberType": "USER|GROUP", "role": "role-name"}`. List members via `GET /protected-resources/{id}/members` and retrieve flattened permissions via `GET /protected-resources/{id}/members/permissions`. Remove members via `DELETE /protected-resources/{id}/members/{memberId}`. Membership operations require `PROTECTED_RESOURCE_MEMBER` permissions scoped to the resource.

### Searching Protected Resources

Query Protected Resources via `GET /protected-resources?q={query}`. If the `q` parameter is present, the system searches `name` and `clientId` fields (case-insensitive) with wildcard support (`*` matches any characters). For example, `?q=client*` matches resources with names or client IDs starting with "client". If `q` is absent, all resources filtered by type are returned. Results are paginated and include `id`, `clientId`, `name`, `description`, `type`, `resourceIdentifiers`, `certificate`, `settings`, `secretSettings`, `features`, and `updatedAt`.

### Client Configuration

Clients authenticating as Protected Resources use the following properties:

| Property | Description | Example |
|:---------|:------------|:--------|
| `client_id` | Protected Resource `clientId` | `mcp-server-123` |
| `client_secret` | Secret value from creation or renewal response | `a1b2c3d4...` |
| `token_endpoint_auth_method` | Must match `settings.oauth.tokenEndpointAuthMethod` | `client_secret_basic` |
| `grant_type` | `client_credentials` or `urn:ietf:params:oauth:grant-type:token-exchange` | `client_credentials` |

### Restrictions

* Protected Resources with type `MCP_SERVER` support only `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types
* Token endpoint authentication for MCP Server context is limited to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`
* Certificate-based authentication methods (`private_key_jwt`, `tls_client_auth`, `self_signed_tls_client_auth`) and `none` are excluded for MCP Server context
* Certificates can't be deleted if referenced by any Protected Resource. Deletion attempts return HTTP 400 with message: `"You can't delete a certificate with existing protected resources."`
* Resource identifiers must be unique within a domain (validated on creation and update)
* Feature keys must be unique within a Protected Resource
* Plaintext secret values are returned only once at creation or renewal
* Secret settings entries are shared across secrets via `settingsId` and deleted only when no secrets reference them
* Token introspection with multiple audiences always uses RFC 8707 resource identifier validation. Client ID matching is skipped. If the audience is not found, the system throws `InvalidTokenException` with message: `"Client or resource not found: {aud}"`
* When updating a Protected Resource, `settings.oauth.clientSecret` is preserved if null in the request
* Feature timestamps are retained from the previous version on update

