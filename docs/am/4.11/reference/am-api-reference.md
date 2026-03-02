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

You can use the `token` endpoint to retrieve the `AM Management API token`. To retrieve the token, present the user credentials in the `Basic authentication scheme`.

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

## Dynamic Client Registration

### Registering Agent Applications via DCR

To register an agent application through the Dynamic Client Registration (DCR) endpoint:

1. Submit a POST request to the DCR endpoint with `application_type: "agent"` and desired OAuth settings.
2. The system validates the request through the standard DCR chain, then applies agent-specific constraints.
3. Forbidden grant types and response types are automatically removed.
4. If `token_endpoint_auth_method` is not specified, the system defaults to `client_secret_basic`.
5. If no valid grants remain, the system assigns `authorization_code` grant and `code` response type.
6. The validated client credentials are returned with sanitized settings.

{% hint style="warning" %}
Agent applications cannot use `implicit`, `password`, or `refresh_token` grant types. Agent applications cannot use response types `token`, `id_token`, or `id_token token`. Token endpoint authentication method `none` is disabled for agent applications in the UI.
{% endhint %}

### Related Changes

The following changes support the new Agent application type:

#### Management Console UI

* A new **Agentic Application** card appears in the application creation wizard. The card uses a `memory` icon and provides a description for AI assistants and autonomous agents.
* A new **Agent Metadata** menu item is added under the **Agent** section for agent applications. This menu item requires the `application_settings_read` permission.
* The grant flows configuration screen automatically filters out forbidden grant types for agent applications.
* The refresh token section is hidden for agent applications.

#### OpenAPI Schema

The OpenAPI schema version is updated to `4.11.0-SNAPSHOT` with the following changes:

* New `agentCardUrl` properties are added to the `Application`, `NewApplication`, and `PatchApplicationAdvancedSettings` schemas.
* The `ApplicationType` enum now includes `AGENT`.

#### Dependencies and Backend

* The frontend adds the `@a2a-js/sdk` dependency (v0.3.10) for parsing AgentCard metadata.
* The backend registers a new `agentCardWebClient` bean for fetching external AgentCard JSON.

## Agent Card Metadata

### Fetching Agent Card Metadata

Retrieve an agent's AgentCard JSON through the gateway proxy endpoint at `/organizations/{orgId}/environments/{envId}/domains/{domain}/applications/{appId}/agent-card`:

1. Ensure the application has `agentCardUrl` configured in advanced settings.
2. Send a GET request to the agent-card endpoint with `APPLICATION[READ]` permission.
3. The gateway fetches the JSON from the configured URL with a 5-second timeout and 512 KB size limit.
4. SSRF protection blocks requests to localhost, private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 169.254.0.0/16), and non-http(s) schemes.
5. The response is validated as JSON and proxied to the client with a 200 status, or an error is returned if validation fails.

{% hint style="warning" %}
AgentCard URLs must use http or https schemes only. AgentCard responses are limited to 512 KB maximum size. AgentCard fetch timeout is 5 seconds. SSRF protection blocks localhost and private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 169.254.0.0/16). AgentCard responses must return HTTP 200 status and valid JSON.
{% endhint %}

## User Migration

For users migrations from an alternative OIDC provider to Access Management, you can define the `lastPasswordReset` attribute. This attribute ensures that a password policy with password expiry requests a password reset according to the value provided during the migration.

In Management REST API, `lastPasswordReset` attribute in the User definition is a long value representing the number of milliseconds since the standard base time known as "the epoch".

## Version Requirements

{% hint style="info" %}
Agent application type requires Gravitee Access Management 4.11.0 or later.
{% endhint %}
