---
description: This page provides the technical details of the API Key policy
---

# API Key

You can use the `api-key` policy to enforce API key checks during request processing, allowing only apps with approved API keys to access your APIs.

This policy ensures that API keys are valid, have not been revoked or expired and are approved to consume the specific resources associated with your API.

Functional and implementation information for the Assign Content policy is organized into the following sections:

* [Examples](api-key.md#examples)
* [Configuration](api-key.md#configuration)
* [Compatibility Matrix](api-key.md#compatibility-matrix)
* [Errors](api-key.md#errors)
* [Changelogs](api-key.md#changelogs)

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
```json
"api-key": {
  "propagateApiKey": false
}
```
{% endcode %}

You can also configure the policy in the APIM Gateway configuration file (`gravitee.yml`). You can customize the `X-Gravitee-Api-Key` header and `api-key` query parameter.

```
policy:
  api-key:
    header: My-Custom-Api-Key
    param: custom-api-key
```

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td><code>propagateApiKey</code></td><td>false</td><td>Propagate API key to upstream API</td><td>boolean</td><td><em>false</em></td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the API Key policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution.&#x20;

## Errors

<table data-full-width="false"><thead><tr><th width="210">Phase</th><th width="171">Key</th></tr></thead><tbody><tr><td>onRequest</td><td>API_KEY_MISSING</td></tr><tr><td></td><td>API_KEY_INVALID_KEY</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-apikey/blob/master/CHANGELOG.md" %}
