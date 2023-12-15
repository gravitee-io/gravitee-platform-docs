# AM API Reference

## Overview

AM API exposes a complete Restful API accessible to anyone wanting to script some part of the administration.

You can access the online API reference or the OpenAPI specification:

* 3.21 — [online reference](https://docs.gravitee.io/am/current/management-api/3.21/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.21/swagger.json)
* 3.20 — [online reference](https://docs.gravitee.io/am/current/management-api/3.20/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.20/swagger.json)
* 3.19 — [online reference](https://docs.gravitee.io/am/current/management-api/3.19/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.19/swagger.json)
* 3.18 — [online reference](https://docs.gravitee.io/am/current/management-api/3.18/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.18/swagger.json)
* 3.17 — [online reference](https://docs.gravitee.io/am/current/management-api/3.17/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.17/swagger.json)
* 3.16 — [online reference](https://docs.gravitee.io/am/current/management-api/3.16/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.16/swagger.json)
* 3.15 — [online reference](https://docs.gravitee.io/am/current/management-api/3.15/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.15/swagger.json)
* 3.14 — [online reference](https://docs.gravitee.io/am/current/management-api/3.14/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.14/swagger.json)
* 3.13 — [online reference](https://docs.gravitee.io/am/current/management-api/3.13/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.13/swagger.json)
* 3.12 — [online reference](https://docs.gravitee.io/am/current/management-api/3.12/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.12/swagger.json)
* 3.11 — [online reference](https://docs.gravitee.io/am/current/management-api/3.11/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.11/swagger.json)
* 3.10 — [online reference](https://docs.gravitee.io/am/current/management-api/3.10/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.10/swagger.json)
* 3.9 — [online reference](https://docs.gravitee.io/am/current/management-api/3.9/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.9/swagger.json)
* 3.8 — [online reference](https://docs.gravitee.io/am/current/management-api/3.8/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.8/swagger.json)
* 3.7 — [online reference](https://docs.gravitee.io/am/current/management-api/3.7/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.7/swagger.json)
* 3.6 — [online reference](https://docs.gravitee.io/am/current/management-api/3.6/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.6/swagger.json)
* 3.5 — [online reference](https://docs.gravitee.io/am/current/management-api/3.5/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.5/swagger.json)
* 3.4 — [online reference](https://docs.gravitee.io/am/current/management-api/3.4/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.4/swagger.json)
* 3.3 — [online reference](https://docs.gravitee.io/am/current/management-api/3.3/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.3/swagger.json)
* 3.2 — [online reference](https://docs.gravitee.io/am/current/management-api/3.2/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.2/swagger.json)
* 3.1 — [online reference](https://docs.gravitee.io/am/current/management-api/3.1/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.1/swagger.json)
* 3.0 — [online reference](https://docs.gravitee.io/am/current/management-api/3.0/index.html) - [OpenAPI spec](https://docs.gravitee.io/am/current/management-api/3.0/swagger.json)

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
  -H 'authorization: Basic base64(admin:adminadmin)' \


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
