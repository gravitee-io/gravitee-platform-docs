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
* `{#context.attributes}` : Contains attributes automatically created by the APIM gateway during an API transaction.

{% hint style="info" %}
**Object properties: custom properties vs attributes**

* **Custom Properties:** defined at the API level and are read-only during the gateway's execution of an API transaction. You can learn more about how to set an API's custom properties [here](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_api\_properties.html).
* **Attributes:** scoped to the current API transaction, and can be manipulated during the execution phase through the [`assign-attributes` policy](https://docs.gravitee.io/apim/3.x/apim\_policies\_assign\_attributes.html). You can view attributes like a kind of variable that is dropped after the API transaction is completed.

Please keep in mind both custom properties and attributes are still _object properties._ Object properties are simply variables that belong to an object. They are part of an object's structure and can be accessed and modified using dot notation or bracket notation.

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

As an API publisher, you can define custom [properties](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_api\_properties.html) for your API. These properties are automatically injected into the expression language context and can be referenced during an API transaction.

#### **Examples**

* Get the value of the property `my-property` defined in an API's custom properties: `{#properties['my-property']}`
* Get the value of the property `my-secret` defined and [encrypted](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_api\_properties.html) in an API's Properties : `{#properties['my-secret'}` to pass a secured property to your backend

### Dictionaries

[Dictionaries](https://docs.gravitee.io/apim/3.x/apim\_installguide\_configuration\_dictionaries.html) work similarly to custom properties, but you need to specify the dictionary id (visible in the URL) as well as the dictionary property name. Dictionary properties are simply key-value pairs.

#### **Example**

* Get the value of the dictionary property `dict-key` defined in dictionary `my-dictionary`: `{#dictionaries['my-dictionary']['dict-key']}`

### Endpoints

When you define endpoints for your API, you need to give them a name which must be a unique identifier across all endpoints of the API. This identifier can be used to get an endpoint reference (i.e. URI).

#### Example

* When you create an API, a default endpoint is created, corresponding to the value you set for the backend property. This endpoint can be retrieved with EL by using the following syntax: `{#endpoints['default']}`

## Request  <a href="#request" id="request"></a>

The object properties you can access for API requests are listed below.

| Object Property | Description            | Type                           | Example                                       |
| --------------- | ---------------------- | ------------------------------ | --------------------------------------------- |
| id              | Identifier             | string                         | 12345678-90ab-cdef-1234-567890ab              |
| transactionId   | Transaction identifier | string                         | cd123456-7890-abcd-ef12-34567890              |
| uri             | URI                    | string                         | /v2/store/MyStore?order=100                   |
| path            | Path                   | string                         | /v2/store/MyStore                             |
| paths           | Path parts             | array of string                | \[,v2,store,MyStore]                          |
| pathInfo        | Path info              | string                         | /store/MyStore                                |
| pathInfos       | Path info parts        | array of string                | \[,store,MyStore]                             |
| contextPath     | Context path           | string                         | /v2/                                          |
| params          | Query parameters       | key / value                    | order → 100                                   |
| pathParams      | Path parameters        | key / value                    | storeId → MyStore (_see Warning for details_) |
| headers         | Headers                | key / value                    | X-Custom → myvalue                            |
| method          | HTTP method            | string                         | GET                                           |
| scheme          | HTTP scheme            | string                         | http                                          |
| version         | HTTP version           | string                         | HTTP\_1\_1                                    |
| timestamp       | Timestamp              | long                           | 1602781000267                                 |
| remoteAddress   | Remote address         | string                         | 0:0:0:0:0:0:0:1                               |
| localAddress    | Local address          | string                         | 0:0:0:0:0:0:0:1                               |
| content[^1]     | Body content           | string                         | -                                             |
| ssl             | SSLSession information | [SSL Object](broken-reference) | -                                             |

### Request context attributes

When APIM Gateway handles an incoming API request, some object properties are automatically created which are known as attributes. These attributes can be accessed from `{#request.context}` the object property. Available attributes are listed below:

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

The object properties you can access in `ssl` session object are listed below

| Object Property | Description               | Type                                 | Example           |
| --------------- | ------------------------- | ------------------------------------ | ----------------- |
| clientHost      | Host name of the client   | string                               | client.domain.com |
| clientPort      | Port number of the client | long                                 | 443               |
| client          | Client information        | [Principal Object](broken-reference) | -                 |
| server          | Server information        | [Principal Object](broken-reference) | -                 |

#### Principal object <a href="#principal_object" id="principal_object"></a>

A `Principal` object represents the currently authenticated user who is making the request to the API. The `Principal` object provides access to various attributes of the user, such as their username, email address, roles, and permissions. The `Principal` object is typically used in conjunction with security policies, such as OAuth2, JWT, or basic authentication, to enforce access control and authorization rules on incoming requests. For example, a policy can check if the current user has a specific role or permission before allowing them to access a protected resource.

`client` and `server` are objects of type `Principal` and have a number of attributes you can access in the EL context.

**Common domain name attributes:**

| Object Property        | Description                            | Type   | Example              |
| ---------------------- | -------------------------------------- | ------ | -------------------- |
| businessCategory       | Business category                      | string | -                    |
| c                      | Country code                           | string | FR                   |
| cn                     | Common name                            | string | -                    |
| countryOfCitizenship   | RFC 3039 CountryOfCitizenship          | string | -                    |
| countryOfResidence     | RFC 3039 CountryOfResidence            | string | -                    |
| dateOfBirth            | RFC 3039 RFC 3039 DateOfBirth          | string | 19830719000000Z      |
| dc                     | Domain component                       | string | -                    |
| description            | Description                            | string | -                    |
| dmdName                | RFC 2256 directory management domain   | string | -                    |
| dnQualifier            | Domain name qualifier                  | string | -                    |
| e                      | Email address in Verisign certificates | string | -                    |
| emailAddress           | Email address (RSA PKCS#9 extension)   | string | -                    |
| gender                 | RFC 3039 Gender                        | string | "M", "F", "m" or "f" |
| generation             | Naming attributes of type X520name     | string | -                    |
| givenname              | Naming attributes of type X520name     | string | -                    |
| initials               | Naming attributes of type X520name     | string | -                    |
| l                      | Locality name                          | string | -                    |
| name                   | Name                                   | string | -                    |
| nameAtBirth            | ISIS-MTT NameAtBirth                   | string | -                    |
| o                      | Organization                           | string | -                    |
| organizationIdentifier | Organization identifier                | string | -                    |
| ou                     | Organization unit name                 | string | -                    |
| placeOfBirth           | RFC 3039 PlaceOfBirth                  | string | -                    |
| postalAddress          | RFC 3039 PostalAddress                 | string | -                    |
| postalCode             | Postal code                            | string | -                    |
| pseudonym              | RFC 3039 Pseudonym                     | string | -                    |
| role                   | Role                                   | string | -                    |
| serialnumber           | Device serial number name              | string | -                    |
| st                     | State or province name                 | string | -                    |
| street                 | Street                                 | string | -                    |
| surname                | Naming attributes of type X520name     | string | -                    |
| t                      | Title                                  | string | -                    |
| telephoneNumber        | Telephone number                       | string | -                    |
| uid                    | LDAP User id                           | string | -                    |
| uniqueIdentifier       | Naming attributes of type X520name     | string | -                    |
| unstructuredAddress    | Unstructured address (from PKCS#9)     | string | -                    |

**Other attributes:**

| Object Property | Description                                                                           | Type        | Example                           |
| --------------- | ------------------------------------------------------------------------------------- | ----------- | --------------------------------- |
| attributes      | Retrieves all attribute values                                                        | key / value | "ou" → \["Test team", "Dev team"] |
| defined         | Returns true if the principal object is defined and contains values. False otherwise. | boolean     | -                                 |
| dn              | Full domain name                                                                      | string      | -                                 |

While some of these attributes can be arrays, EL will always return the first item in the array. If you want to retrieve all values from an array, you can use the `attributes` object property.

If the principal object is not defined, all values are empty.

#### Examples <a href="#examples" id="examples"></a>

* Get the value of the `Content-Type` header for an incoming HTTP request: `{#request.headers['content-type'][0]}`
* Get the second part of the request path: `{#request.paths[1]}`
* Get the client HOST from the SSL session: `{#request.ssl.clientHost}`
* Get the client DN from the SSL session: `{#request.ssl.client.dn}`
* Get the server organization from the SSL session: `{#request.ssl.server.o}`
* Get all the organization units of the server from the SSL session:
  * `{#request.ssl.server.attributes['ou'][0]}`
  * `{#request.ssl.server.attributes['OU'][1]}`
  * `{#request.ssl.server.attributes['Ou'][2]}`
* Get a custom attribute of the client from the SSL session: `{#request.ssl.client.attributes['1.2.3.4'][0]}`
* Determine if the SSL attributes of the client are set: `{#request.ssl.client.defined}`

## Response

The object properties you can access for API responses are listed below.

| Object Property | Description                 | Type        | Example            |
| --------------- | --------------------------- | ----------- | ------------------ |
| content         | Body content                | string      | -                  |
| headers         | Headers                     | key / value | X-Custom → myvalue |
| status          | Status of the HTTP response | int         | 200                |

#### Example

* Get the status of an HTTP response: `{#response.status}`

## Nodes

A node is a component that represents an instance of the Gravitee gateway. Each node runs a copy of the gateway, which is responsible for handling incoming requests, executing policies, and forwarding requests to the appropriate upstream services.

| Property | Description  | Type   | Example                              |
| -------- | ------------ | ------ | ------------------------------------ |
| id       | Node id      | string | 975de338-90ff-41ab-9de3-3890ff41ab62 |
| version  | Node version | string | 3.14.0                               |
| tenant   | Node tenant  | string | Europe                               |

### Example

* Get the version of a node : `{#node.version}`

## Policies

You can use the EL to update some aspects of policy configuration. The policy specifies if it supports EL or not by including a **Condition** section in the policy design studio configuration.

<figure><img src="../../.gitbook/assets/Screenshot 2023-04-03 at 4.58.01 PM.png" alt=""><figcaption><p>Assign attributes policy supports EL conditions</p></figcaption></figure>

## Mixin

In previous examples, we showed various ways to manipulate objects available in the EL context. You can also mix property usage to provide an increasingly dynamic configuration.

For example, we can retrieve the value of an HTTP header where the name is based on an API property named `my-property`:

`{#request.headers[#properties['my-property']]}`

## Conditions

You can also use the EL to set a condition of execution (see 'conditional policies and flows conditions') and it is possible to use logical operators such as `&&` or `||`, as shown in the example below:

`{#request.headers['my-header'] != null && #request.headers['my-header'][0] == "my-value"}`

{% hint style="info" %}
**Alternate equality check**

An alternative method is to use the `equals()` method instead of `==`. When you use `.equals()`, it is recommended to put the string first to prevent an error if `#request.headers['my-header'][0]` is `null` - for example, then `'my-value'.equals(#request.headers['my-header'][0])`will prevent an error.
{% endhint %}

## Debugging

In case of an error when using Expression Language, an exception will be raised :

`The template evaluation returns an error. Expression: {#context.error}`

TODO: add arcade demonstrating method to check output of expression language

\


[^1]: `{#request.content}` is only available for policies bound to an `on-request-content` phase.
