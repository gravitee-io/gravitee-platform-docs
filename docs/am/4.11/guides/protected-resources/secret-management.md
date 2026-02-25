## Overview

Protected Resources in Gravitee Access Management support full client secret lifecycle management—creation, renewal, deletion, and expiration notifications. This feature enables Protected Resources (such as MCP Servers) to act as OAuth2 clients in token introspection and authentication flows, bringing them to parity with Applications. API platform administrators can configure Protected Resources with OAuth2 settings, assign certificates for JWT verification, and search resources by name or client ID.

## Key Concepts

### Protected Resource as OAuth2 Client

Protected Resources authenticate as OAuth2 clients using their `clientId` during token introspection and authentication flows. When a JWT's audience claim matches a Protected Resource's client ID, the introspection service validates it alongside Applications. This enables Protected Resources to participate in standard OAuth2 workflows, including client credentials grants and token exchange.

### Secret Lifecycle Management

Secrets for Protected Resources follow the same lifecycle as Application secrets: create, renew, and delete operations trigger domain events (`CREATE`, `RENEW`, `DELETE`) that drive expiration notifications. Secret settings (such as expiration policies) are reused across multiple secrets and cleaned up only when no longer referenced. Secrets inherit domain-level expiration settings automatically.

### Certificate-Based JWT Verification

Protected Resources can reference a certificate ID to enable JWT signature verification during token introspection. When a certificate is assigned, the introspection service uses it to validate tokens signed with the corresponding private key. Certificates can't be deleted if still referenced by a Protected Resource.

## Prerequisites

Before managing Protected Resource secrets and OAuth2 configuration, ensure the following:

- Access Management domain configured
- User with permissions to manage Protected Resources

- For certificate-based verification: certificate uploaded to the domain
- For secret expiration notifications: domain-level expiration settings configured

## Gateway Configuration

### OAuth2 Default Settings

When creating or updating a Protected Resource without explicit OAuth2 settings, the following defaults are applied:

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `settings.oauth.grantTypes` | `["client_credentials"]` | Default grant type for Protected Resources |
| `settings.oauth.responseTypes` | `["code"]` | Default response type |
| `settings.oauth.tokenEndpointAuthMethod` | `"client_secret_basic"` | Default authentication method |
| `settings.oauth.clientId` | Copied from `resource.clientId` | OAuth2 client identifier |
| `settings.oauth.clientSecret` | Preserved from existing resource | Preserved during updates if already set |

### Protected Resource Schema

Protected Resources accept the following fields:

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `certificate` | String (optional) | Certificate ID for JWT signature verification | `"cert-abc123"` |
| `settings.oauth.grantTypes` | Array of strings | Allowed OAuth2 grant types | `["client_credentials"]` |
| `settings.oauth.responseTypes` | Array of strings | Allowed response types | `["code"]` |
| `settings.oauth.tokenEndpointAuthMethod` | String | Client authentication method | `"client_secret_basic"` |
| `settings.oauth.clientId` | String | OAuth2 client identifier | `"resource-client-001"` |
| `settings.oauth.clientSecret` | String | OAuth2 client secret | `"secret-value"` |

### MCP Server Token Endpoint Auth Methods

For Protected Resources in MCP Server context, only the following authentication methods are allowed:

- `client_secret_basic`
- `client_secret_post`
- `client_secret_jwt`

## Creating a Protected Resource with OAuth2 Settings

To create a Protected Resource with custom OAuth2 settings:

1. Send a POST request to `/organizations/{org}/environments/{env}/domains/{domain}/protected-resources`.
2. Include a JSON body with the `settings.oauth` object.

If you omit the `settings` field, the system applies defaults: `client_credentials` grant type, `code` response type, and `client_secret_basic` authentication method. The `clientId` is copied from the resource's `clientId` field. User-provided settings in the request body are preserved and merged with defaults for any missing fields.

To enable certificate-based JWT verification, include the `certificate` field with a valid certificate ID from the domain.

## Managing Secrets

### Creating a Secret

To create a secret for a Protected Resource:

1. Send a POST request to `/organizations/{org}/environments/{env}/domains/{domain}/protected-resources/{id}/secrets`.
2. The secret inherits the domain's expiration settings.
3. A `CREATE` event is triggered.

### Renewing a Secret

To renew an existing secret:

1. Send a POST request to `/organizations/{org}/environments/{env}/domains/{domain}/protected-resources/{id}/secrets/{secretId}/_renew`.
2. The system generates a new secret value.
3. A `RENEW` event is triggered.

### Deleting a Secret

To delete a secret:

1. Send a DELETE request to `/organizations/{org}/environments/{env}/domains/{domain}/protected-resources/{id}/secrets/{secretId}`.
2. If the secret's settings are still referenced by other secrets, the settings are preserved.
3. If no other secrets reference the settings, they are removed.

All secret operations are managed by the `ProtectedResourceSecretManager` event listener, which handles expiration notifications.

## Searching Protected Resources

To search Protected Resources by name or client ID:

1. Send a GET request to `/organizations/{org}/environments/{env}/domains/{domain}/protected-resources?q={query}`.
2. The search is case-insensitive and supports exact matches on `clientId` and `name` fields.
3. Use the wildcard character (`*`) for partial matching.

**Examples:**

- `?q=mcp*` returns all resources whose name or client ID starts with "mcp"
- `?q=resource-client-001` returns resources with exact match on name or client ID

Combine with `type`, `page`, and `size` parameters for filtered pagination.

## Token Introspection with Protected Resources

During token introspection, the service validates the JWT's audience claim against both Applications and Protected Resources:

1. If the audience is a single value:
    - The service first checks if it matches an Application's client ID.
    - If no match, the service checks Protected Resources.
    - If still no match, the service validates it as a resource identifier per RFC 8707.
2. If the audience contains multiple values, all are validated as resource identifiers.
3. When a Protected Resource is matched, the service returns its certificate ID (or an empty string for HMAC-signed tokens) to enable signature verification.
4. If no valid audience is found, introspection fails with an `InvalidTokenException`.

## Architecture Notes

### Event-Driven Secret Expiration

Secret lifecycle events (`CREATE`, `RENEW`, `DELETE`) are published to the domain event bus and consumed by the `ProtectedResourceSecretManager` listener. This listener schedules expiration notifications using the `ClientSecretNotifierService`, which was extended to support Protected Resources. The event-driven design ensures that secret expiration warnings are sent consistently across all secret types.

### OAuth2 Auth Provider Fallback Chain

The `OAuth2AuthProviderImpl.decodeToken()` method implements a fallback chain when resolving the audience claim: it first attempts to find an Application by client ID, then falls back to Protected Resources, and finally returns an error if neither is found. This ensures backward compatibility while enabling Protected Resources to participate in OAuth2 flows without breaking existing Application-based authentication.

### Secret Settings Reuse

Secret settings (such as expiration policies) are stored separately and referenced by multiple secrets. When a secret is deleted, the service checks if its settings are still in use by other secrets. If not, the settings are removed to prevent orphaned configuration. This design reduces storage overhead and ensures consistent expiration behavior across related secrets.

## Restrictions

