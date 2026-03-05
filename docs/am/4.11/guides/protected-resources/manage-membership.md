### Managing Protected Resource Membership

Protected Resources support role-based access control through user and group membership assignments. Membership operations follow a hierarchical permission model that checks resource-level, domain-level, environment-level, and organization-level permissions in sequence.

#### Assigning Members

Assign users or groups to a Protected Resource via `POST /protected-resources/{id}/members`. The request body requires:

The `memberType` field accepts `USER` or `GROUP`. This operation requires `PROTECTED_RESOURCE_MEMBER[CREATE]` permission.

#### Listing Members

Retrieve all members assigned to a Protected Resource via `GET /members`. The response returns an array of `Membership` objects. This operation requires `PROTECTED_RESOURCE_MEMBER[LIST]` permission.

#### Removing Members

Remove a user or group from a Protected Resource via `DELETE /members/{member}`. The endpoint returns `204 No Content` on successful deletion. This operation requires `PROTECTED_RESOURCE_MEMBER[DELETE]` permission.

#### Retrieving Permissions

Retrieve a flattened permission map for the current user via `GET /members/permissions`. The response includes all permissions the user has on the Protected Resource, resolved through the hierarchical permission model. This operation requires `PROTECTED_RESOURCE[READ]` permission.

#### Permission Hierarchy

All membership operations follow a hierarchical permission check:

1. Resource-level: `PROTECTED_RESOURCE[ACL]` on the specific resource
2. Domain-level: `PROTECTED_RESOURCE[ACL]` on the domain
3. Environment-level: `PROTECTED_RESOURCE[ACL]` on the environment
4. Organization-level: `PROTECTED_RESOURCE[ACL]` on the organization

The system grants access if any level in the hierarchy satisfies the required permission.
