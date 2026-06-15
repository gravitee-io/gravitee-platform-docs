---
description: An overview about user and group access.
metaLinks:
  alternates:
    - user-and-group-access.md
---

# User and Group Access

## Overview

An application's **User and group access** page lets you manage user and group access to individual applications. Application membership management enables application owners and authorized members to control who has access to their applications directly from the Developer Portal. Users can add registered platform users, invite new users by email, manage pending invitations, update member roles, remove members, and transfer application ownership.

## Prerequisites

Before configuring user and group access, ensure the following:

* You have an active account on the Gravitee platform
* For member management: you have `MEMBER[R]` permission to view members, `MEMBER[C]` to add members, `MEMBER[U]` to update roles or transfer ownership, `MEMBER[D]` to delete members
* For invitation management: `portal.next.applications.membership.invitations.enabled` must be `true` and you must have `MEMBER[R]` permission to view invitations
* For ownership transfer: `portal.next.applications.membership.transferOwnership.enabled` must be `true`, you must be the current primary owner, and you must have `MEMBER[U]` permission
* JWT secret must be configured (`jwt.secret` property, minimum 256 bits) for invitation token generation and validation
* Default organization and environment roles must be defined for new user registration
* User registration must be enabled (`Key.CONSOLE_USERCREATION_ENABLED` for organization context, `Key.PORTAL_USERCREATION_ENABLED` for environment context)

## Configure user and group access

To configure user and group access, complete the following steps:

1. [create-an-application.md](create-an-application.md "mention").
2. Log in to your APIM Console, and then click **Applications**.
3.  Find the application you want to configure. Use the radio buttons to select either Active or Archived applications. Next, either scroll through the paginated lists of available applications or use the search field to find the application by name.

    <figure><img src="../../.gitbook/assets/00 groups added to applications 7.png" alt=""><figcaption></figcaption></figure>
4. Click on the application you want to configure.
5.  Click on **User and group access** in the Application menu.

    <figure><img src="../../.gitbook/assets/00 groups added to applications 8.png" alt=""><figcaption></figcaption></figure>

### Members

Under the **Members** tab, you can add users or groups as members of your application and define their roles to manage and perform tasks and operations. The Members tab is visible when `portal.next.applications.membership.enabled` is `true` and the user has `MEMBER[R]` permission.

<figure><img src="../../.gitbook/assets/00 groups added to applications 3.png" alt=""><figcaption></figcaption></figure>

Application members are registered platform users who have been granted a role on a specific application. Each member has a role that determines their permissions within the application context. The primary owner is the user with ultimate authority over the application, including the ability to transfer ownership. Members can view other members, search by display name, and see role assignments. Users with appropriate permissions can add new members, update roles, or remove members who no longer require access.

#### Adding members

To add members to your application:

1. Click **Add Members** (visible when user has `MEMBER[C]` permission).
2. Search for existing platform users by entering a query in the search field. Results are sorted by last name (case-insensitive, nulls last). Users without an ID field are excluded from results. When no query is provided, the system defaults to wildcard `*`. User search applies no backend pagination (all results returned, pagination metadata exposed for compatibility).
3. Select one or more users from the search results.
4. Use the **Role** drop-down menu to select member roles, which grant specific permissions. The role defaults to the lowest application role when omitted. Roles must exist and be assignable (not system, not `PRIMARY_OWNER`). For more information on roles, please refer to the [Roles](../../configure-and-manage-the-platform/manage-organizations-and-environments/user-management.md#roles) documentation.
5. Click **Add** to create the memberships.

The system validates that selected users are not already members and do not have pending invitations. If a user is already a member, they are silently skipped. If a pending invitation exists for the user's email, the request is rejected with HTTP 409 Conflict. All validations occur before any database writes (all-or-nothing).

#### Member search and display

| Field | Description |
|:------|:------------|
| **Search user** | Filters members by display name (case-insensitive substring match). |
| **Name** | User's display name (fallback: first name + last name, fallback: user ID). Shows "(you)" badge when the member is the current user. |
| **Role** | Application role assigned to the member. Primary owner role is marked with `data-testid="members-role-primary-owner"`. |

#### Updating member roles

To update a member's role, click the **Edit member role** action (icon: `edit`) next to the member in the Members table. This action is visible when the user has `MEMBER[U]` permission and the member is not the primary owner. Select a new role from the dropdown and submit. The role must exist and be assignable (not system, not `PRIMARY_OWNER`).

#### Removing members

To remove a member, click the **Delete** action (icon: `delete_outline`, color: `warn`) next to the member in the Members table. This action is visible when the user has `MEMBER[D]` permission and the member is not the primary owner. Confirm the deletion when prompted. The member is immediately removed from the application.

### Invitations

Application invitations allow you to grant application access to people who are not yet registered on the platform. An invitation specifies the invitee's email address and the role they will receive upon acceptance. When an invitation is created, the system can optionally send an email notification containing a registration URL with an embedded JWT token. If the invitee's email matches exactly one existing platform user, that user is added directly as a member instead of creating a pending invitation. Pending invitations can be searched, resent, updated (role change), or deleted before acceptance.

Invitations are stored with a MongoDB index (`ri1rt1e1`) on the `invitations` collection with keys `referenceId` (ascending), `referenceType` (ascending), `email` (ascending) and collation locale `en` with strength `SECONDARY` (case-insensitive). JDBC invitation search uses the SQL pattern `SELECT * FROM invitations WHERE reference_id = ? AND reference_type = ? AND lower(email) LIKE ? ESCAPE '\' ORDER BY CASE WHEN email IS NULL THEN 1 ELSE 0 END, lower(email) ASC`. Sortable columns include `id`, `reference_type`, `reference_id`, `email`, `api_role`, `application_role`, `created_at`, `updated_at`. Default sort is `email` ascending, case-insensitive, with null values sorted last.

#### Invitation acceptance

Invited users accept an application invitation by navigating to the confirmation URL and submitting their registration details (first name, last name, password). The backend validates the JWT token, creates or finalizes the user account, grants default organization and environment roles required for portal access, adds the user as an application member with the invited role, and deletes the pending invitation. If the token action is `RESET_PASSWORD`, the request is rejected with HTTP 409 Conflict.

JWT token decoding creates an HMAC256 algorithm with the secret and builds a verifier with the issuer from `jwt.issuer` (defaults to `DEFAULT_JWT_ISSUER`). The verifier validates the token signature and issuer, throwing `JWTVerificationException` when JWT signature or issuer is invalid. JWT token claims include `ACTION`, `EMAIL`, and optional `SUBJECT`. JWT actions enum includes `RESET_PASSWORD`, `USER_REGISTRATION`, `GROUP_INVITATION`, `APPLICATION_INVITATION`, and `USER_CREATION`.

For `GROUP_INVITATION` action: the system finds invitations by email, adds the user to groups, and deletes the invitations. For `APPLICATION_INVITATION` action: the system finds invitations by email, adds the user to applications, and deletes the invitations. For `USER_REGISTRATION` action: the system creates a new user or finalizes an existing user; no invitations are processed.

User registration enabled check validates `Key.CONSOLE_USERCREATION_ENABLED` for `ORGANIZATION` context and `Key.PORTAL_USERCREATION_ENABLED` for `ENVIRONMENT` context, throwing `UserRegistrationUnavailableException` if disabled. Default role assignment uses `executionContext.environmentId` or `GraviteeContext.getDefaultEnvironment()` for `ENVIRONMENT` scope. If no default `ORGANIZATION` or `ENVIRONMENT` roles are found during user creation, the system throws `DefaultRoleNotFoundException`.

### Groups

Click the **Groups** tab to see which groups have access to your application. Use the drop-down menu to change group selections.

<figure><img src="../../.gitbook/assets/00 groups added to applications 4.png" alt=""><figcaption></figcaption></figure>

Selecting a group gives all members of that group access to your application.

### Transfer ownership

Under the **Transfer ownership** tab, you can grant complete application access to an application member or other user. The **Transfer Ownership** button (icon: `swap_horiz`, stroked button) is visible when the current user is the application owner, has `MEMBER[U]` permission, and `portal.next.applications.membership.transferOwnership.enabled` is `true`.

To transfer ownership:

1. Click **Transfer Ownership**.
2. Click **Application member** and use the drop-down menu to select a user who is already a member of your application, or click **Other user** to search for someone who is not a member of your application. You can enter either their name or email into the search field.

    <figure><img src="../../.gitbook/assets/00 groups added to applications 5.png" alt=""><figcaption></figcaption></figure>

    <figure><img src="../../.gitbook/assets/00 groups added to applications 6.png" alt=""><figcaption></figcaption></figure>

3. Select a **New Role** for yourself from the dropdown. Only assignable application roles are offered (excludes `APPLICATION_PRIMARY_OWNER`, system roles, and roles with empty names). If the **New Role** field is empty or invalid, the submit button is disabled and the error message "Application role is required." is displayed.
4. Click **Transfer** to execute the ownership transfer.

The transfer is atomic: the new owner receives the `PRIMARY_OWNER` role, and the previous owner is reassigned to the selected role.

## Enforce group ownership of applications

You can enforce group ownership of applications by requiring that at least one group is added to an application. Each member of a group has a default role for applications. When that group is added to an application, all members inherit access to the application with the role they have been assigned.

To require an application to have at least one group added to it, complete the following steps:

1. Log in to your APIM Console, and then click **Settings**.
2. From the **Settings** menu, scroll down to the User Management section, and then click **Groups**.
3.  Turn on the toggle that requires an application to have at least one group before it can be created or updated

    <figure><img src="../../.gitbook/assets/00 groups 4.png" alt=""><figcaption></figcaption></figure>

By default, this setting is false. If it is set to true, group selection is required during application creation, and the Management API sends a 400 error in response to an attempt to create an application without a group.

{% hint style="info" %}
If the setting is enabled and there are existing applications without groups, those applications are not impacted. The APIs, subscriptions, and analytics of all applications continue to function properly.
{% endhint %}

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
