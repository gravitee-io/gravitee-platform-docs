## Overview

Protected Resource Secret Management enables API administrators to create, rotate, and manage client secrets for Protected Resources (MCP Servers) in Gravitee Access Management. This feature allows Protected Resources to authenticate as OAuth2 clients for token introspection and token exchange workflows, supporting multi-secret rotation and certificate-based JWT verification.

## Key Concepts

### Protected Resource as OAuth2 Client

Protected Resources function as OAuth2 clients with full secret lifecycle management. Each Protected Resource receives default OAuth2 settings (`client_credentials` grant, `client_secret_basic` authentication) and can maintain multiple active secrets for rotation scenarios. The resource can be resolved by either its `clientId` (like standard Applications) or its `resourceIdentifier` (per RFC 8707).

### Secret Lifecycle

Secrets follow a managed lifecycle:

- **Create**: Generates a random secret and stores algorithm settings
- **Renew**: Generates a new value while preserving the settings reference
- **Delete**: Removes the secret and cleans up orphaned settings

Multiple secrets can exist simultaneously to support zero-downtime rotation.

### Certificate-Based JWT Verification

Protected Resources support an optional `certificate` field that specifies a custom signing key for JWT verification during token introspection. If no certificate is assigned, the system assumes HMAC-signed JWTs.

## Prerequisites

- Access Management domain with OAuth2 enabled
- `PROTECTED_RESOURCE_SECRET` event type configured for audit logging
- Token exchange enabled at domain level (`tokenExchangeSettings.enabled = true`) if using token exchange workflows
- Valid certificate uploaded to the domain if using certificate-based JWT signing

## Gateway Configuration

### OAuth2 Default Settings

Protected Resources automatically receive these defaults on creation or update if not explicitly provided:

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `settings.oauth.grantTypes` | `["client_credentials"]` | Allowed grant types |
| `settings.oauth.responseTypes` | `["code"]` | Allowed response types |
| `settings.oauth.tokenEndpointAuthMethod` | `"client_secret_basic"` | Token endpoint authentication method |
| `settings.oauth.clientId` | Copied from `resource.clientId` | OAuth2 client identifier |
| `settings.oauth.clientSecret` | Preserved if exists | Existing secret value retained |

User-provided values always take precedence over defaults.

### Token Exchange Settings

Configure allowed subject token types at the domain level:

| Property | Example Value | Description |
|:---------|:--------------|:------------|
| `tokenExchangeSettings.enabled` | `true` | Enable token exchange grant |
| `tokenExchangeSettings.allowedSubjectTokenTypes` | `["urn:ietf:params:oauth:token-type:access_token", "urn:ietf:params:oauth:token-type:id_token"]` | Permitted subject token types for exchange |

## Creating and Managing Secrets

Use the Management API to manage Protected Resource secrets through five endpoints under `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets`:

- **Create a secret**: POST to the secrets collection endpoint with a JSON body containing `{"name": "secret-name"}`. The API returns a `ClientSecret` object with the generated secret value, which is only displayed once.

- **Renew a secret**: POST to the `/_renew` endpoint under the specific secret ID. This generates a new value while preserving algorithm settings.

- **Delete a secret**: Send a DELETE request to the secret's endpoint. The system automatically removes orphaned `ApplicationSecretSettings` when no secrets reference them.

- **List all secrets**: Send a GET request to the secrets collection endpoint for the resource.

### Creating a Secret

Create a new secret for a Protected Resource by sending a POST request to the Management API:

```http
POST /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets
Content-Type: application/json

{
  "name": "secret-name"
}
```

The API returns a `ClientSecret` object containing the generated secret value. **This value is displayed only once** and can't be retrieved again. Store it securely before closing the response.

**Response schema:**

| Property | Type | Description |
|:---------|:-----|:------------|
| `id` | String | Secret identifier |
| `name` | String | User-provided secret name |
| `secret` | String | Generated secret value (only returned on create/renew) |
| `createdAt` | Timestamp | Secret creation time |
| `settingsId` | String | Reference to associated `ApplicationSecretSettings` |

### Renewing a Secret

Renew an existing secret by sending a POST request to the renewal endpoint:

```http
POST /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets/{secretId}/_renew
```

Renewal generates a new secret value while preserving the existing algorithm settings reference. The response includes the new secret value, which is **displayed only once**. The previous secret value is immediately invalidated.

### Deleting a Secret

Remove a secret by sending a DELETE request:

```http
DELETE /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets/{secretId}
```

When a secret is deleted, the system automatically removes orphaned `ApplicationSecretSettings` records if no other secrets reference them. This prevents accumulation of unused configuration data.

### Listing Secrets

Retrieve all secrets for a Protected Resource:

```http
GET /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets
```

The response contains an array of `ClientSecret` objects. The `secret` field is **not included** in list responses—secret values are only returned during creation or renewal.

### Secret Rotation

Multiple secrets can exist simultaneously for a single Protected Resource to support zero-downtime rotation. Create a new secret before deleting the old one to maintain continuous service availability during credential updates.

## Protected Resource Schema

### Core Fields

| Property | Type | Description |
|:---------|:-----|:------------|
| `certificate` | String (nullable) | Certificate ID for JWT verification |
| `settings` | ApplicationSettings | OAuth2 configuration object |
| `secretSettings` | List<ApplicationSecretSettings> | Secret algorithm settings |
| `clientId` | String | OAuth2 client identifier |
| `resourceIdentifiers` | List<String> | RFC 8707 resource identifiers (required, non-empty) |

### Secret Response Schema

| Property | Type | Description |
|:---------|:-----|:------------|
| `id` | String | Secret identifier |
| `name` | String | User-provided secret name |
| `secret` | String | Secret value (only on create/renew) |
| `settingsId` | String | Reference to algorithm settings |
| `expiresAt` | Date | Expiration timestamp |
| `createdAt` | Date | Creation timestamp |

## Search Functionality

Search Protected Resources by name or `clientId` using the `q` query parameter:

```http
GET /protected-resources?q=search-term
```

The search supports wildcards (`*`) and performs case-insensitive matching. For example, `?q=mcp-*` returns all resources with names or client IDs starting with "mcp-".

## Event Integration

Secret lifecycle operations emit `PROTECTED_RESOURCE_SECRET` events mapped to standard actions:

- `CREATE` for new secrets
- `UPDATE` for renewals
- `DELETE` for removals

These events integrate with the existing `ClientSecretNotifierService` for expiration notifications.

## Settings Cleanup Architecture

`ApplicationSecretSettings` objects are reference-counted. When a secret is deleted, the system checks if any other secrets reference the same `settingsId`. If no references exist, the settings object is also deleted to prevent orphaned data.

## MCP Server UI Context

The UI filters token endpoint authentication methods when displaying Protected Resources in MCP Server context, showing only:

- `client_secret_basic`
- `client_secret_post`
- `client_secret_jwt`

Methods like `private_key_jwt`, `tls_client_auth`, and `none` are hidden.

## Restrictions

- Resource identifiers (`resourceIdentifiers`) can't be null or empty; validation throws `InvalidProtectedResourceException` if violated
- All resource identifiers within a domain must be unique; duplicate identifiers trigger `InvalidProtectedResourceException` on create or update
- All feature keys within a Protected Resource must be unique; duplicates trigger `InvalidProtectedResourceException`
- Certificates can't be deleted if referenced by any Protected Resource; deletion throws `CertificateWithProtectedResourceException`
- MCP Servers in token exchange flows support only `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grants
- Token exchange doesn't issue refresh tokens or ID tokens, even if `openid` scope is requested
- Subject token types must be in the domain's `allowedSubjectTokenTypes` list; unsupported types return `invalid_request` error
- Secret values are only returned on create and renew operations; subsequent GET requests omit the `secret` field

