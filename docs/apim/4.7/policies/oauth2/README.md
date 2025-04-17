---
hidden: true
---

# OAuth2

## Overview

You can use the `oauth2` policy to check access token validity during request processing using token introspection.

If the access token is valid, the request is allowed to proceed. If not, the process stops and rejects the request.

The access token must be supplied in the `Authorization` HTTP request header:

```sh
$ curl -H "Authorization: Bearer |accessToken|" \
           http://gateway/api/resource
```

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Given the following introspection response payload:

```json
{
    "active": true,
    "client_id": "VDE",
    "exp": 1497536237,
    "jti": "5e075c1c-f4eb-42a5-8b56-fd367133b242",
    "scope": "read write delete",
    "token_type": "bearer",
    "username": "flx"
}
```

You can extract the `username` from the payload using the following JsonPath:

```json
{#jsonPath(#context.attributes['oauth.payload'], '$.username')}
```
{% endtab %}
{% endtabs %}

## Configuration

The `oauth2` policy requires a resource to access an OAuth2 Authorization Server for token introspection. APIM supports two types of authorization server:

* [Generic OAuth2 Authorization Server](generic-oauth2-authorization-server.md): A resource which can be configured to cover any authorization server.
* [Gravitee.io AM Authorization Server](gravitee.io-am-authorization-server.md): A resource which can be easily plugged into APIM using Gravitee.io Access Management with security domain support.

{% code title="Sample Configuration" %}
```json
{
  "oauth2": {
    "oauthResource": "oauth2-resource-name",
    "oauthCacheResource": "cache-resource-name",
    "extractPayload": true,
    "checkRequiredScopes": true,
    "requiredScopes": ["openid", "resource:read", "resource:write"]
  }
}
```
{% endcode %}

### Phases

The phases checked below are supported by the `oauth2` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `oauth2` policy can be configured with the following options:

<table><thead><tr><th width="223">Property</th><th data-type="checkbox">Required</th><th width="243">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>oauthResource</td><td>true</td><td>The OAuth2 resource used to validate <code>access_token</code>. This must reference a valid Gravitee.io OAuth2 resource.</td><td>string</td><td></td></tr><tr><td>oauthCacheResource</td><td>false</td><td>The Cache resource used to store the <code>access_token</code>. This must reference a valid Gravitee.io Cache resource.</td><td>string</td><td></td></tr><tr><td>extractPayload</td><td>false</td><td>When the access token is validated, the token endpoint payload is saved in the <code>oauth.payload</code> context attribute</td><td>boolean</td><td>false</td></tr><tr><td>checkRequiredScopes</td><td>false</td><td>Whether the policy needs to check <code>required</code> scopes to access the underlying resource</td><td>boolean</td><td>false</td></tr><tr><td>requiredScopes</td><td>false</td><td>List of scopes to check to access the resource</td><td>boolean</td><td>array of string</td></tr></tbody></table>

### Attributes

The `oauth2` policy can be configured with the following attributes:

<table><thead><tr><th width="201.5">Name</th><th>Description</th></tr></thead><tbody><tr><td>oauth.access_token</td><td>Access token extracted from <code>Authorization</code> HTTP header.</td></tr><tr><td>oauth.payload</td><td>Payload from token endpoint / authorization server, useful when you want to parse and extract data from it. Only if <code>extractPayload</code> is enabled in policy configuration.</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `oauth2` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.x</td><td>Up to 3.19.x</td></tr><tr><td>2.0.x</td><td>3.20.x</td></tr><tr><td>3.x</td><td>4.x+</td></tr></tbody></table>

## Errors

<table><thead><tr><th width="195.5">HTTP Status Code</th><th>Message</th></tr></thead><tbody><tr><td><code>401</code></td><td><p>* No OAuth Authorization Server resource has been configured</p><p>* No OAuth authorization header was supplied</p><p>* No OAuth access token was supplied</p><p>* Access token can not be validated by authorization server</p></td></tr><tr><td><code>403</code></td><td><p>* Access token can not be validated because of a technical error with authorization server</p><p>* One of the required scopes was missing while introspecting access token</p></td></tr></tbody></table>

You can use the response template feature to override the default response provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

The error keys sent by this policy are as follows:

<table><thead><tr><th width="416.5">Key</th><th>Parameters</th></tr></thead><tbody><tr><td>OAUTH2_MISSING_SERVER</td><td>-</td></tr><tr><td>OAUTH2_MISSING_HEADER</td><td>-</td></tr><tr><td>OAUTH2_MISSING_ACCESS_TOKEN</td><td>-</td></tr><tr><td>OAUTH2_INVALID_ACCESS_TOKEN</td><td>-</td></tr><tr><td>OAUTH2_INVALID_SERVER_RESPONSE</td><td>-</td></tr><tr><td>OAUTH2_INSUFFICIENT_SCOPE</td><td>-</td></tr><tr><td>OAUTH2_SERVER_UNAVAILABLE</td><td>-</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-OAuth2/blob/master/CHANGELOG.md" %}
