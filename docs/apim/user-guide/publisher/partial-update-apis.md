{% assign version = site.products.apim.\_3x.version | split: "." %} {%
capture current\_version %}{{ version\[0\] }}.{{ version\[1\] }}{%
endcapture %}

# Overview

This method lets you update only a part of an existing API definition
and/or its sub-resources (e.g., plans, pages, metadata), either by
adding updating or removing attributes. It provides more flexbility in
case of small updates as you are not required to provide the full API
definition like when using the `**PUT /api/import**` endpoint.

The business rules that apply during a partial update are identical to
those used for the `**PUT /api/import**` endpoint.

# HTTP PATCH and format

To partially update your API use the HTTP `PATCH` verb on the
`**/api/import**` enpdoint.

The expected format of the request body is a JSON document containing
the list of operations describing the changes you want to apply to the
API definition.

The format used to describe these changes is based on [JSON
Patch](https://datatracker.ietf.org/doc/html/rfc6902) but uses [JSON
Path](https://github.com/json-path/JsonPath) instead of JSON Pointer.

## JSON Patch format

A JSON Patch document is an **array** of JSON objects, each object
representing exactly one JSON Patch operation.

Each patch operation takes the following fields:

-   `operation`: defines the type of operation (e.g., ADD, REMOVE,
    REPLACE, TEST)

-   `jsonPath`: defines where the operation applies in the document
    through a JSON Path expression. Check [???](#JsonPath syntax)
    section for more details.

-   `value`: defines the value to apply (e.g., a raw JSON literal,
    object, or array), optional for `REMOVE` operation.

### Example

The below example would update the API version and remove an API
property:

    [
      {
        "jsonPath": "$.version",
        "value": "3.2.0",
        "operation": "REPLACE"
      },
      {
        "jsonPath": "$.properties[?(@.key == 'properties_1')]",
        "operation": "REMOVE"
      }
    ]

## JSON Patch operations

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 80%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Operation</p></td>
<td style="text-align: left;"><p>Description</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>REPLACE (default)</p></td>
<td style="text-align: left;"><p>Updates the value at the targeted
location with a new value.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>ADD</p></td>
<td style="text-align: left;"><p>Adds a new property to an object or
inserts a new item into an array.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>REMOVE</p></td>
<td style="text-align: left;"><p>Removes a value at the defined
location</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>TEST</p></td>
<td style="text-align: left;"><p>Tests that the value at the defined
"path" is equal to the <code>value</code>. Because the PATCH operation
is atomic, the PATCH should be discarded if any of its operations fail.
The test operation can be used to validate that the preconditions and
post-conditions have been met. In case the condition fails the API will
return an <code>HTTP 204 No Content</code>.</p></td>
</tr>
</tbody>
</table>

# JSONPath syntax

A JSONPath expression must be provided in the `jsonPath` attribute of
each JSON Patch operation.

Note that:

-   JSONPath is a **query language** for JSON, similar to XPath for XML.

-   JSONPath expressions always refer to a **JSON structure**.

-   The *root member object* in JSONPath is always referred to as `$`
    regardless if it is an object or array.

-   JSONPath expressions, including property names and values, are
    **case-sensitive**.

## Operators

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 80%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Operator</p></td>
<td style="text-align: left;"><p>Description</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>$</code></p></td>
<td style="text-align: left;"><p>The root element to query. This starts
all path expressions.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>@</code></p></td>
<td style="text-align: left;"><p>The current node being processed by a
filter predicate.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>*</code></p></td>
<td style="text-align: left;"><p>Wildcard. Available anywhere a name or
numeric are required.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>..</code></p></td>
<td style="text-align: left;"><p>Deep scan. Available anywhere a name is
required.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>.&lt;name&gt;</code></p></td>
<td style="text-align: left;"><p>Dot-notated child</p></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p><code>['&lt;name&gt;' (, '&lt;name&gt;')]</code></p></td>
<td style="text-align: left;"><p>Bracket-notated child or
children</p></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p><code>[&lt;number&gt; (, &lt;number&gt;)]</code></p></td>
<td style="text-align: left;"><p>Array index or indexes</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>[start:end]</code></p></td>
<td style="text-align: left;"><p>Array slice operator</p></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p><code>[?(&lt;expression&gt;)]</code></p></td>
<td style="text-align: left;"><p>Filter expression. Expression must
evaluate to a boolean value.</p></td>
</tr>
</tbody>
</table>

## Filters

Filters are logical expressions used to filter arrays:

-   A typical filter would be `[?(@.age > 18)]` where `@` represents the
    current item being processed.

-   More complex filters can be created with logical operators `&&` and
    `||`.

-   String literals must be enclosed by single or double quotes
    (`[?(@.color == 'blue')]` or `[?(@.color == "blue")]`).

<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Operator</p></td>
<td style="text-align: left;"><p>Description</p></td>
<td style="text-align: left;"></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>==</p></td>
<td style="text-align: left;"><p>left is equal to right (note that 1 is
not equal to <em>1</em>)</p></td>
<td style="text-align: left;"></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>!=</p></td>
<td style="text-align: left;"><p>left is not equal to right</p></td>
<td style="text-align: left;"></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>&lt;</p></td>
<td style="text-align: left;"><p>left is less than right</p></td>
<td style="text-align: left;"></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>⇐</p></td>
<td style="text-align: left;"><p>left is less or equal to right</p></td>
<td style="text-align: left;"></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>&gt;</p></td>
<td style="text-align: left;"><p>left is greater than right</p></td>
<td style="text-align: left;"></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>&gt;=</p></td>
<td style="text-align: left;"><p>left is greater than or equal to
right</p></td>
<td style="text-align: left;"></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>=~</p></td>
<td style="text-align: left;"><p>left matches regular expression
[?(@.name =~ /foo.*?/i)]</p></td>
<td style="text-align: left;"></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>in</p></td>
<td style="text-align: left;"><p>left exists in right [?(@.size in
[<em>S</em>, <em>M</em>])]</p></td>
<td style="text-align: left;"></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>nin</p></td>
<td style="text-align: left;"><p>left does not exists in right</p></td>
<td style="text-align: left;"></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>subsetof</p></td>
<td style="text-align: left;"><p>left is a subset of right [?(@.sizes
subsetof [<em>S</em>, <em>M</em>, <em>L</em>])]</p></td>
<td style="text-align: left;"></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>anyof</p></td>
<td style="text-align: left;"><p>left has an intersection with right
[?(@.sizes anyof [<em>M</em>, <em>L</em>])]</p></td>
<td style="text-align: left;"></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>noneof</p></td>
<td style="text-align: left;"><p>left has no intersection with right
[?(@.sizes noneof [<em>M</em>, <em>L</em>])]</p></td>
<td style="text-align: left;"></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>size</p></td>
<td style="text-align: left;"><p>size of left (array or string) should
match right</p></td>
<td style="text-align: left;"></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>empty</p></td>
<td style="text-align: left;"><p>left (array or string) should be
empty</p></td>
<td style="text-align: left;"></td>
</tr>
</tbody>
</table>

# Dry run mode

A good way to test your request before actually applying the changes on
your API definition is to execute a *dry run* of your request.

When executing a *dry run*, no changes will be commited to database and
the targeted API definition will not be affacted.

Instead, a simulation of your changes will be executed and the resulting
API definition will be provided in response.

Set `dryRun` query parameter to `true` to enable *dry run* mode:

`PATCH /apis/{api.id}/definition?dryRun=true`

# Partial update examples

Below a list of examples that you might find useful when managing your
APIs through an automated CI/CD process:

## Update an API version

    curl -H "Authorization: Bearer MY-ACCESS-TOKEN" \
         -H "Content-Type:application/json;charset=UTF-8" \
         -X PATCH \
         -d '[
               {
                 "jsonPath": "$.version",
                 "value": "3.2.0",
                 "operation": "REPLACE"
               }
             ]' \
         https://[GRAVITEEIO-APIM-MGT-API-HOST]/management/organizations/[ORGANIZATION_ID]/environments/[ENVIRONMENT_ID]/apis/[API_ID]/definition

## Update an API version in dry run mode

    curl -H "Authorization: Bearer MY-ACCESS-TOKEN" \
         -H "Content-Type:application/json;charset=UTF-8" \
         -X PATCH \
         -d '[
               {
                 "jsonPath": "$.version",
                 "value": "3.2.0",
                 "operation": "REPLACE"
               }
             ]' \
         https://[GRAVITEEIO-APIM-MGT-API-HOST]/management/organizations/[ORGANIZATION_ID]/environments/[ENVIRONMENT_ID]/apis/[API_ID]/definition?dryRun=true

## Update the weight of a specific backend

    curl -H "Authorization: Bearer MY-ACCESS-TOKEN" \
         -H "Content-Type:application/json;charset=UTF-8" \
         -X PATCH \
         -d '[
               {
                 "jsonPath": "$.proxy.groups[?(@.name == 'my-group')].endpoints[?(@.name == 'my-endpoint')].weight",
                 "value": "10",
                 "operation": "REPLACE"
               }
             ]' \
         https://[GRAVITEEIO-APIM-MGT-API-HOST]/management/organizations/[ORGANIZATION_ID]/environments/[ENVIRONMENT_ID]/apis/[API_ID]/definition

## Switch backup endpoint

    curl -H "Authorization: Bearer MY-ACCESS-TOKEN" \
         -H "Content-Type:application/json;charset=UTF-8" \
         -X PATCH \
         -d '[
               {
                 "jsonPath": "$.proxy.groups[?(@.name == 'my-group')].endpoints[?(@.name == 'my-endpoint')].backup",
                 "value": true,
                 "operation": "REPLACE"
               },
              {
                 "jsonPath": "$.proxy.groups[?(@.name == 'my-group')].endpoints[?(@.name == 'my-endpoint-backup')].backup",
                 "value": false,
                 "operation": "REPLACE"
              }
             ]' \
         https://[GRAVITEEIO-APIM-MGT-API-HOST]/management/organizations/[ORGANIZATION_ID]/environments/[ENVIRONMENT_ID]/apis/[API_ID]/definition

## Update the target of an endpoint

    curl -H "Authorization: Bearer MY-ACCESS-TOKEN" \
         -H "Content-Type:application/json;charset=UTF-8" \
         -X PATCH \
         -d '[
               {
                 "jsonPath": "$.proxy.groups[?(@.name == 'default-group')].endpoints[?(@.name == 'my-endpoint')].target",
                 "value": "https://api.gravitee.io/echo",
                 "operation": "REPLACE"
               }
             ]' \
         https://[GRAVITEEIO-APIM-MGT-API-HOST]/management/organizations/[ORGANIZATION_ID]/environments/[ENVIRONMENT_ID]/apis/[API_ID]/definition

## Create a new policy flow

    curl -H "Authorization: Bearer MY-ACCESS-TOKEN" \
         -H "Content-Type:application/json;charset=UTF-8" \
         -X PATCH \
         -d '[
                {
                  "jsonPath": "$.flows",
                  "value": [
                     {
                       "name": "ALL",
                       "methods": ["GET", "POST", "PUT"],
                       "path-operator": {
                         "path": "/"
                       },
                      "pre": [],
                      "post": []
                    }
                  ],
                  "operation": "REPLACE"
                }
             ]' \
         https://[GRAVITEEIO-APIM-MGT-API-HOST]/management/organizations/[ORGANIZATION_ID]/environments/[ENVIRONMENT_ID]/apis/[API_ID]/definition

## Add a policy to an existing flow

    curl -H "Authorization: Bearer MY-ACCESS-TOKEN" \
         -H "Content-Type:application/json;charset=UTF-8" \
         -X PATCH \
         -d '[
               {
                 "jsonPath": "$.flows[?(@.path-operator.path == '/')].post",
                 "value": {
                   "policy": "mock",
                   "name": "A mock",
                   "configuration": {
                     "status": "200",
                     "content": "{ \"message\": \"This is a mock\" }"
                   }
                 },
                 "operation": "ADD"
               }
             ]' \
         https://[GRAVITEEIO-APIM-MGT-API-HOST]/management/organizations/[ORGANIZATION_ID]/environments/[ENVIRONMENT_ID]/apis/[API_ID]/definition

## Update a policy configuration

    curl -H "Authorization: Bearer MY-ACCESS-TOKEN" \
         -H "Content-Type:application/json;charset=UTF-8" \
         -X PATCH \
         -d '[
               {
                 "jsonPath": "$.flows[?(@.path-operator.path == '/')].post[?(@.name == 'A mock')].configuration",
                 "value": {
                   "status": "500",
                   "content": "{#request.attributes.api}"
                 },
                 "operation": "REPLACE"
               }
             ]' \
         https://[GRAVITEEIO-APIM-MGT-API-HOST]/management/organizations/[ORGANIZATION_ID]/environments/[ENVIRONMENT_ID]/apis/[API_ID]/definition

## Add a resource

    curl -H "Authorization: Bearer MY-ACCESS-TOKEN" \
         -H "Content-Type:application/json;charset=UTF-8" \
         -X PATCH \
         -d '[
               {
                 "jsonPath": "$.resources",
                 "value": {
                   "name": "cache_name",
                   "type": "cache",
                   "enabled": false,
                   "configuration": {
                     "name": "my-cache",
                     "timeToIdleSeconds": 100,
                     "timeToLiveSeconds": 200,
                     "maxEntriesLocalHeap": 1000
                   }
                 },
                 "operation": "ADD"
                }
             ]' \
         https://[GRAVITEEIO-APIM-MGT-API-HOST]/management/organizations/[ORGANIZATION_ID]/environments/[ENVIRONMENT_ID]/apis/[API_ID]/definition

## Update a resource configuration

    curl -H "Authorization: Bearer MY-ACCESS-TOKEN" \
         -H "Content-Type:application/json;charset=UTF-8" \
         -X PATCH \
         -d '[
               {
                 "jsonPath": "$.resources[?(@.name == 'cache_name')].enabled",
                 "value": false
               },
               {
                 "jsonPath": "$.resources[?(@.name == 'cache_name')].configuration.timeToIdleSeconds",
                 "value": 1000
               }
             ]' \
         https://[GRAVITEEIO-APIM-MGT-API-HOST]/management/organizations/[ORGANIZATION_ID]/environments/[ENVIRONMENT_ID]/apis/[API_ID]/definition

## Set properties if don’t already exist

    curl -H "Authorization: Bearer MY-ACCESS-TOKEN" \
         -H "Content-Type:application/json;charset=UTF-8" \
         -X PATCH \
         -d '[
               {
                 "jsonPath": "$.properties",
                 "value": "null",
                 "operation": "TEST"
               },
               {
                 "jsonPath": "$.properties",
                 "value": [
                    { key: "properties_1", value: "my_property_value_1" },
                    { key: "properties_2", value: "my_property_value_2" }
                 ],
                 "operation": "REPLACE"
               }
             ]' \
         https://[GRAVITEEIO-APIM-MGT-API-HOST]/management/organizations/[ORGANIZATION_ID]/environments/[ENVIRONMENT_ID]/apis/[API_ID]/definition

## Remove a property by key

    curl -H "Authorization: Bearer MY-ACCESS-TOKEN" \
         -H "Content-Type:application/json;charset=UTF-8" \
         -X PATCH \
         -d '[
               {
                 "jsonPath": "$.properties[?(@.key == 'properties_1')]",
                 "operation": "REMOVE"
               }
             ]' \
         https://[GRAVITEEIO-APIM-MGT-API-HOST]/management/organizations/[ORGANIZATION_ID]/environments/[ENVIRONMENT_ID]/apis/[API_ID]/definition
