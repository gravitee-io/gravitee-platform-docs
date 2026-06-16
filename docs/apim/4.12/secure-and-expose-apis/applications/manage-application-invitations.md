# Manage Application Invitations

## Inviting Users by Email

Navigate to the application's Invitations tab. The Invitations tab is visible when `portal.next.applications.membership.enabled` is `true`, `portal.next.applications.membership.invitations.enabled` is `true`, and the user has `MEMBER[R]` permission.

1. Click **Invite Members** (visible when user has `MEMBER[C]` permission).
2. Enter one or more email addresses in the **Recipients** field. Emails are trimmed, lowercased, and deduplicated within the request. Each email must pass [RFC 5322](https://datatracker.ietf.org/doc/html/rfc5322) validation.
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
2. Click **Resend** next to the invitation you want to resend.
3. (Optional) Update the **Confirmation Page URL** in the dialog.
4. Click **Resend**.

The system dispatches a new email notification and updates the invitation's `updated_at` timestamp.

#### Updating Invitation Roles

To update an invitation's role:

1. Navigate to the **Invitations** table.
2. Click **Edit invitation role** next to the invitation you want to modify.
3. Select a new role from the dropdown.
4. Submit the changes.

{% hint style="info" %}
The role must exist and be assignable. System roles and `PRIMARY_OWNER` cannot be assigned to invitations.
{% endhint %}

The invitation's `updated_at` timestamp is updated when the role is changed.

#### Deleting Invitations

To delete an invitation:

1. Navigate to the **Invitations** table.
2. Click **Delete** next to the invitation you want to remove.
3. Confirm the deletion when prompted.

The invitation is immediately removed from the system.

