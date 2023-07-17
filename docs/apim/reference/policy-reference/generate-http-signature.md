---
layout:
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
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

### Example

{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

If an API is configured with the Generate HTTP Signature policy, a request with invalid credentials will result in the following response:

{% code title="Default response" %}
```json
```
{% endcode %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies through the Policy Studio in the Management Console or interacting directly with the Management API.

{% tabs %}
{% tab title="Management Console" %}
<mark style="color:yellow;">We should wait to make these once the v4 Policy Studio is finalized</mark>
{% endtab %}

{% tab title="Managment API" %}
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
{% endtab %}
{% endtabs %}

### Reference

<table data-full-width="true"><thead><tr><th width="139">Property</th><th width="103" data-type="checkbox">Required</th><th width="264">Description</th><th width="128" data-type="select">Type</th><th width="169">Options</th><th>Default</th></tr></thead><tbody><tr><td>scheme</td><td>true</td><td>Signature Scheme (authorization header or signature header)</td><td></td><td>AUTHORIZATION, SIGNATURE</td><td>AUTHORIZATION</td></tr><tr><td>keyId</td><td>true</td><td>The key ID used to generate the signature (supports EL)</td><td></td><td>N/a</td><td>N/a</td></tr><tr><td>secret</td><td>true</td><td>The secret key used to generate and verify the signature (supports EL)</td><td></td><td>N/a</td><td>N/a</td></tr><tr><td>algorithm</td><td>true</td><td>The HMAC digest algorithm</td><td></td><td>N/a</td><td>HMAC_SHA256</td></tr><tr><td>headers</td><td>false</td><td>List of headers to build the signature. If no headers, the request must at least contains <code>Date</code> header.</td><td></td><td>N/a</td><td>N/a</td></tr><tr><td>created</td><td>true</td><td>Include the created timestamp in the signature and (created) header</td><td></td><td>true, false</td><td>true</td></tr><tr><td>expires</td><td>true</td><td>Include the expires timestamp in the signature and (expires) header</td><td></td><td>true, false</td><td>true</td></tr><tr><td>validityDuration</td><td>false</td><td>Signature’s maximum validation duration in seconds (minimum is 1). Applied when <code>expires</code> is set to true.</td><td></td><td>N/a</td><td>3</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. Depending on the [version of the Gateway API](../../overview/gravitee-api-definitions-and-execution-engines.md#policy-execution-phases-and-execution-order), the request and response are broken up into what are known as _phases_. Each policy has different compatibility with the available phases:

{% tabs %}
{% tab title="v4 API definition" %}
v4 APIs have the following phases:

* `onRequest`: This phase is executed before invoking the backend services for both proxy and message APIs. Policies can act on the headers and the content for proxy APIs.
* `onMessageRequest`: This phase occurs after the `onRequest` phase and allows policies to act on each incoming message before being sent to the backend service. This only applies to message APIs.
* `onResponse`: This phase is executed after invoking the backend services for both proxy and message APIs. Policies can act on the headers and the content for proxy APIs.
* `onMessageResponse`: This phase after the `onResponse` phase and allows policies to act on each outgoing message before being sent to the client application. This only applies to message APIs.

This policy is compatible with the following v4 API phases:

<table data-full-width="false"><thead><tr><th width="138" data-type="checkbox">onRequest</th><th width="134" data-type="checkbox">onResponse</th><th data-type="checkbox">onMessageRequest</th><th data-type="checkbox">onMessageResponse</th></tr></thead><tbody><tr><td>true</td><td>false</td><td>false</td><td>false</td></tr></tbody></table>
{% endtab %}

{% tab title="v2 API definition" %}
v2 APIs have the following phases:

* `onRequest`: This phase only allows policies to work on request headers. It never accesses the request body.
* `onRequestContent`: This phase always occurs after the `onRequest` phase. It allows policies to work at the content level and access the request body.
* `onResponse`: This phase only allows policies to work on response headers. It never accesses the response body.
* `onResponseContent`: This phase always occurs after the `onResponse` phase. It allows policies to work at the content level and access the response body.

This policy supports the following phases:

<table><thead><tr><th width="134" data-type="checkbox">onRequest</th><th width="144" data-type="checkbox">onResponse</th><th width="191" data-type="checkbox">onRequestContent</th><th data-type="checkbox">onResponseContent</th></tr></thead><tbody><tr><td>true</td><td>false</td><td>false</td><td>false</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

## Compatibility matrix

In the [changelog for each version of APIM](../../releases-and-changelog/changelog/), we provide a list of policies included in the default distribution. The chart below summarizes this information in relation to the `json-xml` policy.

<table data-full-width="false"><thead><tr><th width="161.33333333333331">Plugin Version</th><th width="242">Supported APIM versions</th><th>Included in APIM default distribution</th></tr></thead><tbody><tr><td>2.2</td><td>>=3.20</td><td>>=3.21</td></tr><tr><td>2.1</td><td>^3.0</td><td>>=3.0 &#x3C;3.21</td></tr><tr><td>2.0</td><td>^3.0</td><td>N/a</td></tr></tbody></table>

## Installation and deployment

Each version of APIM includes a number of policies by default. If the policy is not included in the default distribution or you would like to use a different version of the policy, you can modify the plugin.

{% hint style="warning" %}
Please ensure the policy version you select is compatible with your version of APIM.
{% endhint %}

To do so, follow these steps:

1. Download the plugin archive (a `.zip` file) from [the plugins download page](https://download.gravitee.io/#graviteeio-apim/plugins/)
2. Add the file into the `plugins` folder for both the Gateway and management API

{% hint style="info" %}
**Location of `plugins` folder**

The location of the `plugins` folder varies depending on your installation. By default, it is in ${GRAVITEE\_HOME/plugins}. This can be modified in [the `gravitee.yaml` file.](../../getting-started/configuration/the-gravitee-api-gateway/environment-variables-system-properties-and-the-gravitee.yaml-file.md#configure-the-plugins-repository)

Most installations will contain the `plugins` folder in`/gravitee/apim-gateway/plugins` for the Gateway and `/gravitee/apim-management-api/plugins` for the management API.
{% endhint %}

3. Remove any existing plugins of the same name.
4. Restart your APIM nodes

## Errors

<table data-full-width="true"><thead><tr><th width="243">Phase</th><th width="178">HTTP status code</th><th width="184">Error template key</th><th>Description</th></tr></thead><tbody><tr><td>onRequest</td><td><code>400</code></td><td>HTTP_SIGNATURE_IMPOSSIBLE_GENERATION</td><td><p>In case of:</p><ul><li>Request does not contain every header in the configuration headers list.</li><li>Request does not contain <code>Date</code> header and the configuration headers list is empty. Policy needs at least <code>Date</code> header to create a signature.</li><li>Unable to sign because of bad configuration.</li></ul></td></tr></tbody></table>

## Changelog

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-generate-http-signature/blob/master/CHANGELOG.md" %}
