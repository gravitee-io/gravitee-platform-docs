---
description: Installation guide for Organizations and environment.
---

# Administration

## Organizations and environment

Two concepts apply to the setup of **Gravitee Access Management** (AM) installation. Organization and environment.

### Organization

A logical part of your company in the way that makes the most sense in your setup, for example, a region or business unit. In the context of an AM installation it is the level at which shared configurations for environments are managed, such as:

* User permissions to access the AM console
* Roles
* Identity providers to access the AM console

### Environment

An environment in an IT infrastructure, such as development or production. There can be multiple environments linked to one organization. In the context of an AM installation, it is the workspace in which users can manage their security domains and applications.

Examples of environments:

* technical environments such as DEV / TEST / PRODUCTION
* functional environments such as PRIVATE DOMAINS / PUBLIC DOMAINS / PARTNERSHIP

An environment belongs to one organization.

{% hint style="info" %}
By default, the Community Edition version of AM comes with a default organization and a default environment. For a multi-environment setup, you need an integration with Gravitee Cockpit.
{% endhint %}

## Roles and permissions overview

You can create administrator roles in AM to grant access to specific areas of a resource (Organization (Platform), Security Domain, Application). Depending on the role permissions, administrators can have full access to this resource. Administrator accounts represent users that can access the administration portal.

### Assignable type

When you log in AM, you are redirected to the portal with at least one `ORGANIZATION` role to be able to see some screens of the platform.

As an owner of a security domain or an application you want to manage your members by giving them roles that make sense only when associated with a `DOMAIN` / `APPLICATION`.

For example, you don’t want to allow a simple user or the person in charge of your application settings to be able to manage the whole platform.

In order to limit the scope of the roles, scopes are bound to what we call an `assignable type`:

* `ORGANIZATION` — role for the whole platform
* `ENVIRONMENT` — role for an environment
* `DOMAIN` — role for a security domain
* `APPLICATION` — role for an application

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-adminguide-roles-permissions.png" alt=""><figcaption><p>Roles</p></figcaption></figure>

### Role

A role is a functional group of permissions. There is no limit on the number of roles you are allowed to create.

Some roles are special: they are tagged as `System` or `Default`.

#### **System role**

A System role is a read-only role (i.e. you cannot change its permissions) used by AM. For example `ORGANIZATION_PRIMARY_OWNER` gives the user all permissions.

#### **Default role**

A Default role is a role used by AM when a role is not specified. For example, new registered users are assigned the default `ORGANIZATION_USER` role.

### Permission

A permission is a list of actions allowed on a resource. The actions are `Create`, `Read`, `List`, `Update` and `Delete`. Some permissions can be assigned to multiple types of resources. For instance, the `DOMAIN READ` permission has a different meaning depending on whether it is assigned:

* to a domain: the user can read the specified domain
* to an organization: the user can read all the domains of the specified organization

The following tables list the permissions by assignable type.

{% hint style="info" %}
All the permissions required to use AM API are described in the [AM V3 OpenAPI descriptor.](../reference/am-api-reference.md)
{% endhint %}

Table 1. ORGANIZATION permissions

| Name                             | Description                                                                                            |
| -------------------------------- | ------------------------------------------------------------------------------------------------------ |
| ORGANIZATION                     | Read organization / platform information                                                               |
| ORGANIZATION\_SETTINGS           | Manage organization / platform global settings                                                         |
| ORGANIZATION\_IDENTITY\_PROVIDER | Manage organization / platform global identity providers (AM Console authentication)                   |
| ORGANIZATION\_AUDIT              | Manage organization / platform audit logs                                                              |
| ORGANIZATION\_REPORTER           | Manage organization / platform reporters (for the audit logs storage)                                  |
| ORGANIZATION\_USER               | Manage organization / platform users (administrator accounts)                                          |
| ORGANIZATION\_GROUP              | Manage organization / platform groups (administrator groups)                                           |
| ORGANIZATION\_ROLE               | Manage organization / platform roles (roles and permissions used throughout AM Console)                |
| ORGANIZATION\_TAG                | Manage organization / platform sharding tags                                                           |
| ORGANIZATION\_ENTRYPOINT         | Manage organization / platform entry points (root URL for Authentication and Authorization operations) |
| ORGANIZATION\_FORM               | Manage organization / platform HTML templates (AM Console login form)                                  |
| ORGANIZATION\_MEMBER             | Manage organization / platform HTML memberships                                                        |
| ENVIRONMENT                      | Manage organization / platform environments (for example, dev, qual, prod)                             |
| DOMAIN                           | Read all security domain information                                                                   |
| DOMAIN\_SETTINGS                 | Manage all security domain global settings                                                             |
| DOMAIN\_FORM                     | Manage all security domain custom HTML templates                                                       |
| DOMAIN\_EMAIL\_TEMPLATE          | Manage all security domain custom email templates                                                      |
| DOMAIN\_EXTENSION\_POINT         | Manage all security domain custom extension points                                                     |
| DOMAIN\_IDENTITY\_PROVIDER       | Manage all security domain identity providers                                                          |
| DOMAIN\_AUDIT                    | Manage all security domain audit logs                                                                  |
| DOMAIN\_CERTIFICATE              | Manage all security domain certificates                                                                |
| DOMAIN\_USER                     | Manage all security domain users                                                                       |
| DOMAIN\_GROUP                    | Manage all security domain groups                                                                      |
| DOMAIN\_ROLE                     | Manage all security domain roles                                                                       |
| DOMAIN\_SCIM                     | Manage all security domain audit SCIM settings                                                         |
| DOMAIN\_SCOPE                    | Manage all security domain scopes (role permissions)                                                   |
| DOMAIN\_EXTENSION\_GRANT         | Manage all security domain OAuth 2.0 extension grants                                                  |
| DOMAIN\_UMA                      | Manage all security domain User Managed Access settings                                                |
| DOMAIN\_OPENID                   | Manage all security domain OAuth 2.0 / OpenID Connect settings (DCR)                                   |
| DOMAIN\_REPORTER                 | Manage all security domain reporters (audit logs storage)                                              |
| DOMAIN\_MEMBER                   | Manage all security domain memberships                                                                 |
| DOMAIN\_ANALYTICS                | Manage all security domain analytics                                                                   |
| DOMAIN\_FACTOR                   | Manage all security domain MFA settings                                                                |
| DOMAIN\_FLOW                     | Manage all security domain Flow settings                                                               |
| APPLICATION                      | Read all application information                                                                       |
| APPLICATION\_SETTINGS            | Manage all application global settings                                                                 |
| APPLICATION\_IDENTITY\_PROVIDER  | Manage all application identity providers                                                              |
| APPLICATION\_FORM                | Manage all application custom HTML templates                                                           |
| APPLICATION\_EMAIL\_TEMPLATE     | Manage all application custom email templates                                                          |
| APPLICATION\_OPENID              | Manage all application custom OAuth 2.0 / OpenID Connect settings                                      |
| APPLICATION\_CERTIFICATE         | Manage all application certificates                                                                    |
| APPLICATION\_MEMBER              | Manage all application memberships.                                                                    |
| APPLICATION\_FACTOR              | Manage all application MFA settings                                                                    |
| APPLICATION\_ANALYTICS           | Manage all application analytics                                                                       |
| APPLICATION\_FLOW                | Manage all application Flow settings                                                                   |

Table 2. ENVIRONMENT permissions

| Name                            | Description                                                                |
| ------------------------------- | -------------------------------------------------------------------------- |
| ENVIRONMENT                     | Manage organization / platform environments (for example, dev, qual, prod) |
| DOMAIN                          | Read all security domain information                                       |
| DOMAIN\_SETTINGS                | Manage all security domain global settings                                 |
| DOMAIN\_FORM                    | Manage all security domain custom HTML templates                           |
| DOMAIN\_EMAIL\_TEMPLATE         | Manage all security domain custom email templates                          |
| DOMAIN\_EXTENSION\_POINT        | Manage all security domain custom extension points                         |
| DOMAIN\_IDENTITY\_PROVIDER      | Manage all security domain identity providers                              |
| DOMAIN\_AUDIT                   | Manage all security domain audit logs                                      |
| DOMAIN\_CERTIFICATE             | Manage all security domain certificates                                    |
| DOMAIN\_USER                    | Manage all security domain users                                           |
| DOMAIN\_GROUP                   | Manage all security domain groups                                          |
| DOMAIN\_ROLE                    | Manage all security domain roles                                           |
| DOMAIN\_SCIM                    | Manage all security domain audit SCIM settings                             |
| DOMAIN\_SCOPE                   | Manage all security domain scopes (role permissions)                       |
| DOMAIN\_EXTENSION\_GRANT        | Manage all security domain OAuth 2.0 extension grants                      |
| DOMAIN\_UMA                     | Manage all security domain User Managed Access settings                    |
| DOMAIN\_OPENID                  | Manage all security domain OAuth 2.0 / OpenID Connect settings (DCR)       |
| DOMAIN\_REPORTER                | Manage all security domain reporters (audit logs storage)                  |
| DOMAIN\_MEMBER                  | Manage all security domain memberships                                     |
| DOMAIN\_ANALYTICS               | Manage all security domain analytics                                       |
| DOMAIN\_FACTOR                  | Manage all security domain MFA settings                                    |
| DOMAIN\_FLOW                    | Manage all security domain Flow settings                                   |
| APPLICATION                     | Read all application information                                           |
| APPLICATION\_SETTINGS           | Manage all application global settings                                     |
| APPLICATION\_IDENTITY\_PROVIDER | Manage all application identity providers                                  |
| APPLICATION\_FORM               | Manage all application custom HTML templates                               |
| APPLICATION\_EMAIL\_TEMPLATE    | Manage all application custom email templates                              |
| APPLICATION\_OPENID             | Manage all application custom OAuth 2.0 / OpenID Connect settings          |
| APPLICATION\_CERTIFICATE        | Manage all application certificates                                        |
| APPLICATION\_MEMBER             | Manage all application memberships.                                        |
| APPLICATION\_FACTOR             | Manage all application MFA settings                                        |
| APPLICATION\_ANALYTICS          | Manage all application analytics                                           |
| APPLICATION\_FLOW               | Manage all application Flow settings                                       |

Table 3. DOMAIN permissions

| Name                            | Description                                                                       |
| ------------------------------- | --------------------------------------------------------------------------------- |
| DOMAIN                          | Read the security domain information                                              |
| DOMAIN\_SETTINGS                | Manage the security domain global settings                                        |
| DOMAIN\_FORM                    | Manage the security domain custom HTML templates                                  |
| DOMAIN\_EMAIL\_TEMPLATE         | Manage the security domain custom email templates                                 |
| DOMAIN\_EXTENSION\_POINT        | Manage the security domain custom extension points                                |
| DOMAIN\_IDENTITY\_PROVIDER      | Manage the security domain identity providers                                     |
| DOMAIN\_AUDIT                   | Manage the security domain audit logs                                             |
| DOMAIN\_CERTIFICATE             | Manage the security domain certificates                                           |
| DOMAIN\_USER                    | Manage the security domain users                                                  |
| DOMAIN\_GROUP                   | Manage the security domain groups                                                 |
| DOMAIN\_ROLE                    | Manage the security domain roles                                                  |
| DOMAIN\_SCIM                    | Manage the security domain audit SCIM settings                                    |
| DOMAIN\_SCOPE                   | Manage the security domain scopes (role permissions)                              |
| DOMAIN\_EXTENSION\_GRANT        | Manage the security domain OAuth 2.0 extension grants                             |
| DOMAIN\_OPENID                  | Manage the security domain OAuth 2.0 / OpenID Connect settings (DCR)              |
| DOMAIN\_UMA                     | Manage the security domain User Managed Access settings                           |
| DOMAIN\_REPORTER                | Manage the security domain reporters (audit logs storage)                         |
| DOMAIN\_MEMBER                  | Manage the security domain memberships                                            |
| DOMAIN\_ANALYTICS               | Manage the security domain analytics                                              |
| DOMAIN\_FACTOR                  | Manage the security domain MFA settings                                           |
| DOMAIN\_FLOW                    | Manage the security domain Flow settings                                          |
| APPLICATION                     | Read the security domain application information                                  |
| APPLICATION\_SETTINGS           | Manage the security domain application global settings                            |
| APPLICATION\_IDENTITY\_PROVIDER | Manage the security domain application identity providers                         |
| APPLICATION\_FORM               | Manage the security domain application custom HTML templates                      |
| APPLICATION\_EMAIL\_TEMPLATE    | Manage the security domain application custom email templates                     |
| APPLICATION\_OPENID             | Manage the security domain application custom OAuth 2.0 / OpenID Connect settings |
| APPLICATION\_CERTIFICATE        | Manage the security domain application certificates                               |
| APPLICATION\_MEMBER             | Manage the security domain application memberships                                |
| APPLICATION\_FACTOR             | Manage the security domain application MFA settings                               |
| APPLICATION\_ANALYTICS          | Manage the security domain application analytics settings                         |
| APPLICATION\_FLOW               | Manage the security domain application flow settings                              |

Table 4. Permissions `APPLICATION`

| Name                            | Description                                                                       |
| ------------------------------- | --------------------------------------------------------------------------------- |
| APPLICATION                     | Read the security domain application information                                  |
| APPLICATION\_SETTINGS           | Manage the security domain application global settings                            |
| APPLICATION\_IDENTITY\_PROVIDER | Manage the security domain application identity providers                         |
| APPLICATION\_FORM               | Manage the security domain application custom HTML templates                      |
| APPLICATION\_EMAIL\_TEMPLATE    | Manage the security domain application custom email templates                     |
| APPLICATION\_OPENID             | Manage the security domain application custom OAuth 2.0 / OpenID Connect settings |
| APPLICATION\_CERTIFICATE        | Manage the security domain application certificates                               |
| APPLICATION\_MEMBER             | Manage the security domain application memberships                                |
| APPLICATION\_FACTOR             | Manage the security domain application MFA settings                               |
| APPLICATION\_ANALYTICS          | Manage the security domain application analytics settings                         |
| APPLICATION\_FLOW               | Manage the security domain application flow settings                              |

## Manage roles

To manage roles and permissions:

1. Log in to AM Console.
2. From the user menu at the top right, select **Global settings**.
3. Click **Settings > Roles**, then create a role as described in the examples below.

### Create the `REVIEWER_APPLICATION` role

Let’s imagine we want to create a reviewer role, which allows a user to check if your application configuration is valid.

1. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png) and enter the following values:
   * Assignable type : `APPLICATION`
   * Name : `REVIEWER_APPLICATION`
   *   Description : `Read-only role`

       <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-adminguide-new-role.png" alt=""><figcaption><p>Creating a new role</p></figcaption></figure>
2. Click **CREATE**.

### Configure the `REVIEWER_APPLICATION` role

You must give `READ` permissions to all sections of your application. This allows the user to see the whole configuration of your application.

Click **SAVE** to store the changes.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-adminguide-role-configure.png" alt=""><figcaption><p>Configure a role</p></figcaption></figure>

### Result

Go to your application **Administrative roles** settings section and add a new member with the `REVIEWER_APPLICATION` role. The user `Reviewer User` now has read access to your application.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-adminguide-role-member.png" alt=""><figcaption><p>Reviewer application role</p></figcaption></figure>

## Users

When users log in to AM Console, they are listed in the **Users** section of the **Global settings** menu.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-adminguide-users.png" alt=""><figcaption><p>User overview</p></figcaption></figure>

If you select a user, you have access to detailed account information and will be able to manage the user’s permissions and groups via with the **Administrative roles** and **Groups** sections.

## Groups

Groups represent user groups where you place members of the same team/partner and set their roles for an APPLICATION (see [Roles and permissions](administration.md#roles-and-permissions-overview) for details). You can associate a group with an application to give members of the group have access to the application.

In the example below, we will create a `FOO Team` group where you can put all members of your FOO team.

### Create the `FOO Team` group

1. Log in to AM Console.
2. From the user menu at the top right, select **Global settings**.
3. Click **Settings > Groups**.
4. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
5.  Enter the details of the group.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-adminguide-new-group.png" alt=""><figcaption><p>Group details</p></figcaption></figure>
6. Click **CREATE**.

### Configure group members

1. Click the settings icon ![settings icon](https://docs.gravitee.io/images/icons/settings-icon.png) next to the `FOO Team` group.
2. Click the **Members** tab.
3.  Add a user by clicking **+ Add members**.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-adminguide-new-group-members.png" alt=""><figcaption><p>Add members to group</p></figcaption></figure>

### Add the group to an application

Go to the Application you want to modify and click **Administrative roles**.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-adminguide-application-group-members.png" alt=""><figcaption><p>Application admins</p></figcaption></figure>

Now the members of the group section will have access to the Application with the group role permissions.

{% hint style="info" %}
Direct user member permissions and group permissions are merged they apply to the same user.
{% endhint %}
