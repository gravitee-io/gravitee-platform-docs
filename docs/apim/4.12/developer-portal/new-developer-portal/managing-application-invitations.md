# Managing Application Invitations

Navigate to the application's **Invitations** tab in the Portal Next interface. The Invitations tab displays a searchable, paginated list of all pending invitations for the application. Each invitation entry shows the recipient's email address, assigned role, creation and update timestamps, and action buttons for editing, resending, or deleting the invitation.

{% hint style="info" %}
The Invitations tab is visible only when `portal.next.applications.membership.invitations.enabled` is set to `true`.
{% endhint %}

### Prerequisites

Before managing application invitations, ensure the following:

* The `portal.next.applications.membership.invitations.enabled` configuration property is set to `true`.
* User registration is enabled in at least one scope:
  * `CONSOLE_USERCREATION_ENABLED` (ORGANIZATION scope) is `true`, or
  * `PORTAL_USERCREATION_ENABLED` (ENVIRONMENT scope) is `true`.
* You have the required permissions:
  * `APPLICATION_INVITATION[CREATE]` to create invitations
  * `APPLICATION_INVITATION[UPDATE]` to edit or resend invitations
  * `APPLICATION_INVITATION[DELETE]` to delete invitations

### Searching for Invitations

To search for invitations, enter at least one character in the **Email** search field. The search performs a case-insensitive substring match against invitation email addresses using SQL `LIKE` with `%` wildcards.

### Creating Invitations

To create invitations:

1. Open the **Create Invitation** dialog.
2. Enter one or more email addresses in the **Recipients** field (minimum 1 recipient).
3. Select a role from the **Role** dropdown.
4. Toggle **Notify** to control whether invitation notifications are sent (default: `true`).
5. (Optional) Provide a **Confirmation Page URL** for the registration workflow.

The system validates all email addresses using `jakarta.mail.internet.InternetAddress` before creating any invitations. Email addresses are normalized (trimmed and lowercased) and deduplicated.

{% hint style="warning" %}
**Invitation creation behavior:**

* If any recipient already has a pending invitation or is already an application member, the entire request is rejected with a `409 Conflict` error.
* If a recipient email matches multiple existing users, the request is rejected with a `409 Conflict` error.
* Recipients matching existing users are added directly as application members with the requested role; only non-matching recipients are created as pending invitations.
* The response contains only the created pending invitations—it may contain fewer entries than the requested recipients (including none) when recipients match existing users.
* The `PRIMARY_OWNER` role is rejected when any recipient is an existing user but allowed when all recipients are unknown (pending invitation behavior).
{% endhint %}

### Editing an Invitation

To edit an invitation's role:

1. Click the edit button next to the invitation entry.
2. Select a new role from the **Role** dropdown in the **Edit Invitation** dialog.
3. Save the changes.

The system updates the invitation's role and refreshes the invitation list.

### Resending an Invitation

To resend an invitation:

1. Click the resend button next to the invitation entry.
2. (Optional) Provide a new **Confirmation Page URL** in the **Resend Invitation** dialog.

The system updates the invitation's `updatedAt` timestamp to the current time and sends a new invitation email.

### Deleting an Invitation

To delete an invitation:

1. Click the delete button next to the invitation entry.
2. Confirm the deletion.

The system removes the invitation from the application.

### Invitation Search API

**Endpoint:** `POST /applications/{applicationId}/invitations/_search`

**Request Parameters:**

| Parameter | Type    | Description                 |
| --------- | ------- | --------------------------- |
| `page`    | integer | Page number (default: 1)    |
| `size`    | integer | Page size (default: 10)     |

**Request Body:**

```json
{
  "filters": {
    "email": "string"
  }
}
```

**Response:**

```json
{
  "data": [
    {
      "id": "string",
      "email": "string",
      "role": "string",
      "createdAt": "2026-04-23T09:30:00Z",
      "updatedAt": "2026-04-23T09:30:00Z"
    }
  ],
  "metadata": {
    "data": {
      "total": 42
    }
  }
}
```

**Permissions Required:** `APPLICATION_MEMBER[READ]`

**Error Responses:**

* `400`: Bad Request
* `403`: Permission Error
* `404`: Application Not Found

## Accepting Invitations and Finalizing Registration

When a user receives an application invitation email, they click the confirmation link to finalize their registration. The confirmation page collects the user's password, first name, and last name, then submits the registration token to the `/registration/_finalize` endpoint. The system validates the token and password, creates or finalizes the user account, assigns default ORGANIZATION and ENVIRONMENT roles, processes any pending invitations matching the user's email address, and sends a `USER_REGISTERED` portal notification. The user is then redirected to the login page.

### Token Action Types

The system processes the registration token according to its action type:

* **`USER_REGISTRATION`**: Creates a new user or finalizes an existing user.
* **`GROUP_INVITATION`**: Adds the user to a group with specified roles.
* **`APPLICATION_INVITATION`**: Adds the user to the application with the specified role.
* **`RESET_PASSWORD`**: Returns an HTTP 409 Conflict error with the message `"Reset password forbidden on this resource"`.

### Error Conditions

The system throws the following exceptions during registration finalization:

* **`UserAlreadyFinalizedException`**: The user already has a password set.
* **`InvitationCanceledException`**: There are no pending invitations for the user's email.
* **`PasswordFormatInvalidException`**: The password is invalid.
* **`UserRegistrationUnavailableException`**: User registration is disabled (either `CONSOLE_USERCREATION_ENABLED` or `PORTAL_USERCREATION_ENABLED` is `false`).

### Finalize Registration API

**Endpoint:** `POST /registration/_finalize`

**Request Body:**

```json
{
  "token": "string",
  "password": "string",
  "firstname": "string",
  "lastname": "string"
}
```

**Response:** User object

**Error Responses:**

* `400`: Bad Request (invalid token value, passwords do not match)
* `409`: Conflict (RESET_PASSWORD token used on finalize endpoint; error message: `"Reset password forbidden on this resource"`)

### Invitation Management API

#### Create invitations

Create one or more application invitations.

**Endpoint:** `POST /applications/{applicationId}/invitations`

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

**Field descriptions:**

* **Recipients**: Array of recipient objects (minimum 1 item). Recipients matching existing users are added directly as application members. Remaining recipients are created as pending invitations.
* **Role**: Role assigned to created invitations and directly added application members.
* **Notify**: Whether invitation notifications should be sent when pending invitations are created. Default: `true`.
* **Confirmation Page URL**: URL of the confirmation page to be used in the application invitation email. Optional. Format: URI.

**Response:** `201 Created`

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

{% hint style="info" %}
The response contains only the created pending invitations. It may contain fewer entries than the requested recipients (including none) when recipients match existing users and are added directly as members.
{% endhint %}

**Permissions required:** `APPLICATION_INVITATION` with `CREATE` permission

**Error responses:**

* `400`: Bad Request (invalid email format, blank role, or at least one recipient already has a pending invitation or is already an active member)
* `403`: Permission Error
* `404`: Application Not Found
* `409`: Conflict (email matches multiple users, or pending invitation exists)

**Behavior:**

* All-or-nothing operation: invitations created for all recipients or none.
* Does NOT return per-recipient success/error entries.
* Does NOT use `207 Multi-Status`.

##

