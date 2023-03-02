# Repository

## Mongodb

Before running any script, please create a dump of your existing
database.

[/apim/3.x/mongodb/3.5.14/1-fix-cors-env-vars.js](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/3.5.14/1-fix-cors-env-vars.js)  
This script migrate CORS environment variables for portal and console.
(See below).

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
<td style="text-align: left;"><p>before 3.5.14</p></td>
<td style="text-align: left;"><p>after 3.5.14 (for portal)</p></td>
<td style="text-align: left;"><p>after 3.5.14 (for console)</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>portal.http.cors.allow-origin</p></td>
<td
style="text-align: left;"><p>http.api.portal.cors.allow-origin</p></td>
<td style="text-align: left;"><p>X</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>console.http.cors.allow-origin</p></td>
<td style="text-align: left;"><p>X</p></td>
<td
style="text-align: left;"><p>http.api.management.cors.allow-origin</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>portal.http.cors.allow-headers</p></td>
<td
style="text-align: left;"><p>http.api.portal.cors.allow-headers</p></td>
<td style="text-align: left;"><p>X</p></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p>console.http.cors.allow-headers</p></td>
<td style="text-align: left;"><p>X</p></td>
<td
style="text-align: left;"><p>http.api.management.cors.allow-header</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>portal.http.cors.allow-methods</p></td>
<td
style="text-align: left;"><p>http.api.portal.cors.allow-methods</p></td>
<td style="text-align: left;"><p>X</p></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p>console.http.cors.allow-methods</p></td>
<td style="text-align: left;"><p>X</p></td>
<td
style="text-align: left;"><p>http.api.management.cors.allow-methods</p></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p>portal.http.cors.exposed-headers</p></td>
<td
style="text-align: left;"><p>http.api.portal.cors.exposed-headers</p></td>
<td style="text-align: left;"><p>X</p></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p>console.http.cors.exposed-headers</p></td>
<td style="text-align: left;"><p>X</p></td>
<td
style="text-align: left;"><p>http.api.management.cors.exposed-headers</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>portal.http.cors.max-age</p></td>
<td style="text-align: left;"><p>http.api.portal.cors.max-age</p></td>
<td style="text-align: left;"><p>X</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>console.http.cors.max-age</p></td>
<td style="text-align: left;"><p>X</p></td>
<td
style="text-align: left;"><p>http.api.management.cors.max-age</p></td>
</tr>
</tbody>
</table>
