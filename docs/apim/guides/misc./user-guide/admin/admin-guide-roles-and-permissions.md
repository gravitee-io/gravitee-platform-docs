# Overview

APIM allows you to create custom user roles to fit your needs. Some
default roles are provided for you.

In APIM, a role:

-   is associated with a group of permissions

-   has a scope

-   defines what you can do with the APIM UI components and APIM API

Before defining some key concepts, we recommend you first take a look at
the new link:{{
*/apim/3.x/apim\_adminguide\_organizations\_and\_environments.html* |
relative\_url }}\[Gravitee.io Platform design^\].

Any changes to a role may take a short time to be applied to a user.

## Scopes

Roles are defined in terms of *scopes*. As described in the link:{{
*/apim/3.x/apim\_adminguide\_organizations\_and\_environments.html* |
relative\_url }}\[Organizations and environments\] page, an
*environment* corresponds roughly to what you can find in APIM Portal.
More precisely, an environment’s scope is all of the actions that can be
performed in the specific context, whether in APIM Portal or APIM
Console.

For example:

-   APIs can be managed by API publishers in APIM Console.

-   Applications can be managed in both APIM Console and APIM Portal.

-   API ratings can be managed by API consumers in APIM Portal.

As the name suggests, the scope of an *organization* is all aspects of
an organization: users, roles, and so on. Organization-level actions are
only available in APIM Console.

A user can have more than one organization role and more than one
environment role.

The scopes of *API* and *application* work slightly differently.

As an API publisher or consumer, you have access to APIs and/or
applications. APIM allows you to have a different role for each API and
application. You can be the owner for one, an ordinary user for another
and the person in charge of writing the documentation for another. This
means that the API and application roles are only meaningful in terms of
their association with an API or application.

## Role

A role is a functional group of permissions. There is no limit to the
number of roles you can create. They all need to be administered,
however.

Some roles are special. The are tagged as `System` or `Default`.

### System role

The Organization Admin role is a read-only role (i.e. you cannot change
its permissions) used by APIM.

This role gives the user all permissions. If any accidental loss of
access happened to another role, a user with this role will still be
able to perform the action or restore required privileges.

Historically, the roles listed bellow were also created as read-only
system roles and are still tagged as such, but they have been made
editable for the sake of administration flexibility.

1.  The Environment Admin role

2.  The API Primary Owner role

3.  The Application Primary Owner role

In order to edit this roles, you need to activate this mode in
`gravitee.yml`

    console:
      systemRoleEdition:
        enabled: true

Updating permissions for system roles should be done carefully to avoid
any unexpected behavior.

### Default role

The Default role is the role used by APIM when a role is not specified.
For example, new registered users are assigned the default `ENVIRONMENT`
and `ORGANIZATION`. The Default role gives the user limited permissions.

You can change the default on each scope.

## Permission

A permission is a list of actions allowed on a resource. The actions are
`Create`, `Read`, `Update` and `Delete`.

The list of permissions by scope is as follows:

<table>
<caption><code>ENVIRONMENT</code> scope permissions</caption>
<colgroup>
<col style="width: 25%" />
<col style="width: 75%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Name</p></td>
<td style="text-align: left;"><p>Description</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>INSTANCE</p></td>
<td style="text-align: left;"><p>Access to API Gateway instance
information. Only <code>READ</code> permission is used.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GROUP</p></td>
<td style="text-align: left;"><p>Manages user groups.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>TAG</p></td>
<td style="text-align: left;"><p>Manages sharding tags.
<strong>Deprecated, will be removed on 3.10.0</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>TENANT</p></td>
<td style="text-align: left;"><p>Manages tenants. <strong>Deprecated,
will be removed on 3.10.0</strong></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>API</p></td>
<td style="text-align: left;"><p>Manages APIs in general. This means
that the <code>CREATE</code> action is used to establish if the user is
allowed to create an API or not, and the <code>READ</code> permission to
allow the user to request the policies list and resources list.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>APPLICATION</p></td>
<td style="text-align: left;"><p>Manages applications in general.
<code>CREATE</code> allows the user to create an application,
<code>READ</code> allows the user to list applications.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>PLATFORM</p></td>
<td style="text-align: left;"><p>Gets APIM monitoring metrics. Only
<code>READ</code> permission is used.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>AUDIT</p></td>
<td style="text-align: left;"><p>Gets APIM audit. Only <code>READ</code>
permission is used.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>NOTIFICATION</p></td>
<td style="text-align: left;"><p>Manages global notifications.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>MESSAGE</p></td>
<td style="text-align: left;"><p>Manages messaging.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>DICTIONARY</p></td>
<td style="text-align: left;"><p>Manages environment
dictionaries.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>ALERT</p></td>
<td style="text-align: left;"><p>Manages environment alerting.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>ENTRYPOINT</p></td>
<td style="text-align: left;"><p>Manages environment entrypoint
configuration. <strong>Deprecated, will be removed on
3.10.0</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>SETTINGS</p></td>
<td style="text-align: left;"><p>Manages environment settings.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>DASHBOARD</p></td>
<td style="text-align: left;"><p>Manages environment
dashboards.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>QUALITY_RULE</p></td>
<td style="text-align: left;"><p>Manages environment quality
rules.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>METADATA</p></td>
<td style="text-align: left;"><p>Manages APIM metadata.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>DOCUMENTATION</p></td>
<td style="text-align: left;"><p>ManageS APIM Portal
documentation.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>CATEGORY</p></td>
<td style="text-align: left;"><p>Manages categories.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>TOP_APIS</p></td>
<td style="text-align: left;"><p>Manages top apis.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>API_HEADERS</p></td>
<td style="text-align: left;"><p>Manages environment API
headers.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>IDENTITY_PROVIDER</p></td>
<td style="text-align: left;"><p>Manages Identity Providers for
authentication.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>CLIENT_REGISTRATION_PROVIDER</p></td>
<td style="text-align: left;"><p>Manages environment client registration
configuration.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>THEME</p></td>
<td style="text-align: left;"><p>Manages APIM Portal themes.</p></td>
</tr>
</tbody>
</table>

`ENVIRONMENT` scope permissions

<table>
<caption><code>ORGANIZATION</code> scope permissions</caption>
<colgroup>
<col style="width: 25%" />
<col style="width: 75%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Name</p></td>
<td style="text-align: left;"><p>Description</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>USER</p></td>
<td style="text-align: left;"><p>Manages users.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
<td style="text-align: left;"><p>Manages environments.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>ROLE</p></td>
<td style="text-align: left;"><p>Manages roles.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>TAG</p></td>
<td style="text-align: left;"><p>Manages sharding tags.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>TENANT</p></td>
<td style="text-align: left;"><p>Manages tenants.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>ENTRYPOINT</p></td>
<td style="text-align: left;"><p>Manages environment entrypoint
configuration.</p></td>
</tr>
</tbody>
</table>

`ORGANIZATION` scope permissions

<table>
<caption><code>API</code> scope permissions</caption>
<colgroup>
<col style="width: 25%" />
<col style="width: 75%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Name</p></td>
<td style="text-align: left;"><p>Description</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>DEFINITION</p></td>
<td style="text-align: left;"><p>Manages the API definition.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>PLAN</p></td>
<td style="text-align: left;"><p>Manages API plans.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>SUBSCRIPTION</p></td>
<td style="text-align: left;"><p>Manages API subscriptions.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>MEMBER</p></td>
<td style="text-align: left;"><p>Manages API members.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>METADATA</p></td>
<td style="text-align: left;"><p>Manages API metadata.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>ANALYTICS</p></td>
<td style="text-align: left;"><p>Manages API analytics. Only
<code>READ</code> permission is used.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>EVENT</p></td>
<td style="text-align: left;"><p>Manages API events. Only
<code>READ</code> permission is used.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>HEALTH</p></td>
<td style="text-align: left;"><p>Manages API health checks.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>LOG</p></td>
<td style="text-align: left;"><p>Manages API logs. Only
<code>READ</code> permission is used.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>DOCUMENTATION</p></td>
<td style="text-align: left;"><p>Manages API documentation.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GATEWAY_DEFINITION</p></td>
<td style="text-align: left;"><p>A specific permission used to update
the context-path (<code>UPDATE</code>) and to give access to sensitive
data (<code>READ</code>) such as endpoints and paths.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>RATING</p></td>
<td style="text-align: left;"><p>Manages API rating.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>RATING_ANSWERS</p></td>
<td style="text-align: left;"><p>Manages API rating answers.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>AUDIT</p></td>
<td style="text-align: left;"><p>Manages API audits. Only
<code>READ</code> permission is used.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>DISCOVERY</p></td>
<td style="text-align: left;"><p>Manages service discovery.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>NOTIFICATION</p></td>
<td style="text-align: left;"><p>Manages API notifications.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>MESSAGE</p></td>
<td style="text-align: left;"><p>Manages messaging.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>ALERT</p></td>
<td style="text-align: left;"><p>Manages API alerting.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>RESPONSE_TEMPLATES</p></td>
<td style="text-align: left;"><p>Manages API response
templates.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>REVIEWS</p></td>
<td style="text-align: left;"><p>Manages API reviews.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>QUALITY_RULE</p></td>
<td style="text-align: left;"><p>Manages API quality rules.</p></td>
</tr>
</tbody>
</table>

`API` scope permissions

<table>
<caption><code>APPLICATION</code> scope permissions</caption>
<colgroup>
<col style="width: 25%" />
<col style="width: 75%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Name</p></td>
<td style="text-align: left;"><p>Description</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>DEFINITION</p></td>
<td style="text-align: left;"><p>Manages the application
definition.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>MEMBER</p></td>
<td style="text-align: left;"><p>Manages application members.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>ANALYTICS</p></td>
<td style="text-align: left;"><p>Manages application analytics. Only
<code>READ</code> permission is used.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>LOG</p></td>
<td style="text-align: left;"><p>Manages application logs. Only
<code>READ</code> permission is used.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>SUBSCRIPTION</p></td>
<td style="text-align: left;"><p>Manages application
subscriptions.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>NOTIFICATION</p></td>
<td style="text-align: left;"><p>Manages application
notifications.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>ALERT</p></td>
<td style="text-align: left;"><p>Manages application alerting.</p></td>
</tr>
</tbody>
</table>

`APPLICATION` scope permissions

# Create a custom role

In this example, we will create a writer role which allows a user to
create API documentation.

## Create the `WRITER` role

1.  link:{{ */apim/3.x/apim\_quickstart\_console\_login.html* |
    relative\_url }}\[Log in to APIM Console\].

2.  In the **Organization Settings &gt; Roles** page, click **ADD A NEW
    ROLE**.

    image::{% link images/apim/3.x/adminguide/newrole-create.png
    %}\[Gravitee.io - Create a New Role\]

## Configure the `WRITER` role

Assign the following permissions to the writer role:

-   `READ` permissions on `DEFINITION` and `GATEWAY_DEFINITION` — this
    allows the user to see the API in the API list

-   `CRUD` permissions on `DOCUMENTATION`

image::{% link images/apim/3.x/adminguide/newrole-configure.png
%}\[Gravitee.io - Configure a New Role\]

## Result

Users with this role can now only see the documentation menu.

image::{% link images/apim/3.x/adminguide/newrole-menu.png
%}\[Gravitee.io - Menu, 200\]

Granting `GROUP` permissions to the `MANAGEMENT` role also requires the
`READ` operation for the `ROLE` permission in order to see which roles
are provided by a group.
