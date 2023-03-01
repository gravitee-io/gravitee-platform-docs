# Important

If you are using mongoDB, it is **strongly recommended** to run the
scripts to upgrade your database **before** starting the new version of
the gravitee REST APIs. Otherwise, you could experience data corruption
issues.

Mongo version **MUST** be at least **3.6**

# General

## Organization & Environment

In this new version Gravitee comes with a new way of managing your
environments. By default, Gravitee is configured with a first
Organization: \`\`\` organization { id: DEFAULT, name: Default
organization } \`\`\` And a first Environment in this Organization:
\`\`\` environment { id: DEFAULT, name: Default environment,
organization: DEFAULT } \`\`\`

It will allow you to manage more than one environment for each instance
of Gravitee.

# Breaking Changes

## API-Key policy

In this new version, if api-keys used to call an API is invalid or has
expired, the gateway will fail with a **401** (instead of 403 in
previous versions of Gravitee).

## Management API

If you are using the REST API directly, please note that you will have
to adapt the URL from `https://host/management/` to
`https://host/management/organizations/DEFAULT/environments/DEFAULT/`

The resource `/views/default` has been deleted since a view does not
have a **default** field anymore.

## Management UI

The actual portal has been replaced by a brand new version, with its own
location. As a consequence, the URL of the management UI has been
modified to remove the **/management** part.

For instance, to access the *Platform Overview* page, you should use
`https://host/\#!/platform` instead of
`https://host/#!/management/platform`

## Memberships, roles and role mappings

One major breaking change in this new version is the replacement of
**MANAGEMENT** and **PORTAL** scopes by **ENVIRONNMENT** and
**ORGANIZATION** scopes. It’s not just a renaming but a dispatch of
permissions among these 2 news scopes. As a consequence, all existing
memberships, roles, groups and Identity Providers role mappings should
be updated.

-   Memberhips, roles and groups have to be updated with migration
    scripts [here](#mongodb)

-   Role Mappings for Identity Providers stored in database will be
    updated with a specific upgrader. See [Upgrader](#upgrader)

-   Role mappings defined in the **gravitee.yml** file have to be
    updated with these new scopes.

Here’s a correlation table of permissions before and after migration :

<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;">Permission Name</th>
<th style="text-align: left;">Scope Name before migration</th>
<th style="text-align: left;">Scope name after migration</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>INSTANCE</p></td>
<td style="text-align: left;"><p>MANAGEMENT</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GROUP</p></td>
<td style="text-align: left;"><p>MANAGEMENT</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>TAG</p></td>
<td style="text-align: left;"><p>MANAGEMENT</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>TENANT</p></td>
<td style="text-align: left;"><p>MANAGEMENT</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>API</p></td>
<td style="text-align: left;"><p>MANAGEMENT</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>ROLE</p></td>
<td style="text-align: left;"><p>MANAGEMENT</p></td>
<td style="text-align: left;"><p>ORGANIZATION</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>APPLICATION</p></td>
<td style="text-align: left;"><p>MANAGEMENT</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>PLATFORM</p></td>
<td style="text-align: left;"><p>MANAGEMENT</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>AUDIT</p></td>
<td style="text-align: left;"><p>MANAGEMENT</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>NOTIFICATION</p></td>
<td style="text-align: left;"><p>MANAGEMENT</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>USER</p></td>
<td style="text-align: left;"><p>MANAGEMENT</p></td>
<td style="text-align: left;"><p>ORGANIZATION</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>MESSAGE</p></td>
<td style="text-align: left;"><p>MANAGEMENT</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>DICTIONARY</p></td>
<td style="text-align: left;"><p>MANAGEMENT</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>ALERT</p></td>
<td style="text-align: left;"><p>MANAGEMENT</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>ENTRYPOINT</p></td>
<td style="text-align: left;"><p>MANAGEMENT</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>SETTINGS</p></td>
<td style="text-align: left;"><p>MANAGEMENT</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>DASHBOARD</p></td>
<td style="text-align: left;"><p>MANAGEMENT</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>QUALITY_RULE</p></td>
<td style="text-align: left;"><p>MANAGEMENT</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>METADATA</p></td>
<td style="text-align: left;"><p>PORTAL</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>DOCUMENTATION</p></td>
<td style="text-align: left;"><p>PORTAL</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>APPLICATION</p></td>
<td style="text-align: left;"><p>PORTAL</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>VIEW</p></td>
<td style="text-align: left;"><p>PORTAL</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>TOP_APIS</p></td>
<td style="text-align: left;"><p>PORTAL</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>SETTINGS</p></td>
<td style="text-align: left;"><p>PORTAL</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>API_HEADER</p></td>
<td style="text-align: left;"><p>PORTAL</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>IDENTITY_PROVIDER</p></td>
<td style="text-align: left;"><p>PORTAL</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>CLIENT_REGISTRATION_PROVIDER</p></td>
<td style="text-align: left;"><p>PORTAL</p></td>
<td style="text-align: left;"><p>ENVIRONMENT</p></td>
</tr>
</tbody>
</table>

# Repository

## Mongodb

Before running any script, please create a dump of your existing
database.

[/apim/3.x/mongodb/3.0.0/1-collections-linked-to-environment-or-organization.js](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/3.0.0/1-collections-linked-to-environment-or-organization.js)  
This script adds new fields that refer the default environment or the
default organization.

[/apim/3.x/mongodb/3.0.0/2-roles-groups-and-memberships-migration.js](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/3.0.0/2-roles-groups-and-memberships-migration.js)  
This script migrates permission values in roles since MANAGEMENT roles
and PORTAL roles have been merged and dispatched into new ENVIRONMENT
and ORGANIZATION roles. It also updates memberships and groups by adding
or removing columns. All previous indexes for **roles** and
**memberships** will be deleted and replaced by new indexes.

[/apim/3.x/mongodb/3.0.0/3-replace-apiArray-by-unique-api.js](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/3.0.0/3-replace-apiArray-by-unique-api.js)  
This script adds a new field that refers the api and remove the api
array. All previous indexes for **plans** will be deleted and replaced
by new indexes.

[/apim/3.x/mongodb/3.0.0/4-remove-devMode.js](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/3.0.0/4-remove-devMode.js)  
This script removes the *devMode* parameter, since the legacy portal has
been replaced.

[/apim/3.x/mongodb/3.0.0/5-remove-orphan-documentation-pages.js](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/3.0.0/5-remove-orphan-documentation-pages.js)  
Due to a bug in a previous version of gravitee when importing APIs,
orphan pages may have been created. Orphan pages are all pages with a
parentId but no page with such id exists. In some situation, this can
lead to errors when accessing portal or apis documentation. You may use
this script to find and remove orphan pages.

*Note: You can make a *dry run* by commenting line 6 and uncommenting
line 5.*

[/apim/3.x/mongodb/3.0.0/6-remove-ALL-view-and-defaultView-field.js](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/3.0.0/6-remove-ALL-view-and-defaultView-field.js)  
This script removes the *All* **view**, since the legacy portal has been
replaced and the new portal does not need this default view anymore. The
script also updates existing views to remove **defaultView** field.

# Upgrader

## Identity providers

Because of the evolution of the roles and their scope, role mappings in
**Identity Providers** must be updated. To achieve this, a specific
service has been created and will be launched at APIM startup. As this
is not necessary to launch this service more than once, it can be
disabled with some configuration.

    services:
      # v3 upgrader service. Can be disabled after first launch.
      v3-upgrader:
        enabled: true

# Docker

Docker images for Gravitee.io APIM have been renamed to follow the same
conventions as the others Gravitee.io modules.

In the case of Gravitee.io APIM, all the images have been prefixed by
`-apim`.

For example, for the API gateway `graviteeio/gateway` has been replaced
by `graviteeio/apim-gateway`.

Please have a look to the documentation at:
<https://docs.gravitee.io/apim/3.x/apim_installguide_docker_images.html>
