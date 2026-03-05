### Managing Protected Resource Membership

Add members to a Protected Resource by sending `POST` to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/members` with the following request body:

The response returns a `Member` object with HTTP status 201 Created.

List all members by sending `GET` to `/members`. The response returns a list of `Member` objects.

Remove a member by sending `DELETE` to `/members/{member}`. The response returns HTTP status 204 No Content.

Retrieve the authenticated user's flattened permissions by sending `GET` to `/permissions`. The response returns a list of permissions.

All membership operations check `PROTECTED_RESOURCE_MEMBER` permissions with the following scope cascade:

1. Resource
2. Domain
3. Environment
4. Organization

The system grants access if the user has the required permission at any level in the cascade.

| Operation | Permission | Acl | Scope Cascade |
|:----------|:-----------|:----|:--------------|
| List members | `PROTECTED_RESOURCE_MEMBER` | `LIST` | Resource → Domain → Environment → Organization |
| Add member | `PROTECTED_RESOURCE_MEMBER` | `CREATE` | Resource → Domain → Environment → Organization |
| Remove member | `PROTECTED_RESOURCE_MEMBER` | `DELETE` | Resource → Domain → Environment → Organization |
