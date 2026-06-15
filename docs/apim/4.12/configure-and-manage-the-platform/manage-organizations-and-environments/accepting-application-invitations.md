# Accepting Application Invitations

## Accepting Invitations

Invited users receive an email containing a registration URL with an embedded JWT token. Navigate to the confirmation URL (e.g., `https://portal.example.com/user/invitation/confirm/:token`).

1. Enter your **First name** in the field (required).
2. Enter your **Last name** in the field (required).
3. Review the pre-filled **Email** field (disabled, extracted from token).
4. Enter a **Password** in the field (required). The password must meet format requirements.
5. Enter the same password in the **Confirm password** field (required). The value must match the password field.
6. Click **Accept invitation** to submit.

The backend validates the JWT token signature and issuer. If the token signature or issuer is invalid, the request is rejected with `JWTVerificationException`. The backend then creates or finalizes the user account, grants default organization and environment roles required for portal access, adds the user as an application member with the invited role, and deletes the pending invitation.

If the user already has a password set, the request is rejected with `UserAlreadyFinalizedException`. If no active invitation is found for the email, the request is rejected with `InvitationCanceledException` (message: "No active invitation found for email [<email>]"). If the token action is `RESET_PASSWORD`, the request is rejected with HTTP 409 Conflict.

Default role assignment uses `executionContext.environmentId` or `GraviteeContext.getDefaultEnvironment()` for ENVIRONMENT scope. If no default ORGANIZATION or ENVIRONMENT roles are found during user creation, the request is rejected with `DefaultRoleNotFoundException`.

On success, the confirmation page displays the message: "Your account has been successfully activated. You can now sign in using your email address and password." A **Login** link redirects to `/log-in`.

### Error Messages

| Error | Description |
|:------|:------------|
| "Invalid token value" | Token cannot be parsed or signature is invalid. |
| "First name is required" | First name field is empty. |
| "Last name is required" | Last name field is empty. |
| "Password is required" | Password field is empty. |
| "Passwords do not match" | Password and confirm password fields do not match. |
| "Unable to accept the invitation. Please try again." | Generic submission error (e.g., network failure, server error). |

### Management API

#### Search members

Search for members of an application.

```
POST /applications/{applicationId}/members/_search
```

**Request body:**

```json
{
  "filters": {
    "displayName": "string"
  }
}
```

**Query parameters:**

* `page` (integer, default: `1`)
* `size` (integer, default: `10`)

**Response:**

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

#### Create member

Add a member to an application.

```
POST /applications/{applicationId}/members
```

**Request body:**

```json
{
  "user": "string",
  "reference": "string",
  "role": "string"
}
```

**Response:** `201 Created`

#### Update member

Update a member's role.

```
PUT /applications/{applicationId}/members/{memberId}
```

**Request body:**

```json
{
  "role": "string"
}
```

**Response:**

```json
{
  "id": "string",
  "role": "string"
}
```

#### Transfer ownership

Transfer primary ownership of an application to another member.

```
POST /applications/{applicationId}/members/_transfer_ownership
```

**Request body:**

```json
{
  "new_primary_owner_id": "string",
  "new_primary_owner_reference": "string",
  "primary_owner_newrole": "string"
}
```

**Response:** `204 No Content`

#### Create invitations

Invite users to join an application.

```
POST /applications/{applicationId}/invitations
```

**Request body:**

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

**Response:** `201 Created`

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

#### Search invitations

Search for pending invitations to an application.

```
POST /applications/{applicationId}/invitations/_search
```

**Request body:**

```json
{
  "filters": {
    "email": "string"
  }
}
```

**Query parameters:**

* `page` (integer, default: `1`)
* `size` (integer, default: `10`)

**Response:**

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

#### Update invitation

Update the role for a pending invitation.

```
PUT /applications/{applicationId}/invitations/{invitationId}
```

**Request body:**

```json
{
  "role": "OWNER"
}
```

**Response:** `200 OK` (updated invitation object)

#### Delete invitation

Delete a pending invitation.

```
DELETE /applications/{applicationId}/invitations/{invitationId}
```

**Response:** `204 No Content`

#### Resend invitation

Resend an invitation email.

```
POST /applications/{applicationId}/invitations/{invitationId}/_resend
```

**Request body:**

```json
{
  "confirmation_page_url": "https://portal.example.com/user/invitation/confirm"
}
```

**Response:** `204 No Content`

#### Search platform users

Search for users on the platform.

```
POST /users/_search
```

**Query parameters:**

* `q` (string, deprecated — use `filters.query` in the request body instead)

**Request body:**

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

**Response:**

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

{% hint style="warning" %}
This endpoint returns HTTP 400 `BadRequestException` when both the `q` query parameter and request body are provided.
{% endhint %}

#### Finalize user registration

Complete user registration using a token.

```
POST /user/registration/_finalize
```

**Request body:**

```json
{
  "token": "string",
  "password": "string",
  "firstname": "string",
  "lastname": "string"
}
```

**Response:** `200 OK` (user entity)

#### Get application roles

Retrieve available application roles.

```
GET /configuration/applications/roles
```

**Response:**

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

