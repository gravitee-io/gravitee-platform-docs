### Default OAuth Settings

When a Protected Resource is created, the following OAuth settings are applied automatically if not explicitly provided:

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `grantTypes` | `["client_credentials"]` | Default grant types for Protected Resources |
| `responseTypes` | `["code"]` | Default response types |
| `tokenEndpointAuthMethod` | `"client_secret_basic"` | Default authentication method |
| `clientId` | (copied from resource) | Matches the Protected Resource's client ID |
| `clientSecret` | (preserved if exists) | Retained from existing settings during updates |

### Event Configuration

Protected Resource secret lifecycle events are tracked using the `PROTECTED_RESOURCE_SECRET` event type with actions `CREATE`, `RENEW`, and `DELETE`. These events trigger notification registration and audit logging.

### Creating a Protected Resource with Secrets

To create a Protected Resource, submit a POST request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources` with the resource definition. The system performs the following actions:

1. Generates a default secret and applies OAuth settings automatically.
2. Overrides defaults if you provide custom `settings` in the request body.
3. Creates the first secret with the name "default" unless specified otherwise.
4. Registers secret expiration notifications immediately based on domain-level expiration policies.
5. Returns the plaintext secret value in the response—store it securely, as subsequent GET requests return only safe (redacted) representations.

### Managing Protected Resource Secrets

Secret management follows a REST API pattern at `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/secrets`:

1. **List all secrets:** Submit a GET request to `/secrets` (requires `PROTECTED_RESOURCE[LIST]` permission).
2. **Create a new secret:** Submit a POST request to `/secrets` with a JSON body containing `{"name": "string"}`. The response includes the plaintext secret.
3. **Renew an existing secret:** Submit a POST request to `/secrets/{secretId}/_renew`, which generates a new secret value and updates expiration tracking.
4. **Delete a secret:** Submit a DELETE request to `/secrets/{secretId}`, ensuring at least one secret remains. If the deleted secret's settings are not referenced by other secrets, the settings are also removed.

{% hint style="warning" %}
Plaintext secret values are only returned during creation and renewal. Store them securely—subsequent GET requests return only safe (redacted) representations.
{% endhint %}

{% hint style="info" %}
At least one secret must exist for each Protected Resource. The system enforces this requirement during deletion operations.
{% endhint %}

### Configuring Certificate-Based Authentication

Protected Resources support certificate-based JWT verification for token introspection:

1. Upload or reference a certificate in the domain's certificate store.
2. Assign the certificate to the Protected Resource by setting the `certificate` field (stored as `nvarchar(64)` in JDBC, string in MongoDB).
3. During token introspection, if the audience matches the Protected Resource's `clientId` and a certificate is configured, the system uses it for JWT signature verification.
4. If no certificate is configured, HMAC signing is assumed (empty certificate ID).

{% hint style="danger" %}
Certificates cannot be deleted if referenced by any Protected Resource. The system returns a `CertificateWithProtectedResourceException` (HTTP 400) with the message "You can't delete a certificate with existing protected resources."
{% endhint %}
