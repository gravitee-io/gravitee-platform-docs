### Overview

Protected Resources are OAuth 2.0 clients that represent backend services or APIs requiring machine-to-machine authentication. This feature extends Protected Resources with secret lifecycle management, certificate-based JWT verification, membership controls, and token exchange capabilities for secure service-to-service communication using client credentials and token exchange flows, with support for MCP (Model Context Protocol) Server contexts.

### Key Concepts

#### Protected Resource Secrets

Protected Resources use client secrets for authentication at the token endpoint. Secrets support expiration policies inherited from domain settings, can be renewed without downtime, and trigger notifications to domain owners before expiration. Each Protected Resource maintains one or more secrets, with at least one active secret required at all times. Secret settings (algorithm configurations) are reused across secrets when possible and cleaned up automatically when no longer referenced.

#### Certificate-Based Token Verification

Protected Resources can reference a certificate for JWT signature verification during token introspection. When a token's audience (`aud`) claim matches a Protected Resource's `clientId`, the introspection service retrieves the associated certificate to validate the token signature. If no certificate is configured, the system assumes HMAC-signed tokens. Certificates can't be deleted while in use by a Protected Resource.

#### Token Exchange for MCP Servers

MCP Servers use the `urn:ietf:params:oauth:grant-type:token-exchange` grant type to exchange subject tokens (access, refresh, ID, or JWT tokens) for new access tokens. The domain's `tokenExchangeSettings.allowedSubjectTokenTypes` controls which token types are accepted. The issued token inherits the subject token's `gis` claim and has an expiration no longer than the subject token's remaining lifetime. MCP Server contexts restrict available grant types to `client_credentials` and token exchange, and limit token endpoint authentication methods to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`.

### Prerequisites for Secret Management

* Access Management domain with OAuth 2.0 enabled
* Appropriate permissions: `PROTECTED_RESOURCE` (LIST, CREATE, UPDATE, DELETE)
* For secret expiration notifications: domain owners configured

### Prerequisites for Certificate-Based Verification

See [Prerequisites for Certificate-Based Verification](#prerequisites-for-certificate-based-verification) above for details.
### Prerequisites for Token Exchange

See [Prerequisites for Token Exchange](#prerequisites-for-token-exchange) above for details.
### Prerequisites for Membership Management

See [Prerequisites for Membership Management](#prerequisites-for-membership-management) above for details.
### Gateway Configuration

#### Database Schema

| Column | Table | Type | Nullable | Description |
|:-------|:------|:-----|:---------|:------------|
| `certificate` | `protected_resources` | `nvarchar(64)` | true | Certificate ID for JWT signature verification |

#### OAuth 2.0 Default Settings

| Setting | Default Value | Description |
|:--------|:--------------|:------------|
| `grantTypes` | `["client_credentials"]` | Default grant type for Protected Resources |
| `responseTypes` | `["code"]` | Default response type |
| `tokenEndpointAuthMethod` | `client_secret_basic` | Default authentication method |
| `clientId` | `<resource.clientId>` | Copied from resource |
| `clientSecret` | `<preserved from existing>` | Preserved on update if already set |

#### Event Types

| Property | Type | Value | Description |
|:---------|:-----|:------|:------------|
| `PROTECTED_RESOURCE_SECRET` | Enum | CREATE, RENEW, DELETE | Event type for Protected Resource secret lifecycle actions |

### Configuring Token Exchange

1. Enable token exchange at the domain level by setting `tokenExchangeSettings.enabled` to `true` and configuring `allowedSubjectTokenTypes`.
2. Create or update a Protected Resource with the `urn:ietf:params:oauth:grant-type:token-exchange` grant type.
3. For MCP Server contexts, the system automatically restricts grant types to `client_credentials` and token exchange, and limits token endpoint authentication methods to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`.
