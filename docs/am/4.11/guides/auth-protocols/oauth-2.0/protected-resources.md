### Protected Resource Identity

A Protected Resource is an OAuth 2.0 resource server entity identified by a unique client ID and one or more resource identifiers (URIs). The client ID is used for token introspection and secret management, while resource identifiers appear in the `aud` (audience) claim of access tokens. Resource identifiers must be unique across all Protected Resources within a domain. Each resource can have multiple secrets for credential rotation and supports certificate-based JWT signature verification.

## Overview

Protected Resources represent OAuth 2.0 resource servers that can validate access tokens and participate in token exchange flows. This feature enables administrators to manage resource server credentials, certificates, and membership independently from client applications.

Protected Resources support:

* **RFC 8707 resource indicators** — Specify target resources in authorization requests
* **OAuth 2.0 Token Exchange (RFC 8693)** — Enable token exchange flows for MCP Server integrations

### Token Exchange for MCP Servers

MCP Servers use the Token Exchange grant type (`urn:ietf:params:oauth:grant-type:token-exchange`) to exchange subject tokens (access, refresh, ID, or JWT tokens) for new access tokens scoped to the MCP Server's client ID. The exchanged token inherits the subject token's expiration and `gis` claim but never includes refresh tokens or ID tokens in the response. Subject token types can be restricted via domain-level settings (`domain.tokenExchangeSettings.allowedSubjectTokenTypes`).

### Certificate-Based Verification

Protected Resources can reference a certificate for JWT signature verification during token introspection. When a certificate is assigned, the introspection service uses it to validate incoming tokens. When null, HMAC-based verification is assumed. Certificates cannot be deleted if they are in use by any Protected Resource, Application, or Identity Provider.

### Prerequisites

Before creating or managing Protected Resources, ensure the following:

* Access Management domain configured
* `PROTECTED_RESOURCE[CREATE]`, `PROTECTED_RESOURCE[UPDATE]`, `PROTECTED_RESOURCE[READ]` permissions
* For certificate-based verification: valid certificate uploaded to the domain
* For token exchange: MCP Server configured with `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types

### Gateway Configuration

#### OAuth Settings Defaults

When creating or updating a Protected Resource, the following defaults are applied if `settings.oauth` is null or incomplete:

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `settings.oauth.grantTypes` | `["client_credentials"]` | Allowed grant types |
| `settings.oauth.responseTypes` | `["code"]` | Allowed response types |
| `settings.oauth.tokenEndpointAuthMethod` | `"client_secret_basic"` | Token endpoint authentication method |
| `settings.oauth.clientId` | `{resource.clientId}` | OAuth client ID (copied from resource) |
| `settings.oauth.clientSecret` | Preserved from existing | Preserved on update if already set |

#### Certificate Assignment

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `certificate` | String | Certificate ID for JWT signature verification | `"cert-abc123"` |

### Creating a Protected Resource

1. Navigate to the Protected Resources section in your domain.
2. Provide a client ID (e.g., `api-server-1`) and at least one resource identifier URI (e.g., `https://api.example.com`).
3. Optionally assign a certificate for JWT verification.
4. The system applies default OAuth settings (`client_credentials` grant, `client_secret_basic` auth method) unless you override them.
5. After creation, generate secrets via the secrets endpoint to enable authentication.

### Managing Secrets

Protected Resources support multiple secrets for credential rotation.

1. List existing secrets via `GET /secrets`. Secrets are sanitized in responses.
2. Create a new secret by posting to `/secrets` with a `name` field. The response includes the plaintext secret. Store it securely—it won't be shown again.
3. Renew a secret via `POST /secrets/{secretId}/_renew` to generate a new value while preserving metadata.
4. Delete a secret via `DELETE /secrets/{secretId}`. The last secret can be deleted (no minimum count enforced).

Secret expiration notifications are automatically registered and updated on create, renew, and delete operations.

### Configuring Token Exchange for MCP Servers

MCP Servers require restricted grant types and token endpoint authentication methods.

1. When creating an MCP Server, set `grantTypes` to `["client_credentials", "urn:ietf:params:oauth:grant-type:token-exchange"]`.
2. Choose a token endpoint authentication method from: `client_secret_basic`, `client_secret_post`, `client_secret_jwt`, or `null` (based on incoming request).
3. Configure allowed subject token types at the domain level via `domain.tokenExchangeSettings.allowedSubjectTokenTypes` (defaults: `access_token`, `refresh_token`, `id_token`, `jwt`).
4. The exchanged token's `expires_in` will never exceed the subject token's expiration, and the `client_id` and `aud` claims are set to the MCP Server's client ID.

### Managing Membership

Assign users or groups to Protected Resources with specific roles.

1. List members via `GET /members` (requires `PROTECTED_RESOURCE_MEMBER[LIST]` permission).
2. Add a member via `POST /members` with `memberId`, `memberType`, and `role` (requires `PROTECTED_RESOURCE_MEMBER[CREATE]` permission).
3. Remove a member via `DELETE /members/{member}` (requires `PROTECTED_RESOURCE_MEMBER[DELETE]` permission).
4. View permissions via `GET /permissions` (requires `PROTECTED_RESOURCE[READ]` permission).
