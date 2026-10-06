---
description: This article describes how to configure user and group access to your APIs
---

# User and Group Access

## Introduction

The sections below detail how to manage user and group access to individual APIs:

* [Add members to an API](configure-user-and-group-access.md#add-members-to-an-api)
* [Add groups to an API](configure-user-and-group-access.md#add-groups-to-an-api)
* [Transfer API ownership](configure-user-and-group-access.md#transfer-api-ownership)

{% hint style="info" %}
See [User Management and Permissions](../../../administration/user-management-and-permissions.md) to learn more about user and group creation and administration.
{% endhint %}

## Configure API user and group access

To configure user and group access for your APIs:

1. Log in to APIM Console
2. Select **APIs** from the left nav
3. Select your API
4.  From the inner left nav, select **User and group access**

    <figure><img src="../../../../.gitbook/assets/v2 user and group access.png" alt="The Members panel of an API&#x27;s user and group access page, with member notification enabled and one primary owner listed."><figcaption><p>Configure user and group access</p></figcaption></figure>

### Add members to an API

Click **+ Add members** to add members to your API or alter member roles, which grant specific permissions. For more information on roles, please refer to the [roles documentation.](../../../administration/user-management-and-permissions.md#roles)

<figure><img src="../../../../.gitbook/assets/v2 add members.png" alt="The Members panel with a member&#x27;s role dropdown open, listing OWNER, PRIMARY_OWNER, READ_ONLY, REVIEWER, USER, and WRITER, with USER selected."><figcaption><p>Add members and alter roles</p></figcaption></figure>

### Add groups to an API

To give groups access to your API, click **Manage groups** and select the desired group(s) from the drop-down menu. This will give all members of that group access to your API.

<figure><img src="../../../../.gitbook/assets/v2 manage groups.png" alt="The Manage groups dialog open over the Members panel, with the groups dropdown expanded and each group listed with a clear checkbox."><figcaption><p>Give groups access to your API</p></figcaption></figure>

### Transfer API ownership

If you are the owner of the API, you can transfer ownership to another member, user, or group. Click **Transfer ownership**, then select **API member**, **Other user**, or **Primary owner group.** Next, define the stakeholder to which you want to transfer API ownership and assign that stakeholder a role.

<figure><img src="../../../../.gitbook/assets/v2 transfer ownership.png" alt="The Transfer ownership dialog, with API member selected as the transfer method and no member chosen yet."><figcaption><p>Transfer API ownership</p></figcaption></figure>
