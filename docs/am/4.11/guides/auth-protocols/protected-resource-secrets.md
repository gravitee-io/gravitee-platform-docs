### Managing Protected Resource Secrets

Protected Resources maintain a list of client secrets for authentication. Each secret has a unique ID, optional name, expiration date, and associated settings. At least one secret must exist at all times.

#### Creating a Secret

Create a secret for a Protected Resource via the Management API:

**Endpoint:**

```
POST /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/secrets
```

**Request Body:**

```json
{
  "name": "string",
  "expiresAt": "2024-12-31T23:59:59Z"
}
```

**Response:**

```json
{
  "id": "string",
  "name": "string",
  "secret": "string",
  "expiresAt": "2024-12-31T23:59:59Z",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

{% hint style="warning" %}
The `secret` value is only shown once in the response. Store it securely.
{% endhint %}

The system generates a secure random value and stores the secret in both the `clientSecrets` list and the `secretSettings` list. The `secretSettings` entry tracks expiration and notification metadata.

#### Renewing a Secret

Renew a secret before expiration to generate a new value while preserving metadata:

**Endpoint:**

The renewal generates a new secret value, updates the `expiresAt` field, and preserves the `settingsId` reference.

#### Deleting a Secret

Delete a secret via the Management API:

**Endpoint:**

The system removes the secret from the `clientSecrets` list and removes the associated `secretSettings` entry only if no other secrets reference it.

{% hint style="danger" %}
You cannot delete the last client secret. Attempting to do so returns the error: `"Cannot delete the last client secret"`
{% endhint %}

#### Secret Expiration Tracking

The system tracks secret expiration for notification purposes. When a secret approaches expiration, the system generates a `PROTECTED_RESOURCE_SECRET` event and sends notifications to domain owners. The notification includes:

* Client secret name and expiration date
* Protected Resource name
* Domain ID and owner

