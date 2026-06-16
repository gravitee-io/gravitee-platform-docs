# Managing Application Members

## Overview

Application membership management enables application owners and authorized members to control who has access to their applications directly from the Developer Portal. Users can add registered platform users, manage member roles, remove members, and transfer application ownership. Administrators control feature availability through configuration toggles.

## Key Concepts

### Application Members

Application members are registered platform users who have been granted a role on a specific application. Each member has a role that determines their permissions within the application context. The primary owner is the user with ultimate authority over the application, including the ability to transfer ownership. Members can view other members, search by display name, and see role assignments. Users with appropriate permissions can add new members, update roles, or remove members who no longer require access.

### Invitation Acceptance

Invited users accept an application invitation by navigating to the confirmation URL and submitting their registration details (first name, last name, password). The backend validates the JWT token, creates or finalizes the user account, grants default organization and environment roles required for portal access, adds the user as an application member with the invited role, and deletes the pending invitation.

{% hint style="warning" %}
If the token action is `RESET_PASSWORD`, the request is rejected with HTTP 409 Conflict.
{% endhint %}

#### JWT Token Validation

JWT token decoding creates an HMAC256 algorithm with the secret and builds a verifier with the issuer from `jwt.issuer` (defaults to `DEFAULT_JWT_ISSUER`). The verifier validates the token signature and issuer, throwing `JWTVerificationException` when the JWT signature or issuer is invalid.

JWT token claims include:
* `ACTION`
* `EMAIL`
* `SUBJECT` (optional)

JWT actions enum includes:
* `RESET_PASSWORD`
* `USER_REGISTRATION`
* `GROUP_INVITATION`
* `APPLICATION_INVITATION`
* `USER_CREATION`

#### Action-Specific Processing

The system processes invitations based on the JWT action:

* **`GROUP_INVITATION` action**: The system finds invitations by email, adds the user to groups, and deletes the invitations.
* **`APPLICATION_INVITATION` action**: The system finds invitations by email, adds the user to applications, and deletes the invitations.
* **`USER_REGISTRATION` action**: The system creates a new user or finalizes an existing user. No invitations are processed.

#### User Registration Validation

User registration enabled check validates:
* `Key.CONSOLE_USERCREATION_ENABLED` for `ORGANIZATION` context
* `Key.PORTAL_USERCREATION_ENABLED` for `ENVIRONMENT` context

If disabled, the system throws `UserRegistrationUnavailableException`.

#### Default Role Assignment

Default role assignment uses `executionContext.environmentId` or `GraviteeContext.getDefaultEnvironment()` for `ENVIRONMENT` scope.

{% hint style="danger" %}
If no default `ORGANIZATION` or `ENVIRONMENT` roles are found during user creation, the system throws `DefaultRoleNotFoundException`.
{% endhint %}

### Ownership Transfer

Ownership transfer allows the current primary owner to designate a new primary owner from the existing application members. The current owner selects a new primary owner and chooses a new role for themselves from assignable application roles. The transfer is atomic: the new owner receives the `PRIMARY_OWNER` role, and the previous owner is reassigned to the selected role. Only roles where `isAssignableApplicationRole()` returns `true` are offered for the current owner's new role. System roles and roles with empty names are excluded.

### Application Invitations

Application invitations allow users to grant application access to people who are not yet registered on the platform. An invitation specifies the invitee's email address and the role they will receive upon acceptance.

When an invitation is created, the system can optionally send an email notification containing a registration URL with an embedded JWT token. If the invitee's email matches exactly one existing platform user, that user is added directly as a member instead of creating a pending invitation.

Pending invitations can be searched, resent, updated (role change), or deleted before acceptance.

#### Data storage and indexing

Invitations are stored with the following database configurations:

{% tabs %}
{% tab title="MongoDB" %}
The `invitations` collection uses an index (`ri1rt1e1`) with the following configuration:

* **Keys:**
  * `referenceId` (ascending)
  * `referenceType` (ascending)
  * `email` (ascending)
* **Collation:**
  * Locale: `en`
  * Strength: `SECONDARY` (case-insensitive)
{% endtab %}

{% tab title="JDBC" %}
Invitation search uses the following SQL pattern:

```sql
SELECT * FROM invitations
WHERE reference_id = ?
  AND reference_type = ?
  AND lower(email) LIKE ? ESCAPE '\'
ORDER BY CASE WHEN email IS NULL THEN 1 ELSE 0 END, lower(email) ASC
```

**Sortable columns:**
* `id`
* `reference_type`
* `reference_id`
* `email`
* `api_role`
* `application_role`
* `created_at`
* `updated_at`

**Default sort:** `email` ascending, case-insensitive, with null values sorted last.
{% endtab %}
{% endtabs %}

#### Application invitation model

The `ApplicationInvitation` model is mutable and provides the following methods:

* `updateRole(String roleName)`: Updates the role assigned to the invitation
* `markResendAttempted()`: Marks that a resend attempt was made

Both methods update the `updatedAt` timestamp using `TimeProvider.now()`.

## Prerequisites

- User must have an active account on the Gravitee platform
- For member management: user must have `MEMBER[R]` permission to view members, `MEMBER[C]` to add members, `MEMBER[U]` to update roles or transfer ownership, `MEMBER[D]` to delete members
- For ownership transfer: `portal.next.applications.membership.transferOwnership.enabled` must be `true`, user must be the current primary owner, and user must have `MEMBER[U]` permission
- Default organization and environment roles must be defined for new user registration

### JWT Configuration

The following table describes the JWT configuration properties:

| Property | Description | Default/Example |
|:---------|:------------|:----------------|
| `jwt.secret` | JWT signing secret. Must be at least 256 bits. If missing or empty, the system throws an `IllegalStateException` with the message "JWT secret is mandatory". | (required) |
| `jwt.issuer` | JWT issuer claim used for token verification. | `DEFAULT_JWT_ISSUER` |

{% hint style="warning" %}
The `jwt.secret` property is mandatory and must be at least 256 bits in length.
{% endhint %}

## Gateway Configuration

### Portal Next Feature Toggles

| Property | Description | Example |
|:---------|:------------|:--------|
| `portal.next.applications.membership.enabled` | Enables application membership settings in Portal Next. When `false`, the Members tab is hidden. | `true` |
| `portal.next.applications.membership.transferOwnership.enabled` | Enables transfer of application ownership feature. When `false`, the Transfer Ownership button is hidden. | `false` |

**Configuration Scope**: Portal Next keys use `ENVIRONMENT` reference type with reference ID `"DEFAULT"`.

## Creating Application Members

Navigate to the application's [Members tab](../../secure-and-expose-apis/applications/user-and-group-access.md#members) in the Developer Portal. The Members tab is visible when `portal.next.applications.membership.enabled` is `true` and the user has `MEMBER[R]` permission.

1. Click **Add Members** (visible when user has `MEMBER[C]` permission).
2. Search for existing platform users by entering a query in the search field. Results are sorted by last name (case-insensitive, nulls last). Users without an ID field are excluded from results. When no query is provided, the system defaults to wildcard `*`. User search applies no backend pagination (all results returned, pagination metadata exposed for compatibility).
3. Select one or more users from the search results.
4. Select a **Role** from the dropdown. The role defaults to the lowest application role when omitted. Roles must exist and be assignable (not system, not `PRIMARY_OWNER`).
5. Click **Add** to create the memberships.

The system validates that selected users are not already members and do not have pending invitations. If a user is already a member, they are silently skipped. If a pending invitation exists for the user's email, the request is rejected with HTTP 409 Conflict. All validations occur before any database writes (all-or-nothing).

**Member Search and Display**

| Field | Description |
|:------|:------------|
| **Search user** | Filters members by display name (case-insensitive substring match). |
| **Name** | User's display name (fallback: first name + last name, fallback: user ID). Shows "(you)" badge when the member is the current user. |
| **Role** | Application role assigned to the member. Primary owner role is marked with `data-testid="members-role-primary-owner"`. |

## Managing Application Members

### Updating Member Roles

To update a member's role, click the **Edit member role** action (icon: `edit`) next to the member in the Members table. This action is visible when the user has `MEMBER[U]` permission and the member is not the primary owner. Select a new role from the dropdown and submit. The role must exist and be assignable (not system, not `PRIMARY_OWNER`).

### Removing Members

To remove a member, click the **Delete** action (icon: `delete_outline`, color: `warn`) next to the member in the Members table. This action is visible when the user has `MEMBER[D]` permission and the member is not the primary owner. Confirm the deletion when prompted. The member is immediately removed from the application.

### Transferring Ownership

Navigate to the application's Members tab. The **Transfer Ownership** button (icon: `swap_horiz`, stroked button) is visible when the current user is the application owner, has `MEMBER[U]` permission, and `portal.next.applications.membership.transferOwnership.enabled` is `true`.

1. Click **Transfer Ownership**.
2. Select a **New Primary Owner** from the list of existing application members or search for a platform user.
3. Select a **New Role** for yourself from the dropdown. Only assignable application roles are offered (excludes `APPLICATION_PRIMARY_OWNER`, system roles, and roles with empty names).
4. Click **Transfer** to execute the ownership transfer.

The transfer is atomic: the new owner receives the `PRIMARY_OWNER` role, and the previous owner is reassigned to the selected role. If the **New Role** field is empty or invalid, the submit button is disabled and the error message "Application role is required." is displayed.

