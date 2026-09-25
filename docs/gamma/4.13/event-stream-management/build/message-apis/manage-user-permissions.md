---
hidden: false
noIndex: false
description: Decide who can manage a Message API in Event Stream Management. Add members, change their roles, give access to groups, and transfer the primary ownership.
---

# Manage user permissions

The **User Permissions** page of a Message API lists the members of the Message API, directly or through its groups, and the role that each one holds.

## Open the user permissions

1. From the Gamma console, open **Event Stream Management**.
2. In the sidebar, click **Message APIs**.
3. Click the name of the Message API.
4. In the **General** group of the Message API sidebar, click **User Permissions**.

The page has three parts:

* The actions: **Transfer ownership**, **Manage groups**, **Add members**, and the notification switch for new members.
* **Direct Members**, the users added to the Message API, with their roles.
* **Group Inherited Members**, the users who reach the Message API through one of its groups. Their roles are managed on the group.

The roles come from the API roles of your organization. The primary owner's role can't change here.

## Add members

1. Click **Add members**.
2. Search for a user by name or email. Results appear from two characters.
3. Select one or more users.
4. In **Role for new members**, select a role.
5. Click **Add member**, or **Add *n* members** when you selected several users.

The console confirms with **Member added**, or with the number of members added. The **Notify members when they are added to the Message API** switch decides whether new members get a notification.

## Change a role or remove a member

* To change a member's role, select the new role in the member's row. The change applies at once, and the console confirms with **Member role updated**.
* To remove a member, open the actions menu of the member's row, click **Remove member**, then confirm. The console confirms with **Member removed**.

## Give access to groups

1. Click **Manage groups**.
2. Select the groups that should have access to the Message API. The groups that already have access show **Associated**.
3. Click **Save**.

The selection replaces the previous set of groups, and the console confirms with **Groups updated**. The members of the selected groups appear under **Group Inherited Members**.

## Transfer the ownership

Transferring the ownership makes another user the primary owner of the Message API. The console warns that the transfer is irreversible, but a member whose role lets them manage the members of the Message API can transfer the ownership again.

1. Click **Transfer ownership**.
2. Choose the new primary owner:
    * **API Member**. Select one of the members of the Message API.
    * **Other User**. Search for a user by name or email.
3. In **New role for current Primary Owner**, select the role that the current primary owner keeps.
4. Click **Transfer**.

The console confirms with **Ownership transferred**.

## Verification

To verify the permissions, follow these steps:

1. Reload the **User Permissions** page.
2. Check that **Direct Members** lists the members and roles you expect, and that **Group Inherited Members** lists the members of the groups you selected.
