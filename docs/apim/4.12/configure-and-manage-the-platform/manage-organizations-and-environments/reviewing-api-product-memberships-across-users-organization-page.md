# Reviewing API Product Memberships Across Users (Organization Page)

## Review API Products

The **Organization** → **User details** view aggregates membership across resources. For API Products, this view lists all API Products a user is a member of (directly or through a group), with the role on each. This is useful to audit a user's effective access without opening each API Product individually.

## Add a group with API Product role

From the **Membership** tab, you can add the user to a chosen group with a chosen API Product role. The user then gains the chosen API Product role on every API Product the group is currently attached to.

This action requires the `ENVIRONMENT_USER:READ` permission to review API Products for a user and the `ENVIRONMENT_GROUP:UPDATE` permission to add groups with roles.
