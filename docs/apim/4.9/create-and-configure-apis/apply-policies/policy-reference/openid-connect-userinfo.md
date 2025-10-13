# OpenID Connect UserInfo

## Overview

Use the `openid-userinfo` policy to get the OpenId Connect user info from an OAuth2 resource through its UserInfo endpoint.

{% hint style="info" %}
The request will fail with a 401 status if the policy’s Oauth2 resource is misconfigured or not defined at all. To troubleshoot this, check the `WWW_Authenticate` header for more information.
{% endhint %}

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Sample policy configuration for a payload extraction flow:

```json
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
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `openid-userinfo` policy:

<table data-full-width="false"><thead><tr><th width="206">v2 Phases</th><th width="137" data-type="checkbox">Compatible?</th><th width="200.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `openid-userinfo` policy can be configured with the following options:

<table><thead><tr><th width="176">Property</th><th width="100" data-type="checkbox">Required</th><th width="246">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>oauthResource</td><td>true</td><td>The OAuth2 resource used to get UserInfo</td><td>string</td><td></td></tr><tr><td>extractPayload</td><td>false</td><td>When set to <code>true</code>, the payload of the response from the <code>UserInfo</code> endpoint is set in the <code>openid.userinfo.payload</code> gateway attribute</td><td>boolean</td><td></td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-OpenID-Connect-UserInfo/blob/master/CHANGELOG.md" %}
