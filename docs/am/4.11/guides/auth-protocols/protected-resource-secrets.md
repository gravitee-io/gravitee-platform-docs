### Managing Protected Resource secrets

Secrets are managed via the `/protected-resources/{id}/secrets` endpoint. All secret management operations require the `PROTECTED_RESOURCE[UPDATE]` permission.

#### List secrets

Send a GET request to `/protected-resources/{id}/secrets` to retrieve all secrets for a Protected Resource. This operation requires the `PROTECTED_RESOURCE[LIST]` permission. The response excludes plaintext secret values and returns safe metadata (no plaintext).

#### Create a secret

Send a POST request to `/protected-resources/{id}/secrets` with a JSON body containing a `name` field. The response includes the plaintext secret value. Store this value immediately, as it is returned only once.

**Request body:**

**Response:** `ClientSecret` object with plaintext secret value.

#### Renew a secret

Send a POST request to `/secrets/{secretId}/_renew` to generate a new secret value. The secret ID is preserved, but a new value is generated and returned in the response. Store the new value immediately.

**Response:** `ClientSecret` object with new plaintext secret value.

#### Delete a secret

Send a DELETE request to `/secrets/{secretId}` to remove a secret. If the secret is the last one referencing a `secretSettings` entry, that entry is also removed. Multiple secrets can share the same `secretSettings` entry via `settingsId`.

**Response:** `204 No Content`

