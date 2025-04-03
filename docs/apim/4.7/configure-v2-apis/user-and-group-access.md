---
description: This article describes how to configure user and group access to your APIs
---

# User and Group Access

## Introduction

The sections below detail how to manage user and group access to individual APIs:

* [Add members to an API](user-and-group-access.md#add-members-to-an-api)
* [Add groups to an API](user-and-group-access.md#add-groups-to-an-api)
* [Transfer API ownership](user-and-group-access.md#transfer-api-ownership)

{% hint style="info" %}
See [User Management](../administration/user-management.md) to learn more about user and group creation and administration.
{% endhint %}

## Configure API user and group access

To configure user and group access for your APIs:

1. Log in to APIM Console
2. Select **APIs** from the left nav
3. Select your API
4.  From the inner left nav, select **User and group access**&#x20;

    <figure><img src="../.gitbook/assets/v2 user and group access.png" alt=""><figcaption><p>Configure user and group access</p></figcaption></figure>

### Add members to an API

Click **+ Add members** to add members to your API or alter member roles, which grant specific permissions. For more information on roles, please refer to the [roles documentation.](../administration/user-management.md#roles)

<figure><img src="../.gitbook/assets/v2 add members.png" alt=""><figcaption><p>Add members and alter roles</p></figcaption></figure>

### Add groups to an API

To give groups access to your API, click **Manage groups** and select the desired group(s) from the drop-down menu. This will give all members of that group access to your API.&#x20;

<figure><img src="../.gitbook/assets/v2 manage groups.png" alt=""><figcaption><p>Give groups access to your API</p></figcaption></figure>

### Transfer API ownership

If you are the owner of the API, you can transfer ownership to another member, user, or group. Click **Transfer ownership**, then select **API member**, **Other user**, or **Primary owner group.** Next, define the stakeholder to which you want to transfer API ownership and assign that stakeholder a role.

<figure><img src="../.gitbook/assets/v2 transfer ownership.png" alt=""><figcaption><p>Transfer API ownership</p></figcaption></figure>
