# Managing Application Invitations

## Creating Invitations

Navigate to the application details page and select the **Invitations** tab. To invite users by email:

1. Click **Invite users** to open the invitation creation dialog.
2. Enter one or more email addresses in the **Email addresses** field. Press Enter or Tab after each email to add it as a chip. The system validates each email address using `InternetAddress.validate()` and rejects invalid formats with the message "Invalid email address: [email]". Duplicate emails (normalized to lowercase) are rejected with the message "This email address is already selected."
3. Select an **Invitation Role** from the dropdown. The dropdown excludes system roles and roles with empty names. A blank invitation role triggers `ValidationDomainException` with the message "Application invitation role must not be blank."
4. Toggle **Send invitation email** to enable or disable email notifications. When enabled, the system sends an invitation email to each recipient with a confirmation URL.
5. Click **Send invitation** (or **Send {count} invitations** if multiple emails are entered) to create the invitations.

| Field | Description | Validation |
|:------|:------------|:-----------|
| **Email addresses** | Multi-value input field for entering recipient email addresses | Validates email format via `InternetAddress.validate()`; rejects duplicates (normalized to lowercase) |
| **Invitation Role** | Dropdown for selecting the role to assign to invited users | Excludes system roles and empty-name roles; must not be blank |
| **Send invitation email** | Toggle to enable or disable email notifications | Enabled by default |

{% hint style="info" %}
**Invitation Processing Rules:**

- If the email address matches a single registered user, the system adds that user directly as an application member (the invitation does not appear in the Invitations tab and is not included in the response).
- If the email address matches multiple registered users, the system throws `ConflictDomainException` and returns a `409 Conflict` response with the message "Application invitation email [email] matches multiple users."
- If the email address is unknown, the system creates a pending invitation.
- If the email address already has a pending invitation for the application, the system throws `ConflictDomainException` and returns a `409 Conflict` response with the message "At least one selected email already has a pending invitation."
- If the email address belongs to an existing application member, the system skips that recipient (no action taken, not included in the response).
- If the recipients list is empty, the system throws `ValidationDomainException`.
{% endhint %}

**Response:** The system returns a `201 Created` response containing only pending invitations (excludes recipients who were added directly as members).

## Viewing and Searching Invitations

The Invitations tab displays all pending invitations in a paginated table (default page: 1, default size: 10). Each row shows the invitee's email address, invited role, and invitation creation date. Use the search field above the table to filter invitations by email (case-insensitive partial match using SQL LIKE `%value%`). The search returns all invitations when the search field is empty.

To resend an invitation, click the **Resend** action in the invitation's row. The system sends a new invitation email with the confirmation URL. The resend action is disabled while a resend request is in progress for that invitation. The resend request requires a `confirmation_page_url` in the request body; missing or invalid URLs return a `400 Bad Request` response. If the user lacks `APPLICATION_MEMBER[U]` permission, the resend action is hidden.

To update an invitation's role, click the **Edit** action in the invitation's row, select a new role from the **Invitation Role** dropdown, and click **Save**. The system returns the updated invitation object on success. If the user lacks `APPLICATION_MEMBER[U]` permission, the system throws `ForbiddenAccessException` and returns a `403 Forbidden` response. If the invitation is not found or belongs to a different application, the system throws `ApplicationInvitationNotFoundException` and returns a `404 Not Found` response.

To delete an invitation, click the **Delete** action in the invitation's row, confirm the deletion in the dialog, and submit. The system returns a `204 No Content` response on success. If the user lacks `APPLICATION_MEMBER[D]` permission, the system throws `ForbiddenAccessException` and returns a `403 Forbidden` response.

## Accepting Invitations

Invited users receive an email with a confirmation URL containing a JWT token. When the user navigates to the confirmation URL, the system displays an invitation acceptance form:

1. The **Email** field displays the invitee's email address (disabled, pre-filled from the token).
2. Enter a value in the **First name** field.
3. Enter a value in the **Last name** field.
4. Enter a value in the **Password** field.
5. Enter the same value in the **Confirm password** field. The system validates that both password fields match using `passwordMatchValidator('password', 'confirmedPassword')`.
6. Click **Accept invitation** to submit the form.

| Field | Description | Validation |
|:------|:------------|:-----------|
| **Email** | Email address of the invitee (disabled, pre-filled from token) | Read-only |
| **First name** | First name of the invitee | Required (error: "First name is required") |
| **Last name** | Last name of the invitee | Required (error: "Last name is required") |
| **Password** | Password for the new user account | Required (error: "Password is required"); validated via `PasswordValidator` |
| **Confirm password** | Password confirmation | Required (error: "Password is required"); must match **Password** field (error: "Passwords do not match") |

### Acceptance Flow

1. **Token Decode:** The system calls `TokenService.decode(token)` to extract `action`, `email`, and optional `subject` (existing user ID):

    ```java
    var jwtSecret = environment.getProperty("jwt.secret");
    if (jwtSecret == null || jwtSecret.isEmpty()) {
        throw new IllegalStateException("JWT secret is mandatory");
    }
    
    var algorithm = Algorithm.HMAC256(jwtSecret);
    var verifier = JWT.require(algorithm)
        .withIssuer(environment.getProperty("jwt.issuer", DEFAULT_JWT_ISSUER))
        .build();
    var jwt = verifier.verify(token);
    ```

2. **Action Dispatch:** The system determines the action type:

    ```java
    var action = switch (decoded.action()) {
        case String s when JWTHelper.ACTION.GROUP_INVITATION.name().equals(s) -> 
            new GroupInvitationAction(decoded.email(), decoded.subject());
        case String s when JWTHelper.ACTION.APPLICATION_INVITATION.name().equals(s) -> 
            new ApplicationInvitationAction(decoded.email(), decoded.subject());
        case String s when JWTHelper.ACTION.RESET_PASSWORD.name().equals(s) -> 
            throw new UserStateConflictException("Reset password forbidden on this resource");
        default -> new UserRegistrationAction(decoded.email(), decoded.subject());
    };
    ```

3. **User Creation/Finalization:**
    - If `subject` is present: The system loads the existing user via `UserCrudService` and validates that the user does not already have a password set using `UserCrudService.isPasswordSet(user)`. If the password is already set, the system throws `UserAlreadyFinalizedException`.
    - If `subject` is absent: The system checks that user registration is enabled via `UserRegistrationEnabledService.checkEnabled(ExecutionContext)` (reads `Key.PORTAL_USERCREATION_ENABLED` for environment context and `Key.CONSOLE_USERCREATION_ENABLED` for organization context). If disabled, the system throws `UserRegistrationUnavailableException`. The system then calls `CreateUserDomainService.createGraviteeUser(executionContext, email, firstname, lastname)` to create a new Gravitee user.

4. **Password Handling:**
    - The system validates the password via `UserPasswordService.validate(RawPassword)`, which delegates to `PasswordValidator.validate(String)`. If validation fails, the system throws `PasswordFormatInvalidException`.
    - The system encodes the password via `UserPasswordService.encode(RawPassword)` using BCrypt, returning an `EncodedPassword`.
    - The system stores the encoded password via `UserCrudService.updateAndSetPassword(user, encodedPassword)`.

5. **Membership Assignment:**
    - The system finds all pending invitations for the email address via `InvitationRepository.findByEmail(email)`.
    - If no pending invitations are found, the system throws `InvitationCanceledException` with the message "No active invitation found for email [email]".
    - For `GROUP_INVITATION` actions: The system calls `AcceptInvitationDomainService.addMember(executionContext, invitation, userId)`, which delegates to `MembershipDomainService.addGroupMemberships(executionContext, groupId, userId, apiRole, applicationRole)`.
    - For `APPLICATION_INVITATION` actions: The system calls `MembershipDomainService.createNewMembership(executionContext, APPLICATION, applicationId, userId, null, roleName)`.
    - The system grants default organization and environment roles required for portal access.

6. **Cleanup:** The system deletes all processed invitations via `InvitationCrudService.delete(invitationId)`.

7. **Audit:** The system creates an `OrganizationAuditLogEntity` with event `USER_CREATED`.

8. **Notification:** The system triggers `UserPortalNotificationService.triggerUserRegistered(executionContext, user)`, which fires `PortalHook.USER_REGISTERED`.

### Error Handling

- If no pending invitations are found for the email address, the system throws `InvitationCanceledException` with the message "No active invitation found for email [email]".
- If the user already has a password set, the system throws `UserAlreadyFinalizedException`.
- If user registration is disabled, the system throws `UserRegistrationUnavailableException`.
- If the password does not meet format requirements, the system throws `PasswordFormatInvalidException`.
- If the JWT token is invalid (signature mismatch, issuer mismatch, or expired), the system throws `JWTVerificationException`.
- If the `jwt.secret` configuration property is missing or empty, the system throws `IllegalStateException` with the message "JWT secret is mandatory".
- If a reset password action is attempted on the registration endpoint, the system throws `UserStateConflictException` with the message "Reset password forbidden on this resource" and returns a `409 Conflict` response.
