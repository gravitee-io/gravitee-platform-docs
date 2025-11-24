---
description: An overview about javascript.
---

# JavaScript

## Overview

You can use this policy to run [JavaScript](http://www.javascript.com/) scripts at every stage of Gateway processing.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
**Example 1**

This script stops the processing if the request contains a certain header:

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

**Example 2**

The following shows how to use the `javascript` policy to transform JSON content.

Assuming the request body below (input body content):

```json
{
  "age": 32,
  "firstname": "John",
  "lastname": "Doe"
}
```

You can run the following JavaScript script:

```javascript
var content = JSON.parse(response.content);
content.firstname = 'Hacked ' + content.firstname;
content.country = 'US';
JSON.stringify(content);
```

And the request body being passed to the API will be (output body content):

```json
{
  "age": 32,
  "firstname": "Hacked John",
  "lastname": "Doe",
  "country": "US"
}
```

**Example 3**

Assume that you sent the request body modified above to an **echo** API. You can run the following:

```javascript
var content = JSON.parse(response.content);
content.firstname = content.firstname.substring(7);
delete content.country;
JSON.stringify(content);
```

And the response message will be:

```json
{
  "age": 32,
  "firstname": "John",
  "lastname": "Doe"
}
```
{% endtab %}
{% endtabs %}

## Configuration

```javascript
"javascript": {
    "onRequestScript": "response.headers.remove('X-Powered-By');",
    "onResponseScript": "response.headers.set('X-Gravitee-Gateway-Version', '0.14.0');",
    "onRequestContentScript": "" // Not executed if empty
    "onResponseContentScript": "" // Not executed if empty
}
```

### Phases

The phases checked below are supported by the `javascript` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="205.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### onRequest / onResponse

Some variables are automatically bound to the JavaScript script to allow users to use them and define the policy behavior:

<table><thead><tr><th width="172.5">Name</th><th>Description</th></tr></thead><tbody><tr><td><code>request</code></td><td>Inbound HTTP request</td></tr><tr><td><code>response</code></td><td>Outbound HTTP response</td></tr><tr><td><code>context</code></td><td><code>PolicyContext</code> used to access external components such as services and resources</td></tr><tr><td><code>result</code></td><td>JavaScript script result</td></tr></tbody></table>

Request or response processing can be interrupted by setting the result state to `FAILURE`. By default, it will throw a `500 - Internal server error`, but you can override this behavior with the following properties:

* `code`: An HTTP status code
* `error`: The error message
* `key`: The key of a response template

### onRequestContent / onResponseContent <a href="#user-content-onrequestcontent-onresponsecontent" id="user-content-onrequestcontent-onresponsecontent"></a>

In the `onRequestContent` phase you have access to the `content` object, also known as the request body. You can modify this object.

In the `onResponseContent` phase you have access to the `content` object, also known as the response message. You can modify this object.

For example, you can transform request or response body content by applying a JavaScript script on the `OnRequestContent` phase or the `OnResponseContent` phase.

{% hint style="warning" %}
When working with scripts on `OnRequestContent` or `OnResponseContent` phase, the last instruction of the script **must** be the new body content that would be returned by the policy.
{% endhint %}

### Dictionaries, Properties, and Context Attributes <a href="#user-content-dictionaries-properties" id="user-content-dictionaries-properties"></a>

Both dictionaries (defined at the environment level), properties (defined at the API level), and context attributes can be accessed from the JavaScript script using:

* `context.dictionaries()` for dictionaries
* `context.properties()` for properties
* `context.attributes()` for context attributes

Here is an example of how to set a request header based on a property:

```javascript
request.headers.set('X-JavaScript-Policy', context.properties()['KEY_OF_MY_PROPERTY']);
```

Here is an example of reading a context attribute:

```
var myAttribute = context.attributes()['myContextAttributeName'];
```

### Options

The `javascript` policy can be used to configure the `request`, `response`, and `metrics` objects:

{% tabs %}
{% tab title="onRequest" %}
| Object  | Property       | Type                           | Description |
| ------- | -------------- | ------------------------------ | ----------- |
| request | id             | string                         | -           |
| request | transactionId  | string                         | -           |
| request | uri            | string                         | -           |
| request | path           | string                         | -           |
| request | pathInfo       | string                         | -           |
| request | contextPath    | string                         | -           |
| request | parameters     | multivalue map                 | -           |
| request | pathParameters | multivalue map                 | -           |
| request | headers        | iterable map \<string, string> | -           |
| request | method         | enum                           | -           |
| request | version        | enum                           | -           |
| request | timestamp      | long                           | -           |
| request | remoteAddress  | string                         | -           |
| request | localAddress   | string                         | -           |
| request | scheme         | string                         | -           |
| request | sslSession     | javax.net.ssl.SSLSession       | -           |
| request | metrics        | object                         |             |
{% endtab %}

{% tab title="onResponse" %}
In the `onResponse` phase, you have access to the `request`, the `response` and the `context` object.

| Object   | Property | Type                           | Description |
| -------- | -------- | ------------------------------ | ----------- |
| response | status   | int                            | -           |
| response | reason   | String                         | -           |
| response | headers  | iterable map \<string, string> | -           |
{% endtab %}

{% tab title="Metrics" %}
It is highly advisable to use the Metrics Reporter in order to manage the metrics. However, the `request` object does contain a `metrics` object.

Note that the `metrics` object changes in the different processing phases. Some properties may not make sense in certain phases.

<table><thead><tr><th width="137">Object</th><th width="235">Property</th><th width="91">Type</th><th>Description</th></tr></thead><tbody><tr><td>metrics</td><td>api</td><td>String</td><td>ID of the API</td></tr><tr><td>metrics</td><td>apiResponseTimeMs</td><td>long</td><td>Response time spend to call the backend upstream</td></tr><tr><td>metrics</td><td>application</td><td>String</td><td>ID of the consuming application</td></tr><tr><td>metrics</td><td>endpoint</td><td>String</td><td>-</td></tr><tr><td>metrics</td><td>errorKey</td><td>String</td><td>Key of the error if the policy chain is failing</td></tr><tr><td>metrics</td><td>host</td><td>String</td><td>Host header value</td></tr><tr><td>metrics</td><td>httpMethod</td><td>enum</td><td>-</td></tr><tr><td>metrics</td><td>localAddress</td><td>String</td><td>-</td></tr><tr><td>metrics</td><td>log</td><td>object</td><td>-</td></tr><tr><td>metrics</td><td>mappedPath</td><td>String</td><td>-</td></tr><tr><td>metrics</td><td>message</td><td>String</td><td>-</td></tr><tr><td>metrics</td><td>path</td><td>String</td><td>-</td></tr><tr><td>metrics</td><td>plan</td><td>String</td><td>ID of the plan</td></tr><tr><td>metrics</td><td>proxyLatencyMs</td><td>long</td><td>Latency of the gateway to apply policies</td></tr><tr><td>metrics</td><td>proxyResponseTimeMs</td><td>long</td><td>Global response time to process and respond to the consumer</td></tr><tr><td>metrics</td><td>remoteAddress</td><td>String</td><td>-</td></tr><tr><td>metrics</td><td>requestContentLength</td><td>long</td><td>-</td></tr><tr><td>metrics</td><td>requestId</td><td>String</td><td>-</td></tr><tr><td>metrics</td><td>responseContentLength</td><td>long</td><td>-</td></tr><tr><td>metrics</td><td>securityToken</td><td>String</td><td>-</td></tr><tr><td>metrics</td><td>securityType</td><td>enum</td><td>-</td></tr><tr><td>metrics</td><td>status</td><td>int</td><td>-</td></tr><tr><td>metrics</td><td>subscription</td><td>String</td><td>ID of the subscription</td></tr><tr><td>metrics</td><td>tenant</td><td>String</td><td>gateway tenant value</td></tr><tr><td>metrics</td><td>transactionId</td><td>String</td><td>-</td></tr><tr><td>metrics</td><td>uri</td><td>String</td><td>-</td></tr><tr><td>metrics</td><td>user</td><td>String</td><td>End-user doing the call (in case of OAuth2 / JWT / Basic Auth)</td></tr><tr><td>metrics</td><td>userAgent</td><td>String</td><td>Value of the user-agent header</td></tr><tr><td>metrics</td><td>zone</td><td>String</td><td>Gateway zone</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

## Errors

<table data-full-width="false"><thead><tr><th width="171">HTTP status code</th><th width="387">Message</th></tr></thead><tbody><tr><td><code>500</code></td><td>The JavaScript script cannot be parsed/compiled or executed (mainly due to a syntax error)</td></tr></tbody></table>
