
# Protected Resource Certificate Authentication

## Creating a Protected Resource with Certificate Authentication

Create a Protected Resource with certificate-based authentication by sending a POST request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources`.

1. Include the `certificate` field in the request body with a valid certificate ID.
2. The system validates that the certificate exists and applies OAuth defaults:
   * Grant type: `client_credentials`
   * Token endpoint authentication method: `client_secret_basic`
3. On successful creation, the resource receives a `clientId` and initial secret.
4. The secret inherits domain-level expiration settings and registers for expiration notifications.
5. The resource becomes available for token introspection and can be referenced in JWT `aud` claims.

{% hint style="info" %}
Certificate validation occurs during both creation and update operations. If you attempt to delete a certificate that is referenced by a Protected Resource, the system returns a `CertificateWithProtectedResourceException`.
{% endhint %}

## Managing Protected Resource Secrets

Manage secrets for a Protected Resource using the `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets` endpoint.

1. **List secrets:** Send a GET request to `/secrets`. Requires `PROTECTED_RESOURCE[LIST]` permission. The response returns safe (redacted) secrets without plaintext values.
2. **Create a secret:** Send a POST request to `/secrets` with a JSON body containing `{"name": "string"}`. Requires `PROTECTED_RESOURCE[CREATE]` permission. The response includes the plaintext secret value.
3. **Renew a secret:** Send a POST request to `/secrets/{secretId}/_renew`. Requires `PROTECTED_RESOURCE[UPDATE]` permission. The system generates a new secret value and re-registers expiration notifications.
4. **Delete a secret:** Send a DELETE request to `/secrets/{secretId}`. Requires `PROTECTED_RESOURCE[DELETE]` permission. If this is the last secret referencing its settings entry, the system also removes the settings entry.

{% hint style="warning" %}
At least one secret must remain for each Protected Resource. The system enforces this requirement during deletion operations.
{% endhint %}

{% hint style="info" %}
Certificate validation occurs during both creation and update operations. If you attempt to delete a certificate that is referenced by a Protected Resource, the system returns a `CertificateWithProtectedResourceException`.
{% endhint %}

## MCP Server Token Endpoint Restrictions

When the resource context is `McpServer`, only specific authentication methods are permitted at the token endpoint.

### Allowed authentication methods

The following authentication methods are supported for MCP Server contexts:

* `client_secret_basic`
* `client_secret_post`
* `client_secret_jwt`

### Excluded authentication methods

The following authentication methods are **not** supported for MCP Server contexts:

* `private_key_jwt`
* `tls_client_auth`
* `self_signed_tls_client_auth`
* `none`

### Grant type restrictions

Grant types are restricted to:

* `client_credentials`
* `urn:ietf:params:oauth:grant-type:token-exchange`

{% hint style="info" %}
Refresh token and PKCE options are hidden in the UI for MCP Server contexts.
{% endhint %}

## Database Schema

The `protected_resources` table includes a new `certificate` column to store certificate references. The column is nullable and has a maximum length of 64 characters (`nvarchar(64)`).

{% hint style="info" %}
**Migration ID:** `4.11.0-protected-resource-add-certificate`
{% endhint %}


