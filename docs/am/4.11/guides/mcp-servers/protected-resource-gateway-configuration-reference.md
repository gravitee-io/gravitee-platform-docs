### Token Exchange Settings

Configure token exchange at the domain level to enable delegation flows.

| Property | Description | Example/Default |
|:---------|:------------|:----------------|
| `tokenExchangeSettings.enabled` | Enable token exchange grant type | `true` |
| `tokenExchangeSettings.allowedSubjectTokenTypes` | Permitted subject token types for exchange | `['urn:ietf:params:oauth:token-type:access_token', 'urn:ietf:params:oauth:token-type:jwt']` |

### Protected Resource OAuth2 Settings

Protected resources inherit default OAuth2 settings when created. Customize these settings per resource as needed.

| Property | Description | Default |
|:---------|:------------|:--------|
| `settings.oauth.grantTypes` | Allowed grant types | `['client_credentials']` |
| `settings.oauth.responseTypes` | Allowed response types | `['code']` |
| `settings.oauth.tokenEndpointAuthMethod` | Authentication method at token endpoint | `client_secret_basic` |
| `settings.oauth.clientId` | OAuth2 client identifier | Copied from `resource.clientId` |
| `settings.oauth.clientSecret` | Client secret | Generated on creation, preserved on update |

## Prerequisites

Before you configure UMA 2.0 authorization, ensure the following requirements are met:

* **Protected resources enabled**: The domain must have protected resources enabled.
* **Token exchange configured** (if using token exchange): Domain-level token exchange settings must be configured with allowed subject token types.
* **Valid certificate uploaded** (if using certificate-based authentication): A valid certificate must be uploaded to the domain.
* **User or group roles assigned** (if managing membership): Users or groups must have appropriate roles assigned.

### MCP Server Restrictions

MCP servers support a restricted subset of grant types and authentication methods.

**Allowed Grant Types:**
- `client_credentials`
- `urn:ietf:params:oauth:grant-type:token-exchange`

**Allowed Token Endpoint Auth Methods:**
- `client_secret_basic`
- `client_secret_post`
- `client_secret_jwt`
