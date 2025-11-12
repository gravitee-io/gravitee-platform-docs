# OAuth 2.0

## Overview

[OAuth 2.0](https://tools.ietf.org/html/rfc6749) is the industry-standard protocol for authorization, providing specific authorization flows for web applications, desktop applications, mobile phones and home devices.

OAuth 2.0 specifies standard endpoints to interact with the resource owner (or the client when acting on its own behalf) to grant, introspect and revoke tokens used to access protected resources.

You can see which OAuth 2.0 protocol endpoints are exposed by AM in [this file](https://raw.githubusercontent.com/gravitee-io/gravitee-docs/master/am/current/oauth2/swagger.yml).

## Roles

OAuth 2.0 defines four roles:

**Resource owner**

An entity enabled to grant access to a protected resource. When the resource owner is a person, it is referred to as an _end user_.

**Resource server**

The server hosting the protected resources, capable of accepting and responding to protected resource requests using access tokens.

**Client**

An application making protected resource requests on behalf of the resource owner and with the resource owner’s authorization. The term _client_ does not imply any particular implementation characteristics (e.g. whether the application executes on a server, a desktop or other device).

**Authorization server**

The server issuing access tokens to the client after successfully authenticating the resource owner and obtaining authorization.

## Grant types

An authorization grant is a flow used by the client to obtain an access token.

The specification defines four grant types:

* [Authorization code](./#authorization-code)
* [Implicit](./#implicit)
* [Resource owner password credentials](./#resource-owner-password-credentials)
* [Client credentials](./#client-credentials)

{% hint style="info" %}
OAuth 2.0 also supports the use of [refresh tokens](./#refresh-token) to obtain new access tokens.

AM provides a mechanism for defining additional types. See [extension grants](extension-grants.md) for more information.

How you use grant types mainly depends on your type of application.
{% endhint %}

### Authorization code

The authorization code is used by applications to obtain a temporary code after requesting the authorization of the end user.

#### **Flow**

1. The end user clicks **Sign in** in the application.
2. The end user is redirected to the AM authorization server `/oauth/authorize?response_type=code`.
3. The end user authenticates using one of the configured identity providers and login options (MFA for example).
4. (Optional) A consent page is displayed to ask for user approval.
5. AM redirects the end user back to the application with an authorization code.
6. The application calls the AM authorization server `/oauth/token` to exchange the code for an access token (and optionally, a refresh token).
7. The application uses the access token to make secure API calls for the end user.

#### **Additional information**

* Authorization codes are single use.
* For server-side web apps, such as native (mobile) and Javascript apps, you also use the [PKCE extension](https://tools.ietf.org/html/rfc7636) as part of your flow, which provides protection against other attacks where the authorization code may be intercepted.
* Authorization code grant URL: `GET https://am-gateway/{domain}/oauth/authorize?response_type=code&client_id=web-app&redirect_uri=https://web-app/callback`
* For more information about this flow, see the [RFC](https://tools.ietf.org/html/rfc6749#section-1.3.1).

### Implicit

{% hint style="warning" %}
The OAuth standard now discourages the use of an implicit grant to request access tokens from Javascript applications. You should consider using the [Authorization code ](./#authorization-code)grant with a PKCE extension for all your applications.
{% endhint %}

The implicit grant is a simplified authorization code flow. Instead of getting a temporary code first, you can retrieve an access token directly from web browser redirection.

#### **Flow**

1. The end user clicks **Sign in** in the application.
2. The end user is redirected to the AM authorization server `/oauth/authorize?response_type=token`.
3. The end user authenticates using one of the configured identity providers and login options (MFA for example).
4. (Optional) A consent page is displayed to ask for user approval.
5. AM redirects the end user back to the application with an access token.
6. The application uses the access token to make secure API calls for the end user.

#### **Additional information**

* Implicit grant URL: `GET https://am-gateway/{domain}/oauth/authorize?response_type=token&client_id=web-app&redirect_uri=https://web-app/callback`
* For more information about this flow, see the [RFC](https://tools.ietf.org/html/rfc6749#section-1.3.2).

### Resource owner password credentials

The resource owner password credentials (i.e. username and password) can be used directly as an authorization grant to obtain an access token (using a REST approach).

The biggest difference from other flows is that the authentication process is triggered by the application and not the AM authorization server.

{% hint style="info" %}
This grant type should only be used when there is a high degree of trust between the resource owner and the client (e.g. the client is part of the device operating system or a highly privileged application) and when other authorization grant types are not available (such as the authorization code grant type).
{% endhint %}

#### **Flow**

1. The end user clicks **Sign in** and enters the user credentials (username/password) in the application form.
2. The application forward the credentials to the AM authorization server `/oauth/token`.
3. AM checks the credentials.
4. AM responds with an access token (and optionally, a refresh token).
5. The application uses the access token to make secure API calls for the end user.

#### **Additional information**

* Resource owner password credentials grant URL: `POST https://am-gateway/{domain}/oauth/token?grant_type=password&username=john&password=doe (with Basic client credentials)`
* For more information about this flow, see the [RFC](https://tools.ietf.org/html/rfc6749#section-1.3.3).

### Client credentials

The client credentials grant type is used by clients to obtain an access token outside the context of a user. This is typically used by clients to access resources about themselves rather than user resources.

#### **Additional information**

* The flow is typically used when the client is acting on its own behalf (the client is also the resource owner), i.e. machine-to-machine communication.
* Client credentials grant URL: `POST https://am-gateway/{domain}/oauth/token?grant_type=client_credentials` (with basic client credentials)
* For more information about this flow, see the [RFC](https://tools.ietf.org/html/rfc6749#section-1.3.4).

### Refresh token

A refresh token is used to get a new access token, prompting the client application to renew access to protected resources without displaying a login page to the resource owner.

#### **Additional information**

* The refresh token is single use only.
* For security reasons (a user can remain authenticated forever), a refresh token must be stored in a secure place (i.e server side).
* Refresh token grant URL: `POST https://am-gateway/{domain}/oauth/token?grant_type=refresh_token&refresh_token={refreshToken} (with Basic client credentials)`

## Endpoints

As described in the [AM API specification](docs/am/4.8/reference/am-api-reference.md), AM provides the following OAuth 2.0 endpoints:

### Authorization endpoint

The [authorization endpoint](https://tools.ietf.org/html/rfc6749#section-3.1) is used to interact with the resource owner and obtain an authorization grant. The authorization server must first verify the identity of the resource owner.

Authorization endpoint URL: `https://am-gateway/{domain}/oauth/authorize`

### Token endpoint

The [token endpoint](https://tools.ietf.org/html/rfc6749#section-3.2) is used by the client to obtain an access token by presenting its authorization grant or refresh token.

Token endpoint URL: `https://am-gateway/{domain}/oauth/token`

### Introspection endpoint

The [introspection endpoint](https://tools.ietf.org/html/rfc7662#section-2) takes a parameter representing an OAuth 2.0 token and returns a JSON \[RFC7159] document containing meta-information about the token, including whether it is currently active.

Introspection endpoint URL: `https://am-gateway/{domain}/oauth/introspect`

### Revocation endpoint

The [revocation endpoint](https://tools.ietf.org/html/rfc7009) allows clients to notify the authorization server that a previously obtained refresh or access token is no longer needed.

Revocation endpoint URL: `https://am-gateway/{domain}/oauth/revoke`

## Example

Let’s imagine that a user wants to access his personal data via a web application. The personal data is exposed through an API secured by OAuth 2.0 protocol.

1. The user must be logged in to access his data. The user requests the web application to sign in.
2. The web application sends an authorization request (resource owner requests access to be granted to the resource owner’s data) to the authorization server.

{% code overflow="wrap" %}
```bash
GET  https://am-gateway/{domain}/oauth/authorize?response=code&client_id=web-app&redirect_uri=https://web-app/callback&state=6789DSKL HTTP/1.1
```
{% endcode %}

3. The authorization server authenticates the resource owner and obtains authorization.

{% code overflow="wrap" %}
```bash
HTTP/1.1 302 Found
Location: https://am-gateway/{domain}/login?client_id=web-app

Login page with username/password form
```
{% endcode %}

{% code overflow="wrap" %}
```bash
HTTP/1.1 302 Found
Location: https://am-gateway/{domain}/oauth/confirm_access

Consent resource owner page. The resource owner accepts or denies permission for the web application to access the resource owner's personal data
```
{% endcode %}

```bash
HTTP/1.1 302 Found
Location: https://web-app/callback?code=js89p2x1&state=6789DSKL

Return to the web application
```

4\. The resource owner is an authenticated and approved web application acting on the resource owner’s behalf. The web application can request an access token.

{% code overflow="wrap" %}
```bash
POST https://am-gateway/{domain}/oauth/token HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
grant_type=authorization_code&code=6789DSKL&redirect_uri=https://web-app/callback&state=6789DSKL
```
{% endcode %}

```bash
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5...",
    "token_type": "bearer",
    "expires_in": 7199,
    "scope": "read",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5..."
}
```

5\. The web application has obtained an access token, which it can use to get the user’s personal data.

```bash
GET  https://api.company.com/users/@me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5...
```

6\. The Users API must check the incoming token to determine the active state of the access token and decide whether to accept or deny the request.

```bash
POST https://am-gateway/{domain}/oauth/introspect HTTP/1.1
Accept: application/json
Content-Type: application/x-www-form-urlencoded
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
token=eyJhbGciOiJIUzI1NiIsInR5...

Introspection request



HTTP/1.1 200 OK
Content-Type: application/json

{
  "active": true,
  "client_id": "web-app",
  "username": "jdoe",
  "sub": "Z5O3upPC88QrAjx00dis",
  "aud": "https://web-app",
  "iss": "https://am-gateway/",
  "exp": 1419356238,
  "iat": 1419350238
}

Introspection response



HTTP/1.1 200 OK
Content-Type: application/json

{
  "username": "jdoe",
  "family_name": "doe",
  "name": "John doe",
  "email": "jdoe@mail.com"
}

Users API response
```

7\. The access is valid and the web application can display the resource owner’s personal data. 8. If the resource owner decides to log out, the web application can ask the authorization server to revoke the active access token.

```bash
POST https://am-gateway/{domain}/oauth/revoke HTTP/1.1
Host: server.example.com
Content-Type: application/x-www-form-urlencoded
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
token=eyJhbGciOiJIUzI1NiIsInR5...

Revocation request



HTTP/1.1 200 OK

Revocation response
```
