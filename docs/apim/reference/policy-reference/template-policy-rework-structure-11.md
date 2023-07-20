---
description: This page provides the technical details of the HTTP Signature policy
---

# HTTP Signature

## Overview

Functional and implementation information for the HTTP Signature policy is organized into the following sections:

* [Examples](template-policy-rework-structure-11.md#examples)
* [Configuration](template-policy-rework-structure-11.md#configuration)
* [Compatibility Matrix](template-policy-rework-structure-11.md#compatibility-matrix)
* [Errors](template-policy-rework-structure-11.md#errors)
* [Changelogs](template-policy-rework-structure-11.md#changelogs)

## Examples

HTTP Signature is a kind of authentication method which is adding a new level of security. By using this policy, the consumer is enforced to send a _signature_ which is used to identify the request temporarily and ensure that the request is really coming from the requesting consumer, using a secret key.

The "Signature" authentication scheme is based on the model that the client must authenticate itself with a digital signature produced by either a private asymmetric key (e.g., RSA) or a shared symmetric key (e.g., HMAC).

You can use:

* Authorization header: For example: `Authorization: Signature "keyId="rsa-key-1",created=1630590825,expires=1630590831061,algorithm="hmac-sha256",headers="host",signature="Ib/KOuoDjyZPmLbKPvrnz+wj/kcEFZt5aPCxF4e7tO0="",`
* Signature header: For example, `Signature: "keyId="rsa-key-1",created=1630590825,expires=1630590831061,algorithm="hmac-sha256",headers="host",signature="Ib/KOuoDjyZPmLbKPvrnz+wj/kcEFZt5aPCxF4e7tO0="",`

{% hint style="info" %}
The current version of the policy does not support **Digest**, **(request-target)**, **Host** and **Path** headers
{% endhint %}

{% tabs %}
{% tab title="Proxy API example" %}
{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

```
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

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
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
{% endcode %}

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Default</th><th>Example</th></tr></thead><tbody><tr><td>scheme</td><td>true</td><td>Signature Scheme (authorization header or signature header)</td><td>authorization</td><td>-</td></tr><tr><td>secret</td><td>true</td><td>The secret key used to generate and verify the signature (supports EL).</td><td>-</td><td>passphrase</td></tr><tr><td>algorithms</td><td>false</td><td>A list of supported HMAC digest algorithms.</td><td>-</td><td>-</td></tr><tr><td>enforceHeaders</td><td>false</td><td>List of headers the consumer must at least use for HTTP signature creation.</td><td>-</td><td>-</td></tr><tr><td>clockSkew</td><td>false</td><td>Clock Skew in seconds to prevent replay attacks.</td><td>30</td><td>-</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the HTTP Signature policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution. The chart below summarizes this information in relation to the `http-signature` policy.

<table><thead><tr><th>Plugin version</th><th>Supported APIM versions</th><th data-type="checkbox">Included in APIM default distribution</th></tr></thead><tbody><tr><td>1.5 and upper</td><td>3.15.x to latest</td><td>true</td></tr><tr><td>Up to 1.4</td><td>Up to 3.14.x</td><td>true</td></tr></tbody></table>

## Errors

If you’re looking to override the default response provided by the policy, you can do it thanks to the response templates feature. These templates must be define at the API level (see `Response Templates` from the `Proxy` menu).

Here are the error keys send by this policy:

| Key                                 | Parameters |
| ----------------------------------- | ---------- |
| HTTP\_SIGNATURE\_INVALID\_SIGNATURE |            |

### Http status code

<table><thead><tr><th width="166.33333333333331">Phase</th><th>Code</th><th>Message</th></tr></thead><tbody><tr><td>onRequest</td><td><code>401</code></td><td><p>In case of:</p><p>* Missing or signature</p><p>* Request does not contain headers part of the signature</p><p>* Enforce HTTP headers not part of the signature</p></td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-http-signature/blob/master/CHANGELOG.md" %}
