---
description: This page provides the technical details of the Basic Authentication policy
hidden: true
---

# Basic Authentication

## Overview

You can use the `basic-authentication` policy to manage basic authentication headers sent in API calls. The policy compares the user and password sent in the basic authentication header to an APIM user to determine if the user credentials are valid.

To use the policy in an API, you need to:

* Configure an LDAP, inline, or HTTP resource for your API plan to specify where the APIM users are stored
* Configure a basic authentication policy for the API flows

{% hint style="info" %}
LDAP, inline, and HTTP resources are not part of the default APIM configuration. You must first configure an LDAP, inline, or HTTP resource for APIM.
{% endhint %}

Functional and implementation information for the `basic-authentication` policy is organized into the following sections:

* [Examples](basic-authentication.md#examples)
* [Configuration](basic-authentication.md#configuration)
* [Compatibility Matrix](basic-authentication.md#compatibility-matrix)
* [Changelogs](basic-authentication.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
If an API is configured with the `basic-authentication` policy, a request with invalid credentials will result in the following response:

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
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `basic-authentication` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="196.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

You can configure the `basic-authentication` policy with the following options:

<table data-full-width="false"><thead><tr><th width="231">Property</th><th width="109" data-type="checkbox">Required</th><th width="176">Description</th><th width="152">Type</th></tr></thead><tbody><tr><td>authenticationProviders</td><td>true</td><td>A list of authentication providers</td><td>List of strings</td></tr><tr><td>realm</td><td>false</td><td>Name showed to the client in case of error</td><td>string</td></tr></tbody></table>

### Connected user

After successful authentication, connected username is stored in context attributes, accessible with `context.attributes['user']` expression language.

In order to display the connected username in API logging, you can enable the environment setting `Gateway > API logging > Display end user on API Logging`. This adds a `user` column in the logs table.

## Compatibility matrix

The following is the compatibility matrix for APIM and the `basic-authentication` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>Up to 1.x</td><td>Up to 3.14.x</td></tr><tr><td>1.4.x+</td><td>3.15.x+</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-basic-authentication/blob/master/CHANGELOG.md" %}
