# manage-members

## Overview

When you first create your API, by default it is defined as a private API and cannot be accessed through APIM Portal or subscribed to.

If you want to grant specific users or groups access to a private API, the way to do this is by managing its members.

Only users with the required permissions can manage an application’s members. For more details, see link:\{{ _/apim/3.x/apim\_adminguide\_roles\_and\_permissions.html_ | relative\_url \}}\[Roles and permissions].

## Roles

By default, APIM includes three membership roles:

| Role              | Description                                                                                                                                                 |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Primary Owner** | When an API is created, the Primary Owner is the creator of the API. A Primary Owner can perform all possible actions on an API.                            |
| **Owner**         | Owner is similar to the Primary Owner role. An Owner can perform all the same actions on an API apart from change the context-path of the API or delete it. |
| **User**          | A User is a person who can access the API and subscribe to it through a plan.                                                                               |

### Primary Owner groups

New in version 3.7

From APIM 3.7, APIM Console provides a configurable mode to define how you manage the primary owners of your API. For more details, see link:\{{ _/apim/3.x/apim\_adminguide\_users\_and\_groups.html#primary\_owner\_mode_ | relative\_url \}}\[Configure primary owners as groups^].

## Add and remove users

You can manage users for APIs and applications.

1. link:\{{ _/apim/3.x/apim\_quickstart\_portal\_login.html_ | relative\_url \}}\[Log in to APIM Console^].
2. If you want to manage users for an:
   * application, click **Applications** in the menu, then select your application and click **Members**.
   *   API, click **APIs** in the menu, then select your API and click **Portal > Members**.

       image::\{% link images/apim/3.x/api-publisher-guide/members/manage-members.png %\}\[Gravitee.io - manage members]

To add new users:

1. Click the plus icon image:\{% link images/icons/plus-icon.png %\}\[role="icon"] at the bottom right of the page.
2.  Search for the user with the form, then select the user.

    image::\{% link images/apim/3.x/api-publisher-guide/members/manage-members-add.png %\}\[Gravitee.io - add member,300]

To remove users:

Navigate to the **Members** page for the API or application as described above, then click the delete icon next to the user.

image::\{% link images/apim/3.x/api-publisher-guide/members/manage-members-remove.png %\}\[Gravitee.io - remove member]

## Transfer ownership

You can transfer ownership of an API or application from one user to another. You do this when the current Primary Owner leaves a project, for example.

From APIM 3.7, you can also transfer ownership to a group, depending on your configuration. For more details, see link:\{{ _/apim/3.x/apim\_adminguide\_users\_and\_groups.html#primary\_owner\_mode_ | relative\_url \}}\[Configure primary owners as groups^].

1. In APIM Console, click **APIs** or **Applications** in the left menu.
2. If you want to transfer ownership for an:
   * application, click **Applications** in the menu, then select your application and click **Members**.
   * API, click **APIs** in the menu, then select your API and click **Portal > Transfer ownership**.
3.  Choose the new Primary Owner or Primary Owner Group.

    You can only select a Primary Owner Group which you belong to. If your Primary owner mode is configured as **GROUP**, you can only select a Primary Owner Group and not a user.
4. Choose the new role of the current Primary Owner, if the current Primary Owner is a user.
5.  Click **TRANSFER**.

    image::\{% link images/apim/3.x/api-publisher-guide/members/manage-members-transfer-ownership.png %\}\[Gravitee.io - transfer ownership]
