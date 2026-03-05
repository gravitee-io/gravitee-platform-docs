### Gateway Configuration

#### Protected Resource Properties

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `certificate` | String | `null` | Certificate ID for JWT signature verification (RSA/ECDSA) |
| `settings.oauth.grantTypes` | List\<String> | `["client_credentials"]` | Allowed grant types |
| `settings.oauth.responseTypes` | List\<String> | `["code"]` | Allowed response types |
| `settings.oauth.tokenEndpointAuthMethod` | String | `"client_secret_basic"` | Authentication method for token endpoint |
| `settings.oauth.clientId` | String | `{resource.clientId}` | OAuth client identifier (auto-populated from resource) |
| `settings.oauth.clientSecret` | String | preserved | OAuth client secret (preserved from existing settings on update) |

The `certificate` field specifies a certificate ID for JWT signature verification using RSA or ECDSA algorithms. When `null`, the system uses HMAC-based verification.

The `settings.oauth.clientId` field is automatically populated with the Protected Resource's `clientId` value during creation and update operations.

The `settings.oauth.clientSecret` field is preserved from existing settings during update operations. If no existing settings are present, the field remains `null`.

#### Domain Token Exchange Settings

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `tokenExchangeSettings.allowedSubjectTokenTypes` | List\<String> | `["access_token", "refresh_token", "id_token", "jwt"]` | Token types accepted as subject tokens in token exchange requests |

### Token Exchange for MCP Servers

MCP Servers are Protected Resources restricted to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types. During token exchange, the system validates the subject token, preserves its `gis` claim, and issues a new access token with `client_id` and `aud` set to the MCP Server's `clientId`. Exchanged tokens never include refresh tokens or ID tokens (even with `openid` scope), and their expiration cannot exceed the subject token's remaining lifetime.

### Prerequisites

* Domain with OAuth 2.0 enabled
* For certificate-based authentication: uploaded certificate in PEM format
* For token exchange: domain `tokenExchangeSettings.allowedSubjectTokenTypes` configured (defaults: `access_token`, `refresh_token`, `id_token`, `jwt`)
* For secret expiration notifications: domain `SecretExpirationSettings` configured

### Creating a Protected Resource

Create a Protected Resource by calling `POST /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources` with a JSON body containing `name`, `description`, `type` (e.g., `MCP_SERVER`), and optional `resourceIdentifiers` array. The system generates a `clientId`, creates an initial client secret, and applies default OAuth settings (`client_credentials` grant, `client_secret_basic` auth method). For MCP Servers, the system restricts grant types to `client_credentials` and token exchange only. If you specify a `certificate` field with a valid certificate ID, the resource will use JWT signature verification instead of HMAC. The response includes the generated `clientId` and initial secret value (store this securely — it cannot be retrieved later).

### Managing Secrets

Rotate secrets by calling `POST /protected-resources/{id}/secrets/{secretId}/_renew`, which generates a new secret value while preserving the algorithm settings and updating the expiration timestamp. The system removes settings only if no other secrets reference the same `settingsId`.
