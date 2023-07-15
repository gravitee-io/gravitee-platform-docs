---
description: Sample structure for policy documentation
---

# Basic Authentication

## Overview

You can use the Basic-authentication policy to manage basic authentication headers sent in API calls. The policy compares the user and password sent in the basic authentication header to a Gravitee API Management (APIM) user to determine if the user credentials are valid.

To use the policy in an API, you need to:

* configure an LDAP, inline, or HTTP resource for your API plan, which specifies where the APIM users are stored
* configure a basic authentication policy for the API flows

{% hint style="warning" %}
LDAP, inline, and HTTP resources are not part of the default APIM configuration, so you must [configure an LDAP, inline, or HTTP resource for APIM first](../../guides/api-configuration/resources.md).
{% endhint %}

### Example

{% hint style="warning" %}
This example will work for [v2 APIs, v4 proxy APIs, and for the initial connection request of v4 message APIs](../../overview/gravitee-api-definitions-and-execution-engines.md).

Currently, this policy can **not** be applied at the message level.
{% endhint %}

If an API is configured with the Basic-authentication policy, a request with invalid credentials will result in the following response:

{% code title="Default response" %}
```json
{
    "http_status_code": 401,
    "message": "Unauthorized"
}
```
{% endcode %}

The response headers will also contain a `WWW-Authenticate` header containing the `realm` value the API publisher configured.

To authenticate, pass the `Authorization: Basic yourCredentials` header with your request.

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
  "description": "Adds basic auth to your gateway API",
  "policy": "basic-authentication",
  "configuration": {
          "authenticationProviders": [ "Name of your resource" ],
          "realm": "Sample realm"
        }
}
```
{% endcode %}
{% endtab %}
{% endtabs %}

### Reference

<table data-full-width="false"><thead><tr><th width="156">Property</th><th data-type="checkbox">Required</th><th>Description</th><th data-type="select">Type</th><th>Options</th><th>Default</th></tr></thead><tbody><tr><td>authenticationProviders</td><td>true</td><td>A list of authentication providers</td><td></td><td>N/a</td><td>N/a</td></tr><tr><td>realm</td><td>false</td><td>Name showed to the client in case of error</td><td></td><td>N/a</td><td>N/a</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a gateway API transaction. Depending on the [version of the gateway API](../../overview/gravitee-api-definitions-and-execution-engines.md#policy-execution-phases-and-execution-order), the request and response are broken up into what are known as _phases_. Each policy has different compatibility with the available phases:

{% tabs %}
{% tab title="v4 API definition" %}
v4 APIs have the following phases:

* `onRequest`: This phase is executed before invoking the backend services for both proxy and message APIs. Policies can act on the headers and the content for proxy APIs.
* `onMessageRequest`: This phase occurs after the `onRequest` phase and allows policies to act on each incoming message before being sent to the backend service. This only applies to message APIs.
* `onResponse`: This phase is executed after invoking the backend services for both proxy and message APIs. Policies can act on the headers and the content for proxy APIs.
* `onMessageResponse`: This phase after the `onResponse` phase and allows policies to act on each outgoing message before being sent to the client application. This only applies to message APIs.

This policy is compatible with the following v4 API phases:

<table data-full-width="false"><thead><tr><th width="138" data-type="checkbox">onRequest</th><th width="142" data-type="checkbox">onResponse</th><th data-type="checkbox">onMessageRequest</th><th data-type="checkbox">onMessageResponse</th></tr></thead><tbody><tr><td>true</td><td>false</td><td>false</td><td>false</td></tr></tbody></table>
{% endtab %}

{% tab title="v2 API definition" %}
v2 APIs have the following phases:

* `onRequest`: This phase only allows policies to work on request headers. It never accesses the request body.
* `onRequestContent`: This phase always occurs after the `onRequest` phase. It allows policies to work at the content level and access the request body.
* `onResponse`: This phase only allows policies to work on response headers. It never accesses the response body.
* `onResponseContent`: This phase always occurs after the `onResponse` phase. It allows policies to work at the content level and access the response body.

This policy supports the following phases:

<table><thead><tr><th width="172" data-type="checkbox">onRequest</th><th width="138" data-type="checkbox">onResponse</th><th width="182" data-type="checkbox">onRequestContent</th><th data-type="checkbox">onResponseContent</th></tr></thead><tbody><tr><td>true</td><td>false</td><td>false</td><td>false</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

## Compatibility matrix

In the [changelog for each version of APIM](../../releases-and-changelog/changelog/), we provide a list of policies included in the default distribution. The chart below summarizes this information in relation to the `json-xml` policy.

<table data-full-width="false"><thead><tr><th width="164.33333333333331">Plugin Version</th><th width="239">Supported APIM versions</th><th>Included in APIM default distribution</th></tr></thead><tbody><tr><td>>=1.4</td><td>>=3.15</td><td>>=3.15</td></tr><tr><td>&#x3C;1.4</td><td>&#x3C;3.15</td><td>&#x3C;3.15</td></tr></tbody></table>

## Installation and deployment

Each version of APIM includes a number of policies by default. If the policy is not included in the default distribution or you would like to use a different version of the policy, you can modify the plugin.

{% hint style="warning" %}
Please ensure the policy version you select is compatible with your version of APIM.
{% endhint %}

To do so, follow these steps:

1. Download the plugin archive (a `.zip` file) from [the plugins download page](https://download.gravitee.io/#graviteeio-apim/plugins/)
2. Add the file into the `plugins` folder for both the gateway and management API

{% hint style="info" %}
**Location of `plugins` folder**

The location of the `plugins` folder varies depending on your installation. By default, it is in ${GRAVITEE\_HOME/plugins}. This can be modified in [the `gravitee.yaml` file.](../../getting-started/configuration/the-gravitee-api-gateway/environment-variables-system-properties-and-the-gravitee.yaml-file.md#configure-the-plugins-repository)

Most installations will contain the `plugins` folder in`/gravitee/apim-gateway/plugins` for the gateway and `/gravitee/apim-management-api/plugins` for the management API.
{% endhint %}

3. Remove any existing plugins of the same name.
4. Restart your APIM nodes

## Errors

<table data-full-width="false"><thead><tr><th width="243">Phase</th><th>HTTP status code</th><th>Error template key</th><th>Description</th></tr></thead><tbody><tr><td>onRequest</td><td><code>401</code></td><td>N/a</td><td>Unauthorized</td></tr></tbody></table>

## Changelog

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-basic-authentication/blob/master/CHANGELOG.md" %}
