# Roles and Groups Mapping

## Overview

Groups let you more efficiently assign roles to users. Users are assigned to groups, and then groups are assigned to APIs and configured with specific roles.

Once you configure your chosen identity provider(s) in API Management, you can automatically map these user accounts into specific roles and groups within Gravitee. This article explains how to convert user roles, groups, and custom claims from your identity provider into Gravitee roles and groups.

## Configuration

After you add your identity provider, two new items appear within your identity provider configuration: **Groups Mapping** and **Roles Mapping**.

<figure><img src="../../../.gitbook/assets/image (37).png" alt=""><figcaption></figcaption></figure>

**Groups Mapping** maps users into groups. Groups can be assigned to APIs. You can use the APIM Console to control the interactions between groups and the APIs to which they are assigned. The visibility of APIs and API documentation pages can be controlled at the group level using the Developer Portal.

<details>

<summary>Example 1</summary>

If you want to give only internal users access to certain APIs, you can create two groups in Gravitee to distinguish between internal and external users, and then control API visibility using the Developer Portal.

Every new user who signs into the Developer Portal is automatically added to the "external" users group, while the access tokens of known internal users are queried via Group Mapping against specific conditions. If a known user's access token matches a given condition, the user is added to the "internal" user group.

You can define access controls via the groups on your API's User Permissions configuration page.

</details>

<details>

<summary>Example 2</summary>

To provide certain users with full ownership rights over a specific Gravitee API, these users must be grouped by your identity provider. For example, through a group, metadata, or custom access token claims.

You can create a new group in Gravitee, and then link it to your specific API. Next, you can create a new Group Mapping to automatically map these new users into the group with full ownership permissions.

</details>

**Roles Mapping** maps users to Gravitee roles. Roles provide the user with a functional group of individual permissions to perform certain actions. For example, permissions to create, read, update, or delete specific pages or configurations. &#x20;

<details>

<summary>Example 1</summary>

The built-in `API:PRIMARY_OWNER` role gives a user or group assigned to an API full permissions to modify that specific API.

</details>

<details>

<summary>Example 2</summary>

The built-in `ENVIRONMENT:USER` role allows the user to read APIs, create and delete applications, and read documentation.

</details>

The specific group of users you intend to map from an identity provider is typically identified by a common group membership, metadata, or custom claim. This information is available in the access token provided to Gravitee when the user logs in.

## Create group and role mapping

In the following example, the access token payload includes both a `roles` claim and a `my_API_Group` custom claim.

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

The following example configurations grant the user FULL\_ADMIN permissions, or the equivalent role in Gravitee, for the Petstore API only.

### Groups Mapping

Create a new Groups Mapping and specify the name of the group that you've already added to your API via the **User Permissions** configuration page.

Gravitee uses Gravitee Expression Language in the **Condition** to evaluate the specific data in the JSON returned by the IdP’s UserInfo endpoint.&#x20;

In the example below, Gravitee walks the profile, which is the UserInfo endpoint's response payload, to the "my\_API\_Group" key, and then checks if its value contains "Petstore-Group."  If true, the user is added to the "Petstore-Group."

<figure><img src="../../../.gitbook/assets/image (192).png" alt=""><figcaption><p>Group Mapping configuration</p></figcaption></figure>

### Roles Mapping

The procedure for mapping a role is similar to adding a user to a group, but the role(s) the user inherits must also be specified.

In the example below, the condition evaluates the `roles` custom claim, or JSON key, in the JSON returned by the IdP’s UserInfo endpoint. If the `roles` array contains `FULL_ADMIN`, Gravitee will actions the role mapping.

<figure><img src="../../../.gitbook/assets/image (194).png" alt=""><figcaption><p>Role Mapping configuration</p></figcaption></figure>
