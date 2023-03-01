# Breaking Changes

## Environment variables

Some environment variables have been doubled for the portal and the
console, see correspondence table:

<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>before 3.5.0</p></td>
<td style="text-align: left;"><p>after 3.5.0 (for portal)</p></td>
<td style="text-align: left;"><p>after 3.5.0 (for console)</p></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p>authentication.localLogin.enabled</p></td>
<td
style="text-align: left;"><p>portal.authentication.localLogin.enabled</p></td>
<td
style="text-align: left;"><p>console.authentication.localLogin.enabled</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>scheduler.tasks</p></td>
<td style="text-align: left;"><p>portal.scheduler.tasks</p></td>
<td style="text-align: left;"><p>console.scheduler.tasks</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>scheduler.notifications</p></td>
<td style="text-align: left;"><p>portal.scheduler.notifications</p></td>
<td
style="text-align: left;"><p>console.scheduler.notifications</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>reCaptcha.enabled</p></td>
<td style="text-align: left;"><p>portal.reCaptcha.enabled</p></td>
<td style="text-align: left;"><p>console.reCaptcha.enabled</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>reCaptcha.siteKey</p></td>
<td style="text-align: left;"><p>portal.reCaptcha.siteKey</p></td>
<td style="text-align: left;"><p>console.reCaptcha.siteKey</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>portal.support.enabled</p></td>
<td style="text-align: left;"><p>portal.support.enabled</p></td>
<td style="text-align: left;"><p>console.support.enabled</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>portal.userCreation.enabled</p></td>
<td style="text-align: left;"><p>portal.userCreation.enabled</p></td>
<td style="text-align: left;"><p>console.userCreation.enabled</p></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p>portal.userCreation.automaticValidation.enabled</p></td>
<td
style="text-align: left;"><p>portal.userCreation.automaticValidation.enabled</p></td>
<td
style="text-align: left;"><p>console.userCreation.automaticValidation.enabled</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>http.cors.allow-origin</p></td>
<td style="text-align: left;"><p>portal.http.cors.allow-origin</p></td>
<td style="text-align: left;"><p>console.http.cors.allow-origin</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>http.cors.allow-headers</p></td>
<td style="text-align: left;"><p>portal.http.cors.allow-headers</p></td>
<td
style="text-align: left;"><p>console.http.cors.allow-headers</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>http.cors.allow-methods</p></td>
<td style="text-align: left;"><p>portal.http.cors.allow-methods</p></td>
<td
style="text-align: left;"><p>console.http.cors.allow-methods</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>http.cors.exposed-headers</p></td>
<td
style="text-align: left;"><p>portal.http.cors.exposed-headers</p></td>
<td
style="text-align: left;"><p>console.http.cors.exposed-headers</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>http.cors.max-age</p></td>
<td style="text-align: left;"><p>portal.http.cors.max-age</p></td>
<td style="text-align: left;"><p>console.http.cors.max-age</p></td>
</tr>
</tbody>
</table>

# Distribution

From this version, Gravitee.IO APIM is distributed with MongoDB and JDBC
plugins, as well as Hybrid HTTP plugin (gateway-bridge-http), in the
`full` ZIP.  
You no longer have to choose between the "full" or "full-jdbc" ZIP file.

# Repository

## Mongodb

Before running any script, please create a dump of your existing
database.

[/apim/3.x/mongodb/3.5.01-duplicate-some-parameters-for-console.js](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/3.5.0/1-duplicate-some-parameters-for-console.js)  
This script duplicates some parameters for the console to have different
behaviors between portal and console. It also modifies the \_id of each
mongo document to add referenceId and referenceType.
