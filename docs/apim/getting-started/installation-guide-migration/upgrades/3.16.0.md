# API definition import process changes

Gravitee 3.16.0 introduces a new **crossId** in API definition, which
identifies entities across environments. This improves the API import
and promotion processes reliability.

If you are using the *API import from JSON definition* feature, we
**highly recommend** updating your API definitions by re-exporting your
API.

Otherwise, if you import an API definition which doesn’t contain
**crossId**, Gravitee will do the best-effort to import your API
definition without it.

# Deprecations

The Rest API endpoints listed below are deprecated since Gravitee
v3.0.9, and will be removed in a future version.

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
<td style="text-align: left;"><p>POST /apis/{api.id}/import</p></td>
<td style="text-align: left;"><p>POST /apis/import</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>POST
/apis/{api.id}/import/swagger</p></td>
<td style="text-align: left;"><p>PUT
/apis/{api.id}/import/swagger</p></td>
</tr>
</tbody>
</table>
