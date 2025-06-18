---
hidden: true
---

# Groovy

## Overview
You can use the `groovy` policy to execute Groovy scripts at any stage of request processing within the Gateway.

This policy is applicable to the following API types:

* v2 APIs
* v4 HTTP proxy APIs 
* v4 message APIs

**Note:** The Groovy policy is not supported by v4 TCP or Native APIs.

Several variables are automatically bound to the Groovy script. These let you read, and potentially modify, their values to define the behavior of the policy.

### Request/response

| Variable   | Description                                                                 |
|------------|-----------------------------------------------------------------------------|
| `request`  | Inbound HTTP request                                                        |
| `response` | Outbound HTTP response                                                      | 
| `message`  | Message transiting the Gateway                                              | 
| `context`  | Context usable to access external components such as services and resources |
| `result`   | Object to return to alter the outcome of the request/response      |

See the [Usage](#usage) section for object attributes and methods.

### Content

| Variable           | Description                      |
|--------------------|----------------------------------|
| `request.content`  | When "Read content" is enabled   |
| `response.content` | When "Read content" is enabled   |
| `message.content`  | Always available                 |





## Usage

### Change the outcome of a proxy API


To change the outcome of the request or response to access the `result` object, use the following properties in your script:

| Attribute | Type               | Description                    |
|-----------|--------------------|--------------------------------|
| `state`   | PolicyResult.State | To indicate a failure          |
| `code`    | integer            | An HTTP status code            |
| `error`   | string             | The error message              |
| `key`     | string             | The key of a response template |

Here is an example on the request phase:

```groovy
import io.gravitee.policy.groovy.PolicyResult.State

if (request.headers.containsKey('X-Gravitee-Break')) {
    result.key = 'RESPONSE_TEMPLATE_KEY'
    result.state = State.FAILURE
    result.code = 500
    result.error = 'Stop request processing due to X-Gravitee-Break header'
} else {
    request.headers.'X-Groovy-Policy' = 'ok'
}
```

### Override content

To override content in a proxy API, you must enable "Override content." "Override content" is always enabled for message APIs.

To override existing content, make your script the expected content.

**Input body content**

```json
{
"age": 32,
"firstname": "John",
"lastname": "Doe"
}
```

**Groovy script**

_You must enable "Read content" for this to work_

```groovy
import groovy.json.JsonSlurper
import groovy.json.JsonOutput

def jsonSlurper = new JsonSlurper()
def content = jsonSlurper.parseText(response.content)
content.firstname = 'Hacked ' + content.firstname
content.country = 'US'
return JsonOutput.toJson(content)
```

**Output body content**

```json
{
  "age": 32,
  "firstname": "Hacked John",
  "lastname": "Doe",
  "country": "US"
}
```

## Bound objects properties and methods

### Request

`request.<property>`

| Property           | Type                         | Mutable | Description                                                                                                                                              |
|--------------------|------------------------------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `content`          | `String`                     |         | Body of the request.                                                                                                                                     |
| `transactionId`    | `String`                     |         | Unique identifier for the transaction.                                                                                                                   |
| `clientIdentifier` | `String`                     |         | Identifies the client that made the request.                                                                                                             |
| `uri`              | `String`                     |         | The complete request URI.                                                                                                                                |
| `host`             | `String`                     |         | Host from the incoming request.                                                                                                                          |
| `originalHost`     | `String`                     |         | Host as originally received before any internal rewriting.                                                                                               |
| `contextPath`      | `String`                     |         | API context path.                                                                                                                                         |
| `pathInfo`         | `String`                     |         | Path beyond the context path.                                                                                                                             |
| `path`             | `String`                     |         | The full path component of the request URI.                                                                                                              |
| `parameters`       | `Map<String, <List<String>>` | ✅️      | Query parameters as a multi-value map. For methods, refer to [Multimap methods](#multimap-methods).                                                           |
| `pathParameters`   | `Map<String, <List<String>>` |         | Parameters extracted from path templates. For methods, refer to [Multimap methods](#multimap-methods). Note that altering method are useless in this context. |
| `headers`          | `Map<String, String>`        | ✅       | HTTP headers. For methods, refer to [Headers methods](#headers-methods).                                                                                     |
| `method`           | `HttpMethod` (enum)          |         | HTTP method used in the request (e.g., GET, POST).                                                                                                       |
| `scheme`           | `String`                     |         | The scheme (HTTP or HTTPS) used by the request.                                                                                                          |
| `version`          | `HttpVersion` (enum)         |         | HTTP protocol version: `HTTP_1_0`,  `HTTP_1_1`,  `HTTP_2`.                                                                                               |
| `timestamp`        | `long`                       |         | Epoch timestamp of when the request was received.                                                                                                        |
| `remoteAddress`    | `String`                     |         | IP address of the client.                                                                                                                                 |
| `localAddress`     | `String`                     |         | Local IP address of the server handling the request.                                                                                                          |

### Response

`response.<property>`

| Property  | Type                  | Mutable | Description                                                                                       |
|-----------|-----------------------|---------|---------------------------------------------------------------------------------------------------|
| `content` | `String`              |         | Body of the response.                                                                              |
| `status`  | `int`                 |         | Response status code.                                                                              |
| `reason`  | `String`              |         | Reason for the status.                                                                              |
| `headers` | `Map<String, String>` | ✅       | HTTP headers wrapped in a bindable object. For methods, refer to [Headers methods](#headers-methods). |



### Message
`message.<property>`

| Property              | Type                | Mutable | Description                                                              |
|-----------------------|---------------------|---------|--------------------------------------------------------------------------|
| `correlationId`       | String              |         | Correlation ID to track the message.                                      |
| `parentCorrelationId` | String              |         | Parent correlation ID.                                                    |
| `timestamp`           | long                |         | Epoch (ms) timestamp.                                                     |
| `error`               | boolean             |         | Message is an error message.                                              |
| `metadata`            | Map<String, Object> | ✅       | Message metadata. Dependent on the messaging system.                        |
| `headers`             | Map<String, String> | ✅       | Message headers. For methods, refer to [Headers methods](#headers-methods).  |
| `content`             | String              |         | Message body as a string.                                                 |
| `contentAsBase64`     | String              |         | Message body bytes as a basic base64 string.                                |
| `contentAsByteArray`  | byte[]              |         | Message body bytes.                                                       |
| `attributes`          | Map<String, Object> | ✅       | Message attributes wrapped in a bindable object. For methods, see below. |

**Message attributes methods**

`message.attributes.<method>`

| Method          | Arguments (type) | Return type   | Description                                |
|-----------------|------------------|---------------|--------------------------------------------|
| `remove`        | key (`Object`)   |               | Remove an attribute.                       |
| `containsKey`   | key (`Object`)   | `boolean`     | Check if an attribute exists.               |
| `containsValue` | key (`Object`)   | `boolean`     | Check if one of the attributes contains the value. |
| `empty`         |                  | `boolean`     | `true` when the attribute exists.           |
| `size`          |                  | `int`         | Return an attribute count.                  |
| `keySet`        |                  | `Set<String>` | All attribute names.                        |

### Context

| Property          | Type                | Mutable | Description                  | 
|-------------------|---------------------|---------|------------------------------|
| `attributes`      | Map<String, Object> | ✅       | Context attributes as a map. |
| `attributeNames`  | Set<String>         |         | All attribute names.         |
| `attributeAsList` | List<Object>        |         | All attribute values.         |

**Context attributes methods**

`context.attributes.<method>`

Use a prefix to get an attribute or verify that it exists.

For example, `context.attributes.'my-specific-attribute'` returns an attribute map entry with the key `gravitee.attribute.my-specific-attribute`.

Refer to the Gravitee documentation for available attributes. 

**Note: This rule only applies when reading an attribute. You must explicitly add `gravitee.attribute.<key>` to alter an attribute.**


| Method        | Arguments (type)                | Return type | Description                                                                                                                                  |
|---------------|---------------------------------|-------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| `get`         | key (`Object`)                  | `Object`    | Get a Gravitee attribute starting with `gravitee.attribute.`. Works with Groovy `context.attributes.'key'` syntax using the same prefix rule. |
| `containsKey` | key (`Object`)                  | `boolean`   | Check if a Gravitee attribute starting with `gravitee.attribute.` exists.                                                                       |
| `put`         | key (`String`) value (`Object`) |             | Equivalent of `context.attributes.'key' = value`.                                                                                            |

Other methods of `java.util.Map` are accessible, such as `remove` and `size`.


### Common objects

#### Headers methods

Applicable to `request.headers`, `response.headers`, `message.headers`.

| Method          | Arguments (type) | Return type    | Description               |
|-----------------|------------------|----------------|---------------------------|
| `remove`        | key (`Object`)   |                | Remove a header.          |
| `containsKey`   | key (`Object`)   | `boolean`      | Check if a header exists.  |
| `clear`         |                  |                | Remove all headers.         |
| `empty`         |                  | `boolean`      | `true` when header exists. |
| `size`          |                  | `int`          | Return header count.      |
| `keySet`        |                  | `Set<String>`  | All header names.         |


#### Multimap methods

Multimap lets you use several values for a single map entry without pre-initializing a collection.

Multimap is applicable to `request.parameters` and `request.pathParameters`.

All methods of the Gravitee [MultiValueMap](https://github.com/gravitee-io/gravitee-common/blob/master/src/main/java/io/gravitee/common/util/MultiValueMap.java) implementation: `getFirst`, `add`, `set`, `setAll`, `toSingleValueMap`, `containsAllKeys`.

All `java.util.Map` are also available.




## Errors
These templates are defined at the API level, in the "Entrypoint" section for v4 APIs, or in "Response Templates" for v2 APIs.
The error keys sent by this policy are as follows:

| Key |
| ---  |
| GROOVY_EXECUTION_FAILURE |



## Phases
The `groovy` policy can be applied to the following API types and flow phases.

### Compatible API types

* `PROXY`
* `MESSAGE`

### Supported flow phases:

* Request
* Response
* Publish
* Subscribe

## Compatibility matrix
Strikethrough text indicates that a version is deprecated.

| Plugin version| APIM |
| --- | ---  |
|3.x|4.6.x and above |
|2.x|4.5.x and below |



## Configuration
### Gateway configuration
### Whitelist sandbox

The `groovy` policy includes a native sandbox feature, which lets you safely run Groovy scripts. The sandbox is based on a predefined list of allowed methods, fields, constructors, and annotations.

The complete whitelist can be found here: [gravitee groovy whitelist](https://gh.gravitee.io/gravitee-io/gravitee-policy-groovy/master/src/main/resources/groovy-whitelist).

This whitelist should address the majority of possible use cases. If you have specific needs which are not satisfied by the built-in whitelist, you can extend, or even replace, the list with your own declarations. To modify the whitelist, configure the `gravitee.yml` file to specify:

* `groovy.whitelist.mode`: `append` or `replace`. This lets you append whitelisted definitions to the built-in list, or completely replace it. We recommend selecting `append` to avoid unintended behaviors.
* `groovy.whitelist.list`: This lets you declare other methods, constructors, fields, or annotations in the whitelist.
    * Start with `method` to allow a specific method (complete signature)
    * Start with `class` to allow a complete class. All methods, constructors, and fields of the class are then accessible.
    * Start with `new` to allow a specific constructor (complete signature)
    * Start with `field` to allow access to a specific field of a class
    * Start with `annotation` to allow use of a specific annotation


gravitee.yml
```YAML
groovy:
  whitelist:
    mode: append
    list:
      - method com.acme.common.Strings toTitleCase java.lang.String
      - class com.acme.common.Strings
```
Environment variables (Helm)
```YAML
gateway:
  env:
    - name: GRAVITEE_GROOVY_WHITELIST_MODE
      value: append
    - name: GRAVITEE_GROOVY_WHITELIST_LIST_0
      value: "method com.acme.common.Strings toTitleCase java.lang.String"
    - name: GRAVITEE_GROOVY_WHITELIST_LIST_1
      value: "class com.acme.common.Strings"
```

**Security implications**

Exercise care when using classes or methods. In some cases, giving access to all methods of a class may make unwanted methods accessible via transitivity and risk security breaches.


### Configuration options


#### 
| Name <br>`json name`  | Type <br>`constraint`  | Mandatory  | Default  | Description  |
|:----------------------|:-----------------------|:----------:|:---------|:-------------|
| Override content<br>`overrideContent`| boolean|  | | Enable to override the content of the request or response with the value returned by your script.|
| Read content<br>`readContent`| boolean|  | | Enable if your script needs to access the content of the HTTP request or response in your script.|
| Script<br>`script`| string|  | | Groovy script to evaluate.|




## Examples

*Proxy API on Request phase*
```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "Groovy example API",
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
            "name": "Groovy",
            "enabled": true,
            "policy": "groovy",
            "configuration":
              {
                  "readContent": false,
                  "overrideContent": false,
                  "script": "response.headers.remove 'X-Powered-By'\nresponse.headers.'X-Gravitee-Gateway-Version' = '0.14.0'"
              }
          }
        ]
      }
    ]
  }
}

```
*Message API CRD*
```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiV4Definition"
metadata:
    name: "groovy-message-api-crd"
spec:
    name: "Groovy example"
    type: "MESSAGE"
    flows:
      - name: "Common Flow"
        enabled: true
        selectors:
            matchRequired: false
            mode: "DEFAULT"
        request:
          - name: "Groovy"
            enabled: true
            policy: "groovy"
            configuration:
              overrideContent: false
              readContent: false
              script: |-
                  response.headers.remove 'X-Powered-By'
                  response.headers.'X-Gravitee-Gateway-Version' = '0.14.0'

```


## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-groovy/blob/master/CHANGELOG.md" %}
