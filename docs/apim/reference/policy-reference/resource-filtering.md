---
description: This page provides the technical details of the Resource Filtering policy
---

# Resource Filtering

## Overview

You can use the `resource-filtering` policy to filter REST resources. By applying this filter, you can restrict or allow access to a specific resource determined by a path and a method (or an array of methods).

This policy is mainly used in plan configuration, to limit subscriber access to specific resources only.

A typical usage would be to allow access to all paths (`/**`) but in read-only mode (GET method).

Functional and implementation information for the `resource-filtering` policy is organized into the following sections:

* [Configuration](resource-filtering.md#configuration)
* [Compatibility Matrix](resource-filtering.md#compatibility-matrix)
* [Errors](resource-filtering.md#errors)
* [Changelogs](resource-filtering.md#changelogs)

{% hint style="warning" %}
This policy can be applied to [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines/) Currently, this policy can **not** be applied at the message level.
{% endhint %}

## Configuration

Sample policy configuration is shown below:

{% code title="Sample Configuration" %}
```json
"resource-filtering" : {
    "whitelist":[
        {
            "pattern":"/**",
            "methods": ["GET"]
        }
    ]
}
```
{% endcode %}

The implementation supports Ant style path patterns, where URL mapping matches URLs using the following rules:

* `?` matches one character
* `*` matches zero or more characters
* `**` matches zero or more directories in a path

### Phases

The phases checked below are supported by the `resource-filtering` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="135" data-type="checkbox">Compatible?</th><th width="203.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `resource-filtering` policy can be configured with the following options:

<table><thead><tr><th width="156">Property</th><th data-type="checkbox">Required</th><th width="243">Description</th><th width="155">Type</th><th>Default</th></tr></thead><tbody><tr><td>whitelist</td><td>false</td><td>List of allowed resources</td><td>array of <a href="https://docs.gravitee.io/apim/3.x/apim_policies_resource_filtering.html#gravitee-policy-resource-filtering-resource"><code>resources</code></a></td><td>-</td></tr><tr><td>blacklist</td><td>false</td><td>List of restricted resources</td><td>array of <a href="https://docs.gravitee.io/apim/3.x/apim_policies_resource_filtering.html#gravitee-policy-resource-filtering-resource"><code>resources</code></a></td><td>-</td></tr></tbody></table>

{% hint style="info" %}
You can’t apply whitelisting and blacklisting to the same resource. Whitelisting takes precedence over blacklisting.
{% endhint %}

A resource is defined as follows:

<table><thead><tr><th width="122">Property</th><th data-type="checkbox">Required</th><th width="230">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>pattern</td><td>true</td><td>An <a href="https://docs.gravitee.io/apim/3.x/apim_policies_resource_filtering.html#gravitee-policy-resource-filtering-ant">Ant-style path pattern</a> (<a href="http://ant.apache.org/">Apache Ant</a>).</td><td>string</td><td>-</td></tr><tr><td>methods</td><td>false</td><td>List of HTTP methods for which filter is applied.</td><td>array of HTTP methods</td><td>All HTTP methods</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `resource-filtering` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>All</td></tr></tbody></table>

## Errors

| HTTP status code | Message                                                                   |
| ---------------- | ------------------------------------------------------------------------- |
| `403`            | Access to the resource is forbidden according to resource-filtering rules |
| `405`            | Method not allowed while accessing this resource                          |

You can use the response template feature to override the default responses provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

The error keys sent by this policy are as follows:

<table><thead><tr><th width="428.5">Key</th><th>Parameters</th></tr></thead><tbody><tr><td>RESOURCE_FILTERING_FORBIDDEN</td><td>path - method</td></tr><tr><td>RESOURCE_FILTERING_METHOD_NOT_ALLOWED</td><td>path - method</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-resource-filtering/blob/master/CHANGELOG.md" %}
