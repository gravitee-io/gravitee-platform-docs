### Searching Protected Resources

The protected resources list endpoint accepts a `q` query parameter for search. When provided, the system performs a case-insensitive search across `name` and `clientId` fields. Use `*` as a wildcard for partial matching (e.g., `q=prod*` matches resources starting with "prod"). Results are paginated and sorted by `updatedAt` descending. Omitting `q` returns all protected resources filtered by type.

**Endpoint:** `GET /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources`

**Query Parameter:**

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `q` | String | Search query (supports wildcards with `*`) |

## Restrictions

The following restrictions apply when using token exchange and Model Context Protocol (MCP) servers:

### Token exchange

* Token exchange grant type must be explicitly enabled in domain settings.
* Subject token types must be in the domain's `allowedSubjectTokenTypes` list.
* Requested token type must be `urn:ietf:params:oauth:token-type:access_token` or omitted.
* Token exchange never issues refresh tokens or ID tokens.
* Issued token expiration cannot exceed the subject token's remaining lifetime.

### MCP servers

* MCP servers cannot use `authorization_code`, `implicit`, `password`, or `refresh_token` grant types.
* MCP servers cannot use `private_key_jwt`, `tls_client_auth`, `self_signed_tls_client_auth`, or `none` authentication methods.

### Protected resources

* Protected resource secrets require a `name` field.
* Secret renewal requires an existing secret with matching `secretId`.
* Certificate deletion fails if referenced by any protected resource.

### Token introspection

* Token introspection with protected resources requires the JWT `aud` claim to match the resource's `clientId`.
* Multiple audiences in a JWT always trigger RFC 8707 resource identifier validation.

### Protected Resource Membership

Membership endpoints enable role-based access control for protected resources.

**Base Path:** `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/members`

#### Add a Member

**Endpoint:** `POST /members`

**Permission Required:** `PROTECTED_RESOURCE_MEMBER[CREATE]`

**Request Body:**

```json
{
  "memberId": "string",
  "memberType": "USER|GROUP",
  "role": "string"
}
```

**Response:** `Member`

The system creates the membership and returns the member object.

#### Remove a Member

**Endpoint:** `DELETE /members/{member}`

**Permission Required:** `PROTECTED_RESOURCE_MEMBER[DELETE]`

**Response:** `204 No Content`

#### Retrieve All Members

**Endpoint:** `GET /members`

**Permission Required:** `PROTECTED_RESOURCE_MEMBER[LIST]`

**Response:** `Array<Member>`

#### View Available Permissions

**Endpoint:** `GET /members/permissions`

**Permission Required:** `PROTECTED_RESOURCE[READ]`

**Response:** `Map<Permission, List<Acl>>`
