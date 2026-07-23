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

Configure the default API key header and query parameter for the whole Gateway in the `gravitee.yml` configuration file:

```yaml
policy:
  api-key:
    header: My-Custom-Api-Key
    param: custom-api-key
```

## API key header resolution

When the API key is read from a header, which is the default, the Gateway resolves the header name in the following order:

1. The `apiKeyHeader` value configured on the plan, when that value isn't empty.
2. The `policy.api-key.header` value from `gravitee.yml`, when the plan doesn't set a header name.
3. The default `X-Gravitee-Api-Key` header.

When the resolved header carries no key, the Gateway falls back to the `api-key` query parameter. Set the query parameter name for the whole Gateway with `policy.api-key.param`. A plan can't override the query parameter name.

APIM 4.11.14 and later, and every 4.12 and later release, bundle version 6.x of the policy. From that version, the header name set on the plan applies when it isn't empty, and the `enableCustomApiKeyHeader` option is deprecated. Earlier versions apply the header name set on the plan only when `enableCustomApiKeyHeader` is `true`, and that option defaults to `false`. Keep the option enabled for Gateways that still run version 5.x of the policy, and for V2 APIs that don't run on the emulation engine. For the upgrade impact, see [Breaking Changes and Deprecations](../../../release-information/breaking-changes-and-deprecations.md).

## Configuration

Sample policy configuration:

{% code title="Sample Configuration" %}
```json
"api-key": {
  "propagateApiKey": false,
  "apiKeyHeader": "My-Custom-Api-Key"
}
```
{% endcode %}

### Phases

The phases checked below are supported by the `api-key` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

You can configure the `api-key` policy with the following options:

<table>
    <thead>
        <tr>
            <th width="191">Property</th>
            <th width="100" data-type="checkbox">Required</th>
            <th width="179">Description</th>
            <th>Type</th>
            <th>Default</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>propagateApiKey</td>
            <td>false</td>
            <td>Propagate API key to upstream API</td>
            <td>boolean</td>
            <td><em>false</em></td>
        </tr>
        <tr>
            <td>apiKeyHeader</td>
            <td>false</td>
            <td>Name of the header that carries the API key. Takes precedence over the Gateway-level <code>policy.api-key.header</code> value</td>
            <td>string</td>
            <td><em>X-Gravitee-Api-Key</em></td>
        </tr>
        <tr>
            <td>enableCustomApiKeyHeader</td>
            <td>false</td>
            <td>Deprecated. Applies the header name set on the plan when the Gateway runs version 5.x of the policy</td>
            <td>boolean</td>
            <td><em>false</em></td>
        </tr>
    </tbody>
</table>

## Compatibility matrix

The following table shows the compatibility between the `api-key` policy and APIM:

<table data-full-width="false">
    <thead>
        <tr>
            <th>Plugin Version</th>
            <th>Supported APIM versions</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>2.x</td>
            <td>3.x</td>
        </tr>
        <tr>
            <td>4.x</td>
            <td>4.0.x to 4.5.x</td>
        </tr>
        <tr>
            <td>5.x</td>
            <td>4.6.x to 4.10.x</td>
        </tr>
        <tr>
            <td>6.x</td>
            <td>4.11.x to latest</td>
        </tr>
    </tbody>
</table>

## Errors

<table data-full-width="false"><thead><tr><th width="230.3858267716535">Phase</th><th width="334">Key</th></tr></thead><tbody><tr><td>onRequest</td><td>API_KEY_MISSING</td></tr><tr><td></td><td>API_KEY_INVALID_KEY</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-apikey/blob/master/CHANGELOG.md" %}
