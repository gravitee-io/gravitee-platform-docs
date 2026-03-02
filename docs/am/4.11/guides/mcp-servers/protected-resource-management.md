### Overview

Protected resources are OAuth2 clients configured for server-to-server communication. Each resource has a unique client ID, supports multiple authentication methods, and validates tokens issued for its audience. Protected resources default to the `client_credentials` grant type and can participate in token exchange flows. They support certificate-based authentication and maintain multiple client secrets with expiration tracking.

### Prerequisites

Before creating or managing protected resources, ensure the following:

* Domain with OAuth2 settings configured
* For token exchange: domain-level token exchange enabled with allowed subject token types
* For certificate authentication: valid X.509 certificate uploaded to the domain
* Appropriate permissions: `PROTECTED_RESOURCE[CREATE]`, `PROTECTED_RESOURCE[UPDATE]`, `PROTECTED_RESOURCE[DELETE]`

### OAuth2 Default Settings

Protected resources are automatically initialized with OAuth2 settings when created or updated. These defaults apply if settings are missing:

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `settings.oauth.grantTypes` | `["client_credentials"]` | Default grant types for server-to-server authentication |
| `settings.oauth.responseTypes` | `["code"]` | Default response types |
| `settings.oauth.tokenEndpointAuthMethod` | `"client_secret_basic"` | Default authentication method |
| `settings.oauth.clientId` | (copied from resource) | Matches the protected resource's client ID |
| `settings.oauth.clientSecret` | (preserved if exists) | Preserved from existing settings during updates |

### Protected Resource Schema

| Property | Type | Description |
|:---------|:-----|:------------|
| `certificate` | String | Certificate ID for TLS client authentication (max 64 chars) |
| `settings.oauth.scopeSettings` | Array | Scope configuration with default scope flags |
| `secretSettings` | Array | Client secret metadata (ID and algorithm) |

### Creating a Protected Resource

Create a protected resource by sending a POST request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources` with the resource name and optional client ID.

1. The system generates a unique client ID if not provided.
2. Default OAuth2 settings are applied automatically, including `client_credentials` grant type and `client_secret_basic` authentication method.
3. An initial client secret is generated with the domain's default expiration period.
4. If certificate-based authentication is required, include the `certificate` property with a valid certificate ID from the domain.
5. The response includes the complete resource configuration with the plaintext secret visible only at creation time.

### Managing Client Secrets

#### Client Secret Lifecycle

Protected resources support multiple concurrent client secrets, each with independent expiration dates. Secrets can be created, renewed, and deleted through the API. The system prevents deletion of the last remaining secret and automatically registers expiration notifications when secrets are created or renewed. Secret values are visible in plaintext only at creation or renewal time.

#### API Endpoints

Manage multiple concurrent secrets for a protected resource through the secrets API at `/protected-resources/{id}/secrets`:

**List Secrets**

```http
GET /protected-resources/{id}/secrets
```

* **Permission Required:** `PROTECTED_RESOURCE[LIST]`
* **Response:** `Array<ClientSecret>` (plaintext values are never returned in list operations)

**Create Secret**

```http
POST /protected-resources/{id}/secrets
Content-Type: application/json

{
  "name": "string"
}
```

* **Permission Required:** `PROTECTED_RESOURCE[CREATE]`
* **Response:** `ClientSecret` (includes plaintext secret value)

**Renew Secret**

```http
POST /protected-resources/{id}/secrets/{secretId}/_renew
```

* **Permission Required:** `PROTECTED_RESOURCE[UPDATE]`
* **Response:** `ClientSecret` (new secret value)

**Delete Secret**

```http
DELETE /protected-resources/{id}/secrets/{secretId}
```

* **Permission Required:** `PROTECTED_RESOURCE[DELETE]`
* **Response:** `204 No Content`
* **Note:** The last remaining secret cannot be deleted.

#### Audit Events

Each secret operation triggers an expiration notification registration and emits audit events:

* `PROTECTED_RESOURCE_SECRET.CREATE`
* `PROTECTED_RESOURCE_SECRET.RENEW`
* `PROTECTED_RESOURCE_SECRET.DELETE`

### Token Exchange for MCP Servers

Token exchange (RFC 8749) allows MCP servers to exchange an existing token (access, refresh, ID, or JWT) for a new access token. The exchanged token inherits the subject's identity but is issued to the MCP server's client ID. Token exchange is restricted to specific grant types and authentication methods, and must be explicitly enabled at the domain level with allowed subject token types configured.

#### Domain-Level Configuration

Configure token exchange at the domain level before enabling it for protected resources:

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `tokenExchangeSettings.enabled` | Boolean | Enable token exchange for the domain | `true` |
| `tokenExchangeSettings.allowedSubjectTokenTypes` | Array<String> | Permitted subject token types for exchange | `["urn:ietf:params:oauth:token-type:access_token", "urn:ietf:params:oauth:token-type:id_token"]` |

**Supported Subject Token Types:**

* `urn:ietf:params:oauth:token-type:access_token`
* `urn:ietf:params:oauth:token-type:refresh_token`
* `urn:ietf:params:oauth:token-type:id_token`
* `urn:ietf:params:oauth:token-type:jwt`

#### Enabling Token Exchange

Enable token exchange for an MCP server by adding the `urn:ietf:params:oauth:grant-type:token-exchange` grant type to the protected resource's OAuth settings:

1. Verify that the domain has `tokenExchangeSettings.enabled = true` and includes the desired subject token types in `allowedSubjectTokenTypes`.
2. Configure the protected resource with allowed grant types: `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange`.
3. Select an authentication method from the MCP-compatible subset: `client_secret_basic`, `client_secret_post`, or `client_secret_jwt`.
4. The MCP server can now exchange tokens by sending a POST to `/oauth/token` with `grant_type=urn:ietf:params:oauth:grant-type:token-exchange`, the subject token, and its type.
5. The response includes an access token with the MCP server's client ID as both issuer and audience, inheriting the subject's identity (`gis` claim) and expiring at the earlier of the subject token's expiration or the MCP server's token lifetime.

#### Grant Type and Authentication Method Restrictions

**For MCP Server Context:**

* **Allowed Grant Types:** `client_credentials`, `urn:ietf:params:oauth:grant-type:token-exchange`
* **Disallowed Grant Types:** `authorization_code`, `implicit`, `password`, `refresh_token`
* **Allowed Authentication Methods:** `client_secret_basic`, `client_secret_post`, `client_secret_jwt`
* **Disallowed Authentication Methods:** `private_key_jwt`, `tls_client_auth`, `self_signed_tls_client_auth`, `none`

### Token Introspection with Protected Resources

Protected resources participate in token introspection by validating audience claims:

1. When a token is introspected, the system extracts the `aud` claim and checks if it matches a protected resource's client ID.
2. For single-audience tokens, the system first checks applications, then protected resources, then validates against RFC 8707 resource identifiers.
3. For multi-audience tokens, all audiences are validated via RFC 8707.
4. If a protected resource is matched and has a certificate configured, the system uses that certificate to verify the JWT signature.
5. If no matching client or resource is found, introspection fails with error `invalid_token` and description "Client or resource not found: {audience}".

### Searching Protected Resources

Search protected resources by name or client ID using the query parameter `q` on the list endpoint:

1. Queries are case-insensitive and match against both the `name` and `clientId` fields.
2. Wildcard support: use `*` to match partial strings (e.g., `clientId*` matches all client IDs starting with "clientId").
3. Results are sorted by `updated_at` in descending order.
4. Pagination is supported via `page` and `size` parameters.

**Example Request:**

```http
GET /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources?q=mcp*&page=0&size=50
```

### Certificate Deletion Validation

When deleting a certificate, the system checks if it's used by any protected resources. If a certificate is referenced by one or more protected resources, deletion fails with:

* **Error:** `CertificateWithProtectedResourceException`
* **HTTP Status:** `400`
* **Message:** "You can't delete a certificate with existing protected resources."

### Managing Protected Resource Membership

Assign users and groups to protected resources through the membership API at `/protected-resources/{id}/members`.

1. List current members with GET, requiring `PROTECTED_RESOURCE_MEMBER[LIST]` permission.
2. Add a member with POST, specifying `memberId`, `memberType` (USER or GROUP), and `role`.
3. Retrieve available permissions for the resource with GET `/members/permissions`.
4. Remove a member with DELETE to `/members/{memberId}`.

Membership management follows the same permission model as applications, with role-based access control determining what operations members can perform on the protected resource.

### Token Exchange Response

The token exchange endpoint returns a JSON response containing the new access token and metadata:

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### Token Claims

The exchanged access token contains the following claims:

* **`client_id`**: The MCP server's client ID (not the original subject token's client)
* **`aud`**: The MCP server's client ID
* **`gis`**: Preserved from the subject token (subject identity)
* **`exp`**: The minimum value between the subject token expiration and the MCP server token lifetime

{% hint style="info" %}
The `client_id` and `aud` claims reflect the MCP server's identity, while the `gis` claim preserves the original subject's identity from the subject token.
{% endhint %}

## Restrictions

The following restrictions apply to protected resources and token exchange in AM:

### Protected resources

* Protected resources must have at least one client secret. The last secret cannot be deleted.
* Certificates used by protected resources cannot be deleted. Attempting to delete a certificate with existing protected resources returns HTTP 400 with the error message: "You can't delete a certificate with existing protected resources."

### Token exchange

* Token exchange requires domain-level enablement.
* The subject token type must be included in the domain's `allowedSubjectTokenTypes` list.
* Token exchange responses never include `refresh_token` or `id_token`, even if the subject token has `openid` scope.

### MCP server context

* Grant types are restricted to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` only.
* Authentication methods are restricted to `client_secret_basic`. 
