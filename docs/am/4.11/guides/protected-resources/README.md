### Prerequisites

Before managing Protected Resource secrets, ensure the following:

* Gravitee Access Management 4.11.0 or later
* Domain with OAuth 2.0 enabled
* Appropriate permissions: `PROTECTED_RESOURCE[CREATE]`, `PROTECTED_RESOURCE[UPDATE]`, `PROTECTED_RESOURCE[DELETE]`, or `PROTECTED_RESOURCE[LIST]` at the resource, domain, environment, or organization level

### Secret lifecycle model

Protected Resources support multiple client secrets with independent lifecycles. Each secret includes:

* Unique identifier
* Name
* Expiration date
* Associated settings (algorithm, etc.)

The system enforces a minimum of one active secret per resource. Secret values are generated using cryptographically secure random generation and are returned in plaintext only once during creation or renewal.

### Create a secret

To create a new secret for a Protected Resource:

1. Send a POST request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/secrets` with the following request body:

   ```json
   {
     "name": "string"
   }
   ```

2. The system generates a cryptographically secure secret value and returns the following response:

   ```json
   {
     "id": "string",
     "name": "string",
     "secret": "string",
     "settingsId": "string",
     "expiresAt": "date",
     "createdAt": "date"
   }
   ```

{% hint style="warning" %}
The plaintext secret value is returned only in this response. Store it securely, as it cannot be retrieved again.
{% endhint %}

### Renew a secret

To renew an existing secret:

1. Send a POST request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/secrets/{secretId}/_renew`.

2. The system deletes the old secret value, generates a new cryptographically secure value, and returns the same response structure as secret creation.

The renewal operation automatically unregisters the old secret's expiration notifications and registers new ones for the renewed secret.

### Delete a secret

To delete a secret:

1. Send a DELETE request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/secrets/{secretId}`.

2. The system removes the secret and unregisters its expiration notifications. If no other secrets reference the associated settings, those settings are also deleted.

{% hint style="danger" %}
You cannot delete the last remaining secret of a Protected Resource. The system returns the error message: `"You can't delete the last secret of a protected resource"`.
{% endhint %}

### List secrets

To retrieve all secrets for a Protected Resource:

1. Send a GET request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/secrets`.

2. The system returns a list of secrets without the plaintext secret values:

   ```json
   [
     {
       "id": "string",
       "name": "string",
       "settingsId": "string",
       "expiresAt": "date",
       "createdAt": "date"
     }
   ]
   ```

### Token Introspection with Protected Resources

When introspecting tokens, AM validates the `aud` (audience) claim against both Applications and Protected Resources using the following process:

#### Single-audience tokens

1. Check Application `clientId` values
2. Check Protected Resource `clientId` values
3. Fall back to resource identifier validation per RFC 8707

#### Multi-audience tokens

* Validate all audiences via resource identifiers

The matched client or resource provides the certificate ID for JWT signature verification.

{% hint style="info" %}
Token introspection follows RFC 8707 standards for resource identifier validation when direct client ID matching fails.
{% endhint %}

## Overview

Protected Resources in Gravitee Access Management support advanced secret management, certificate-based authentication, and token introspection workflows. These capabilities allow Protected Resources to participate in OAuth 2.0 token exchange flows (RFC 8693) and Model Context Protocol (MCP) server integrations. Full lifecycle management is available for client secrets, certificates, and membership permissions.

### Prerequisites

Before creating and configuring Protected Resources, ensure you have:

* Gravitee Access Management 4.11.0 or later
* Domain with OAuth 2.0 enabled
* For certificate-based authentication: valid certificate uploaded to the domain
* For membership management: `PROTECTED_RESOURCE_MEMBER` permission scope

### Creating a Protected Resource

Create a Protected Resource using the following endpoint:

```
POST /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources
```

The request body must include:

* `name` (required): Resource name
* `resourceIdentifiers` (required): Array of unique identifiers for the resource
* `settings` (optional): OAuth configuration object
* `certificate` (optional): Certificate ID for JWT signature verification

The system validates that:

* Resource identifiers are unique across the domain. Duplicate identifiers return the error: `Resource identifier [{identifier}] is already in use`
* The certificate exists if a certificate ID is provided
* The resource identifier list is not empty. Empty lists return the error: `Field [resourceIdentifiers] must not be empty`

On successful creation, the system:

* Applies default OAuth settings for any missing configuration fields
* Initializes secret expiration notifications

### OAuth Default Settings

When creating or updating a Protected Resource without explicit OAuth settings, the system applies the following defaults:

| Field | Default Value | Applied When |
|:------|:--------------|:-------------|
| `grantTypes` | `["client_credentials"]` | Field is null or empty |
| `responseTypes` | `["code"]` | Field is null or empty |
| `tokenEndpointAuthMethod` | `"client_secret_basic"` | Field is null |
| `clientId` | Resource's `clientId` | Field is null |

### Database Schema

The database schema for protected resources varies depending on your database type.

{% tabs %}
{% tab title="JDBC" %}
The `protected_resources` table includes a `certificate` column with the following properties:

* **Type:** `nvarchar(64)`
* **Nullable:** Yes

{% endtab %}

{% tab title="MongoDB" %}
The `protected_resources` collection includes a `certificate` field with the following properties:

* **Type:** `string`

{% endtab %}
{% endtabs %}

### MCP Server Context

The MCP Server context restricts OAuth configuration to grant types and authentication methods suitable for machine-to-machine communication. For more information, see [MCP Server Context](guides/mcp-servers/create-an-mcp-server.md#mcp-server-context).

**Allowed Grant Types:**

| Grant Type | Label | Usage |
|:-----------|:------|:------|
| `client_credentials` | Client Credentials | Direct machine-to-machine authentication |
| `urn:ietf:params:oauth:grant-type:token-exchange` | Token Exchange | Exchange subject tokens for access tokens (RFC 8693) |

**Allowed Token Endpoint Authentication Methods:**

| Method | Description |
|:-------|:------------|
| `client_secret_basic` | HTTP Basic authentication with client credentials |
| `client_secret_post` | Client credentials in request body |
| `client_secret_jwt` | JWT-based client authentication |

Refresh token and PKCE configuration sections are hidden in this context.

### Managing Secrets

#### Creating Secrets

Add secrets to a Protected Resource using:

```
POST /protected-resources/{protected-resource}/secrets
```

The request body requires a `name` field. The response includes the generated `secret` value. This is the only time the plaintext secret is returned.

#### Renewing Secrets

Renew an existing secret using:

```
POST /protected-resources/{protected-resource}/secrets/{secretId}/_renew
```

The system deletes the old secret, generates a new value, and returns the updated secret object with the new plaintext value.

#### Deleting Secrets

Delete a secret using:

```
DELETE /protected-resources/{protected-resource}/secrets/{secretId}
```

Deletion fails with the error `You can't delete the last secret of a protected resource` if only one secret remains. The system unregisters expiration notifications and removes associated settings if no other secrets reference them.

### Searching Protected Resources

Search for Protected Resources using:

```
GET /protected-resources?q={query}&type={type}&page={page}&size={size}
```

**Query Parameters:**

* `q` (optional): Search query supporting exact matches (case-insensitive on `name` or `clientId`) and wildcard patterns using `*` (e.g., `client*` matches `clientId` starting with "client")
* `type`: Resource type filter
* `page`: Page number (default: 0)
* `size`: Page size (default: 50)

Empty queries return all resources for the domain, ordered by `updated_at` descending.

### Managing Membership

Membership endpoints are available at `/protected-resources/{protected-resource}/members`. All operations require `PROTECTED_RESOURCE_MEMBER` permissions at the resource, domain, environment, or organization level.

**List Members:**

```
GET /members
```

Returns list of members with their roles.

**Add or Update Member:**

```
POST /members
```

Request body:

```json
{
  "memberId": "string",
  "memberType": "USER",
  "role": "string"
}
```

**Remove Member:**

```
DELETE /members/{member}
```

### Token Introspection with Protected Resources

See [Token Introspection with Protected Resources](#token-introspection-with-protected-resources) above for details.
### Token Introspection with Protected Resources

When introspecting tokens, the system validates the `aud` (audience) claim against both Applications and Protected Resources to determine which entity's certificate should be used for JWT signature verification.

#### Single-Audience Token Validation

For tokens with a single audience value, the system follows this resolution order:

1. Check if the audience matches an Application `clientId`
2. If not found, check if the audience matches a Protected Resource `clientId`
3. If not found, validate the audience as a resource identifier per RFC 8707

The matched Application or Protected Resource provides the certificate ID for JWT signature verification. If no certificate is configured, the system falls back to HMAC verification.

### OAuth Default Settings

See [OAuth Default Settings](#oauth-default-settings) above for details.
#### Multi-Audience Token Validation

For tokens with multiple audience values, the system validates all audiences by resource identifier according to RFC 8707. Each audience must resolve to a valid Protected Resource.

#### Validation Errors

The system returns specific error messages when audience validation fails:

| Condition | Error Message | Description |
|:----------|:--------------|:------------|
| Missing `aud` claim | `"The token is invalid"` | `"Token has no audience claim"` |
| Unresolvable audience | `"The token is invalid"` | `"Client or resource not found: {aud}"` |

{% hint style="info" %}
Token introspection requires the `aud` claim. Tokens without an audience claim are rejected.
{% endhint %}

### Database Schema

See [Database Schema](#database-schema) above for details.
## Prerequisites

Before you configure OAuth 2.0 resource protection, ensure the following:

* Gravitee Access Management 4.11.0 or later is installed
* A domain with OAuth 2.0 enabled
* For certificate-based authentication: A valid certificate uploaded to the domain
* For membership management: The `PROTECTED_RESOURCE_MEMBER` permission scope is configured

### Prerequisites

See [Prerequisites](#prerequisites) above for details.
### Search endpoint

Use the following endpoint to search Protected Resources:

```
GET /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources?q={query}&type={type}&page={page}&size={size}
```

#### Query parameters

| Parameter | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `q` | string | No | Search query. Supports exact matches (case-insensitive) on `name` or `clientId`, and wildcard patterns using `*` (e.g., `client*` matches any `clientId` starting with "client"). |
| `type` | string | No | Resource type filter. |
| `page` | integer | No | Page number. Default: 0. |
| `size` | integer | No | Page size. Default: 50. |

#### Response

Returns a paginated list of Protected Resources matching the search criteria.

### Search behavior

The search endpoint supports the following query types:

| Query Type | Behavior | Example |
|:-----------|:---------|:--------|
| Exact match | Case-insensitive match on `name` or `clientId` | `q=myresource` matches "MyResource" or "myresource" |
| Wildcard (`*`) | Pattern match using `*` as wildcard | `q=client*` matches "client-api", "client-web", etc. |
| Empty query | Returns all resources for the domain, ordered by `updated_at` descending | No `q` parameter |

{% hint style="info" %}
Wildcard queries are implemented using SQL LIKE (with `%`) in JDBC databases and regex (with `.*`) in MongoDB. Both implementations are case-insensitive.
{% endhint %}

## Renewing and Deleting Secrets

### Renew a Secret

To renew a secret, call:

```
POST /protected-resources/{protected-resource}/secrets/{secretId}/_renew
```

The system performs the following actions:

1. Deletes the old secret
2. Generates a new value
3. Returns the updated secret object with the new plaintext value

### Delete a Secret

See [Delete a Secret](#delete-a-secret) above for details.
### Example requests

Search for resources with names or client IDs starting with "api":

```
GET /protected-resources?q=api*
```

Retrieve all resources for a domain with custom pagination:

```
GET /protected-resources?page=0&size=100
```

Search for an exact resource name:

```
GET /protected-resources?q=production-api
```

### Prerequisites

See [Prerequisites](#prerequisites) above for details.
### Membership endpoints

Membership operations are available at the following base path:

```
/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/members
```

#### List members

Use `GET /members` to retrieve all members and their assigned roles for the Protected Resource.

#### Add or update a member

Use `POST /members` to add a new member or update an existing member's role.

**Request schema:**

```json
{
  "memberId": "string",
  "memberType": "USER",
  "role": "string"
}
```

#### Remove a member

Use `DELETE /members/{member}` to remove a member from the Protected Resource.

### Permission requirements

All membership operations require `PROTECTED_RESOURCE_MEMBER` permissions. The system checks permissions in the following order:

1. `PROTECTED_RESOURCE_MEMBER` on the specific resource
2. `PROTECTED_RESOURCE_MEMBER` on the domain
3. `PROTECTED_RESOURCE_MEMBER` on the environment
4. `PROTECTED_RESOURCE_MEMBER` on the organization

## Creating a Protected Resource with Secrets

To create a protected resource, send a `POST` request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources` with a JSON body containing the following fields:

* `name`: The name of the protected resource.
* `resourceIdentifiers`: An array of unique identifiers for the resource.
* `settings` (optional): OAuth configuration settings.
* `certificate` (optional): The ID of an existing certificate.

The system validates that:

* Resource identifiers are unique across the domain.
* The certificate exists if a certificate ID is provided.

On creation, the system applies default OAuth settings for any missing fields and initializes secret expiration notifications.

### Adding Secrets

To add a secret to a protected resource, send a `POST` request to `/protected-resources/{protected-resource}/secrets` with a JSON body containing the `name` field.

The response includes the generated `secret` value.

{% hint style="warning" %}
The plaintext secret is returned only once. Store it securely.
{% endhint %}

## Related Changes

The UI now filters grant types and token endpoint authentication methods when the context is set to `McpServer`. This hides the refresh token and PKCE configuration sections.

The notification system exposes Protected Resource data to templates via `ClientSecretNotifierSubject`. This includes:

* Domain
* User
* Client secret properties
* `resourceType` field

## Searching Protected Resources

To search for protected resources, use the following endpoint:

```
GET /protected-resources?q={query}&type={type}&page={page}&size={size}
```

### Query Parameters

See [Query Parameters](#query-parameters) above for details.
### Pagination

Results are paginated with a default page size of 50. Use the `page` and `size` parameters to control pagination.

### Default Behavior

If the query is empty, the endpoint returns all protected resources for the domain, ordered by `updated_at` in descending order.

### Prerequisites

- Gravitee Access Management 4.11.0 or later

### Event Subscription

The Protected Resource Secret Manager subscribes to lifecycle events on service initialization.

| Event Type | Operations | Description |
|:-----------|:-----------|:------------|
| `PROTECTED_RESOURCE_SECRET` | `CREATE`, `RENEW`, `DELETE` | Secret lifecycle operations |

### OAuth Default Settings

See [OAuth Default Settings](#oauth-default-settings) above for details.
### Database Schema

#### JDBC

The `protected_resources` table includes a `certificate` column (nvarchar(64), nullable).

#### MongoDB

The `protected_resources` collection includes a `certificate` field (string).

### Protected Resource Secrets

Protected Resources can maintain multiple client secrets with independent lifecycles. Each secret includes:

* An identifier
* An expiration date
* Associated settings

The system enforces a minimum of one active secret per resource and generates cryptographically secure values using `SecureRandomString.generate()`.

#### Secret Management Operations

You can perform the following operations on Protected Resource secrets:

* **Create**: Add a new secret to the resource
* **Renew**: Generate a new secret value while preserving the existing settings
* **Delete**: Remove a secret from the resource

{% hint style="info" %}
Renewal operations automatically unregister old expiration notifications and register new ones.
{% endhint %}

### Token Introspection with Protected Resources

See [Token Introspection with Protected Resources](#token-introspection-with-protected-resources) above for details.
### MCP Server Context

The MCP Server context restricts OAuth configuration to a subset of grant types and authentication methods suitable for machine-to-machine communication.

#### Available Grant Types

Only the following grant types are available in MCP Server context:

* `client_credentials`
* `urn:ietf:params:oauth:grant-type:token-exchange`

#### Token Endpoint Authentication

Token endpoint authentication is limited to the following methods:

* `client_secret_basic`
* `client_secret_post`
* `client_secret_jwt`

#### Hidden Configuration Sections

The following configuration sections are not available in MCP Server context:

* Refresh token configuration
* PKCE (Proof Key for Code Exchange) configuration

### Certificate-Based Authentication

Protected Resources can use certificates for authentication during token introspection. When creating or updating a Protected Resource, you can optionally specify a certificate ID in the `certificate` field. If provided, the certificate must already exist in the domain.

During token introspection, the system validates the JWT audience claim against registered clients and Protected Resources. For single-audience tokens, the system first checks if the audience matches an Application `clientId`, then checks if it matches a Protected Resource `clientId`, and finally validates against resource identifiers per RFC 8707. For multi-audience tokens, all audiences are validated via resource identifiers. The matched client or resource provides the certificate ID for JWT signature verification.

#### Prerequisites

Before configuring certificate-based authentication for a Protected Resource:

* Upload a valid certificate to the domain via the Certificate Management API or Console

## Managing Membership

Use the membership endpoints to control access to protected resources. All operations require `PROTECTED_RESOURCE_MEMBER` permissions at the resource, domain, environment, or organization level.

### List Members

See [List Members](#list-members) above for details.
### Add or Update a Member

See [Add or Update a Member](#add-or-update-a-member) above for details.
### Remove a Member

See [Remove a Member](#remove-a-member) above for details.
