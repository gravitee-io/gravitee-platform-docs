---
description: This page describes how to create and configure the default APIM resources
---

# Resources

## Examples

Below are example JSON configuration files for several of the default resources.

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
