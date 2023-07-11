# Gravitee Expression Language

The Gravitee Expression Language (EL) is a powerful tool that can be used by API publishers to dynamically configure various aspects and policies of an API.

EL is a language used for querying and manipulating an object graph. It is a superset of the [Spring Expression Language](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#expressions) (SpEL) that extends standard SpEL capabilities by providing additional object properties inside the expression language context.

EL allows you to reference values from the current API transaction. This means you can use expressions to create dynamic filters, routing rules, and policies that respond to specific conditions or parameters.

## Basic usage

Since EL is an extension of SpEL, all capabilities detailed in the SpEL documentation are available in EL. This section will focus on detailing the EL's modifications to the SpEL syntax, object properties added to the EL context, and commonly used operators and functions.

### Syntax

Expressions in Gravitee are enclosed in curly braces `{}` and begin with the `#` symbol. Both dot notation and bracket notation are supported for accessing the properties of an object: `{#context.attributes['user'].email}`

{% hint style="info" %}
**Dot notation vs bracket notation**

Please note that dot notation will not work with special characters:

`{#request.headers.my-header}` <- **This will result in an error**

therefore, bracket notation should be used for property names that have a space or a hyphen, or start with a number:

`{#request.headers['my-header']}`
{% endhint %}

### Object properties

EL allows you to reference certain values injected into the EL context as object properties. The available object properties will be further detailed in the following sections. EL adds the following root-level object properties:

* `{#properties}` : Contains custom properties defined by the API publisher for that gateway API.
* `{#dictionaries}` : Contains custom dictionaries defined by the API publisher for that gateway API.
* `{#endpoints}` : Contains information about the gateway API's respective endpoint.
* `{#request}` : Contains information about the current API request.
* `{#response}` : Contains information about the current API response.
* `{#context.attributes}` : Contains attributes automatically created by the APIM gateway during an API transaction or added during the execution phase through the [assign-attributes policy](https://docs.gravitee.io/apim/3.x/apim\_policies\_assign\_attributes.html).
* `{#node}` : Contains information about the node hosting the instance of the gateway handling the API transaction.

{% hint style="info" %}
**Object properties: custom properties vs attributes**

* **Custom Properties:** defined at the API level and are read-only during the gateway's execution of an API transaction. You can learn more about how to set an API's custom properties [here](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_api\_properties.html).
* **Attributes:** scoped to the current API transaction, and can be manipulated during the execution phase through the`assign-attributes` policy. You can view attributes like a kind of variable that is dropped after the API transaction is completed.

Please keep in mind both custom properties and attributes are still _object properties._ Object properties are simply variables that belong to an object. They are part of an object's structure and can be accessed using dot notation or bracket notation.

On the other hand, custom properties and attributes are terms that have special meaning in the Gravitee ecosystem as defined above. They can both be accessed through their associated, root-level object property.
{% endhint %}

### Operators

EL supports various operators, such as arithmetic, logical, comparison, and ternary operators. Here are some examples of commonly used operators in Gravitee:

* Arithmetic Operators: `+, -, *, /`
* Logical Operators: `&& (logical and), || (logical or), ! (logical not)`
* Comparison Operators: `==, !=, <, <=, >, >=`
* Ternary Operator: `condition ? expression1 : expression2`

### Functions

EL provides a variety of built-in functions that you can use to manipulate and transform data in your expressions. Some examples of commonly used functions in Gravitee include:

* string functions: `length(), substring(), replace()`
* `#jsonPath`: Evaluates a `jsonPath` on a specified object. This function invokes `JsonPathUtils.evaluate(…​)`, which delegates to the [Jayway JsonPath library](https://github.com/json-path/JsonPath). The best way to learn the jsonPath syntax is to use the [online evaluator](https://jsonpath.com/). JsonPath can be used with EL as in the following example:

Suppose you have a JSON payload in the request body that contains the following data:

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

To extract the value of the `price` property for the book with `title` "The Lord of the Rings", you can use the following expression:

`{#jsonPath(#request.content, "$.store.book[?(@.title=='The Lord of the Rings')].price")}`

* `#xpath`: To evaluate an `xpath` on some provided object. For more information regarding XML and XPath, see [XML Support - Dealing with XML Payloads](https://docs.spring.io/spring-integration/reference/html/xml.html#xml) from the SpEL documentation.

## APIs

Using EL, you can access information about a gateway API through several root-level objects that are injected into the EL context.

### Custom Properties

As an API publisher, you can define custom [properties](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_api\_properties.html) for your API. These properties are automatically injected into the expression language context and can be referenced during an API transaction from the `{#properties}` root-level object property.

#### **Examples**

* Get the value of the property `my-property` defined in an API's custom properties: `{#properties['my-property']}`
* Get the value of the property `my-secret` defined and [encrypted](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_api\_properties.html) in an API's custom properties : `{#properties['my-secret']}` to pass a secured property to your backend

{% hint style="info" %}
**Encrypted custom properties**

When accessing an encrypted custom property, Gravitee's gateway will automatically manage the decryption and provide a plaintext value.
{% endhint %}

### Dictionaries

[Dictionaries](https://docs.gravitee.io/apim/3.x/apim\_installguide\_configuration\_dictionaries.html) work similarly to custom properties, but you need to specify the dictionary id as well as the dictionary property name. Dictionary properties are simply key-value pairs that can be accessed from the `{#dictionaries}` root-level object property.

#### **Example**

* Get the value of the dictionary property `dict-key` defined in dictionary `my-dictionary-id`: `{#dictionaries['my-dictionary-id']['dict-key']}`

### Endpoints

When you define endpoints for your API, you need to give them a name which must be a unique identifier across all endpoints of the API. This identifier can be used to get an endpoint reference (i.e. URI) from the `{#endpoints}` root-level object property.

#### Example

* When you create an API, a default endpoint is created, corresponding to the value you set for the backend property. This endpoint can be retrieved with EL by using the following syntax: `{#endpoints['default']}`

## Request <a href="#request" id="request"></a>

The object properties you can access for API requests from the `{#request}` root-level object property are listed below:

| Object Property | Description            | Type                            | Example                                       |
| --------------- | ---------------------- | ------------------------------- | --------------------------------------------- |
| id              | Identifier             | string                          | 12345678-90ab-cdef-1234-567890ab              |
| transactionId   | Transaction identifier | string                          | cd123456-7890-abcd-ef12-34567890              |
| uri             | URI                    | string                          | /v2/store/MyStore?order=100                   |
| path            | Path                   | string                          | /v2/store/MyStore                             |
| paths           | Path parts             | array of string                 | \[,v2,store,MyStore]                          |
| pathInfo        | Path info              | string                          | /store/MyStore                                |
| pathInfos       | Path info parts        | array of string                 | \[,store,MyStore]                             |
| contextPath     | Context path           | string                          | /v2/                                          |
| params          | Query parameters       | key / value                     | order → 100                                   |
| pathParams      | Path parameters        | key / value                     | storeId → MyStore (_see Warning for details_) |
| headers         | Headers                | key / value                     | X-Custom → myvalue                            |
| method          | HTTP method            | string                          | GET                                           |
| scheme          | HTTP scheme            | string                          | http                                          |
| version         | HTTP version           | string                          | HTTP\_1\_1                                    |
| timestamp       | Timestamp              | long                            | 1602781000267                                 |
| remoteAddress   | Remote address         | string                          | 0:0:0:0:0:0:0:1                               |
| localAddress    | Local address          | string                          | 0:0:0:0:0:0:0:1                               |
| content[^1]     | Body content           | string                          | -                                             |
| ssl             | SSLSession information | [SSL Object](broken-reference/) | -                                             |

#### Examples

* Get the value of the `Content-Type` header for an incoming HTTP request: `{#request.headers['content-type']}`
* Get the second part of the request path: `{#request.paths[1]}`

### Request context attributes

When APIM Gateway handles an incoming API request, some object properties are automatically created or added during the execution phase through the [assign-attributes policy](https://docs.gravitee.io/apim/3.x/apim\_policies\_assign\_attributes.html). These object properties are known as attributes. Attributes can be accessed from the `{#context.attributes}` root-level object property. Available attributes are listed below:

| Object Property | Description                                                                                                                                      | Type   | Nullable                |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------ | ----------------------- |
| context-path    | Context-path                                                                                                                                     | string | -                       |
| resolved-path   | Resolved-path is the path defined in policies                                                                                                    | string | -                       |
| application     | The authenticated application doing incoming HTTP request                                                                                        | string | X (for keyless plan)    |
| api             | Called API                                                                                                                                       | string | -                       |
| user-id         | <p>The user identifier of incoming HTTP request:</p><p>* The subscription id for api-key based plan</p><p>* Remote IP for keyless based plan</p> | string | -                       |
| plan            | Plan used to manage incoming HTTP request                                                                                                        | string | -                       |
| api-key         | the api-key used (in case of an api-key based plan)                                                                                              | string | X (for no api-key plan) |

Additionally, some policies (like the [OAuth2 policy](https://docs.gravitee.io/apim/3.x/apim\_policies\_oauth2.html#attributes)) register other attributes in the request context. See the documentation for the policies you are using for more information.

#### Examples

* Get the value of the `user-id` attribute for an incoming HTTP request:`{#context.attributes['user-id']}`
* Get the value of the `plan` attribute for an incoming HTTP request:`{#context.attributes['plan']}`

### SSL and principal objects <a href="#ssl_object" id="ssl_object"></a>

The object properties you can access in the `ssl` session object from the `{#request.ssl}` root-level object property are listed below:

| Object Property | Description               | Type                                  | Example           |
| --------------- | ------------------------- | ------------------------------------- | ----------------- |
| clientHost      | Host name of the client   | string                                | client.domain.com |
| clientPort      | Port number of the client | long                                  | 443               |
| client          | Client information        | [Principal Object](broken-reference/) | -                 |
| server          | Server information        | [Principal Object](broken-reference/) | -                 |

#### Example <a href="#principal_object" id="principal_object"></a>

* Get the client HOST from the SSL session: `{#request.ssl.clientHost}`

#### Principal objects <a href="#principal_object" id="principal_object"></a>

A `Principal` object represents the currently authenticated user who is making the request to the API. The `Principal` object provides access to various attributes of the user, such as their username, email address, roles, and permissions. The `Principal` object is typically used with security policies, such as OAuth2, JWT, or basic authentication, to enforce access control and authorization rules on incoming requests. For example, a policy can check if the current user has a specific role or permission before allowing them to access a protected resource.

`client` and `server` are objects of type `Principal`. If the `Principal` object is not defined, all values are empty.

Otherwise, the attributes you can access from the `{#request.ssl.client}` and `{#request.ssl.server}`root-level object properties are listed below:

**Common domain name attributes:**

<table><thead><tr><th>Object Property</th><th>Description</th><th width="126">Type</th><th>Example</th></tr></thead><tbody><tr><td>businessCategory</td><td>Business category</td><td>string</td><td>-</td></tr><tr><td>c</td><td>Country code</td><td>string</td><td>FR</td></tr><tr><td>cn</td><td>Common name</td><td>string</td><td>-</td></tr><tr><td>countryOfCitizenship</td><td>RFC 3039 CountryOfCitizenship</td><td>string</td><td>-</td></tr><tr><td>countryOfResidence</td><td>RFC 3039 CountryOfResidence</td><td>string</td><td>-</td></tr><tr><td>dateOfBirth</td><td>RFC 3039 RFC 3039 DateOfBirth</td><td>string</td><td>19830719000000Z</td></tr><tr><td>dc</td><td>Domain component</td><td>string</td><td>-</td></tr><tr><td>description</td><td>Description</td><td>string</td><td>-</td></tr><tr><td>dmdName</td><td>RFC 2256 directory management domain</td><td>string</td><td>-</td></tr><tr><td>dnQualifier</td><td>Domain name qualifier</td><td>string</td><td>-</td></tr><tr><td>e</td><td>Email address in Verisign certificates</td><td>string</td><td>-</td></tr><tr><td>emailAddress</td><td>Email address (RSA PKCS#9 extension)</td><td>string</td><td>-</td></tr><tr><td>gender</td><td>RFC 3039 Gender</td><td>string</td><td>"M", "F", "m" or "f"</td></tr><tr><td>generation</td><td>Naming attributes of type X520name</td><td>string</td><td>-</td></tr><tr><td>givenname</td><td>Naming attributes of type X520name</td><td>string</td><td>-</td></tr><tr><td>initials</td><td>Naming attributes of type X520name</td><td>string</td><td>-</td></tr><tr><td>l</td><td>Locality name</td><td>string</td><td>-</td></tr><tr><td>name</td><td>Name</td><td>string</td><td>-</td></tr><tr><td>nameAtBirth</td><td>ISIS-MTT NameAtBirth</td><td>string</td><td>-</td></tr><tr><td>o</td><td>Organization</td><td>string</td><td>-</td></tr><tr><td>organizationIdentifier</td><td>Organization identifier</td><td>string</td><td>-</td></tr><tr><td>ou</td><td>Organization unit name</td><td>string</td><td>-</td></tr><tr><td>placeOfBirth</td><td>RFC 3039 PlaceOfBirth</td><td>string</td><td>-</td></tr><tr><td>postalAddress</td><td>RFC 3039 PostalAddress</td><td>string</td><td>-</td></tr><tr><td>postalCode</td><td>Postal code</td><td>string</td><td>-</td></tr><tr><td>pseudonym</td><td>RFC 3039 Pseudonym</td><td>string</td><td>-</td></tr><tr><td>role</td><td>Role</td><td>string</td><td>-</td></tr><tr><td>serialnumber</td><td>Device serial number name</td><td>string</td><td>-</td></tr><tr><td>st</td><td>State or province name</td><td>string</td><td>-</td></tr><tr><td>street</td><td>Street</td><td>string</td><td>-</td></tr><tr><td>surname</td><td>Naming attributes of type X520name</td><td>string</td><td>-</td></tr><tr><td>t</td><td>Title</td><td>string</td><td>-</td></tr><tr><td>telephoneNumber</td><td>Telephone number</td><td>string</td><td>-</td></tr><tr><td>uid</td><td>LDAP User id</td><td>string</td><td>-</td></tr><tr><td>uniqueIdentifier</td><td>Naming attributes of type X520name</td><td>string</td><td>-</td></tr><tr><td>unstructuredAddress</td><td>Unstructured address (from PKCS#9)</td><td>string</td><td>-</td></tr></tbody></table>

{% hint style="info" %}
**Limitation on arrays**

All attributes of the `Principal`object are flattened to be accessed directly with dot or bracket notation. While some of these attributes can be arrays, EL will only return the first item in the array. If you want to retrieve all values of an attribute, you can use the `attributes` object property shown in the table below.
{% endhint %}

**Other attributes:**

| Object Property | Description                                                                              | Type        | Example                           |
| --------------- | ---------------------------------------------------------------------------------------- | ----------- | --------------------------------- |
| attributes      | Retrieves all the `Prinicipal` object's domain name attributes listed in the table above | key / value | "ou" → \["Test team", "Dev team"] |
| defined         | Returns true if the principal object is defined and contains values. False otherwise.    | boolean     | -                                 |
| dn              | Fully qualified domain name                                                              | string      | -                                 |

#### Examples <a href="#examples" id="examples"></a>

* Get the client DN from the SSL session: `{#request.ssl.client.dn}`
* Get the server organization from the SSL session: `{#request.ssl.server.o}`
* Get all the organization units of the server from the SSL session:
  * `{#request.ssl.server.attributes['ou'][0]}`
  * `{#request.ssl.server.attributes['OU'][1]}`
  * `{#request.ssl.server.attributes['Ou'][2]}`
* Get a custom attribute of the client from the SSL session: `{#request.ssl.client.attributes['1.2.3.4'][0]}`
* Determine if the SSL attributes of the client are set: `{#request.ssl.client.defined}`

## Response

The object properties you can access for API responses from the `{#response}` root-level object property are listed below.

| Object Property | Description                 | Type        | Example            |
| --------------- | --------------------------- | ----------- | ------------------ |
| content         | Body content                | string      | -                  |
| headers         | Headers                     | key / value | X-Custom → myvalue |
| status          | Status of the HTTP response | int         | 200                |

#### Example

* Get the status of an HTTP response: `{#response.status}`

## Nodes

A node is a component that represents an instance of the Gravitee gateway. Each node runs a copy of the gateway, which is responsible for handling incoming requests, executing policies, and forwarding requests to the appropriate upstream services. The object properties you can access for nodes from the `{#node}` root-level object property are listed below.

| Property     | Description                 | Type            | Example                              |
| ------------ | --------------------------- | --------------- | ------------------------------------ |
| id           | Node id                     | string          | 975de338-90ff-41ab-9de3-3890ff41ab62 |
| version      | Node version                | string          | 3.14.0                               |
| tenant       | Node tenant                 | string          | Europe                               |
| shardingTags | Node sharding tag           | array of string | \[internal,external]                 |
| zone         | Zone the node is grouped in | string          | europe-west-2                        |

#### Example

* Get the version of a node : `{#node.version}`

## Policies

You can use the EL to update some aspects of policy configuration. The policy specifies if it supports EL or not by including a **Condition** section in the Policy Studio configuration.

<figure><img src="../../.gitbook/assets/Screenshot 2023-04-03 at 4.58.01 PM.png" alt=""><figcaption><p>Assign attributes policy supports EL conditions</p></figcaption></figure>

## Mixin

In previous examples, we showed various ways to manipulate objects available in the EL context. You can also mix root-level object property usage to provide an increasingly dynamic configuration.

For example, we can retrieve the value of an HTTP header where the name is based on an API custom property named `my-property`:

`{#request.headers[#properties['my-property']]}`

## Conditions

You can also use the EL to set a condition of execution (see 'conditional policies and flows conditions') and it is possible to use logical operators such as `&&` or `||`, as shown in the example below:

`{#request.headers['my-header'] != null && #request.headers['my-header'] == "my-value"}`

{% hint style="info" %}
**Alternate equality check**

An alternative method is to use the `equals()` method instead of `==`. When you use `.equals()`, it is recommended to put the string first to prevent an error if `#request.headers['my-header']` is `null` - for example, then `'my-value'.equals(#request.headers['my-header'])`will prevent an error.
{% endhint %}

## Debugging

In case of an error when using Expression Language, an exception will be raised :

`The template evaluation returns an error. Expression: {#context.error}`

If you are having a hard time debugging your expression, here's the best way to proceed. Let's say you have the following conditional expression on a flow:

`{#request.content.length() >= 10}`

When testing, you are expecting the condition to evaluate to `false` and stop the flow from executing, but the flow continues to function unexpectedly. So how do you know the actual output of the `#request.content.length()` expression? You can easily check the output of an expression using the assign-attributes policy as shown in the arcade below:

\{% @arcade/embed flowId="Q5mHqjjdv2gzuuVwLffu" url="https://app.arcade.software/share/Q5mHqjjdv2gzuuVwLffu" %\}

\\

[^1]: `{#request.content}` is only available for policies bound to an `on-request-content` phase.
