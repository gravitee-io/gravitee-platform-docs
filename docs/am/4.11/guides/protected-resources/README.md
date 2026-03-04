### Overview

Protected Resources enable secure machine-to-machine communication in OAuth 2.0 workflows. They represent backend services or APIs that consume access tokens issued by AM, supporting multiple client secrets with independent lifecycles, certificate-based authentication for JWT signature verification, and token introspection against RFC 8707 resource identifiers. Protected Resources integrate with Applications to validate token audiences and enforce access controls through membership management.

### Prerequisites

Before configuring Protected Resources, ensure the following:

* Domain exists and is accessible
* For certificate-based authentication: valid certificate uploaded to the domain
* For membership management: users or groups exist in the organization
* For token introspection: tokens include `aud` claim matching client ID or resource identifier

### Token Introspection with Protected Resources

Token introspection validates the `aud` claim against both Applications and Protected Resources. For single-audience tokens, the system checks `ClientSyncService` for Application clients, then `ProtectedResourceSyncService` for Protected Resource clients, and finally `ProtectedResourceManager` for RFC 8707 resource identifiers. Multi-audience tokens always use RFC 8707 validation. The certificate ID from the matched client or resource is used for JWT signature verification.

Offline verification decodes the JWT and validates the audience. Online verification additionally checks token existence and expiration in the repository. Tokens without an `aud` claim return error "Token has no audience claim". Unmatched audiences return error "Client or resource not found: {aud}".

### Managing Protected Resource Secrets

Protected Resources support multiple client secrets with independent lifecycles. Each secret has a unique identifier, expiration date, and algorithm configuration. Multiple secrets may share the same algorithm settings (`settingsId`) to simplify configuration management.

#### Listing Secrets

List secrets via `GET /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets`. The response returns metadata without secret values:

```json
[
  {
    "id": "string",
    "name": "string",
    "settingsId": "string",
    "expiresAt": "2024-01-01T00:00:00Z",
    "createdAt": "2024-01-01T00:00:00Z"
  }
]
```

#### Creating a Secret

Create a secret via `POST /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets` with JSON body:

```json
{
  "name": "string"
}
```

The system generates a random secret value, creates algorithm settings, and returns the secret (visible only once):

```json
{
  "id": "string",
  "name": "string",
  "secret": "string",
  "settingsId": "string",
  "expiresAt": "2024-01-01T00:00:00Z",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

A `PROTECTED_RESOURCE_SECRET.CREATE` event is published, triggering expiration notification registration.

#### Renewing a Secret

Renew a secret via `POST /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets/{secretId}/_renew`. The system generates a new secret value, preserves the `settingsId`, and updates the `createdAt` timestamp. The response matches the creation response schema. A `PROTECTED_RESOURCE_SECRET.RENEW` event is published, unregistering the old expiration notification and registering a new one.

#### Deleting a Secret

Delete a secret via `DELETE /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets/{secretId}`. The system removes the secret and cleans up unused `secretSettings` entries. A `PROTECTED_RESOURCE_SECRET.DELETE` event is published, unregistering the expiration notification.

#### Permissions

Secret operations require `PROTECTED_RESOURCE.CREATE`, `PROTECTED_RESOURCE.UPDATE`, or `PROTECTED_RESOURCE.DELETE` permissions on the resource, domain, environment, or organization.

### Protected Resource Restrictions and Validation Rules

#### Resource Identifier Requirements

Protected Resources must have at least one resource identifier. Empty `resourceIdentifiers` arrays return `InvalidProtectedResourceException` with message "Field [resourceIdentifiers] must not be empty".

Resource identifiers must be unique across all Protected Resources in a domain. Duplicate identifiers return `InvalidProtectedResourceException` with message "Resource identifier [{identifier}] is already in use by another protected resource".

#### Certificate Deletion Restrictions

Certificates in use by Protected Resources cannot be deleted. Attempts return `CertificateWithProtectedResourceException` with message "You can't delete a certificate with existing protected resources."

#### MCP Server Grant Type Restrictions

MCP Server contexts restrict grant types to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange`.

#### MCP Server Authentication Method Restrictions

MCP Server contexts restrict token endpoint authentication to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`. Methods `private_key_jwt`, `tls_client_auth`, and `self_signed_tls_client_auth` are excluded.

#### Permission Requirements

* Secret operations: `PROTECTED_RESOURCE.CREATE`, `PROTECTED_RESOURCE.UPDATE`, or `PROTECTED_RESOURCE.DELETE`
* Membership operations: `PROTECTED_RESOURCE_MEMBER.LIST`, `PROTECTED_RESOURCE_MEMBER.CREATE`, or `PROTECTED_RESOURCE_MEMBER.DELETE`

#### Search Limitations

Search queries with wildcards are limited to prefix matching (e.g., `clientId*`). Infix or suffix wildcards are not supported.

#### Token Introspection Requirements

Token introspection requires tokens to include an `aud` claim. Tokens without audience claims are rejected.

### Configuring Certificate-Based Authentication for Protected Resources

Assign a certificate to a Protected Resource by setting the `certificate` field to a valid certificate ID during creation or update. The system validates the certificate exists in the domain via `CertificateService`. If the certificate is not found, the request fails with `CertificateNotFoundException`.

During token introspection, the certificate ID is extracted from the Protected Resource and used to verify JWT signatures. Certificates in use by Protected Resources cannot be deleted.

### Client Configuration for Protected Resources

Clients using Protected Resources must configure OAuth 2.0 settings and token exchange parameters:

| Property | Type | Example | Description |
|:---------|:-----|:--------|:------------|
| `grantTypes` | Array | `["client_credentials", "urn:ietf:params:oauth:grant-type:token-exchange"]` | Allowed grant types (MCP Servers limited to these two) |
| `tokenEndpointAuthMethod` | String | `"client_secret_basic"` | Authentication method (MCP Servers: `client_secret_basic`, `client_secret_post`, `client_secret_jwt` only) |
| `resourceIdentifiers` | Array | `["https://mcp-server.example.com"]` | RFC 8707 resource identifiers for token exchange |
| `scopeSettings` | Array | `[{ "scope": "openid", "defaultScope": true }]` | Scope configuration with default flags |

### Protected Resource Creation and Default Settings

Create a Protected Resource via `POST /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources` with JSON body containing `name`, `resourceIdentifiers`, and optional `settings`.

The system applies OAuth 2.0 default settings when the corresponding field is null or empty:

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `settings.oauth.grantTypes` | `["client_credentials"]` | Default grant types |
| `settings.oauth.responseTypes` | `["code"]` | Default response types |
| `settings.oauth.tokenEndpointAuthMethod` | `"client_secret_basic"` | Default authentication method |
| `settings.oauth.clientId` | (copied from resource) | Matches Protected Resource client ID |
| `settings.oauth.clientSecret` | (preserved if exists) | Retained from existing settings during updates |

The creation sequence: (1) default client secret generated and OAuth defaults applied, (2) custom settings applied if provided, (3) resource persisted with `secretSettings` and `clientSecrets` arrays, (4) `PROTECTED_RESOURCE_SECRET.CREATE` event published, (5) response includes resource ID and initial secret value (visible only once).

Protected Resource secret lifecycle events are published to the event bus:

| Event Type | Action | Description |
|:-----------|:-------|:------------|
| `PROTECTED_RESOURCE_SECRET` | `CREATE` | Secret created |
| `PROTECTED_RESOURCE_SECRET` | `RENEW` | Secret renewed (new value generated) |
| `PROTECTED_RESOURCE_SECRET` | `DELETE` | Secret deleted |

