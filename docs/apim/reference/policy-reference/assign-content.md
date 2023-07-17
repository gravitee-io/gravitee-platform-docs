---
description: This page provides the technical details of the Assign Content policy
---

# Assign Content

You can use the `assign-content` policy to change or transform the content of the request body or response body.

This policy is compatible with the [Freemarker](https://freemarker.apache.org/) template engine, which allows you to apply complex transformations, such as transforming from XML to JSON and vice versa.

By default, you can access multiple objects from the template context — request and response bodies, dictionaries, context attributes and more.

Functional and implementation information for the Assign Content policy is organized into the following sections:

* [Examples](assign-content.md#examples)
* [Configuration](assign-content.md#configuration)
* [Compatibility Matrix](assign-content.md#compatibility-matrix)
* [Errors](assign-content.md#errors)
* [Changelogs](assign-content.md#changelogs)

## Examples

{% tabs %}
{% tab title="Proxy API" %}
{% hint style="info" %}
The proxy API example also applies to v2 APIs.
{% endhint %}

For example, you could use the Assign Content policy to inject a dictionary value and application into the request payload

```
{
  "example": "${context.dictionaries['my-dictionary']['my-value']}",
  "application": "${context.attributes['application']}"
}
```
{% endtab %}

{% tab title="Message API" %}

{% endtab %}
{% endtabs %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
```json
"policy-assign-content": {
    "scope":"REQUEST",
    "body":"Put your content here"
}
```
{% endcode %}

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>true</td><td>The execution scope of the policy.</td><td>scope</td><td>REQUEST</td></tr><tr><td>body</td><td>true</td><td>The data to push as request or response body content.</td><td>string</td><td>-</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](./#phases) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the Assign Content policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution. The chart below summarizes this information in relation to the `json-xml` policy.

<table data-full-width="false"><thead><tr><th width="161.33333333333331">Plugin Version</th><th width="242">Supported APIM versions</th><th data-type="checkbox">Included in APIM default distribution</th></tr></thead><tbody><tr><td>>= 1.7.x</td><td>>=3.10</td><td>true</td></tr><tr><td>&#x3C;=1.6.x</td><td>&#x3C;=3.9</td><td>true</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="210">Phase</th><th width="171">HTTP status code</th><th width="387">Error template key</th></tr></thead><tbody><tr><td>onRequestContent</td><td><code>500</code></td><td>The body content cannot be transformed.</td></tr><tr><td>onResponseContent</td><td><code>500</code></td><td>The body content cannot be transformed.</td></tr><tr><td>onMessageRequest</td><td><code>400</code></td><td>The body content cannot be transformed.</td></tr><tr><td>onMessageResponse</td><td><code>500</code></td><td>The body content cannot be transformed.</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-assign-content/blob/master/CHANGELOG.md" %}
