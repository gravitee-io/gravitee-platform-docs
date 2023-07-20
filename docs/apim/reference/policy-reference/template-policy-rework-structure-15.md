---
description: This page provides the technical details of the HTTP Callout policy
---

# HTTP Callout

## Overview

Functional and implementation information for the HTTP Callout policy is organized into the following sections:

* [Examples](template-policy-rework-structure-15.md#examples)
* [Configuration](template-policy-rework-structure-15.md#configuration)
* [Compatibility Matrix](template-policy-rework-structure-15.md#compatibility-matrix)
* [Errors](template-policy-rework-structure-15.md#errors)
* [Changelogs](template-policy-rework-structure-15.md#changelogs)

## Examples

You can use the `callout-http` policy to invoke an HTTP(S) URL and place a subset or all of the content in one or more variables of the request execution context.

This can be useful if you need some data from an external service and want to inject it during request processing.

The result of the callout is placed in a variable called `calloutResponse` and is only available during policy execution. If no variable is configured the result of the callout is no longer available.

{% tabs %}
{% tab title="Proxy API example" %}
{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

```
"policy-http-callout": {
    "method": "GET",
    "url": "https://api.gravitee.io/echo",
    "headers": [ {
        "name": "X-Gravitee-Request-Id",
        "value": "{#request.id}"
    }],
    "variables": [{
        "name": "my-server",
        "value": "{#jsonPath(#calloutResponse.content, '$.headers.X-Forwarded-Server')}"
    }]
}
```
{% endtab %}
{% endtabs %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
```json
"policy-http-callout": {
    "method": "GET",
    "url": "https://api.gravitee.io/echo",
    "headers": [ {
        "name": "X-Gravitee-Request-Id",
        "value": "{#request.id}"
    }],
    "variables": [{
        "name": "my-server",
        "value": "{#jsonPath(#calloutResponse.content, '$.headers.X-Forwarded-Server')}"
    }]
}
```
{% endcode %}

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>method</td><td>true</td><td>HTTP Method used to invoke URL</td><td>HTTP method</td><td>GET</td></tr><tr><td>useSystemProxy</td><td>true</td><td>Use the system proxy configured by your administrator</td><td>boolean</td><td>false</td></tr><tr><td>url</td><td>true</td><td>URL invoked by the HTTP client (support EL)</td><td>URL</td><td>-</td></tr><tr><td>headers</td><td>true</td><td>List of HTTP headers used to invoke the URL (support EL)</td><td>HTTP Headers</td><td>-</td></tr><tr><td>body</td><td>true</td><td>The body content send when calling the URL (support EL)</td><td>string</td><td>-</td></tr><tr><td>fireAndForget</td><td>true</td><td>Make the http call without expecting any response. When activating this mode, context variables and exit on error are useless.</td><td>boolean</td><td>false</td></tr><tr><td>variables</td><td>true</td><td>The variables to set in the execution context when retrieving content of HTTP call (support EL)</td><td>List of variables</td><td>-</td></tr><tr><td>exitOnError</td><td>true</td><td>Terminate the request if the error condition is true</td><td>boolean</td><td>false</td></tr><tr><td>errorCondition</td><td>true</td><td>The condition which will be verified to end the request (support EL)</td><td>string</td><td>{#calloutResponse.status >= 400 and #calloutResponse.status ⇐ 599}</td></tr><tr><td>errorStatusCode</td><td>true</td><td>HTTP Status Code sent to the consumer if the condition is true</td><td>int</td><td>500</td></tr><tr><td>errorContent</td><td>true</td><td>The body response of the error if the condition is true (support EL)</td><td>string</td><td></td></tr></tbody></table>

### System Proxy

If the option `useSystemProxy` is checked, proxy information will be read from `JVM_OPTS` or from the `gravitee.yml` file if `JVM_OPTS` is not set. The system properties are as follows:

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th></tr></thead><tbody><tr><td>system.proxy.host</td><td>true</td><td>Proxy Hostname or IP</td></tr><tr><td>system.proxy.port</td><td>true</td><td>The proxy port</td></tr><tr><td>system.proxy.type</td><td>true</td><td>The type of proxy (HTTP, SOCK4, SOCK5)</td></tr><tr><td>system.proxy.username</td><td>false</td><td>Username for proxy authentication if any</td></tr><tr><td>system.proxy.password</td><td>false</td><td>Password for proxy authentication if any</td></tr></tbody></table>

#### HTTP client proxy options

```
# global configuration of the http client
system:
  proxy:
    type: HTTP
    host: localhost
    port: 3128
    username: user
    password: secret
```

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the HTTP Callout policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution. The chart below summarizes this information in relation to the `callout-http` policy.

<table data-full-width="false"><thead><tr><th width="161.33333333333331">Plugin Version</th><th width="242">Supported APIM versions</th><th data-type="checkbox">Included in APIM default distribution</th></tr></thead><tbody><tr><td>>= 2.x</td><td>>=3.18</td><td>true</td></tr><tr><td>>= 1.15.x</td><td>3.15.x - 3.17.x</td><td>true</td></tr><tr><td>1.13.x - 1.14.x</td><td>3.10.x - 3.14.x</td><td>true</td></tr><tr><td>&#x3C;= 1.12.x</td><td>&#x3C;=3.9.x</td><td>true</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="210">Phase</th><th width="171">HTTP status code</th><th width="387">Error template key</th></tr></thead><tbody><tr><td>onRequest</td><td><code>500</code></td><td>An error occurred while invoking URL</td></tr><tr><td>onResponse</td><td><code>500</code></td><td>An error occurred while invoking URL</td></tr><tr><td>onRequestContent</td><td><code>500</code></td><td>An error occurred while invoking URL</td></tr><tr><td>onResponseContent</td><td><code>500</code></td><td>An error occurred while invoking URL</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-callout-http/blob/master/CHANGELOG.md" %}
