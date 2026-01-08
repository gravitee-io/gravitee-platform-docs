---
description: An overview about http signature.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/create-and-configure-apis/apply-policies/policy-reference/http-signature
---

# HTTP Signature

## Overview

HTTP Signature is a kind of authentication method which is adding a new level of security. By using this policy, the consumer is enforced to send a _signature_ which is used to identify the request temporarily and ensure that the request is really coming from the requesting consumer, using a secret key.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Sample policy configuration:

```json
{
  "http-signature": {
	"scheme":"AUTHORIZATION",
	"clockSkew":30,
	"secret":"my-passphrase",
	"algorithms":["HMAC_SHA256"],
	"enforceHeaders":["Date","Host"]
  }
}
```
{% endtab %}
{% endtabs %}

## Configuration

The "Signature" authentication scheme is based on the model that the client must authenticate itself with a digital signature produced by either a private asymmetric key (e.g., RSA) or a shared symmetric key (e.g., HMAC).

To authenticate, clients can use `Authorization` header or `Signature` header. For example:

* `Authorization: Signature "keyId="rsa-key-1",created=1630590825,expires=1630590831061,algorithm="hmac-sha256",headers="host",signature="Ib/KOuoDjyZPmLbKPvrnz+wj/kcEFZt5aPCxF4e7tO0="",`
* `Signature: "keyId="rsa-key-1",created=1630590825,expires=1630590831061,algorithm="hmac-sha256",headers="host",signature="Ib/KOuoDjyZPmLbKPvrnz+wj/kcEFZt5aPCxF4e7tO0="",`

{% hint style="info" %}
The current version of the policy does not support `Digest`, `(request-target)`, `Host`, and `Path` headers
{% endhint %}

### Phases

The phases checked below are supported by the `http-signature` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="203.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `http-signature` policy can be configured with the following options:

<table><thead><tr><th width="183">Property</th><th width="113" data-type="checkbox">Required</th><th width="248">Description</th><th width="136">Default</th><th>Example</th></tr></thead><tbody><tr><td>scheme</td><td>true</td><td>Signature Scheme (authorization header or signature header)</td><td>authorization</td><td>-</td></tr><tr><td>secret</td><td>true</td><td>The secret key used to generate and verify the signature (supports EL).</td><td>-</td><td>passphrase</td></tr><tr><td>algorithms</td><td>false</td><td>A list of supported HMAC digest algorithms.</td><td>-</td><td>-</td></tr><tr><td>enforceHeaders</td><td>false</td><td>List of headers the consumer must at least use for HTTP signature creation.</td><td>-</td><td>-</td></tr><tr><td>clockSkew</td><td>false</td><td>Clock Skew in seconds to prevent replay attacks.</td><td>30</td><td>-</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `http-signature` policy:

| Plugin version | Supported APIM versions |
| -------------- | ----------------------- |
| 1.x            | All                     |

## Errors

<table><thead><tr><th width="102.5">Code</th><th>Message</th></tr></thead><tbody><tr><td><code>401</code></td><td><ul><li>Missing or signature</li><li>Request does not contain headers part of the signature</li><li>Enforce HTTP headers not part of the signature</li></ul></td></tr></tbody></table>

To override the default response provided by the policy, use the response templates feature. These templates must be define at the API level (see `Response Templates` from the `Proxy` menu).

Below are the error keys sent by the `http-signature` policy:

<table><thead><tr><th width="360.5">Key</th><th>Parameters</th></tr></thead><tbody><tr><td>HTTP_SIGNATURE_INVALID_SIGNATURE</td><td>-</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-http-signature/blob/master/CHANGELOG.md" %}
