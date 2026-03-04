### Overview

Protected Resources support secret management, certificate binding, membership control, and token exchange flows for MCP Server contexts. These features enable secure server-to-server authentication and delegation scenarios while maintaining compatibility with existing OAuth 2.0 workflows. Administrators can manage multiple secrets per resource, bind mTLS certificates, and control access through role-based memberships.

### Key Concepts

#### Protected Resource Secrets

Protected Resources support multiple named secrets with independent lifecycles. Each secret generates a unique `ApplicationSecretSettings` entry and emits lifecycle events (`CREATE`, `RENEW`, `DELETE`). When a secret is deleted, unused settings entries are automatically cleaned up. Secrets are returned in plaintext only at creation or renewal; subsequent API calls return safe representations without the secret value.

#### Certificate Binding

Protected Resources can bind to domain certificates for mTLS authentication. The system validates certificate existence before assignment and prevents deletion of certificates in use by Protected Resources. Certificate validation occurs during resource creation and update operations.

#### Token Exchange for MCP Servers

MCP Servers support RFC 8693 token exchange flows, allowing clients to exchange existing tokens (access, refresh, ID, or JWT) for new access tokens. The exchanged token inherits the subject token's `gis` claim and respects its expiration constraints. Token exchange requires domain-level enablement and restricts MCP Servers to `client_credentials` and token exchange grant types only.

### Prerequisites for Protected Resource Management

- Domain with Protected Resources feature enabled
- For token exchange: `tokenExchangeSettings.enabled = true` in domain configuration
- For certificate binding: Valid certificate uploaded to the domain
- Appropriate permissions: `PROTECTED_RESOURCE[CREATE|UPDATE|DELETE]`, `PROTECTED_RESOURCE_MEMBER[LIST|CREATE|DELETE]`

### OAuth 2.0 Default Settings

Protected Resources automatically receive OAuth 2.0 defaults on creation. These settings are preserved during updates unless explicitly overridden.

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `settings.oauth.grantTypes` | `["client_credentials"]` | Default grant types applied on creation |
| `settings.oauth.responseTypes` | `["code"]` | Default response types |
| `settings.oauth.tokenEndpointAuthMethod` | `"client_secret_basic"` | Default client authentication method |
| `settings.oauth.clientId` | (copied from resource) | Matches the Protected Resource `clientId` |
| `settings.oauth.clientSecret` | (preserved if exists) | Retained from existing settings during updates |

### Token Exchange Settings

Enable token exchange at the domain level to allow MCP Servers to perform token delegation.

| Property | Type | Default Value | Description |
|:---------|:-----|:--------------|:------------|
| `tokenExchangeSettings.enabled` | Boolean | `false` | Enable token exchange for the domain |
| `tokenExchangeSettings.allowedSubjectTokenTypes` | Array | `["urn:ietf:params:oauth:token-type:access_token", "urn:ietf:params:oauth:token-type:refresh_token", "urn:ietf:params:oauth:token-type:id_token", "urn:ietf:params:oauth:token-type:jwt"]` | Permitted subject token types for exchange |

### MCP Server Grant Type Restrictions

When configuring a Protected Resource with `type: "MCP_SERVER"`, only specific grant types and authentication methods are permitted.

| Setting | Allowed Values |
|:--------|:---------------|
| `grantTypes` | `["client_credentials", "urn:ietf:params:oauth:grant-type:token-exchange"]` |
| `tokenEndpointAuthMethod` | `["client_secret_basic", "client_secret_post", "client_secret_jwt"]` |

### Creating a Protected Resource with Secrets

1. POST to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources` with `name`, `clientId`, `type` (e.g., `"MCP_SERVER"`), and `resourceIdentifiers` (at least one unique identifier).
2. The system applies default OAuth settings automatically.
3. To add a secret, POST to `/protected-resources/{id}/secrets` with `{"name": "secret-name"}`.
4. The response includes the plaintext secret value—store it securely, as subsequent API calls return only metadata.
5. Optionally bind a certificate by setting the `certificate` field to a valid certificate ID from the domain.

### Managing Protected Resource Memberships

1. Add members by posting to `/protected-resources/{id}/members` with `{"memberId": "user-or-group-id", "memberType": "USER|GROUP", "role": "role-name"}`.
2. Members inherit permissions based on their assigned role.
3. Remove a member with DELETE `/members/{memberId}`.
4. Retrieve all members with GET `/members` (requires `PROTECTED_RESOURCE_MEMBER[LIST]` permission).
5. View available permissions for the resource using GET `/members/permissions`.

### Performing Token Exchange with an MCP Server

1. Ensure the domain has `tokenExchangeSettings.enabled = true`.
2. Configure the MCP Server with grant types `["client_credentials", "urn:ietf:params:oauth:grant-type:token-exchange"]`.
3. Obtain a subject token from an application (e.g., via password grant).
4. POST to `/oauth/token` with `grant_type=urn:ietf:params:oauth:grant-type:token-exchange`, `subject_token={token}`, and `subject_token_type=urn:ietf:params:oauth:token-type:access_token`.
5. Authenticate the MCP Server using Basic Auth with its `clientId` and secret.
6. The response contains a new access token with `client_id` and `aud` set to the MCP Server's `clientId`, and the `gis` claim preserved from the subject token. The new token's expiration cannot exceed the subject token's remaining lifetime.

### Searching Protected Resources

Search for Protected Resources using GET `/protected-resources?q={query}`. The query supports exact matches on `clientId` or `name`, or wildcard searches using `*` (e.g., `q=mcp*` for case-insensitive prefix matching). Filter results by `type` and paginate with `page` and `size` parameters (default: page 0, size 50). The response returns a paginated list of `ProtectedResourcePrimaryData` objects.

### Restrictions and Validation Rules

- Resource identifiers must be unique within a domain; duplicate identifiers return `InvalidProtectedResourceException`.
- At least one resource identifier is required; empty `resourceIdentifiers` arrays are rejected.
- Feature keys must be unique within a single Protected Resource.
- Certificates in use by Protected Resources cannot be deleted; attempts return `CertificateWithProtectedResourceException` with HTTP 400.
- MCP Servers are restricted to `client_credentials` and token exchange grant types; other grant types (authorization_code, password, implicit, refresh_token) are filtered out in the UI.
- MCP Servers support only `client_secret_basic`, `client_secret_post`, and `client_secret_jwt` authentication methods; methods like `private_key_jwt`, `tls_client_auth`, and `none` are unavailable.
- Token exchange responses never include `id_token` or `refresh_token`, even if the subject token has `openid` scope.
- The `requested_token_type` parameter must be `urn:ietf:params:oauth:token-type:access_token` or omitted; other types are unsupported.
- Token introspection validates audiences by first checking Application `clientId`, then Protected Resource `clientId`, then falling back to resource identifier validation per RFC 8707.
