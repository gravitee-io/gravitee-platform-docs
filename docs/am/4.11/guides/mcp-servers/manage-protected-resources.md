### OAuth 2.0 Settings

When you create or update a Protected Resource, the system applies default OAuth 2.0 settings if none are provided. The following table specifies these defaults:

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `grantTypes` | `["client_credentials"]` | Allowed grant types |
| `responseTypes` | `["code"]` | OAuth response types |
| `tokenEndpointAuthMethod` | `client_secret_basic` | Client authentication method |
| `clientId` | `<resource.clientId>` | Copied from Protected Resource |
| `clientSecret` | `<preserved>` | Retained from existing settings on update |

### Token Exchange Settings

Enable token exchange at the domain level to allow MCP Servers to exchange subject tokens for access tokens:

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `tokenExchangeSettings.enabled` | boolean | Enable token exchange flow | `true` |
| `tokenExchangeSettings.allowedSubjectTokenTypes` | array | Permitted subject token types | `["urn:ietf:params:oauth:token-type:access_token", "urn:ietf:params:oauth:token-type:id_token"]` |

### Creating Protected Resource Secrets

To create a secret, send a POST request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/secrets` with a JSON body:

```json
{
  "name": "string"
}
```

The system generates a random secret value, creates associated OAuth settings, and emits a `PROTECTED_RESOURCE_SECRET.CREATE` event. The response includes the secret value—this is the only time it will be visible:

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

To renew a secret, POST to `/secrets/{secretId}/_renew`. The system generates a new value while preserving the settings ID and emits a `PROTECTED_RESOURCE_SECRET.RENEW` event. The response schema is identical to secret creation.

To delete a secret, send DELETE to `/secrets/{secretId}`. If no other secrets reference the same settings ID, the settings are removed automatically.

### Configuring Certificate-Based Authentication

To enable JWT signature verification for a Protected Resource:

1. Upload a certificate to the domain via the Certificates API.
2. Update the Protected Resource with `{"certificate": "<certificateId>"}`.
3. During token introspection, the system uses this certificate to verify JWT signatures.

If you attempt to delete a certificate that is referenced by one or more Protected Resources, the operation fails with `CertificateWithProtectedResourceException` (HTTP 400):

```
You can't delete a certificate with existing protected resources.
```

Remove the certificate reference from all Protected Resources before deletion.

### Using Token Exchange with MCP Servers

Enable token exchange in the domain settings (`tokenExchangeSettings.enabled = true`) and configure the MCP Server with grant type `urn:ietf:params:oauth:grant-type:token-exchange`. To exchange a token, POST to `/oauth/token`:

```http
POST /oauth/token
Content-Type: application/x-www-form-urlencoded
Authorization: Basic <mcpServerBasicAuth>

grant_type=urn:ietf:params:oauth:grant-type:token-exchange
&subject_token=<token>
&subject_token_type=<type>
```

The response includes an `access_token` with `client_id` and `aud` claims set to the MCP Server's client ID, `gis` claim preserved from the subject token, and `expires_in` capped by the subject token's expiration. No `refresh_token` or `id_token` is issued.

If the domain restricts `allowedSubjectTokenTypes`, only listed types are accepted. Otherwise, the request fails with:

```json
{
  "error": "invalid_request",
  "error_description": "subject_token_type not allowed"
}
```

### Managing Protected Resource Membership

Membership endpoints allow assigning users and roles to Protected Resources.

To list members, GET `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/members`. The response schema:

```json
[
  {
    "id": "string",
    "memberId": "string",
    "memberType": "USER",
    "referenceId": "string",
    "referenceType": "PROTECTED_RESOURCE",
    "role": "string"
  }
]
```

To add a member, POST to `/members` with:

```json
{
  "memberId": "string",
  "memberType": "USER",
  "role": "string"
}
```

To remove a member, DELETE `/members/{member}`.

To retrieve available permissions, GET `/members/permissions`. The response includes:

```json
{
  "PROTECTED_RESOURCE": ["READ", "UPDATE", "DELETE"],
  "PROTECTED_RESOURCE_MEMBER": ["LIST", "CREATE", "DELETE"]
}
```

### Searching Protected Resources

The Protected Resources list endpoint supports a `q` query parameter for text search. Send GET to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources?q=<query>` to search by `name` or `clientId` (case-insensitive). Wildcards are supported: `q=client*` matches `clientId`, `clientId2`, `clientId-test`. Combine with `type`, `page`, and `size` parameters for filtered, paginated results.

Example:

```
GET /protected-resources?q=client*&type=MCP_SERVER&page=0&size=50
```

### Restrictions

- MCP Servers are limited to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types
- Token endpoint authentication methods for MCP Servers exclude `private_key_jwt`, `tls_client_auth`, `self_signed_tls_client_auth`, and `none`
- Protected Resource `resourceIdentifiers` field must not be empty
- All `resourceIdentifiers` within a domain must be unique across Protected Resources
- All feature keys within a Protected Resource must be unique
- Certificates referenced by Protected Resources cannot be deleted until the reference is removed
- Token exchange requires domain-level `tokenExchangeSettings.enabled = true`
- If `allowedSubjectTokenTypes` is configured, only listed token types are accepted in token exchange requests
- Secret values are returned only during creation or renewal; they cannot be retrieved afterward
