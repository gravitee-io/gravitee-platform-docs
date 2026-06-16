# Application Membership and Invitations Management API Reference

## Management API

### POST `/applications/{applicationId}/members/_search`

Search for application members by display name. Supports pagination.

**Request body:**
```json
{
  "filters": {
    "displayName": "string"
  }
}
```

**Query parameters:**
- `page` (integer, default: 1)
- `size` (integer, default: 10)

**Response (`200 OK`):**
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
      "created_at": "string",
      "updated_at": "string"
    }
  ],
  "metadata": {
    "pagination": {
      "current_page": 1,
      "total": 0,
      "size": 10
    }
  }
}
```

### POST `/applications/{applicationId}/members`

Add a registered user as an application member.

**Request body:**
```json
{
  "user": "string",
  "reference": "string",
  "role": "string"
}
```

**Response (`201 Created`):**
```json
{
  "id": "string",
  "role": "string",
  "user": { ... }
}
```

### PUT `/applications/{applicationId}/members/{memberId}`

Update an application member's role.

**Request body:**
```json
{
  "role": "string"
}
```

**Response (`200 OK`):**
```json
{
  "id": "string",
  "role": "string",
  "user": { ... }
}
```

### DELETE `/applications/{applicationId}/members/{memberId}`

Remove an application member.

**Response:** `204 No Content`

### POST `/applications/{applicationId}/members/_transfer_ownership`

Transfer application ownership to another member.

**Request body:**
```json
{
  "new_primary_owner_id": "string",
  "new_primary_owner_reference": "string (optional)",
  "primary_owner_newrole": "string"
}
```

**Response:** `204 No Content`

### POST `/applications/{applicationId}/invitations`

Create application invitations for one or more recipients.

**Request body:**
```json
{
  "recipients": [
    { "email": "alice@example.com" },
    { "email": "bob@example.com" }
  ],
  "role": "USER",
  "notify": true,
  "confirmation_page_url": "https://portal.example.com/user/invitation/confirm"
}
```

**Response (`201 Created`):**
```json
{
  "data": [
    {
      "id": "00000000-0000-0000-0000-000000000001",
      "email": "alice@example.com",
      "role": "USER",
      "created_at": "2026-04-23T09:30:00Z",
      "updated_at": "2026-04-23T09:30:00Z"
    }
  ]
}
```

### POST `/applications/{applicationId}/invitations/_search`

Search for application invitations by email address. Supports pagination.

**Request body:**
```json
{
  "filters": {
    "email": "string (optional)"
  }
}
```

**Query parameters:**
- `page` (integer, default: 1)
- `size` (integer, default: 10)

### PUT `/applications/{applicationId}/invitations/{invitationId}`

Update an application invitation's role.

**Request body:**
```json
{
  "role": "string"
}
```

**Response (`200 OK`):**
```json
{
  "id": "string",
  "email": "string",
  "role": "string",
  "created_at": "string",
  "updated_at": "string"
}
```

### DELETE `/applications/{applicationId}/invitations/{invitationId}`

Delete a pending application invitation.

**Response:** `204 No Content`

### POST `/applications/{applicationId}/invitations/{invitationId}/_resend`

Resend an application invitation email.

**Request body:**
```json
{
  "confirmation_page_url": "string (URI, required)"
}
```

**Response:** `204 No Content`

### POST `/users/_search`

Search for platform users. Optionally enrich results with application membership metadata. When the search query is null or blank, the system defaults to `*`.

**Query parameters (deprecated):**
- `q` (string, deprecated): Query string for search. Use `filters.query` in request body instead. When both are provided, the system returns `400 Bad Request`.

**Request body (optional):**
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

**Response (`200 OK`):**
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

### GET `/configuration/applications/roles`

Retrieve all application roles available in the organization.

**Response (`200 OK`):**
```json
{
  "data": [
    {
      "id": "string",
      "name": "string",
      "default": false,
      "system": false
    }
  ]
}
```

### POST `/portal/registration/_finalize`

Finalize user registration or accept an invitation.

**Request body:**
```json
{
  "token": "string (JWT)",
  "password": "string (optional)",
  "firstname": "string (optional)",
  "lastname": "string (optional)"
}
```

**Response:**
- **200 OK**: Returns `User` entity
- **409 Conflict**: When token action is `RESET_PASSWORD`
- **500 Internal Server Error**: When token decode fails
