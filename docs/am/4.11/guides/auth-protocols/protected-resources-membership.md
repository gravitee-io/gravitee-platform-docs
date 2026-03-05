### Managing Membership

Users or groups can be assigned to Protected Resources with specific roles to control access.

#### List members

Retrieve all members assigned to a Protected Resource:

1. Send a `GET` request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/members`.
2. The response returns a list of members with their assigned roles.

**Required permission:** `PROTECTED_RESOURCE_MEMBER[LIST]`

#### Add a member

Assign a user or group to a Protected Resource:

1. Send a `POST` request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/members`.
2. Include the following fields in the request body:
   * `memberId`: The ID of the user or group
   * `memberType`: The type of member (user or group)
   * `role`: The role to assign

**Required permission:** `PROTECTED_RESOURCE_MEMBER[CREATE]`

**Response:** `201 Created` with the created membership details.

#### Remove a member

Remove a user or group from a Protected Resource:

1. Send a `DELETE` request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/members/{member}`.

**Required permission:** `PROTECTED_RESOURCE_MEMBER[DELETE]`

**Response:** `204 No Content`

#### Query permissions

Retrieve the flattened permissions for the current user on a Protected Resource:

1. Send a `GET` request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/permissions`.
2. The response returns a permission map showing all permissions granted to the current user.

**Required permission:** `PROTECTED_RESOURCE[READ]`

### Searching Protected Resources

Query Protected Resources by name or client ID using wildcard patterns.

1. Send a `GET` request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources` with the following query parameters:
   * `q`: Search string (supports `*` wildcards)
   * `type`: Resource type filter
   * `page`: Page number (default: 0)
   * `size`: Page size (default: 50)
2. The search is case-insensitive and matches against `name` and `clientId` fields.
3. Results are sorted by `updatedAt` in descending order and returned as a paginated response with total count.

**Required permission:** `PROTECTED_RESOURCE[READ]`

**Example:** `q=clientId*` matches `clientId`, `clientId2`, and `clientIdTest`.

### Token Introspection with Protected Resources

When introspecting a token, the system resolves the audience claim to determine the resource server.

1. The system decodes the JWT and extracts the audience claim (`aud`).
2. For a single audience matching a client ID:
   * The system queries `ClientSyncService`.
   * If not found, the system queries `ProtectedResourceSyncService`.
   * If still not found, the system validates the audience as a resource identifier.
3. For multiple audiences, the system validates all as resource identifiers.
4. The system resolves the certificate for JWT verification:
   * If the client or resource has a `certificate` field, the system uses it.
   * If null, the system assumes an HMAC-signed token.
5. The introspection response includes `client_id` and `aud` set to the resolved client or resource ID.
