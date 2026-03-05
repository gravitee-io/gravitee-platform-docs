### Overview

Protected Resources in Gravitee Access Management participate in OAuth token introspection workflows and enforce MCP Server-specific OAuth constraints. This feature enables API platform administrators to manage resource servers and OAuth clients with full lifecycle controls, including secret rotation, certificate-based authentication, and membership management.

### What are Protected Resources?

Protected Resources represent resource servers in AM's OAuth architecture. Each Protected Resource maintains one or more client secrets for authentication and can be configured with certificates for JWT verification. Protected Resources use the same secret management patterns as Applications but operate under different OAuth constraints when used in MCP Server contexts.

### Token Introspection with Protected Resources

Token introspection validates audiences against both Applications and Protected Resources. The validation logic depends on the number of audiences in the token:

**Single-audience tokens:**
1. Check the Application registry for a matching `clientId`
2. If not found, check the Protected Resource registry
3. If still not found, fall back to RFC 8707 resource identifier validation

**Multi-audience tokens:**
- Always validate via RFC 8707 resource identifiers

When a Protected Resource has a certificate configured, the system uses it for JWT verification. If no certificate is configured, the system assumes HMAC signing.

### MCP Server Context Restrictions

Protected Resources operating in MCP Server context are restricted to specific grant types and authentication methods:

**Allowed grant types:**
- `client_credentials`
- `urn:ietf:params:oauth:grant-type:token-exchange`

**Allowed token endpoint authentication methods:**
- `client_secret_basic`
- `client_secret_post`
- `client_secret_jwt`

These restrictions prevent MCP Servers from using user-facing flows such as `authorization_code` or `password`.

### OAuth Default Settings

When you create a Protected Resource, AM applies the following OAuth settings automatically if you don't provide custom values:

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `grantTypes` | `["client_credentials"]` | Default grant types for Protected Resources |
| `responseTypes` | `["code"]` | Default response types |
| `tokenEndpointAuthMethod` | `"client_secret_basic"` | Default authentication method |
| `clientId` | (copied from resource) | Matches the Protected Resource's client ID |
| `clientSecret` | (preserved if exists) | Retained from existing settings during updates |

You can override these defaults by providing custom `settings` in the request body when creating a Protected Resource.

### Secret Lifecycle Events

Protected Resource secret lifecycle events use the `PROTECTED_RESOURCE_SECRET` event type with the following actions:

- `CREATE` — Secret creation
- `RENEW` — Secret renewal
- `DELETE` — Secret deletion

These events trigger notification registration and audit logging. Secret expiration notifications are registered immediately based on domain-level expiration policies.

### Prerequisites

Before managing Protected Resources, ensure you have:

- A configured Gravitee Access Management domain
- `PROTECTED_RESOURCE[CREATE]` permission for resource creation
- `PROTECTED_RESOURCE[UPDATE]` permission for secret renewal
- `PROTECTED_RESOURCE_MEMBER[CREATE]` permission for membership management
- Domain-level `SecretExpirationSettings` configured (inherited by Protected Resource secrets)

