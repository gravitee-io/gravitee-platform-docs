### Audience Validation Rules

Token introspection validates the `aud` claim according to the following scenarios:

| Scenario | Validation Behavior |
|:---------|:-------------------|
| Single audience = Application `clientId` | Validates as Application, returns certificate ID |
| Single audience = Protected Resource `clientId` | Validates as Protected Resource, returns certificate ID or empty string |
| Single audience = resource identifier | Falls back to RFC 8707 validation |
| Multiple audiences | Always validates via RFC 8707 (resource identifiers) |

{% hint style="info" %}
Multi-audience tokens always use RFC 8707 validation regardless of audience content.
{% endhint %}

### MCP Server Grant Type Filtering

When operating in MCP Server context, the system restricts available grant types:

| Context | Allowed Grant Types |
|:--------|:-------------------|
| `McpServer` | `client_credentials`, `urn:ietf:params:oauth:grant-type:token-exchange` |
| `Application` | All grant types |

## Related Changes

The following changes support MCP Server integration and enhanced client secret management:

### UI Grant Flows Component

The UI Grant Flows component now filters available grant types and authentication methods when operating in MCP Server context. User-facing flows such as `authorization_code` and `password` are hidden in this mode.

### Client Secret Expiration Notifications

Client secret expiration notifications now support dynamic resource types (Application or Protected Resource). Notifications include:

- Formatted log messages
- Metadata keys (e.g., `protectedResourceId`)

### Database Schema Changes

**JDBC:**

A nullable `certificate` column has been added to the `protected_resources` table.

**MongoDB:**

A corresponding `certificate` field has been added to the Protected Resource document schema.

### Repository Methods

New repository methods enable certificate dependency checks and resource discovery:

- `findByCertificate()` — Checks certificate dependencies
- `search()` — Enables wildcard-based resource discovery

### Permission Checks

Permission checks for secret and membership operations follow a four-tier hierarchy:

1. Resource
2. Domain
3. Environment
4. Organization

## Restrictions

The following restrictions apply to Protected Resources and their associated secrets and certificates:

* **Secret deletion**: At least one secret must exist per Protected Resource. Deletion of the last secret is blocked.
* **Certificate deletion**: Certificates cannot be deleted while referenced by any Protected Resource. Attempting to do so results in an HTTP 400 error.
* **MCP Server grant types**: The MCP Server context restricts grant types to `client_credentials` and `token-exchange` only.
* **MCP Server authentication methods**: The MCP Server context restricts token endpoint authentication methods to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`.
* **Secret settings**: Secret settings are shared across secrets. Deleting a secret removes its settings only if no other secrets reference them.
* **Multi-audience tokens**: Multi-audience tokens always use RFC 8707 validation regardless of audience content.
* **Certificate-based JWT verification**: Certificate-based JWT verification requires the `certificate` field to be populated. Null values default to HMAC signing.

### MCP Server Auth Method Filtering

When operating in MCP Server context, the system restricts available token endpoint authentication methods:

| Context | Allowed Methods |
|:--------|:---------------|
| `McpServer` | `client_secret_basic`, `client_secret_post`, `client_secret_jwt` |
| `Application` | All methods |

## Configuring Certificate-Based Authentication

Protected Resources support certificate-based JWT verification for token introspection. This allows you to verify JWT signatures using uploaded certificates instead of relying solely on HMAC-signed tokens.

### Prerequisites

Before configuring certificate-based authentication, you must upload a certificate to the domain via the certificate management API.

### Configuration Steps

1. Upload a certificate to the domain using the certificate management API.
2. Update the Protected Resource configuration by adding the certificate ID to the `certificate` field.
3. During token introspection, the system performs the following verification:
   * If the audience matches the Protected Resource's `clientId` and a certificate is configured, the system uses that certificate for JWT signature verification.
   * If no certificate is configured, the system assumes HMAC-signed tokens.

{% hint style="warning" %}
Certificates cannot be deleted while referenced by any Protected Resource. Deletion attempts return HTTP 400 with the error message: "You can't delete a certificate with existing protected resources."
{% endhint %}

## Searching Protected Resources

The search API supports wildcard queries across resource names and client IDs.

To search for protected resources, submit a GET request to `/protected-resources?q={query}`, where `{query}` is an optional case-insensitive search term. Wildcards (`*`) are supported for pattern matching.

If the query parameter is absent, all resources filtered by type are returned. Results are paginated and include only primary data fields (ID, name, clientId, type).

## Managing Protected Resource Membership

Membership controls access to Protected Resource management operations. Use the following endpoints to manage member assignments and permissions:

### Add members

Add members to a Protected Resource by sending a POST request to `/members`. Include the following parameters in the request body:

* `memberId`: The unique identifier of the user or group
* `memberType`: The type of member. Valid values are `USER` or `GROUP`
* `role`: The role to assign to the member

### List members

Retrieve a list of current member assignments by sending a GET request to `/members`.

### Remove members

Remove a member from a Protected Resource by sending a DELETE request to `/members/{member}`, where `{member}` is the member identifier.

### Query flattened permissions

View effective access rights by sending a GET request to `/members/permissions`. This endpoint returns the flattened permissions for the current user.

{% hint style="info" %}
All membership operations require `PROTECTED_RESOURCE_MEMBER` permissions at the resource, domain, environment, or organization level.
{% endhint %}
