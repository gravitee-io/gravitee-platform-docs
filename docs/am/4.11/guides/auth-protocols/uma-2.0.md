# UMA 2.0

## Overview

User-Managed Access (UMA) is an OAuth-based protocol designed to give an individual a unified control point for authorizing who and what can get access to their digital data, content, and services, no matter where all those things live.

The authorization server and resource server interact with the client and requesting party in a way that is asynchronous with respect to resource owner interactions.

This lets a resource owner configure an authorization server with authorization grant rules (policy conditions) at will, rather than authorizing access token issuance synchronously just after authenticating.

For example, bank customer (resource owner) Alice with a bank account service (resource server) can use a sharing management service (authorization server) hosted by the bank to manage access to her various protected resources by her spouse Bob, accounting professional Charline, and financial information aggregation company Decide Account, all using different client applications. Each of her bank accounts is a protected resource, and two different scopes of access she can control on them are viewing account data and accessing payment functions.

{% hint style="info" %}
[The User-Managed Access (UMA) 2.0 Grant for OAuth 2.0 Authorization specification](https://docs.kantarainitiative.org/uma/wg/oauth-uma-grant-2.0-08.html#claim-redirect) discusses the use of the authorization server’s claims interaction endpoint for one or more interactive claims-gathering processes as the authorization server requires. AM does not support interactive claims gathering. Claims gathering is accomplished by having the requesting party acquire an OpenID Connect (OIDC) ID token.
{% endhint %}

## Using UMA 2.0

AM exposes an endpoint for discovering information about the UMA provider configuration.

* Discovery endpoint URL: `https://am-gateway/{domain}/uma/.well-known/uma2-configuration`
* UMA 2.0 protocol endpoints exposed by [AM API](https://raw.githubusercontent.com/gravitee-io/gravitee-docs/master/am/current/uma2/swagger.yml)

## Roles

The UMA grant flow enhances the OAuth entity definitions in order to accommodate the requesting party role.

**resource owner**

An entity capable of granting access to a protected resource, the _user_ in User-Managed Access. The resource owner may be an end user (natural person) or a non-human entity treated as a person for limited legal purposes (legal person), such as a corporation.

**requesting party**

A natural or legal person that uses a client to seek access to a protected resource. The requesting party may or may not be the same party as the resource owner.

**client**

An application that is capable of making requests for protected resources with the resource owner’s authorization and on the requesting party’s behalf.

**resource server**

A server that hosts resources on a resource owner’s behalf and is capable of accepting and responding to requests for protected resources.

**authorization server**

A server that protects, on a resource owner’s behalf, resources hosted on a resource server.

## Protocol flow

The UMA 2.0 flow enhances the standard OAuth 2.0 grant by defining formal communications between the UMA-enabled authorization server and resource server as they act on behalf of the resource owner.

```
                                             +------------------+
                                             |     resource     |
       +------------manage (out of scope)----|       owner      |
       |                                     +------------------+
       |                                               |
       |                protection                     |
       |                API access                  control
       |                token (PAT)              (out of scope)
       |                                               |
       v                                               v
+------------+                    +----------+------------------+
|            |                    |protection|                  |
|  resource  |                    |   API    |   authorization  |
|   server   |<-----protect-------| (needs   |      server      |
|            |                    |   PAT)   |                  |
+------------+                    +----------+------------------+
| protected  |                               |        UMA       |
| resource   |                               |       grant      |
|(needs RPT) |          requesting           |  (PCT optional)  |
+------------+          party token          +------------------+
       ^                  (RPT)               ^  persisted   ^
       |                                      |   claims     |
       |                                    push   token     |
       |                                   claim   (PCT)     |
       |                                   tokens         interact
       |                                      +--------+    for
       +------------access--------------------| client |   claims
                                              +--------+  gathering
                                                +---------------+
                                                |  requesting   |
                                                |     party     |
                                                +---------------+
```

## Endpoints

### Resource registration endpoint

The [resource registration endpoint](https://docs.kantarainitiative.org/uma/wg/rec-oauth-uma-federated-authz-2.0.html#resource-registration-endpoint) enables the resource server to put resources under the protection of an authorization server on behalf of the resource owner and manage them over time. The authorization server must first verify the identity of the resource owner.

* Resource registration endpoint URL: `https://am-gateway/{domain}/uma/protection/resource_set`

### Access policies endpoint

The [access policies endpoint](https://docs.kantarainitiative.org/uma/wg/rec-oauth-uma-federated-authz-2.0.html#reg-api) allows the resource server to redirect an end user resource owner to a specific user interface within the authorization server where the resource owner can immediately set or modify access policies subsequent to the resource registration action just completed.

* Access policies endpoint URL: `https://am-gateway/{domain}/uma/protection/resource_set/:resourceId/policies`
* Only the resource owner can create a policy to protect a resource; administrator users cannot create policies on behalf of a resource owner

The policies can be written with the Groovy language using the Groovy policy.

When the authorization server handles an incoming UMA 2 grant request, some attributes are automatically created.

* `{#request}`: current HTTP request including parameters, headers, path, and so on
* `{#context.attributes['client']}`: OAuth 2.0 client including clientId, clientName, and so on
* `{#context.attributes['user']}`: requesting party user including elementusername, firstName, lastName, email, roles and so on
* `{#context.attributes['permissionRequest']}`: requested permission for the given resource including resourceId and resourceScopes

The following example gives **read** access to a resource only for the requesting party **Bob**.

```
import io.gravitee.policy.groovy.PolicyResult.State

user = context.attributes['user']
permissionRequest = context.attributes['permissionRequest']

if (user.username == 'bob' && permissionRequest.resourceScopes.contains('read')) {
  result.state = State.SUCCESS;
} else {
  result.state = State.FAILURE;
}
```

### Permission endpoint

The [permission endpoint](https://docs.kantarainitiative.org/uma/wg/rec-oauth-uma-federated-authz-2.0.html#permission-endpoint) defines a means for the resource server to request one or more permissions (resource identifiers and corresponding scopes) from the authorization server on the client’s behalf, and to receive a permission ticket in return (for example, request party wants to access Alice documents (`GET /alice/documents/**`).

* Authorization endpoint URL: `https://am-gateway/{domain}/uma/protection/permission`

### Introspection endpoint

The [introspection endpoint](https://docs.kantarainitiative.org/uma/wg/rec-oauth-uma-federated-authz-2.0.html#introspection-endpoint) is an OAuth 2.0 endpoint that takes a parameter representing an OAuth 2.0 token and returns a JSON \[RFC7159] document representing the meta information about the token, including whether this token is currently active. The resource server uses this endpoint to determine whether the access token (RPT) is active and, if so, its associated permissions.

* Introspection endpoint URL: `https://am-gateway/{domain}/oauth/introspect`

## Example

Let’s imagine the user Alice (the resource owner) wants to share read access to her bank account with her accountant Bob (the requesting party). The personal bank account data is exposed through an API (the resource server) secured by OAuth 2.0 protocol.

1. Alice must log in to the bank application and configure access to personal data resources.
2. Bob will log in and use the bank application and the bank API to access Alice’s personal data.

### Configure your security domain

To use the UMA 2.0 protocol you must enable it at the security domain level.

1. Log in to AM Console as an administrator of your security domain.
2. Click **Settings > UMA**.
3. On the UMA page, enable **User-Managed Access (UMA) 2.0 support** and click **SAVE**.

#### **Create a resource owner**

1. Click **Settings > Users** and click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
2. Complete the details of the resource owner (Alice) and click **CREATE**.

{% hint style="info" %}
The resource owner needs to use the same identity provider as the provider to be used for the resource server application.
{% endhint %}

#### **Create a requesting party**

1. In **Settings > Users**, click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
2. Complete the details of the requesting party (Bob) and click **CREATE**.

{% hint style="info" %}
The requesting party needs to use the same identity provider as the provider to be used for the client application.
{% endhint %}

#### **Create the client application**

1. Click **Applications** and click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
2. Select the **Web** application type and click **Next**.
3. Complete the application details and click **Create**.
4. Click the **Identity Providers** tab and select the identity provider you set for your requesting party user (Bob).
5. Click the **Settings** tab and click **OAuth 2.0 / OIDC**.
6. In the **Scopes** section, add **openid** and **read** scopes and click **SAVE**.

#### **Create the resource server application**

1. In **Applications**, click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
2. Select **Resource Server** as the application type and click **Next**.
3. Complete the application details and click **Create**.
4. Click the **Identity Providers** tab and select the identity provider you set for your resource owner (Alice).

### Protect the resource owner's resources

#### **Get a Protection API Token (PAT)**

The resource owner must acquire a PAT to register a resource and create authorization grant rules. To obtain the PAT the resource owner must log in to the application using any [OAuth 2.0 flow](oauth-2.0#flow).

In this example, we are using the [Resource owner password flow](oauth-2.0#flow):

{% code overflow="wrap" %}
```sh
$ curl \
--request POST \
--data 'grant_type=password' \
--data 'username=alice' \
--data 'password=password' \
--data 'client_id=:Resource-Server-Client-ID' \
--data 'client_secret=:Resource-Server-Client-Secret' \
https://am-gateway/{domain}/oauth/token

{
  "access_token": "eyJraWQiOiJkZWZhdWx0LWdyYXZpdGVlLUFNLWtleSIsImFsZyI6IkhTMjU2In0.eyJzdWIiOi....",
  "token_type": "bearer",
  "scope": "uma_protection"
  "expires_in": 7199
}
```
{% endcode %}

{% hint style="info" %}
`Resource-Server-Client-ID` and `Resource-Server-Client-Secret` can be found in your resource server application settings page.

The `access_token` is the Protection API Token (PAT) that you can use to register the resources to protect.
{% endhint %}

#### **Register resources**

With the acquired PAT, the resource owner can now register a resource.

{% code overflow="wrap" %}
```sh
$ curl -X POST \
--header 'authorization: Bearer eyJraWQiOiJkZWZhdWx0LWdyYXZpdGVlLUFNLWtleSIsImFsZyI6IkhTMjU2In0.eyJzdWIiOi....' \
--header 'cache-control: no-cache' \
--header 'content-type: application/json' \
--data '{
   "resource_scopes":[
      "read"
   ],
   "description":"Account read access",
   "icon_uri":"http://www.example.com/icons/picture.png",
   "name":"Account access",
   "type":"http://www.example.com/resource/account"
}' \
https://am-gateway/{domain}/uma/protection/resource_set

{
  "_id": "62dcf5d7-baa6-4e01-9cf5-d7baa61e01ac",
  "resource_scopes": [
    "phone"
  ],
  "description": "Account read access",
  "iconUri": "http://www.example.com/icons/picture.png",
  "name": "Account access",
  "type": "http://www.example.com/resource/account",
  "user_access_policy_uri": "https://am-gateway/{domain}/uma/protection/resource_set/62dcf5d7-baa6-4e01-9cf5-d7baa61e01ac/policies"
  "created_at": 1593006070414,
  "updated_at": 1593006070414
}
```
{% endcode %}

{% hint style="info" %}
The PAT Bearer Token is used via the Authorization HTTP header. The `user_access_policy_uri` field gives you the URL to assign access policies to this resource.
{% endhint %}

#### **Assign access policies**

Now that your resource is created, you can protect and share access to it by defining some access policies.

{% code overflow="wrap" %}
```sh
$ curl -X POST \
--header 'authorization: Bearer eyJraWQiOiJkZWZhdWx0LWdyYXZpdGVlLUFNLWtleSIsImFsZyI6IkhTMjU2In0.eyJzdWIiOi....' \
--header 'cache-control: no-cache' \
--header 'content-type: application/json' \
--data '{
	"name": "policy-name",
	"enabled": true,
	"description": "policy-description",
	"type": "groovy",
	"condition": {
		"onRequestScript": "import io.gravitee.policy.groovy.PolicyResult.State\\nuser = context.attributes['user']\\nif(user.username == 'bob') { result.state = State.SUCCESS; } else { result.state = State.FAILURE;}"
	}
}' \
https://am-gateway/{domain}/uma/protection/resource_set/62dcf5d7-baa6-4e01-9cf5-d7baa61e01ac/policies

{
  "id": "f05eef05-adb3-4e66-9eef-05adb3be6683",
  "type": "GROOVY",
  "enabled": true,
  "name": "policy-name",
  "description": "policy-description",
  "order": 0,
  "condition": "{\"onRequestScript\":\"import io.gravitee.policy.groovy.PolicyResult.State\\nuser = context.attributes['user']\\nif(user.username == 'bob') { result.state = State.SUCCESS; } else { result.state = State.FAILURE;}\"}",
  "domain": "uma2_postman",
  "resource": "62dcf5d7-baa6-4e01-9cf5-d7baa61e01ac",
  "createdAt": 1593006804494,
  "updatedAt": 1593006859663
}
```
{% endcode %}

{% hint style="info" %}
The PAT Bearer Token is used via the Authorization HTTP header.

In this example we want to share access with our requesting party Bob. See [Access policies endpoint](uma-2.0.md#access-policies-endpoint) for more information.
{% endhint %}

### Request access to the resource owner's resources

#### **Get a Permission Ticket (PT)**

When the resource server receives a request for access to a resource, it needs to request a permission ticket. This permission ticket will be bound to a particular resource and corresponding scopes.

{% code overflow="wrap" %}
```sh
$ curl -X POST \
--header 'authorization: Bearer eyJraWQiOiJkZWZhdWx0LWdyYXZpdGVlLUFNLWtleSIsImFsZyI6IkhTMjU2In0.eyJzdWIiOi....' \
--header 'cache-control: no-cache' \
--header 'content-type: application/json' \
--data '[
	{
		"resource_id":"62dcf5d7-baa6-4e01-9cf5-d7baa61e01ac",
		"resource_scopes":[
			"read"
		]
	}
]' \
https://am-gateway/{domain}/uma/protection/permission

{
  "ticket": "fe594f7c-5284-4172-994f-7c5284617215"
}
```
{% endcode %}

{% hint style="info" %}
The PAT Bearer Token which is used via the Authorization HTTP header must be obtained by the resource server via the [OAuth 2.0 client credentials flow](https://github.com/gravitee-io/gravitee-platform-docs/tree/main/docs/am/4.2/guides/auth-protocols/oauth-2.0).

The `ticket` property in the response is the permission ticket, which will be used to obtain the Requesting Party Token.
{% endhint %}

#### **Get the Requesting Party Token (RPT)**

In order to get an RPT, the requesting party must be authenticated, so the first step is to log in to the requesting party.

In this example, we are using the Resource owner password flow:

{% code overflow="wrap" %}
```sh
$ curl \
--request POST \
--data 'grant_type=password' \
--data 'username=bob' \
--data 'password=password' \
--data 'client_id=:Client-Client-ID' \
--data 'client_secret=:Client-Client-Secret' \
https://am-gateway/{domain}/oauth/access_token

{
  "access_token": "eyJraWQiOiJkZWZhdWx0LWdyYXZpdGVlLUFNLWtleSIsImFsZyI6IkhTMjU2In0.eyJzdWIiOi....",
  "id_token": "eyJraWQiOiJkZWZhdWx0LWdyYXZpdGVlLUFNLWtleSIsImFsZyI6IkhTMjU2In0.eyJzdWIiOi....",
  "token_type": "bearer",
  "scope": "openid read"
  "expires_in": 7199
}
```
{% endcode %}

{% hint style="info" %}
`Client-Client-ID` and `Client-Client-Secret` can be found in your client application settings page.

The `id_token` will be used to prove the requesting party's identity and authentication state (known as claim token).
{% endhint %}

The requesting party then makes a request using the permission ticket and the acquired claim token (the `id_token`) to get a Requesting Party Token (RPT).

{% code overflow="wrap" %}
```sh
$ curl -X POST \
--header 'Authorization: Basic (Client-Client-ID:Client-Client-Secret)' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data 'grant_type=urn:ietf:params:oauth:grant-type:uma-ticket' \
--data 'ticket=fe594f7c-5284-4172-994f-7c5284617215' \
--data 'claim_token=eyJraWQiOiJkZWZhdWx0LWdyYXZpdGVlLUFNLWtleSIsImFsZyI6IkhTMjU2In0.eyJzdWIiOi...' \
--data 'claim_token_format=urn:ietf:params:oauth:token-type:id_token'
https://am-gateway/{domain}/oauth/token

{
  "access_token": "eyJraWQiOiJkZWZhdWx0LWdyYXZpdGVlLUFNLWtleSIsImFsZyI6IkhTMjU2In0.eyJzdWIiOi....",
  "token_type": "bearer",
  "expires_in": 7199
}
```
{% endcode %}

{% hint style="info" %}
To make the request you must use the permission `ticket` and the `claim_token` (`id_token`) acquired earlier.

The `access_token` property is the RPT.
{% endhint %}

#### **Get the resource owner's data**

The client application can now use the RPT to get the resource owner's personal data.

{% code overflow="wrap" %}
```sh
GET  https://api.company.com/bank/users/alice/documents
Authorization: Bearer eyJraWQiOiJkZWZhdWx0LWdyYXZpdGVlLUFNLWtleSIsImFsZyI6IkhTMjU2In0.eyJzdWIiOi....
```
{% endcode %}

{% hint style="info" %}
The RPT Bearer Token is used via the Authorization HTTP header.
{% endhint %}

The Bank API must check the incoming token to determine the active state of the access token and decide whether to accept or deny the request.

You can use the [Introspection endpoint](https://github.com/gravitee-io/gravitee-platform-docs/tree/main/docs/am/4.2/guides/auth-protocols/oauth-2.0) to inspect the properties of the RPT.

```sh
POST https://am-gateway/{domain}/oauth/introspect HTTP/1.1
Accept: application/json
Content-Type: application/x-www-form-urlencoded
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
token=b02063f8-2698-4141-a063-f82698e1419c

{
  "sub": "241322ab-1d10-4f5a-9322-ab1d105f5ac8",
  "permissions": [
    {
      "resourceId": "62dcf5d7-baa6-4e01-9cf5-d7baa61e01ac",
      "resourceScopes": [
        "read"
      ]
    }
  ],
  "domain": "uma2_postman",
  "iss": "https://am-gateway/{domain}/oidc",
  "active": true,
  "exp": 1593020894,
  "token_type": "bearer",
  "iat": 1593013694,
  "client_id": "Client-Client-ID",
  "jti": "SZtDy09nZVChtFVNW-_UxqE8iImfNspar2eE20mZxSU",
  "username": "bob"
}
```

In this example the RPT is valid and the resource server application can check if the requesting party can access the resource using the `permissions` property.

### Protected Resource as OAuth2 Client

Protected Resources can now function as OAuth2 clients with full secret lifecycle management. Each Protected Resource receives default OAuth2 settings on creation or update and can maintain multiple active secrets for rotation scenarios. The resource can be resolved by either its `clientId` (like standard Applications) or its `resourceIdentifier` (per RFC 8707).

#### Default OAuth2 Settings

Protected Resources automatically receive these defaults on creation or update if not explicitly provided:

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `settings.oauth.grantTypes` | `["client_credentials"]` | Allowed grant types |
| `settings.oauth.responseTypes` | `["code"]` | Allowed response types |
| `settings.oauth.tokenEndpointAuthMethod` | `"client_secret_basic"` | Token endpoint authentication method |
| `settings.oauth.clientId` | Copied from `resource.clientId` | OAuth2 client identifier |
| `settings.oauth.clientSecret` | Preserved if exists | Existing secret value retained |

User-provided values always take precedence over defaults.

#### Dual Resolution

The system can resolve Protected Resources by:
- **clientId**: Standard OAuth2 client identifier lookup
- **resourceIdentifier**: RFC 8707 resource identifier lookup

During token introspection, the system extracts the `aud` claim from the JWT. For single-audience tokens, it queries `ClientSyncService` by `clientId`, then `ProtectedResourceSyncService` by `clientId`, and finally validates via `ProtectedResourceManager` using the resource identifier. For multi-audience tokens, it always validates via resource identifier per RFC 8707.

### Secret Lifecycle Management

Protected Resources support full secret lifecycle operations: create, renew, and delete. Multiple secrets can exist simultaneously to support zero-downtime rotation.

#### Creating Secrets

Create a secret by sending a POST request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets` with a JSON body containing `{"name": "secret-name"}`. The API returns a `ClientSecret` object with the generated secret value, which is only displayed once.

**Request:**
```sh
POST /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets
Content-Type: application/json

{
  "name": "secret-name"
}
```

**Response:**
```json
{
  "id": "secret-id",
  "name": "secret-name",
  "secret": "generated-secret-value",
  "settingsId": "settings-reference-id",
  "expiresAt": "2024-12-31T23:59:59Z",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

{% hint style="warning" %}
The `secret` field is only returned on create and renew operations. Subsequent GET requests omit this field.
{% endhint %}

#### Renewing Secrets

Renew a secret by posting to the `/_renew` endpoint under the specific secret ID. This generates a new value while preserving algorithm settings.

**Request:**
```sh
POST /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets/{secretId}/_renew
```

**Response:**
```json
{
  "id": "secret-id",
  "name": "secret-name",
  "secret": "new-generated-secret-value",
  "settingsId": "settings-reference-id",
  "expiresAt": "2024-12-31T23:59:59Z",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

#### Deleting Secrets

Delete a secret with a DELETE request to its endpoint. The system automatically removes orphaned `ApplicationSecretSettings` when no secrets reference them.

**Request:**
```sh
DELETE /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets/{secretId}
```

#### Listing Secrets

List all secrets for a resource with a GET request to the secrets collection endpoint.

**Request:**
```sh
GET /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets
```

**Response:**
```json
[
  {
    "id": "secret-id-1",
    "name": "secret-name-1",
    "settingsId": "settings-reference-id",
    "expiresAt": "2024-12-31T23:59:59Z",
    "createdAt": "2024-01-01T00:00:00Z"
  },
  {
    "id": "secret-id-2",
    "name": "secret-name-2",
    "settingsId": "settings-reference-id",
    "expiresAt": "2024-12-31T23:59:59Z",
    "createdAt": "2024-01-01T00:00:00Z"
  }
]
```

### Certificate-Based JWT Verification

Protected Resources support an optional `certificate` field that specifies a custom signing key for JWT verification during token introspection. If no certificate is assigned, the system assumes HMAC-signed JWTs.

During token introspection, if the Protected Resource has a `certificate` field, that certificate is used for JWT signature verification. Otherwise, HMAC signing is assumed.

### Token Exchange with Protected Resources

Protected Resources in MCP Server context can exchange subject tokens for new access tokens using the token exchange grant.

#### Prerequisites

- Token exchange enabled at domain level (`tokenExchangeSettings.enabled = true`)
- Allowed subject token types configured in `tokenExchangeSettings.allowedSubjectTokenTypes`

#### Token Exchange Flow

1. The application obtains a subject token (access, refresh, or ID token) using standard OAuth2 flows.
2. The MCP Server submits a token exchange request with `grant_type=urn:ietf:params:oauth:grant-type:token-exchange`, the subject token, and its type.
3. The system validates the subject token type against the domain's `allowedSubjectTokenTypes`, verifies the token signature and expiration, extracts the `gis` claim, and issues a new access token.
4. The new token's lifetime cannot exceed the subject token's remaining validity.

**Request:**
```sh
POST /oauth/token
Content-Type: application/x-www-form-urlencoded
Authorization: Basic {client_credentials}

grant_type=urn:ietf:params:oauth:grant-type:token-exchange
&subject_token={subject_token}
&subject_token_type={token_type}
```

**Response:**
```json
{
  "access_token": "new-access-token",
  "token_type": "bearer",
  "expires_in": 3600
}
```

{% hint style="info" %}
Token exchange does not issue refresh tokens or ID tokens, even if `openid` scope is requested.
{% endhint %}

#### Token Exchange Configuration

Configure allowed subject token types at the domain level:

| Property | Example Value | Description |
|:---------|:--------------|:------------|
| `tokenExchangeSettings.enabled` | `true` | Enable token exchange grant |
| `tokenExchangeSettings.allowedSubjectTokenTypes` | `["urn:ietf:params:oauth:token-type:access_token", "urn:ietf:params:oauth:token-type:id_token"]` | Permitted subject token types for exchange |

### Protected Resource Schema

#### Core Fields

| Property | Type | Description |
|:---------|:-----|:------------|
| `certificate` | String (nullable) | Certificate ID for JWT verification |
| `settings` | ApplicationSettings | OAuth2 configuration object |
| `secretSettings` | List<ApplicationSecretSettings> | Secret algorithm settings |
| `clientId` | String | OAuth2 client identifier |
| `resourceIdentifiers` | List<String> | RFC 8707 resource identifiers (required, non-empty) |

#### Secret Response Schema

| Property | Type | Description |
|:---------|:-----|:------------|
| `id` | String | Secret identifier |
| `name` | String | User-provided secret name |
| `secret` | String | Secret value (only on create/renew) |
| `settingsId` | String | Reference to algorithm settings |
| `expiresAt` | Date | Expiration timestamp |
| `createdAt` | Date | Creation timestamp |

### Searching Protected Resources

Search Protected Resources by name or `clientId` using the `q` query parameter on the list endpoint:

```sh
GET /protected-resources?q=search-term
```

The search supports wildcards (`*`) and performs case-insensitive matching. For example, `?q=mcp-*` returns all resources with names or client IDs starting with "mcp-".

### Event Integration

Secret lifecycle operations emit `PROTECTED_RESOURCE_SECRET` events mapped to standard actions:
- `CREATE` for new secrets
- `UPDATE` for renewals
- `DELETE` for removals

These events integrate with the existing `ClientSecretNotifierService` for expiration notifications.

### Settings Cleanup

`ApplicationSecretSettings` objects are reference-counted. When a secret is deleted, the system checks if any other secrets reference the same `settingsId`. If not, the settings object is also deleted to prevent orphaned data.

### Restrictions

- Resource identifiers (`resourceIdentifiers`) must not be null or empty; validation throws `InvalidProtectedResourceException` if violated
- All resource identifiers within a domain must be unique; duplicate identifiers trigger `InvalidProtectedResourceException` on create or update
- All feature keys within a Protected Resource must be unique; duplicates trigger `InvalidProtectedResourceException`
- Certificates cannot be deleted if referenced by any Protected Resource; deletion throws `CertificateWithProtectedResourceException`
- MCP Servers in token exchange flows support only `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grants
- Subject token types must be in the domain's `allowedSubjectTokenTypes` list; unsupported types return `invalid_request` error
- Secret values are only returned on create and renew operations; subsequent GET requests omit the `secret` field

