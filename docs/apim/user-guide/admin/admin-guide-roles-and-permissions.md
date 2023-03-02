# admin-guide-roles-and-permissions

## Overview

APIM allows you to create custom user roles to fit your needs. Some default roles are provided for you.

In APIM, a role:

* is associated with a group of permissions
* has a scope
* defines what you can do with the APIM UI components and APIM API

Before defining some key concepts, we recommend you first take a look at the new link:\{{ _/apim/3.x/apim\_adminguide\_organizations\_and\_environments.html_ | relative\_url \}}\[Gravitee.io Platform design^].

Any changes to a role may take a short time to be applied to a user.

### Scopes

Roles are defined in terms of _scopes_. As described in the link:\{{ _/apim/3.x/apim\_adminguide\_organizations\_and\_environments.html_ | relative\_url \}}\[Organizations and environments] page, an _environment_ corresponds roughly to what you can find in APIM Portal. More precisely, an environment’s scope is all of the actions that can be performed in the specific context, whether in APIM Portal or APIM Console.

For example:

* APIs can be managed by API publishers in APIM Console.
* Applications can be managed in both APIM Console and APIM Portal.
* API ratings can be managed by API consumers in APIM Portal.

As the name suggests, the scope of an _organization_ is all aspects of an organization: users, roles, and so on. Organization-level actions are only available in APIM Console.

A user can have more than one organization role and more than one environment role.

The scopes of _API_ and _application_ work slightly differently.

As an API publisher or consumer, you have access to APIs and/or applications. APIM allows you to have a different role for each API and application. You can be the owner for one, an ordinary user for another and the person in charge of writing the documentation for another. This means that the API and application roles are only meaningful in terms of their association with an API or application.

### Role

A role is a functional group of permissions. There is no limit to the number of roles you can create. They all need to be administered, however.

Some roles are special. The are tagged as `System` or `Default`.

#### System role

The Organization Admin role is a read-only role (i.e. you cannot change its permissions) used by APIM.

This role gives the user all permissions. If any accidental loss of access happened to another role, a user with this role will still be able to perform the action or restore required privileges.

Historically, the roles listed bellow were also created as read-only system roles and are still tagged as such, but they have been made editable for the sake of administration flexibility.

1. The Environment Admin role
2. The API Primary Owner role
3. The Application Primary Owner role

In order to edit this roles, you need to activate this mode in `gravitee.yml`

```
console:
  systemRoleEdition:
    enabled: true
```

Updating permissions for system roles should be done carefully to avoid any unexpected behavior.

#### Default role

The Default role is the role used by APIM when a role is not specified. For example, new registered users are assigned the default `ENVIRONMENT` and `ORGANIZATION`. The Default role gives the user limited permissions.

You can change the default on each scope.

### Permission

A permission is a list of actions allowed on a resource. The actions are `Create`, `Read`, `Update` and `Delete`.

The list of permissions by scope is as follows:

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

`ENVIRONMENT` scope permissions

| Name        | Description                                   |
| ----------- | --------------------------------------------- |
| USER        | Manages users.                                |
| ENVIRONMENT | Manages environments.                         |
| ROLE        | Manages roles.                                |
| TAG         | Manages sharding tags.                        |
| TENANT      | Manages tenants.                              |
| ENTRYPOINT  | Manages environment entrypoint configuration. |

`ORGANIZATION` scope permissions

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

`API` scope permissions

| Name         | Description                                                    |
| ------------ | -------------------------------------------------------------- |
| DEFINITION   | Manages the application definition.                            |
| MEMBER       | Manages application members.                                   |
| ANALYTICS    | Manages application analytics. Only `READ` permission is used. |
| LOG          | Manages application logs. Only `READ` permission is used.      |
| SUBSCRIPTION | Manages application subscriptions.                             |
| NOTIFICATION | Manages application notifications.                             |
| ALERT        | Manages application alerting.                                  |

`APPLICATION` scope permissions

## Create a custom role

In this example, we will create a writer role which allows a user to create API documentation.

### Create the `WRITER` role

1. link:\{{ _/apim/3.x/apim\_quickstart\_console\_login.html_ | relative\_url \}}\[Log in to APIM Console].
2.  In the **Organization Settings > Roles** page, click **ADD A NEW ROLE**.

    image::\{% link images/apim/3.x/adminguide/newrole-create.png %\}\[Gravitee.io - Create a New Role]

### Configure the `WRITER` role

Assign the following permissions to the writer role:

* `READ` permissions on `DEFINITION` and `GATEWAY_DEFINITION` — this allows the user to see the API in the API list
* `CRUD` permissions on `DOCUMENTATION`

image::\{% link images/apim/3.x/adminguide/newrole-configure.png %\}\[Gravitee.io - Configure a New Role]

### Result

Users with this role can now only see the documentation menu.

image::\{% link images/apim/3.x/adminguide/newrole-menu.png %\}\[Gravitee.io - Menu, 200]

Granting `GROUP` permissions to the `MANAGEMENT` role also requires the `READ` operation for the `ROLE` permission in order to see which roles are provided by a group.
