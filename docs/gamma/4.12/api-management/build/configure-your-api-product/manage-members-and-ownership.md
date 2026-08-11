---
hidden: false
noIndex: false
description: Add members, attach groups, change roles, and transfer ownership of an API product. Follow the steps to manage access from the User Permissions tab.
---

# Manage members and ownership

The **User Permissions** tab controls who can view and manage an API product. It is the only page in the **Security** group of the API Product detail sidebar. It covers direct members, members inherited from groups, ownership transfer, and membership notifications.

## Membership model

A user gains access to an API product in one of the following two ways:

* **Direct membership**. The user is added to the product itself and holds a product role. Direct members appear in the **Direct Members** table, where you can change their role or remove them.
* **Group inheritance**. The user belongs to a group that is attached to the product. Inherited members appear in read-only cards under **Group Inherited Members**, one card per group. Their roles are managed at the group level, not on the product.

When a user is both a direct member and a member of an attached group, the permissions granted by each of their roles are combined. The user can perform any operation that at least one of their roles allows.

When you detach a group, that group's members lose their inherited access. The change does not affect anyone who is a direct member of the product.

### Roles

Roles for API products are defined at the organization level with the `API_PRODUCT` scope. The Gamma console offers the following roles when you add a member, change a member's role, or transfer ownership:

| Role      | Permissions on the product                                                                   | Notes                                    |
| --------- | -------------------------------------------------------------------------------------------- | ---------------------------------------- |
| **OWNER** | Create, read, update, and delete the definition, plans, subscriptions, members, and notifications | Preselected in the role picker           |
| **USER**  | Read-only access to the definition, plans, subscriptions, members, and notifications          | The default role for the `API_PRODUCT` scope |

`PRIMARY_OWNER` is a third, system-managed role for the `API_PRODUCT` scope. It is never offered in a role picker: it is held by exactly one member, and it can only move to another user through **Transfer ownership**.

### Primary owner

Every API product has a single primary owner, assigned when the product is created. In the **Direct Members** table, the primary owner's role is shown as a **Primary Owner** badge, and the row has no actions menu. As a result, the primary owner cannot be given a different role or removed from the product while they hold that role.

## Open the User Permissions tab

1. From the Gamma console sidebar, select **API Management**.
2. From the module navigation, select **API Products**.
3. Select the product you want to configure.
4. In the product detail sidebar, under **Security**, select **User Permissions**.

The page header is **User Permissions**, followed by an action bar with the membership notification toggle and the **Transfer ownership**, **Manage groups**, and **Add members** actions.

The product **Overview** page also reports a **Direct product members** count, and its onboarding checklist links to this tab from the **Invite teammates and assign roles** row.

## Add members

1. On the **User Permissions** tab, select **Add members**.
2. In the **Add Members** panel, type at least two characters into the search field to search for users by name or email. Users who are already members of the product are excluded from the results.
3. Select each user you want to add. Selected users are listed as removable chips above the role picker, and the panel reports how many users are selected.
4. From **Role for new members**, select **OWNER** or **USER**. The same role is applied to every user you selected in this panel.
5. Select **Add member**. When you have selected more than one user, the button reads **Add \<n> members**.

To leave without adding anyone, select **Cancel**.

## Change a member's role

1. In the **Direct Members** table, open the actions menu at the end of the member's row.
2. Select **Edit role**.
3. Choose the new role from the picker that replaces the role badge.
4. Select **Save**, or discard the change with the cancel button beside it.

The actions menu is not rendered for the primary owner.

## Remove a member

1. In the **Direct Members** table, open the actions menu at the end of the member's row.
2. Select **Remove member**.
3. In the **Remove API member** confirmation dialog, select **Remove**.

When you remove a direct member, only their direct access is revoked. If they also belong to a group attached to the product, they keep the access that group grants.

## Transfer ownership

When you transfer ownership, the `PRIMARY_OWNER` role moves to another user, and the previous primary owner is assigned a different product role. The action cannot be undone.

1. On the **User Permissions** tab, select **Transfer ownership**.
2. Choose one of the following sources for the new primary owner:
    * **API Member**. Select an existing product member from **Select API member**. The current primary owner is not listed.
    * **Other User**. Search the organization's users by name or email, typing at least two characters, and then select the user from the results.
3. From **New role for current Primary Owner**, select the role the outgoing primary owner receives. **OWNER** and **USER** are offered, and **OWNER** is preselected. The panel restates the choice in a warning that the action is irreversible.
4. Select **Transfer**.

The **Transfer** button stays disabled until you have selected both a new primary owner and a role for the current one. To leave the primary owner unchanged, select **Cancel**.

## Attach groups to a product

1. On the **User Permissions** tab, select **Manage groups**.
2. In the **Manage groups** panel, use the search field to filter the environment's groups by name.
3. Select the checkbox for each group that should have access to the product, and clear the checkbox for each group whose access you want to remove. Groups already attached to the product carry an **Associated** badge, and the panel reports how many groups are selected.
4. Select **Save**.

If the environment has no groups, the panel reports **No groups found in this environment.**

Members of the groups you attach appear under **Group Inherited Members**, in one card per group, with the role that group grants them for the `API_PRODUCT` scope.

## Membership notifications

The toggle in the action bar, **Notify members when they are added to the product**, controls whether users are notified when they gain membership. It is enabled by default and is saved as part of the product configuration as soon as you change it.

## Required permissions

Product roles map to permission checks on the Management API, so the operations on this tab need the following:

| Operation                             | Required permission        |
| ------------------------------------- | -------------------------- |
| View members                          | `api_product-member-r`     |
| Add a member                          | `api_product-member-c`     |
| Change a member's role                | `api_product-member-u`     |
| Remove a member                       | `api_product-member-d`     |
| Transfer ownership                    | `api_product-member-u`     |
| Attach or detach groups               | `api_product-definition-u` |

## Next steps

* [Manage product APIs](manage-product-apis.md). Attach the API proxies your product bundles.
* [Configure API products](README.md). Review the other product configuration areas.
