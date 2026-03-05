### Creating a Protected Resource

Create a Protected Resource by calling `POST /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources` with a JSON request body:

**Request Body:**
```json
{
 "name": "string",
 "description": "string",
 "type": "MCP_SERVER",
 "resourceIdentifiers": ["https://example.com"],
 "certificate": "cert-id"
}
```

**Required Fields:**

| Field | Type | Description |
|:------|:-----|:------------|
| `name` | String | Resource name  |
| `description` | String | Resource description  |
| `type` | String | Resource type (e.g., `MCP_SERVER`) |

**Optional Fields:**

| Field | Type | Description |
|:------|:-----|:------------|
| `resourceIdentifiers` | Array of Strings | Resource identifiers for validation |
| `certificate` | String | Certificate ID for JWT signature verification (RSA/ECDSA). If omitted, HMAC is used. |

**Response:**
```json
{
 "id": "string",
 "clientId": "string",
 "name": "string",
 "description": "string",
 "type": "MCP_SERVER",
 "resourceIdentifiers": ["https://example.com"],
 "certificate": "cert-id",
 "settings": {
 "oauth": {
 "grantTypes": ["client_credentials"],
 "responseTypes": ["code"],
 "tokenEndpointAuthMethod": "client_secret_basic",
 "clientId": "string",
 "clientSecret": "string"
 }
 },
 "clientSecrets": [
 {
 "id": "string",
 "name": "string",
 "secret": "string",
 "settingsId": "string",
 "expiresAt": "2025-01-01T00:00:00Z",
 "createdAt": "2025-01-01T00:00:00Z"
 }
 ],
 "updatedAt": "2025-01-01T00:00:00Z"
}
```

The system automatically generates a `clientId` and creates an initial client secret.  Default OAuth settings are applied:

| Setting | Default Value |
|:--------|:--------------|
| `grantTypes` | `["client_credentials"]` |
| `responseTypes` | `["code"]` |
| `tokenEndpointAuthMethod` | `"client_secret_basic"` |
| `clientId` | Auto-generated value |
| `clientSecret` | Auto-generated value |

For MCP Server types, the system restricts grant types to `client_credentials` and token exchange only during creation.

{% hint style="warning" %}
Store the initial secret value from the response securely. Secret values cannot be retrieved after creation.
{% endhint %}

#### Certificate-Based Authentication

To use JWT signature verification instead of HMAC, provide a `certificate` field with a valid certificate ID in the request body. The system will use the certificate's public key to verify JWT signatures (RSA or ECDSA algorithms).

### Managing Secrets

#### Creating Additional Secrets

Create additional secrets by calling `POST /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{id}/secrets`:

**Request Body:**
```json
{
 "name": "string"
}
```

**Response:**
```json
{
 "id": "string",
 "name": "string",
 "secret": "string",
 "settingsId": "string",
 "expiresAt": "2025-01-01T00:00:00Z",
 "createdAt": "2025-01-01T00:00:00Z"
}
```

#### Listing Secrets

List all secrets for a Protected Resource by calling `GET /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{id}/secrets`:

**Response:**
```json
[
 {
 "id": "string",
 "name": "string",
 "settingsId": "string",
 "expiresAt": "2025-01-01T00:00:00Z",
 "createdAt": "2025-01-01T00:00:00Z"
 }
]
```

{% hint style="info" %}
The `GET /secrets` endpoint returns metadata only. Secret values are not included in the response.
{% endhint %}

#### Renewing Secrets

Rotate a secret by calling `POST /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{id}/secrets/{secretId}/_renew`:

**Response:**
```json
{
 "id": "string",
 "name": "string",
 "secret": "string",
 "settingsId": "string",
 "expiresAt": "2025-01-01T00:00:00Z",
 "createdAt": "2025-01-01T00:00:00Z"
}
```

The system generates a new secret value, preserves the `settingsId`, and updates the `expiresAt` timestamp.

#### Deleting Secrets

Delete a secret by calling `DELETE /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{id}/secrets/{secretId}`. The system removes the secret from the `clientSecrets` array and cleans up unused settings references.

#### Secret Expiration

The system triggers expiration notifications based on domain `SecretExpirationSettings` and emits `PROTECTED_RESOURCE_SECRET` events for audit trails:

| Event Action | Description |
|:-------------|:------------|
| `CREATE` | Secret creation event |
| `RENEW` | Secret renewal event |
| `DELETE` | Secret deletion event |

### Configuring Token Exchange

Enable token exchange for an MCP Server by including `urn:ietf:params:oauth:grant-type:token-exchange` in the resource's `settings.oauth.grantTypes` array. This grant type is restricted to MCP Server types only.

**Domain Token Exchange Settings:**

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `tokenExchangeSettings.allowedSubjectTokenTypes` | Array of Strings | `["access_token", "refresh_token", "id_token", "jwt"]` | Token types accepted as subject tokens |
