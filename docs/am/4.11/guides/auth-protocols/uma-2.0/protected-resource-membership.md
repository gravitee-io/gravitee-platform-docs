### Managing Protected Resource Membership

Membership controls who can administer a Protected Resource. Administrators can delegate management to specific users or groups by assigning roles through the membership API.

#### Listing Members

Retrieve all members assigned to a Protected Resource:

```http
GET /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/members
```

**Required Permission:** `PROTECTED_RESOURCE_MEMBER[LIST]`

**Response:** Array of `Membership` objects.

#### Adding a Member

Assign a user or group to a Protected Resource:

```http
POST /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/members
```

**Required Permission:** `PROTECTED_RESOURCE_MEMBER[CREATE]`

**Request Body:**

```json
{
  "memberId": "string",
  "memberType": "USER|GROUP",
  "role": "string"
}
```

**Parameters:**

* `memberId`: Unique identifier of the user or group
* `memberType`: Either `USER` or `GROUP`
* `role`: Role identifier defining the member's permissions

#### Removing a Member

Remove a user or group from a Protected Resource:

```http
DELETE /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/members/{member}
```

**Required Permission:** `PROTECTED_RESOURCE_MEMBER[DELETE]`

**Response:** `204 No Content`

#### Viewing Flattened Permissions

Retrieve the effective permissions for all members:

```http
GET /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/members/permissions
```

**Required Permission:** `PROTECTED_RESOURCE[READ]`

**Response:** Flattened permission map showing all inherited and direct permissions.

#### Permission Hierarchy

All membership endpoints enforce permissions in the following order:

1. Resource-level: `PROTECTED_RESOURCE[ACL]` on the specific Protected Resource
2. Domain-level: `PROTECTED_RESOURCE[ACL]` on the domain
3. Environment-level: `PROTECTED_RESOURCE[ACL]` on the environment
4. Organization-level: `PROTECTED_RESOURCE[ACL]` on the organization

If a user has the required permission at any level, the operation is authorized.
