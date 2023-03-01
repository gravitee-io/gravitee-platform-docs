# Overview

The APIM Expression Language (EL for short) is one of the key features
that can be used by API publishers to configure various aspects and
services of an API.

The EL is a powerful language used for querying and manipulating an
object graph. It is based on the
[SpEL^](http://docs.spring.io/spring/docs/current/spring-framework-reference/html/expressions.html)
(Spring Expression Language). This means that you can do everything
described in the link.

In addition, APIM extends the standard SpEL capabilities by providing
extra objects and properties inside the expression language context.

# Usage

The basic expression language syntax is as follows:

`{#request.id}`

See the sections below for example expression notations.

# API

## Properties

As an API publisher, you can define properties for your API. These
properties are automatically *injected* into the expression language
context to be used later.

### Example

-   Get the value of the property `my-property` defined in API
    properties: `{#properties['my-property']}`

## Dictionaries

Dictionaries work in a similar way to properties, but you need to
specify the dictionary name as well as the property name.

### Example

-   Get the value of the property `my-property` defined in dictionary
    `my-dictionary`: `{#dictionaries['my-dictionary']['my-property']}`

## Endpoints

When you define endpoints for your API, you need to give them a *name*
which must be a unique identifier across all endpoints of the API. This
identifier can be used to get an endpoint reference (i.e. uri).

For example: when you create an API, a *default* endpoint is created,
corresponding to the value you set for the backend property. This
endpoint can be retrieved with EL by using the following syntax:

`{#endpoints['default']}`

# Request

The properties you can access for API requests are listed below.

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Property</p></td>
<td style="text-align: left;"><p>Description</p></td>
<td style="text-align: center;"><p>Type</p></td>
<td style="text-align: left;"><p>Example</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>id</p></td>
<td style="text-align: left;"><p>Identifier</p></td>
<td style="text-align: center;"><p>string</p></td>
<td
style="text-align: left;"><p>12345678-90ab-cdef-1234-567890ab</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>transactionId</p></td>
<td style="text-align: left;"><p>Transaction identifier</p></td>
<td style="text-align: center;"><p>string</p></td>
<td
style="text-align: left;"><p>cd123456-7890-abcd-ef12-34567890</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>uri</p></td>
<td style="text-align: left;"><p>URI</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>/v2/store/MyStore?order=100</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>path</p></td>
<td style="text-align: left;"><p>Path</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>/v2/store/MyStore</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>paths</p></td>
<td style="text-align: left;"><p>Path parts</p></td>
<td style="text-align: center;"><p>array of string</p></td>
<td style="text-align: left;"><p>[,v2,store,MyStore]</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>pathInfo</p></td>
<td style="text-align: left;"><p>Path info</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>/store/MyStore</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>pathInfos</p></td>
<td style="text-align: left;"><p>Path info parts</p></td>
<td style="text-align: center;"><p>array of string</p></td>
<td style="text-align: left;"><p>[,store,MyStore]</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>contextPath</p></td>
<td style="text-align: left;"><p>Context path</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>/v2/</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>params</p></td>
<td style="text-align: left;"><p>Query parameters</p></td>
<td style="text-align: center;"><p>key / value</p></td>
<td style="text-align: left;"><p>order → 100</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>pathParams</p></td>
<td style="text-align: left;"><p>Path parameters</p></td>
<td style="text-align: center;"><p>key / value</p></td>
<td style="text-align: left;"><p>storeId → MyStore (<em>see Warning for
details</em>)</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>headers</p></td>
<td style="text-align: left;"><p>Headers</p></td>
<td style="text-align: center;"><p>key / value</p></td>
<td style="text-align: left;"><p>X-Custom → myvalue</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>method</p></td>
<td style="text-align: left;"><p>HTTP method</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>GET</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>scheme</p></td>
<td style="text-align: left;"><p>HTTP scheme</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>http</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>version</p></td>
<td style="text-align: left;"><p>HTTP version</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>HTTP_1_1</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>timestamp</p></td>
<td style="text-align: left;"><p>Timestamp</p></td>
<td style="text-align: center;"><p>long</p></td>
<td style="text-align: left;"><p>1602781000267</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>remoteAddress</p></td>
<td style="text-align: left;"><p>Remote address</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>0:0:0:0:0:0:0:1</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>localAddress</p></td>
<td style="text-align: left;"><p>Local address</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>0:0:0:0:0:0:0:1</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>content</p></td>
<td style="text-align: left;"><p>Body content</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>ssl</p></td>
<td style="text-align: left;"><p>SSLSession information</p></td>
<td style="text-align: center;"><p><a
href="#SSL Object">???</a></p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
</tbody>
</table>

`{#request.content}` is only available for policies bound to an
`on-request-content` phase.

## SSL Object

The properties you can access in SSL Session object are listed below.

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Property</p></td>
<td style="text-align: left;"><p>Description</p></td>
<td style="text-align: center;"><p>Type</p></td>
<td style="text-align: left;"><p>Example</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>clientHost</p></td>
<td style="text-align: left;"><p>Host name of the client</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>client.domain.com</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>clientPort</p></td>
<td style="text-align: left;"><p>Port number of the client</p></td>
<td style="text-align: center;"><p>long</p></td>
<td style="text-align: left;"><p>443</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>client</p></td>
<td style="text-align: left;"><p>Client information</p></td>
<td style="text-align: center;"><p><a
href="#Principal Object">???</a></p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>server</p></td>
<td style="text-align: left;"><p>Server information</p></td>
<td style="text-align: center;"><p><a
href="#Principal Object">???</a></p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
</tbody>
</table>

## Principal Object

The properties you can access in Principal object are listed below.

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Property</p></td>
<td style="text-align: left;"><p>Description</p></td>
<td style="text-align: center;"><p>Type</p></td>
<td style="text-align: left;"><p>Example</p></td>
</tr>
<tr class="even">
<td colspan="4" style="text-align: left;"><p><strong>Common DN
attributes</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>businessCategory</p></td>
<td style="text-align: left;"><p>Business category</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>c</p></td>
<td style="text-align: left;"><p>Country code</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>FR</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>cn</p></td>
<td style="text-align: left;"><p>Common name</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>countryOfCitizenship</p></td>
<td style="text-align: left;"><p>RFC 3039 CountryOfCitizenship</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>countryOfResidence</p></td>
<td style="text-align: left;"><p>RFC 3039 CountryOfResidence</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>dateOfBirth</p></td>
<td style="text-align: left;"><p>RFC 3039 RFC 3039 DateOfBirth</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>19830719000000Z</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>dc</p></td>
<td style="text-align: left;"><p>Domain component</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>description</p></td>
<td style="text-align: left;"><p>Description</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>dmdName</p></td>
<td style="text-align: left;"><p>RFC 2256 directory management
domain</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>dnQualifier</p></td>
<td style="text-align: left;"><p>Domain name qualifier</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>e</p></td>
<td style="text-align: left;"><p>Email address in Verisign
certificates</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>emailAddress</p></td>
<td style="text-align: left;"><p>Email address (RSA PKCS#9
extension)</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>gender</p></td>
<td style="text-align: left;"><p>RFC 3039 Gender</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>"M", "F", "m" or "f"</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>generation</p></td>
<td style="text-align: left;"><p>Naming attributes of type
X520name</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>givenname</p></td>
<td style="text-align: left;"><p>Naming attributes of type
X520name</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>initials</p></td>
<td style="text-align: left;"><p>Naming attributes of type
X520name</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>l</p></td>
<td style="text-align: left;"><p>Locality name</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>name</p></td>
<td style="text-align: left;"><p>Name</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>nameAtBirth</p></td>
<td style="text-align: left;"><p>ISIS-MTT NameAtBirth</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>o</p></td>
<td style="text-align: left;"><p>Organization</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>organizationIdentifier</p></td>
<td style="text-align: left;"><p>Organization identifier</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>ou</p></td>
<td style="text-align: left;"><p>Organization unit name</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>placeOfBirth</p></td>
<td style="text-align: left;"><p>RFC 3039 PlaceOfBirth</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>postalAddress</p></td>
<td style="text-align: left;"><p>RFC 3039 PostalAddress</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>postalCode</p></td>
<td style="text-align: left;"><p>Postal code</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>pseudonym</p></td>
<td style="text-align: left;"><p>RFC 3039 Pseudonym</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>role</p></td>
<td style="text-align: left;"><p>Role</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>serialnumber</p></td>
<td style="text-align: left;"><p>Device serial number name</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>st</p></td>
<td style="text-align: left;"><p>State or province name</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>street</p></td>
<td style="text-align: left;"><p>Street</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>surname</p></td>
<td style="text-align: left;"><p>Naming attributes of type
X520name</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>t</p></td>
<td style="text-align: left;"><p>Title</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>telephoneNumber</p></td>
<td style="text-align: left;"><p>Telephone number</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>uid</p></td>
<td style="text-align: left;"><p>LDAP User id</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>uniqueIdentifier</p></td>
<td style="text-align: left;"><p>Naming attributes of type
X520name</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>unstructuredAddress</p></td>
<td style="text-align: left;"><p>Unstructured address (from
PKCS#9)</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td colspan="4" style="text-align: left;"><p><strong>Other
attributes</strong></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>attributes</p></td>
<td style="text-align: left;"><p>Retrieves all attribute values</p></td>
<td style="text-align: center;"><p>key / value</p></td>
<td style="text-align: left;"><p>"ou" → ["Test team", "Dev
team"]</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>defined</p></td>
<td style="text-align: left;"><p>Returns true if the principal object is
defined and contains values. False otherwise.</p></td>
<td style="text-align: center;"><p>boolean</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>dn</p></td>
<td style="text-align: left;"><p>Full domain name</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
</tbody>
</table>

Even if some of these attributes can be arrays, EL will return the first
item in the array. If you want to retrieve all values of an attribute,
you can use the `attributes` field

If the principal is not defined, all values are empty.

## Examples

-   Get the value of the `Content-Type` header for an incoming HTTP
    request: `{#request.headers['content-type'][0]}`

-   Get the second part of the request path: `{#request.paths[1]}`

-   Get the client HOST from the SSL session:
    `{#request.ssl.clientHost}`

-   Get the client DN from the SSL session: `{#request.ssl.client.dn}`

-   Get the server organization from the SSL session:
    `{#request.ssl.server.o}`

-   Get all the organization units of the server from the SSL session:

    -   `{#request.ssl.server.attributes['ou'][0]}`

    -   `{#request.ssl.server.attributes['OU'][1]}`

    -   `{#request.ssl.server.attributes['Ou'][2]}`

-   Get a custom attribute of the client from the SSL session:
    `{#request.ssl.client.attributes['1.2.3.4'][0]}`

-   Determine if the SSL attributes of the client are set:
    `{#request.ssl.client.defined}`

# Request context

## Properties

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Property</p></td>
<td style="text-align: left;"><p>Description</p></td>
<td style="text-align: left;"><p>Type</p></td>
<td style="text-align: left;"><p>Always present</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>attributes</p></td>
<td style="text-align: left;"><p>Request context attributes</p></td>
<td style="text-align: center;"><p>key-value</p></td>
<td style="text-align: center;"><p>X</p></td>
</tr>
</tbody>
</table>

## Attributes

When APIM Gateway handles an incoming HTTP request, some attributes are
automatically created. These attributes are:

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Property</p></td>
<td style="text-align: left;"><p>Description</p></td>
<td style="text-align: left;"><p>Type</p></td>
<td style="text-align: left;"><p>Nullable</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>context-path</p></td>
<td style="text-align: left;"><p>Context-path</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: center;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>resolved-path</p></td>
<td style="text-align: left;"><p>Resolved-path is the path defined in
policies</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: center;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>application</p></td>
<td style="text-align: left;"><p>The authenticated application doing
incoming HTTP request</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: center;"><p>X (for keyless plan)</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>api</p></td>
<td style="text-align: left;"><p>Called API</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: center;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>user-id</p></td>
<td style="text-align: left;"><p>The user identifier of incoming HTTP
request:</p>
<p>* The subscription id for api-key based plan</p>
<p>* Remote IP for keyless based plan</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: center;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>plan</p></td>
<td style="text-align: left;"><p>Plan used to manage incoming HTTP
request</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: center;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>api-key</p></td>
<td style="text-align: left;"><p>the api-key used (in case of an api-key
based plan)</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: center;"><p>X (for no api-key plan)</p></td>
</tr>
</tbody>
</table>

Additionally, some policies (like the link:{{
*/apim/3.x/apim\_policies\_oauth2.html#attributes* | relative\_url
}}\[OAuth2 policy\]) register other attributes in the context. See the
documentation for the policies you are using for more information.

## Example

-   Get the value of the `user-id` attribute for an incoming HTTP
    request:

`{#context.attributes['user-id']}`

-   Get the value of the `plan` attribute for an incoming HTTP request:

`{#context.attributes['plan']}`

-   Check that the path starts with a given value:

`{#request.path.startsWith('/my/api')}`

# Response

## Properties

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Property</p></td>
<td style="text-align: left;"><p>Description</p></td>
<td style="text-align: center;"><p>Type</p></td>
<td style="text-align: left;"><p>Example</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>content</p></td>
<td style="text-align: left;"><p>Body content</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>headers</p></td>
<td style="text-align: left;"><p>Headers</p></td>
<td style="text-align: center;"><p>key / value</p></td>
<td style="text-align: left;"><p>X-Custom → myvalue</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>status</p></td>
<td style="text-align: left;"><p>Status of the HTTP response</p></td>
<td style="text-align: center;"><p>int</p></td>
<td style="text-align: left;"><p>200</p></td>
</tr>
</tbody>
</table>

## Example

-   Get the status of an HTTP response: `{#response.status}`

# Node

The properties you can access for node are listed below.

## Properties

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Property</p></td>
<td style="text-align: left;"><p>Description</p></td>
<td style="text-align: center;"><p>Type</p></td>
<td style="text-align: left;"><p>Example</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>id</p></td>
<td style="text-align: left;"><p>Node id</p></td>
<td style="text-align: center;"><p>string</p></td>
<td
style="text-align: left;"><p>975de338-90ff-41ab-9de3-3890ff41ab62</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>version</p></td>
<td style="text-align: left;"><p>Node version</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>3.14.0</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>tenant</p></td>
<td style="text-align: left;"><p>Node tenant</p></td>
<td style="text-align: center;"><p>string</p></td>
<td style="text-align: left;"><p>Europe</p></td>
</tr>
</tbody>
</table>

## Example

-   Get the version of a node : `{#node.version}`

# Policies

You can use the EL to update some aspects of policy configuration. The
policy specifies if it supports EL or not.

# Mixin

In previous examples, we showed various ways to manipulate objects
available in the EL context. You can also mix property usage to provide
an increasingly dynamic configuration.

For example, we can retrieve the value of an HTTP header where the name
is based on an API property named `my-property`:

`{#request.headers[#properties['my-property']]}`
