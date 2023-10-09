---
description: This page provides the technical details of the Assign Content policy
---

# Assign Content

## Overview

You can use the `assign-content` policy to change or transform the content of the request body or response body.

This policy is compatible with the [Freemarker](https://freemarker.apache.org/) template engine, which allows you to apply complex transformations, such as transforming from XML to JSON and vice versa.

By default, you can access multiple objects from the template context: request and response bodies, dictionaries, context attributes and more.

Functional and implementation information for the `assign-content` policy is organized into the following sections:

* [Examples](assign-content.md#examples)
* [Configuration](assign-content.md#configuration)
* [Compatibility Matrix](assign-content.md#compatibility-matrix)
* [Errors](assign-content.md#errors)
* [Changelogs](assign-content.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to all Gravitee APIs: v2 APIs, v4 proxy APIs, and v4 message APIs.
{% endhint %}

{% tabs %}
{% tab title="Proxy API" %}
You could use the Assign Content policy to inject a dictionary value and application into the request payload:

```
{
  "example": "${context.dictionaries['my-dictionary']['my-value']}",
  "application": "${context.attributes['application']}"
}
```
{% endtab %}

{% tab title="Message API" %}
You could use the Assign Content policy to inject a dictionary value and metadata into the message:

```
{
  "example": "${message.dictionaries['my-dictionary']['my-value']}",
  "metadata": "${message.attributes['metadata']}"
}
```
{% endtab %}
{% endtabs %}

## Configuration

Sample policy configuration is shown below:

{% code title="Sample Configuration" %}
```json
"policy-assign-content": {
    "scope":"REQUEST",
    "body":"Put your content here"
}
```
{% endcode %}

### Phases

The phases checked below are supported by the `assign-content` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

### Options

You can configure the `assign-content` policy with the following options:

<table><thead><tr><th width="121">Property</th><th width="101" data-type="checkbox">Required</th><th width="202">Description</th><th width="87">Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>true</td><td>The execution scope of the policy</td><td>scope</td><td><code>REQUEST</code></td></tr><tr><td>body</td><td>true</td><td>The data to push as request or response body content</td><td>string</td><td>-</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `assign-content` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>Up to 1.6.x</td><td>Up to 3.9.x</td></tr><tr><td>1.7.x</td><td>3.10.x to 3.20.x</td></tr><tr><td>2.x</td><td>4.0+</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="210">Phase</th><th width="171">HTTP status code</th><th width="387">Error template key</th></tr></thead><tbody><tr><td>onRequestContent</td><td><code>500</code></td><td>The body content cannot be transformed.</td></tr><tr><td>onResponseContent</td><td><code>500</code></td><td>The body content cannot be transformed.</td></tr><tr><td>onMessageRequest</td><td><code>400</code></td><td>The body content cannot be transformed.</td></tr><tr><td>onMessageResponse</td><td><code>500</code></td><td>The body content cannot be transformed.</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-assign-content/blob/master/CHANGELOG.md" %}
