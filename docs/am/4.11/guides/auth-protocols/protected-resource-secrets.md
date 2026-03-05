### Secret Management Architecture

Protected Resources store secrets in two parallel arrays:

* **`clientSecrets`**: Stores full secret data (value, expiration, name)
* **`secretSettings`**: Stores algorithm configurations shared across secrets via `settingsId`

When you create a secret, the system generates a random value and creates an `ApplicationSecretSettings` entry. Both the secret and its settings are stored in their respective arrays. The `settingsId` links the secret to its configuration.

On renewal, the system generates a new secret value while preserving the `settingsId` reference. When you delete a secret, the system removes its settings only if no other secrets reference the same `settingsId`.

### Create a Secret

To create a new secret for a Protected Resource:

1. Send a POST request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/secrets` with the following request body:

   ```json
   {
     "name": "string"
   }
   ```

   The `name` field is required.

2. The system generates a random secret value and returns the following response:

   ```json
   {
     "id": "string",
     "name": "string",
     "secret": "string",
     "settingsId": "string",
     "expiresAt": "2025-01-01T00:00:00Z",
     "createdAt": "2025-01-01T00:00:00Z"
   }
   ```

   The `secret` field contains the generated value. This is the only time the secret value is returned.

3. The system emits a `PROTECTED_RESOURCE_SECRET.CREATE` audit event.

4. The system registers an expiration notification based on the domain's `SecretExpirationSettings`.

### Renew a Secret

To renew an existing secret:

1. Send a POST request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/secrets/{secretId}/_renew`.

2. The system generates a new secret value, updates the expiration date, and preserves the `settingsId`. The response matches the creation response format:

   ```json
   {
     "id": "string",
     "name": "string",
     "secret": "string",
     "settingsId": "string",
     "expiresAt": "2025-01-01T00:00:00Z",
     "createdAt": "2025-01-01T00:00:00Z"
   }
   ```

   The `secret` field contains the new value. This is the only time the renewed secret value is returned.

3. The system emits a `PROTECTED_RESOURCE_SECRET.RENEW` audit event.

4. The system unregisters the old expiration notification and registers a new one.

### List Secrets

To retrieve metadata for all secrets associated with a Protected Resource:

1. Send a GET request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/secrets`.

2. The system returns an array of secret metadata:

   ```json
   [
     {
       "id": "string",
       "name": "string",
       "settingsId": "string",
       "expiresAt": "2025-01-01T00:00:00Z",
       "createdAt": "2025-01-01T00:00:00Z"
     }
   ]
   ```

   The response does not include secret values. Secret values are only returned on creation or renewal.

## Prerequisites

Before configuring Token Exchange, ensure the following requirements are met:

* **OAuth 2.0 enabled domain**: The domain must have OAuth 2.0 enabled.
* **Certificate-based authentication** (if applicable): Upload a certificate in PEM format to the domain.
* **Token exchange configuration**: Configure the domain's `tokenExchangeSettings.allowedSubjectTokenTypes` property. The default allowed types are:
  * `access_token`
  * `refresh_token`
  * `id_token`
  * `jwt`
* **Secret expiration notifications** (if applicable): Configure the domain's `SecretExpirationSettings` to enable notifications for expiring secrets.

### Protected Resource Identity

A Protected Resource functions as an OAuth 2.0 client with resource server capabilities. Each resource has a unique `clientId`, optional `resourceIdentifiers` (URIs per RFC 8707), and OAuth settings that control authentication methods and grant types.

Resources can authenticate using:

* **Client secrets** with rotation support
* **JWT signatures** verified against uploaded certificates

When a token's `aud` claim matches a Protected Resource's `clientId` or resource identifier, the system validates the token against that resource's credentials.

### Delete a Secret

To delete a secret:

1. Send a DELETE request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/secrets/{secretId}`.

2. The system removes the secret from the `clientSecrets` array.

3. The system checks if the `settingsId` is still referenced by other secrets. If not, the system removes the settings from the `secretSettings` array.

4. The system emits a `PROTECTED_RESOURCE_SECRET.DELETE` audit event.

5. The system unregisters the expiration notification and deletes the acknowledgement.

### Secret Expiration Notifications

The system automatically triggers expiration notifications based on the domain's `SecretExpirationSettings`. Notifications are managed by the `ClientSecretNotifierService`.

When the service starts, it loads all Protected Resources, unregisters existing expiration notifications, and registers new notifications for each secret.
