# Gravitee Expression Language

## Overview

Gravitee Expression Language (EL) is used to query and manipulate object graphs and dynamically configure various aspects and policies of an API. It allows you to reference values from the current API transaction to use expressions to create dynamic filters, routing rules, and policies that respond to specific conditions or parameters.

EL is an extended version of the [Spring Expression Language](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#expressions) (SpEL) that augments standard SpEL capabilities by providing additional object properties inside the expression language context. As an extension of SpEL, all capabilities detailed in the [SpEL documentation ](https://docs.spring.io/spring-framework/reference/core/expressions.html)are available in EL. However, Gravitee has implemented customizations that are detailed below.

{% hint style="info" %}
**Object properties**

Custom properties and attributes have special meanings in the Gravitee ecosystem:

* **Custom Properties:** Defined at the API level and read-only during the Gateway's execution of an API transaction. You can learn more about how to set an API's custom properties [here](gravitee-expression-language.md#custom-properties).
* **Attributes:** Scoped to the current API transaction and can be manipulated during the execution phase through the `assign-attributes` policy. Attributes are used to attach additional information to a request or message via a variable that is dropped after the API transaction is completed.
{% endhint %}

The following sections define the scope and usage of EL:

* [Basic usage](gravitee-expression-language.md#basic-usage)
* [APIs](gravitee-expression-language.md#apis)
* [Request](gravitee-expression-language.md#request)
* [Response](gravitee-expression-language.md#response)
* [Message](gravitee-expression-language.md#message)
* [Nodes](gravitee-expression-language.md#nodes)
* [Mixin](gravitee-expression-language.md#mixin)
* [Policies](gravitee-expression-language.md#policies)
* [Conditions](gravitee-expression-language.md#conditions)
* [Debugging](gravitee-expression-language.md#debugging)

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
The `attributes` object property contains attributes that are automatically created by the APIM Gateway during an API transaction or added during the execution phase through the [Assign Attributes policy](broken-reference/). However, attributes fall into one of two categories based on API type:

* `{#context.attributes}`: Contains attributes associated with v2 APIs or v4 Proxy APIs. A v4 Proxy API is created using the **Proxy upstream protocol** method.
* `{#message.attributes}`: Contains attributes associated with v4 Message APIs. These APIs are created using the **Introspect messages from event-driven backend** method.

See the [v4 API creation wizard](../create-apis/v4-api-creation-wizard.md) for more details.
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
* `#jsonPath`: Evaluates a `jsonPath` on a specified object. This function invokes `JsonPathUtils.evaluate(…​)`, which delegates to the [Jayway JsonPath library](https://github.com/json-path/JsonPath). The best way to learn jsonPath syntax is by using the [online evaluator](https://jsonpath.com/).
* `#xpath`: To evaluate an `xpath` on some provided object. For more information regarding XML and XPath, see [XML Support - Dealing with XML Payloads](https://docs.spring.io/spring-integration/reference/html/xml.html#xml) in the SpEL documentation.

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
{% endtabs %}

## APIs

Using EL, you can access information about an API transaction through several root-level objects that are injected into the EL context: custom properties, dictionaries, and endpoints.

{% tabs %}
{% tab title="Custom properties" %}
As an API publisher, you can define [custom properties ](gravitee-expression-language.md#custom-properties)for your API. These properties are automatically injected into the expression language context and can be referenced during an API transaction from the `{#api.properties}` root-level object property.

**Examples**

* Get the value of the property `my-property` defined in an API's custom properties using `{#api.properties['my-property']}`
* Get the value of the property `my-secret` defined and encrypted in an API's custom properties using `{#api.properties['my-secret']}` to pass a secured property to your backend

{% hint style="info" %}
**Encrypted custom properties**

When accessing an encrypted custom property, Gravitee's Gateway will automatically manage the decryption and provide a plain text value.
{% endhint %}
{% endtab %}

{% tab title="Dictionaries" %}
[Dictionaries](https://docs.gravitee.io/apim/3.x/apim_installguide_configuration_dictionaries.html) work similarly to custom properties, but you need to specify the dictionary ID as well as the dictionary property name. Dictionary properties are simply key-value pairs that can be accessed from the `{#dictionaries}` root-level object property.

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
<table><thead><tr><th width="172">Object Property</th><th width="157">Description</th><th width="134">Type</th><th>Example</th></tr></thead><tbody><tr><td><a data-footnote-ref href="#user-content-fn-1">content</a></td><td>Body content</td><td>string</td><td>-</td></tr><tr><td>contextPath</td><td>Context path</td><td>string</td><td>/v2/</td></tr><tr><td>headers</td><td>Headers</td><td>key / value</td><td>X-Custom → myvalue</td></tr><tr><td>host</td><td>The host of the request. This is preferable to using the Host header of the request because HTTP2 requests do not provide this header.</td><td>string</td><td>gravitee.example.com</td></tr><tr><td>id</td><td>Identifier</td><td>string</td><td>12345678-90ab-cdef-1234-567890ab</td></tr><tr><td>localAddress</td><td>Local address</td><td>string</td><td>0:0:0:0:0:0:0:1</td></tr><tr><td>method</td><td>HTTP method</td><td>string</td><td>GET</td></tr><tr><td>params</td><td>Query parameters</td><td>key / value</td><td>order → 100</td></tr><tr><td>path</td><td>Path</td><td>string</td><td>/v2/store/MyStore</td></tr><tr><td>pathInfo</td><td>Path info</td><td>string</td><td>/store/MyStore</td></tr><tr><td>pathInfos</td><td>Path info parts</td><td>array of strings</td><td>[,store,MyStore]</td></tr><tr><td>pathParams</td><td>Path parameters</td><td>key / value</td><td>storeId → MyStore (<em>see Warning for details</em>)</td></tr><tr><td>pathParamsRaw</td><td>Path parameters</td><td>string</td><td>/something/:id/**</td></tr><tr><td>paths</td><td>Path parts</td><td>array of strings</td><td>[,v2,store,MyStore]</td></tr><tr><td>remoteAddress</td><td>Remote address</td><td>string</td><td>0:0:0:0:0:0:0:1</td></tr><tr><td>scheme</td><td>The scheme of the request (either <code>http</code> or <code>https</code>)</td><td>string</td><td>http</td></tr><tr><td>host</td><td></td><td>string</td><td></td></tr><tr><td>ssl</td><td>SSL session information</td><td>SSL object</td><td>-</td></tr><tr><td>timestamp</td><td>Timestamp</td><td>long</td><td>1602781000267</td></tr><tr><td>transactionId</td><td>Transaction identifier</td><td>string</td><td>cd123456-7890-abcd-ef12-34567890</td></tr><tr><td>uri</td><td>URI</td><td>string</td><td>/v2/store/MyStore?order=100</td></tr><tr><td>version</td><td>HTTP version</td><td>string</td><td>HTTP_1_1</td></tr></tbody></table>
{% endtab %}

{% tab title="Examples" %}
* Get the value of the `Content-Type` header for an incoming HTTP request using `{#request.headers['content-type']}`
* Get the second part of the request path using `{#request.paths[1]}`
{% endtab %}
{% endtabs %}

### Request context attributes

When APIM Gateway handles an incoming API request, some object properties are automatically created or added during the execution phase through the Assign Attributes policy. These object properties are known as attributes. Attributes can be accessed from the `{#context.attributes}` root-level object property.

Some policies (e.g., the OAuth2 policy) register other attributes in the request context. For more information, refer to the documentation for individual policies.

Request context attributes and examples are listed below.

{% tabs %}
{% tab title="Table" %}
<table><thead><tr><th width="170">Object Property</th><th width="190">Description</th><th width="104">Type</th><th>Nullable</th></tr></thead><tbody><tr><td>api</td><td>Called API</td><td>string</td><td>-</td></tr><tr><td>api-key</td><td>The API key used (for an API Key plan)</td><td>string</td><td>X (for no API Key plan)</td></tr><tr><td>application</td><td>The authenticated application making incoming HTTP requests</td><td>string</td><td>X (for Keyless plan)</td></tr><tr><td>context-path</td><td>Context path</td><td>string</td><td>-</td></tr><tr><td>plan</td><td>Plan used to manage incoming HTTP requests</td><td>string</td><td>-</td></tr><tr><td>resolved-path</td><td>The path defined in policies</td><td>string</td><td>-</td></tr><tr><td>user-id</td><td><p>The user identifier of an incoming HTTP request:</p><p>* The subscription ID for an API Key plan</p><p>* The remote IP for a Keyless plan</p></td><td>string</td><td>-</td></tr></tbody></table>
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
<table><thead><tr><th width="172">Object Property</th><th width="177">Description</th><th width="169">Type</th><th>Example</th></tr></thead><tbody><tr><td>clientHost</td><td>Host name of the client</td><td>string</td><td>client.domain.com</td></tr><tr><td>clientPort</td><td>Port number of the client</td><td>long</td><td>443</td></tr><tr><td>client</td><td>Client information</td><td>Principal object</td><td>-</td></tr><tr><td>server</td><td>Server information</td><td>Principal object</td><td>-</td></tr></tbody></table>
{% endtab %}

{% tab title="Example" %}
Get the client HOST from the SSL session using `{#request.ssl.clientHost}`
{% endtab %}
{% endtabs %}

#### Principal objects <a href="#principal_object" id="principal_object"></a>

The `client` and `server` objects are of type `Principal`. A `Principal` object represents the currently authenticated user who is making the request to the API and provides access to various user attributes such as username, email address, roles, and permissions.

The `Principal` object is typically used with security policies such as OAuth2, JWT, or basic authentication to enforce access control and authorization rules on incoming requests. For example, a policy can check if the current user has a specific role or permission before allowing them to access a protected resource.

Otherwise, there are domain name attributes you can access from the `{#request.ssl.client}` and `{#request.ssl.server}` `Principal` objects as shown in the table below:

{% hint style="warning" %}
**Limitation on arrays**

All attributes of the `Principal`object are flattened to be accessed directly with dot or bracket notation. While some of these attributes can be arrays, EL will only return the first item in the array. To retrieve all values of an attribute, use the `attributes` object property shown in the table and examples below.
{% endhint %}

{% tabs %}
{% tab title="Table" %}
<table><thead><tr><th width="218">Object Property</th><th width="154">Description</th><th width="102">Type</th><th>Example</th></tr></thead><tbody><tr><td>attributes</td><td>Retrieves all the <code>Principal</code> object's domain name attributes</td><td>key / value</td><td>"ou" → ["Test team", "Dev team"]</td></tr><tr><td>businessCategory</td><td>Business category</td><td>string</td><td>-</td></tr><tr><td>c</td><td>Country code</td><td>string</td><td>FR</td></tr><tr><td>cn</td><td>Common name</td><td>string</td><td>-</td></tr><tr><td>countryOfCitizenship</td><td>RFC 3039 CountryOfCitizenship</td><td>string</td><td>-</td></tr><tr><td>countryOfResidence</td><td>RFC 3039 CountryOfResidence</td><td>string</td><td>-</td></tr><tr><td>dateOfBirth</td><td>RFC 3039 RFC 3039 DateOfBirth</td><td>string</td><td>19830719000000Z</td></tr><tr><td>dc</td><td>Domain component</td><td>string</td><td>-</td></tr><tr><td>defined</td><td><p>Returns <code>true</code> if the <code>Principal</code> object is defined and contains values.</p><p><strong>Standard Object Properties</strong></p><ul><li>Get the client DN from the SSL session: <code>{#request.ssl.client.dn}</code></li><li>Get the server organization from the SSL session: <code>{#request.ssl.server.o}</code></li></ul><p><strong>Arrays and boolean logic</strong></p><ul><li><p>Get all the organization units of the server from the SSL session:</p><ul><li><code>{#request.ssl.server.attributes['ou'][0]}</code></li><li><code>{#request.ssl.server.attributes['OU'][1]}</code></li><li><code>{#request.ssl.server.attributes['Ou'][2]}</code></li></ul></li><li>Get a custom attribute of the client from the SSL session: <code>{#request.ssl.client.attributes['1.2.3.4'][0]}</code></li><li>Determine if the SSL attributes of the client are set: <code>{#request.ssl.client.defined}</code></li></ul><h3>Response</h3><p>The object properties you can access for API responses from the <code>{#response}</code> root-level object property are listed below.</p><div data-gb-custom-block data-tag="tabs"><div data-gb-custom-block data-tag="tab" data-title="Table"><table><thead><tr><th width="172">Object Property</th><th>Description</th><th width="125">Type</th><th>Example</th></tr></thead><tbody><tr><td>content</td><td>Body content</td><td>string</td><td>-</td></tr><tr><td>headers</td><td>Headers</td><td>key / value</td><td>X-Custom → myvalue</td></tr><tr><td>status</td><td>Status of the HTTP response</td><td>int</td><td>200</td></tr></tbody></table></div><div data-gb-custom-block data-tag="tab" data-title="Example"><p>Get the status of an HTTP response: <code>{#response.status}</code></p></div></div><h3>Message</h3><p>The object properties you can access for API messages from the <code>{#message}</code> root-level object property are listed below. A message (either sent or received) may also contain attributes that can be retrieved via <code>{#message.attributes[key]}</code>.</p><div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info"><p>The EL used for a message does not change based on phase. EL is executed on the message itself, so whether the message is sent in the subscribe or publish phase is irrelevant.</p></div><div data-gb-custom-block data-tag="tabs"><div data-gb-custom-block data-tag="tab" data-title="Table"><table><thead><tr><th width="172">Object Property</th><th>Description</th><th width="125">Type</th><th>Example</th></tr></thead><tbody><tr><td>attributeNames</td><td>The names of the attributes</td><td>list / array</td><td>-</td></tr><tr><td>attributes</td><td>Attributes attached to the message</td><td>key / value</td><td>-</td></tr><tr><td>content</td><td>Content of the message</td><td>string</td><td>-</td></tr><tr><td>contentLength</td><td>Size of the content</td><td>integer</td><td>-</td></tr><tr><td>error</td><td>Flag regarding the error state of the message</td><td>boolean</td><td>-</td></tr><tr><td>headers</td><td>Headers attached to the message</td><td>key / value</td><td>-</td></tr><tr><td>id</td><td>ID of the message</td><td>string</td><td>-</td></tr><tr><td>metadata</td><td>Metadata attached to the message</td><td>key / value</td><td>-</td></tr></tbody></table></div><div data-gb-custom-block data-tag="tab" data-title="Examples"><ul><li>Get the value of the <code>Content-Type</code> header for a message using <code>{#message.headers['content-type']}</code></li><li>Get the size of a message using <code>{#message.contentLength}</code></li></ul></div></div><h3>Nodes</h3><p>A node is a component that represents an instance of the Gravitee Gateway. Each node runs a copy of the Gateway that is responsible for handling incoming requests, executing policies, and forwarding requests to the appropriate upstream services. The object properties you can access for nodes from the <code>{#node}</code> root-level object property are listed below.</p><div data-gb-custom-block data-tag="tabs"><div data-gb-custom-block data-tag="tab" data-title="Table"><table><thead><tr><th width="179">Object Property</th><th width="153">Description</th><th width="94">Type</th><th>Example</th></tr></thead><tbody><tr><td>id</td><td>Node ID</td><td>string</td><td>975de338-90ff-41ab-9de3-3890ff41ab62</td></tr><tr><td>shardingTags</td><td>Node sharding tag</td><td>array of string</td><td>[internal,external]</td></tr><tr><td>tenant</td><td>Node tenant</td><td>string</td><td>Europe</td></tr><tr><td>version</td><td>Node version</td><td>string</td><td>3.14.0</td></tr><tr><td>zone</td><td>Zone the node is grouped in</td><td>string</td><td>europe-west-2</td></tr></tbody></table></div><div data-gb-custom-block data-tag="tab" data-title="Example"><p>Get the version of a node : <code>{#node.version}</code></p></div></div><h3>Mixin</h3><p>In previous examples, we showed various ways to manipulate objects available in the EL context. You can also mix root-level object property usage to provide an increasingly dynamic configuration.</p><p>For example, to retrieve the value of an HTTP header where the name is based on an API custom property named <code>my-property</code>, use <code>{#request.headers[#api.properties['my-property']]}</code>.</p><h3>Policies</h3><p>You can use the EL to update some aspects of policy configuration. The policy specifies if it supports EL or not by including a <strong>Condition</strong> section in the Policy Studio configuration.</p><p><img src="../.gitbook/assets/Screenshot 2023-04-03 at 4.58.01 PM.png" alt="Assign attributes policy supports EL conditions" data-size="original"></p><h3>Conditions</h3><p>You can use the EL to set a condition of execution (see 'conditional policies and flows conditions') and it is possible to use logical operators such as <code>&#x26;&#x26;</code> or <code>||</code>, as shown in the example below:</p><p><code>{#request.headers['my-header'] != null &#x26;&#x26; #request.headers['my-header'][0] =="my-value"}</code></p><div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info"><p><strong>Alternate equality check</strong></p><p>You can use the <code>equals()</code> method instead of <code>==</code>. When you use <code>.equals()</code>, it is recommended to put the string first to prevent an error. For example, if <code>#request.headers['my-header']</code> is <code>null</code> , then <code>'my-value'.equals(#request.headers['my-header'])</code>will prevent an error.</p></div><h3>Debugging</h3><p>In case of an error when using EL, an exception will be raised :</p><p><code>The template evaluation returns an error. Expression: {#context.error}</code></p><p>If debugging your expression is difficult, consider the following example for guidance:</p><p>Assume <code>{#request.content.length() >= 10}</code> is the conditional expression on a flow. When testing, you are expecting the condition to evaluate to <code>false</code> and stop the flow from executing, but the flow continues to function unexpectedly. To check the actual output of the <code>#request.content.length()</code> expression, use the Assign Attributes policy as shown in the arcade below.</p></td><td></td><td></td></tr><tr><td>Object Property</td><td>Description</td><td>Type</td><td>Example</td></tr><tr><td>content</td><td>Body content</td><td>string</td><td>-</td></tr><tr><td>headers</td><td>Headers</td><td>key / value</td><td>X-Custom → myvalue</td></tr><tr><td>status</td><td>Status of the HTTP response</td><td>int</td><td>200</td></tr><tr><td>Object Property</td><td>Description</td><td>Type</td><td>Example</td></tr><tr><td>attributeNames</td><td>The names of the attributes</td><td>list / array</td><td>-</td></tr><tr><td>attributes</td><td>Attributes attached to the message</td><td>key / value</td><td>-</td></tr><tr><td>content</td><td>Content of the message</td><td>string</td><td>-</td></tr><tr><td>contentLength</td><td>Size of the content</td><td>integer</td><td>-</td></tr><tr><td>error</td><td>Flag regarding the error state of the message</td><td>boolean</td><td>-</td></tr><tr><td>headers</td><td>Headers attached to the message</td><td>key / value</td><td>-</td></tr><tr><td>id</td><td>ID of the message</td><td>string</td><td>-</td></tr><tr><td>metadata</td><td>Metadata attached to the message</td><td>key / value</td><td>-</td></tr><tr><td>Object Property</td><td>Description</td><td>Type</td><td>Example</td></tr><tr><td>id</td><td>Node ID</td><td>string</td><td>975de338-90ff-41ab-9de3-3890ff41ab62</td></tr><tr><td>shardingTags</td><td>Node sharding tag</td><td>array of string</td><td>[internal,external]</td></tr><tr><td>tenant</td><td>Node tenant</td><td>string</td><td>Europe</td></tr><tr><td>version</td><td>Node version</td><td>string</td><td>3.14.0</td></tr><tr><td>zone</td><td>Zone the node is grouped in</td><td>string</td><td>europe-west-2</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

[^1]: `{#request.content}` is only available for policies bound to an `on-request-content` phase.
