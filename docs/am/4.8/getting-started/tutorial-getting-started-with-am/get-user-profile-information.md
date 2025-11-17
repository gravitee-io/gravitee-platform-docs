# Get User Profile Information

## Overview

After you have [set up your first application](set-up-your-first-application.md), you can retrieve user profile information with OpenID Connect.

{% hint style="info" %}
For more information on OpenID Connect and OAuth2, see [Authorization in AM.](../../README.md#authorization-in-am)
{% endhint %}

In this example, we will use the [Resource Owner Password Credentials flow](https://tools.ietf.org/html/rfc6749#section-1.3.3). You use it to obtain and verify user identities for your applications by issuing [ID Tokens](http://openid.net/specs/openid-connect-core-1_0.html#IDToken) or calling the [UserInfo Endpoint](http://openid.net/specs/openid-connect-core-1_0.html#UserInfo). The default flow is the [Authorization Code flow](https://tools.ietf.org/html/rfc6749#section-1.3.1) with a login page displayed to the end user.

## ID Token

### Get an ID Token with AM Console

An ID Token is a signed [JSON Web Token (JWT)](https://tools.ietf.org/html/draft-ietf-oauth-json-web-token-32) that contains user profile information, also known as a _claim_. Claims are statements about end-user authentication and can be trusted only if application consumers can verify the signature. ID tokens are self-contained and supply all the necessary information about the current user without making additional HTTP requests.

You can retrieve an ID Token by requesting an access token with a specific `openid` scope.

1. [Log in to AM Console](login-to-am-console.md).
2. Click **Applications**.
3. Click the application, then click the **Settings** tab.
4.  Click **OAuth 2.0 / OIDC**.

    <figure><img src="https://docs.gravitee.io/images/am/current/quickstart-applications-oauth2.png" alt=""><figcaption><p>Application grant flows</p></figcaption></figure>
5. In the **Scopes** section, select **openid** from the **Scope** drop-down menu and click **+ADD**.
6. Scroll to the bottom of the page and click **SAVE**.

### Get an ID Token with AM API

Request a token

{% code overflow="wrap" %}
```sh
curl -L -X POST 'http://GRAVITEEIO-AM-GATEWAY-HOST/:domainPath/oauth/token' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'Authorization: Basic Base64.encode(:clientId + ':' + :clientSecret)' \
-H 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=password' \
--data-urlencode 'username=:username' \
--data-urlencode 'password=:password' \
--data-urlencode 'scope=openid'
```
{% endcode %}

| Parameter      | Description                                 |
| -------------- | ------------------------------------------- |
| grant\_type    | **REQUIRED.** Set the value to `password`.  |
| client\_id     | **REQUIRED.** Client’s ID. (Basic Auth)     |
| client\_secret | **REQUIRED.** Client’s secret. (Basic Auth) |
| username       | **REQUIRED.** User’s name.                  |
| password       | **REQUIRED.** User’s password.              |
| scope          | **REQUIRED.** Set the value to `openid`.    |

If it works correctly, you will see the following response:

{% code overflow="wrap" %}
```sh
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
{
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsXQiOjE...WlseV9uYW1lIjoiYWRtaW4ifQ.P4nEWfdOCR6ViWWu_uh7bowLQfttkOjBmmkqDIY1nxRoxsSWJjJCXaDmwzvcnmk6PsfuW9ZOryJ9AyMMXjE_4cR70w4OESy01qnH-kKAE9jiLt8wj1mbObZEhFYAVcDHOZeKGBs5UweW-s-9eTjbnO7y7i6OYuugZJ3qdKIhzlp9qhzwL2cqRDDwgYFq4iVnv21L302JtO22Q7Up9PGCGc3vxmcRhyQYiKB3TFtxnxm8fPMFcuHLdMuwaYSRp3EesOBXa8UN_iIokCGyk0Cw_KPvpRq91GU8x6cMnVEFXnlYokEuP3aYWE4VYcQu0_cErr122vD6774HSnOVns_BLA",
    "token_type": "bearer",
    "expires_in": 7199,
    "scope": "openid",
    "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsXQiOjE...WlseV9uYW1lIjoiYWRtaW4ifQ.P4nEWfdOCR6ViWWu_uh7bowLQfttkOjBmmkqDIY1nxRoxsSWJjJCXaDmwzvcnmk6PsfuW9ZOryJ9AyMMXjE_4cR70w4OESy01qnH-kKAE9jiLt8wj1mbObZEhFYAVcDHOZeKGBs5UweW-s-9eTjbnO7y7i6OYuugZJ3qdKIhzlp9qhzwL2cqRDDwgYFq4iVnv21L302JtO22Q7Up9PGCGc3vxmcRhyQYiKB3TFtxnxm8fPMFcuHLdMuwaYSRp3EesOBXa8UN_iIokCGyk0Cw_KPvpRq91GU8x6cMnVEFXnlYokEuP3aYWE4VYcQu0_cErr122vD6774HSnOVns_BLA"
}
```
{% endcode %}

### Verify ID Token

An ID Token can be decoded and verified using a 3rd-party JWT library that you can find on the [JWT.IO website](https://jwt.io/).

ID Tokens must contain at least the following [required claims](http://openid.net/specs/openid-connect-core-1_0.html#IDToken):

| Claim |                                                                                               |
| ----- | --------------------------------------------------------------------------------------------- |
| iss   | Issuer Identifier, must be the `oidc.iss` configuration value (default `http://gravitee.am`). |
| sub   | Subject Identifier represented by the unique user’s `username`.                               |
| aud   | Audience(s) that this ID Token is intended for. It MUST contain your OAuth 2.0 `client_id`.   |
| exp   | Expiration time on or after which the ID Token MUST NOT be accepted for processing.           |
| iat   | Time at which the JWT was issued.                                                             |

Finally, you need to have the ID Token signed by AM.

1. In AM Console, click **Settings**.
2.  In the **Security** section, click **Certificates**.

    <figure><img src="https://docs.gravitee.io/images/am/current/quickstart-applications-certificates.png" alt=""><figcaption><p>AM Certificates</p></figcaption></figure>
3. Retrieve your public key by clicking the key icon.
4. Copy the signature and use a JWT library to verify it.

{% hint style="info" %}
You can also use Gravitee API Management with the JWT Policy to verify and retrieve user profile information.
{% endhint %}

## UserInfo Endpoint

In addition to the claims in the ID Token, OpenID Connect defines a standard protected endpoint, the [UserInfo Endpoint](http://openid.net/specs/openid-connect-core-1_0.html#UserInfo), that returns claims about the current user through the access token.

{% code title="Request a token" overflow="wrap" %}
```sh
curl -X GET http://GRAVITEEIO-AM-GATEWAY-HOST/:securityDomainPath/oidc/userinfo -H 'Authorization: Bearer :access_token'
```
{% endcode %}

If it works correctly, you will see the following response:

```sh
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
{
  "sub": "14ea6291-...-916bb7056c9a",
  "auth_time": 1587317601,
  "name": "John Doe",
  "preferred_username": "johndoe",
  "given_name": "John",
  "family_name": "Doe"
}
```

## Custom claims

The identity provider serves default claims such as the user’s `username`, `given_name`, `family_name`, and so on. You can add custom claims by updating the identity provider configuration.

### Add new user information

1. In AM Console, click **Settings > Providers**.
2. Select your identity provider settings, then click the **User mappers** tab.
3.  Map new custom claims with user attributes contained in your user data store.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-quickstart-profile-user-mappers.png" alt=""><figcaption><p>Add new user information</p></figcaption></figure>
4. Custom user attributes will be available in the UserInfo Endpoint response.

{% hint style="info" %}
You can find more information about User mapping in the [User and role mapping](../../guides/identity-providers/user-and-role-mapping.md) section.
{% endhint %}
