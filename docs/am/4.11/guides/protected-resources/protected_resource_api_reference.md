### Protected Resource Membership

Protected Resources support role-based membership management. Members (users or groups) are assigned roles that control access to resource configuration and secrets. Permissions are enforced at the API level using `PROTECTED_RESOURCE_MEMBER[LIST|CREATE|DELETE]` and `PROTECTED_RESOURCE[READ]` scopes.

### Prerequisites

* Domain with OAuth 2.0 enabled
* For token exchange: Token Exchange enabled in domain settings
* For certificate binding: Valid certificate uploaded to the domain
* For membership: Users or groups defined in the organization

### Secret Management Endpoints

#### Base Path

`/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/secrets`

**Example:**
```
/organizations/org-1/environments/env-1/domains/my-domain/protected-resources/pr-123/secrets
```

#### Authentication

All endpoints require a Bearer token with appropriate permissions.

**Example:**

#### Supported Operations

| Method | Path | Description | Required Permission |
|:---|:---|:---|:---|
| GET | `/` | List secrets of a protected resource | PROTECTED_RESOURCE[LIST] |
| POST | `/` | Create a secret for a protected resource | PROTECTED_RESOURCE[CREATE] |
| POST | `/{secretId}/_renew` | Renew a secret for a protected resource | PROTECTED_RESOURCE[UPDATE] |
| DELETE | `/{secretId}` | Remove a secret for a protected resource | PROTECTED_RESOURCE[DELETE] |

#### Request Body for POST (Create Secret)

#### Response Schema (ClientSecret)

### Membership Endpoints

#### Base Path

See [Base Path](#base-path) above for details.
#### Authentication

See [Authentication](#authentication) above for details.
#### Supported Operations

See [Supported Operations](#supported-operations) above for details.
#### Request Body for POST (Add Member)

See [Request Body for POST (Add Member)](#request-body-for-post-add-member) above for details.
### Search Parameters

The following query parameters are supported for Protected Resource search operations:

| Parameter | Description | Default | Example |
|:----------|:------------|:--------|:--------|
| `q` | Search query with wildcard support (`*`). Searches against `name` and `clientId` fields. | None | `q=client*` |
| `type` | Resource type filter | None | `type=MCP_SERVER` |
| `page` | Page number | 0 | `page=0` |
| `size` | Page size | 50 | `size=10` |

**Example Request:**
