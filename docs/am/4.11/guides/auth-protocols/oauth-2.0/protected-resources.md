### Overview

Protected Resources in Gravitee Access Management enable secure token introspection workflows and OAuth-based authorization. A Protected Resource represents an API or service that validates access tokens issued by AM. Unlike Applications, which request tokens, Protected Resources verify tokens and enforce access policies.

When you create a Protected Resource, AM automatically applies default OAuth settings to enable token introspection. These settings include grant types, response types, and authentication methods. Protected Resources can maintain multiple client secrets with independent lifecycle management and support certificate-based authentication for JWT verification.

### Protected Resources vs Applications

| Aspect | Protected Resource | Application |
|:-------|:------------------|:------------|
| Primary role | Validates access tokens | Requests access tokens |
| Token introspection | Performs introspection | Subject of introspection |
| Default grant type | `client_credentials` | Varies by use case |
| Secret management | Multiple secrets supported | Multiple secrets supported |
| Certificate support | Optional, for JWT verification | Optional, for client authentication |

### Default OAuth Settings

When you create or update a Protected Resource, AM applies the following defaults if not explicitly set:

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `grantTypes` | `["client_credentials"]` | Allowed OAuth grant types |
| `responseTypes` | `["code"]` | Allowed OAuth response types |
| `tokenEndpointAuthMethod` | `"client_secret_basic"` | Client authentication method |
| `clientId` | `resource.getClientId()` | Copied from resource client ID |
| `clientSecret` | (preserved from existing) | Preserved from existing settings if present |

These defaults ensure that Protected Resources can immediately participate in token introspection workflows without additional configuration.

### MCP Server Context Restrictions

When operating in MCP Server context, Protected Resources are restricted to specific grant types and authentication methods:

**Allowed grant types:**
- `client_credentials`
- `urn:ietf:params:oauth:grant-type:token-exchange`

**Allowed authentication methods:**
- `client_secret_basic`
- `client_secret_post`
- `client_secret_jwt`

These restrictions do not apply to standard Application contexts. The UI enforces these restrictions automatically when you configure a Protected Resource in MCP Server context.

### Secret Management

Protected Resources can maintain multiple client secrets with independent lifecycle management. Each secret inherits domain-level expiration settings and triggers notification events on creation, renewal, and deletion.

**Secret lifecycle rules:**
- At least one secret must exist per Protected Resource
- When you delete a secret, AM automatically removes its associated OAuth settings if no other secrets reference them
- Secrets inherit domain-level `SecretExpirationSettings`
- AM registers expiration notifications for each secret

**Secret operations:**
- **Create**: Generates a new secret and registers expiration notification
- **Renew**: Unregisters the old secret notification and registers a new notification
- **Delete**: Unregisters expiration notification and removes the secret

### Prerequisites

Before you create or configure a Protected Resource, ensure you have:

- A domain with configured OAuth settings
- `PROTECTED_RESOURCE[CREATE]` permission for resource creation
- `PROTECTED_RESOURCE[UPDATE]` permission for secret renewal
- `PROTECTED_RESOURCE_MEMBER[CREATE]` permission for membership management
- (Optional) A certificate uploaded to the domain for certificate-based authentication
