---
metaLinks:
  alternates:
    - https://app.gitbook.com/s/H4VhZJXn1S232OEmh8Wv/reference/am-api-reference
---

# API Reference

## Overview

{% hint style="info" %}
The OpenAPI specs for other versions of AM are available in the documentation for that version.
{% endhint %}

The AM API exposes a complete Restful API accessible to anyone wanting to script some part of the administration.

* To access the OpenAPI spec for AM 4.11, go to [OpenAPI spec](https://raw.githubusercontent.com/gravitee-io/gravitee-access-management/4.11.x/docs/mapi/openapi.yaml).

## Authorization

AM API is secured using token-based authorization.

{% hint style="info" %}
Use the following HTTP Authorization request header to call the API: `Authorization Bearer token`. Also, you can use an `Authorization="Bearer token"` cookie to access the API resources.
{% endhint %}

### Token endpoint

You can use the `token` endpoint to retrieve the `AM Management API token` . To retrieve the token, present the user credentials in the `Basic authentication scheme`.

The following example exchanges default admin account credentials (`admin/adminadmin`) for a token:

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

The `authorization` endpoint is used to interact with the end user to obtain the `AM Management API token`. The user is redirected to the AM login page, and the authentication is processed to obtain the token using an HTTP cookie.

Here is an example of how to retrieve and use the accessToken on the Management API:

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

* `redirect_uri`: redirection endpoint after authentication success

### User Migration

For user migrations from an alternative OIDC provider to Access Management, you can define the `lastPasswordReset` attribute. This attribute ensures that a password policy with password expiry requests a password reset according to the value provided during the migration.

In Management REST API, `lastPasswordReset` attribute in the User definition is a long value representing the number of milliseconds since the standard base time known as "the epoch".

### CIMD Logo Endpoint

**Endpoint:** `GET /{domain}/cimd/logo?clientId={url-encoded-client-id}`

Retrieves the logo image for a CIMD client. The gateway fetches the `logo_uri` from cached metadata (or fetches metadata on cache miss), validates the URI against SSRF rules, and retrieves the logo with a 256 KB size limit. Logos are cached in-memory with TTL equal to the remaining metadata TTL.

**Response Codes:**

- `200 OK`: Logo retrieved successfully. Response includes `Content-Type: image/*` and `Cache-Control: max-age={ttl}` header.
- `404 Not Found`: No logo available or metadata missing.

**Validation:**

- Logo URIs are validated against SSRF protection rules (same as metadata document URIs)
- Maximum logo size is 256 KB
- Logos are cached in-memory with TTL matching the remaining metadata cache TTL
