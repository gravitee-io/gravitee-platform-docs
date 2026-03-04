### Restrictions and Constraints

Protected Resource management enforces the following technical restrictions:

#### Secret Management Constraints

* At least one secret must exist per Protected Resource. Deletion of the last secret is blocked.
* Secret settings are shared across secrets. Deleting a secret removes its settings only if no other secrets reference them.

#### Certificate Constraints

* Certificates cannot be deleted while referenced by any Protected Resource. Attempting to delete a referenced certificate returns an HTTP 400 error with the message: "You can't delete a certificate with existing protected resources."

#### MCP Server Context Restrictions

When operating in MCP Server context, the following grant types and authentication methods are restricted:

**Allowed Grant Types:**
* `client_credentials`
* `urn:ietf:params:oauth:grant-type:token-exchange`

**Allowed Token Endpoint Authentication Methods:**
* `client_secret_basic`
* `client_secret_post`
* `client_secret_jwt`

User-facing grant types (e.g., `authorization_code`, `password`) and authentication methods are not available in MCP Server context.

#### Token Validation Constraints

* Multi-audience tokens always use RFC 8707 validation regardless of audience content.
* Certificate-based JWT verification requires the `certificate` field to be populated. Null values default to HMAC signing.

## Managing Protected Resource Membership

Membership controls access to Protected Resource management operations. You can add, list, remove members, and query their effective permissions.

### Add a member

Add a member to a Protected Resource:

```
POST /members
```

**Request body:**

```json
{
  "memberId": "string",
  "memberType": "USER | GROUP",
  "role": "string"
}
```

* `memberId`: The unique identifier of the user or group
* `memberType`: Either `USER` or `GROUP`
* `role`: The role to assign to the member

### List members

Retrieve all members assigned to a Protected Resource:

```
GET /members
```

This endpoint returns current membership assignments.

### Remove a member

Remove a member from a Protected Resource:

```
DELETE /members/{member}
```

Replace `{member}` with the member identifier.

### Query flattened permissions

View effective access rights for members:

```
GET /members/permissions
```

This endpoint returns the flattened permissions for all members, showing their effective access rights.

{% hint style="info" %}
All membership operations require `PROTECTED_RESOURCE_MEMBER` permissions at the resource, domain, environment, or organization level.
{% endhint %}
