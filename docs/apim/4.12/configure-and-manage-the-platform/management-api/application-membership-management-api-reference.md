# Application Membership Management API Reference

## Management API

### Search Members

```
POST /applications/{applicationId}/members/_search
```

**Query Parameters**

| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `page` | Integer | `1` | Page number for pagination |
| `size` | Integer | `10` | Number of results per page |

**Request Body**

```json
{
  "filters": {
    "displayName": "string"
  }
}
```

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `filters.displayName` | String | No | Filter members by display name |

**Response**

```json
{
  "data": [
    {
      "id": "string",
      "user": {
        "id": "string",
        "display_name": "string",
        "first_name": "string",
        "last_name": "string",
        "email": "string",
        "_links": { "avatar": "string" }
      },
      "role": "string",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "metadata": {
    "pagination": {
      "current_page": 1,
      "total": 42,
      "size": 10
    }
  }
}
```

| Field | Type | Description |
|:------|:-----|:------------|
| `data` | Array | List of application members |
| `data[].id` | String | Member ID |
| `data[].user` | Object | User details |
| `data[].user.id` | String | User ID |
| `data[].user.display_name` | String | User display name |
| `data[].user.first_name` | String | User first name |
| `data[].user.last_name` | String | User last name |
| `data[].user.email` | String | User email address |
| `data[].user._links.avatar` | String | URL to user avatar image |
| `data[].role` | String | Application role assigned to the member |
| `data[].created_at` | String | ISO 8601 timestamp of member creation |
| `data[].updated_at` | String | ISO 8601 timestamp of last update |
| `metadata.pagination` | Object | Pagination metadata |
| `metadata.pagination.current_page` | Integer | Current page number |
| `metadata.pagination.total` | Integer | Total number of members |
| `metadata.pagination.size` | Integer | Number of results per page |

### Create Member

```
POST /applications/{applicationId}/members
```

**Request Body**

```json
{
  "user": "string",
  "reference": "string",
  "role": "string"
}
```

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `user` | String | Yes | User ID |
| `reference` | String | Yes | User reference |
| `role` | String | No | Application role to assign (defaults to lowest application role if omitted) |

**Response**

HTTP 201 Created

### Update Member

```
PUT /applications/{applicationId}/members/{memberId}
```

**Request Body**

```json
{
  "role": "string"
}
```

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `role` | String | Yes | New application role to assign |

**Response**

```json
{
  "id": "string",
  "role": "string"
}
```

| Field | Type | Description |
|:------|:-----|:------------|
| `id` | String | Member ID |
| `role` | String | Updated application role |

### Transfer Ownership

```
POST /applications/{applicationId}/members/_transfer_ownership
```

**Request Body**

```json
{
  "new_primary_owner_id": "string",
  "new_primary_owner_reference": "string",
  "primary_owner_newrole": "string"
}
```

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `new_primary_owner_id` | String | Yes | User ID of the new primary owner |
| `new_primary_owner_reference` | String | Yes | User reference of the new primary owner |
| `primary_owner_newrole` | String | Yes | Application role to assign to the current primary owner |

**Response**

HTTP 204 No Content

### Create Invitations

```
POST /applications/{applicationId}/invitations
```

**Request Body**

```json
{
  "recipients": [
    { "email": "user@example.com" }
  ],
  "role": "USER",
  "notify": true,
  "confirmation_page_url": "https://portal.example.com/user/invitation/confirm"
}
```

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `recipients` | Array | Yes | List of invitation recipients |
| `recipients[].email` | String | Yes | Email address of the recipient |
| `role` | String | Yes | Application role to assign |
| `notify` | Boolean | No | Whether to send email notifications (defaults to `true`) |
| `confirmation_page_url` | String | No | URL for invitation confirmation page (auto-generated if omitted) |

**Response**

HTTP 201 Created

```json
{
  "data": [
    {
      "id": "string",
      "email": "string",
      "role": "string",
      "created_at": "2026-04-23T09:30:00Z",
      "updated_at": "2026-04-23T09:30:00Z"
    }
  ]
}
```

| Field | Type | Description |
|:------|:-----|:------------|
| `data` | Array | List of created invitations |
| `data[].id` | String | Invitation ID |
| `data[].email` | String | Recipient email address |
| `data[].role` | String | Application role assigned to the invitation |
| `data[].created_at` | String | ISO 8601 timestamp of invitation creation |
| `data[].updated_at` | String | ISO 8601 timestamp of last update |

### Search Invitations

```
POST /applications/{applicationId}/invitations/_search
```

**Query Parameters**

| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `page` | Integer | `1` | Page number for pagination |
| `size` | Integer | `10` | Number of results per page |

**Request Body**

```json
{
  "filters": {
    "email": "string"
  }
}
```

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `filters.email` | String | No | Filter invitations by email address (case-insensitive substring match) |

**Response**

```json
{
  "data": [
    {
      "id": "string",
      "email": "string",
      "role": "string",
      "created_at": "2026-04-23T09:30:00Z",
      "updated_at": "2026-04-23T09:30:00Z"
    }
  ],
  "metadata": {
    "pagination": {
      "total": 1,
      "size": 10,
      "current_page": 1
    }
  }
}
```

| Field | Type | Description |
|:------|:-----|:------------|
| `data` | Array | List of application invitations |
| `data[].id` | String | Invitation ID |
| `data[].email` | String | Recipient email address |
| `data[].role` | String | Application role assigned to the invitation |
| `data[].created_at` | String | ISO 8601 timestamp of invitation creation |
| `data[].updated_at` | String | ISO 8601 timestamp of last update |
| `metadata.pagination` | Object | Pagination metadata |
| `metadata.pagination.total` | Integer | Total number of invitations |
| `metadata.pagination.size` | Integer | Number of results per page |
| `metadata.pagination.current_page` | Integer | Current page number |

### Update Invitation

```
PUT /applications/{applicationId}/invitations/{invitationId}
```

**Request Body**

```json
{
  "role": "OWNER"
}
```

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `role` | String | Yes | New application role to assign |

**Response**

HTTP 200 OK (returns updated Invitation object)

### Delete Invitation

```
DELETE /applications/{applicationId}/invitations/{invitationId}
```

**Response**

HTTP 204 No Content

### Resend Invitation

```
POST /applications/{applicationId}/invitations/{invitationId}/_resend
```

**Request Body**

```json
{
  "confirmation_page_url": "https://portal.example.com/user/invitation/confirm"
}
```

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `confirmation_page_url` | String | Yes | URL for invitation confirmation page |

**Response**

HTTP 204 No Content

### Search Platform Users

```
POST /users/_search
```

**Query Parameters**

| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `q` | String | N/A | Deprecated. Use `filters.query` in request body instead |

{% hint style="warning" %}
The `q` query parameter is deprecated. Use `filters.query` in the request body instead. If both are provided, the endpoint returns HTTP 400.
{% endhint %}

**Request Body**

```json
{
  "filters": {
    "query": "string"
  },
  "includes": {
    "applicationMembership": "string"
  }
}
```

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `filters.query` | String | No | Search query (defaults to `"*"` if omitted) |
| `includes.applicationMembership` | String | No | Application ID to include membership metadata for |

**Response**

```json
{
  "data": [
    {
      "id": "string",
      "display_name": "string",
      "first_name": "string",
      "last_name": "string",
      "email": "string",
      "reference": "string",
      "editableProfile": true,
      "permissions": {
        "APPLICATION": ["C", "R"],
        "USER": ["R"]
      },
      "_links": { "avatar": "string" }
    }
  ],
  "metadata": {
    "applicationMembership": {
      "user-1": true,
      "user-2": false
    }
  }
}
```

| Field | Type | Description |
|:------|:-----|:------------|
| `data` | Array | List of users |
| `data[].id` | String | User ID |
| `data[].display_name` | String | User display name |
| `data[].first_name` | String | User first name |
| `data[].last_name` | String | User last name |
| `data[].email` | String | User email address |
| `data[].reference` | String | User reference |
| `data[].editableProfile` | Boolean | Whether the user profile is editable |
| `data[].permissions` | Object | User permissions by scope |
| `data[].permissions.APPLICATION` | Array | Application-level permissions |
| `data[].permissions.USER` | Array | User-level permissions |
| `data[]._links.avatar` | String | URL to user avatar image |
| `metadata.applicationMembership` | Object | Application membership status by user ID |

**Error Responses**

| Status Code | Description |
|:------------|:------------|
| `400` | Both `q` query parameter and request body are provided |

### Finalize User Registration

```
POST /user/registration/_finalize
```

**Request Body**

```json
{
  "token": "string",
  "password": "string",
  "firstname": "string",
  "lastname": "string"
}
```

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `token` | String | Yes | JWT token containing registration action and user email |
| `password` | String | No | User password |
| `firstname` | String | No | User first name |
| `lastname` | String | No | User last name |

**Response**

HTTP 200 OK (returns User entity)

### Get Application Roles

```
GET /configuration/applications/roles
```

**Response**

```json
{
  "data": [
    {
      "id": "string",
      "name": "string",
      "default": true,
      "system": false
    }
  ]
}
```

| Field | Type | Description |
|:------|:-----|:------------|
| `data` | Array | List of application roles |
| `data[].id` | String | Role ID |
| `data[].name` | String | Role name |
| `data[].default` | Boolean | Whether the role is the default application role |
| `data[].system` | Boolean | Whether the role is a system role |
