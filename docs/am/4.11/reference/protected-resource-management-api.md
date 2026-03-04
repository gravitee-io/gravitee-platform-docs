### Managing Protected Resource Memberships

Add members to a Protected Resource by calling `POST /protected-resources/{id}/members` with the following request body:

```json
{
  "memberId": "user-or-group-id",
  "memberType": "USER|GROUP",
  "role": "role-name"
}
```

The `memberType` field accepts either `USER` or `GROUP`. The `role` field specifies the role assigned to the member within the Protected Resource context.

List all members by calling `GET /protected-resources/{id}/members`. The response returns an array of membership objects.

Retrieve flattened permissions for all members by calling `GET /protected-resources/{id}/members/permissions`. This endpoint returns a consolidated permission map for the Protected Resource.

Remove a member by calling `DELETE /protected-resources/{id}/members/{memberId}`. The system removes the membership association.

Membership operations require the following permissions scoped to the Protected Resource:

| Operation | Required Permission |
|:----------|:-------------------|
| List members | `PROTECTED_RESOURCE_MEMBER[LIST]` |
| Add member | `PROTECTED_RESOURCE_MEMBER[CREATE]` |
| Remove member | `PROTECTED_RESOURCE_MEMBER[DELETE]` |
| Retrieve permissions | `PROTECTED_RESOURCE[READ]` |

**Example Request (Add Member):**

```json
POST /protected-resources/pr-123/members

{
  "memberId": "user-456",
  "memberType": "USER",
  "role": "READER"
}
```

**Example Response (List Members):**

```json
[
  {
    "memberId": "user-456",
    "memberType": "USER",
    "role": "READER"
  },
  {
    "memberId": "group-789",
    "memberType": "GROUP",
    "role": "ADMIN"
  }
]
```

## Client Configuration

Clients authenticating as Protected Resources use the following properties:

| Property | Description | Example |
|----------|-------------|---------|
| `client_id` | Protected Resource `clientId` | `mcp-server-123` |
| `client_secret` | Secret value from creation or renewal response |  |

## Renewing or Deleting Secrets

### Renew a Secret

To renew a secret, call the following endpoint:

```
POST /protected-resources/{id}/secrets/{secretId}/_renew
```

The response contains the new plaintext value of the secret.

### Delete a Secret

To delete a secret, call the following endpoint:

```
DELETE /protected-resources/{id}/secrets/{secretId}
```

The system removes the secret from `clientSecrets` and removes the associated `secretSettings` entry only if no other secret references it.

### List All Secrets

To list all secrets without plaintext values, call the following endpoint:

```
GET /protected-resources/{id}/secrets
```
