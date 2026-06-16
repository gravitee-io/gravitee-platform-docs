# Managing Application Invitations

## Inviting Users by Email

Navigate to the application's Invitations tab. The Invitations tab is visible when `portal.next.applications.membership.enabled` is `true`, `portal.next.applications.membership.invitations.enabled` is `true`, and the user has `MEMBER[R]` permission.

1. Click **Invite Members**. This button is visible when the user has `MEMBER[C]` permission.
2. Enter one or more email addresses in the **Recipients** field. Emails are trimmed, lowercased, and deduplicated within the request. Each email must pass RFC 5322 validation.
3. Select a **Role** from the dropdown. The role must exist and be assignable (not system, not `PRIMARY_OWNER`). If any recipient matches an existing user, the role cannot be `PRIMARY_OWNER`. If all recipients are unknown (no existing users), `PRIMARY_OWNER` role is allowed for pending invitations.
4. Toggle **Notify** to enable or disable email notifications. The checkbox is enabled by default.
5. Optionally, enter a **Confirmation Page URL** in the field. If omitted, the system auto-generates a confirmation URL.
6. Click **Send Invitations** to create the invitations.

The system validates all emails and roles before creating any invitations (all-or-nothing). If a recipient email matches exactly one existing platform user in the organization, that user is added directly as an application member instead of creating a pending invitation. If a recipient email matches multiple existing users, the request is rejected with HTTP 409 Conflict. If a recipient already has a pending invitation for the application, the request is rejected with HTTP 409 Conflict. If a recipient is already an application member, they are silently skipped (no invitation created, no error).

When `notify: true` and pending invitations are created, email notifications are dispatched asynchronously for each pending invitation. If all recipients matched existing users (no pending invitations created), no notifications are sent.

### Invitation Search and Display

| Field | Description |
|:------|:------------|
| **Search email** | Filters invitations by email (case-insensitive substring match). |
| **Email** | Invitee's email address. |
| **Role** | Application role the invitee will receive upon acceptance. |
| **Created At** | Timestamp when the invitation was created. |
| **Updated At** | Timestamp when the invitation was last updated (role change or resend attempt). |

### Managing Pending Invitations

#### Resending Invitations

To resend an invitation:

1. Navigate to the **Invitations** table.
2. Click the **Resend** action next to the invitation you want to resend.
3. (Optional) Update the **Confirmation Page URL** in the dialog.
4. Click **Resend**.

The system dispatches a new email notification and updates the invitation's `updated_at` timestamp.

#### Updating Invitation Roles

To update an invitation's role:

1. Navigate to the **Invitations** table.
2. Click the **Edit invitation role** action next to the invitation you want to modify.
3. Select a new role from the dropdown.
4. Submit the changes.

{% hint style="info" %}
The role must exist and be assignable. System roles and `PRIMARY_OWNER` cannot be assigned to invitations.
{% endhint %}

The invitation's `updated_at` timestamp is updated when the role is changed.

#### Deleting Invitations

To delete an invitation:

1. Navigate to the **Invitations** table.
2. Click the **Delete** action next to the invitation you want to remove.
3. Confirm the deletion when prompted.

The invitation is immediately removed from the system.

## Accepting Invitations

Invited users receive an email containing a registration URL with an embedded JWT token. Navigate to the confirmation URL (e.g., `https://portal.example.com/user/invitation/confirm/:token`).

1. Enter your **First name** in the field (required).
2. Enter your **Last name** in the field (required).
3. Review the pre-filled **Email** field (disabled, extracted from token).
4. Enter a **Password** in the field (required). The password must meet format requirements.
5. Enter the same password in the **Confirm password** field (required). The value must match the password field.
6. Click **Accept invitation** to submit.

The backend validates the JWT token, creates or finalizes the user account, grants default organization and environment roles required for portal access, adds the user as an application member with the invited role, and deletes the pending invitation. If the user already has a password set, the request is rejected. If no active invitation is found for the email, the request is rejected with the message "No active invitation found for email [<email>]". If the token action is `RESET_PASSWORD`, the request is rejected with HTTP 409 Conflict.

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
