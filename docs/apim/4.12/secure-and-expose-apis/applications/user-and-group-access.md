---
description: An overview about user and group access.
metaLinks:
  alternates:
    - user-and-group-access.md
---

# User and Group Access

## Overview

An application's **User and group access** page lets you manage user and group access to individual applications.

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

#### Adding members

The **Members** tab is visible when `portal.next.applications.membership.enabled` is `true` and the user has `MEMBER[R]` permission.

To add members to your application:

1. Click **+ Add members**. This button is visible when the user has `MEMBER[C]` permission.
2. Search for existing platform users by entering a query in the search field. Results are sorted by last name (case-insensitive, nulls last). Users without an ID field are excluded from results. When no query is provided, the system defaults to wildcard `*`. User search applies no backend pagination (all results returned, pagination metadata exposed for compatibility).
3. Select one or more users from the search results.
4. Use the **Role** drop-down menu to select member roles, which grant specific permissions. The role defaults to the lowest application role when omitted. Roles must exist and be assignable (not system, not `PRIMARY_OWNER`). For more information on roles, refer to the [Roles](../../configure-and-manage-the-platform/manage-organizations-and-environments/user-management.md#roles) documentation.
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

### Groups

Click the **Groups** tab to see which groups have access to your application. Use the drop-down menu to change group selections.

<figure><img src="../../.gitbook/assets/00 groups added to applications 4.png" alt=""><figcaption></figcaption></figure>

Selecting a group gives all members of that group access to your application.

### Transfer ownership

Under the **Transfer ownership** tab, you can grant complete application access to an application member or other user.

The **Transfer Ownership** button (icon: `swap_horiz`, stroked button) is visible when the current user is the application owner, has `MEMBER[U]` permission, and `portal.next.applications.membership.transferOwnership.enabled` is `true`.

To transfer ownership:

1. Click **Application member** and use the drop-down menu to select a user who is already a member of your application.

    <figure><img src="../../.gitbook/assets/00 groups added to applications 5.png" alt=""><figcaption></figcaption></figure>

    Alternatively, click **Other user** to search for someone who is not a member of your application. You can enter either their name or email into the search field.

    <figure><img src="../../.gitbook/assets/00 groups added to applications 6.png" alt=""><figcaption></figcaption></figure>

2. Select a **New Role** for yourself from the dropdown. Only roles where assignable role validation returns `true` are offered for the current owner's new role. If the **New Role** field is empty or invalid, the submit button is disabled and the error message "Application role is required." is displayed.
3. Click **Transfer** to execute the ownership transfer.

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
