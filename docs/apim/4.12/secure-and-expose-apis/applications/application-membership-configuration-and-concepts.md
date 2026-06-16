# Application Membership Configuration and Concepts

## Overview

Application membership management enables application owners and authorized members to control who has access to their applications directly from the Developer Portal. Users can add registered platform users, invite new users by email, manage pending invitations, update member roles, remove members, and transfer application ownership. Administrators control feature availability through configuration toggles.

## Key Concepts

### Application Members

Application members are registered platform users who have been granted a role on a specific application. Each member has a role that determines their permissions within the application context. The primary owner is the user with ultimate authority over the application, including the ability to transfer ownership. Members can view other members, search by display name, and see role assignments. Users with appropriate permissions can add new members, update roles, or remove members who no longer require access.

### Application Invitations

Application invitations allow users to grant application access to people who are not yet registered on the platform. An invitation specifies the invitee's email address and the role they will receive upon acceptance. When an invitation is created, the system can optionally send an email notification containing a registration URL with an embedded JWT token. If the invitee's email matches exactly one existing platform user, that user is added directly as a member instead of creating a pending invitation. Pending invitations can be searched, resent, updated (role change), or deleted before acceptance.

Invitations are stored with a MongoDB index (`ri1rt1e1`) on the `invitations` collection with keys `referenceId`, `referenceType`, `email` and collation locale `en` with strength `SECONDARY`. JDBC invitation search uses the SQL pattern `SELECT * FROM invitations WHERE reference_id = ? AND reference_type = ? AND lower(email) LIKE ? ESCAPE '\' ORDER BY CASE WHEN email IS NULL THEN 1 ELSE 0 END, lower(email) ASC`. Sortable columns include `id`, `reference_type`, `reference_id`, `email`, `api_role`, `application_role`, `created_at`, `updated_at`. Default sort is `email` ascending, case-insensitive, with null values sorted last.

The `ApplicationInvitation` model is mutable and provides `updateRole(String roleName)` and `markResendAttempted()` methods that update the `updatedAt` timestamp using the current timestamp.

### Invitation Acceptance

Invited users accept an application invitation by navigating to the confirmation URL and submitting their registration details (first name, last name, password). The backend validates the JWT token, creates or finalizes the user account, grants default organization and environment roles required for portal access, adds the user as an application member with the invited role, and deletes the pending invitation. If the token action is `RESET_PASSWORD`, the request is rejected with HTTP 409 Conflict.

JWT token decoding creates an HMAC256 algorithm with the secret and builds a verifier with the issuer from `jwt.issuer` (defaults to `DEFAULT_JWT_ISSUER`). The verifier validates the token signature and issuer, throwing `JWTVerificationException` when JWT signature or issuer is invalid. JWT token claims include `ACTION`, `EMAIL`, and optional `SUBJECT`. JWT actions enum includes `RESET_PASSWORD`, `USER_REGISTRATION`, `GROUP_INVITATION`, `APPLICATION_INVITATION`, and `USER_CREATION`.

For `GROUP_INVITATION` action: the system finds invitations by email, adds the user to groups, and deletes the invitations. For `APPLICATION_INVITATION` action: the system finds invitations by email, adds the user to applications, and deletes the invitations. For `USER_REGISTRATION` action: the system creates a new user or finalizes an existing user; no invitations are processed.

User registration enabled check validates `Key.CONSOLE_USERCREATION_ENABLED` for `ORGANIZATION` context and `Key.PORTAL_USERCREATION_ENABLED` for `ENVIRONMENT` context, throwing `UserRegistrationUnavailableException` if disabled. Default role assignment uses the current environment context for `ENVIRONMENT` scope. If no default `ORGANIZATION` or `ENVIRONMENT` roles are found during user creation, the system throws `DefaultRoleNotFoundException`.

### Ownership Transfer

Ownership transfer allows the current primary owner to designate a new primary owner from the existing application members. The current owner selects a new primary owner and chooses a new role for themselves (from assignable application roles). The transfer is atomic: the new owner receives the `PRIMARY_OWNER` role, and the previous owner is reassigned to the selected role. Only roles where `isAssignableApplicationRole()` returns `true` are offered for the current owner's new role. System roles and roles with empty names are excluded.

## Prerequisites

- User must have an active account on the Gravitee platform
- For member management: user must have `MEMBER[R]` permission to view members, `MEMBER[C]` to add members, `MEMBER[U]` to update roles or transfer ownership, `MEMBER[D]` to delete members
- For invitation management: `portal.next.applications.membership.invitations.enabled` must be `true` and user must have `MEMBER[R]` permission to view invitations
- For ownership transfer: `portal.next.applications.membership.transferOwnership.enabled` must be `true`, user must be the current primary owner, and user must have `MEMBER[U]` permission
- JWT secret must be configured (`jwt.secret` property, minimum 256 bits) for invitation token generation and validation
- Default organization and environment roles must be defined for new user registration
- User registration must be enabled (`Key.CONSOLE_USERCREATION_ENABLED` for organization context, `Key.PORTAL_USERCREATION_ENABLED` for environment context)

## Gateway Configuration

### Portal Next Feature Toggles

| Property | Description | Example |
|:---------|:------------|:--------|
| `portal.next.applications.membership.enabled` | Enables application membership settings in Portal Next. When `false`, the Members tab is hidden. | `true` |
| `portal.next.applications.membership.transferOwnership.enabled` | Enables transfer of application ownership feature. When `false`, the Transfer Ownership button is hidden. | `false` |
| `portal.next.applications.membership.invitations.enabled` | Enables application membership invitation feature. When `false`, the Invitations tab is hidden. | `false` |

**Configuration Scope**: Portal Next keys use `ENVIRONMENT` reference type with reference ID `"DEFAULT"`.

### JWT Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `jwt.secret` | JWT signing secret; must be at least 256 bits. Throws `IllegalStateException` with message "JWT secret is mandatory" if missing or empty. | (required) |
| `jwt.issuer` | JWT issuer claim used for token verification. | `DEFAULT_JWT_ISSUER` |
