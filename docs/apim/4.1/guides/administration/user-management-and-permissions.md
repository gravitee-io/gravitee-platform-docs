---
description: >-
  This article walks through how to set up and manage Gravitee roles, scopes,
  permissions, users, and user groups.
---

# User Management and Permissions

### Introduction

In this article, we will walk through how to set up:

* Roles
* Permissions
* Users
* User groups

{% hint style="info" %}
**By default**

By default, **System Admins** (a role created by Gravitee) are the only roles that can create and edit more roles. However, you can create your own custom roles with these permissions.
{% endhint %}

### Roles

{% @arcade/embed url="https://app.arcade.software/share/KyYnhU8h2uPwM46fbMdk" flowId="KyYnhU8h2uPwM46fbMdk" %}

Gravitee API Management (APIM) allows you to create custom user roles to fit your needs. A role is a functional group of permissions, and can be defined at the Organization, Environment, API, and/or Application levels.

Gravitee comes with some pre-built default roles, but there is no limit to the number of custom roles that you can create. Each role:

* Is associated with a group of permissions
* Has a **Scope**
  * A **Scope** is essentially the level of API Management resources that a user can act within. The **Scope** in Gravitee are:
    * Organization
    * Environment
    * API
    * Application
* Defines what you can do with the APIM UI components and the APIM Management API

To set up roles, log-in to the Gravitee API Management Console, and select Organization in the left-hand nav. In your Organization settings, select **Roles** from the **User Management** section. You'll be brought to the **Roles** page. Here, you can add, see members within, and delete roles at the Organization, Environment, API, and Application Scopes. Depending on which Scope a role is created at, that role will have a different set of permissions. Please see the following tables that describe the permissions per scope:

#### Organization permissions

<table><thead><tr><th width="180">Name</th><th>Description</th></tr></thead><tbody><tr><td>USER</td><td>Manages users.</td></tr><tr><td>ENVIRONMENT</td><td>Manages environments.</td></tr><tr><td>ROLE</td><td>Manages roles.</td></tr><tr><td>TAG</td><td>Manages sharding tags.</td></tr><tr><td>TENANT</td><td>Manages tenants.</td></tr><tr><td>ENTRYPOINT</td><td>Manages environment entrypoint configuration.</td></tr></tbody></table>

#### Environment permissions

| Name                           | Description                                                                                                                                                                                                                    |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| INSTANCE                       | Access to API Gateway instance information. Only `READ` permission is used.                                                                                                                                                    |
| GROUP                          | Manages user groups.                                                                                                                                                                                                           |
| TAG                            | Manages sharding tags. **Deprecated, will be removed on 3.10.0**                                                                                                                                                               |
| TENANT                         | Manages tenants. **Deprecated, will be removed on 3.10.0**                                                                                                                                                                     |
| API                            | Manages APIs in general. This means that the `CREATE` action is used to establish if the user is allowed to create an API or not, and the `READ` permission to allow the user to request the policies list and resources list. |
| APPLICATION                    | Manages applications in general. `CREATE` allows the user to create an application, `READ` allows the user to list applications.                                                                                               |
| PLATFORM                       | Gets APIM monitoring metrics. Only `READ` permission is used.                                                                                                                                                                  |
| AUDIT                          | Gets APIM audit. Only `READ` permission is used.                                                                                                                                                                               |
| NOTIFICATION                   | Manages global notifications.                                                                                                                                                                                                  |
| MESSAGE                        | Manages messaging.                                                                                                                                                                                                             |
| DICTIONARY                     | Manages environment dictionaries.                                                                                                                                                                                              |
| ALERT                          | Manages environment alerting.                                                                                                                                                                                                  |
| ENTRYPOINT                     | Manages environment entrypoint configuration. **Deprecated, will be removed on 3.10.0**                                                                                                                                        |
| SETTINGS                       | Manages environment settings.                                                                                                                                                                                                  |
| DASHBOARD                      | Manages environment dashboards.                                                                                                                                                                                                |
| QUALITY\_RULE                  | Manages environment quality rules.                                                                                                                                                                                             |
| METADATA                       | Manages APIM metadata.                                                                                                                                                                                                         |
| DOCUMENTATION                  | ManageS APIM Portal documentation.                                                                                                                                                                                             |
| CATEGORY                       | Manages categories.                                                                                                                                                                                                            |
| TOP\_APIS                      | Manages top apis.                                                                                                                                                                                                              |
| API\_HEADERS                   | Manages environment API headers.                                                                                                                                                                                               |
| IDENTITY\_PROVIDER             | Manages Identity Providers for authentication.                                                                                                                                                                                 |
| CLIENT\_REGISTRATION\_PROVIDER | Manages environment client registration configuration.                                                                                                                                                                         |
| THEME                          | Manages APIM Portal themes.                                                                                                                                                                                                    |

#### API permissions

| Name                | Description                                                                                                                                 |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| DEFINITION          | Manages the API definition.                                                                                                                 |
| PLAN                | Manages API plans.                                                                                                                          |
| SUBSCRIPTION        | Manages API subscriptions.                                                                                                                  |
| MEMBER              | Manages API members.                                                                                                                        |
| METADATA            | Manages API metadata.                                                                                                                       |
| ANALYTICS           | Manages API analytics. Only `READ` permission is used.                                                                                      |
| EVENT               | Manages API events. Only `READ` permission is used.                                                                                         |
| HEALTH              | Manages API health checks.                                                                                                                  |
| LOG                 | Manages API logs. Only `READ` permission is used.                                                                                           |
| DOCUMENTATION       | Manages API documentation.                                                                                                                  |
| GATEWAY\_DEFINITION | A specific permission used to update the context-path (`UPDATE`) and to give access to sensitive data (`READ`) such as endpoints and paths. |
| RATING              | Manages API rating.                                                                                                                         |
| RATING\_ANSWERS     | Manages API rating answers.                                                                                                                 |
| AUDIT               | Manages API audits. Only `READ` permission is used.                                                                                         |
| DISCOVERY           | Manages service discovery.                                                                                                                  |
| NOTIFICATION        | Manages API notifications.                                                                                                                  |
| MESSAGE             | Manages messaging.                                                                                                                          |
| ALERT               | Manages API alerting.                                                                                                                       |
| RESPONSE\_TEMPLATES | Manages API response templates.                                                                                                             |
| REVIEWS             | Manages API reviews.                                                                                                                        |
| QUALITY\_RULE       | Manages API quality rules.                                                                                                                  |

| Name         | Description                                                    |
| ------------ | -------------------------------------------------------------- |
| DEFINITION   | Manages the application definition.                            |
| MEMBER       | Manages application members.                                   |
| ANALYTICS    | Manages application analytics. Only `READ` permission is used. |
| LOG          | Manages application logs. Only `READ` permission is used.      |
| SUBSCRIPTION | Manages application subscriptions.                             |
| NOTIFICATION | Manages application notifications.                             |
| ALERT        | Manages application alerting.                                  |

{% hint style="warning" %}
**Enterprise only**

As of Gravitee 4.0, Custom Roles is an Enterprise Edition capability. To learn more about Gravitee Enterprise, and what's included in various enterprise packages, please:

* [Refer to the EE vs OSS documentation](../../overview/ee-vs-oss/README.md)
* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

To create a role in Gravitee, select **+ Add a role** at your desired Scope. You'll be brought the the **Create a role in the (chosen scope) scope** page. Here, you will:

* Give the role a name
* Give the role a description (optional)
* Enable the role as a default role for new users by toggling **Default tole** ON or OFF

After you define the above, you will set CRUD permissions. CRUD is an acronym that stands for the four actions than can be granted:

* **Create**
* **Read**
* **Update**
* **Delete**

{% hint style="info" %}
**CRUD permissions**

If a user has full **CRUD** permissions, that means that they can create, read, update, and delete for a specific permission.
{% endhint %}

Once you are done selecting your permissions, select **Create** at the bottom of the page to officially create your role.

#### Example: create a "Writer" role

To further illustrate this concept, we'll walk through a step by step process to create a "Writer" role that will be able to create API documentation.

To create a custom "Writer" role, follow these steps:

1. Log-in to the API Management Console
2. Select **Organizations** from the left-hand nav
3. Select **Roles** under **User Management**
4.  At the **API** scope, select **+ Add a role**\\

    <figure><img src="../../../../../.gitbook/assets/Add an API scope role (1).gif" alt=""><figcaption><p>Create an API scope role</p></figcaption></figure>
5. Enter in "**Writer**" in the **Role name** text field
6. Give the role a description, such as **"These users can create, update, read, and delete API documentation."**
7. (Optional) If you want this to be the default role for new users, toggle **Default role** ON or OFF.
8. Define the following permissions:\
   &#xNAN;**`Read`** permissions on **`DEFINITION`** and **`GATEWAY_DEFINITION`** : this allows the user to see the API in the API list\
   &#xNAN;**`CRUD`** permissions on **`DOCUMENTATION`**: this allows the user to write new API documentation
9.  Once you are done, select **Create.** \\

    <figure><img src="../../../../../.gitbook/assets/Writer role (1).gif" alt=""><figcaption><p>Define the "Writer" role permissions</p></figcaption></figure>

{% hint style="success" %}
**Success!**

Once you're done, you'll see the "**Writer**" role in the **API** Scope section.
{% endhint %}

### Users and user groups

In Gravitee, users are simply profiles for individuals that use the platform. User groups are groupings of users that share the same role(s) for the **API** and/or **Application** Scope(s).

#### Create and manage users

There are two main ways for users to be created:

* System Administrators can create users
* Users can self-register via a registration form

To create a user via the System administrator flow, follow these steps:

1. Log-in to the API Management Console, and select Organization from the left-hand nav.
2. Select **Users** under **User Management.**
3. Select **+ Add user** from the top left corner of the **Users** page.\\
4. From here, you will define the user profile for this user. To define the user profile:
   * Define the IdP for the user by using the IdP name that you configured as a part of your [IdP configuration](how-to.md#defining-organization-authentication-and-access-settings).
   * Define the user's info:
     * First name
     * Last name
     * Email
   * Select whether the user will be a normal **User** or a **Service Account**
     * Setting up a user as a service account will essentially enable somebody from a Gravitee servicer (perhaps a partner or consultant) to subscribe to email notifications coming from the Gravitee platform
5. Select **Create** at the bottom of the page.

To delete a user from your Organization, select the **Delete user** icon from the table on the **Users** page.

<figure><img src="../../../../../.gitbook/assets/Delete a user (1).png" alt=""><figcaption><p>Delete a user</p></figcaption></figure>

#### Create and manage User groups

To create and manage User groups, follow these steps:

1. Log-in to the API Management Console, and select **Settings** from the left-hand nav.
2. Under **User Management,** select **Groups**.
3. You'll be brought to a list of User groups. Here, you can create, edit, and delete User groups. To:
   * Create groups: select the + icon at the bottom right corner of the page
   * Edit groups: select the hyperlinked group name
   * Delete groups: select the Delete icon.
4. If you are creating or editing a User group, you will need to dedfine:
   * General info: this is just the name of the User group
   * Roles and members: define the maximum amount of members and choose whether or not to allow:
     * Invitations via user search
     * Email invitations
     * The group admin to change the API role
     * The group admin to change the application role
     * Notifications when members are added to this group
   * Associations: choose whether or not to associate this group to every new API and/or application
5. Under **Actions,** select **Create.**

Once a User group is created, you will be able to:

* Define a default API role by selecting the role from the **Default API Role** drop-down
* Define default application roles by selecting the role from the **Default Application Role** drop-down
* Choose to associate the User group with existing APIs or Applications by selecting **Associate to existing APIs** and/or **Associate to existing applications**
* View all members, associated APIs, and associated applications in the **Dependents** section

If you are making a change to your User group, you can either:

* Reset the User group settings by selecting **Reset** under **Actions**
* Update the User group to save new settings by selecting **Update** under **Actions**
