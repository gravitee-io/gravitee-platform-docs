---
description: This page provides the technical details of the Generate HTTP Signature policy
---

# Generate HTTP Signature

## Overview

HTTP Signature is an authentication method for adding additional security.

The `Signature` authentication model requires the client to authenticate itself with a digital signature produced by either a private asymmetric key (e.g., RSA) or a shared symmetric key (e.g., HMAC).

To authenticate, clients can use:

* `Authorization` header: For example: `Authorization: Signature "keyId="rsa-key-1",created=1630590825,expires=1630590831061,algorithm="hmac-sha256",headers="host",signature="Ib/KOuoDjyZPmLbKPvrnz+wj/kcEFZt5aPCxF4e7tO0="",`
* `Signature` header: For example, `Signature: "keyId="rsa-key-1",created=1630590825,expires=1630590831061,algorithm="hmac-sha256",headers="host",signature="Ib/KOuoDjyZPmLbKPvrnz+wj/kcEFZt5aPCxF4e7tO0="",`

{% hint style="info" %}
The current version of the policy does not support `Digest`, `request-target`, `Host`, or `Path` headers.
{% endhint %}

Functional and implementation information for the `generate-http-signature` policy is organized into the following sections:

* [Examples](generate-http-signature.md#examples)
* [Configuration](generate-http-signature.md#configuration)
* [Errors](generate-http-signature.md#errors)
* [Changelogs](generate-http-signature.md#changelogs)

## Examples

{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines/) Currently, this policy can **not** be applied at the message level.
{% endhint %}

{% tabs %}
{% tab title="Proxy API example" %}
```
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

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

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

### Options

You can configure the `generate-http-signature` policy with the following options:

<table data-full-width="false"><thead><tr><th width="139">Property</th><th width="103" data-type="checkbox">Required</th><th width="264">Description</th><th width="128" data-type="select">Type</th><th width="169">Options</th><th>Default</th></tr></thead><tbody><tr><td>scheme</td><td>true</td><td>Signature Scheme (authorization header or signature header)</td><td></td><td>AUTHORIZATION, SIGNATURE</td><td>AUTHORIZATION</td></tr><tr><td>keyId</td><td>true</td><td>The key ID used to generate the signature (supports EL)</td><td></td><td>N/a</td><td>N/a</td></tr><tr><td>secret</td><td>true</td><td>The secret key used to generate and verify the signature (supports EL)</td><td></td><td>N/a</td><td>N/a</td></tr><tr><td>algorithm</td><td>true</td><td>The HMAC digest algorithm</td><td></td><td>N/a</td><td>HMAC_SHA256</td></tr><tr><td>headers</td><td>false</td><td>List of headers to build the signature. If no headers, the request must at least contains <code>Date</code> header.</td><td></td><td>N/a</td><td>N/a</td></tr><tr><td>created</td><td>true</td><td>Include the created timestamp in the signature and (created) header</td><td></td><td>true, false</td><td>true</td></tr><tr><td>expires</td><td>true</td><td>Include the expires timestamp in the signature and (expires) header</td><td></td><td>true, false</td><td>true</td></tr><tr><td>validityDuration</td><td>false</td><td>Signature’s maximum validation duration in seconds (minimum is 1). Applied when <code>expires</code> is set to true.</td><td></td><td>N/a</td><td>3</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines/). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the `generate-http-signature` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Errors

<table data-full-width="false"><thead><tr><th width="137">Phase</th><th width="128">HTTP status code</th><th width="177">Error template key</th><th>Description</th></tr></thead><tbody><tr><td>onRequest</td><td><code>400</code></td><td>HTTP_SIGNATURE_IMPOSSIBLE_GENERATION</td><td><p>In case of:</p><ul><li>Request does not contain every header in the configuration headers list.</li><li>Request does not contain <code>Date</code> header and the configuration headers list is empty. Policy needs at least <code>Date</code> header to create a signature.</li><li>Unable to sign because of bad configuration.</li></ul></td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-generate-http-signature/blob/master/CHANGELOG.md" %}
