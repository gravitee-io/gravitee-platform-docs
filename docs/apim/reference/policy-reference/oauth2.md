---
description: This page provides the technical details of the OAuth2 policy
---

# OAuth2

## Overview

Functional and implementation information for the OAuth2 policy is organized into the following sections:

* [Examples](oauth2.md#examples)
* [Configuration](oauth2.md#configuration)
* [Errors](oauth2.md#errors)
* [Changelogs](oauth2.md#changelogs)

## Examples

You can use the `oauth2` policy to check access token validity during request processing using token introspection.

If the access token is valid, the request is allowed to proceed. If not, the process stops and rejects the request.

The access token must be supplied in the `Authorization` HTTP request header:

```
$ curl -H "Authorization: Bearer |accessToken|" \
           http://gateway/api/resource
```

{% tabs %}
{% tab title="Proxy API example" %}
{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

Given the following introspection response payload:

```
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

```
{#jsonPath(#context.attributes['oauth.payload'], '$.username')}

```
{% endtab %}
{% endtabs %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

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

### Reference

The OAuth2 policy requires a resource to access an OAuth2 Authorization Server for token introspection. APIM supports two types of authorization server:

* [Generic OAuth2 Authorization Server](https://docs.gravitee.io/apim/3.x/apim\_resources\_oauth2\_generic.html) — a resource which can be configured to cover any authorization server.
* [Gravitee.io Access Management](https://docs.gravitee.io/apim/3.x/apim\_resources\_oauth2\_am.html) — a resource which can be easily plugged into APIM using Gravitee.io Access Management with security domain support.

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>oauthResource</td><td>true</td><td>The OAuth2 resource used to validate <code>access_token</code>. This must reference a valid Gravitee.io OAuth2 resource.</td><td>string</td><td></td></tr><tr><td>oauthCacheResource</td><td>false</td><td>The Cache resource used to store the <code>access_token</code>. This must reference a valid Gravitee.io Cache resource.</td><td>string</td><td></td></tr><tr><td>extractPayload</td><td>false</td><td>When the access token is validated, the token endpoint payload is saved in the <code>oauth.payload</code> context attribute</td><td>boolean</td><td>false</td></tr><tr><td>checkRequiredScopes</td><td>false</td><td>Whether the policy needs to check <code>required</code> scopes to access the underlying resource</td><td>boolean</td><td>false</td></tr><tr><td>requiredScopes</td><td>false</td><td>List of scopes to check to access the resource</td><td>boolean</td><td>array of string</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the OAuth2 policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility matrix

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution. The chart below summarizes this information in relation to the `json-xml` policy.

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>2.2</td><td>>=3.20</td></tr><tr><td>2.1</td><td>^3.0</td></tr><tr><td>2.0</td><td>^3.0</td></tr></tbody></table>

## Errors

#### HTTP status code

| Code  | Message                                                                                                                                                                                                                                                      |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `401` | <p>Issue encountered:</p><p>* No OAuth Authorization Server resource has been configured</p><p>* No OAuth authorization header was supplied</p><p>* No OAuth access token was supplied</p><p>* Access token can not be validated by authorization server</p> |
| `403` | <p>Issue encountered:</p><p>* Access token can not be validated because of a technical error with authorization server</p><p>* One of the required scopes was missing while introspecting access token</p>                                                   |

#### Default response override

You can use the response template feature to override the default response provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

#### Error keys

The error keys sent by this policy are as follows:

| Key                               | Parameters |
| --------------------------------- | ---------- |
| OAUTH2\_MISSING\_SERVER           | -          |
| OAUTH2\_MISSING\_HEADER           | -          |
| OAUTH2\_MISSING\_ACCESS\_TOKEN    | -          |
| OAUTH2\_INVALID\_ACCESS\_TOKEN    | -          |
| OAUTH2\_INVALID\_SERVER\_RESPONSE | -          |
| OAUTH2\_INSUFFICIENT\_SCOPE       | -          |
| OAUTH2\_SERVER\_UNAVAILABLE       | -          |

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-OAuth2/blob/master/CHANGELOG.md" %}
