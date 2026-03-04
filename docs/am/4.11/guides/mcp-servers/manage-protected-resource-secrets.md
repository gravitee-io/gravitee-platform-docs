
## Overview

Protected Resources now support advanced secret management, certificate-based authentication, and membership controls. These enhancements enable Protected Resources to participate fully in OAuth 2.0 token introspection flows and token exchange scenarios, with parity to Application-level security features. This feature is designed for API platform administrators managing resource servers and MCP (Model Context Protocol) server integrations.

### Certificate-Based Authentication

Protected Resources support X.509 certificate binding for mutual TLS (mTLS) authentication. Certificates are validated when you create or update a resource.

{% hint style="info" %}
A certificate cannot be deleted if any Protected Resource references it. The system enforces referential integrity and throws a `CertificateWithProtectedResourceException` if deletion is attempted.
{% endhint %}

### Managing Protected Resource Secrets

Protected Resource secrets are managed via the Management API at `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets`.

#### List Secrets

Retrieve all secrets for a Protected Resource.

**Endpoint:** `GET /secrets`

**Permission Required:** `PROTECTED_RESOURCE[LIST]`

**Response:** Array of `ClientSecret` objects (safe secrets, no plaintext values)

#### Create a Secret

Generate a new client secret for a Protected Resource.

**Endpoint:** `POST /secrets`

**Permission Required:** `PROTECTED_RESOURCE[CREATE]`

**Request Body:**

```json
{
  "name": "string"
}
```

**Response:** `ClientSecret` object (includes plaintext secret value on creation only)

{% hint style="info" %}
The plaintext secret is returned only once during creation. Store it securely.
{% endhint %}

Secrets inherit domain-level expiration policies and trigger notifications before expiry.

#### Renew a Secret

Generate a new value for an existing secret and re-register expiration notifications.

**Endpoint:** `POST /secrets/{secretId}/_renew`

**Permission Required:** `PROTECTED_RESOURCE[UPDATE]`

**Response:** `ClientSecret` object (new secret value)

#### Delete a Secret

Remove a client secret from a Protected Resource.

**Endpoint:** `DELETE /secrets/{secretId}`

**Permission Required:** `PROTECTED_RESOURCE[DELETE]`

**Response:** `204 No Content`

{% hint style="warning" %}
At least one secret must remain per Protected Resource. Deletion of the last secret is blocked.
{% endhint %}

If the deleted secret is the last one referencing its settings entry, the `ApplicationSecretSettings` entry is also removed.

### Managing Protected Resource Membership

Protected Resource membership is controlled via the Management API at `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/members`.

#### List Members

Retrieve all members assigned to a Protected Resource.

**Endpoint:** `GET /members`

**Permission Required:** `PROTECTED_RESOURCE_MEMBER[LIST]`

**Response:** Array of `Member` objects

#### Add a Member

Assign a user or group to a Protected Resource with a specific role.

**Endpoint:** `POST /members`

**Permission Required:** `PROTECTED_RESOURCE_MEMBER[CREATE]`

**Request Body:**

```json
{
  "memberId": "string",
  "memberType": "USER|GROUP",
  "role": "string"
}
```

**Response:** `Member` object

#### Remove a Member

Remove a user or group from a Protected Resource.

**Endpoint:** `DELETE /members/{member}`

**Permission Required:** `PROTECTED_RESOURCE_MEMBER[DELETE]`

**Response:** `204 No Content`

#### Retrieve Permissions

Retrieve flattened permissions for the current user on a Protected Resource.

**Endpoint:** `GET /members/permissions`

**Permission Required:** `PROTECTED_RESOURCE[READ]`

**Response:** Flattened permission list

Permissions are checked hierarchically:
1. Resource-level
2. Domain-level
3. Environment-level
4. Organization-level

The system returns the union of all applicable permissions for the current user.


