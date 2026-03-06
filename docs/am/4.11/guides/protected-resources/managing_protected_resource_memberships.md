### Managing Protected Resource Memberships

Add a member by sending a POST request to `/organizations/{orgId}/environments/{envId}/domains/{domainId}/protected-resources/{resourceId}/members` with the following JSON body:

```json
{
  "memberId": "user-id",
  "memberType": "USER",
  "role": "OWNER"
}
```

The `memberType` field must be set to `USER`. The `role` field specifies the role assigned to the member.

To remove a member, send a DELETE request to `/members/{memberId}`.

To view all members of a Protected Resource, send a GET request to `/members`. This operation requires the `PROTECTED_RESOURCE_MEMBER[LIST]` permission.

To check your own permissions on a Protected Resource, send a GET request to `/members/permissions`. This operation requires the `PROTECTED_RESOURCE[READ]` permission.

#### Permission Hierarchy

Permissions are evaluated hierarchically. Resource-level ACLs override domain-level ACLs, which override environment-level ACLs, which override organization-level ACLs. The system checks permissions in the following order:

1. Resource-level: `PROTECTED_RESOURCE_MEMBER[ACL]` on the specific Protected Resource
2. Domain-level: `PROTECTED_RESOURCE_MEMBER[ACL]` on the domain
3. Environment-level: `PROTECTED_RESOURCE_MEMBER[ACL]` on the environment
4. Organization-level: `PROTECTED_RESOURCE_MEMBER[ACL]` on the organization

The following ACL actions are supported:

* `LIST` — View members
* `CREATE` — Add or update members
* `DELETE` — Remove members
* `READ` — View permissions
