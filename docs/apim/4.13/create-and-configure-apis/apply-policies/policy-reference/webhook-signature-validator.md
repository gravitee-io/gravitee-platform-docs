---
description: The Webhook Signature Validator policy checks the HMAC signature of an incoming request in API Management 4.13. Learn how to set it.
---

# Webhook Signature Validator

## Overview

The Webhook Signature Validator policy checks the HMAC signature that a webhook sender attaches to a request. It computes its own signature over the request body with a shared secret, and lets the request through only when the two signatures match. Otherwise, it rejects the request with a `401` status.

The policy can include the values of selected headers in the signed input. When **Replay Protection** is enabled, it also rejects requests whose signed timestamp is too old or too far in the future. It checks signatures produced by the [Webhook Signature Generator](webhook-signature-generator.md) policy, or by any sender that builds the signed input the same way.

{% hint style="info" %}
This policy isn't included in the APIM distribution. Download the plugin archive from [download.gravitee.io](https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-validate-webhook-signature/), and then deploy it. For more information, see [Deployment](../../../plugins/deployment.md).
{% endhint %}

## Examples

{% hint style="warning" %}
This policy applies to the request phase of v2 APIs and v4 HTTP proxy APIs. It can't be applied to v4 message APIs, v4 TCP proxy APIs, or the response side of any API.
{% endhint %}

Sample policy configuration that checks a signature computed over a timestamp, one header value, and the request body:

```json
{
  "name": "Webhook Signature Validator",
  "policy": "webhook-signature-validator",
  "configuration": {
    "sourceSignatureHeader": "{#request.headers['X-HMAC-Signature'][0]}",
    "schemeType": {
      "enabled": true,
      "headersDelimiter": ".",
      "headers": ["X-Event-Id"]
    },
    "timestampValidity": {
      "enabled": true,
      "sourceTimestampHeader": "X-HMAC-Timestamp",
      "delimiter": ".",
      "maxSignatureAge": 300,
      "clockSkew": 60
    },
    "secret": "{#dictionaries['webhook']['signing-secret']}",
    "algorithm": "HmacSHA256"
  }
}
```

The `secret` field supports Gravitee Expression Language, so the secret can be sourced from a dictionary or another EL expression instead of an inline literal.

## Configuration

The policy reads the signature to check by evaluating `sourceSignatureHeader`, and then rebuilds the signed input from the request:

* By default, the signed input is the request body.
* When `schemeType.enabled` is `true`, the values of the headers listed in `schemeType.headers`, each followed by `schemeType.headersDelimiter`, are prepended to the body.
* When `timestampValidity.enabled` is `true`, the value of the `timestampValidity.sourceTimestampHeader` header, followed by `timestampValidity.delimiter`, is prepended to the result.

For example, with both options enabled, the default delimiters, and one header, the signed input is `<timestamp>.<header value>.<body>`. That's the input the Webhook Signature Generator policy signs with the same settings.

The policy computes the HMAC of the signed input with `secret` and `algorithm`, Base64-encodes it, and compares it with the signature. When **Replay Protection** is enabled, the policy also rejects a request whose timestamp is older than `timestampValidity.maxSignatureAge` seconds, or ahead of the Gateway's clock by more than `timestampValidity.clockSkew` seconds.

### Phases

The phases checked below are supported by the `webhook-signature-validator` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

You can configure the `webhook-signature-validator` policy with the following options:

<table data-full-width="false"><thead><tr><th width="200">Property</th><th width="100" data-type="checkbox">Required</th><th width="280">Description</th><th width="140">Default</th><th>Example</th></tr></thead><tbody><tr><td>sourceSignatureHeader</td><td>true</td><td>Gravitee Expression Language expression that returns the signature to check, Base64-encoded.</td><td>{#request.headers['X-HMAC-Signature'][0]}</td><td>-</td></tr><tr><td>schemeType.enabled</td><td>true</td><td>When <code>false</code>, the signed input is the request body only. When <code>true</code>, the values of <code>schemeType.headers</code> are prepended to the body.</td><td>false</td><td>-</td></tr><tr><td>schemeType.headersDelimiter</td><td>false</td><td>Delimiter that follows each header value in the signed input. It must match the one the sender used.</td><td>.</td><td>-</td></tr><tr><td>schemeType.headers</td><td>false</td><td>List of request header names whose values are prepended to the body. Required when <code>schemeType.enabled</code> is <code>true</code>.</td><td>-</td><td>["X-Event-Id"]</td></tr><tr><td>timestampValidity.enabled</td><td>false</td><td>When <code>true</code>, the policy requires a timestamp header, checks its age, and includes it in the signed input.</td><td>false</td><td>-</td></tr><tr><td>timestampValidity.sourceTimestampHeader</td><td>false</td><td>Request header that carries the timestamp, in epoch seconds. Required when <code>timestampValidity.enabled</code> is <code>true</code>.</td><td>X-HMAC-Timestamp</td><td>-</td></tr><tr><td>timestampValidity.delimiter</td><td>false</td><td>Delimiter between the timestamp and the rest of the signed input. It must match the one the sender used.</td><td>.</td><td>-</td></tr><tr><td>timestampValidity.maxSignatureAge</td><td>false</td><td>Maximum age of the timestamp, in seconds.</td><td>300</td><td>-</td></tr><tr><td>timestampValidity.clockSkew</td><td>false</td><td>How far ahead of the Gateway's clock the timestamp can be, in seconds.</td><td>60</td><td>-</td></tr><tr><td>secret</td><td>true</td><td>Shared secret used to compute the HMAC signature. Supports Gravitee Expression Language.</td><td>-</td><td>mySecret</td></tr><tr><td>algorithm</td><td>true</td><td>HMAC algorithm. One of <code>HmacSHA1</code>, <code>HmacSHA256</code>, <code>HmacSHA384</code>, or <code>HmacSHA512</code>.</td><td>HmacSHA256</td><td>-</td></tr></tbody></table>

### Errors

<table data-full-width="false"><thead><tr><th width="188">HTTP status code</th><th>Description</th></tr></thead><tbody><tr><td><code>401</code></td><td><ul><li>The <code>sourceSignatureHeader</code> expression returns no value (<code>WEBHOOK_SIGNATURE_NOT_FOUND</code>).</li><li><code>schemeType.enabled</code> is <code>true</code> but <code>schemeType.headers</code> is empty, or one of the listed headers is missing from the request (<code>WEBHOOK_ADDITIONAL_HEADERS_NOT_VALID</code>).</li><li>The timestamp header is missing or empty (<code>WEBHOOK_SIGNATURE_TIMESTAMP_NOT_FOUND</code>).</li><li>The timestamp isn't a number (<code>WEBHOOK_SIGNATURE_TIMESTAMP_INVALID</code>).</li><li>The timestamp is older than <code>timestampValidity.maxSignatureAge</code> (<code>WEBHOOK_SIGNATURE_TIMESTAMP_EXPIRED</code>).</li><li>The timestamp is ahead of the Gateway's clock by more than <code>timestampValidity.clockSkew</code> (<code>WEBHOOK_SIGNATURE_TIMESTAMP_IN_FUTURE</code>).</li><li>The policy can't compute the signature, for example because the secret or the algorithm is invalid (<code>WEBHOOK_SIGNATURE_GENERATION_FAILED</code>).</li><li>The computed signature doesn't match the one in the request (<code>WEBHOOK_SIGNATURE_INVALID_SIGNATURE</code>).</li></ul></td></tr></tbody></table>

You can override the default response with a response template defined at the API level. The policy sends the following keys:

<table data-full-width="false"><thead><tr><th width="401">Key</th><th>Parameters</th></tr></thead><tbody><tr><td>WEBHOOK_SIGNATURE_NOT_FOUND</td><td>-</td></tr><tr><td>WEBHOOK_ADDITIONAL_HEADERS_NOT_VALID</td><td>-</td></tr><tr><td>WEBHOOK_SIGNATURE_TIMESTAMP_NOT_FOUND</td><td>-</td></tr><tr><td>WEBHOOK_SIGNATURE_TIMESTAMP_INVALID</td><td>-</td></tr><tr><td>WEBHOOK_SIGNATURE_TIMESTAMP_EXPIRED</td><td>-</td></tr><tr><td>WEBHOOK_SIGNATURE_TIMESTAMP_IN_FUTURE</td><td>-</td></tr><tr><td>WEBHOOK_SIGNATURE_GENERATION_FAILED</td><td>-</td></tr><tr><td>WEBHOOK_SIGNATURE_INVALID_SIGNATURE</td><td>-</td></tr></tbody></table>
