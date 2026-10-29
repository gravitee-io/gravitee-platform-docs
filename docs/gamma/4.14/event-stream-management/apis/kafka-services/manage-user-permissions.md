---
hidden: false
noIndex: false
description: Decide who can manage a Kafka Service in Event Stream Management. Add members, change their roles, give access to groups, and transfer the primary ownership.
---

# Manage user permissions

The **User Permissions** page of a Kafka Service lists the members of the Kafka Service, directly or through its groups, and the role that each one holds. These members manage the Kafka Service in the console. They're separate from the Kafka clients that connect through its plans.

## Open the user permissions

1. From the Gamma console, open **Event Stream Management**.
2. In the **APIs** group of the sidebar, click **Kafka Services**.
3. Click the name of the Kafka Service.
4. In the **General** group of the Kafka Service sidebar, click **User Permissions**.

The page has three parts:

* The actions: **Transfer ownership**, **Manage groups**, **Add members**, and the notification switch for new members.
* **Direct Members**, the users added to the Kafka Service, with their roles.
* **Group Inherited Members**, the users who reach the Kafka Service through one of its groups. Their roles are managed on the group.

The roles come from the API roles of your organization. The primary owner's role can't change here.

## Add members

1. Click **Add members**.
2. Search for a user by name or email. Results appear from two characters.
3. Select one or more users.
4. In **Role for new members**, select a role.
5. Click **Add member**, or **Add *n* members** when you selected several users.

The console confirms with **Member added**, or with the number of members added.

The **Notify members when they are added to the Kafka Service** switch decides whether new members get a notification. The switch saves at once, and the console confirms with **Notification preference saved**.

## Change a role or remove a member

* To change a member's role, select the new role in the member's row. The change applies at once, and the console confirms with **Member role updated**.
* To remove a member, open the actions menu of the member's row, click **Remove member**, then confirm in the **Remove &lt;name&gt;?** dialog. The console confirms with **Member removed**.

## Give access to groups

1. Click **Manage groups**.
2. Select the groups that should have access to the Kafka Service. The groups that already have access show **Associated**.
3. Click **Save**.

The selection replaces the previous set of groups, and the console confirms with **Groups updated**. The members of the selected groups appear under **Group Inherited Members**.

## Transfer the ownership

Transferring the ownership makes another user the primary owner of the Kafka Service. The console warns that the transfer is irreversible, but a member whose role lets them manage the members of the Kafka Service can transfer the ownership again.

1. Click **Transfer ownership**.
2. Choose the new primary owner:
    * **API Member**. Select one of the members of the Kafka Service.
    * **Other User**. Search for a user by name or email.
3. In **New role for current Primary Owner**, select the role that the current primary owner keeps.
4. Click **Transfer**.

The console confirms with **Ownership transferred**.

## Verification

To verify the permissions, follow these steps:

1. Reload the **User Permissions** page.
2. Check that **Direct Members** lists the members and roles you expect, and that **Group Inherited Members** lists the members of the groups you selected.
