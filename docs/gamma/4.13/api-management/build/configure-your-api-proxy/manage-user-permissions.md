---
description: >-
  Add members, attach groups, change roles, and transfer primary ownership of
  an API proxy.
hidden: false
noIndex: false
---

# Manage user permissions

The **User Permissions** page manages who can interact with your API through the API Management console. Access comes either from direct membership, or is inherited through groups.

To open the page, follow these steps:

1. Click **API Proxies** in the module sidebar.
2. Select your API proxy.
3. Click **User Permissions** in the API proxy sidebar.

<!-- TODO: Screenshot of the User Permissions page -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-user-permissions.png" alt=""><figcaption><p>The User Permissions page</p></figcaption></figure>

The **Notify members when they are added to the API** toggle at the top of the page controls membership notifications.

## Add direct members

The **Direct Members** section lists users with direct access to this API. You change their roles or remove them from here.

To add members, follow these steps:

1. Click **Add members**.
2. In the **Add Members** panel, search for users by name or email.
3. Select one or more users.
4. Under **Role for new members**, select the role. The primary owner role isn't assignable from this list.
5. Confirm to add the selected users.

To change a member's role, edit it inline in the **Direct Members** table. To remove a member, use the remove action and confirm with **Remove**.

## Attach groups

The **Group Inherited Members** section lists members whose access comes through their group membership. Their roles are managed at the group level, not on this page.

To attach or detach groups, follow these steps:

1. Click **Manage groups**.
2. In the **Manage groups** panel, select the groups that should have access to this API.
3. Confirm the selection.

## Transfer ownership

To transfer primary ownership of this API to another user, follow these steps:

1. Click **Transfer ownership**.
2. In the **Transfer ownership** panel, select an existing API member, or search for a user by name or email.
3. Under **New role for current Primary Owner**, select the role the current primary owner is reassigned to.
4. Confirm the transfer.

## Verification

To verify the permissions are working as expected, follow these steps:

1. Add a user as a direct member with a role that grants read-only access.
2. Sign in as that user and open the API. The read-only screens are visible, and editing actions stay unavailable.

<!-- TODO: Screenshot of the Direct Members table with the added member -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-user-permissions-member.png" alt=""><figcaption><p>The Direct Members table</p></figcaption></figure>
