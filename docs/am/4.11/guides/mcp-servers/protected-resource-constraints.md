### Overview

Protected Resources in Gravitee Access Management support full lifecycle management including secret rotation, certificate-based authentication, and membership controls. These enhancements enable Protected Resources to participate in token introspection workflows and enforce MCP Server-specific OAuth constraints. This feature is designed for API platform administrators managing resource servers and OAuth clients.

### Key Concepts

#### Protected Resource Secrets

Protected Resources use client secrets for authentication, similar to Applications. Each Protected Resource maintains one or more secrets with independent expiration tracking. Secrets can be created, renewed, and deleted via REST API. When a secret is deleted, its associated OAuth settings are removed only if no other secrets reference them. At least one secret must exist per Protected Resource.

#### Token Introspection with Protected Resources

Token introspection validates audiences against both Applications and Protected Resources. For single-audience tokens, the system checks the Application registry first, then the Protected Resource registry, and finally falls back to RFC 8707 resource identifier validation. Multi-audience tokens always use RFC 8707 validation. Certificate-based JWT verification is supported when the Protected Resource has a certificate configured. If no certificate is configured, the system assumes HMAC-signed tokens.

#### MCP Server Context Restrictions

When operating in MCP Server context, grant types are restricted to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange`. Token endpoint authentication methods are limited to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`. These restrictions prevent MCP Servers from using user-facing flows like `authorization_code` or `password`.

### Prerequisites

Before managing Protected Resource secrets, ensure the following:

* Domain-level `SecretExpirationSettings` configured for secret lifecycle management
* Appropriate permissions: `PROTECTED_RESOURCE[LIST|CREATE|UPDATE|DELETE]` for secret operations
* For certificate-based authentication: valid certificate uploaded to the domain
* For membership management: `PROTECTED_RESOURCE_MEMBER[LIST|CREATE|DELETE]` permissions

### Gateway Configuration

#### OAuth Settings Defaults

When creating a Protected Resource, the following OAuth settings are applied automatically if not explicitly provided:

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `grantTypes` | `["client_credentials"]` | Allowed OAuth grant types |
| `responseTypes` | `["code"]` | Allowed OAuth response types |
| `tokenEndpointAuthMethod` | `"client_secret_basic"` | Default authentication method for token endpoint |
| `clientId` | (copied from resource) | OAuth client identifier |
| `clientSecret` | (preserved or generated) | OAuth client secret |

#### Event Configuration

Protected Resource secret lifecycle events are tracked using the `PROTECTED_RESOURCE_SECRET` event type:

| Event Action | Trigger | Description |
|:-------------|:--------|:------------|
| `CREATE` | Secret creation | Registers expiration notification |
| `RENEW` | Secret renewal | Unregisters old notification, registers new |
| `DELETE` | Secret deletion | Unregisters notification and acknowledgement |

### Creating Protected Resources with Secrets

Protected Resources are created via the domain API with automatic OAuth settings initialization.

1. Submit a POST request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources` with the resource definition.
2. The system generates a default secret and applies OAuth settings (grant types, auth method, client credentials).
3. If a certificate is specified, it is linked for JWT verification.
4. The secret expiration notification is registered based on domain-level expiration policies.
5. The plaintext secret is returned only in the creation response. Subsequent retrievals return safe (redacted) secrets.

### Managing Protected Resource Secrets

Secret rotation follows a create-renew-delete cycle.

1. List existing secrets via GET `/secrets` to identify the target secret.
2. To rotate, POST to `/secrets/{secretId}/_renew`. This generates a new secret value and updates the expiration timestamp.
3. Delete obsolete secrets via DELETE `/secrets/{secretId}`. The system enforces that at least one secret remains.
4. If the deleted secret was the last reference to a specific OAuth settings object, those settings are also removed.
5. All secret operations emit events that update expiration notifications in the background.

### Configuring Certificate-Based Authentication

Protected Resources support certificate-based JWT verification for token introspection.

1. Upload a certificate to the domain via the certificate management API.
2. Update the Protected Resource with the certificate ID in the `certificate` field.
3. During token introspection, if the audience matches the Protected Resource's `clientId` and a certificate is configured, the system uses that certificate for JWT signature verification.
4. If no certificate is configured, the system assumes HMAC-signed tokens.
5. Certificates cannot be deleted while referenced by any Protected Resource. Deletion attempts return HTTP 400 with error message "You can't delete a certificate with existing protected resources."
