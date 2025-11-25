---
description: This article walks through how to configure user and group access to your APIs
---

# User Permissions

## Introduction

The sections below detail how to manage user and group access to individual APIs:

* [Add members to an API](user-permissions.md#add-members-to-an-api)
* [Add groups to an API](user-permissions.md#add-groups-to-an-api)
* [Transfer API ownership](user-permissions.md#transfer-api-ownership)

{% hint style="info" %}
See [User Management and Permissions](../../../administration/user-management-and-permissions.md) to learn more about user and group creation and administration.
{% endhint %}

## Configure API user and group access

To configure user and group access for an API:

1. Log in to your APIM Console
2. Click on **APIs** in the left nav
3. Select your API
4. Click on **Configuration** in the inner left nav
5. Select the **User Permissions** tab

### Add members to an API

Click **+ Add members** to add members to your API or alter member roles, which grant specific permissions. For more information on roles, please refer to the [roles documentation.](../../../administration/user-management-and-permissions.md#roles)

<figure><img src="broken-reference" alt=""><figcaption><p>Add members and alter roles</p></figcaption></figure>

### Add groups to an API

To give groups access to your API, click **Manage groups** and select the desired group(s) from the drop-down menu. This will give all members of that group access to your API.

<figure><img src="broken-reference" alt=""><figcaption><p>Give groups access to your API</p></figcaption></figure>

### Transfer API ownership

If you are the owner of the API, you can transfer ownership to another member, user, or group. Click **Transfer ownership**, then select **API member**, **Other user**, or **Primary owner group.** Next, define the stakeholder to which you want to transfer API ownership and assign that stakeholder a role.

<figure><img src="broken-reference" alt=""><figcaption><p>Transfer API ownership</p></figcaption></figure>
