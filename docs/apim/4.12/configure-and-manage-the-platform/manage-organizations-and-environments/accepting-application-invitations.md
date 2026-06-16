# Accepting Application Invitations

## Accepting Invitations

Invited users receive an email containing a registration URL with an embedded JWT token. Navigate to the confirmation URL (e.g., `https://portal.example.com/user/invitation/confirm/:token`).

1. Enter your **First name** in the field (required).
2. Enter your **Last name** in the field (required).
3. Review the pre-filled **Email** field (disabled, extracted from token).
4. Enter a **Password** in the field (required).
5. Enter the same password in the **Confirm password** field (required). The value must match the password field.
6. Click **Accept invitation** to submit.

The backend validates the JWT token using HMAC256 signature verification and issuer claim matching. The system then creates or finalizes the user account, grants default organization and environment roles required for portal access, adds the user as an application member with the invited role, and deletes the pending invitation.

### Validation and Error Conditions

The following conditions result in request rejection:

| Condition | Error |
|:----------|:------|
| User already has a password set | `UserAlreadyFinalizedException` |
| No active invitation found for the email | `InvitationCanceledException` with message "No active invitation found for email [<email>]" |
| Token action is `RESET_PASSWORD` | HTTP 409 Conflict |
| Token signature is invalid or issuer does not match | `JWTVerificationException` |
| User registration is disabled | `UserRegistrationUnavailableException` |
| Password does not meet format requirements | `PasswordFormatInvalidException` |
| No default organization or environment roles found | `DefaultRoleNotFoundException` |

### Success Confirmation

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

### Key Concepts

**JWT Token Actions**

The JWT token contains an `action` claim that determines the invitation acceptance workflow:

| Action | Behavior |
|:-------|:---------|
| `APPLICATION_INVITATION` | Finds invitations by email, creates or finalizes user, adds application membership, deletes invitation |
| `GROUP_INVITATION` | Finds invitations by email, creates or finalizes user, adds group membership, deletes invitation |
| `USER_REGISTRATION` | Creates new user or finalizes existing user; no invitations processed |
| `RESET_PASSWORD` | Rejected with HTTP 409 Conflict |

**User Registration Enabled Checks**

The system validates that user registration is enabled before processing invitations:

- For `ORGANIZATION` context: checks `Key.CONSOLE_USERCREATION_ENABLED` parameter
- For `ENVIRONMENT` context: checks `Key.PORTAL_USERCREATION_ENABLED` parameter

If disabled, the request is rejected with `UserRegistrationUnavailableException`.

**Default Role Assignment**

After user creation or finalization, the system assigns default roles for `ORGANIZATION` and `ENVIRONMENT` scopes. If no default roles are found, the request is rejected with `DefaultRoleNotFoundException`.
