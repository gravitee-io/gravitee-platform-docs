---
description: An overview about user and group access.
metaLinks:
  alternates:
    - user-and-group-access.md
---

# User and Group Access

## Overview

An application's **User and group access** page lets you to manage user and group access to individual applications.

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

Under the **Members** tab, you can add users or groups as members of your application and define their roles to manage and perform tasks and operations.

<figure><img src="../../.gitbook/assets/00 groups added to applications 3.png" alt=""><figcaption></figcaption></figure>

The Members tab displays all registered users who have been granted a role on the application. Each member entry shows the user's display name, email, role, and timestamps for when the membership was created and last updated.

Use the search field to filter members by display name. The search supports partial, case-insensitive matching. Pagination controls appear when the member count exceeds the page size (default: 10 members per page).

{% hint style="warning" %}
If the page number is less than 1 or the start index is greater than or equal to the total count, the system throws a `PaginationInvalidException`.
{% endhint %}

#### Add members in the Console

* Click **+ Add members** to add members to your application. You can search for users by name or email.
* Use the **Role** drop-down menu to select member roles, which grant specific permissions. For more information on roles, please refer to the [Roles](../../configure-and-manage-the-platform/manage-organizations-and-environments/user-management.md#roles) documentation.

#### Add members in the Developer Portal

The **Members** tab is visible in the Developer Portal when `portal.next.applications.membership.enabled` is `true` and you have the `MEMBER[R]` permission.

To add a registered user as an application member, click **Add member** and search for the user by display name, first name, last name, or email. Select the user from the search results, choose an application role from the dropdown, and click **Add**.

| Field | Description |
|:------|:------------|
| **User** | Search for a registered platform user by display name, first name, last name, or email. Users without an ID are excluded from results. Users already members of the application are annotated with `isAlreadyMember: true` but remain selectable. The current primary owner is marked `isDisabled: true` in search results. |
| **Role** | Select an application role from the dropdown. Only non-system roles are shown. The `PRIMARY_OWNER` role is excluded from assignable roles. If the role is omitted, the system assigns the lowest application role by default. |

The system validates that the user is not already a member and that no pending invitation exists for their email address. If the user is already a member, the request is rejected with a 409 Conflict response. If a pending invitation exists for the user's email, the system throws a `ConflictDomainException` with the message "A pending application invitation already exists for email [{email}]." Member creation is limited to 3 concurrent requests.

#### Update member roles

To change a member's role:

1. Click the **Edit** action next to the member's name.
2. Select a new role from the dropdown.
3. Click **Save**.

Only non-system roles are available. The `PRIMARY_OWNER` role is excluded from assignable roles. The system validates that the role exists in the organization and throws a `RoleNotFoundException` if the role is not found.

#### Remove members

To remove a member from the application:

1. Click the **Delete** action next to the member's name.
2. Confirm the deletion.

The member's application role is revoked immediately. This action does not delete the user's platform account or affect their memberships in other applications.

### Invitations

Navigate to **Applications > [Application Name] > Invitations** (visible when `portal.next.applications.membership.invitations.enabled` is `true`).

The Invitations tab displays all pending invitations for the application. Each invitation entry shows the recipient's email address, assigned role, and timestamps for when the invitation was created and last updated.

Use the search field to filter invitations by email address. The search supports partial, case-insensitive matching using SQL `LIKE`.

{% hint style="warning" %}
The JDBC implementation no longer escapes SQL LIKE wildcards (`%`, `_`, `\`). User input containing these characters will be treated as wildcards.
{% endhint %}

Pagination controls appear when the invitation count exceeds the page size (default: 10 invitations per page). The repository uses 0-based page indexing internally (`pageNumber - 1`) while the API uses 1-based pagination.

#### Create invitations

1. Click **Invite members**.
2. Enter one or more email addresses.
3. Select an application role.
4. Optionally provide a confirmation page URL.
5. Toggle **Send notification** to send an email notification to each recipient.
6. Click **Invite**.

The system normalizes each email address to lowercase and trims whitespace before processing. For each recipient:

* If the email matches exactly one existing registered user, that user is added directly as an application member. No invitation is created.
* If the email matches multiple existing users, the request is rejected with a 409 Conflict response. No invitations or members are created.
* If the email matches no existing user, a pending invitation is created.
* If the email already has a pending invitation for the application, the request is rejected with a 409 Conflict response.
* If the recipient is already an application member, that recipient is skipped and the remaining recipients are processed.

{% hint style="warning" %}
If the role is `PRIMARY_OWNER` and any recipient matches an existing user, the system throws a `SinglePrimaryOwnerException` and rejects the request. If the role is `PRIMARY_OWNER` and all recipients are unknown, pending invitations are created.
{% endhint %}

Email validation, duplicate detection, and pending invitation conflicts are checked before any write operations. If any validation fails, no invitations or members are created. Notifications are dispatched asynchronously only when **Send notification** is enabled and at least one pending invitation was created. If all recipients matched existing users (added as members), no notifications are sent.

| Field | Description |
|:------|:------------|
| **Recipients** | Enter one or more email addresses. Each email is validated using `jakarta.mail.internet.InternetAddress` with strict validation. Invalid emails trigger a `ValidationDomainException` with the message "Application invitation email is invalid: {email}". Duplicate emails in the request trigger a validation error with the message "already selected". |
| **Role** | Select an application role from the dropdown. The role must not be blank or whitespace-only. If the role is blank, the system throws a `ValidationDomainException` with the message "Application invitation role must not be blank." If the role does not exist in the organization, the system throws a `RoleNotFoundException`. |
| **Confirmation Page URL** | Provide a URL where the recipient can accept the invitation. This URL is included in the invitation email. |
| **Send Notification** | Toggle to send an email notification to each recipient. Enabled by default. |

#### Update invitation roles

To change an invitation's role before it is accepted:

1. Click the **Edit** action next to the invitation.
2. Select a new role from the dropdown.
3. Click **Save**.

The role must not be blank or whitespace-only. If the role is blank, the system throws a `ValidationDomainException` with the message "Application invitation role must not be blank." If the role does not exist in the organization, the system throws a `RoleNotFoundException`. System roles and the `PRIMARY_OWNER` role are excluded from assignable roles in the UI.

#### Resend invitations

To resend an invitation email:

1. Click the **Resend** action next to the invitation.
2. Provide a confirmation page URL.
3. Click **Resend**.

The system validates that the invitation exists and belongs to the application. If the invitation is not found or belongs to another application, the system throws an `ApplicationInvitationNotFoundException`. A new email notification is sent to the recipient with the updated confirmation URL.

#### Delete invitations

To delete a pending invitation:

1. Click the **Delete** action next to the invitation.
2. Confirm the deletion.

The invitation is removed immediately. The recipient will no longer be able to accept the invitation using the original token.

#### Accept invitations

When a user receives an invitation email, they click the confirmation link to navigate to **User > Invitation > Confirm** in the Developer Portal. The confirmation page displays the recipient's email address (prefilled and disabled) and prompts the user to provide their first name, last name, and password. If the user already has a platform account, they can skip the password fields.

1. Enter your first name.
2. Enter your last name.
3. Choose a password (required for new users).
4. Re-enter your password to confirm.
5. Click **Accept invitation**.

The system decodes the JWT token from the URL, extracts the `action`, `email`, and optional `subject` (existing user ID) claims, and validates the token signature and issuer. If the token is invalid, the page displays "Invalid token" with the message "Invalid token value". If the token action is `RESET_PASSWORD`, the system rejects the request with a 409 Conflict response and the message "Reset password forbidden on this resource".

If the `subject` claim is present, the system validates that the user exists and does not already have a password set. If the user already has a password, the system throws a `UserAlreadyFinalizedException`. If the user is not found, the system throws a `UserNotFoundException`. If the `subject` claim is absent, the system creates a new user account using the provided first name, last name, and email.

If a password is provided, the system validates the password format via `PasswordValidator.validate`, encodes the password, and stores it. If the password is invalid, the system throws a `PasswordFormatInvalidException`. If no password is provided, the user account is created or updated without a password.

The system assigns default organization roles and default environment roles to the new user. If default roles are not found, the system throws a `DefaultRoleNotFoundException`. The system then retrieves all pending invitations matching the user's email address, adds the user to each application with the specified role, and deletes each invitation. If no invitations are found, the system throws an `InvitationCanceledException` with the message "No active invitation found for email [<email>]".

Finally, the system creates an `OrganizationAuditLogEntity` with event `USER_CREATED` and triggers a `PortalHook.USER_REGISTERED` notification. The confirmation page displays "Invitation accepted" with a link to log in.

| Field | Description |
|:------|:------------|
| **First Name** | Enter your first name. Required. If blank, the system displays "First name is required". |
| **Last Name** | Enter your last name. Required. If blank, the system displays "Last name is required". |
| **Email** | Your email address. Prefilled from the invitation token and disabled. |
| **Password** | Choose a password. Required for new users. If blank, the system displays "Password is required". |
| **Confirm Password** | Re-enter your password. Must match the password field. If the passwords do not match, the system displays "Passwords do not match". |

### Groups

Click the **Groups** tab to see which groups have access to your application. Use the drop-down menu to change group selections.

<figure><img src="../../.gitbook/assets/00 groups added to applications 4.png" alt=""><figcaption></figcaption></figure>

Selecting a group gives all members of that group access to your application.

### Transfer ownership

Under the **Transfer ownership** tab, you can grant complete application access to an application member or other user.

The **Transfer ownership** button is visible when you are the current primary owner, you have the `MEMBER[U]` permission, and `portal.next.applications.membership.transferOwnership.enabled` is `true`.

Click **Application member** and use the drop-down menu to select a user who is already a member of your application.

<figure><img src="../../.gitbook/assets/00 groups added to applications 5.png" alt=""><figcaption></figcaption></figure>

Click **Other user** to search for someone who is not a member of your application. You can enter either their name or email into the search field. Once you've selected a new primary owner for your application, use the drop-down to assign their role.

<figure><img src="../../.gitbook/assets/00 groups added to applications 6.png" alt=""><figcaption></figcaption></figure>

The system validates that the target user is already an application member. If the target is not a member, the request is rejected. The system validates that the new role for the current owner exists in the organization. If the role is not found, the system throws a `RoleNotFoundException`. The transfer is atomic: the target becomes the new primary owner, and the former owner assumes the specified role.

| Field | Description |
|:------|:------------|
| **New Primary Owner** | Search for a registered application member by display name, first name, last name, or email. The current primary owner is marked `isDisabled: true` in search results and cannot be selected. |
| **Application Role** | Select a new application role for yourself. Required. If blank, the system displays "Application role is required." |

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
