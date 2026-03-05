### Managing Protected Resource Memberships

Members can be added to a Protected Resource to grant specific permissions based on assigned roles. Members must be defined in the domain's identity providers before they can be added.

#### Prerequisites

Users or groups must be defined in the domain identity providers.

#### Add a member

Add a member to a Protected Resource via `POST /protected-resources/{id}/members` with a JSON body specifying `memberId`, `memberType` (e.g., `"USER"`), and `role`. Members inherit permissions based on their assigned role.

**Request Body:**

#### View members

To view current members, call `GET /protected-resources/{id}/members`. This endpoint requires the `PROTECTED_RESOURCE_MEMBER[LIST]` permission.

#### Remove a member

Remove a member with `DELETE /protected-resources/{id}/members/{memberId}`.

#### Check authenticated user's permissions

The authenticated user's permissions on a specific resource can be retrieved via `GET /protected-resources/{id}/members/permissions`. Permission checks occur at resource, domain, environment, and organization levels in that order.

**Permission Hierarchy:**
1. Resource-level: `PROTECTED_RESOURCE_MEMBER[ACL]` on specific resource
2. Domain-level: `PROTECTED_RESOURCE_MEMBER[ACL]` on domain
3. Environment-level: `PROTECTED_RESOURCE_MEMBER[ACL]` on environment
4. Organization-level: `PROTECTED_RESOURCE_MEMBER[ACL]` on organization

**ACLs:**
- `LIST` — View members
- `CREATE` — Add/update members
- `DELETE` — Remove members
- `READ` — View permissions
