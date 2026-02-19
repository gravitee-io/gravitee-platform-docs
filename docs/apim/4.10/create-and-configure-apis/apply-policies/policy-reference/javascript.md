---
description: An overview about javascript.
metaLinks:
  alternates:
    - javascript.md
---

# JavaScript

## Overview

You can use the [JavaScript](http://www.javascript.com/) policy to run JavaScript scripts at any stage of request processing through the gateway. Several variables are automatically bound to the JavaScript script. These let you read, and potentially modify, their values to define the behavior of the policy.

This policy is applicable to the following API types:

* v2 APIs
* v4 HTTP proxy APIs
* v4 message APIs
* v4 LLM proxy
* v4 MCP proxy

**Note:** The JavaScript policy is not supported by v4 TCP or Native APIs.

### High level variables

List of high-level variables available within the script:

| Variable   | Description                                                                 |
| ---------- | --------------------------------------------------------------------------- |
| `request`  | Inbound HTTP request                                                        |
| `response` | Outbound HTTP response                                                      |
| `message`  | Message transiting the Gateway                                              |
| `context`  | Context usable to access external components such as services and resources |
| `result`   | Object to return to alter the outcome of the request/response               |

### Content variables

List of content-specific variables available within the script:

| Variable           | Description                                                          |
| ------------------ | -------------------------------------------------------------------- |
| `request.content`  | Inbound request content, available when "Read content" is enabled.   |
| `response.content` | Outbound response content, available when "Read content" is enabled. |
| `message.content`  | Message content, always available.                                   |

***

See the **Usage** and **Schema** sections for further explanation regarding available objects, their attributes, and methods.

## Usage

### Change the outcome

To change the outcome, access the `result` object in your script and use the following properties:

List of variables that allow you to control the outcome:

| Attribute | Type                 | Description                    |
| --------- | -------------------- | ------------------------------ |
| `state`   | `PolicyResult.State` | To indicate a failure          |
| `code`    | integer              | An HTTP status code            |
| `error`   | string               | The error message              |
| `key`     | string               | The key of a response template |

Setting `state` to `FAILURE` will, by default, throw a `500 - internal server error`, but you can override this behavior with the above properties.

Example in the request phase:

```javascript
if (request.headers.containsKey('X-Gravitee-Break')) {
    result.key = 'RESPONSE_TEMPLATE_KEY';
    result.state = State.FAILURE;
    result.code = 500
    result.error = 'Stop request processing due to X-Gravitee-Break header'
} else {
    request.headers.set('X-JavaScript-Policy', 'ok');
}
```

To customize the error sent by the policy:

```javascript
result.key = 'RESPONSE_TEMPLATE_KEY';
result.state = State.FAILURE;
result.code = 400
result.error = '{"error":"My specific error message","code":"MY_ERROR_CODE"}'
result.contentType = 'application/json'
```

### Override content

To override content, you must enable **Override content** and make your script return the new content as the last instruction.

#### Input body content

```json
[
    {
        "age": 32,
        "firstname": "John",
        "lastname": "Doe"
    }
]
```

#### JavaScript script

The following example shows how to use the JavaScript policy to transform JSON content:

```javascript
var content = JSON.parse(response.content);
content[0].firstname = 'Hacked ' + content[0].firstname;
content[0].country = 'US';

JSON.stringify(content);
```

#### Output body content

```json
[
    {
        "age": 32,
        "firstname": "Hacked John",
        "lastname": "Doe",
        "country": "US"
    }
]
```

***

## Dictionaries - Properties

Both Dictionaries (defined at the environment level) and Properties (defined at the API level) can be accessed from the JavaScript script, using:

* `context.dictionaries()` for Dictionaries
* `context.properties()` for Properties

Example of setting a request header based on a Property:

```javascript
request.headers.set('X-JavaScript-Policy', context.properties()['KEY_OF_MY_PROPERTY']);
```

***

## Schema

### Request

`request.<property>`

| Property           | Type                        | Mutable | Description                                                                                        |
| ------------------ | --------------------------- | ------- | -------------------------------------------------------------------------------------------------- |
| `content`          | `String`                    |         | Body of the request.                                                                               |
| `transactionId`    | `String`                    |         | Unique identifier for the transaction.                                                             |
| `clientIdentifier` | `String`                    |         | Identifies the client that made the request.                                                       |
| `uri`              | `String`                    |         | The complete request URI.                                                                          |
| `host`             | `String`                    |         | Host from the incoming request.                                                                    |
| `originalHost`     | `String`                    |         | Host as originally received before any internal rewriting.                                         |
| `contextPath`      | `String`                    |         | API context path.                                                                                  |
| `pathInfo`         | `String`                    |         | Path beyond the context path.                                                                      |
| `path`             | `String`                    |         | The full path component of the request URI.                                                        |
| `parameters`       | `Map<String, List<String>>` | ✅       | Query parameters as a multi-value map. See Multimap methods.                                       |
| `pathParameters`   | `Map<String, List<String>>` |         | Parameters extracted from path templates. Alter methods are not useful here. See Multimap methods. |
| `headers`          | `Map<String, List<String>>` | ✅       | HTTP headers. See Headers methods.                                                                 |
| `method`           | `HttpMethod` (enum)         |         | HTTP method (GET, POST, etc.).                                                                     |
| `scheme`           | `String`                    |         | HTTP or HTTPS.                                                                                     |
| `version`          | `HttpVersion` (enum)        |         | Protocol version: `HTTP_1_0`, `HTTP_1_1`, `HTTP_2`.                                                |
| `timestamp`        | `long`                      |         | Epoch timestamp when request was received.                                                         |
| `remoteAddress`    | `String`                    |         | Client IP address.                                                                                 |
| `localAddress`     | `String`                    |         | Local server IP address.                                                                           |

***

### Response

`response.<property>`

| Property  | Type                        | Mutable | Description                        |
| --------- | --------------------------- | ------- | ---------------------------------- |
| `content` | `String`                    |         | Body of the response.              |
| `status`  | `int`                       |         | Response status code.              |
| `reason`  | `String`                    |         | Reason for the status.             |
| `headers` | `Map<String, List<String>>` | ✅       | HTTP headers. See Headers methods. |

***

### Message

`message.<property>`

| Property              | Type                        | Mutable | Description                              |
| --------------------- | --------------------------- | ------- | ---------------------------------------- |
| `correlationId`       | `String`                    |         | Correlation ID to track the message.     |
| `parentCorrelationId` | `String`                    |         | Parent correlation ID.                   |
| `timestamp`           | `long`                      |         | Epoch (ms) timestamp.                    |
| `error`               | `boolean`                   |         | Whether the message is an error message. |
| `metadata`            | `Map<String, Object>`       | ✅       | Message metadata, system-dependent.      |
| `headers`             | `Map<String, List<String>>` | ✅       | Message headers. See Headers methods.    |
| `content`             | `String`                    |         | Message body as a string.                |
| `contentAsBase64`     | `String`                    |         | Message body as a base64 string.         |
| `contentAsByteArray`  | `byte[]`                    |         | Message body as bytes.                   |
| `attributes`          | `Map<String, Object>`       | ✅       | Message attributes. See below.           |

#### Message attributes methods

`message.attributes.<method>`

| Method          | Arguments (type) | Return type   | Description                          |
| --------------- | ---------------- | ------------- | ------------------------------------ |
| `remove`        | key (`Object`)   |               | Remove an attribute.                 |
| `containsKey`   | key (`Object`)   | `boolean`     | Check if an attribute exists.        |
| `containsValue` | value (`Object`) | `boolean`     | Check if attributes contain a value. |
| `empty`         |                  | `boolean`     | `true` if no attributes exist.       |
| `size`          |                  | `int`         | Attribute count.                     |
| `keySet`        |                  | `Set<String>` | All attribute names.                 |

***

## Context

`context.<property>`

| Property          | Type                  | Mutable | Description                  |
| ----------------- | --------------------- | ------- | ---------------------------- |
| `attributes`      | `Map<String, Object>` | ✅       | Context attributes as a map. |
| `attributeNames`  | `Set<String>`         |         | All attribute names.         |
| `attributeAsList` | `List<Object>`        |         | All attribute values.        |

### Context attributes methods

`context.attributes.<method>`

Refer to Gravitee documentation for available attributes.

| Method        | Arguments (type)                 | Return type | Description                                              |
| ------------- | -------------------------------- | ----------- | -------------------------------------------------------- |
| `get`         | key (`Object`)                   | `Object`    | Get a Gravitee attribute (e.g., `gravitee.attribute.*`). |
| `containsKey` | key (`Object`)                   | `boolean`   | Check if a Gravitee attribute exists.                    |
| `set`         | key (`String`), value (`Object`) |             | Set a Gravitee attribute.                                |

Other `java.util.Map` methods are also available, such as `remove` and `size`.

## Common objects

### Headers methods <a href="#headers-methods" id="headers-methods"></a>

Applicable to `request.headers`, `response.headers`, `message.headers`.

| Method        | Arguments (type)                             | Return type                            | Description                          |
| ------------- | -------------------------------------------- | -------------------------------------- | ------------------------------------ |
| `get`         | key (`String`)                               | `String`                               | Get first value of a header.         |
| `getAll`      | key (`String`)                               | `List<String>`                         | Get all values of a header.          |
| `put`         | key (`String`), value (`String`)             | `List<String>` (previous values)       | Replace header with a single value.  |
| `put`         | key (`String`), value (`List<String>`)       | `List<String>` (previous values)       | Replace header with multiple values. |
| `set`         | key (`String`), value (`String`)             | Updated headers object                 | Set a header.                        |
| `set`         | key (`String`), value (`List<String>`)       | Updated headers object                 | Set a header.                        |
| `remove`      | key (`String`)                               | Updated headers object                 | Remove a header.                     |
| `containsKey` | key (`Object`)                               | `boolean`                              | Check if a header exists.            |
| `clear`       |                                              |                                        | Remove all headers.                  |
| `isEmpty`     |                                              | `boolean`                              | `true` if no headers exist.          |
| `size`        |                                              | `int`                                  | Header count.                        |
| `keySet`      |                                              | `Set<String>`                          | All header names.                    |
| `entrySet`    |                                              | `Set<Map.Entry<String, List<String>>>` | All headers as entries.              |
| `forEach`     | consumer (`Map.Entry<String, List<String>>`) |                                        | Iterate over headers.                |

***

### Multimap methods <a href="#multimap-methods" id="multimap-methods"></a>

Multimap lets you use several values for a single map entry without pre-initializing a collection.

Applicable to `request.parameters` and `request.pathParameters`.

All methods of the Gravitee [MultiValueMap](https://github.com/gravitee-io/gravitee-common/blob/master/src/main/java/io/gravitee/common/util/MultiValueMap.java) implementation are supported:\
`getFirst`, `add`, `set`, `setAll`, `toSingleValueMap`, `containsAllKeys`.

Other `java.util.Map` methods are also available, such as `remove` and `size`.

## Coming from Apigee

You will find below the main differences between JS scripts coming from **Apigee** and the ones you can run on the **Gravitee** platform:

| Feature                                | Apigee                                                      | Gravitee                                                                                                                                                                   | Comment                                                                                                                                                                                   |
| -------------------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Access to context variables            | `context.getVariable('foo');`                               | `context.attributes.foo;`                                                                                                                                                  |                                                                                                                                                                                           |
| Setting a context variable             | `context.setVariable('foo', 'bar');`                        | `context.attributes.foo = 'bar';`                                                                                                                                          |                                                                                                                                                                                           |
| Changing request or response header    | `context.targetRequest.headers['TARGET-HEADER-X']='foo';`   | `request.headers.set('TARGET-HEADER-X', 'foo');`                                                                                                                           | `set` is used to replace the header value.                                                                                                                                                |
| Multivalued request or response header | ?                                                           | `response.headers.add('TARGET-HEADER-X', 'foo'); response.headers.add('TARGET-HEADER-X', 'bar');`                                                                          | `add` can be used for multivalued headers.                                                                                                                                                |
| Changing response code or message      | `targetResponse.status.code = 500;`                         | `response.status(500);`                                                                                                                                                    | See `result` if you want to break the policy chain and return an error.                                                                                                                   |
| Changing the body response             | `context.proxyResponse.content = 'foo';`                    | `'foo';`                                                                                                                                                                   | Just set last instruction of the `OnRequestContent` to override the request body or `OnResponseContent` to override the response body.                                                    |
| Print messages                         | `print('foo');`                                             | `print('foo');`                                                                                                                                                            | The `print` statement has no effect and is simply ignored for now.                                                                                                                        |
| Importing another js script            |                                                             |                                                                                                                                                                            | This is not supported for now.                                                                                                                                                            |
| Playing with request / response phases | `if (context.flow=="PROXY_RESP_FLOW") { // do something; }` | Use a script on each phase                                                                                                                                                 | Phases are not exactly the same and Gravitee does not allow a single script on different phases. You must define one script per phase or leave the field blank if no script is necessary. |
| Timeout                                | `timeLimit` configuration at JavaScript policy level        |                                                                                                                                                                            | The timeout is not supported for now.                                                                                                                                                     |
| Manage errors                          | ?                                                           | `result.state = State.FAILURE; result.code = 400; result.error = '{"error":"My specific error message","code":"MY_ERROR_CODE"}'; result.contentType = 'application/json';` |                                                                                                                                                                                           |
| Http call                              | `httpClient.get("http://example.com", callback);`           | `httpClient.get("http://example.com", callback);`                                                                                                                          | ⚠️ This feature is a draft and may change or be unsupported in the final version.                                                                                                         |

## Compatibility and Deprecation Notes

The following properties of the JavaScript policy are **deprecated** and will be removed in future releases:

* `onRequestScript`
* `onResponseScript`
* `onRequestContentScript`
* `onResponseContentScript`

Use the new configuration format, which allows defining a single **script** along with additional options such as _Read content_ and _Override content_.

If you created a v4 HTTP API with the JavaScript policy (version <= 1.4.0), `onRequestScript` and `onResponseScript` will still execute during the request and response phases respectively.\
It is strongly recommended to migrate your API to the new configuration format and use the `script` property instead.

Because `onRequestScript` and `onResponseScript` are no longer displayed due to deprecation, you can retrieve their values via the Management API (e.g., [listing plans associated with the given API](https://gravitee-io-labs.github.io/mapi-v1-docs/#tag/api-plans/get/v1/organizations/{orgId}/environments/{envId}/apis/{api}/plans)) or using the export feature in the Gravitee UI under **API Configuration → General** section.

> **Note:**\
> The easiest migration path is:
>
> 1. Create a new policy with the copied script.
> 2. Delete the old one.
> 3. Save and deploy the API.

## Errors

These templates are defined at the API level, in the "Entrypoint" section for v4 APIs, or in "Response Templates" for v2 APIs. The error keys sent by this policy are as follows:

| Key                            |
| ------------------------------ |
| JAVASCRIPT\_EXECUTION\_FAILURE |

## Phases

The `javascript` policy can be applied to the following API types and flow phases.

### Compatible API types

* `PROXY`
* `MESSAGE`
* `MCP PROXY`
* `LLM PROXY`
* `A2A PROXY`

### Supported flow phases:

* Request
* Response
* Publish
* Subscribe

### Compatibility matrix

Strikethrough text indicates that a version is deprecated.

| Plugin version | APIM             |
| -------------- | ---------------- |
| 2.x            | 4.7.x and above  |
| 1.x            | 3.18.x and above |

## Configuration options

| <p>Name<br><code>json name</code></p>                   | <p>Type<br><code>constraint</code></p> | Mandatory | Default | Description                                                                                       |
| ------------------------------------------------------- | -------------------------------------- | :-------: | ------- | ------------------------------------------------------------------------------------------------- |
| <p>Override content<br><code>overrideContent</code></p> | boolean                                |           |         | Enable to override the content of the request or response with the value returned by your script. |
| <p>Read content<br><code>readContent</code></p>         | boolean                                |           |         | Enable if your script needs to access the content of the HTTP request or response in your script. |
| <p>Script<br><code>script</code></p>                    | string                                 |           |         | Javascript script to evaluate.                                                                    |

## Examples

_Proxy API With Defaults_

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "Javascript example API",
    "flows": [
      {
        "name": "Common Flow",
        "enabled": true,
        "selectors": [
          {
            "type": "HTTP",
            "path": "/",
            "pathOperator": "STARTS_WITH"
          }
        ],
        "request": [
          {
            "name": "Javascript",
            "enabled": true,
            "policy": "javascript",
            "configuration":
              {
                "overrideContent": false,
                "readContent": false
              }
          }
        ]
      }
    ]
  }
}

```

_Proxy API on Request phase_

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "Javascript example API",
    "flows": [
      {
        "name": "Common Flow",
        "enabled": true,
        "selectors": [
          {
            "type": "HTTP",
            "path": "/",
            "pathOperator": "STARTS_WITH"
          }
        ],
        "request": [
          {
            "name": "Javascript",
            "enabled": true,
            "policy": "javascript",
            "configuration":
              {
                  "readContent": false,
                  "overrideContent": false,
                  "script": "request.headers.set('X-JavaScript-Policy', 'ok');"
              }
          }
        ]
      }
    ]
  }
}

```

_Proxy API on Response phase_

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "Javascript example API",
    "flows": [
      {
        "name": "Common Flow",
        "enabled": true,
        "selectors": [
          {
            "type": "HTTP",
            "path": "/",
            "pathOperator": "STARTS_WITH"
          }
        ],
        "response": [
          {
            "name": "Javascript",
            "enabled": true,
            "policy": "javascript",
            "configuration":
              {
                  "readContent": false,
                  "overrideContent": false,
                  "script": "response.headers.set('X-JavaScript-Policy', 'ok');"
              }
          }
        ]
      }
    ]
  }
}

```

_Proxy API on Request phase - override content_

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "Javascript example API",
    "flows": [
      {
        "name": "Common Flow",
        "enabled": true,
        "selectors": [
          {
            "type": "HTTP",
            "path": "/",
            "pathOperator": "STARTS_WITH"
          }
        ],
        "response": [
          {
            "name": "Javascript",
            "enabled": true,
            "policy": "javascript",
            "configuration":
              {
                  "readContent": true,
                  "overrideContent": true,
                  "script": "response.content + ' appended by JavaScript policy';"
              }
          }
        ]
      }
    ]
  }
}

```

_Message API CRD_

```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiV4Definition"
metadata:
    name: "javascript-message-api-crd"
spec:
    name: "Javascript example"
    type: "MESSAGE"
    flows:
      - name: "Common Flow"
        enabled: true
        selectors:
            matchRequired: false
            mode: "DEFAULT"
        request:
          - name: "Javascript"
            enabled: true
            policy: "javascript"
            configuration:
              overrideContent: false
              readContent: false
              script: message.headers.set('X-JavaScript-Policy', 'ok');

```

_Message API CRD - override content_

```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiV4Definition"
metadata:
    name: "javascript-message-api-crd"
spec:
    name: "Javascript example"
    type: "MESSAGE"
    flows:
      - name: "Common Flow"
        enabled: true
        selectors:
            matchRequired: false
            mode: "DEFAULT"
        request:
          - name: "Javascript"
            enabled: true
            policy: "javascript"
            configuration:
              overrideContent: true
              readContent: true
              script: message.content + ' appended by JavaScript policy';

```

## Changelog

#### [2.0.0](https://github.com/gravitee-io/gravitee-policy-javascript/compare/1.5.0...2.0.0) (2025-12-12)

**Bug Fixes**

* few project changes ([71b8ddc](https://github.com/gravitee-io/gravitee-policy-javascript/commit/71b8ddc16badb5d72ab0fd59290fa77df65c1935))
* override version of central-publishing-maven-plugin with 0.9.0 ([2d28389](https://github.com/gravitee-io/gravitee-policy-javascript/commit/2d283893cda4ab8a0ee31449ef969a05aa19bdff))
* rewrite documentation to doc-gen ([#46](https://github.com/gravitee-io/gravitee-policy-javascript/issues/46)) ([90f09f4](https://github.com/gravitee-io/gravitee-policy-javascript/commit/90f09f4ec6d934eb01a41a933f8be1fc177cb615))

**Features**

* add v4 messaging support ([#45](https://github.com/gravitee-io/gravitee-policy-javascript/issues/45)) ([6ea67fe](https://github.com/gravitee-io/gravitee-policy-javascript/commit/6ea67fe1e3b441f0ca7bb588355314e4a7be592d))
* enable for LLM & MCP Proxy API ([#49](https://github.com/gravitee-io/gravitee-policy-javascript/issues/49)) ([63f97f4](https://github.com/gravitee-io/gravitee-policy-javascript/commit/63f97f4564b21b39f19ffec3f2eff10a57bccffb))

**BREAKING CHANGES**

* requires APIM 4.8+

Co-authored-by: Michal Balinski [michal@incubly.com](mailto:michal@incubly.com)

#### [2.0.0-alpha.5](https://github.com/gravitee-io/gravitee-policy-javascript/compare/2.0.0-alpha.4...2.0.0-alpha.5) (2025-11-14)

**Features**

* enable for LLM & MCP Proxy API ([#49](https://github.com/gravitee-io/gravitee-policy-javascript/issues/49)) ([63f97f4](https://github.com/gravitee-io/gravitee-policy-javascript/commit/63f97f4564b21b39f19ffec3f2eff10a57bccffb))

#### [2.0.0-alpha.4](https://github.com/gravitee-io/gravitee-policy-javascript/compare/2.0.0-alpha.3...2.0.0-alpha.4) (2025-10-09)

**Bug Fixes**

* override version of central-publishing-maven-plugin with 0.9.0 ([2d28389](https://github.com/gravitee-io/gravitee-policy-javascript/commit/2d283893cda4ab8a0ee31449ef969a05aa19bdff))

#### [2.0.0-alpha.3](https://github.com/gravitee-io/gravitee-policy-javascript/compare/2.0.0-alpha.2...2.0.0-alpha.3) (2025-10-02)

**Bug Fixes**

* few project changes ([71b8ddc](https://github.com/gravitee-io/gravitee-policy-javascript/commit/71b8ddc16badb5d72ab0fd59290fa77df65c1935))

#### [2.0.0-alpha.2](https://github.com/gravitee-io/gravitee-policy-javascript/compare/2.0.0-alpha.1...2.0.0-alpha.2) (2025-09-19)

**Bug Fixes**

* rewrite documentation to doc-gen ([#46](https://github.com/gravitee-io/gravitee-policy-javascript/issues/46)) ([90f09f4](https://github.com/gravitee-io/gravitee-policy-javascript/commit/90f09f4ec6d934eb01a41a933f8be1fc177cb615))

#### [2.0.0-alpha.1](https://github.com/gravitee-io/gravitee-policy-javascript/compare/1.4.0...2.0.0-alpha.1) (2025-09-16)

**Features**

* add v4 messaging support ([#45](https://github.com/gravitee-io/gravitee-policy-javascript/issues/45)) ([6ea67fe](https://github.com/gravitee-io/gravitee-policy-javascript/commit/6ea67fe1e3b441f0ca7bb588355314e4a7be592d))

**BREAKING CHANGES**

* requires APIM 4.8+

Co-authored-by: Michal Balinski [michal@incubly.com](mailto:michal@incubly.com)

#### [1.5.0](https://github.com/gravitee-io/gravitee-policy-javascript/compare/1.4.0...1.5.0) (2025-12-09)

**Features**

* allow to use it with LLM & MCP ([eb1c425](https://github.com/gravitee-io/gravitee-policy-javascript/commit/eb1c425c6fb7ac2368d2a7231612aa308844e083))

#### [1.4.0](https://github.com/gravitee-io/gravitee-policy-javascript/compare/1.3.3...1.4.0) (2025-04-01)

**Features**

* enable policy for v4 proxy API ([f85cabf](https://github.com/gravitee-io/gravitee-policy-javascript/commit/f85cabf3fed61aa74ff680b0a3abe2bed80c3506))

[**1.3.3**](https://github.com/gravitee-io/gravitee-policy-javascript/compare/1.3.2...1.3.3) **(2023-07-20)**

**Bug Fixes**

* update policy description ([e055cc5](https://github.com/gravitee-io/gravitee-policy-javascript/commit/e055cc5ba4b79be5ffd94875270feef1ed6eb4b8))

[**1.3.2**](https://github.com/gravitee-io/gravitee-policy-javascript/compare/1.3.1...1.3.2) **(2023-07-11)**

**Bug Fixes**

* Protect the engine property from being deleted every time a script is evaluated ([16446ed](https://github.com/gravitee-io/gravitee-policy-javascript/commit/16446ed5b2214bfda97a4750c7690aa811433da3))

[**1.3.1**](https://github.com/gravitee-io/gravitee-policy-javascript/compare/1.3.0...1.3.1) **(2023-06-27)**

**Bug Fixes**

* add policy result key to readme ([f37613e](https://github.com/gravitee-io/gravitee-policy-javascript/commit/f37613ede529eaa18f39fddcebfc77f4390461ed))

#### [1.3.0](https://github.com/gravitee-io/gravitee-policy-javascript/compare/1.2.1...1.3.0) (2023-06-27)

**Features**

* allow to add response template key in policy result ([b0ffc3a](https://github.com/gravitee-io/gravitee-policy-javascript/commit/b0ffc3a2988376d1e2810e5693eff2bab4ac6666))

[**1.2.1**](https://github.com/gravitee-io/gravitee-policy-javascript/compare/1.2.0...1.2.1) **(2023-06-22)**

**Bug Fixes**

* **engine:** Protect the engine property from being deleted ([b0cae0f](https://github.com/gravitee-io/gravitee-policy-javascript/commit/b0cae0fc3c4764809f508689fd7fcfc89e69741b))

#### [1.2.0](https://github.com/gravitee-io/gravitee-policy-javascript/compare/1.1.1...1.2.0) (2023-04-12)

**Bug Fixes**

* add `getMetrics` method to be consistent with other fields ([123d585](https://github.com/gravitee-io/gravitee-policy-javascript/commit/123d585489967c4a9eac4da33cc9c8aae8117fcd))
* fix `scheme` getter that was returning local address instead ([bb10890](https://github.com/gravitee-io/gravitee-policy-javascript/commit/bb1089056ab6974faabea3e9ba2ae9908eb1c921))

**Features**

* add getter for `host` ([84bc68c](https://github.com/gravitee-io/gravitee-policy-javascript/commit/84bc68cd8aa21bb832b9a08a49a5a3f8c68e71ea))
* expose `properties` just like it's done for `dictionaries` ([2e4f8fa](https://github.com/gravitee-io/gravitee-policy-javascript/commit/2e4f8faa03d215e0730faba849b1d38754a58a88))

[**1.1.1**](https://github.com/gravitee-io/gravitee-policy-javascript/compare/\[secure]...1.1.1) **(2022-02-21)**

**Bug Fixes**

* allow error on request and response content phases ([#17](https://github.com/gravitee-io/gravitee-policy-javascript/issues/17)) ([d1c6be9](https://github.com/gravitee-io/gravitee-policy-javascript/commit/d1c6be912c03e544e3e6a6b0173a38f2b37f5b33)), closes [gravitee-io/issues#7173](https://github.com/gravitee-io/issues/issues/7173)

#### [\[secure\]](https://github.com/gravitee-io/gravitee-policy-javascript/compare/1.0.0...\[secure]) (2022-01-24)

**Features**

* **headers:** Internal rework and introduce HTTP Headers API ([f5354c4](https://github.com/gravitee-io/gravitee-policy-javascript/commit/f5354c4282abffa53b0c184f911e6db0ac49638f)), closes [gravitee-io/issues#6772](https://github.com/gravitee-io/issues/issues/6772)
* **perf:** adapt policy for new classloader system ([b70c9c8](https://github.com/gravitee-io/gravitee-policy-javascript/commit/b70c9c89013ca20b7064c9ac37f6f460446dbf27)), closes [gravitee-io/issues#6758](https://github.com/gravitee-io/issues/issues/6758)
