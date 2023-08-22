---
description: This page provides the technical details of the Javascript policy
---

# Javascript

## Overview

You can use this policy to run [Javascript](http://www.javascript.com/) scripts at every stage of Gateway processing.

Functional and implementation information for the `javascript` policy is organized into the following sections:

* [Examples](javascript.md#examples)
* [Configuration](javascript.md#configuration)
* [Changelogs](javascript.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines/) Currently, this policy can **not** be applied at the message level.
{% endhint %}

{% tabs %}
{% tab title="Proxy API example" %}
### onRequest phase

As an example of what you can do in the **onRequest** phase, this script stops the processing if the request contains a certain header.

```
if (request.headers.containsKey('X-Gravitee-Break')) {
    result.state = State.FAILURE;
    result.code = 500
    result.error = 'Stopped processing due to X-Gravitee-Break header'
} else {
    request.headers.set('X-Javascript-Policy', 'ok');
}
```

### onRequestContent

In the **onRequestContent** phase you have access to the **content** object, also known as the [request body](https://dzone.com/articles/rest-api-path-vs-request-body-parameters). You can modify this object.

As an example, assuming the following request body:

```
[
    {
        "age": 32,
        "firstname": "John",
        "lastname": "Doe"
    }
]
```

Then you can do the following:

```
var content = JSON.parse(request.content);
content[0].firstname = 'Hacked ' + content[0].firstname;
content[0].country = 'US';

JSON.stringify(content);
```

And the request body being passed to the API would be:

```
[
    {
        "age": 32,
        "firstname": "Hacked John",
        "lastname": "Doe",
        "country": "US"
    }
]
```

{% hint style="info" %}
When working with scripts on onRequestContent phase, the last instruction of the script **must be** the new body content that would be returned by the policy.
{% endhint %}

### onResponseContent

In the **onResponseContent** phase you have access to the **content** object, also known response message. You can modify this object.

As an example, assume that you sent the request body modified in the **onRequestContent** phase to an **echo** API. You can do the following:

```
var content = JSON.parse(response.content);
content[0].firstname = content[0].firstname.substring(7);
delete content[0].country;
JSON.stringify(content);
```

And the response message would be:

```
[
    {
        "age": 32,
        "firstname": "John",
        "lastname": "Doe"
    }
]
```

{% hint style="info" %}
When working with scripts on onResponseContent phase, the last instruction of the script **must be** the new body content that would be returned by the policy.
{% endhint %}
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `javascript` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="205.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `javascript` policy can be configured with the following options:

#### onRequest

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

#### onResponse

In the **onResponse** phase you have access to the **request**, the **response** and the **context** object.

| Object   | Property | Type                           | Description |
| -------- | -------- | ------------------------------ | ----------- |
| response | status   | int                            | -           |
| response | reason   | String                         | -           |
| response | headers  | iterable map \<string, string> | -           |

#### Metrics

It is highly advisable to use the Metrics Reporter in order to manage the metrics. However, the request object does contain a **metrics** object.

<table><thead><tr><th width="137">Object</th><th width="235">Property</th><th width="91">Type</th><th>Description</th></tr></thead><tbody><tr><td>metrics</td><td>api</td><td>String</td><td>ID of the API</td></tr><tr><td>metrics</td><td>apiResponseTimeMs</td><td>long</td><td>Response time spend to call the backend upstream</td></tr><tr><td>metrics</td><td>application</td><td>String</td><td>ID of the consuming application</td></tr><tr><td>metrics</td><td>endpoint</td><td>String</td><td>-</td></tr><tr><td>metrics</td><td>errorKey</td><td>String</td><td>Key of the error if the policy chain is failing</td></tr><tr><td>metrics</td><td>host</td><td>String</td><td>Host header value</td></tr><tr><td>metrics</td><td>httpMethod</td><td>enum</td><td>-</td></tr><tr><td>metrics</td><td>localAddress</td><td>String</td><td>-</td></tr><tr><td>metrics</td><td>log</td><td>object</td><td>-</td></tr><tr><td>metrics</td><td>mappedPath</td><td>String</td><td>-</td></tr><tr><td>metrics</td><td>message</td><td>String</td><td>-</td></tr><tr><td>metrics</td><td>path</td><td>String</td><td>-</td></tr><tr><td>metrics</td><td>plan</td><td>String</td><td>ID of the plan</td></tr><tr><td>metrics</td><td>proxyLatencyMs</td><td>long</td><td>Latency of the gateway to apply policies</td></tr><tr><td>metrics</td><td>proxyResponseTimeMs</td><td>long</td><td>Global response time to process and respond to the consumer</td></tr><tr><td>metrics</td><td>remoteAddress</td><td>String</td><td>-</td></tr><tr><td>metrics</td><td>requestContentLength</td><td>long</td><td>-</td></tr><tr><td>metrics</td><td>requestId</td><td>String</td><td>-</td></tr><tr><td>metrics</td><td>responseContentLength</td><td>long</td><td>-</td></tr><tr><td>metrics</td><td>securityToken</td><td>String</td><td>-</td></tr><tr><td>metrics</td><td>securityType</td><td>enum</td><td>-</td></tr><tr><td>metrics</td><td>status</td><td>int</td><td>-</td></tr><tr><td>metrics</td><td>subscription</td><td>String</td><td>ID of the subscription</td></tr><tr><td>metrics</td><td>tenant</td><td>String</td><td>gateway tenant value</td></tr><tr><td>metrics</td><td>transactionId</td><td>String</td><td>-</td></tr><tr><td>metrics</td><td>uri</td><td>String</td><td>-</td></tr><tr><td>metrics</td><td>user</td><td>String</td><td>End-user doing the call (in case of OAuth2 / JWT / Basic Auth)</td></tr><tr><td>metrics</td><td>userAgent</td><td>String</td><td>Value of the user-agent header</td></tr><tr><td>metrics</td><td>zone</td><td>String</td><td>Gateway zone</td></tr></tbody></table>

{% hint style="info" %}
The metrics object changes in the different processing phases and some properties may not make sense in certain phases!
{% endhint %}

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-javascript/blob/master/CHANGELOG.md" %}
