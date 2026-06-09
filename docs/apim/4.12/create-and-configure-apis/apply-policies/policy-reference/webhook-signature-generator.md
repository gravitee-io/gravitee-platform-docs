---
description: An overview about webhook signature generator.
hidden: true
noIndex: true
---

# Webhook Signature Generator

## Overview

The Webhook Signature Generator policy computes an HMAC signature over the outbound HTTP response body or v4 API message content and writes the Base64-encoded signature to a configurable HTTP or message header. Use this policy to let downstream webhook receivers verify the authenticity of the payload using a shared secret.

The policy can optionally prepend a list of selected header values to the body or message content before computing the signature, joined by a configurable delimiter. The receiver must reconstruct the same input in the same order to validate the signature.

## Examples

{% hint style="warning" %}
This policy applies to v4 HTTP proxy APIs (response phase) and v4 message APIs (message response phase). It can't be applied to v2 APIs, v4 TCP proxy APIs, or to the request side of any API.
{% endhint %}

{% tabs %}
{% tab title="v4 HTTP proxy API example" %}
Sample policy configuration that signs the response body and writes the signature to `X-HMAC-Signature`:

```json
{
  "name": "Webhook Signature Generator",
  "policy": "webhook-signature-generator",
  "configuration": {
    "targetSignatureHeader": "X-HMAC-Signature",
    "schemeType": {
      "enabled": false
    },
    "secret": "mySecret",
    "algorithm": "HmacSHA256"
  }
}
```
{% endtab %}

{% tab title="v4 message API example" %}
Sample policy configuration that signs the message content together with the values of a prepended header, joined by `.`:

```json
{
  "name": "Webhook Signature Generator",
  "policy": "webhook-signature-generator",
  "configuration": {
    "targetSignatureHeader": "X-HMAC-Signature",
    "schemeType": {
      "enabled": true,
      "headersDelimiter": ".",
      "headers": ["my-custom-header-confluent"]
    },
    "secret": "{#dictionaries['webhook']['signing-secret']}",
    "algorithm": "HmacSHA256"
  }
}
```

The `secret` field supports Gravitee Expression Language, so the secret can be sourced from a dictionary or another EL expression instead of an inline literal.
{% endtab %}
{% endtabs %}

## Configuration

The policy computes the HMAC signature using the configured algorithm and secret. By default, the signature is computed only over the body or message content. When `schemeType.enabled` is `true`, the policy concatenates the configured header values, separated by `headersDelimiter`, prepends the result to the body or message content, and signs the combined input. The receiver must apply the same concatenation order and delimiter to validate the signature.

The result is Base64-encoded and written to the header named by `targetSignatureHeader`, replacing any existing value.

### Phases

The phases checked below are supported by the `webhook-signature-generator` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

### Options

You can configure the `webhook-signature-generator` policy with the following options:

<table data-full-width="false"><thead><tr><th width="200">Property</th><th width="100" data-type="checkbox">Required</th><th width="280">Description</th><th width="140">Default</th><th>Example</th></tr></thead><tbody><tr><td>targetSignatureHeader</td><td>true</td><td>HTTP or message header that receives the generated HMAC signature. Any existing value on this header is overwritten.</td><td>X-HMAC-Signature</td><td>-</td></tr><tr><td>schemeType.enabled</td><td>true</td><td>When <code>false</code>, the signature is computed only over the body or message content. When <code>true</code>, the values of <code>schemeType.headers</code> are concatenated with <code>schemeType.headersDelimiter</code>, prepended to the body, and signed together.</td><td>false</td><td>-</td></tr><tr><td>schemeType.headersDelimiter</td><td>false</td><td>Delimiter used to separate each header value and the body when <code>schemeType.enabled</code> is <code>true</code>.</td><td>.</td><td>-</td></tr><tr><td>schemeType.headers</td><td>false</td><td>List of HTTP or message header names whose values are prepended to the body before signing. Required when <code>schemeType.enabled</code> is <code>true</code>.</td><td>-</td><td>["my-custom-header-confluent"]</td></tr><tr><td>secret</td><td>true</td><td>Shared secret used to compute the HMAC signature. Supports Gravitee Expression Language.</td><td>-</td><td>mySecret</td></tr><tr><td>algorithm</td><td>true</td><td>HMAC algorithm. One of <code>HmacSHA1</code>, <code>HmacSHA256</code>, <code>HmacSHA384</code>, or <code>HmacSHA512</code>.</td><td>HmacSHA256</td><td>-</td></tr></tbody></table>

### Compatibility matrix

The following is the compatibility matrix for APIM and the `webhook-signature-generator` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>4.x+</td></tr></tbody></table>

### Errors

<table data-full-width="false"><thead><tr><th width="188">HTTP status code</th><th>Description</th></tr></thead><tbody><tr><td><code>500</code></td><td><ul><li>One of the headers listed in <code>schemeType.headers</code> is missing from the response or message, or <code>schemeType.enabled</code> is <code>true</code> but <code>schemeType.headers</code> is empty.</li><li>Signature generation fails because the payload can't be read or the secret and algorithm combination is invalid.</li></ul></td></tr></tbody></table>

You can override the default response provided by the policy via the response templates feature. These templates must be defined at the API level (see `Response Templates` from the `Proxy` menu). The following keys are sent by the `webhook-signature-generator` policy:

<table data-full-width="false"><thead><tr><th width="401">Key</th><th>Parameters</th></tr></thead><tbody><tr><td>WEBHOOK_SIGNATURE_ERROR</td><td>-</td></tr><tr><td>WEBHOOK_ADDITIONAL_HEADERS_NOT_VALID</td><td>-</td></tr></tbody></table>
