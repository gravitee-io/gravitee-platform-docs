# Refresh Tokens

## Overview

A refresh token is used to get a new access token without user interaction (i.e. sign-in process).

This allows good practices such as shortening the access token lifetime for security purposes without involving the user when the access token expires.

By default, the refresh token is single-use only and must be used to request a new access token until it expires.

{% hint style="info" %}
For security reasons, a refresh token must be stored in a secure place (i.e. server-side) because they essentially allow a user to remain authenticated forever.
{% endhint %}

## Get refresh tokens

To get refresh tokens during OAuth 2.0 flows (authorization\_code or password) the **Refresh Token** Grant Type must be selected in your application settings.

For example, if you are using the OAuth 2.0 Password Flow, the request would look like the following:

```sh
curl --request POST \
  --url 'https://AM_GW/{domain}/oauth/token' \
  --header 'content-type: application/x-www-form-urlencoded' \
  --header 'authorization: Basic (clientId:clientSecret)'
  --data 'grant_type=password' \
  --data 'username={password}' \
  --data 'password={password}'
```

The response will contain an access token and a refresh token (+ id\_token if you have specified the openid scope).

```sh
{
  "access_token": "eyJraWQiOi...kZWZh",
  "refresh_token": "eyJraWBHSHD...zessdOLS",
  "token_type": "Bearer",
  "scope": "...",
  "expires_in": "..."
}
```

{% hint style="info" %}
Be sure to securely store the refresh token as it will be used to get a new access token without user credentials.
{% endhint %}

## Use refresh tokens

A refresh token is used to get a new access token without user interaction (i.e. sign-in process).

To use a refresh token, the application must call the OAuth 2.0 Token Endpoint, the request would look like the following :

```sh
curl --request POST \
  --url 'https://AM_GW/{domain}/oauth/token' \
  --header 'content-type: application/x-www-form-urlencoded' \
  --header 'authorization: Basic (clientId:clientSecret)'
  --data 'grant_type=refresh_token' \
  --data 'refresh_token={refreshToken}'
```

{% hint style="info" %}
By default the refresh token is single use only. See [refresh token rotation](refresh-tokens.md#refresh-token-rotation) for more information.
{% endhint %}

The response will contain an access token and a **new** refresh token (+ id\_token if you have specified the openid scope).

```sh
{
  "access_token": "eyJraWQiOi...kZWZh",
  "refresh_token": "eyJraWBHSHD...zessdOLS",
  "token_type": "Bearer",
  "scope": "...",
  "expires_in": "..."
}
```

## Revoke refresh tokens

A refresh token can be revoked if it has been compromised or it has to be removed by the end of a user session.

{% hint style="info" %}
By default the refresh token is single use only. See[ refresh token rotation](refresh-tokens.md#refresh-token-rotation) for more information.
{% endhint %}

To revoke a refresh token, the application must call the OAuth 2.0 Revocation Endpoint, the request would look like the following :

```sh
curl --request POST \
  --url 'https://AM_GW/{domain}/oauth/revoke' \
  --header 'content-type: application/x-www-form-urlencoded' \
  --header 'authorization: Basic (clientId:clientSecret)'
  --data 'token={refreshToken}'
```

The application should match the one for which the refresh token was issued.

## Refresh token rotation

Refresh token rotation enabled applications to get a new access token and a new refresh token every time a refresh token is used.

The way refresh token rotation works is to conform with the [OAuth 2.0 Best Security Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics-22#name-refresh-token-protection) meaning that each refresh token can be used only once and a new refresh token is issued after every new token request.

### Disable Refresh Token Rotation

You can disable the refresh token rotation to reuse refresh tokens until expiration to issue new access tokens.

With this mode, you limit the number of refresh tokens to be issued and force the user to sign in after the refresh token has expired, but you can be exposed to security risk if the refresh token has been compromised as it can be reused.

To disable the refresh token rotation :

1. Log in to AM Console.
2. Go to **Application → Settings → OAuth 2.0 / OIDC**.
3. Select **Disable Refresh Token Rotation**.
4. Press **SAVE**.
