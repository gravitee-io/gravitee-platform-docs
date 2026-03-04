### Creating Protected Resource Secrets

To create a secret for a protected resource:

1. Send a POST request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/secrets` with a JSON body containing the secret `name`.
2. The system generates a random secret value and returns it in plaintext along with the secret metadata.
3. Store the plaintext secret securely—it will not be retrievable later.
4. If the secret includes an `expiresAt` timestamp, the system registers an expiration notification.
5. The secret is immediately available for authentication at the token endpoint using the configured `tokenEndpointAuthMethod`.

**Request Body:**

```json
{
  "name": "string"
}
```

**Response:**

The response includes the `ClientSecret` object with the plaintext secret value. This is the only time the plaintext secret is returned.

{% hint style="warning" %}
Store the plaintext secret securely. It cannot be retrieved after creation.
{% endhint %}

### Renewing Protected Resource Secrets

To renew an existing secret:

1. Send a POST request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/secrets/{secretId}/_renew`.
2. The system generates a new secret value while preserving the secret's settings identifier.
3. The response includes the new plaintext secret.
4. The system unregisters the old expiration notification and registers a new one if the renewed secret has an `expiresAt` value.
5. The old secret value is immediately invalidated.

**Response:**

The response includes the `ClientSecret` object with the new plaintext secret value.

{% hint style="info" %}
Secret renewal requires an existing secret with a matching `secretId`.
{% endhint %}

### Secret Lifecycle Events

The system tracks secret lifecycle events and triggers notifications:

| Event | Description |
|:------|:------------|
| `CREATE` | Secret creation event |
| `RENEW` | Secret renewal event |
| `DELETE` | Secret deletion event |

Secrets with an `expiresAt` timestamp trigger expiration warnings when enabled.

### MCP Server Restrictions

MCP servers support a restricted subset of grant types and authentication methods.

#### Allowed Grant Types

* `client_credentials`
* `urn:ietf:params:oauth:grant-type:token-exchange`

#### Allowed Token Endpoint Auth Methods

* `client_secret_basic`
* `client_secret_post`
* `client_secret_jwt`

{% hint style="info" %}
MCP servers do not support other grant types or authentication methods outside of those listed above.
{% endhint %}
