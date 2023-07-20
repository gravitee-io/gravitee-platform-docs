---
description: This page provides the technical details of the Javascript policy
---

# Javascript

## Overview

Functional and implementation information for the Javascript policy is organized into the following sections:

* [Examples](template-policy-rework-structure-17.md#examples)
* [Configuration](template-policy-rework-structure-17.md#configuration)
* [Changelogs](template-policy-rework-structure-17.md#changelogs)

## Examples

You can use this policy to run [Javascript](http://www.javascript.com/) scripts at every stage of gateway processing.

{% tabs %}
{% tab title="Proxy API example" %}
{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

#### onRequest phase

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

#### Phase - onRequestContent

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

#### Phase - onResponseContent

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

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

### Reference

#### onRequest phase

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

#### Phase - onResponse

In the **onResponse** phase you have access to the **request**, the **response** and the **context** object.

| Object   | Property | Type                           | Description |
| -------- | -------- | ------------------------------ | ----------- |
| response | status   | int                            | -           |
| response | reason   | String                         | -           |
| response | headers  | iterable map \<string, string> | -           |

#### Metrics

It is highly advisable to use the Metrics Reporter in order to manage the metrics. However, the request object does contain a **metrics** object.

| Object  | Property              | Type   | Description                                                    |
| ------- | --------------------- | ------ | -------------------------------------------------------------- |
| metrics | api                   | String | ID of the API                                                  |
| metrics | apiResponseTimeMs     | long   | Response time spend to call the backend upstream               |
| metrics | application           | String | ID of the consuming application                                |
| metrics | endpoint              | String | -                                                              |
| metrics | errorKey              | String | Key of the error if the policy chain is failing                |
| metrics | host                  | String | Host header value                                              |
| metrics | httpMethod            | enum   | -                                                              |
| metrics | localAddress          | String | -                                                              |
| metrics | log                   | object | -                                                              |
| metrics | mappedPath            | String | -                                                              |
| metrics | message               | String | -                                                              |
| metrics | path                  | String | -                                                              |
| metrics | plan                  | String | ID of the plan                                                 |
| metrics | proxyLatencyMs        | long   | Latency of the gateway to apply policies                       |
| metrics | proxyResponseTimeMs   | long   | Global response time to process and respond to the consumer    |
| metrics | remoteAddress         | String | -                                                              |
| metrics | requestContentLength  | long   | -                                                              |
| metrics | requestId             | String | -                                                              |
| metrics | responseContentLength | long   | -                                                              |
| metrics | securityToken         | String | -                                                              |
| metrics | securityType          | enum   | -                                                              |
| metrics | status                | int    | -                                                              |
| metrics | subscription          | String | ID of the subscription                                         |
| metrics | tenant                | String | gateway tenant value                                           |
| metrics | transactionId         | String | -                                                              |
| metrics | uri                   | String | -                                                              |
| metrics | user                  | String | End-user doing the call (in case of OAuth2 / JWT / Basic Auth) |
| metrics | userAgent             | String | Value of the user-agent header                                 |
| metrics | zone                  | String | Gateway zone                                                   |

|   | The metrics object changes in the different processing phases and some properties may not make sense in certain phases! |
| - | ----------------------------------------------------------------------------------------------------------------------- |

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the Javascript policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-javascript/blob/master/CHANGELOG.md" %}
