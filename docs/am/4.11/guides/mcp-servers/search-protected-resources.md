### Searching Protected Resources

Query Protected Resources via `GET /protected-resources?q={query}`. The `q` parameter is optional and supports wildcard matching.

**Query behavior:**

* If `q` is present, the system searches the `name` and `clientId` fields using case-insensitive matching. Wildcards are supported: `*` matches any characters.
* If `q` is absent, all resources filtered by type are returned.

**Example query:**

`?q=client*` matches resources with names or client IDs starting with "client".

**Response structure:**

Results are paginated and include the following fields:

| Field | Type | Description |
|:------|:-----|:------------|
| `id` | String | Protected Resource identifier |
| `clientId` | String | Client identifier for OAuth authentication |
| `name` | String | Resource name |
| `description` | String | Resource description |
| `type` | String | Resource type (e.g., `MCP_SERVER`) |
| `resourceIdentifiers` | Array | Resource identifier URIs |
| `certificate` | String | Certificate identifier (if configured) |
| `settings` | Object | OAuth settings including grant types, token endpoint auth method, and scope settings |
| `secretSettings` | Array | Secret algorithm configurations |
| `features` | Array | Feature configurations |
| `updatedAt` | String | ISO 8601 timestamp of last update |

**Example request:**

```http
GET /protected-resources?q=mcp-server*
```

**Example response:**

```json
{
  "data": [
    {
      "id": "pr-123",
      "clientId": "mcp-server-123",
      "name": "MCP Server Production",
      "description": "Production MCP server instance",
      "type": "MCP_SERVER",
      "resourceIdentifiers": ["https://api.example.com"],
      "certificate": "cert-456",
      "settings": {
        "oauth": {
          "grantTypes": ["client_credentials"],
          "responseTypes": ["code"],
          "tokenEndpointAuthMethod": "client_secret_basic",
          "clientId": "mcp-server-123",
          "scopeSettings": [
            {
              "scope": "read",
              "defaultScope": true
            }
          ]
        }
      },
      "secretSettings": [
        {
          "id": "secret-settings-789",
          "algorithm": "HS256"
        }
      ],
      "features": [],
      "updatedAt": "2025-01-15T10:30:00Z"
    }
  ],
  "page": 0,
  "size": 10,
  "totalElements": 1
}
```

## Client Configuration

Clients authenticating as Protected Resources use the following properties:

| Property | Description | Example |
|:---------|:------------|:--------|
| `client_id` | Protected Resource `clientId` | `mcp-server-123` |
| `client_secret` | Secret value from creation or renewal response | `a1b2c3d4...` |
| `token_endpoint_auth_method` | Must match `settings.oauth.tokenEndpointAuthMethod` | `client_secret_basic` |
| `grant_type` | `client_credentials` or `urn:ietf:params:oauth:grant-type:token-exchange` | `client_credentials` |

## Restrictions

MCP Server Protected Resources have the following limitations:

* **Grant types**: Only `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` are supported.
* **Token endpoint authentication methods**: Limited to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`.
* **Certificate-based authentication**: 
