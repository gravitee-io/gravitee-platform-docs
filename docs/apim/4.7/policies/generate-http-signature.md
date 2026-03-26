---
description: An overview about ---.
hidden: true
---

# Generate HTTP Signature

## Overview

HTTP Signature is an authentication method for adding additional security.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Sample policy configuration:

```json
{
  "generate-http-signature": {
	"scheme":"AUTHORIZATION",
	"validityDuration":30,
	"keyId":"my-key-id",
	"secret":"my-passphrase",
	"algorithm":"HMAC_SHA256",
	"headers":["X-Gravitee-Header","Host"],
    "created": true,
    "expires": true
  }
}
```
{% endtab %}
{% endtabs %}

## Configuration

The `Signature` authentication model requires the client to authenticate itself with a digital signature produced by either a private asymmetric key (e.g., RSA) or a shared symmetric key (e.g., HMAC).

To authenticate, clients can use `Authorization` header or `Signature` header. For example:

* `Authorization: Signature "keyId="rsa-key-1",created=1630590825,expires=1630590831061,algorithm="hmac-sha256",headers="host",signature="Ib/KOuoDjyZPmLbKPvrnz+wj/kcEFZt5aPCxF4e7tO0="",`
* `Signature: "keyId="rsa-key-1",created=1630590825,expires=1630590831061,algorithm="hmac-sha256",headers="host",signature="Ib/KOuoDjyZPmLbKPvrnz+wj/kcEFZt5aPCxF4e7tO0="",`

{% hint style="info" %}
The current version of the policy does not support `Digest`, (`request-target)`, `Host`, or `Path` headers.
{% endhint %}

Sample policy configuration is shown below:

{% code title="Sample Configuration" %}
```json
{
  "name": "Custom name",
  "description": "Adds HTTP signature auth",
  "policy": "generate-http-signature",
  "configuration": {
	"scheme": "AUTHORIZATION",
	"validityDuration": 30,
	"keyId": "my-key-id",
	"secret": "my-passphrase",
	"algorithm": "HMAC_SHA256",
	"headers": ["X-Gravitee-Header","Host"],
    	"created": true,
   	"expires": true
  }
}
```
{% endcode %}

### Phases

The phases checked below are supported by the `generate-http-signature` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

You can configure the `generate-http-signature` policy with the following options:

<table data-full-width="false"><thead><tr><th width="175">Property</th><th width="103" data-type="checkbox">Required</th><th width="232">Description</th><th width="156">Default</th><th>Example</th></tr></thead><tbody><tr><td>scheme</td><td>true</td><td>Signature Scheme (authorization header or signature header)</td><td>authorization</td><td>-</td></tr><tr><td>keyId</td><td>true</td><td>The key ID used to generate the signature (supports EL)</td><td>-</td><td>rsa-key-1</td></tr><tr><td>secret</td><td>true</td><td>The secret key used to generate and verify the signature (supports EL)</td><td>-</td><td>passphrase</td></tr><tr><td>algorithm</td><td>true</td><td>The HMAC digest algorithm</td><td>HMAC_SHA256</td><td>-</td></tr><tr><td>headers</td><td>false</td><td>List of headers to build the signature. If no headers, the request must at least contains <code>Date</code> header.</td><td>-</td><td>-</td></tr><tr><td>created</td><td>true</td><td>Include the created timestamp in the signature and (created) header</td><td>true</td><td>-</td></tr><tr><td>expires</td><td>true</td><td>Include the expires timestamp in the signature and (expires) header</td><td>true</td><td>-</td></tr><tr><td>validityDuration</td><td>false</td><td>Signature’s maximum validation duration in seconds (minimum is 1). Applied when <code>expires</code> is set to true.</td><td>3</td><td>-</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `generate-http-signature` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>Up to 1.x</td><td>All</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="188">HTTP status code</th><th>Description</th></tr></thead><tbody><tr><td><code>400</code></td><td><ul><li>Request does not contain every header in the configuration headers list.</li><li>Request does not contain <code>Date</code> header and the configuration headers list is empty. Policy needs at least <code>Date</code> header to create a signature.</li><li>Unable to sign because of bad configuration.</li></ul></td></tr></tbody></table>

You can override the default response provided by the policy via the response templates feature. These templates must be defined at the API level (see `Response Templates` from the `Proxy` menu). The following keys are sent by the `generate-http-signature` policy:

<table data-full-width="false"><thead><tr><th width="401">Key</th><th>Parameters</th></tr></thead><tbody><tr><td>HTTP_SIGNATURE_IMPOSSIBLE_GENERATION</td><td>-</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-generate-http-signature/blob/master/CHANGELOG.md" %}
