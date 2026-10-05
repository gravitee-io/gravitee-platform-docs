---
hidden: false
noIndex: false
description: Decide who can manage a Cluster or a Virtual Cluster in Event Stream Management. Add members, change their roles, give access to groups, and transfer the primary ownership.
---

# Manage cluster permissions

The **User Permissions** page of a Cluster lists its members and the role that each one holds on it. A Virtual Cluster has the same page, with the same roles and actions.

## Open the user permissions

1. From the Gamma console sidebar, select **Event Stream Management**.
2. In the **Kafka Infrastructure** group, select **Clusters**, or **Virtual Clusters**.
3. Select the name of the Cluster or the Virtual Cluster.
4. In the **General** group of the sidebar, select **User Permissions**.

The page has three parts:

* **Your permissions**, the access that you hold on the Cluster for each of **Definition**, **Configuration**, **Members**, and **Analytics**, from **No access** to **Full access**.
* The actions that your role allows: **Transfer ownership**, **Manage groups**, and **Add members**.
* **Direct Members**, the users added to the Cluster, with their **Display name** and **Roles**.

## Cluster roles

A Cluster carries the following roles:

| Role | What it allows |
| --- | --- |
| **Primary Owner** | The creator of the Cluster holds this role. Only a transfer moves it to another user, and the primary owner can't be removed. |
| **Owner** | Every action on the Cluster: read and update its definition and its configuration, delete it, and manage its members. |
| **User** | Read the definition and the members of the Cluster. The connection configuration isn't included. |

These roles decide what the Management API lets a user do to one Cluster. The `CLUSTER` permissions of the user's environment role still decide which pages and actions the console offers at all, such as **Create Cluster**, the lifecycle actions, and **Delete cluster**.

## Add members

1. Select **Add members**.
2. Search for a user by name or email, and select one or more users in the results. Users who are already members aren't offered.
3. In **Role for new members**, select **User** or **Owner**.
4. Select **Add member**, or **Add *n* members** when you selected several users.

The console confirms with **Member added**.

## Change a role or remove a member

* To change a member's role, select **User** or **Owner** in the member's row. The change applies at once, and the console confirms with **Member role updated**.
* To remove a member, open the row menu of the member, and select **Remove member**. In the **Remove \<name\>?** dialog, select **Remove member**. The console confirms with **Member removed**.

The primary owner's role can't be changed here, and the primary owner can't be removed. Transfer the ownership first.

## Give access to groups

1. Select **Manage groups**.
2. Select the groups that should have access to the Cluster. The groups that already have access show **Associated**.
3. Select **Save**.

The selection replaces the previous set of groups, and the console confirms with **Groups updated**.

## Transfer the ownership

Transferring the ownership makes another user the primary owner of the Cluster.

1. Select **Transfer ownership**.
2. In **New primary owner**, search for the user and select them.
3. Optional: in **Current owner's new role**, select the role that the current primary owner keeps, **User** or **Owner**. The default, **Keep current role**, leaves that role unchanged.
4. Select **Transfer ownership**.

The console confirms with **Ownership transferred**. If the transfer fails, the dialog shows **Transfer failed** with the reason and stays open.

## Verification

To verify the permissions, follow these steps:

1. Reload the **User Permissions** page.
2. Check that **Direct Members** lists the members and the roles that you expect.

## Next steps

* **Manage the Cluster**. See [Manage clusters](manage-a-cluster.md).
