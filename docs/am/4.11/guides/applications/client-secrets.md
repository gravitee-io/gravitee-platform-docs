# Client Secrets

Gravitee AM supports enhanced client secret management, allowing for multiple secrets for each application and configurable expiration policies at both the domain level and application level. These features improve security and flexibility in managing client credentials.

## Multiple Client Secrets for each Application

### Overview

* **Multiple Secrets:** Each application can have multiple active client secrets. This facilitates secret rotation without downtime, as new secrets can be added before deprecating old secrets.
* **Management:** Secrets can be added, renewed, and revoked through the Gravitee AM UI Console or using the Management API.

### Use Cases

* **Secret Rotation:** Introduce a new secret while keeping the old one active to ensure uninterrupted service during rotation.
* **Environment Separation:** Assign different secrets for different environments under the same application. For example, development, staging, and production.
* **Third-Party Access:** Provide distinct secrets to third-party partners, allowing for individual revocation if necessary.

### Managing Secrets

You can manage secrets by adding, renewing, and deleting them from Application. Default limitation of client secrets for each Application is 10. You can override this in `gravitee.yml` like the following example:

```yaml
applications:
  secretsMax: 20
```

#### **Accessing Application Settings:**

1. Navigate to the **Applications** section in the Gravitee AM Console.
2. Select the application. that you want to configure.
3. Go to **Settings**, and select **Secrets & Certificates.**

#### **Adding a new secret:**

1.  Click **"+ New client secret"**.<br>

    <figure><img src="../../.gitbook/assets/Screenshot 2025-06-02 at 11.56.31 (1).png" alt=""><figcaption><p>New client secret</p></figcaption></figure>
2.  Provide description of new secret.<br>

    <div align="left"><figure><img src="../../.gitbook/assets/Screenshot 2025-06-02 at 11.57.31 (1).png" alt="" width="308"><figcaption><p>New client secret description</p></figcaption></figure></div>
3.  Copy generated secret.<br>

    <div align="left"><figure><img src="../../.gitbook/assets/Screenshot 2025-06-02 at 11.57.49.png" alt="" width="305"><figcaption><p>New client secret - copy</p></figcaption></figure></div>
4. Click OK.

#### **Renewing a secret:**

1. In the **Secrets & Certificates** tab, locate the secret to renew.
2.  Click **renew button** next to the corresponding secret.

    <figure><img src="../../.gitbook/assets/Screenshot 2025-06-02 at 12.32.24.png" alt=""><figcaption><p>Renew Client Secret</p></figcaption></figure>
3. Copy generated secret.\
   ![](<../../.gitbook/assets/Screenshot 2025-06-02 at 12.00.01.png>)
4. Click OK.

#### Deleting a secret:

1. In the **Secrets & Certificates** tab, locate the secret that you want to delete.
2.  Click the **delete button** next to the corresponding secret.\
    <br>

    <figure><img src="../../.gitbook/assets/Screenshot 2025-06-02 at 12.32.45.png" alt=""><figcaption><p>Delete Client Secret</p></figcaption></figure>
3. Confirm that you want to delete the secret by entering secret description.\
   ![](<../../.gitbook/assets/Screenshot 2025-06-02 at 12.00.38.png>)

{% hint style="warning" %}
Revoked secrets are immediately invalidated and cannot be used for authentication.
{% endhint %}

## Configurable Client Secret Expiration

### **Domain-Level Configuration:**

* **Purpose:** Set a default expiration duration for all client secrets within a domain to enforce regular rotation.
* **Configuration Steps:**
  1. Navigate to the **Domain**.
  2.  Go to **Settings**, and then **Client Secrets.**<br>

      <figure><img src="../../.gitbook/assets/Screenshot 2025-06-02 at 12.06.56.png" alt=""><figcaption><p>Domain Secret Settings</p></figcaption></figure>
  3. Enable client secret expiry.
  4. Set the **Expiry Time Unit** and **Expiry Time Duration**. For example, 3 months.
  5. Save the changes.

### **Application-Level Configuration:**

* **Purpose:** Override the domain-level expiration setting for specific applications requiring different policies.
* **Configuration Steps:**
  1. Navigate to the **Applications** section in the Gravitee AM Console.
  2. Select the desired application.
  3. Go to **Settings**, and then **Secrets & Certificates**.
  4.  Click **Settings**.<br>

      <figure><img src="../../.gitbook/assets/Screenshot 2025-06-02 at 12.28.04 (1).png" alt=""><figcaption><p>Application Secret Settings</p></figcaption></figure>
  5. Toggle **Use Domain Rules**, and then and select **Expiry Time Unit** and **Expiry Time Duration**.\
     ![](<../../.gitbook/assets/image (10).png>)
  6. Save the changes.

### **Behavior:**

* When a new secret is generated or a existing secret is renewed, the expiration date is calculated based on the configured duration.
* When Expiry Time Unit is set to NONE in application settings, no policy is applied for new/renewed secrets in application and expiry time is not set.
* Expired secrets are automatically invalidated and cannot be used for authentication.

### **Best Practices:**

* **Regular Rotation:** Implement a rotation policy that aligns with your organization's security requirements.
* **Monitoring:** Regularly monitor set alerts about upcoming expirations.

## Monitoring Client Secret Expiration

Gravitee AM provides support for monitoring client secret expiration through customizable notifications, allowing proactive management of client credentials.

### Notification Events

#### Notifications can be triggered automatically in the following two scenarios:

* **Client Secret Expired**: A notification is sent when a client secret reaches its expiration date.
* **Upcoming Secret Expiration**: Periodic notifications can be sent ahead of time, based on a configurable cron schedule, to proactively manage client secrets approaching expiration.

These notifications facilitate timely renewal of client secrets and reduce the risk of authentication failures due to expired credentials.

For detailed instructions on configuring the notification mechanisms, refer to the [AM API configuration](../../getting-started/configuration/configure-am-api/#configure-notifications-on-certificates-and-client-secret-expiry) section.

### Protected Resource Secret Management

Protected Resource Secret Management enables API administrators to create, rotate, and manage client secrets for Protected Resources (MCP Servers) in Gravitee Access Management. This feature allows Protected Resources to authenticate as OAuth2 clients for token introspection and token exchange workflows, supporting multi-secret rotation and certificate-based JWT verification.

#### Protected Resource as OAuth2 Client

Protected Resources function as OAuth2 clients with full secret lifecycle management. Each Protected Resource receives default OAuth2 settings (`client_credentials` grant, `client_secret_basic` authentication) and can maintain multiple active secrets for rotation scenarios. The resource can be resolved by either its `clientId` (like standard Applications) or its `resourceIdentifier` (per RFC 8707).

#### Secret Lifecycle

Secrets follow a managed lifecycle:

* **Create**: Generates a random secret and stores algorithm settings
* **Renew**: Generates a new value while preserving the settings reference
* **Delete**: Removes the secret and cleans up orphaned settings

Multiple secrets can exist simultaneously to support zero-downtime rotation.

#### Certificate-Based JWT Verification

Protected Resources support an optional `certificate` field that specifies a custom signing key for JWT verification during token introspection. If no certificate is assigned, the system assumes HMAC-signed JWTs.

#### Prerequisites

* Access Management domain with OAuth2 enabled
* `PROTECTED_RESOURCE_SECRET` event type configured for audit logging
* Token exchange enabled at domain level (`tokenExchangeSettings.enabled = true`) if using token exchange workflows
* Valid certificate uploaded to the domain if using certificate-based JWT signing

#### OAuth2 Default Settings

Protected Resources automatically receive these defaults on creation or update if not explicitly provided:

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `settings.oauth.grantTypes` | `["client_credentials"]` | Allowed grant types |
| `settings.oauth.responseTypes` | `["code"]` | Allowed response types |
| `settings.oauth.tokenEndpointAuthMethod` | `"client_secret_basic"` | Token endpoint authentication method |
| `settings.oauth.clientId` | Copied from `resource.clientId` | OAuth2 client identifier |
| `settings.oauth.clientSecret` | Preserved if exists | Existing secret value retained |

User-provided values always take precedence over defaults.

#### Token Exchange Settings

Configure allowed subject token types at the domain level:

| Property | Example Value | Description |
|:---------|:--------------|:------------|
| `tokenExchangeSettings.enabled` | `true` | Enable token exchange grant |
| `tokenExchangeSettings.allowedSubjectTokenTypes` | `["urn:ietf:params:oauth:token-type:access_token", "urn:ietf:params:oauth:token-type:id_token"]` | Permitted subject token types for exchange |

#### Creating and Managing Secrets

Use the Management API to manage Protected Resource secrets:

* **Create a secret**: Send a POST request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets` with a JSON body containing `{"name": "secret-name"}`. The API returns a `ClientSecret` object with the generated secret value, which is only displayed once.
* **Renew a secret**: Post to the `/_renew` endpoint under the specific secret ID. This generates a new value while preserving algorithm settings.
* **Delete a secret**: Send a DELETE request to the secret's endpoint. The system automatically removes orphaned `ApplicationSecretSettings` when no secrets reference them.
* **List secrets**: Send a GET request to the secrets collection endpoint to retrieve all secrets for a resource.

#### Token Introspection with Protected Resources

During token introspection, the system resolves the caller by extracting the `aud` claim from the JWT:

* **Single-audience tokens**: The system first queries `ClientSyncService` by `clientId`, then `ProtectedResourceSyncService` by `clientId`, and finally validates via `ProtectedResourceManager` using the resource identifier.
* **Multi-audience tokens**: The system always validates via resource identifier per RFC 8707.

If the Protected Resource has a `certificate` field, that certificate is used for JWT signature verification. Otherwise, HMAC signing is assumed.

#### Token Exchange with MCP Servers

MCP Servers (Protected Resources in MCP context) can exchange subject tokens for new access tokens:

1. The application obtains a subject token (access, refresh, or ID token) using standard OAuth2 flows.
2. The MCP Server submits a token exchange request with `grant_type=urn:ietf:params:oauth:grant-type:token-exchange`, the subject token, and its type.
3. The system validates the subject token type against the domain's `allowedSubjectTokenTypes`, verifies the token signature and expiration, extracts the `gis` claim, and issues a new access token with the MCP Server's `clientId` as both client and audience.

The new token's lifetime cannot exceed the subject token's remaining validity. No refresh or ID tokens are issued in token exchange flows.

#### Protected Resource Schema

**Core Fields**

| Property | Type | Description |
|:---------|:-----|:------------|
| `certificate` | String (nullable) | Certificate ID for JWT verification |
| `settings` | ApplicationSettings | OAuth2 configuration object |
| `secretSettings` | List<ApplicationSecretSettings> | Secret algorithm settings |
| `clientId` | String | OAuth2 client identifier |
| `resourceIdentifiers` | List<String> | RFC 8707 resource identifiers (required, non-empty) |

**Secret Response Schema**

| Property | Type | Description |
|:---------|:-----|:------------|
| `id` | String | Secret identifier |
| `name` | String | User-provided secret name |
| `secret` | String | Secret value (only on create/renew) |
| `settingsId` | String | Reference to algorithm settings |
| `expiresAt` | Date | Expiration timestamp |
| `createdAt` | Date | Creation timestamp |

#### Searching Protected Resources

Search Protected Resources by name or `clientId` using the `q` query parameter on the list endpoint: `GET /protected-resources?q=search-term`. The search supports wildcards (`*`) and performs case-insensitive matching. For example, `?q=mcp-*` returns all resources with names or client IDs starting with "mcp-".

#### Event Integration

Secret lifecycle operations emit `PROTECTED_RESOURCE_SECRET` events mapped to standard actions:

* `CREATE` for new secrets
* `UPDATE` for renewals
* `DELETE` for removals

These events integrate with the existing `ClientSecretNotifierService` for expiration notifications.

#### Settings Cleanup

`ApplicationSecretSettings` objects are reference-counted. When a secret is deleted, the system checks if any other secrets reference the same `settingsId`. If not, the settings object is also deleted to prevent orphaned data.

#### MCP Server UI Context

The UI filters token endpoint authentication methods when displaying Protected Resources in MCP Server context, showing only `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`. Methods like `private_key_jwt`, `tls_client_auth`, and `none` are hidden.

#### Restrictions

* Resource identifiers (`resourceIdentifiers`) must not be null or empty. Validation throws `InvalidProtectedResourceException` if violated.
* All resource identifiers within a domain must be unique. Duplicate identifiers trigger `InvalidProtectedResourceException` on create or update.
* All feature keys within a Protected Resource must be unique. Duplicates trigger `InvalidProtectedResourceException`.
* Certificates cannot be deleted if referenced by any Protected Resource. Deletion throws `CertificateWithProtectedResourceException`.
* MCP Servers in token exchange flows support only `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange` grants.
* Token exchange does not issue refresh tokens or ID tokens, even if `openid` scope is requested.
* Subject token types must be in the domain's `allowedSubjectTokenTypes` list. Unsupported types return `invalid_request` error.
* Secret values are only returned on create and renew operations. Subsequent GET requests omit the `secret` field.

#### Related Changes

The Management API adds five new endpoints under `/protected-resources/{id}/secrets` for CRUD operations. The UI filters token endpoint authentication methods in MCP Server context to exclude certificate-based and public client methods. Token introspection logic now queries Protected Resources by `clientId` as a fallback after checking Applications. Validation rules enforce uniqueness for resource identifiers and feature keys, and prevent certificate deletion when referenced by Protected Resources. The search capability extends the list endpoint with wildcard support for name and `clientId` fields.

