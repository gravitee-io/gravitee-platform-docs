---
hidden: true
noIndex: true
---

# Reviewing API Product Memberships Across Users

## Review API Products

1. From the **Dashboard**, click **Organization**.
2. In the **Organization** menu, click **Users**.
3. Click the name of the user that you want to view.
4. Navigate to the **Membership** section. You can view the API Products that user is a member of. This section lists all API Products a user is a member of, either directly or through a group, with the role on each. This information is useful to audit a user's effective access without opening each API Product individually.

## Add a group with API Product role

From the **Membership** tab, you can add the user to a chosen group with a chosen API Product role. The user then gains the chosen API Product role on every API Product the group is currently attached to. This action requires the `ENVIRONMENT_USER:READ` permission to review API Products for a user and the `ENVIRONMENT_GROUP:UPDATE` permission to add groups with roles. to add a user to a group with an API Product role, complete the following steps:

1. From the **Membership** tab, clock **+ Add a group**.
2. From the ** Add a group with roles** pop-up menu, assign the user to a group and one or more roles by completing the following steps:
 a. From the **Group** dropdown menu, select the group that you want to assign the user to.
 b. (Optional) Enable the **Group admin role**, which provides the user with admin permissions for that group.
 c. From the **API Role** dropdown menu, select the role that you want to assign to the user.
 d. From the **API Product Role** dropdown menu, select the API Product Role for the user.
 e. From the **Application Role** dropdown menu, select the Application Role for the user.
 f. From the **Integration Role** dropdown menu, select the Integration Role for the user.
 g. Click **Save**.

 ## Verification

 The API Product appears in the **API Products** section.

