### Prerequisites

Before configuring Protected Resources, ensure the following:

* Gravitee Access Management 4.11.0 or later
* Domain with OAuth 2.0 enabled
* `PROTECTED_RESOURCE[CREATE]` permission to create Protected Resources
* `PROTECTED_RESOURCE[UPDATE]` permission to manage secrets and certificates
* Valid certificate uploaded to the domain (if using certificate-based authentication)

### Protected Resource Secrets

Protected Resources authenticate to the authorization server using client secrets managed through a dedicated lifecycle API. Secrets are generated as secure random values, stored in hashed form, and returned in plaintext only once at creation or renewal. Each secret supports expiration dates and algorithm-specific settings. Multiple secrets can be active simultaneously, enabling zero-downtime rotation.

#### Creating a Protected Resource with Secrets

1. Send a POST request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources` with a JSON payload containing `name`, `type`, and optional `certificate` field.
2. The system auto-generates `clientId`, applies default OAuth settings (`client_credentials` grant, `client_secret_basic` auth method), and creates an initial hashed secret.
3. Retrieve the plaintext secret from the response—it will not be accessible again.

#### Adding Additional Secrets

1. Send a POST request to `/protected-resources/{id}/secrets` with a `name` field.
2. The response includes the new plaintext secret.

#### Renewing Secrets

1. Send a POST request to `/secrets/{secretId}/_renew`.
2. The system invalidates the old secret and returns a new one.

#### Deleting Secrets

1. Send a DELETE request to `/secrets/{secretId}` when the secret is no longer needed.

#### OAuth 2.0 Default Settings

Protected Resources are automatically configured with OAuth 2.0 defaults on creation. These settings can be overridden via the `settings` field in the Protected Resource payload.

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `grantTypes` | `["client_credentials"]` | Allowed grant types for token requests |
| `responseTypes` | `["code"]` | OAuth 2.0 response types |
| `tokenEndpointAuthMethod` | `"client_secret_basic"` | Default authentication method for token endpoint |
| `clientId` | (auto-generated) | OAuth 2.0 client identifier |
| `clientSecret` | (auto-generated) | Initial client secret (hashed after creation) |

#### Client Configuration

Protected Resources authenticate to the token endpoint using standard OAuth 2.0 client credentials. The client must configure:

| Property | Description | Example |
|:---------|:------------|:--------|
| `client_id` | Protected Resource's `clientId` | `"pr-abc123"` |
| `client_secret` | Active secret value (obtained at creation/renewal) | `"s3cr3t-v4lu3"` |
| `token_endpoint_auth_method` | Authentication method (must match Protected Resource settings) | `"client_secret_basic"` |
| `grant_type` | `client_credentials` or `urn:ietf:params:oauth:grant-type:token-exchange` | `"client_credentials"` |

Secrets are transmitted only once at creation or renewal. Clients must store secrets securely and rotate them before expiration.

#### Secret Expiration Notifications

Secret expiration notifications extend the existing notification system to support Protected Resources alongside Applications. The `ProtectedResourceSecretManager` listens for `PROTECTED_RESOURCE_SECRET` events (`CREATE`, `RENEW`, `DELETE`) and registers or unregisters expiration notifications accordingly. Secret expiration notifications require the notification system to be enabled at the domain level.

### Certificate-Based JWT Signature Verification

Protected Resources can reference a certificate for JWT signature verification during token introspection. When a token's `aud` claim matches the Protected Resource's `clientId`, the introspection service retrieves the associated certificate ID and uses it to validate the token signature. This enables asymmetric cryptography workflows where the Protected Resource verifies tokens signed by the authorization server's private key.

#### Certificate Configuration

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `certificate` | String | Certificate ID for JWT signature verification | `"cert-abc123"` |

The certificate must exist in the same domain as the Protected Resource. Certificate validation occurs during Protected Resource creation and update operations.

#### Configuring Certificate-Based Authentication

1. Upload a certificate to the domain via the Certificates API.
2. Note the certificate ID from the response.
3. Send a PATCH request to `/protected-resources/{id}` with `{"certificate": "cert-abc123"}` in the request body.
4. The system validates that the certificate exists and belongs to the correct domain.
5. During token introspection, when the token's `aud` claim matches the Protected Resource's `clientId`, the introspection service retrieves this certificate ID for signature validation.

If the certificate is later deleted, the operation fails with `CertificateWithProtectedResourceException` and message "You can't delete a certificate with existing protected resources."

#### Database Schema

**JDBC (`protected_resources` table):**

| Column | Type | Nullable | Description |
|:-------|:-----|:---------|:------------|
| `certificate` | `nvarchar(64)` | `true` | Certificate ID reference |

**MongoDB (`protected_resources` collection):**

| Field | Type | Description |
|:------|:-----|:------------|
| `certificate` | `String` | Certificate ID reference |

### Token Introspection with Protected Resources

When validating a token via introspection, the service examines the `aud` claim to determine the target resource.

#### Single-Audience Tokens

1. Check if `aud` matches an Application's `clientId`—if found, return the Application's certificate.
2. If not found, check if `aud` matches a Protected Resource's `clientId`—if found, return the Protected Resource's certificate.
3. If still not found, validate `aud` as a resource identifier per RFC 8707.

#### Multi-Audience Tokens

For multi-audience tokens, all audiences are validated as resource identifiers.

The returned certificate ID (or empty string for HMAC) is used to verify the token signature. This enables Protected Resources to participate in OAuth 2.0 flows as both clients (requesting tokens) and resource servers (validating tokens).

### Protected Resource Membership

Membership controls which users can manage a Protected Resource.

#### Listing Members

1. Send a GET request to `/protected-resources/{id}/members` (requires `PROTECTED_RESOURCE_MEMBER[LIST]` permission).

#### Adding Members

1. Send a POST request to `/members` with the following payload (requires `PROTECTED_RESOURCE_MEMBER[CREATE]` permission):

```json
{
  "memberId": "user-123",
  "memberType": "USER",
  "role": "OWNER"
}
```

#### Removing Members

1. Send a DELETE request to `/members/{memberId}` (requires `PROTECTED_RESOURCE_MEMBER[DELETE]` permission).

#### Querying Permissions

1. Send a GET request to `/members/permissions` to query available permissions for the current user.
2. The endpoint returns a map of `Permission` to `Set<Acl>` based on organization, environment, domain, and resource-level grants.

### Searching Protected Resources

The Protected Resources list endpoint supports text search via the `q` query parameter. Search matches against `name` and `clientId` fields (case-insensitive) and supports wildcard patterns using `*`.

#### Search Example

```
GET /protected-resources?q=client*&type=MCP_SERVER&page=0&size=50
```

This returns all MCP Server Protected Resources with names or client IDs starting with "client".

#### Search Implementation

The search uses regex patterns in MongoDB (`Pattern.compile("^" + query, CASE_INSENSITIVE)`) and SQL LIKE clauses in JDBC (`upper(pr.name) LIKE :value OR upper(pr.client_id) LIKE :value`). Results are paginated and sorted by `updated_at` descending.

### MCP Server Context Restrictions

Protected Resources operating in MCP Server context are restricted to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types. Token endpoint authentication methods are limited to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`. The following authentication methods are excluded: `private_key_jwt`, `tls_client_auth`, `self_signed_tls_client_auth`, `none`.

The UI automatically filters grant type and authentication method options when the MCP Server context is active, hiding refresh token and PKCE configuration sections.

### Restrictions

* Protected Resources in MCP Server context are limited to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types.
* MCP Server context restricts token endpoint authentication methods to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`.
* Certificates must belong to the same domain as the Protected Resource; cross-domain certificate references are rejected with `InvalidCertificateException`.
* Deleting a certificate fails if any Protected Resources reference it (`CertificateWithProtectedResourceException`).
* Client secrets are returned in plaintext only once (at creation or renewal); subsequent API calls return hashed values only.
* Search queries are case-insensitive and support only prefix wildcards (`*` at end of query).
* Secret expiration notifications require the notification system to be enabled at the domain level.

