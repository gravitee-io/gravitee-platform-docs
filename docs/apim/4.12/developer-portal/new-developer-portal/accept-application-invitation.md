# Accept Application Invitation

## Accepting Invitations

Invited users receive an email containing a registration URL with an embedded JWT token. The URL follows the pattern `https://portal.example.com/user/invitation/confirm/:token`.

To accept an invitation:

1. Navigate to the confirmation URL provided in the invitation email.
2. Enter your **First name** (required).
3. Enter your **Last name** (required).
4. Review the pre-filled **Email** field. This field is disabled and extracted from the token.
5. Enter a **Password** (required). The password must meet platform requirements.
6. Enter the same password in the **Confirm password** field (required). The value must match the password field.
7. Click **Accept invitation** to submit.

The backend validates the JWT token, creates or finalizes the user account, grants default organization and environment roles required for portal access, adds the user as an application member with the invited role, and deletes the pending invitation.

{% hint style="danger" %}
If the user already has a password set, the request is rejected with `UserAlreadyFinalizedException`. If no active invitation is found for the email, the request is rejected with `InvitationCanceledException` (message: "No active invitation found for email [<email>]"). If the token action is `RESET_PASSWORD`, the request is rejected with HTTP 409 Conflict.
{% endhint %}

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
