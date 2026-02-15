---
description: An overview about gravitee expression language.
metaLinks:
  alternates:
    - gravitee-expression-language.md
---

# Gravitee Expression Language

## Overview

Gravitee Expression Language (EL) is used to query and manipulate object graphs and dynamically configure various aspects and policies of an API. It allows you to reference values from the current API transaction to use expressions to create dynamic filters, routing rules, and policies that respond to specific conditions or parameters.

EL is an extended version of the Spring Expression Language (SpEL) that augments standard SpEL capabilities by providing additional object properties inside the expression language context. As an extension of SpEL, all capabilities detailed in the SpEL documentation are available in EL. However, Gravitee has implemented customizations that are detailed below.

{% hint style="info" %}
**Object properties**

Custom properties and attributes have special meanings in the Gravitee ecosystem:

* **Custom Properties:** Defined at the API level and read-only during the Gateway's execution of an API transaction. You can learn more about how to set an API's custom properties here.
* **Attributes:** Scoped to the current API transaction and can be manipulated during the execution phase through the `assign-attributes` policy. Attributes are used to attach additional information to a request or message via a variable that is dropped after the API transaction is completed.
{% endhint %}

## Basic usage

The information below summarizes:

* Object properties added to the EL context
* How attributes are accessed for v4 and v2 APIs
* Commonly used operators and functions

{% tabs %}
{% tab title="Syntax" %}
**Expressions**

Expressions in Gravitee are enclosed in curly braces `{}` and begin with the `#` symbol. Both dot notation and bracket notation are supported for accessing the properties of an object.

Example: `{#context.attributes['user'].email}`

{% hint style="info" %}
**Dot notation vs bracket notation**

Please note that dot notation will not work with special characters:

`{#request.headers.my-header}` <- **This will result in an error**

Bracket notation should be used for property names that include a space or a hyphen, or start with a number:

`{#request.headers['my-header']}`
{% endhint %}

**Lists**

Expressions can be used to assign lists, e.g., `{({'admin', 'writer'})}`

1. The outer enclosing brackets start and end the EL expression
2. The parentheses indicates an object is being instantiated
3. The list comprises the inner brackets and enclosed values, e.g., `{'admin', 'writer'}`
{% endtab %}

{% tab title="Object properties" %}
EL allows you to reference certain values injected into the EL context as object properties. The available object properties will be further detailed in later sections. EL adds the following root-level object properties:

* `{#api.properties}`: Contains custom properties defined by the API publisher for that Gateway API.
* `{#dictionaries}`: Contains custom dictionaries defined by the API publisher for that Gateway API.
* `{#endpoints}`: Contains information about the Gateway API's respective endpoints.
* `{#request}`: Contains information about the current API request.
* `{#response}`: Contains information about the current API response.
* `{#message}`: Contains information about the current API message.
* `{#node}` : Contains information about the node hosting the instance of the Gateway handling the API transaction.
{% endtab %}

{% tab title="Attributes" %}
The `attributes` object property contains attributes that are automatically created by the APIM Gateway during an API transaction or added during the execution phase through the Assign Attributes policy. However, attributes fall into one of two categories based on API type:

* `{#context.attributes}`: Contains attributes associated with v2 APIs or v4 Proxy APIs. A v4 Proxy API is created using the **Proxy upstream protocol** method.
* `{#message.attributes}`: Contains attributes associated with v4 Message APIs. These APIs are created using the **Introspect messages from event-driven backend** method.

See the v4 API creation wizard for more details.
{% endtab %}

{% tab title="Operators" %}
EL supports various operators, such as arithmetic, logical, comparison, and ternary operators. Examples of commonly used operators in Gravitee include:

* Arithmetic operators: `+, -, *, /`
* Logical operators: `&& (logical and), || (logical or), ! (logical not)`
* Comparison operators: `==, !=, <, <=, >, >=`
* Ternary operators: `condition ? expression1 : expression2`
{% endtab %}

{% tab title="Functions" %}
EL provides a variety of built-in functions to manipulate and transform data in expressions. Examples of commonly used functions in Gravitee include:

* String functions: `length(), substring(), replace()`
* `#jsonPath`: Evaluates a `jsonPath` on a specified object. This function invokes `JsonPathUtils.evaluate(…​)`, which delegates to the Jayway JsonPath library. The best way to learn jsonPath syntax is by using the online evaluator.
* `#xpath`: To evaluate an `xpath` on some provided object. For more information regarding XML and XPath, see XML Support - Dealing with XML Payloads in the SpEL documentation.

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

To extract the value of the `price` property for the book with `title` "The Lord of the Rings," you can use the following expression:

`{#jsonPath(#request.content, "$.store.book[?(@.title=='The Lord of the Rings')].price")}`
{% endtab %}

{% tab title="Request/Response body access" %}
You can access the request/response raw content using `{#request.content}` .

However, depending on the content-type, you can have access to specific content.

**JSON content**

{% hint style="warning" %}
If a JSON payload that has duplicate keys, APIM keeps the last key.

To avoid any errors because of duplicate keys, apply the JSON threat protection policy to the API. For more information about the JSON threat protection policy, see [json-threat-protection.md](create-and-configure-apis/apply-policies/policy-reference/json-threat-protection.md "mention").
{% endhint %}

You can access specific attribute of a JSON request/response payload with `{#request.jsonContent.foo.bar}` , where the request body is similar to the following example:

```json
{
  "foo": {
      "bar": "something"
  }
}
```

**XML content**

You can access specific tag of a XML request/response payload with `{#request.xmlContent.foo.bar}` , where the request body is similar to the following example:

```xml
<foo>
  <bar>something</bar>
</foo>
```
{% endtab %}
{% endtabs %}

## JSONPath in policy configuration

JSONPath expressions can be used within policy configurations to extract specific data from structured payloads. This is particularly useful when working with complex JSON structures, such as LLM chat completion messages.

### Use case: AI Semantic Caching policy

The AI Semantic Caching policy uses JSONPath to extract relevant content from incoming requests before generating vector embeddings. When caching LLM chat completions, you typically want to cache based on the user's prompt rather than the entire conversation history.

**Example: Extract the last message content**

For an OpenAI-compatible chat completion request with the following structure:

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "What is the capital of France?"
    }
  ]
}
```

Use the following JSONPath expression to extract only the last message content:

```
{#jsonPath(#request.content, '$.messages[-1:].content')}
```

This expression:
* Targets the `messages` array
* Selects the last element using `[-1:]`
* Extracts the `content` property

**Policy configuration example**

The AI Semantic Caching policy demonstrates advanced EL usage through its configuration options. The policy supports three primary EL-enabled fields:

#### Cache condition expression

The `cacheCondition` field determines whether a response should be cached. The default expression is:

```
{#response.status >= 200 && #response.status < 300}
```

This expression evaluates the HTTP response status to cache only successful responses (2xx status codes). You can customize this condition to implement more complex caching logic based on response properties.

When configuring cache conditions, avoid caching error responses or non-deterministic results. This ensures only successful responses are cached, preventing error propagation and maintaining cache quality.

#### Prompt expression

The `promptExpression` field extracts the content to be vectorized for semantic matching. The default expression is:

```
{#request.content}
```

For structured payloads like LLM chat completions, you can use JSONPath to extract specific content:

```
{#jsonPath(#request.content, '$.messages[-1:].content')}
```

This expression extracts only the last message content from an OpenAI-compatible chat completion request, improving semantic matching accuracy by ensuring that only the relevant content is used for semantic matching. This approach improves cache hit rates and reduces token usage.

#### Metadata parameter expressions

The `parameters` array allows you to attach metadata to cached vectors using EL expressions in the `value` field. These metadata parameters enable scoped caching and filtering. Common patterns include:

* Scope cache per API: `{#context.attributes['api']}`
* Scope cache per plan: `{#context.attributes['plan']}`
* Scope cache per user: `{#context.attributes['user-id']}`

You can combine multiple attributes to create composite cache keys:

```
{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}
```

When handling sensitive information like user identifiers, set `encode: true` to hash the value using MurmurHash3 (Base64 encoded):

```json
{
  "key": "user_context",
  "value": "{#context.attributes['user-id']}",
  "encode": true
}
```

**Complete configuration example**

```json
{
  "name": "AI Semantic Caching",
  "policy": "ai-semantic-caching",
  "configuration": {
    "modelName": "ai-model-text-embedding-resource",
    "vectorStoreName": "vector-store-redis-resource",
    "promptExpression": "{#jsonPath(#request.content, '$.messages[-1:].content')}",
    "cacheCondition": "{#response.status >= 200 && #response.status < 300}",
    "parameters": [
      {
        "key": "retrieval_context_key",
        "value": "{#context.attributes['api']}",
        "encode": true
      }
    ]
  }
}
```

For more information about the AI Semantic Caching policy configuration, see <a data-mention href="ai-semantic-caching-policy.md">ai-semantic-caching-policy.md</a>.

## Expression Language Assistant

### Overview

The Expression Language (EL) Assistant helps you write the EL expression needed for the field. You provide the Assistant with the prompt for the EL that you want, and then the assistant returns the corresponding EL for the prompt.

<figure><img src=".gitbook/assets/anim (1).gif" alt=""><figcaption></figcaption></figure>

### Prerequisites

* Gravitee Cloud account. To register for Gravitee Cloud, go to [Cloud](https://cockpit.gravitee.io/).
* (Self-hosted and Hybrid installations only) Register your installation in Gravitee Cloud. For more information about registering your installation, see Register installations.
* (Self-hosted and Hybrid installations only) Depending on your installation method, add the following configuration:

{% tabs %}
{% tab title="gravitee.yaml" %}
-   Add the following configuration to the root level of your `gravitee.yaml` file:

    ```yaml
    newtai:
      elgen:
        enabled: true
    ```
{% endtab %}

{% tab title=".env" %}
* Add the following line to your `.env` file:

```
gravitee_newtai_elgen_enabled=true
```
{% endtab %}

{% tab title="values.yaml" %}
*   Add the following configuration to your `values.yaml` file:

    ```yaml
    newtai:
      elgen:
        enabled: true
    ```
{% endtab %}
{% endtabs %}

### Generate Expression Language with the EL assistant

{% hint style="info" %}
Any field that supports Expression Language, supports the AI assistant.
{% endhint %}

1.  In the field that supports expression language, click the **{EL}** icon.

    <figure><img src=".gitbook/assets/304A887B-9FD1-4011-961A-7DB7D91D3478_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
2. In the **EL Assistant** pop-up window, type the prompt for the Expression Language that you want the AI assistant to generate. For example, only run this policy if the header equals test.
3.  Click **Ask Newt AI**. The AI assistant generates the Expression Language.

    <figure><img src=".gitbook/assets/DBE0A0C1-3171-4CA4-A586-A503EBD2B0BD_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
4.  (Optional) Provide feedback about the answer. To provide feedback, click either the **thumbs u**p or the **thumbs down**.

    <figure><img src=".gitbook/assets/6D6E46F0-AECF-41F9-BE38-53C6EC0EDA38_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

### Use case examples

The following use cases provide you with an understanding of how to use the EL Assistant.

#### Add a condition to a policy flow

To add a condition to a policy flow to only run the policy flow when header equals true, type the following prompt in the EL Assistant pop-up window: Only run this policy flow if the header equals test.

The EL Assistant returns the following Expression language to use in your policy flow:

`{#request.headers['Test_Endpoints_header'][0] == 'test'}`

#### Targeting an endpoint

To add a Target url for your endpoint that targets `https://jsonplaceholder.typicode.com/` , type the following prompt in the EL Assistant pop-up window: The target URL must target the following URL: https://jsonplaceholder.typicode.com/.

The EL assistant returns the following response:

`{#context.attributes['https://jsonplaceholder.typicode.com']}`

#### Add an assertion for API Health checks

To add an assertion that only checks the HTTP response, 200, type the following prompt in the EL Assistant pop-up window: Check only the status of the following HTTP response that equals 200

The EL Assistant returns the following response:

`{#response.status == 200}`

## APIs

Using EL, you can access information about an API transaction through several root-level objects that are injected into the EL context: custom properties, dictionaries, and endpoints.

{% tabs %}
{% tab title="Custom properties" %}
As an API publisher, you can define custom properties for your API. These properties are automatically injected into the expression language context and can be referenced during an API transaction from the `{#api.properties}` root-level object property.

**Examples**

* Get the value of the property `my-property` defined in an API's custom properties using `{#api.properties['my-property']}`
* Get the value of the property `my-secret` defined and encrypted in an API's custom properties using `{#api.properties['my-secret']}` to pass a secured property to your backend

{% hint style="info" %}
**Encrypted custom properties**

When accessing an encrypted custom property, Gravitee's Gateway will automatically manage the decryption and provide a plain text value.
{% endhint %}
{% endtab %}

{% tab title="Dictionaries" %}
Dictionaries work similarly to custom properties, but you need to specify the dictionary ID as well as the dictionary property name. Dictionary properties are simply key-value pairs that can be accessed from the `{#dictionaries}` root-level object property.

**Example**

Get the value of the dictionary property `dict-key` defined in dictionary `my-dictionary-id` using `{#dictionaries['my-dictionary-id']['dict-key']}`.
{% endtab %}

{% tab title="Endpoints" %}
When you define endpoints for your API, you need to give them a name that is a unique identifier across all endpoints of the API. This identifier can be used to get an endpoint reference (i.e., a URI) from the `{#endpoints}` root-level object property.

**Example**

When you create an API, a default endpoint is created that corresponds to the value you set for the backend property. This endpoint can be retrieved with EL by using the following syntax: `{#endpoints['default']}`.
{% endtab %}
{% endtabs %}

## Request <a href="#request" id="request"></a>

EL can be used to access request properties and attributes as described below.

### Request object properties

The object properties you can access from the `{#request}` root-level object property and use for API requests are listed below.

{% tabs %}
{% tab title="Table" %}
| Object Property | Description | Type | Example |
| --- | --- | --- | --- |
| content | Body content | string | - |
| contextPath | Context path | string | /v2/ |
| headers | Headers | key / value | X-Custom → myvalue |
| host | The host of the request. This is preferable to using the Host header of the request because HTTP2 requests do not provide this header. | string | gravitee.example.com |
| id | Identifier | string | 12345678-90ab-cdef-1234-567890ab |
| localAddress | Local address | string | 0:0:0:0:0:0:0:1 |
| method | HTTP method | string | GET |
| params | Query parameters | key / value | order → 100 |
| path | Path | string | /v2/store/MyStore |
| pathInfo | Path info | string | /store/MyStore |
| pathInfos | Path info parts | array of strings | [,store,MyStore] |
| pathParams | Path parameters | key / value | storeId → MyStore (*see Warning for details*) |
| pathParamsRaw | Path parameters | string | /something/:id/\*\* |
| paths | Path parts | array of strings | [,v2,store,MyStore] |
| remoteAddress | Remote address | string | 0:0:0:0:0:0:0:1 |
| scheme | The scheme of the request (either `http` or `https`) | string | http |
| ssl | SSL session information | SSL object | - |
| timestamp | Timestamp | long | 1602781000267 |
| transactionId | Transaction identifier | string | cd123456-7890-abcd-ef12-34567890 |
| uri | URI | string | /v2/store/MyStore?order=100 |
| version | HTTP version | string | HTTP_1_1 |
{% endtab %}

{% tab title="Examples" %}
* Get the value of the `Content-Type` header for an incoming HTTP request using `{#request.headers['content-type']}`
* Get the second part of the request path using `{#request.paths[1]}`
{% endtab %}
{% endtabs %}

{% hint style="info" %}
`{#request.content}` is only available for policies bound to an `on-request-content` phase.
{% endhint %}

### Request context attributes

When APIM Gateway handles an incoming API request, some object properties are automatically created or added during the execution phase through the Assign Attributes policy. These object properties are known as attributes. Attributes can be accessed from the `{#context.attributes}` root-level object property.

Some policies (e.g., the OAuth2 policy) register other attributes in the request context. For more information, refer to the documentation for individual policies.

Request context attributes and examples are listed below.

{% tabs %}
{% tab title="Table" %}
| Object Property | Description | Type | Nullable |
| --- | --- | --- | --- |
| api | Called API | string | - |
| api-key | The API key used (for an API Key plan) | string | X (for no API Key plan) |
| application | The authenticated application making incoming HTTP requests | string | X (for Keyless plan) |
| context-path | Context path | string | - |
| plan | Plan used to manage incoming HTTP requests | string | - |
| resolved-path | The path defined in policies | string | - |
| user-id | The user identifier of an incoming HTTP request:<br>* The subscription ID for an API Key plan<br>* The remote IP for a Keyless plan | string | - |
{% endtab %}

{% tab title="Examples" %}
* Get the value of the `user-id` attribute for an incoming HTTP request using `{#context.attributes['user-id']}`
* Get the value of the `plan` attribute for an incoming HTTP request using `{#context.attributes['plan']}`
{% endtab %}
{% endtabs %}

### SSL object properties <a href="#ssl_object" id="ssl_object"></a>

The object properties you can access in the `ssl` session object from the `{#request.ssl}` root-level object property are listed below.

{% tabs %}
{% tab title="Table" %}
| Object Property | Description | Type | Example |
| --- | --- | --- | --- |
| clientHost | Host name of the client | string | client.domain.com |
| clientPort | Port number of the client | long | 443 |
| client | Client information | Principal object | - |
| server | Server information | Principal object | - |
{% endtab %}

{% tab title="Example" %}
Get the client HOST from the SSL session using `{#request.ssl.clientHost}`
{% endtab %}
{% endtabs %}

#### Principal objects <a href="#principal_object" id="principal_object"></a>

The `client` and `server` objects are of type `Principal`. A `Principal` object represents the currently authenticated user who is making the request to the API and provides access to various user attributes such as username, email address, roles, and permissions.

The `Principal` object is typically used with security policies such as OAuth2, JWT, or basic authentication to enforce access control and authorization rules on incoming requests. For example, a policy can check if the current user has a specific role or permission before allowing them to access a protected resource.

If the `Principal` object is not defined, `client` and `server` object values are empty. Otherwise, there are domain name attributes you can access from the `{#request.ssl.client}` and `{#request.ssl.server}` `Principal` objects as shown in the table below:

{% hint style="warning" %}
**Limitation on arrays**

All attributes of the `Principal`object are flattened to be accessed directly with dot or bracket notation. While some of these attributes can be arrays, EL will only return the first item in the array. To retrieve all values of an attribute, use the `attributes` object property shown in the table and examples below.
{% endhint %}

{% tabs %}
{% tab title="Table" %}
| Object Property | Description | Type | Example |
| --- | --- | --- | --- |
| attributes | Retrieves all the `Principal` object's domain name attributes | key / value | "ou" → ["Test team", "Dev team"] |
| businessCategory | Business category | string | - |
| c | Country code | string | FR |
| cn | Common name | string | - |
| countryOfCitizenship | RFC 3039 CountryOfCitizenship | string | - |
| countryOfResidence | RFC 3039 CountryOfResidence | string | - |
| dateOfBirth | RFC 3039 RFC 3039 DateOfBirth | string | 19830719000000Z |
| dc | Domain component | string | - |
| defined | Returns `true` if the `Principal` object is defined and contains values. Returns `false` otherwise. | boolean | - |
| description | Description | string | - |
| dmdName | RFC 2256 directory management domain | string | - |
| dn | Fully qualified domain name | string | - |
| dnQualifier | Domain name qualifier | string | - |
| e | Email address in Verisign certificates | string | - |
| emailAddress | Email address (RSA PKCS#9 extension) | string | - |
| gender | RFC 3039 Gender | string | "M", "F", "m" or "f" |
| generation | Naming attributes of type X520name | string | - |
| givenname | Naming attributes of type X520name | string | - |
| initials | Naming attributes of type X520name | string | - |
| l | Locality name | string | - |
| name | Name | string | - |
| nameAtBirth | ISIS-MTT NameAtBirth | string | - |
| o | Organization | string | - |
| organizationIdentifier | Organization identifier | string | - |
| ou | Organization unit name | string | - |
| placeOfBirth | RFC 3039 PlaceOfBirth | string | - |
| postalAddress | RFC 3039 PostalAddress | string | - |
| postalCode | Postal code | string | - |
| pseudonym | RFC 3039 Pseudonym | string | - |
| role | Role | string | - |
| serialnumber | Device serial number name | string | - |
| st | State or province name | string | - |
| street | Street | string | - |
| surname | Naming attributes of type X520name | string | - |
| t | Title | string | - |
| telephoneNumber | Telephone number | string | - |
| uid | LDAP User id | string | - |
| uniqueIdentifier | Naming attributes of type X520name | string | - |
| unstructuredAddress | Unstructured address (from PKCS#9) | string | - |
{% endtab %}

{% tab title="Examples" %}
**Standard Object Properties**

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

The object properties you can access for API responses from the `{#response}` root-level object property are listed below.

{% tabs %}
{% tab title="Table" %}
| Object Property | Description | Type | Example |
| --- | --- | --- | --- |
| content | Body content | string | - |
| headers | Headers | key / value | X-Custom → myvalue |
| status | Status of the HTTP response | int | 200 |
{% endtab %}

{% tab title="Example" %}
Get the status of an HTTP response: `{#response.status}`
{% endtab %}
{% endtabs %}

## Message

The object properties you can access for API messages from the `{#message}` root-level object property are listed below. A message (either sent or received) may also contain attributes that can be retrieved via `{#message.attributes[key]}`.

{% hint style="info" %}
The EL used for a message does not change based on phase. EL is executed on the message itself, so whether the message is sent in the subscribe or publish phase is irrelevant.
{% endhint %}

{% tabs %}
{% tab title="Table" %}
| Object Property | Description | Type | Example |
| --- | --- | --- | --- |
| attributeNames | The names of the attributes | list / array | - |
| attributes | Attributes attached to the message | key / value | - |
| content | Content of the message | string | - |
| contentLength | Size of the content | integer | - |
| error | Flag regarding the error state of the message | boolean | - |
| headers | Headers attached to the message | key / value | - |
| id | ID of the message | string | - |
| metadata | Metadata attached to the message | key / value | - |
{% endtab %}

{% tab title="Examples" %}
* Get the value of the `Content-Type` header for a message using `{#message.headers['content-type']}`
* Get the size of a message using `{#message.contentLength}`
{% endtab %}
{% endtabs %}

## Nodes

A node is a component that represents an instance of the Gravitee Gateway. Each node runs a copy of the Gateway that is responsible for handling incoming requests, executing policies, and forwarding requests to the appropriate upstream services. The object properties you can access for nodes from the `{#node}` root-level object property are listed below.

{% tabs %}
{% tab title="Table" %}
| Object Property | Description | Type | Example |
| --- | --- | --- | --- |
| id | Node ID | string | 975de338-90ff-41ab-9de3-3890ff41ab62 |
| shardingTags | Node sharding tag | array of string | [internal,external] |
| tenant | Node tenant | string | Europe |
| version | Node version | string | 3.14.0 |
| zone | Zone the node is grouped in | string | europe-west-2 |
{% endtab %}

{% tab title="Example" %}
Get the version of a node : `{#node.version}`
{% endtab %}
{% endtabs %}