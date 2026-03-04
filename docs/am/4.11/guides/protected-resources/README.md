### Overview

Protected Resources now support advanced secret management, certificate-based authentication, and membership controls. These enhancements enable Protected Resources to participate fully in OAuth 2.0 token introspection flows and token exchange scenarios, with parity to Application-level security features. This feature is designed for API platform administrators managing resource servers and MCP (Model Context Protocol) server integrations.

### Key Concepts

#### Protected Resource Secrets

Protected Resources can manage multiple client secrets with expiration tracking and renewal workflows. Secrets inherit domain-level expiration policies and trigger notifications before expiry. At least one active secret must exist per resource. When a secret is deleted, its associated settings are removed if no other secrets reference them.

#### Certificate-Based Authentication

Protected Resources support X.509 certificate binding for mutual TLS authentication. Certificates are validated on resource creation and update. A certificate can't be deleted if any Protected Resource references it — the system enforces referential integrity via `CertificateWithProtectedResourceException`.

#### Token Introspection Audience Resolution

When introspecting a JWT, the system resolves the `aud` claim by checking Application client IDs first, then Protected Resource client IDs, and finally resource identifiers (RFC 8707). For tokens with multiple audiences, all values are validated as resource identifiers. The matched client or resource provides the certificate ID for signature verification.

### OAuth 2.0 Default Settings

Protected Resources automatically receive OAuth 2.0 defaults on creation. These values are applied when the `settings` object is null or incomplete.

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `settings.oauth.grantTypes` | `["client_credentials"]` | Allowed grant types |
| `settings.oauth.responseTypes` | `["code"]` | Allowed response types |
| `settings.oauth.tokenEndpointAuthMethod` | `"client_secret_basic"` | Default authentication method |
| `settings.oauth.clientId` | (copied from resource) | OAuth client identifier |
| `settings.oauth.clientSecret` | (preserved if exists) | Preserved on update |

{% hint style="info" %}
The `clientId` is automatically copied from the resource identifier. The `clientSecret` is preserved during updates if it already exists.
{% endhint %}

### Prerequisites

Before configuring Protected Resource enhancements, ensure the following:

* Domain with OAuth 2.0 enabled
* For certificate authentication: valid X.509 certificate uploaded to the domain
* For secret expiration: domain-level `SecretExpirationSettings` configured
* For membership management: users or groups defined in the domain identity provider

### Restrictions

#### Secret Management

* At least one secret must exist per Protected Resource
* Secret deletion removes associated settings if no other secrets reference the same `settingsId`
* Expiration notifications require domain-level `SecretExpirationSettings`

#### Certificate Management

* Certificate deletion is blocked if any Protected Resource references it (`CertificateWithProtectedResourceException`)
* Certificate ID must exist when set on a Protected Resource (`CertificateNotFoundException`)

#### MCP Server Context

When the resource context is `McpServer`, the following restrictions apply:

**Grant Types:**
* Only `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` are allowed
* All other grant types are excluded

**Token Endpoint Authentication Methods:**
* Allowed: `client_secret_basic`, `client_secret_post`, `client_secret_jwt`
* Excluded: `private_key_jwt`, `tls_client_auth`, `self_signed_tls_client_auth`, `none`

#### Token Introspection

* Multi-audience introspection always uses resource identifiers for validation
* Single-audience tokens fall back to resource identifier validation if no matching Application or Protected Resource client ID is found

