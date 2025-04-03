---
description: This page provides the technical details of the URL Rewriting policy
hidden: true
---

# URL Rewriting

## Overview

You can use the `url-rewriting` policy to rewrite URLs from an HTTP response header or response body.

Functional and implementation information for the `url-rewriting` policy is organized into the following sections:

* [Examples](url-rewriting.md#examples)
* [Configuration](url-rewriting.md#configuration)
* [Compatibility Matrix](url-rewriting.md#compatibility-matrix)
* [Changelogs](url-rewriting.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Sample policy configuration:

```json
"url-rewriting": {
    "rewriteResponseHeaders": true,
    "rewriteResponseBody": true,
    "fromRegex": "https?://[^\/]*\/((?>\w|\d|\-|\/|\?|\=|\&)*)",
    "toReplacement": "https://apis.gravitee.io/{#group[0]}"
}
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `url-rewriting` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `url-rewriting` policy can be configured with the following options:

<table><thead><tr><th width="272">Property</th><th data-type="checkbox">Required</th><th width="226">Description</th><th width="136">Type</th><th>Default</th></tr></thead><tbody><tr><td><code>rewriteResponseHeaders</code></td><td>true</td><td>Rewrite the value of HTTP response headers</td><td>boolean</td><td>true</td></tr><tr><td><code>rewriteResponseBody</code></td><td>true</td><td>Rewrite the HTTP response body</td><td>boolean</td><td>true</td></tr><tr><td><code>fromRegex</code></td><td>true</td><td>The regex pattern for matching URLs</td><td>string (regex)</td><td>true</td></tr><tr><td><code>toReplacement</code></td><td>true</td><td>The value used to replace matching URLs (supports Expression Language)</td><td>string</td><td>true</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `url-rewriting` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>All supported versions</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-url-rewriting/blob/master/CHANGELOG.md" %}
