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

## Protected Resource Endpoints

Protected Resources represent OAuth 2.0 resource servers that can validate access tokens and participate in token exchange flows. The Management API provides endpoints for managing Protected Resources, their secrets, and memberships.

### Resource Management

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources` | POST | Create a new Protected Resource |
| `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources` | GET | List Protected Resources with optional search filters |
| `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{id}` | GET | Retrieve a specific Protected Resource |
| `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{id}` | DELETE | Delete a Protected Resource |

**Query Parameters for GET /protected-resources:**

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `q` | String | Search query supporting wildcard matching on name and clientId fields |
| `type` | String | Filter by resource type (e.g., `MCP_SERVER`) |
| `page` | Integer | Page number for pagination |
| `size` | Integer | Number of results per page (default: 50) |

### Secret Management

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{id}/secrets` | GET | List all secrets for a Protected Resource (metadata only) |
| `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{id}/secrets` | POST | Create a new secret for a Protected Resource |
| `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{id}/secrets/{secretId}` | DELETE | Delete a specific secret |
| `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{id}/secrets/{secretId}/_renew` | POST | Renew a secret, generating a new value while preserving settings |

### Membership Management

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{id}/members` | GET | List members assigned to a Protected Resource |
| `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{id}/members` | POST | Assign a user or group to a Protected Resource |
| `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{id}/members/{memberId}` | DELETE | Remove a member from a Protected Resource |
| `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{id}/members/permissions` | GET | Retrieve available permissions for Protected Resource members |
