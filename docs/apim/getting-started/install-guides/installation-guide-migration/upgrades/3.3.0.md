# Repository

## Mongodb

Before running any script, please create a dump of your existing
database.

[/apim/3.x/mongodb/3.3.0/1-update-users-and-identityProviders.js](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/3.3.0/1-update-users-and-identityProviders.js)  
This script replaces **referenceId** and **referenceType** with
**organizationId** for `users` and `identity_providers` collections.

[/apim/3.x/mongodb/3.3.0/2-update-json-validation-policy-scopes.js](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/3.3.0/2-update-json-validation-policy-scopes.js)  
This script replaces **REQUEST** and **RESPONSE** with
**REQUEST\_CONTENT** and **RESPONSE\_CONTENT** for json-validation
policy configuration in `apis` collections.

# Deprecation

## Management API

Starting with this version, `User` and `IdentityProvider` are now linked
to an organization and not to an environment. As a consequence, the
Management REST API has been updated. If you are using the REST API
directly, please note that you should adapt your URL for these resources
as they will no longer be accessible from version 4.x In the meantime,
these resources will be tagged as `Deprecated`.

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;">Deprecated in 3.3.0, deleted in 4.x</th>
<th style="text-align: left;">Since 3.3.0</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p>/organizations/DEFAULT/environments/DEFAULT/configuration/identities</p></td>
<td
style="text-align: left;"><p>/organizations/DEFAULT/configuration/identities</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p>/organizations/DEFAULT/environments/DEFAULT/configuration/rolescopes</p></td>
<td
style="text-align: left;"><p>/organizations/DEFAULT/configuration/rolescopes</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr class="even">
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr class="odd">
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr class="even">
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p>/organizations/DEFAULT/environments/DEFAULT/search/users</p></td>
<td
style="text-align: left;"><p>/organizations/DEFAULT/search/users</p></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p>/organizations/DEFAULT/environments/DEFAULT/user</p></td>
<td style="text-align: left;"><p>/organizations/DEFAULT/user</p></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p>/organizations/DEFAULT/environments/DEFAULT/user/subscribeNewsletter</p></td>
<td
style="text-align: left;"><p>/organizations/DEFAULT/user/subscribeNewsletter</p></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p>/organizations/DEFAULT/environments/DEFAULT/user/avatar</p></td>
<td
style="text-align: left;"><p>/organizations/DEFAULT/user/avatar</p></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p>/organizations/DEFAULT/environments/DEFAULT/user/login</p></td>
<td
style="text-align: left;"><p>/organizations/DEFAULT/user/login</p></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p>/organizations/DEFAULT/environments/DEFAULT/user/logout</p></td>
<td
style="text-align: left;"><p>/organizations/DEFAULT/user/logout</p></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p>/organizations/DEFAULT/environments/DEFAULT/user/tasks</p></td>
<td
style="text-align: left;"><p>/organizations/DEFAULT/user/tasks</p></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p>/organizations/DEFAULT/environments/DEFAULT/user/tags</p></td>
<td
style="text-align: left;"><p>/organizations/DEFAULT/user/tags</p></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p>/organizations/DEFAULT/environments/DEFAULT/user/notifications</p></td>
<td
style="text-align: left;"><p>/organizations/DEFAULT/user/notifications</p></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p>/organizations/DEFAULT/environments/DEFAULT/user/tokens</p></td>
<td
style="text-align: left;"><p>/organizations/DEFAULT/user/tokens</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p>/organizations/DEFAULT/environments/DEFAULT/users</p></td>
<td style="text-align: left;"><p>/organizations/DEFAULT/users</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr class="even">
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr class="odd">
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr class="even">
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr class="odd">
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr class="even">
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr class="odd">
<td style="text-align: left;"></td>
<td style="text-align: left;"></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p>/organizations/DEFAULT/environments/DEFAULT/users/registration</p></td>
<td
style="text-align: left;"><p>/organizations/DEFAULT/users/registration</p></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p>/organizations/DEFAULT/environments/DEFAULT/users/registration/finalize</p></td>
<td
style="text-align: left;"><p>/organizations/DEFAULT/users/registration/finalize</p></td>
</tr>
</tbody>
</table>
