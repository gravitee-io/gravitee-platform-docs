### Creating a Protected Resource with Secrets

Create a Protected Resource by sending a POST request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources` with `name`, `resourceIdentifiers`, and optional `settings` and `certificate` fields. The system applies default OAuth settings (`client_credentials` grant, `client_secret_basic` auth method) if not provided.

Generate the first secret by sending a POST to `/protected-resources/{protected-resource}/secrets` with a `name` field:

The secret inherits expiration settings from the domain and triggers a `PROTECTED_RESOURCE_SECRET` CREATE event. If domain owners are configured, the system registers an expiration notification. Use the returned `clientId` and `secret` for client credentials authentication at the token endpoint.

### Renewing Secrets

Renew a secret without downtime by sending POST to `/protected-resources/{protected-resource}/secrets/{secretId}/_renew`. The system generates a new secret value while preserving the secret ID and name, allowing clients to rotate credentials gradually.

### Deleting Secrets

Delete a secret by sending DELETE to `/protected-resources/{protected-resource}/secrets/{secretId}`. The system blocks deletion if it is the last remaining secret, returning `ClientSecretNotFoundException`. Unused secret settings are automatically removed when no secrets reference them.
