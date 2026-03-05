### Restrictions and Constraints

Protected Resources are subject to the following technical restrictions and validation rules:

#### Uniqueness Requirements

* **Resource identifiers:** Must be unique across all Protected Resources in a domain.
* **Feature keys:** Must be unique within a single Protected Resource.

#### Certificate Management

Certificates in use by Protected Resources, Applications, or Identity Providers cannot be deleted. Attempting to delete a certificate that is referenced by any Protected Resource will result in an error.

#### MCP Server Limitations

MCP Servers support only the following grant types:

* `client_credentials`
* `urn:ietf:params:oauth:grant-type:token-exchange`

Token endpoint authentication methods for MCP Servers are restricted to:

* `client_secret_basic`
* `client_secret_post`
* `client_secret_jwt`
* `null` (based on incoming request)

#### Token Exchange Constraints

* Exchanged tokens never include refresh tokens or ID tokens, even if the subject token has `offline_access` or `openid` scopes.
* Exchanged token expiration cannot exceed the subject token's expiration.

#### Secret Management

* Last secret deletion is allowed. No minimum secret count is enforced.

#### Search Functionality

Search queries are limited to the `name` and `clientId` fields. Wildcard matching is supported using the `*` character. Results are sorted by `updatedAt` descending and returned as a paginated response with total count.

Example: `q=clientId*` matches `clientId`, `clientId2`, and `clientIdTest`.

### Token Introspection with Protected Resources

When introspecting a token, the system resolves the audience claim to determine the resource server:

1. **Single audience matching a client ID:** The system queries `ClientSyncService`, then `ProtectedResourceSyncService`, and finally validates as a resource identifier via `ProtectedResourceManager`.
2. **Multiple audiences:** All audiences are validated as resource identifiers per RFC 8707.
3. **Certificate resolution:** If the resolved client or resource has a `certificate` field, it is used for JWT verification. Otherwise, HMAC verification is assumed.
4. **Introspection response:** The response includes `client_id` and `aud` set to the resolved client or resource ID.
