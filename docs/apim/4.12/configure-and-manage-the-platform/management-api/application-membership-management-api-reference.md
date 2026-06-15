# Application Membership Management API Reference

## Management API

### Search Application Members

**POST** `/applications/{applicationId}/members/_search`

Search application members by display name with pagination. Requires `APPLICATION_MEMBER[READ]` permission.

**Request Body:**
```json
{
  "filters": {
    "displayName": "string"
  }
}
```

**Query Parameters:**
- `page` (integer): Page number (1-indexed)
- `size` (integer): Page size

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": "string",
      "user": {
        "id": "string",
        "display_name": "string",
        "email": "string",
        "first_name": "string",
        "last_name": "string",
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
    "paginateMetaData": {
      "totalElements": 42
    },
    "pagination": {
      "total": 42,
      "current_page": 1,
      "size": 10
    }
  },
  "links": {}
}
```

**Error Responses:**
- `400 Bad Request`: Invalid pagination or search query parameter
- `403 Forbidden`: User lacks `APPLICATION_MEMBER[READ]` permission
- `404 Not Found`: Application not found

### Create Application Member

**POST** `/applications/{applicationId}/members`

Create a new application member. Requires `APPLICATION_MEMBER[CREATE]` permission.

**Request Body:**
```json
{
  "user": "string",
  "reference": "string",
  "role": "string"
}
```

**Response (201 Created):**
```json
{
  "id": "string",
  "role": "string"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid input
- `403 Forbidden`: Missing `APPLICATION_MEMBER[CREATE]` permission
- `404 Not Found`: Application not found
- `409 Conflict`: User is already a member of the application
- `500 Internal Server Error`

### Update Application Member Role

**PUT** `/applications/{applicationId}/members/{memberId}`

Update an application member's role. Requires `APPLICATION_MEMBER[U]` permission.

**Request Body:**
```json
{
  "role": "string"
}
```

**Response (200 OK):**
```json
{
  "id": "string",
  "role": "string"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid input
- `403 Forbidden`: Missing `APPLICATION_MEMBER[U]` permission
- `404 Not Found`: Application or member not found

### Delete Application Member

**DELETE** `/applications/{applicationId}/members/{memberId}`

Delete an application member. Requires `APPLICATION_MEMBER[D]` permission. Returns `204 No Content` on success.

**Error Responses:**
- `403 Forbidden`: User lacks `APPLICATION_MEMBER[D]` permission
- `404 Not Found`: Application or member not found

### Create Application Invitations

**POST** `/applications/{applicationId}/invitations`

Create application invitations. Requires `APPLICATION_MEMBER[C]` permission.

**Request Body:**
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

**Response (201 Created):** Returns only pending invitations. Recipients who were added directly as members are excluded from the response.

**Error Responses:**
- `400 Bad Request`: Invalid input
- `403 Forbidden`: Missing `APPLICATION_MEMBER[C]` permission
- `404 Not Found`: Application not found
- `409 Conflict`: Pending invitation exists or multiple user matches

### Search Application Invitations

**POST** `/applications/{applicationId}/invitations/_search`

Search application invitations by email with pagination. Requires `APPLICATION_MEMBER[READ]` permission.

**Request Body:**
```json
{
  "filters": {
    "email": "string"
  }
}
```

**Query Parameters:**
- `page` (integer, default: 1)
- `size` (integer, default: 10)

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": "string",
      "email": "string",
      "role": "string",
      "created_at": "2026-04-23T09:30:00Z",
      "updated_at": "2026-04-23T09:45:00Z"
    }
  ],
  "metadata": {
    "paginateMetaData": {
      "totalElements": 10
    },
    "pagination": {
      "current_page": 1,
      "size": 10,
      "total": 10
    }
  }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid pagination or search query
- `403 Forbidden`: User lacks `APPLICATION_MEMBER[READ]` permission
- `404 Not Found`: Application not found

### Update Application Invitation Role

**PUT** `/applications/{applicationId}/invitations/{invitationId}`

Update an application invitation's role. Requires `APPLICATION_MEMBER[U]` permission.

**Request Body:**
```json
{
  "role": "string"
}
```

**Response (200 OK):**
```json
{
  "id": "string",
  "email": "string",
  "role": "string"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid input
- `403 Forbidden`: Missing `APPLICATION_MEMBER[U]` permission
- `404 Not Found`: Application or invitation not found

### Delete Application Invitation

**DELETE** `/applications/{applicationId}/invitations/{invitationId}`

Delete an application invitation. Requires `APPLICATION_MEMBER[D]` permission. Returns `204 No Content` on success.

**Error Responses:**
- `403 Forbidden`: User lacks `APPLICATION_MEMBER[D]` permission
- `404 Not Found`: Application or invitation not found

### Resend Application Invitation Email

**POST** `/applications/{applicationId}/invitations/{invitationId}/_resend`

Resend an application invitation email. Requires `APPLICATION_MEMBER[U]` permission.

**Request Body:**
```json
{
  "confirmation_page_url": "https://portal.example.com/user/invitation/confirm"
}
```

**Response (204 No Content):** Invitation email resent successfully.

**Error Responses:**
- `400 Bad Request`: Missing or invalid `confirmation_page_url`
- `403 Forbidden`: User lacks `APPLICATION_MEMBER[U]` permission
- `404 Not Found`: Application or invitation not found

### Transfer Application Ownership

**POST** `/applications/{applicationId}/members/_transfer_ownership`

Transfer application ownership to a new primary owner. Requires `APPLICATION_MEMBER[U]` permission and user must be current owner.

**Request Body:**
```json
{
  "new_primary_owner_id": "user-id",
  "new_primary_owner_reference": "user-reference",
  "primary_owner_newrole": "OWNER"
}
```

**Response (204 No Content):** Ownership transferred successfully.

**Error Responses:**
- `400 Bad Request`: Invalid input (e.g., new owner is current owner)
- `403 Forbidden`: Missing `APPLICATION_MEMBER[U]` permission or user is not current owner
- `404 Not Found`: Application not found

### Search Users with Application Membership Enrichment

**POST** `/users/_search`

Search platform users with optional application membership enrichment. Requires `MANAGEMENT_USERS[READ]` permission. When `includes.applicationMembership` is provided, also requires `APPLICATION_MEMBER[READ]` permission for the specified application.

**Request Body:**
```json
{
  "filters": {
    "query": "string"
  },
  "includes": {
    "applicationMembership": "application-id"
  }
}
```

**Query Parameters:**
- `q` (deprecated): Query string for search engine. Use `filters.query` in request body instead. Cannot be used together with request body (returns `400 Bad Request` if both are provided).
- `page` (integer, default: 1)
- `size` (integer, default: 20)

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": "string",
      "display_name": "string",
      "email": "string",
      "first_name": "string",
      "last_name": "string",
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
    "data": { "total": 10 },
    "applicationMembership": {
      "user-1": true,
      "user-2": false
    }
  }
}
```

**Membership Enrichment Behavior:** When `includes.applicationMembership` is provided, the system filters out users without IDs or with blank IDs before performing the membership lookup. If no valid user IDs remain after filtering, the system returns an empty map for `applicationMembership`.

**Error Responses:**
- `400 Bad Request`: Query parameter `q` cannot be used together with request body
- `403 Forbidden`: Missing `MANAGEMENT_USERS[READ]` or `APPLICATION_MEMBER[READ]` permission
- `404 Not Found`: Application not found (when `applicationMembership` is requested)
- `500 Internal Server Error`

### Finalize User Registration or Accept Invitation

**POST** `/registration/_finalize`

Finalize user registration or accept invitation. Requires a valid JWT token.

**Request Body:**
```json
{
  "token": "string",
  "password": "string",
  "firstname": "string",
  "lastname": "string"
}
```

**Response (200 OK):**
```json
{
  "id": "string",
  "email": "string"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid token or input
- `409 Conflict`: Reset password action attempted on registration endpoint
