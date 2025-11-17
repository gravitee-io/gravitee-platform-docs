---
hidden: true
---

# Custom Query Parameters Parser

## Overview

You can use the `custom-query-parameters-parser` policy to:

* Set variables such as request attributes and other execution context attributes
* Change the way query parameters are extracted

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

## Configuration

When configuring the `custom-query-parameters-parser` policy, note the following:

* The semicolon character (`;`) is not considered to be a separator, e.g., `http://host:port/my-api?filter=field1;field2` will be computed with the query parameter `filter: ['field1;field']`
* Policies are executed after flow evaluation. For a condition on a flow using [EL](../getting-started/gravitee-expression-language.md) to test query parameters, they will be extracted by the Gateway using `;` as a separator.

### Phases

The phases checked below are supported by the `custom-query-parameters-parser` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `custom-query-parameters-parser` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>Up to 1.x</td><td>3.20.x</td></tr><tr><td>2.x</td><td>4.0.x to latest</td></tr></tbody></table>

## Errors

The error keys sent by these policies are as follows:

<table><thead><tr><th width="291.5">HTTP error code</th><th>Message</th></tr></thead><tbody><tr><td><code>500</code></td><td>An error occurred while extracting query parameters from the request URL</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-custom-query-parameters-parser/blob/master/CHANGELOG.md" %}
