
## Prerequisites

Before managing Protected Resource secrets, ensure the following requirements are met:

* Access Management 4.11.0 or later
* `PROTECTED_RESOURCE[CREATE]`, `PROTECTED_RESOURCE[UPDATE]`, `PROTECTED_RESOURCE[DELETE]` permissions for secret management operations
* `PROTECTED_RESOURCE_MEMBER[LIST]`, `PROTECTED_RESOURCE_MEMBER[CREATE]`, `PROTECTED_RESOURCE_MEMBER[DELETE]` permissions for membership operations
* Valid domain-scoped certificate if using certificate-based authentication

## Gateway Configuration

### OAuth 2.0 Default Settings


When creating or updating a Protected Resource, the system applies default OAuth settings if the `settings.oauth` field is null or incomplete. These defaults ensure functional client credentials flows without explicit configuration.

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `settings.oauth.grantTypes` | `["client_credentials"]` | Default grant types |
| `settings.oauth.responseTypes` | `["code"]` | Default response types |
| `settings.oauth.tokenEndpointAuthMethod` | `client_secret_basic` | Default authentication method |
| `settings.oauth.clientId` | (copied from `clientId`) | Synchronized with resource client ID |
| `settings.oauth.clientSecret` | (preserved if exists) | Retained from existing settings on update |

#### Event Configuration

Secret lifecycle operations emit domain events for audit and synchronization purposes.

| Event Type | Action | Description |
|:-----------|:-------|:------------|
| `PROTECTED_RESOURCE_SECRET` | `CREATE` | Emitted when a new secret is generated |
| `PROTECTED_RESOURCE_SECRET` | `RENEW` | Emitted when an existing secret is renewed |
| `PROTECTED_RESOURCE_SECRET` | `DELETE` | Emitted when a secret is deleted |

## Renewing or Deleting Secrets

### Renew a Secret

To renew a secret, call the following endpoint:

```
POST /protected-resources/{id}/secrets/{secretId}/_renew
```

The response contains the new plaintext value of the secret.

### Delete a Secret

To delete a secret, call the following endpoint:

```
DELETE /protected-resources/{id}/secrets/{secretId}
```

The system removes the secret from `clientSecrets` and removes the associated `secretSettings` entry only if no other secret references it.

### List All Secrets

To list all secrets without plaintext values, call the following endpoint:

```
GET /protected-resources/{id}/secrets
```

### Creating a Protected Resource with Secrets

1. Create a Protected Resource via `POST /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources` with a JSON body containing `name`, `clientId`, `type`, and optional `certificate` field. The system validates certificate existence if provided and applies default OAuth settings.
2. After creation, generate a secret via `POST /protected-resources/{id}/secrets` with `{"name": "secret-name"}`. The response includes the plaintext secret value, which is never returned again.
3. Configure the Protected Resource as an audience in token exchange or client credentials flows.
4. Use the `clientId` and secret for authentication at the token endpoint.

### Event Configuration

See [Event Configuration](#event-configuration) above for details.
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

* MCP Server Protected Resources support only `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types
* MCP Server token endpoint authentication methods are limited to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`
* Certificate-based authentication methods (`private_key_jwt`, `tls_client_auth`, `self_signed_tls_client_auth`) are excluded for MCP Server contexts
* Plaintext secret values are returned only once at creation or renewal
* Secret settings (`secretSettings`) are shared across multiple secrets via `settingsId` and deleted only when no secrets reference them
* Certificates cannot be deleted if referenced by Protected Resources (HTTP 400 error)
* Resource identifiers must be unique within the domain
* Feature keys must be unique within the Protected Resource

## Overview

Protected Resources now support secret management, certificate-based authentication, and membership controls. Token introspection has been extended to validate Protected Resource audiences alongside traditional OAuth clients. These enhancements enable secure machine-to-machine communication patterns, including MCP Server integrations with token exchange flows.

### Prerequisites

Before managing Protected Resource memberships, ensure you have the following permissions scoped to the target resource:

* `PROTECTED_RESOURCE_MEMBER[LIST]` to view members
* `PROTECTED_RESOURCE_MEMBER[CREATE]` to add members
* `PROTECTED_RESOURCE_MEMBER[DELETE]` to remove members
* `PROTECTED_RESOURCE[READ]` to retrieve flattened permissions

### Adding Members

Add a user or group to a Protected Resource via `POST /protected-resources/{id}/members` with a JSON body containing `memberId`, `memberType`, and `role`:

```json
{
  "memberId": "user-or-group-id",
  "memberType": "USER|GROUP",
  "role": "role-name"
}
```

The `memberType` field accepts `USER` or `GROUP`. The `role` field specifies the role assigned to the member.

### Listing Members

Retrieve all members assigned to a Protected Resource via `GET /protected-resources/{id}/members`. The response returns an array of `Membership` objects.

### Retrieving Flattened Permissions

Query the flattened permission map for a Protected Resource via `GET /protected-resources/{id}/members/permissions`. This endpoint returns a consolidated view of permissions across all members.

### Removing Members

Remove a member from a Protected Resource via `DELETE /protected-resources/{id}/members/{memberId}`. The system returns HTTP 204 on successful deletion.

### Event Configuration

See [Event Configuration](#event-configuration) above for details.

## Client Configuration

Clients authenticating as Protected Resources use the following properties:

| Property | Description | Example |
|:---------|:------------|:--------|
| `client_id` | Protected Resource `clientId` | `mcp-server-123` |
| `client_secret` | Secret value from creation or renewal response | `a1b2c3d4...` |
| `token_endpoint_auth_method` | Must match `settings.oauth.tokenEndpointAuthMethod` | `client_secret_basic` |
| `grant_type` | `client_credentials` or `urn:ietf:params:oauth:grant-type:token-exchange` | `client_credentials` |

### Token Introspection Audience Validation

Token introspection validates JWT audiences against both OAuth clients and Protected Resources. This enables Protected Resources to act as audience targets in token exchange and client credentials flows.

#### Single-Audience Token Validation

For tokens with a single audience, the introspection service performs the following checks in order:

1. Query `ClientSyncService.findByDomainAndClientId(domain, audience)` to check if the audience matches an OAuth client ID
2. If not found, query `ProtectedResourceSyncService.findByDomainAndClientId(domain, audience)` to check if the audience matches a Protected Resource client ID
3. If still not found, fall back to RFC 8707 resource identifier validation

If the audience matches a client or Protected Resource, the system extracts the certificate ID for JWT signature verification. If neither a client nor Protected Resource is found, `OAuth2AuthProvider` throws `InvalidTokenException` with the message: `"Client or resource not found: {aud}"`.

#### Multi-Audience Token Validation

Tokens with multiple audiences always use RFC 8707 resource identifier validation. Client ID matching is skipped for multi-audience tokens.

#### Implementation Details

The `BaseIntrospectionTokenService.validateAudienceAndGetCertificateId()` method:

1. Decodes the JWT and extracts the `aud` claim
2. Routes to single-audience or multi-audience validation based on the number of audiences
3. Returns the certificate ID for JWT signature verification (or an empty string for HMAC-based tokens)

The `OAuth2AuthProviderImpl.decodeToken()` method:

1. Calls `introspectionTokenService.introspect(token, offlineVerification)`
2. Extracts the `aud` claim from the JWT
3. Queries `clientSyncService.findByDomainAndClientId(domain, aud)`
4. If not found, queries `protectedResourceSyncService.findByDomainAndClientId(domain, aud)`
5. If neither is found, throws `InvalidTokenException` with message: `"Client or resource not found: {aud}"`
6. Returns `OAuth2AuthResponse(jwt, client)`

### OAuth 2.0 Default Settings

See [OAuth 2.0 Default Settings](#oauth-20-default-settings) above for details.

## Prerequisites

Before you configure protected resources, ensure you meet the following requirements:

* Access Management 4.11.0 or later
* The following permissions for secret management:
  * `PROTECTED_RESOURCE[CREATE]`
  * `PROTECTED_RESOURCE[UPDATE]`
  * `PROTECTED_RESOURCE[DELETE]`
* The following permissions for membership operations:
  * `PROTECTED_RESOURCE_MEMBER[LIST]`
  * `PROTECTED_RESOURCE_MEMBER[CREATE]`
  * `PROTECTED_RESOURCE_MEMBER[DELETE]`
* A valid domain-scoped certificate if using certificate-based authentication

### MCP Server restrictions

Protected Resources with type `MCP_SERVER` enforce restricted grant type and authentication method sets to ensure secure machine-to-machine communication patterns.

#### Grant types

MCP Server Protected Resources support only the following grant types:

* `client_credentials`
* `urn:ietf:params:oauth:grant-type:token-exchange`

All other OAuth 2.0 grant types are excluded from MCP Server contexts.

#### Token endpoint authentication methods

MCP Server Protected Resources support only the following token endpoint authentication methods:

* `client_secret_basic`
* `client_secret_post`
* `client_secret_jwt`

The following authentication methods are excluded:

* `private_key_jwt`
* `tls_client_auth`
* `self_signed_tls_client_auth`
* `none`

#### UI behavior

When the context is `McpServer`, the UI automatically filters the available token endpoint authentication methods to show only the permitted options. The Refresh Token and PKCE sections are hidden, as these features are not applicable to MCP Server grant flows.

## Creating a Protected Resource with Secrets

To create a protected resource, send a `POST` request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources` with a JSON body containing the following fields:

* `name`: The name of the protected resource
* `clientId`: The client identifier
* `type`: The resource type
* `certificate` (optional): The certificate identifier

{% hint style="info" %}
If you provide a `certificate` field, the system validates that the certificate exists before creating the resource.
{% endhint %}

The system applies the default OAuth set during resource creation.
