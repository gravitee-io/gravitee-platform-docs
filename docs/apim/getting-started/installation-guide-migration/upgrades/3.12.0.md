# Breaking Change

**Policy plugin `gravitee-policy-apikey` prior to version 2.3.0 is no
longer compatible with APIM 3.12.0.**

Starting in version 3.12.0, you must use `gravitee-policy-apikey` &gt;=
2.3.0.

# Default Settings Change Announcement

HTTP Bridge Service will be disabled by default starting in version
3.13.

If you are using this feature, **do not forget to update your
settings.**

For more information, [click
here](https://docs.gravitee.io/apim/3.x/apim_installguide_hybrid_deployment.html#apim_gateway_http_bridge_server)
for documentation.

# API Keys

## Model Change

Before this version, API keys contained a **key** attribute, which is
both the value of the key and also the database ID.

Starting in version 3.12.0, APIKeys now contain distinct attributes:

-   **key**: API key value

-   **ID**: API key database unique ID

The 3 Portal API endpoints listed below now expose distinct **IDs** and
**keys** in the HTTP response (previously, the key attribute was exposed
as ***ID***) :

-   GET /subscriptions/{subscription.id}

-   POST /subscriptions/{subscription.id}

-   POST /subscriptions/{subscription.id}/\_renew

## Deprecated Endpoints

The Rest API endpoints listed below are now deprecated, and will be
removed in a future version.

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Deprecated Endpoint</p></td>
<td style="text-align: left;"><p>Replace With</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>PUT
/apis/{api.id}/keys/{apiKey.key}</p></td>
<td style="text-align: left;"><p>PUT
/apis/{api.id}/subscriptions/{subscription.id}/apikeys/{apiKey.id}</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>DELETE
/apis/{api.id}/keys/{apiKey.key}</p></td>
<td style="text-align: left;"><p>DELETE
/apis/{api.id}/subscriptions/{subscription.id}/apikeys/{apiKey.id}</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>POST
/apis/{api.id}/keys/_verify?apiKey={apiKey.key}</p></td>
<td style="text-align: left;"><p>GET
/apis/{api.id}/subscriptions/_canCreate?application={application.id}&amp;key={apiKey.key}</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>DELETE
/apis/{api.id}/subscriptions/{subscription.id}/keys/{apiKey.key}</p></td>
<td style="text-align: left;"><p>DELETE
/apis/{api.id}/subscriptions/{subscription.id}/apikeys/{apiKey.id}</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET
/apis/{api.id}/subscriptions/{subscription.id}/keys</p></td>
<td style="text-align: left;"><p>GET
/apis/{api.id}/subscriptions/{subscription.id}/apikeys</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>POST
/apis/{api.id}/subscriptions/{subscription.id}</p></td>
<td style="text-align: left;"><p>POST
/apis/{api.id}/subscriptions/{subscription.id}/apikeys/_renew</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>POST
/apis/{api.id}/subscriptions/{subscription.id}/keys/{apiKey.key}/_reactivate</p></td>
<td style="text-align: left;"><p>POST
/apis/{api.id}/subscriptions/{subscription.id}/apikeys/{apiKey.id}/_reactivate</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GET
/applications/{application.id}/subscriptions/{subscription.id}/keys</p></td>
<td style="text-align: left;"><p>GET
/applications/{application.id}/subscriptions/{subscription.id}/apikeys</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>POST
/applications/{application.id}/subscriptions/{subscription.id}</p></td>
<td style="text-align: left;"><p>POST
/applications/{application.id}/subscriptions/{subscription.id}/apikeys/_renew</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>DELETE
/applications/{application.id}/subscriptions/{subscription.id}/keys/{apiKey.key}</p></td>
<td style="text-align: left;"><p>DELETE
/applications/{application.id}/subscriptions/{subscription.id}/apikeys/{apiKey.id}</p></td>
</tr>
</tbody>
</table>

# Repository

## MongoDB

Before running any script, please create a dump of your existing
database.

[/apim/3.x/mongodb/3.12.0/api-keys-migration.js](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/3.12.0/api-keys-migration.js)  
This script adds **key** and **api** columns in api keys **keys** table.
