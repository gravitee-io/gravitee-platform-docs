### Restrictions

#### Client Secret Management
- At least one client secret must exist per Protected Resource
- Deletion of the last client secret returns `"Cannot delete the last client secret"`

#### MCP Server Grant Type Restrictions
MCP Servers support only the following grant types:
- `client_credentials`
- `urn:ietf:params:oauth:grant-type:token-exchange`

#### MCP Server Token Endpoint Authentication Methods
MCP Servers support only the following token endpoint authentication methods:
- `client_secret_basic`
- `client_secret_post`
- `client_secret_jwt`

#### Token Exchange Constraints
- Exchanged tokens inherit the subject token's expiration; `expires_in` of the new token ≤ subject token's remaining lifetime
- Token exchange does not issue refresh tokens or ID tokens, even if `openid` scope is requested

#### Certificate Deletion
Certificate deletion is blocked if any Protected Resource references the certificate. Attempting to delete a referenced certificate returns `"You can't delete a certificate with existing protected resources."`

#### Search Query Behavior
- Search queries are case-insensitive
- Wildcard (`*`) matching is supported on `name` and `clientId` fields

#### Settings Persistence
Protected Resource settings must be included in the creation request to be persisted. Omitted settings trigger default OAuth values:

| Field | Default Value | Condition |
|:------|:--------------|:----------|
| `grantTypes` | `["client_credentials"]` | If null or empty |
| `responseTypes` | `["code"]` | If null or empty |
| `tokenEndpointAuthMethod` | `"client_secret_basic"` | If null |
| `clientId` | `resource.getClientId()` | If null |
| `clientSecret` | Preserved from existing resource | If null and existing resource has value |
