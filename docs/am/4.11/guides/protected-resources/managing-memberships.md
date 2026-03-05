### Managing memberships

Assign users or groups to Protected Resources to control access via role-based permissions. Membership management follows the same pattern as Application memberships.

#### Assign a member

Add a user or group to a Protected Resource:

```
POST /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/members
```

**Request body:**

```json
{
  "memberId": "string",
  "memberType": "USER",
  "role": "string"
}
```

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `memberId` | String | Yes | User or group identifier |
| `memberType` | String | Yes | Member type (`USER` or `GROUP`) |
| `role` | String | Yes | Role identifier  |

#### List members

Retrieve all members assigned to a Protected Resource:

```
GET /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/members
```

**Query parameters:**

| Parameter | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `page` | Integer | No | Page number (default: 0) |
| `size` | Integer | No | Page size  |

**Response:**

```json
{
  "data": [
    {
      "id": "string",
      "memberId": "string",
      "memberType": "USER",
      "referenceId": "string",
      "referenceType": "PROTECTED_RESOURCE",
      "role": "string"
    }
  ],
  "currentPage": 0,
  "totalCount": 1
}
```

#### Retrieve available permissions

List permission scopes available for Protected Resource memberships:

```
GET /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/members/permissions
```

**Response:**

```json
{
  "PROTECTED_RESOURCE": ["READ", "UPDATE", "DELETE"],
  "PROTECTED_RESOURCE_MEMBER": ["LIST", "CREATE", "DELETE"]
}
```

| Scope | Permissions | Description |
|:------|:------------|:------------|
| `PROTECTED_RESOURCE` | `READ`, `UPDATE`, `DELETE` | Permissions for managing the Protected Resource itself |
| `PROTECTED_RESOURCE_MEMBER` | `LIST`, `CREATE`, `DELETE` | Permissions for managing Protected Resource memberships |

#### Remove a member

Delete a user or group from a Protected Resource:

```
DELETE /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/members/{member}
```

## Searching Protected Resources

To search for protected resources, use the following endpoint:

```
GET /protected-resources?q={query}&type={type}&page={page}&size={size}
```

### Query Parameters

* **`q`**: Search query that supports wildcard matching (`*`) on `name` and `clientId` fields. Matching is case-insensitive.
* **`type`**: Filter results by resource type (e.g., `type=MCP_SERVER`).
* **`page`**: Page number for pagination.
* **`size`**: Number of resources per page. Default is 50.

### Response

The response includes:

* Full resource details:
  * Settings
  * Certificate ID
  * Resource identifiers
  * Update timestamps
* Pagination metadata:
  * `currentPage`
  * `totalCount`

{% hint style="info" %}
Use wildcard matching to search across multiple resources. For example, `q=api*` returns all resources with names or client IDs starting with "api".
{% endhint %}

## Token Introspection Configuration

When introspecting tokens, AM resolves the `aud` claim using the following process:

1. Check registered clients via `ClientSyncService`
2. Check Protected Resources via `ProtectedResourceSyncService`

If the audience matches a Protected Resource's `clientId`, AM uses that resource's `certificate` for JWT verification. If no certificate is configured, AM uses HMAC for verification.

### Multiple Audiences

For tokens with multiple audiences, AM:

* Validates each audience as a resource identifier
* Ensures all audiences belong to the token's domain
* If RFC 8707 legacy mode is enabled, verifies the caller's client ID matches one audience

### Validation Errors

Tokens with unresolvable audiences trigger an `InvalidTokenException` with the following message:

```
Client or resource not found: {aud}
```

{% hint style="info" %}
The `aud` claim resolution process prioritizes registered clients before checking Protected Resources.
{% endhint %}
