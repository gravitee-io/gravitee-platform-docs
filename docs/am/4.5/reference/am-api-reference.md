---
description: API and reference documentation for AM API Reference.
---

# AM API Reference

## Overview

{% hint style="info" %}
The OpenAPI specs for other versions of AM are available in the documentation for that version.
{% endhint %}

The AM API exposes a complete Restful API accessible to anyone wanting to script some part of the administration.

* To access the OpenAPI spec for AM 4.5, go to [OpenAPI spec](https://raw.githubusercontent.com/gravitee-io/gravitee-access-management/4.5.x/docs/mapi/openapi.yaml).

## Authorization

AM API is secured using token-based authorization.

{% hint style="info" %}
Use the HTTP Authorization request header (`Authorization Bearer token`) to call the API. You can also use an `Authorization="Bearer token"` cookie to access the API resources.
{% endhint %}

### Token endpoint

The `token` endpoint is used to obtain the `AM Management API token` by presenting user credentials via the `Basic authentication scheme`.

The following example exchanges default admin account credentials (`admin/adminadmin`) for a token.

{% code overflow="wrap" %}
```sh
POST http(s)://AM_MANAGEMENT_API/management/auth/token HTTP/1.1

curl -X POST \
  http(s)://AM_MANAGEMENT_API/management/auth/token \
  -H 'authorization: Basic base64(admin:adminadmin)' 


  HTTP/1.1 200 OK
  Cache-Control: no-cache, no-store, max-age=0, must-revalidate
  Pragma: no-cache
  Expires: 0
  Content-Type: application/json
  {
      "access_token": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhZ....m4g9SK1fPtcPTLmbxWZDyP1hV9vjdsLdA",
      "expires_at": "Thu Jun 28 10:35:31 CEST 2018",
      "token_type": "bearer"
  }
```
{% endcode %}

### Authorization endpoint

The `authorization` endpoint is used to interact with the end user to obtain the `AM Management API token`. The user will be redirected to the AM login page and authentication processed to obtain the token via an HTTP cookie.

{% code overflow="wrap" %}
```sh
GET http(s)://AM_MANAGEMENT_API/management/auth/authorize?redirect_uri=http://callback-app HTTP/1.1

curl http(s)://AM_MANAGEMENT_API/management/auth/authorize?redirect_uri=http://callback-app

  HTTP/1.1 302 Found
  Location: http(s)://AM_MANAGEMENT_API/management/auth/login


POST http(s)://AM_MANAGEMENT_API/management/auth/login

  Set-Cookie: Authorization="Bearer token"
  HTTP/1.1 302 Found
  Location: http://callback-app
```
{% endcode %}

* `redirect_uri`: redirection endpoint after authentication success\\
