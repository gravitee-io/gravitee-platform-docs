
## Managing protected resource secrets


Secret rotation follows a create-renew-delete cycle:

1. **List existing secrets** via `GET /secrets` to identify the target secret.
2. **Rotate the secret** by sending a `POST` request to `/secrets/{secretId}/_renew`. This generates a new secret value and updates the expiration timestamp.
3. **Delete obsolete secrets** via `DELETE /secrets/{secretId}`. The system enforces that at least one secret must remain.
4. If the deleted secret was the last reference to a specific OAuth settings object, those settings are also removed.
5. All secret operations emit events that update expiration notifications in the background.

{% hint style="info" %}
The system requires at least one active secret at all times. Deletion requests that would remove the last secret will be rejected.
{% endhint %}

### GET `/secrets`

Retrieve all secrets for a Protected Resource. The response returns safe secrets with redacted plaintext values.

**Endpoint:**

```
GET /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/secrets
```

**Permission Required:** `PROTECTED_RESOURCE[LIST]`

**Response:** `Array<ClientSecret>` (safe secrets, no plaintext)

### POST `/secrets/{secretId}/_renew`

Renew an existing secret. This operation generates a new secret value and updates the expiration timestamp based on domain-level expiration policies.

**Endpoint:**

```
POST /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/secrets/{secretId}/_renew
```

**Permission Required:** `PROTECTED_RESOURCE[UPDATE]`

**Response:** `ClientSecret` (new secret value)

**Event Emitted:** `PROTECTED_RESOURCE_SECRET.RENEW`

**Background Actions:**
- Unregisters the old secret's expiration notification
- Registers a new expiration notification for the renewed secret

### DELETE `/secrets/{secretId}`

Delete a secret. The system enforces that at least one secret must remain. If the deleted secret is the last reference to a specific OAuth settings object, those settings are also removed.

**Endpoint:**

```
DELETE /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/secrets/{secretId}
```

**Permission Required:** `PROTECTED_RESOURCE[DELETE]`

**Response:** `204 No Content`

**Event Emitted:** `PROTECTED_RESOURCE_SECRET.DELETE`

**Background Actions:**
- Unregisters the secret's expiration notification
- Deletes the acknowledgement record
- Removes associated OAuth settings if no other secrets reference them

**Constraint:** Deletion fails if the secret is the only remaining secret for the Protected Resource.

### Secret Lifecycle Events

Protected Resource secret operations emit events tracked using the `PROTECTED_RESOURCE_SECRET` event type:

| Event Action | Trigger | Description |
|:-------------|:--------|:------------|
| `CREATE` | Secret creation | Registers expiration notification |
| `RENEW` | Secret renewal | Unregisters old notification, registers new |
| `DELETE` | Secret deletion | Unregisters notification and acknowledgement |

## OAuth Settings Defaults

When creating a Protected Resource, the following OAuth settings are applied automatically if not explicitly provided:

| Property | Default Value | Description |
|----------|---------------|-------------|
| `grantTypes` | `["client_credentials"]` | Allowed OAuth grant types |
| `responseTypes` | `["code"]` | Allowed OAuth response types |
| `tokenEndpointAuthMethod` | `"client_secret_basic"` | Default authentication method for token endpoint |
| `clientId` | (copied from resource) | OAuth client identifier |
| `clientSecret` | (preserved or generated) | OAuth client secret |

{% hint style="info" %}
These defaults ensure that Protected Resources have a valid OAuth configuration even when OAuth settings are not explicitly specified during creation.
{% endhint %}

## Configuring Certificate-Based Authentication

Protected Resources support certificate-based JWT verification for token introspection. This allows you to verify JWT signatures using uploaded certificates instead of shared secrets.

### Prerequisites

Before configuring certificate-based authentication, you must upload a certificate to the domain using the certificate management API.

### Configuration Steps

1. Upload a certificate to the domain via the certificate management API.
2. Update the Protected Resource configuration by adding the certificate ID to the `certificate` field.
3. Save the Protected Resource configuration.

### Verification Behavior

During token introspection, the system applies the following logic:

* If the token's audience matches the Protected Resource's `clientId` **and** a certificate is configured, the system uses that certificate for JWT signature verification.
* If no certificate is configured, the system assumes HMAC-signed tokens.

{% hint style="warning" %}
Certificates cannot be deleted while referenced by any Protected Resource. Deletion attempts return HTTP 400 with the error message: "You can't delete a certificate with existing protected resources."
{% endhint %}

### Audience Validation Rules

The following table describes how AM validates the `aud` (audience) claim in a JWT assertion based on the number and type of audiences present:

| Scenario | Validation Behavior |
|:---------|:-------------------|
| Single audience = Application clientId | Validates as Application, returns certificate ID |
| Single audience = Protected Resource clientId | Validates as Protected Resource, returns certificate ID or empty string |
| Single audience = Resource identifier | Falls back to RFC 8707 validation |
| Multiple audiences | Always validates via RFC 8707 (resource identifiers) |

{% hint style="info" %}
When multiple audiences are specified, AM always applies RFC 8707 validation rules using resource identifiers.
{% endhint %}

## Managing Members

Protected Resources support role-based access control through member assignments. Members can be individual users or groups, each assigned specific roles that define their permissions.

### Add a Member

1. Submit a POST request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{protected-resource}/members` with the member definition:

   ```json
   {
     "memberId": "string",
     "memberType": "USER|GROUP",
     "role": "string"
   }
   ```

   * `memberId`: Unique identifier of the user or group
   * `memberType`: Either `USER` or `GROUP`
   * `role`: Role identifier to assign

2. The system validates the request and creates the membership assignment.

### List Members

Submit a GET request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{protected-resource}/members` to retrieve all current member assignments.

The response includes an array of membership objects with member IDs, types, and assigned roles.

### Remove a Member

Submit a DELETE request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{protected-resource}/members/{member}` where `{member}` is the member identifier.

The system removes the membership assignment and returns HTTP 204 on success.

### Query Flattened Permissions

Submit a GET request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{protected-resource}/members/permissions` to retrieve the effective permission map for the current user.

The response shows all permissions inherited from resource, domain, environment, and organization levels.

{% hint style="info" %}
All membership operations require `PROTECTED_RESOURCE_MEMBER` permissions at the resource, domain, environment, or organization level. The system checks permissions in this four-tier hierarchy.
{% endhint %}

## Searching Protected Resources

The search API supports wildcard queries across resource names and client IDs. Submit a GET request to `/protected-resources?q={query}` where `{query}` is an optional case-insensitive search term.

Wildcards (`*`) are supported for pattern matching. If the query parameter is absent, all resources filtered by type are returned.

Results are paginated and include only primary data fields (ID, name, clientId, type).

## Restrictions

The following restrictions apply when configuring Protected Resources and their associated secrets:

* **Secret deletion**: At least one secret must exist per Protected Resource. Deletion of the last secret is blocked.
* **Certificate deletion**: Certificates cannot be deleted while referenced by any Protected Resource. Attempting to do so returns an HTTP 400 error.
* **MCP Server grant types**: The MCP Server context restricts grant types to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` only.
* **MCP Server authentication methods**: The MCP Server context restricts token endpoint authentication methods to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`.
* **Secret settings**: Secret settings are shared across secrets. Deleting a secret removes its settings only if no other secrets reference them.
* **Multi-audience token validation**: Multi-audience tokens always use RFC 8707 validation regardless of audience content.

{% hint style="warning" %}
Ensure that at least one secret remains configured for each Protected Resource to maintain functionality.
{% endhint %}

### MCP Server Grant Type Filtering

The following table describes the grant types allowed for MCP Server and Application contexts:

| Context | Allowed Grant Types |
|---------|---------------------|
| `McpServer` | `client_credentials`, `urn:ietf:params:oauth:grant-type:token-exchange` |
| `Application` | All grant types |

{% hint style="info" %}
MCP Server contexts are restricted to the `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grant types. Application contexts support all available grant types.
{% endhint %}
