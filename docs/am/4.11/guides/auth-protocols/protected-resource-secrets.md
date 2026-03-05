### Creating a Protected Resource with Secrets

Create a Protected Resource via `POST /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources`. The system automatically generates an initial secret and applies default OAuth settings (`client_credentials` grant, `client_secret_basic` auth method).

#### Adding Additional Secrets

To add additional secrets, call `POST /protected-resources/{id}/secrets` with a `name` property. The response includes the plaintext secret value, which is visible only on creation.

**Request Body:**

**Response:** `ClientSecret` (includes plaintext secret on creation)

#### Renewing Secrets

Renew an existing secret via `POST /secrets/{secretId}/_renew`. This invalidates the old secret and returns a new plaintext value.

**Response:** `ClientSecret` (new secret value)

#### Deleting Secrets

Delete secrets via `DELETE /secrets/{secretId}`. The system prevents deletion if it would leave the resource with no secrets.

**Response:** `204 No Content`

### Secret Settings Reuse

When deleting a secret, if no other secrets reference the same `settingsId`, the OAuth settings are also removed.
