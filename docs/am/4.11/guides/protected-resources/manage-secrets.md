### Creating a Protected Resource with Secrets

Create a Protected Resource via `POST /organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources` with a JSON body containing `name`, `clientId`, `type`, and an optional `certificate` field. The system validates certificate existence if provided and applies default OAuth settings from the Gateway Configuration section.

After creation, generate a secret via `POST /protected-resources/{id}/secrets` with the following request body:

```json
{
  "name": "secret-name"
}
```

The response includes the plaintext secret value, which is never returned again. Configure the Protected Resource as an audience in token exchange or client credentials flows. Use the `clientId` and secret for authentication at the token endpoint.

**Required Permission:** `PROTECTED_RESOURCE[CREATE]`

### Renewing Secrets

To renew a secret, call `POST /protected-resources/{id}/secrets/{secretId}/_renew`. The response contains the new plaintext value.

**Required Permission:** `PROTECTED_RESOURCE[UPDATE]`

### Deleting Secrets

To delete a secret, call `DELETE /protected-resources/{id}/secrets/{secretId}`. The system removes the secret from `clientSecrets` and removes the associated `secretSettings` entry only if no other secret references it.

**Required Permission:** `PROTECTED_RESOURCE[DELETE]`

### Listing Secrets

List all secrets (without plaintext values) via `GET /protected-resources/{id}/secrets`. The response returns safe (redacted) secrets containing metadata only.

**Required Permission:** `PROTECTED_RESOURCE[LIST]`

**Response Schema:**

```json
[
  {
    "id": "string",
    "name": "string",
    "settingsId": "string",
    "createdAt": "2025-01-01T00:00:00Z"
  }
]
```

### Managing Protected Resource Memberships

Add members via `POST /protected-resources/{id}/members` with the following request body:

```json
{
  "memberId": "user-or-group-id",
  "memberType": "USER|GROUP",
  "role": "role-name"
}
```

List members via `GET /protected-resources/{id}/members` and retrieve flattened permissions via `GET /protected-resources/{id}/members/permissions`. Remove members via `DELETE /protected-resources/{id}/members/{memberId}`.

**Required Permissions:**
- `PROTECTED_RESOURCE_MEMBER[CREATE]` for adding members
- `PROTECTED_RESOURCE_MEMBER[LIST]` for listing members
- `PROTECTED_RESOURCE[READ]` for retrieving permissions
- `PROTECTED_RESOURCE_MEMBER[DELETE]` for removing members

### Searching Protected Resources

Query Protected Resources via `GET /protected-resources?q={query}`. If the `q` parameter is present, the system searches `name` and `clientId` fields (case-insensitive) with wildcard support (`*` matches any characters). For example, `?q=client*` matches resources with names or client IDs starting with "client". If `q` is absent, all resources filtered by type are returned.

**Response Schema:**

```json
{
  "data": [
    {
      "id": "string",
      "clientId": "string",
      "name": "string",
      "description": "string",
      "type": "MCP_SERVER",
      "resourceIdentifiers": ["string"],
      "certificate": "string",
      "updatedAt": "2025-01-01T00:00:00Z"
    }
  ],
  "currentPage": 0,
  "totalCount": 1
}
```

### Event Configuration

Secret lifecycle operations emit domain events for audit and synchronization purposes.

The following table describes the event types emitted during secret lifecycle operations:

| Event Type | Action | Description |
|:-----------|:-------|:------------|
| `PROTECTED_RESOURCE_SECRET` | `CREATE` | Emitted when a new secret is generated |
| `PROTECTED_RESOURCE_SECRET` | `RENEW` | Emitted when an existing secret is renewed |
| `PROTECTED_RESOURCE_SECRET` | `DELETE` | Emitted when a secret is deleted |

{% hint style="info" %}
These events can be used to track secret lifecycle changes for compliance and monitoring purposes.
{% endhint %}
