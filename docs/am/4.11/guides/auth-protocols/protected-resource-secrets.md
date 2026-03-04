### Overview

Protected resources in Gravitee Access Management now function as OAuth2 clients with full secret management, certificate-based authentication, and membership controls. This enhancement enables server-to-server authentication scenarios, including token exchange flows for MCP (Model Context Protocol) servers. Protected resources can authenticate at the token introspection endpoint and participate in delegation workflows.

### Key Concepts

#### Protected Resource Secrets

Protected resources maintain one or more client secrets for authentication. Each secret has a unique identifier, optional expiration date, and can be renewed or deleted independently. Secrets are generated server-side and returned in plaintext only at creation or renewal. The system triggers expiration notifications when secrets approach their expiration date.

#### Token Exchange Grant

The token exchange grant type (`urn:ietf:params:oauth:grant-type:token-exchange`) enables delegation scenarios where a client exchanges an existing token (access, refresh, ID, or JWT) for a new access token. The issued token inherits the subject token's expiration constraints and preserves the `gis` claim. Token exchange never issues refresh tokens or ID tokens, even when the `openid` scope is requested.

#### Protected Resource Authentication

Protected resources authenticate at the token introspection endpoint using their client credentials. When a JWT's `aud` claim matches a protected resource's `clientId`, the system validates the token signature using the resource's configured certificate (or HMAC if no certificate is specified). This enables protected resources to verify tokens issued for their audience.

### Prerequisites

Before configuring protected resources as OAuth2 clients, ensure the following:

* Domain with protected resources enabled
* For token exchange: domain-level token exchange settings configured with allowed subject token types
* For certificate-based authentication: valid certificate uploaded to the domain
* For membership management: users or groups with appropriate roles

### Gateway Configuration

#### Token Exchange Settings

Configure token exchange at the domain level to enable delegation flows.

| Property | Description | Example |
|:---------|:------------|:--------|
| `tokenExchangeSettings.enabled` | Enable token exchange grant type | `true` |
| `tokenExchangeSettings.allowedSubjectTokenTypes` | Permitted subject token types for exchange | `['urn:ietf:params:oauth:token-type:access_token', 'urn:ietf:params:oauth:token-type:jwt']` |

#### Protected Resource OAuth2 Settings

Protected resources inherit default OAuth2 settings when created. These can be customized per resource.

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `settings.oauth.grantTypes` | Array<String> | `['client_credentials']` | Default grant types |
| `settings.oauth.responseTypes` | Array<String> | `['code']` | Default response types |
| `settings.oauth.tokenEndpointAuthMethod` | String | `'client_secret_basic'` | Default authentication method |
| `settings.oauth.clientId` | String | `<resource.clientId>` | Copied from resource |
| `settings.oauth.clientSecret` | String | `<preserved from existing>` | Preserved on update if present |
