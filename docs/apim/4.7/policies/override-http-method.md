---
hidden: true
---

# Override HTTP Method

{% hint style="warning" %}
This feature requires [Gravitee's Enterprise Edition](../overview/enterprise-edition.md)
{% endhint %}

## Overview

You can use the `override-http-method` policy to override the HTTP method provided by the initial consumer with a new configured value when the inbound request is sent to the backend API.

This policy does not act on messages and only applies to the request phase of API flows.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
The Gravitee echo API returns a JSON response when a `GET` request is sent to [https://api.gravitee.io/echo](https://api.gravitee.io/echo). The response is formatted as follows:

{% code title="Default response" %}
```json
{
    "bodySize": 0,
    "headers": {
        "Accept": "*/*",
        "Host": "api.gravitee.io",
        "User-Agent": "{{user-agent-info}}",
        "X-Gravitee-Request-Id": "{{generated-request-id}}",
        "X-Gravitee-Transaction-Id": "{{generated-trx-id}}",
        "accept-encoding": "deflate, gzip"
    },
    "query_params": {}
}
```
{% endcode %}

This API would typically be called with just a `GET` request, but if a client tries to run a `PUT` request, they will get a [405 Method Not Allowed](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/405) response. If the API publisher wants to ensure consistent behavior regardless of HTTP method called (in this case, returning the standard response), then adding an `override-http-method` policy to convert the request from any method (e.g. `PUT`, `POST`, etc) to a `GET` request will ensure that the expected response above is always returned.
{% endtab %}
{% endtabs %}

## Configuration

Sample policy configuration:

{% code title="Sample Configuration" %}
```json
{
  "name": "Custom name",
  "description": "Overrides HTTP method",
  "policy": "policy-override-request-method",
  "configuration": {
    "method": "GET"
  }
```
{% endcode %}

### Phases

The phases checked below are supported by the `override-http-method` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `override-http-method` policy can be configured with the following options:

<table data-full-width="false"><thead><tr><th width="121">Property</th><th width="100" data-type="checkbox">Required</th><th width="156">Description</th><th width="94">Type<select></select></th><th width="149">Options</th></tr></thead><tbody><tr><td>method</td><td>true</td><td>HTTP method used regardless of method called</td><td></td><td>GET<br>POST<br>PUT<br>DELETE<br>PATCH<br>HEAD<br>CONNECT<br>OPTIONS<br>TRACE</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the`override-http-method` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>2.0 to 2.1</td><td>4.0+</td></tr><tr><td>Up to 1.x</td><td>Up to 3.20</td></tr></tbody></table>

## Errors

There are no out-of-the-box errors returned by this policy.

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-override-http-method/blob/master/CHANGELOG.md" %}
