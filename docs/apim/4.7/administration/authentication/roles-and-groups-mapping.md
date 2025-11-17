# Roles and Groups Mapping

## Overview

After you have configured your chosen Identity Provider(s) in Gravitee API Management, you may want to start automatically mapping these user accounts into specific roles and groups within Gravitee. This article focuses on how to configure users' roles/groups/custom claims from your Identity Provider into Roles and Groups in Gravitee API Management.

## Configuration

After adding your Identity Provider, two new items will appear within your Identity Provider configuration; **Groups Mapping** and **Roles Mapping** (as shown below).

<figure><img src="../../../4.6/.gitbook/assets/image (4) (1).png" alt=""><figcaption><p>Identity Provider Groups and Roles Mapping configuration</p></figcaption></figure>

**Groups Mapping** - used for mapping users into groups that can then be assigned to APIs to control their interaction with your API through the API Management console, as well as control visibility of APIs and Documentation pages within the Developer Portal.

_Example 1_: Because you have some APIs you only want your internal users to access, you want to distinguish between internal users, and external customers, to control the visibility of specific APIs in the Developer Portal. You need to create two Groups in Gravitee. Every new customer (signing into the Developer Portal) will be added to the "external-customers" group automatically. For our known internal users, you can create a Group Mapping that queries the users' access\_token (for a specific claim etc) and if it matches a certain condition, then that user will be added to the "internal-users" group. Now you can define specific access controls using these Groups in your APIs User Permissions configuration page.

_Example 2_: You want to give a group of users full ownership rights over a specific API in Gravitee. These users need to grouped together from your Identity Provider (either by a group, metadata, custom claim in their access\_token, etc). You can create a new Group in Gravitee and link it to your specific API (using the "Manage groups" button). Now you can create a new Group Mapping so these new users are automatically mapped into this '"full ownership" Group.

**Roles Mapping** - used for mapping users to Gravitee Roles. Roles provide the user with a functional group of individual permissions to perform certain actions, such as create/read/update/delete on specific actions/pages/configs/etc.

_Example 1_: The built-in `API:PRIMARY_OWNER` role includes full permissions to make any changes to an API - but requires the user (or Group) to be specifically assigned to an API before those permissions can be actually used.

_Example 2_: The built-in `ENVIRONMENT:USER` role enables users to read APIs, create/delete applications, and read documentation.

{% hint style="info" %}
Ultimately, defining groups helps you to assign roles more efficiently for the users.

Users are assigned to Groups. Groups are added to an API, and then configured with a specific Role.
{% endhint %}

<figure><img src="../../../4.6/.gitbook/assets/image (149) (1).png" alt=""><figcaption><p>APIM Console - adding group(s) to the User Permissions page of an API.</p></figcaption></figure>

### Creating a Group and Role Mapping

So let's say we want to map a specific group of users from the Identity Provider, so they have full ownership of a specific API in Gravitee. We need to be able to identify the group of users somehow - this is typically done by a common group membership, metadata, or custom claim. Ultimately, this information will be available in the access\_token provided to Gravitee when the user logs in.

For example; the following access\_token payload includes both a `roles` claim and a `my_API_Group` custom claim.

```json
{
  "aud": "https://graph.microsoft.com",
  "iss": "https://sts.windows.net/123456789-abcd-1234-abcd-1a2b3c4d5e6f/",
  "iat": 1739871619,
  "nbf": 1739871619,
  "exp": 1739875519,
  "app_displayname": "Example App Registration 101",
  "appid": "af38c835-9598-4ce0-b6dd-79541aad6286",
  "appidacr": "1",
  "idp": "https://sts.windows.net/123456789-abcd-1234-abcd-1a2b3c4d5e6f/",
  "idtyp": "app",
  "my_API_Group": "Petstore-Group",
  "oid": "e340ff0e-aaaa-bbbb-cccc-abcdef123456",
  "roles": [
    "FULL_ADMIN",
    "USER"
  ],
  "sub": "e340ff0e-aaaa-bbbb-cccc-abcdef123456",
  "wids": [
    "0997a1d0-0d1d-4acb-b408-d5ca73121e90"
  ]
}
```

We want this user to have FULL\_ADMIN permissions (or the equivalent _role_ in Gravitee), and only for the Petstore API.

#### Group Mapping

Create a new Group Mapping and specify the name of the Group (that you've already added to your API using the 'User Permissions" configuration page).

The Condition (using the Gravitee Expression Language) is how Gravitee evaluates the specific data in the access\_token. In the example below, Gravitee will walk the profile (access\_token) to the "my\_API\_Group" key, and check if its value contains "Petstore-Group". If true, then the user is added into the "Petstore-Group".

<figure><img src="../../../4.6/.gitbook/assets/image (150) (1).png" alt=""><figcaption><p>Group Mapping configuration</p></figcaption></figure>

#### Role Mapping

This can be performed in almost the same way as adding the user into a group. But you'll need to also specify the Role(s) this user will inherit.

In the example screenshot below, this Condition is evaluating the `roles` custom claim (or JSON key) from the access\_token. If the `roles` array contains `FULL_ADMIN`, then Gravitee will action this role mapping.

<figure><img src="../../../4.6/.gitbook/assets/image (152) (1).png" alt=""><figcaption><p>Role Mapping configuration</p></figcaption></figure>
