---
description: An overview about ---.
hidden: true
---

# SSL Enforcement

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../overview/enterprise-edition.md)**.**
{% endhint %}

## Overview

You can use the `ssl-enforcement` policy to filter incoming SSL requests. It allows you to restrict or allow access only to requests with client certificate authentication or only to a subset of valid clients.

This policy is mainly used in plan configuration to allow access to consumers for a given set of certificates. The client is able to pass a valid certificate in one of two ways:

* In session: This is the default behavior. The client certificate is accessible through the TLS session, which must remain active during the certificate request. If the session is terminated, the certificate will not be visible.
* In header: A reverse proxy (e.g., NGINX, Apache) passes the client certificate using a specified header. This option requires the user to specify which header contains the certificate, which is base64-encoded.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 TCP proxy APIs or v4 message APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Sample policy configuration:

```json
"ssl-enforcement" : {
    "requiresSsl": true,
    "requiresClientAuthentication": true,
    "whitelistClientCertificates": [
        "CN=localhost,O=GraviteeSource,C=FR"
    ]
}
```
{% endtab %}
{% endtabs %}

## Configuration

The implementation of the `ssl-enforcement` policy supports Ant-style path patterns, where URL mapping matches URLs using the following rules:

* `?` matches one character
* `*` matches zero or more characters
* `**` matches zero or more directories in a path

### Phases

The phases checked below are supported by the `ssl-enforcement` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="204.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `ssl-enforcement` policy can be configured with the following options:

<table><thead><tr><th width="266">Property</th><th data-type="checkbox">Required</th><th width="222">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>requiresSsl</td><td>false</td><td>Is SSL requires to access this resource?</td><td>boolean</td><td>true</td></tr><tr><td>requiresClientAuthentication</td><td>false</td><td>Is client authentication required to access this resource?</td><td>boolean</td><td>false</td></tr><tr><td>whitelistClientCertificates</td><td>false</td><td>List of allowed X.500 names (from client certificate)</td><td>array of strings</td><td>-</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `ssl-enforcement` policy:

| Plugin version | Supported APIM versions |
| -------------- | ----------------------- |
| 1.x            | All                     |

## Errors

<table><thead><tr><th width="209.5">HTTP status code</th><th>Message</th></tr></thead><tbody><tr><td><code>401</code></td><td>Access to the resource is unauthorized according to policy rules</td></tr><tr><td><code>403</code></td><td>Access to the resource is forbidden according to policy rules</td></tr></tbody></table>

You can use the response template feature to override the default responses provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

The error keys sent by this policy are as follows:

<table><thead><tr><th width="442.5">Key</th><th>Parameters</th></tr></thead><tbody><tr><td>SSL_ENFORCEMENT_SSL_REQUIRED</td><td>-</td></tr><tr><td>SSL_ENFORCEMENT_AUTHENTICATION_REQUIRED</td><td>-</td></tr><tr><td>SSL_ENFORCEMENT_CLIENT_FORBIDDEN</td><td>name (X.500 name from client certificate)</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-ssl-enforcement/blob/master/CHANGELOG.md" %}
