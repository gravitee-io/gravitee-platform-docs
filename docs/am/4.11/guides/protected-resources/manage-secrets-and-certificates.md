### Prerequisites for Secret Management

Before managing Protected Resource secrets, complete the following:

* Access Management 4.11.0 or later
* Domain with OAuth 2.0 enabled
* For certificate-based verification: valid certificate uploaded to the domain
* For membership management: appropriate role permissions (PROTECTED_RESOURCE scope)

### Gateway Configuration for Token Introspection

Configure the following environment property to control RFC 8707 validation behavior:

| Property | Description | Default |
|:---------|:------------|:--------|
| `legacy.rfc8707.enabled` | Enable legacy RFC 8707 validation behavior (validates caller client ID match) | `true` |

### Creating a Protected Resource with Secrets

Create a Protected Resource via the Management API, optionally specifying a certificate for JWT verification and OAuth settings:

1. Send a POST request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources` with the resource definition.
2. If `settings` are provided in the request body, they are preserved. Otherwise, default OAuth settings are applied (`client_credentials` grant, `client_secret_basic` auth method).
3. To add a secret, POST to `/protected-resources/{resourceId}/secrets` with the following payload:



4. The response includes the plaintext secret value. Store it securely, as subsequent GET requests return masked values.
5. Associate a certificate by setting the `certificate` field to a valid certificate ID during creation or update.

### Managing Protected Resource Membership

Assign users or groups to Protected Resources to control access and permissions:

1. POST to `/protected-resources/{resourceId}/members` with a membership payload (user/group ID, role).
2. Retrieve current members via GET on the same endpoint.
3. Query available permissions with GET `/members/permissions`.
4. Remove a member by sending DELETE to `/members/{memberId}`.

Membership changes are audited and reflected immediately in access control checks.

### Searching Protected Resources

Query Protected Resources by name, client ID, or type using the search endpoint:

1. Send GET to `/protected-resources?q={query}&type={type}&page={page}&size={size}`.
2. The `q` parameter supports exact match or wildcard pattern matching using `*`.

### Secret Lifecycle Notifications

Protected Resource secrets trigger expiration notifications with the following structure:

**Notification Subject Data:**

| Field | Description |
|:------|:------------|
| `clientSecret` | Secret name and expiration date |
| `application` | Protected Resource name |
| `resourceType` | Formatted class name (e.g., "protected resource") |

**Metadata:**

| Field | Description |
|:------|:------------|
| `domainId` | Domain identifier |
| `domainOwner` | User identifier |
| `protectedResourceId` | Protected Resource identifier |
| `clientSecretId` | Secret identifier |

**Log Message Format:**

```
Client secret {clientSecretName} for protected resource {protectedResourceName} will expire on {expirationDate}
```

### Secret Value Masking

Secret values are masked in list operations. The plaintext value is returned only during creation or renewal. Subsequent GET requests return masked values via `ClientSecret.safeSecret()`.
