### Creating a Protected Resource

Create a Protected Resource by sending a POST request to `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources`. The request requires the `PROTECTED_RESOURCE[CREATE]` permission.

**Request Body:**

| Field | Required | Description |
|:------|:---------|:------------|
| `name` | Yes | Protected Resource name |
| `clientId` | Yes | Client identifier |
| `type` | Yes | Resource type (e.g., `MCP_SERVER`) |
| `resourceIdentifiers` | No | Array of resource identifier URIs |

#### Default OAuth Settings

If the `settings` field is omitted or incomplete, the system applies default OAuth settings:

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `grantTypes` | `["client_credentials"]` | Default grant types |
| `responseTypes` | `["code"]` | Default response types |
| `tokenEndpointAuthMethod` | `client_secret_basic` | Default authentication method |
| `clientId` | (copied from resource) | Matches Protected Resource client ID |
| `clientSecret` | (preserved if exists) | Retained from existing settings during updates |

#### Certificate-Based Authentication

To enable certificate-based authentication, include a `certificate` field in the request body with the certificate ID. The system validates that the certificate exists before persisting the Protected Resource.

**Request Body with Certificate:**

#### Response

After creation, the resource is assigned a unique ID and `updatedAt` timestamp.

**Response Body:**

#### Adding Secrets

To add secrets to a Protected Resource, send a POST request to `/protected-resources/{id}/secrets` with a `name` field. The request requires the `PROTECTED_RESOURCE[CREATE]` permission.

**Request Body:**

**Response:**

The response includes the plaintext secret value. This value is returned only once and cannot be retrieved later.

{% hint style="warning" %}
Store the plaintext secret value immediately. It cannot be retrieved after the initial response.
{% endhint %}

#### Configuring Membership

To configure membership for a Protected Resource, send a POST request to `/protected-resources/{id}/members`. The request requires the `PROTECTED_RESOURCE_MEMBER[CREATE]` permission.

**Request Body:**

| Field | Required | Description |
|:------|:---------|:------------|
| `memberId` | Yes | User or group identifier |
| `memberType` | Yes | Member type: `USER` or `GROUP` |
| `role` | Yes | Role identifier |

### Searching Protected Resources

Search Protected Resources by sending a GET request to `/protected-resources?q={query}`.

**Query Parameter:**

| Parameter | Required | Description |
|:----------|:---------|:------------|
| `q` | No | Search query supporting wildcards (`*`) |

**Behavior:**

* If the `q` parameter is present, the system searches by `name` or `clientId`.
* If the `q` parameter is absent, the system returns all resources filtered by type.

**Response:**

**Search Examples:**

| Query | Behavior |
|:------|:---------|
| `"clientId123"` | Exact match: searches for resources where `name` or `clientId` equals `"clientId123"` |
| `"client*"` | Wildcard match: searches for resources where `name` or `clientId` starts with `"client"` |
