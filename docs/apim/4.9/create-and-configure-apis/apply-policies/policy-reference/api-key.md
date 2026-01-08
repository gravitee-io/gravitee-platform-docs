---
description: An overview about api key.
metaLinks:
  alternates:
    - api-key.md
---

# API Key

## Overview

You can use the `api-key` policy to enforce API key checks during request processing, allowing only apps with approved API keys to access your APIs.

This policy ensures that API keys are valid, have not been revoked or expired and are approved to consume the specific resources associated with your API.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
You can configure the policy in the APIM Gateway configuration file (`gravitee.yml`). You can customize the `X-Gravitee-Api-Key` header and `api-key` query parameter.

```yaml
policy:
  api-key:
    header: My-Custom-Api-Key
    param: custom-api-key
```
{% endtab %}
{% endtabs %}

## Configuration

Sample policy configuration:

{% code title="Sample Configuration" %}
```json
"api-key": {
  "propagateApiKey": false
}
```
{% endcode %}

### Phases

The phases checked below are supported by the `api-key` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

You can configure the `api-key` policy with the following options:

<table><thead><tr><th width="191">Property</th><th width="100" data-type="checkbox">Required</th><th width="179">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>propagateApiKey</td><td>false</td><td>Propagate API key to upstream API</td><td>boolean</td><td><em>false</em></td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `assign-metrics` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>2.x</td><td>3.x</td></tr><tr><td>4.x</td><td>4.0+</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="230.3858267716535">Phase</th><th width="334">Key</th></tr></thead><tbody><tr><td>onRequest</td><td>API_KEY_MISSING</td></tr><tr><td></td><td>API_KEY_INVALID_KEY</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-apikey/blob/master/CHANGELOG.md" %}
