### Related Changes

#### UI Changes

The Grant Flows component hides Refresh Token and PKCE settings for MCP Server resources. Token endpoint authentication methods are filtered to client secret variants only (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`).

#### Notification Changes

Client secret expiration notifications now include a `resourceType` field (`"application"` or `"protected resource"`) and use `protectedResourceId` in metadata instead of `applicationId`. Log notification format changed from `"Client Secret %s of application %s in domain %s expires on %s"` to `"Client Secret %s of %s %s in domain %s expires on %s"` to accommodate both Applications and Protected Resources.

#### Permission Implementation

Permission checks for secret and membership operations use `ReferenceType.PROTECTED_RESOURCE` with scope cascade from Resource → Domain → Environment → Organization.

#### Search Implementation

Search queries use MongoDB regex or JDBC `LIKE` with wildcard replacement (`*` to `%` or `.*`) and case-insensitive matching across `name` and `clientId` fields.
