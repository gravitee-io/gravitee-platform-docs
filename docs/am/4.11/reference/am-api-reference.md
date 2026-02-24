# API Reference

## Overview

{% hint style="info" %}
The OpenAPI specs for other versions of AM are available in the documentation for that version.
{% endhint %}

The AM API exposes a complete Restful API accessible to anyone wanting to script some part of the administration.

* To access the OpenAPI spec for AM 4.10, go to [OpenAPI spec](https://raw.githubusercontent.com/gravitee-io/gravitee-access-management/4.10.x/docs/mapi/openapi.yaml).

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

The `authorization` endpoint is used to interact with the end user to obtain the `AM Management API token`. The user is redirected to the AM login page and the authentication is processed to obtain the token using an HTTP cookie.

Here is example of how to retrieve and use the accessToken on the Management API:

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

For users migrations from an alternative OIDC provider to Access Management, you can define the `lastPasswordReset` attribute. This attribute ensures that a password policy with password expiry requests a password reset according to the value provided during the migration.

In Management REST API, `lastPasswordReset` attribute in the User definition is a long value representing the number of milliseconds since the standard base time known as "the epoch".

### Certificate Settings Endpoint

The Management API provides a dedicated endpoint for updating domain certificate settings without triggering a full domain reload. This endpoint enables administrators to configure fallback certificates and manage certificate-related domain settings with zero downtime.

#### Endpoint Details

**Method**: `PUT`
**Path**: `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings`

**Path Parameters**:
- `organizationId` — Organization identifier
- `environmentId` — Environment identifier
- `domain` — Domain identifier

**Request Body**:
```json
{
  "fallbackCertificate": "cert-id-or-null"
}
```

**Required Permission**: `DOMAIN_SETTINGS[UPDATE]`

#### Request Body Schema

| Property | Type | Description | Required |
|:---------|:-----|:------------|:---------|
| `fallbackCertificate` | string or null | Certificate ID to use when primary certificate fails. Set to `null` to disable fallback. | Yes |

#### Behavior

When you update certificate settings:

1. The system validates that the specified certificate exists and is accessible to the domain.
2. The configuration change is broadcast to all gateway nodes via a `DOMAIN_CERTIFICATE_SETTINGS` event.
3. Each gateway node reloads its in-memory certificate settings without requiring a domain restart.

#### Validation Rules

- The fallback certificate must exist in the target domain (or be accessible if the domain is a master domain).
- The fallback certificate cannot be the same as the client's primary certificate.
- Master domains can access certificates from all domains.
- Regular domains can only access certificates belonging to their own domain.

#### Example Request

```sh
curl -X PUT \
  http(s)://AM_MANAGEMENT_API/management/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings \
  -H 'Authorization: Bearer token' \
  -H 'Content-Type: application/json' \
  -d '{
    "fallbackCertificate": "cert-backup-2024"
  }'
```

#### Example Response

```
HTTP/1.1 200 OK
Content-Type: application/json
```

To disable fallback, send the same request with `"fallbackCertificate": null`.

