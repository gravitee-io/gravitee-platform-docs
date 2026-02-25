## Protected Resource secret management overview

Protected Resource secret management enables OAuth2-compliant credential rotation and certificate-based authentication for MCP Servers in Gravitee Access Management. Administrators can create, renew, and delete multiple client secrets per Protected Resource through REST endpoints, while the system automatically applies OAuth2 defaults and validates token audiences during introspection.

### Protected Resources as OAuth2 clients

Protected Resources function as OAuth2 clients with full credential lifecycle management. Each resource receives default OAuth2 settings on creation:
- `client_credentials` grant type
- `code` response type
- `client_secret_basic` token endpoint authentication method

The system preserves user-provided `clientSecret` values during updates while applying defaults to missing fields.

### Multi-secret rotation

A Protected Resource can maintain multiple active secrets simultaneously. Each secret includes:
- Name
- Raw secret value
- Algorithm-specific settings
- Optional expiration date

When a secret is deleted, the system automatically removes orphaned secret settings entries that no longer reference any active secrets.

### Certificate-based authentication

Protected Resources support an optional `certificate` field that references a domain certificate ID. During token introspection, the system resolves this certificate for signature verification. If no certificate is assigned, the system assumes HMAC signing and returns an empty certificate ID.

The certificate field must reference an existing certificate ID in the domain. Invalid IDs are rejected.

For instructions on uploading and managing domain certificates, see [Certificate management](../certificates/README.md).

## Prerequisites

- Gravitee Access Management domain configured
- Organization and environment IDs available
- User permissions: `DOMAIN_PROTECTED_RESOURCE` scope with `CREATE`, `READ`, `UPDATE`, `DELETE` actions
- For certificate authentication: valid certificate uploaded to the domain

## Gateway configuration

### Protected Resource fields

| Property | Description | Example |
|:---------|:------------|:--------|
| `certificate` | Certificate ID for signature verification | `"cert-abc123"` |
| `settings.oauth.grantTypes` | Allowed OAuth2 grant types | `["client_credentials"]` |
| `settings.oauth.responseTypes` | Allowed OAuth2 response types | `["code"]` |
| `settings.oauth.tokenEndpointAuthMethod` | Token endpoint authentication method | `"client_secret_basic"` |
| `settings.oauth.clientId` | OAuth2 client identifier | Copied from resource `clientId` |
| `settings.oauth.clientSecret` | OAuth2 client secret | Preserved from existing settings |
| `secretSettings` | Array of secret algorithm configurations | `[{"id": "ss-1", "algorithm": "HS256"}]` |

### Secret management endpoints

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets` | GET | List all secrets for a Protected Resource |
| `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets` | POST | Create a new secret |
| `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets/{secretId}/_renew` | POST | Renew an existing secret |
| `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets/{secretId}` | DELETE | Delete a secret |

### Secret response schema

| Property | Description | Example |
|:---------|:------------|:--------|
| `id` | Unique secret identifier | `"secret-xyz789"` |
| `name` | User-provided secret name | `"Production Secret"` |
| `secret` | Raw secret value (returned only on creation/renewal) | `"s3cr3t_v4lu3"` |
| `settingsId` | Reference to secret settings entry | `"ss-1"` |
| `expiresAt` | Optional expiration timestamp | `"2024-12-31T23:59:59Z"` |
| `createdAt` | Secret creation timestamp | `"2024-01-15T10:30:00Z"` |

## Creating a Protected Resource

Create a Protected Resource by sending a POST request to:

```
/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources
```

**Request body:**

```json
{
  "name": "Resource Name",
  "clientId": "unique-client-id",
  "certificate": "cert-abc123"
}
```

The `certificate` field is optional. If provided, it must reference an existing certificate ID in the domain.

The system automatically applies OAuth2 defaults on creation:
- `grantTypes`: `["client_credentials"]`
- `responseTypes`: `["code"]`
- `tokenEndpointAuthMethod`: `"client_secret_basic"`

## Generating the first client secret

After creating a Protected Resource, generate the first client secret:

1. Send a POST request to:
   ```
   /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets
   ```

2. Include a JSON body with the secret name:
   ```json
   {
     "name": "Secret Name"
   }
   ```

3. The response includes the raw secret value:
   ```json
   {
     "id": "secret-xyz789",
     "name": "Secret Name",
     "secret": "s3cr3t_v4lu3",
     "settingsId": "ss-1",
     "createdAt": "2024-01-15T10:30:00Z"
   }
   ```

{% hint style="warning" %}
The raw secret value is returned only once. Store it securely. Subsequent GET requests omit the raw secret.
{% endhint %}

## Creating additional secrets

Generate additional secrets for an existing Protected Resource:

1. Send a POST request to:
   ```
   /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets
   ```

2. Provide a unique name in the request body:
   ```json
   {
     "name": "Additional Secret Name"
   }
   ```

Each secret receives its own ID, algorithm settings, and optional expiration date. The system maintains all active secrets in the `secretSettings` array, allowing gradual rotation without service interruption.

## Renewing a secret

Renew an existing secret to generate a new value while preserving the name and settings ID:

1. Send a POST request to:
   ```
   /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets/{secretId}/_renew
   ```

2. The response includes the new secret value:
   ```json
   {
     "id": "secret-xyz789",
     "name": "Secret Name",
     "secret": "n3w_s3cr3t_v4lu3",
     "settingsId": "ss-1",
     "createdAt": "2024-01-15T10:30:00Z"
   }
   ```

## Deleting a secret

Delete a secret by sending a DELETE request to:

```
/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets/{secretId}
```

The system automatically deletes orphaned secret settings entries when the last referencing secret is removed.

## Listing all secrets

Retrieve all secrets for a Protected Resource by sending a GET request to:

```
/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets
```

The response includes all secrets without raw secret values:

```json
[
  {
    "id": "secret-xyz789",
    "name": "Secret Name",
    "settingsId": "ss-1",
    "createdAt": "2024-01-15T10:30:00Z"
  }
]
```

## Searching Protected Resources

Search for Protected Resources using the `q` query parameter:

```
/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources?q=prod*
```

The system performs case-insensitive wildcard matching against both `name` and `clientId` fields:
- `?q=prod*` returns all resources with names or client IDs starting with "prod"
- `?q=production` returns exact matches for "production"

Regex patterns aren't supported.

## Token introspection with Protected Resources

During token introspection, the system validates JWT audiences against both Applications and Protected Resources.

**Single-audience tokens:**
The introspection service first attempts to resolve the audience as a client ID by checking Applications, then Protected Resources. If found, it returns the associated certificate ID for signature verification or an empty string for HMAC.

**Multi-audience tokens:**
The system validates all audiences using RFC 8707 resource identifier rules.

This dual-lookup mechanism ensures Protected Resources are recognized as valid token audiences alongside traditional OAuth2 clients.

## Console UI integration

### Certificate field in Protected Resource forms

Protected Resources support an optional `certificate` field that references a domain certificate ID. This field enables certificate-based authentication for signature verification during token introspection.

**To configure certificate authentication:**

1. Upload a valid certificate to your domain.
2. When creating or updating a Protected Resource, include the `certificate` field with the certificate ID.
3. During token introspection, the system automatically resolves the certificate for signature verification.

If no certificate is assigned, the system assumes HMAC signing and returns an empty certificate ID.

### Secret management interface

The secret management interface provides controls for creating, renewing, deleting, and listing client secrets for Protected Resources. Each secret includes:

- **Name**: User-provided identifier for the secret
- **Secret value**: Raw credential displayed only on creation or renewal
- **Expiration date**: Optional timestamp for automatic expiration
- **Settings ID**: Reference to algorithm-specific configuration

#### Creating secrets

To create a new secret:

1. Navigate to the Protected Resource in the Console UI.
2. Access the secret management interface.
3. Enter a unique name for the secret.
4. Optionally set an expiration date.
5. Submit the form to generate the secret.

The system displays the raw secret value once. Store this value securely—subsequent views will not show it.

#### Renewing secrets

To renew an existing secret:

1. Select the secret from the list.
2. Click the renew action.
3. The system generates a new secret value while preserving the name and settings ID.
4. Store the new secret value securely.

#### Deleting secrets

To delete a secret:

1. Select the secret from the list.
2. Click the delete action.
3. Confirm the deletion.

When a secret is deleted, the system automatically removes orphaned secret settings entries that no longer reference any active secrets.

#### Listing secrets

The secret list displays:

- Secret name
- Settings ID
- Expiration date (if configured)
- Creation timestamp

The raw secret value is never displayed in the list view.

## Architecture notes

### Secret settings lifecycle

Secret settings entries are shared across multiple secrets when they use the same algorithm. The system tracks references and automatically deletes settings entries when the last referencing secret is removed. This prevents orphaned configuration data while allowing efficient reuse of algorithm parameters.

### MCP Server token endpoint filtering

When operating in MCP Server context, the system restricts available token endpoint authentication methods to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`. This filtering occurs in the `GrantFlowsComponent.filteredTokenEndpointAuthMethods()` method and ensures MCP Servers use only secret-based authentication flows.

### OAuth2 auth provider integration

The OAuth2 authentication provider now recognizes Protected Resources during token decoding. After introspecting a token, the provider attempts to resolve the JWT audience as an Application client ID, then as a Protected Resource client ID. If neither lookup succeeds, the provider rejects the token with an `InvalidTokenException` containing the message "Client or resource not found: {audience}".

### ProtectedResourceSecretEvent enum

The `ProtectedResourceSecretEvent` enum introduces three new event types for audit logging and webhook integrations:

- **CREATE**: Triggered when a new secret is generated for a Protected Resource
- **RENEW**: Triggered when an existing secret is renewed via the `/_renew` endpoint
- **DELETE**: Triggered when a secret is removed from a Protected Resource

These events track the complete secret lifecycle and enable monitoring of credential rotation operations through AM's audit log and webhook systems.

## Restrictions

- Secret values are returned only during creation and renewal operations; subsequent GET requests omit the raw secret
- Certificate field must reference an existing certificate ID in the domain; invalid IDs are rejected
- Secret settings cleanup occurs only when no secrets reference a settings entry
- Token endpoint authentication methods are restricted to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt` in MCP Server context
- Search functionality supports only wildcard (`*`) and exact match patterns; regex is not supported
- Permission checks for Application resources use `ReferenceType.APPLICATION` consistently across all operations
- Default OAuth2 settings are applied only when corresponding fields are null or empty; existing values are preserved

## Related changes

The Management API now exposes five new REST endpoints for Protected Resource secret management under the `/secrets` path. The Console UI requires updates to display the certificate field in Protected Resource forms and to provide secret management controls. Token introspection logic was enhanced to recognize Protected Resources as valid audiences, requiring coordination with any custom introspection implementations.

