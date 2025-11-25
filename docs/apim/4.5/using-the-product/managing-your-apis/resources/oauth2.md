---
description: Configuration and usage guide for oauth2.
---

# OAuth2

{% tabs %}
{% tab title="Generic Authorization Server" %}
<figure><img src="../../../.gitbook/assets/resource_oauth2 generic (1).png" alt=""><figcaption><p>Create an OAuth2 Generic Authorization Server resource</p></figcaption></figure>

<table><thead><tr><th width="190">Config param</th><th width="245">Description</th><th>Default</th></tr></thead><tbody><tr><td>Resource name</td><td>Name of the resource</td><td>-</td></tr><tr><td>Authorization server URL</td><td>URL of the authorization server</td><td>https://authorization_server</td></tr><tr><td>Token introspect endpoint</td><td>URL the resource uses to introspect an incoming access token</td><td>/oauth/check_token</td></tr><tr><td>System proxy</td><td>Toggle to use system proxy</td><td>false</td></tr><tr><td>Token introspect method</td><td>HTTP method to introspect the access token</td><td>GET</td></tr><tr><td>Client ID</td><td>Client identifier</td><td>-</td></tr><tr><td>Client secret</td><td>Client secret</td><td>-</td></tr><tr><td>Use HTTP header for client authorization</td><td>To prevent token scanning attacks, the endpoint MUST require access authorization. Gravitee uses an HTTP header for client authentication.</td><td>true</td></tr><tr><td>Authorization header</td><td>Authorization header</td><td>Authorization</td></tr><tr><td>Authorization scheme</td><td>Authorization scheme</td><td>Basic</td></tr><tr><td>Use a query parameter to supply access token</td><td>Access token is passed to the introspection endpoint using a query parameter</td><td>true</td></tr><tr><td>Token query param name</td><td>Query parameter that supplies access token</td><td>token</td></tr><tr><td>Use an HTTP header to supply access token</td><td>Access token is passed to the introspection endpoint using an HTTP header</td><td>false</td></tr><tr><td>HTTP header name</td><td>HTTP header used to supply access token</td><td>-</td></tr><tr><td>Use application/x-www-form-urlencoded form to send access token</td><td>Send access token in <strong>application/x-www-form-urlencoded</strong> form</td><td>false</td></tr><tr><td>Form param name</td><td>Form parameter name</td><td>token</td></tr><tr><td>User claim</td><td>User claim field to store end user in log analytics</td><td>sub</td></tr></tbody></table>
{% endtab %}

{% tab title="Gravitee AM Authorization Server" %}
<figure><img src="../../../.gitbook/assets/resource_oauth2 am (1).png" alt=""><figcaption><p>Create an OAuth2 Gravitee AM Authorization Server resource</p></figcaption></figure>

<table><thead><tr><th width="177">Config param</th><th width="414">Description</th><th>Default</th></tr></thead><tbody><tr><td>Resource name</td><td>Name of the resource</td><td>-</td></tr><tr><td>Server URL</td><td>URL of the Gravitee Access Management server</td><td>-</td></tr><tr><td>System proxy</td><td>Toggle to use system proxy</td><td>false</td></tr><tr><td>Version</td><td>Version of the Access Management server</td><td>V3_X</td></tr><tr><td>Security domain</td><td>Security domain (realm) from which the token has been generated and must be introspected</td><td>-</td></tr><tr><td>Client ID</td><td>Client identifier</td><td>-</td></tr><tr><td>Client secret</td><td>Client secret</td><td>-</td></tr><tr><td>User claim</td><td>User claim field to store end user in log analytics</td><td>sub</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

## Examples

{% tabs %}
{% tab title="OAuth2 - Gravitee AM" %}
```json
{
    "configuration": {
        "clientId": "my-client",
        "clientSecret": "f2ddb55e-30b5-4a45-9db5-5e30b52a4574",
        "securityDomain": "my-security",
        "serverURL": "https://graviteeio_access_management",
        "userClaim": "sub"
    }
}
```
{% endtab %}

{% tab title="OAuth2 - Generic Auth Server" %}
```json
{
    "configuration": {
        "introspectionEndpoint": "https://my_authorization_server/oauth/check_token",
        "introspectionEndpointMethod": "POST",
        "clientAuthorizationHeaderName": "Authorization",
        "clientAuthorizationHeaderScheme": "Basic",
        "clientId": "my-client",
        "clientSecret": "f2ddb55e-30b5-4a45-9db5-5e30b52a4574",
        "tokenIsSuppliedByHttpHeader": false,
        "tokenIsSuppliedByQueryParam": true,
        "tokenQueryParamName": "token",
        "useClientAuthorizationHeader": true
    }
}
```
{% endtab %}
{% endtabs %}
