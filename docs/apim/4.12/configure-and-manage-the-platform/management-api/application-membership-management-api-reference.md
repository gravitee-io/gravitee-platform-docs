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
        "_links": {
          "avatar": "string"
        }
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

**Response**

```json
{
  "id": "string",
  "role": "string"
}
```

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
    {
      "email": "user@example.com"
    }
  ],
  "role": "USER",
  "notify": true,
  "confirmation_page_url": "https://portal.example.com/user/invitation/confirm"
}
```

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

**Response**

HTTP 200 OK (updated Invitation object)

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

**Response**

HTTP 204 No Content

### Search Platform Users

```
POST /users/_search
```

**Query Parameters**

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `q` | String | Deprecated. Use `filters.query` in the request body instead. |

{% hint style="warning" %}
The user search endpoint returns HTTP 400 `BadRequestException` when both the `q` query parameter and request body are provided.
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
      "_links": {
        "avatar": "string"
      }
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

The `includes.applicationMembership` field accepts an application ID. When provided, the response `metadata.applicationMembership` object contains a boolean value for each user ID indicating whether that user is a member of the specified application.

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

**Response**

HTTP 200 OK (User entity)

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
