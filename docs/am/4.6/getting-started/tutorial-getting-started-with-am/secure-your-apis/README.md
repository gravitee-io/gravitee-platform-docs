# Secure Your APIs

## Overview

In this section, we will demonstrate how to use [Gravitee API Management](https://www.gravitee.io/products/api-management) to secure your APIs.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-quickstart-secure-apis-overview.png" alt=""><figcaption><p>Gravitee platform</p></figcaption></figure>

### Before you begin

We assume that you have installed Gravitee API Management and have a fully operational environment which can interact with your published APIs.

Ensure you have set up a new AM application and have your Client ID, Client Secret and Security Domain information at hand.

## Protect your API with OAuth 2

Securing an API with OAuth2 is a multi-stage process. The following sections provide step-by-step instructions for configuration and verification:

1. [Configure an authorization server resource](./#configure-an-authorization-server-resource)
2. [Configure the OAuth2 policy](./#configure-the-oauth2-policy)
3. [Verify OAuth2 security](./#verify-oauth2-security)

### Configure an authorization server resource

The OAuth2 policy requires a resource to access an OAuth2 Authorization Server for token introspection, which must be configured prior to adding it to the OAuth2 policy. APIM supports [Generic OAuth2 Authorization Server](https://documentation.gravitee.io/apim/reference/policy-reference/oauth2/generic-oauth2-authorization-server) and [Gravitee.io AM Authorization Server](https://documentation.gravitee.io/apim/reference/policy-reference/oauth2/gravitee.io-am-authorization-server) resources. Refer to the following pages for the configuration details of each APIM resource type:

* [Generic OAuth2 Authorization Server](configure-generic-oauth2-authorization-server.md)
* [Gravitee.io AM Authorization Server](configure-gravitee.io-access-management.md)

### Configure the OAuth2 policy

The OAuth2 policy can be configured in the Gravitee API Management Console:

1. Log in to APIM Management Console.
2. Click **APIs** in the left sidebar.
3. Select the API you want to secure.
4. Click **Policy Studio** in the inner left sidebar.
5. Select the flow you want to secure.
6.  Under the Initial connection tab, click the `+` icon of the **Request phase**. The OAuth2 policy can be applied to v2 APIs and v4 proxy APIs. It cannot be applied at the message level.&#x20;

    <figure><img src="../../../.gitbook/assets/oauth2 add to flow.png" alt=""><figcaption><p>Add a policy to Request phase flow</p></figcaption></figure>
7.  In the resulting dialog box, **Select** the OAuth2 tile:

    <figure><img src="../../../.gitbook/assets/oauth2 policy.png" alt=""><figcaption><p>Add the OAuth2 policy to the flow</p></figcaption></figure>
8.  Configure the OAuth2 policy per the [documentation](https://documentation.gravitee.io/apim/reference/policy-reference/oauth2):

    <figure><img src="../../../.gitbook/assets/oauth2 policy details.png" alt=""><figcaption><p>Configure the OAuth2 policy</p></figcaption></figure>
9. Click **Add policy**.
10. **Save** and deploy/redeploy your API.
11. [Verify that your API is OAuth2 secured.](./#verify-oauth2-security)

### Verify OAuth2 security

You can confirm that your API is OAuth2 secured by calling it through APIM Gateway:

```sh
curl -X GET http://GRAVITEEIO-APIM-GATEWAY-HOST/echo
```

If OAuth2 security is correctly configured, you will receive the following response:

{% code overflow="wrap" %}
```sh
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm=gravitee.io - No OAuth authorization header was supplied
{
    "message": "No OAuth authorization header was supplied",
    "http_status_code": 401
}
```
{% endcode %}

## Request an access token for your application

To access your protected API, you must acquire an access token from AM by using OAuth2.

1.  Get your **Client ID**, **Client Secret,** and **Security Domain** values and request an access token.

    Request a token

```sh
curl -X POST \
  'http://GRAVITEEIO-AM-GATEWAY-HOST/:domainPath/oauth/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Authorization: Basic Base64.encode64(:clientId + ':' + :clientSecret)' \
  -d 'grant_type=client_credentials'
```

| Parameter      | Description                                          |
| -------------- | ---------------------------------------------------- |
| grant\_type    | **REQUIRED.** Set the value to `client_credentials`. |
| client\_id     | **REQUIRED.** Client’s ID.                           |
| client\_secret | **REQUIRED.** Client’s secret.                       |
| scope          | **OPTIONAL.** The scopes of the access token.        |

{% hint style="info" %}
In this example we are using server-to-server interactions with the Client Credentials grant type that does not involve user registration.
{% endhint %}

If it is working correctly, you will receive the following response:

{% code overflow="wrap" %}
```sh
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
{
    "access_token" : "eyJraWQiOiJkZWZhdWx0LWdyYXZpdGVlLUFNLWtleSIsImFsZyI6IkhTMjU2In0.eyJzdWIiOiI0NTM...QW5rN0h2SEdUOFNMYyJ9.w8A9yKJcuFbE_SYmRRAdGBEz-6nnXg7rdv1S4JD9xGI",
    "token_type": "bearer",
    "expires_in": 7199
}
```
{% endcode %}

## Use the access token

You can use the access token obtained in the previous section to make API calls.

1. In APIM Portal, go to your API page and choose the operation you want to call.
2. Provide your access token and get your secured API data.

{% code overflow="wrap" %}
```
curl -X GET http://GRAVITEEIO-APIM-GATEWAY-HOST/echo -H 'Authorization: Bearer :access_token'
```
{% endcode %}

{% hint style="info" %}
See the APIM OAuth2 Policy for more information about how to supply the access token while making the API call.
{% endhint %}

If it is working correctly, you will see the data from the selected API operation:

{% code overflow="wrap" %}
```sh
{
    "headers": {
        "Host": "api.gravitee.io",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4",
        "Authorization": "Bearer b7d0afc4-c96d-40d4-90af-c4c96d20d4c7",
        "Cache-Control": "no-cache",
        "Postman-Token": "14a75ef7-6df4-9290-e2b0-467a4be1eb6b",
        "X-Forwarded-For": "90.110.233.212",
        "X-Forwarded-Host": "api.gravitee.io",
        "X-Forwarded-Proto": "https",
        "X-Forwarded-Server": "734bb5636800",
        "X-Gravitee-Transaction-Id": "16b4c23c-c992-46c6-b4c2-3cc992a6c6db",
        "X-Traefik-Reqid": "2855484"
    }
}
```
{% endcode %}
