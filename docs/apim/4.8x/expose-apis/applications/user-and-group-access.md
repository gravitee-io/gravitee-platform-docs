# User and Group Access

## Overview

An application's **User and group access** page lets you to manage user and group access to individual applications.

## Configure user and group access

To configure user and group access, complete the following steps:

1. [create-an-application.md](create-an-application.md "mention").
2. Log in to your APIM Console, and then click **Applications**.
3.  Find the application you want to configure. Use the radio buttons to select either Active or Archived applications. Next, either scroll through the paginated lists of available applications or use the search field to find the application by name.\


    <figure><img src="../../.gitbook/assets/00 groups added to applications 7.png" alt=""><figcaption></figcaption></figure>
4. Click on the application you want to configure.
5.  Click on **User and group access** in the Application menu.\


    <figure><img src="../../.gitbook/assets/00 groups added to applications 8.png" alt=""><figcaption></figcaption></figure>

### Members

Under the **Members** tab, you can add users or groups as members of you application and define their roles to manage and perform tasks and operations.

<figure><img src="../../.gitbook/assets/00 groups added to applications 3.png" alt=""><figcaption></figcaption></figure>

* Click **+ Add members** to add members to your application. You can search for users by name or email.&#x20;
* Use the **Role** drop-down menu to select member roles, which grant specific permissions. For more information on roles, please refer to the [Roles](../../administration/user-management.md#roles) documentation.

### Groups

Click the **Groups** tab to see which groups have access to your application. Use the drop-down menu to change group selections.&#x20;

<figure><img src="../../.gitbook/assets/00 groups added to applications 4.png" alt=""><figcaption></figcaption></figure>

Selecting a group gives all members of that group access to your application.

### Transfer ownership

Under the **Transfer ownership** tab, you can grant complete application access to an application member or other user.&#x20;

Click **Application member** and use the drop-down menu to select a user who is already a member of your application.&#x20;

<figure><img src="../../.gitbook/assets/00 groups added to applications 5.png" alt=""><figcaption></figcaption></figure>

Click **Other user** to search for someone who is not a member of your application. You can enter either their name or email into the search field. Once you've selected a new primary owner for your application, use the drop-down to assign their role.

<figure><img src="../../.gitbook/assets/00 groups added to applications 6.png" alt=""><figcaption></figcaption></figure>

## Enforce group ownership of applications

You can enforce group ownership of applications by requiring that at least one group is added to an application. Each member of a group has a default role for applications. When that group is added to an application, all members inherit access to the application with the role they have been assigned.

To require an application to have at least one group added to it, complete the following steps:

1. Log in to your APIM Console, and then click **Settings**.
2. From the **Settings** menu, scroll down to the User Management section, and then click **Groups**.
3.  Turn on the toggle that requires an application to have at least one group before it can be created or updated\


    <figure><img src="../../.gitbook/assets/00 groups 4.png" alt=""><figcaption></figcaption></figure>

By default, this setting is false. If it is set to true, group selection is required during application creation, and the Management API sends a 400 error in response to an attempt to create an application without a group.

{% hint style="info" %}
If the setting is enabled and there are existing applications without groups, those applications are not impacted. The APIs, subscriptions, and analytics of all applications continue to function properly.
{% endhint %}
