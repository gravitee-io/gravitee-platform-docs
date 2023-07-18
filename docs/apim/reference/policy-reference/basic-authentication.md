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

# Basic Authentication

## Overview

Functional and implementation information for the Basic Authentication policy is organized into the following sections:

* [Examples](basic-authentication.md#examples)
* [Configuration](basic-authentication.md#configuration)
* [Compatibility Matrix](basic-authentication.md#compatibility-matrix)
* [Changelogs](basic-authentication.md#changelogs)

## Examples

You can use the `basic-authentication` policy to manage basic authentication headers sent in API calls. The policy compares the user and password sent in the basic authentication header to an APIM user to determine if the user credentials are valid.

To use the policy in an API, you need to:

* configure an LDAP, inline or http resource for your API plan, which specifies where the APIM users are stored
* configure a basic authentication policy for the API flows

{% hint style="info" %}
LDAP, inline and http resources are not part of the default APIM configuration, so you must configure an LDAP, inline or http resource for APIM first.
{% endhint %}

{% tabs %}
{% tab title="Proxy APIs" %}
{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

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

To authenticate, pass the `Authorization: Basic yourCredentials` header with your request
{% endtab %}
{% endtabs %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

### Reference

<table data-full-width="false"><thead><tr><th width="231">Property</th><th width="107" data-type="checkbox">Required</th><th>Description</th><th width="152">Type</th></tr></thead><tbody><tr><td>authenticationProviders</td><td>true</td><td>A list of authentication providers</td><td>List of strings</td></tr><tr><td>realm</td><td>false</td><td>Name showed to the client in case of error</td><td>string</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the Basic Authentication policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Connected user

After successful authentication, connected username is stored in context attributes, accessible with `context.attributes['user']` expression language.

In order to display the connected username in API logging, you can enable the environment setting `Gateway > API logging > Display end user on API Logging`.

This adds a `user` column in the logs table.

## Compatibility matrix

In the [changelog for each version of APIM](../../releases-and-changelog/changelog/), we provide a list of policies included in the default distribution. The chart below summarizes this information in relation to the `basic-authentication` policy.

<table data-full-width="false"><thead><tr><th width="164.33333333333331">Plugin Version</th><th width="239">Supported APIM versions</th><th data-type="checkbox">Included in APIM default distribution</th></tr></thead><tbody><tr><td>>=1.4</td><td>>=3.15</td><td>true</td></tr><tr><td>&#x3C;=1.x</td><td>&#x3C;3.15</td><td>true</td></tr></tbody></table>

## Changelog

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-basic-authentication/blob/master/CHANGELOG.md" %}
