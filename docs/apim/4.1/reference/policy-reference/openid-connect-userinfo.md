---
description: This page provides the technical details of the OpenID Connect UserInfo policy
---

# OpenID Connect UserInfo

## Overview

Use the `openid-userinfo` policy to get the OpenId Connect user info from an OAuth2 resource through its UserInfo endpoint.

{% hint style="info" %}
The request will fail with a 401 status if the policy’s Oauth2 resource is misconfigured or not defined at all. To troubleshoot this, check the `WWW_Authenticate` header for more information.
{% endhint %}

Functional and implementation information for the `openid-userinfo` policy is organized into the following sections:

* [Examples](openid-connect-userinfo.md#examples)
* [Configuration](openid-connect-userinfo.md#configuration)
* [Changelogs](openid-connect-userinfo.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 proxy APIs. It cannot be applied to v4 message APIs.
{% endhint %}

{% tabs %}
{% tab title="Proxy API example" %}
Sample policy configuration:

```json
{
  "id": "my-api",
  "name": "my-api",
  "gravitee": "2.0.0",
  "proxy": {
    "context_path": "/test",
    "endpoints": [
      {
        "name": "default",
        "target": "http://localhost:8080/endpoint",
        "http": {
          "connectTimeout": 3000,
          "readTimeout": 60000
        }
      }
    ]
  },
  "flows": [
    {
      "name": "No payload extraction flow",
      "methods": [
        "GET"
      ],
      "enabled": true,
      "path-operator": {
        "path": "/no-payload-extraction",
        "operator": "STARTS_WITH"
      },
      "pre": [
        {
          "name": "OpenId Connect - UserInfo",
          "description": "",
          "enabled": true,
          "policy": "policy-openid-userinfo",
          "configuration": {
            "oauthResource": "dummy-oauth-resource",
            "extractPayload": false
          }
        }
      ],
      "post": []
    },
    {
      "name": "Payload extraction flow",
      "methods": [
        "GET"
      ],
      "enabled": true,
      "path-operator": {
        "path": "/payload-extraction",
        "operator": "STARTS_WITH"
      },
      "pre": [
        {
          "name": "OpenId Connect - UserInfo",
          "description": "",
          "enabled": true,
          "policy": "policy-openid-userinfo",
          "configuration": {
            "oauthResource": "dummy-oauth-resource",
            "extractPayload": true
          }
        }
      ],
      "post": []
    },
    {
      "name": "Attribute copy to response payload",
      "methods": [
        "GET"
      ],
      "enabled": true,
      "path-operator": {
        "path": "/",
        "operator": "STARTS_WITH"
      },
      "post": [{
        "name": "Copy attribute from UserInfoPolicy to payload",
        "description": "",
        "enabled": true,
        "policy": "copy-attribute-to-response",
        "configuration": {
        }
      }]
    }
  ],
  "resources": [
    {
      "name": "dummy-oauth-resource",
      "enabled": true,
      "type": "dummy-oauth",
      "configuration": {
      }
    }
  ]
}
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `openid-userinfo` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="137" data-type="checkbox">Compatible?</th><th width="200.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `openid-userinfo` policy can be configured with the following options:

<table><thead><tr><th width="176">Property</th><th width="100" data-type="checkbox">Required</th><th width="246">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>oauthResource</td><td>true</td><td>The OAuth2 resource used to get UserInfo</td><td>string</td><td></td></tr><tr><td>extractPayload</td><td>false</td><td>When set to <code>true</code>, the payload of the response from the <code>UserInfo</code> endpoint is set in the <code>openid.userinfo.payload</code> gateway attribute</td><td>boolean</td><td></td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-OpenID-Connect-UserInfo/blob/master/CHANGELOG.md" %}
