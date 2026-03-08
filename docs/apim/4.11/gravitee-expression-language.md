# Gravitee Expression Language

<final_file>
## Overview

Gravitee Expression Language (EL) queries and manipulates object graphs to dynamically configure API aspects and policies. Use EL to reference values from the current API transaction and create dynamic filters, routing rules, and policies that respond to specific conditions or parameters.

EL extends the Spring Expression Language (SpEL) by providing additional object properties inside the expression language context. All capabilities detailed in the SpEL documentation are available in EL. Gravitee has implemented customizations detailed in this guide.

{% hint style="info" %}
**Object properties**

Custom properties and attributes have special meanings in the Gravitee ecosystem:

* **Custom properties:** Defined at the API level and read-only during the Gateway's execution of an API transaction. Learn more about setting an API's custom properties in [link to custom properties documentation].
* **Attributes:** Scoped to the current API transaction and can be manipulated during the execution phase through the `assign-attributes` policy. Attributes attach additional information to a request or message via a variable that is dropped after the API transaction completes.
{% endhint %}

## Basic usage

This section summarizes:

* Object properties added to the Expression Language (EL) context
* How attributes are accessed for v4 and v2 APIs
* Commonly used operators and functions

{% tabs %}
{% tab title="Syntax" %}
**Expressions**

Expressions in Gravitee are enclosed in curly braces `{}` and begin with the `#` symbol. Both dot notation and bracket notation are supported for accessing object properties.

Example: `{#context.attributes['user'].email}`

{% hint style="info" %}
**Dot notation vs bracket notation**

Dot notation doesn't work with special characters:

`{#request.headers.my-header}` ← **This will result in an error**

Use bracket notation for property names that include a space or hyphen, or start with a number:

`{#request.headers['my-header']}`
{% endhint %}

**Lists**

Expressions can be used to assign lists, for example: `{({'admin', 'writer'})}`

1. The outer curly braces start and end the EL expression
2. The parentheses indicate an object is being instantiated
3. The list comprises the inner brackets and enclosed values: `{'admin', 'writer'}`
{% endtab %}

{% tab title="Object properties" %}
EL allows you to reference certain values injected into the EL context as object properties. The available object properties are detailed in later sections. EL adds the following root-level object properties:

* `{#api.properties}`: Custom properties defined by the API publisher for that Gateway API
* `{#dictionaries}`: Custom dictionaries defined by the API publisher for that Gateway API
* `{#endpoints}`: Information about the Gateway API's respective endpoints
* `{#request}`: Information about the current API request
* `{#response}`: Information about the current API response
* `{#message}`: Information about the current API message
* `{#node}`: Information about the node hosting the instance of the Gateway handling the API transaction
* `{#application}`: Information about the consumer's Application authenticated by the Gateway (for example: `{#application.metadata['some_key']}`)
* `{#subscription}`: Information about the consumer's Subscription authenticated by the Gateway (for example: `{#subscription.metadata['some_key']}`)
{% endtab %}

{% tab title="Attributes" %}
The `attributes` object property contains attributes that are automatically created by the APIM Gateway during an API transaction or added during the execution phase through the Assign Attributes policy. Attributes fall into one of two categories based on API type:

* `{#context.attributes}`: Attributes associated with v2 APIs or v4 Proxy APIs. A v4 Proxy API is created using the **Proxy upstream protocol** method.
* `{#message.attributes}`: Attributes associated with v4 Message APIs. These APIs are created using the **Introspect messages from event-driven backend** method.

See the v4 API creation wizard for more details.
{% endtab %}

{% tab title="Operators" %}
EL supports various operators, such as arithmetic, logical, comparison, and ternary operators. Examples of commonly used operators in Gravitee include:

* Arithmetic operators: `+`, `-`, `*`, `/`
* Logical operators: `&&` (logical and), `||` (logical or), `!` (logical not)
* Comparison operators: `==`, `!=`, `<`, `<=`, `>`, `>=`
* Ternary operators: `condition ? expression1 : expression2`
{% endtab %}

{% tab title="Functions" %}
EL provides a variety of built-in functions to manipulate and transform data in expressions. Examples of commonly used functions in Gravitee include:

* String functions: `length()`, `substring()`, `replace()`
* `#jsonPath`: Evaluates a `jsonPath` on a specified object. This function invokes `JsonPathUtils.evaluate(…​)`, which delegates to the Jayway JsonPath library. The best way to learn jsonPath syntax is by using the online evaluator.
* `#xpath`: Evaluates an `xpath` on a provided object. For more information regarding XML and XPath, see XML Support - Dealing with XML Payloads in the SpEL documentation.

**`jsonPath` example**

As an example of how `jsonPath` can be used with EL, suppose you have a JSON payload in the request body that contains the following data:

```json
{
  "store": {
    "book": [
      {
        "category": "fiction",
        "author": "Herman Melville",
        "title": "Moby Dick",
        "isbn": "0-553-21311-3",
        "price": 8.99
      },
      {
        "category": "fiction",
        "author": "J. R. R. Tolkien",
        "title": "The Lord of the Rings",
        "isbn": "0-395-19395-8",
        "price": 22.99
      }
    ]
  }
}
```

To extract the value of the `price` property for the book with `title` "The Lord of the Rings," use the following expression:

`{#jsonPath(#request.content, "$.store.book[?(@.title=='The Lord of the Rings')].price")}`
{% endtab %}

{% tab title="Request/Response body access" %}
You can access the request/response raw content using `{#request.content}`.

Depending on the content-type, you can access specific content.

**JSON content**

{% hint style="warning" %}
If a JSON payload has duplicate keys, APIM keeps the last key.

To avoid errors caused by duplicate keys, apply the JSON threat protection policy to the API. For more information about the JSON threat protection policy, see [json-threat-protection](create-and-configure-apis/apply-policies/policy-reference/json-threat-protection "mention").
{% endhint %}

You can access specific attributes of a JSON request/response payload with `{#request.jsonContent.foo.bar}`, where the request body is similar to the following example:

```json
{
  "foo": {
      "bar": "something"
  }
}
```

**XML content**

You can access specific tags of an XML request/response payload with `{#request.xmlContent.foo.bar}`, where the request body is similar to the following example:

```xml
<foo>
  <bar>something</bar>
</foo>
```
{% endtab %}
{% endtabs %}

## Expression Language Assistant

### Overview

The Expression Language (EL) Assistant generates EL expressions based on natural language prompts. You describe the condition or logic you need, and the Assistant returns the corresponding EL syntax.

<figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2Fgit-blob-7672c60e0db5e4b1f2a071af3eba3f0b759cb7e3%2Fanim.gif?alt=media" alt=""><figcaption></figcaption></figure>

### Prerequisites

Before using the EL Assistant, complete the following:

* Register for a Gravitee Cloud account at [Cloud](https://cockpit.gravitee.io/).
* (Self-hosted and Hybrid installations only) Register your installation in Gravitee Cloud. For more information, see Register installations.
* (Self-hosted and Hybrid installations only) Enable the EL Assistant by adding the following configuration:

{% tabs %}
{% tab title="gravitee.yaml" %}
Add the following configuration to the root level of your `gravitee.yaml` file:

```yaml
newtai:
  elgen:
    enabled: true
```
{% endtab %}

{% tab title=".env" %}
Add the following line to your `.env` file:

```bash
gravitee_newtai_elgen_enabled=true
```
{% endtab %}

{% tab title="Helm values.yaml" %}
Add the following configuration to your `values.yaml` file:

```yaml
newtai:
  elgen:
    enabled: true
```
{% endtab %}
{% endtabs %}

### Generate Expression Language with the EL Assistant

{% hint style="info" %}
The EL Assistant is available in any field that supports Expression Language.
{% endhint %}

1.  In the field that supports Expression Language, click the **{EL}** icon.

    <figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2Fgit-blob-008c4fc76a06b5570f9af67bb2cfc51457ab629f%2F304A887B-9FD1-4011-961A-7DB7D91D3478_1_201_a.jpeg?alt=media" alt=""><figcaption></figcaption></figure>

2. In the **EL Assistant** pop-up window, enter a natural language prompt describing the Expression Language you need. For example: "Only run this policy if the header equals test."

3.  Click **Ask Newt AI**. The Assistant generates the corresponding Expression Language.

    <figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2Fgit-blob-7d9c2dbfbfb15a07488aef31b1f2ff476bc84c4c%2FDBE0A0C1-3171-4CA4-A586-A503EBD2B0BD_1_201_a.jpeg?alt=media" alt=""><figcaption></figcaption></figure>

4.  (Optional) Provide feedback by clicking the **thumbs up** or **thumbs down** icon.

    <figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2Fgit-blob-fdfd3541a28f3f38863088cd442a5d75838cbcc3%2F6D6E46F0-AECF-41F9-BE38-53C6EC0EDA38_1_201_a.jpeg?alt=media" alt=""><figcaption></figcaption></figure>

### Use case examples

The following examples demonstrate how to use the EL Assistant for common tasks.

#### Add a condition to a policy flow

To run a policy flow only when a header equals "test," enter the following prompt:

"Only run this policy flow if the header equals test."

The EL Assistant returns:

```
{#request.headers['Test_Endpoints_header'][0] == 'test'}
```

#### Target an endpoint

To configure a target URL for an endpoint that points to `https://jsonplaceholder.typicode.com/`, enter the following prompt:

"The target URL must target the following URL: https://jsonplaceholder.typicode.com/."

The EL Assistant returns:

```
{#context.attributes['https://jsonplaceholder.typicode.com']}
```

#### Add an assertion for API health checks

To create an assertion that validates an HTTP 200 response, enter the following prompt:

"Check only the status of the following HTTP response that equals 200."

The EL Assistant returns:

```
{#response.status == 200}
```

## APIs

Use the Gravitee Expression Language (EL) to access API transaction information through root-level objects injected into the EL context: custom properties, dictionaries, and endpoints.

{% tabs %}
{% tab title="Custom properties" %}
Define custom properties for your API. These properties are automatically injected into the expression language context and can be referenced during an API transaction from the `{#api.properties}` root-level object property.

**Examples**

* Get the value of the property `my-property` defined in an API's custom properties: `{#api.properties['my-property']}`
* Get the value of the property `my-secret` defined and encrypted in an API's custom properties: `{#api.properties['my-secret']}`

{% hint style="info" %}
**Encrypted custom properties**

When you access an encrypted custom property, the Gateway automatically decrypts it and provides a plain text value.
{% endhint %}
{% endtab %}

{% tab title="Dictionaries" %}
Dictionaries work similarly to custom properties, but you must specify both the dictionary ID and the dictionary property name. Dictionary properties are key-value pairs that can be accessed from the `{#dictionaries}` root-level object property.

**Example**

Get the value of the dictionary property `dict-key` defined in dictionary `my-dictionary-id`: `{#dictionaries['my-dictionary-id']['dict-key']}`.
{% endtab %}

{% tab title="Endpoints" %}
When you define endpoints for your API, assign each a unique name across all endpoints. Use this identifier to get an endpoint reference (a URI) from the `{#endpoints}` root-level object property.

**Example**

When you create an API, a default endpoint is created that corresponds to the backend property value. Retrieve this endpoint using the following syntax: `{#endpoints['default']}`.
{% endtab %}
{% endtabs %}

## Request

EL can be used to access request properties and attributes as described below.

### Request object properties

The object properties you can access from the `{#request}` root-level object property and use for API requests are listed below.

{% tabs %}
{% tab title="Table" %}
<table><thead><tr><th width="172">Object property</th><th width="157">Description</th><th width="134">Type</th><th>Example</th></tr></thead><tbody><tr><td>content</td><td>Body content</td><td>string</td><td>-</td></tr><tr><td>contextPath</td><td>Context path</td><td>string</td><td>/v2/</td></tr><tr><td>headers</td><td>Headers</td><td>key / value</td><td>X-Custom → myvalue</td></tr><tr><td>host</td><td>The host of the request. This is preferable to using the Host header of the request because HTTP2 requests do not provide this header.</td><td>string</td><td>gravitee.example.com</td></tr><tr><td>id</td><td>Identifier</td><td>string</td><td>12345678-90ab-cdef-1234-567890ab</td></tr><tr><td>localAddress</td><td>Local address</td><td>string</td><td>0:0:0:0:0:0:0:1</td></tr><tr><td>method</td><td>HTTP (Hypertext Transfer Protocol) method</td><td>string</td><td>GET</td></tr><tr><td>params</td><td>Query parameters</td><td>key / value</td><td>order → 100</td></tr><tr><td>path</td><td>Path</td><td>string</td><td>/v2/store/MyStore</td></tr><tr><td>pathInfo</td><td>Path info</td><td>string</td><td>/store/MyStore</td></tr><tr><td>pathInfos</td><td>Path info parts</td><td>array of strings</td><td>[,store,MyStore]</td></tr><tr><td>pathParams</td><td>Path parameters</td><td>key / value</td><td>storeId → MyStore (<em>see Warning for details</em>)</td></tr><tr><td>pathParamsRaw</td><td>Path parameters</td><td>string</td><td>/something/:id/**</td></tr><tr><td>paths</td><td>Path parts</td><td>array of strings</td><td>[,v2,store,MyStore]</td></tr><tr><td>remoteAddress</td><td>Remote address</td><td>string</td><td>0:0:0:0:0:0:0:1</td></tr><tr><td>scheme</td><td>The scheme of the request (either <code>http</code> or <code>https</code>)</td><td>string</td><td>http</td></tr><tr><td>ssl</td><td>SSL (Secure Sockets Layer) session information</td><td>SSL object</td><td>-</td></tr><tr><td>timestamp</td><td>Timestamp</td><td>long</td><td>1602781000267</td></tr><tr><td>transactionId</td><td>Transaction identifier</td><td>string</td><td>cd123456-7890-abcd-ef12-34567890</td></tr><tr><td>uri</td><td>URI (Uniform Resource Identifier)</td><td>string</td><td>/v2/store/MyStore?order=100</td></tr><tr><td>version</td><td>HTTP version</td><td>string</td><td>HTTP_1_1</td></tr></tbody></table>
{% endtab %}

{% tab title="Examples" %}
* Get the value of the `Content-Type` header for an incoming HTTP request: `{#request.headers['content-type']}`
* Get the second part of the request path: `{#request.paths[1]}`
{% endtab %}
{% endtabs %}

### Request context attributes

When APIM Gateway handles an incoming API request, some object properties are automatically created or added during the execution phase through the Assign Attributes policy. These object properties are known as attributes. Attributes can be accessed from the `{#context.attributes}` root-level object property.

Some policies (e.g., the OAuth2 policy) register other attributes in the request context. For more information, refer to the documentation for individual policies.

Request context attributes and examples are listed below.

{% tabs %}
{% tab title="Table" %}
<table><thead><tr><th width="170">Object property</th><th width="190">Description</th><th width="104">Type</th><th>Nullable</th></tr></thead><tbody><tr><td>api</td><td>Called API</td><td>string</td><td>-</td></tr><tr><td>api-key</td><td>The API key used (for an API Key plan)</td><td>string</td><td>X (for no API Key plan)</td></tr><tr><td>application</td><td>The authenticated application making incoming HTTP requests</td><td>string</td><td>X (for Keyless plan)</td></tr><tr><td>context-path</td><td>Context path</td><td>string</td><td>-</td></tr><tr><td>plan</td><td>Plan used to manage incoming HTTP requests</td><td>string</td><td>-</td></tr><tr><td>resolved-path</td><td>The path defined in policies</td><td>string</td><td>-</td></tr><tr><td>user-id</td><td><p>The user identifier of an incoming HTTP request:</p><p>* The subscription ID for an API Key plan</p><p>* The remote IP for a Keyless plan</p></td><td>string</td><td>-</td></tr></tbody></table>
{% endtab %}

{% tab title="Examples" %}
* Get the value of the `user-id` attribute for an incoming HTTP request: `{#context.attributes['user-id']}`
* Get the value of the `plan` attribute for an incoming HTTP request: `{#context.attributes['plan']}`
{% endtab %}
{% endtabs %}

### SSL object properties

The object properties you can access in the `ssl` session object from the `{#request.ssl}` root-level object property are listed below.

{% tabs %}
{% tab title="Table" %}
<table><thead><tr><th width="172">Object property</th><th width="177">Description</th><th width="169">Type</th><th>Example</th></tr></thead><tbody><tr><td>clientHost</td><td>Host name of the client</td><td>string</td><td>client.domain.com</td></tr><tr><td>clientPort</td><td>Port number of the client</td><td>long</td><td>443</td></tr><tr><td>client</td><td>Client information</td><td>Principal object</td><td>-</td></tr><tr><td>server</td><td>Server information</td><td>Principal object</td><td>-</td></tr></tbody></table>
{% endtab %}

{% tab title="Example" %}
Get the client HOST from the SSL session: `{#request.ssl.clientHost}`
{% endtab %}
{% endtabs %}

#### Principal objects

The `client` and `server` objects are of type `Principal`. A `Principal` object represents the currently authenticated user who is making the request to the API and provides access to various user attributes such as username, email address, roles, and permissions.

The `Principal` object is typically used with security policies such as OAuth2, JWT (JSON Web Token), or basic authentication to enforce access control and authorization rules on incoming requests. For example, a policy can check if the current user has a specific role or permission before allowing them to access a protected resource.

If the `Principal` object is not defined, `client` and `server` object values are empty. Otherwise, there are domain name attributes you can access from the `{#request.ssl.client}` and `{#request.ssl.server}` `Principal` objects as shown in the table below:

{% hint style="warning" %}
**Limitation on arrays**

All attributes of the `Principal` object are flattened to be accessed directly with dot or bracket notation. While some of these attributes can be arrays, EL will only return the first item in the array. To retrieve all values of an attribute, use the `attributes` object property shown in the table and examples below.
{% endhint %}

{% tabs %}
{% tab title="Table" %}
<table><thead><tr><th width="218">Object property</th><th width="154">Description</th><th width="102">Type</th><th>Example</th></tr></thead><tbody><tr><td>attributes</td><td>Retrieves all the <code>Principal</code> object's domain name attributes</td><td>key / value</td><td>"ou" → ["Test team", "Dev team"]</td></tr><tr><td>businessCategory</td><td>Business category</td><td>string</td><td>-</td></tr><tr><td>c</td><td>Country code</td><td>string</td><td>FR</td></tr><tr><td>cn</td><td>Common name</td><td>string</td><td>-</td></tr><tr><td>countryOfCitizenship</td><td>RFC 3039 CountryOfCitizenship</td><td>string</td><td>-</td></tr><tr><td>countryOfResidence</td><td>RFC 3039 CountryOfResidence</td><td>string</td><td>-</td></tr><tr><td>dateOfBirth</td><td>RFC 3039 DateOfBirth</td><td>string</td><td>19830719000000Z</td></tr><tr><td>dc</td><td>Domain component</td><td>string</td><td>-</td></tr><tr><td>defined</td><td>Returns <code>true</code> if the <code>Principal</code> object is defined and contains values. Returns <code>false</code> otherwise.</td><td>boolean</td><td>-</td></tr><tr><td>description</td><td>Description</td><td>string</td><td>-</td></tr><tr><td>dmdName</td><td>RFC 2256 directory management domain</td><td>string</td><td>-</td></tr><tr><td>dn</td><td>Fully qualified domain name</td><td>string</td><td>-</td></tr><tr><td>dnQualifier</td><td>Domain name qualifier</td><td>string</td><td>-</td></tr><tr><td>e</td><td>Email address in Verisign certificates</td><td>string</td><td>-</td></tr><tr><td>emailAddress</td><td>Email address (RSA PKCS#9 extension)</td><td>string</td><td>-</td></tr><tr><td>gender</td><td>RFC 3039 Gender</td><td>string</td><td>"M", "F", "m" or "f"</td></tr><tr><td>generation</td><td>Naming attributes of type X520name</td><td>string</td><td>-</td></tr><tr><td>givenname</td><td>Naming attributes of type X520name</td><td>string</td><td>-</td></tr><tr><td>initials</td><td>Naming attributes of type X520name</td><td>string</td><td>-</td></tr><tr><td>l</td><td>Locality name</td><td>string</td><td>-</td></tr><tr><td>name</td><td>Name</td><td>string</td><td>-</td></tr><tr><td>nameAtBirth</td><td>ISIS-MTT NameAtBirth</td><td>string</td><td>-</td></tr><tr><td>o</td><td>Organization</td><td>string</td><td>-</td></tr><tr><td>organizationIdentifier</td><td>Organization identifier</td><td>string</td><td>-</td></tr><tr><td>ou</td><td>Organization unit name</td><td>string</td><td>-</td></tr><tr><td>placeOfBirth</td><td>RFC 3039 PlaceOfBirth</td><td>string</td><td>-</td></tr><tr><td>postalAddress</td><td>RFC 3039 PostalAddress</td><td>string</td><td>-</td></tr><tr><td>postalCode</td><td>Postal code</td><td>string</td><td>-</td></tr><tr><td>pseudonym</td><td>RFC 3039 Pseudonym</td><td>string</td><td>-</td></tr><tr><td>role</td><td>Role</td><td>string</td><td>-</td></tr><tr><td>serialnumber</td><td>Device serial number name</td><td>string</td><td>-</td></tr><tr><td>st</td><td>State or province name</td><td>string</td><td>-</td></tr><tr><td>street</td><td>Street</td><td>string</td><td>-</td></tr><tr><td>surname</td><td>Naming attributes of type X520name</td><td>string</td><td>-</td></tr><tr><td>t</td><td>Title</td><td>string</td><td>-</td></tr><tr><td>telephoneNumber</td><td>Telephone number</td><td>string</td><td>-</td></tr><tr><td>uid</td><td>LDAP (Lightweight Directory Access Protocol) User id</td><td>string</td><td>-</td></tr><tr><td>uniqueIdentifier</td><td>Naming attributes of type X520name</td><td>string</td><td>-</td></tr><tr><td>unstructuredAddress</td><td>Unstructured address (from PKCS#9)</td><td>string</td><td>-</td></tr></tbody></table>
{% endtab %}

{% tab title="Examples" %}
**Standard object properties**

* Get the client DN from the SSL session: `{#request.ssl.client.dn}`
* Get the server organization from the SSL session: `{#request.ssl.server.o}`

**Arrays and boolean logic**

* Get all the organization units of the server from the SSL session:
  * `{#request.ssl.server.attributes['ou'][0]}`
  * `{#request.ssl.server.attributes['OU'][1]}`
  * `{#request.ssl.server.attributes['Ou'][2]}`
* Get a custom attribute of the client from the SSL session: `{#request.ssl.client.attributes['1.2.3.4'][0]}`
* Determine if the SSL attributes of the client are set: `{#request.ssl.client.defined}`
{% endtab %}
{% endtabs %}

## Response

The `{#response}` root-level object property provides access to API response data. The following table lists the available object properties.

{% tabs %}
{% tab title="Table" %}
<table><thead><tr><th width="172">Object property</th><th>Description</th><th width="125">Type</th><th>Example</th></tr></thead><tbody><tr><td>content</td><td>Body content</td><td>string</td><td>-</td></tr><tr><td>headers</td><td>Headers</td><td>key / value</td><td>X-Custom → myvalue</td></tr><tr><td>status</td><td>Status of the HTTP response</td><td>int</td><td>200</td></tr></tbody></table>
{% endtab %}

{% tab title="Example" %}
Get the status of an HTTP response:

```
{#response.status}
```
{% endtab %}
{% endtabs %}

## Message

The `{#message}` root-level object property provides access to API message properties. A message (sent or received) may contain attributes that can be retrieved via `{#message.attributes[key]}`.

{% hint style="info" %}
The EL (Expression Language) used for a message does not change based on phase. EL is executed on the message itself, so whether the message is sent in the subscribe or publish phase is irrelevant.
{% endhint %}

{% tabs %}
{% tab title="Table" %}
<table><thead><tr><th width="172">Object property</th><th>Description</th><th width="125">Type</th><th>Example</th></tr></thead><tbody><tr><td>attributeNames</td><td>The names of the attributes</td><td>list / array</td><td>-</td></tr><tr><td>attributes</td><td>Attributes attached to the message</td><td>key / value</td><td>-</td></tr><tr><td>content</td><td>Content of the message</td><td>string</td><td>-</td></tr><tr><td>contentLength</td><td>Size of the content</td><td>integer</td><td>-</td></tr><tr><td>error</td><td>Flag regarding the error state of the message</td><td>boolean</td><td>-</td></tr><tr><td>headers</td><td>Headers attached to the message</td><td>key / value</td><td>-</td></tr><tr><td>id</td><td>ID of the message</td><td>string</td><td>-</td></tr><tr><td>metadata</td><td>Metadata attached to the message</td><td>key / value</td><td>-</td></tr></tbody></table>
{% endtab %}

{% tab title="Examples" %}
* Get the value of the `Content-Type` header for a message: `{#message.headers['content-type']}`
* Get the size of a message: `{#message.contentLength}`
{% endtab %}
{% endtabs %}
