### Searching Protected Resources

Search Protected Resources using `GET /protected-resources` with the following query parameters:

| Parameter | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `q` | String | No | Search query supporting wildcard matching (`*`) on `name` and `clientId` fields (case-insensitive) |
| `type` | String | No | Filter by resource type (e.g., `type=MCP_SERVER`) |
| `page` | Integer | No | Page number (default: 0) |
| `size` | Integer | No | Page size (default: 50) |

**Response:**

```json
{
  "data": [
    {
      "id": "string",
      "clientId": "string",
      "name": "string",
      "description": "string",
      "type": "MCP_SERVER",
      "resourceIdentifiers": ["https://example.com"],
      "certificate": "cert-id",
      "settings": { "oauth": { ... } },
      "updatedAt": "2025-01-01T00:00:00Z"
    }
  ],
  "currentPage": 0,
  "totalCount": 1
}
```

The response includes full resource details (settings, certificate ID, resource identifiers, update timestamps) with pagination metadata (`currentPage`, `totalCount`).

## Restrictions

AM MCP Servers are subject to the following restrictions:

* **Grant types**: MCP Servers support only `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types.
* **Authentication methods**: MCP Servers cannot use `private_key_jwt`, `tls_client_auth`, or `self_signed_tls_client_auth` authentication methods.
* **Token exchange limitations**:
  * Token exchange never issues refresh tokens or ID tokens, even when the `openid` scope is requested.
  * Exchanged token expiration cannot exceed the subject token's remaining lifetime.
* **Certificate deletion**: Certificates used by Protected Resources cannot be deleted. Attempting to delete a certificate in use triggers a `CertificateWithProtectedResourceException` with HTTP 400.
* **Secret retrieval**: Secret values are returned only on creation or renewal. The `GET /secrets` endpoint returns metadata only.
* **Protected Resource updates**: The Protected Resource `settings` field is not copied during update unless explicitly provided in the request body.
* **Token introspection**: Token introspection requires the audience to resolve to either a registered client or Protected Resource. Unresolvable audiences fail with `InvalidTokenException`.
