# Create an MCP Server

## Overview <a href="#prerequisites" id="prerequisites"></a>

This guide describes how to create an MCP Server in Gravitee Access Management (AM).

## Prerequisites <a href="#prerequisites" id="prerequisites"></a>

Before creating an MCP Server, ensure you have the following:

* Access to Gravitee AM Console with `PROTECTED_RESOURCE[CREATE]` permission.
* The URL(s) of the MCP endpoint(s) you want to protect.

## Create an MCP Server using the AM Console <a href="#create-an-mcp-server-using-am-console" id="create-an-mcp-server-using-am-console"></a>

Complete the following steps to create an MCP Server using the AM Console.

### Step 1: Navigate to MCP Servers <a href="#step-1-navigate-to-mcp-servers" id="step-1-navigate-to-mcp-servers"></a>

1. Log in to the AM Console
2. Select your security domain
3. Click **MCP Servers** in the left navigation menu
4. Click the **+** (plus) icon to create a new MCP Server

### Step 2: Configure basic settings <a href="#step-2-configure-basic-settings" id="step-2-configure-basic-settings"></a>

Provide the following required information:

* **Name:** A descriptive name for your MCP Server. For example, `AI File Management Service`.
* **Resource Identifier:** The URL of the MCP endpoint to protect. For example, `https://mcp.example.com/api`.
  * Must be unique in the domain.
  * Must be a valid URL without fragment identifiers.
* **Description:** (Optional) Additional information about the MCP Server. For example, `Provides file management tools for AI agents`.

### Step 3: (Optional) Configure OAuth 2.0 settings <a href="#step-3-configure-oauth-20-settings-optional" id="step-3-configure-oauth-20-settings-optional"></a>

By default, Gravitee AM automatically generates OAuth 2.0 credentials and applies default OAuth 2.0 settings. You can optionally provide the following custom values:

* **Client ID:** A custom OAuth 2.0 Client Identifier.
  * If not provided, a secure random identifier is generated.
  * Must be unique within the domain.
* **Client Secret:** A custom OAuth 2.0 Client Secret.
  * If not provided, a secure random secret will be generated.

{% hint style="warning" %}
The Client Secret is shown only once during creation. Make sure to copy and store it securely. You cannot retrieve the raw secret later.
{% endhint %}

If OAuth 2.0 settings are not explicitly configured, the system applies the following defaults:

| Property | Default Value | Description |
|:---------|:--------------|:------------|
| `grantTypes` | `["client_credentials"]` | Default grant types for Protected Resources |
| `responseTypes` | `["code"]` | Default response types |
| `tokenEndpointAuthMethod` | `client_secret_basic` | Default authentication method |
| `clientId` | (copied from resource) | Matches the Protected Resource's client ID |
| `clientSecret` | (preserved if exists) | Existing secret is retained during updates |

#### MCP Server context restrictions

Protected Resources with type `MCP_SERVER` have the following restrictions:

| Restriction Type | Allowed Values | Excluded Values |
|:-----------------|:---------------|:----------------|
| Grant Types | `client_credentials`, `urn:ietf:params:oauth:grant-type:token-exchange` | All other grant types |
| Token Endpoint Authentication Methods | `client_secret_basic`, `client_secret_post`, `client_secret_jwt` | `private_key_jwt`, `tls_client_auth`, `self_signed_tls_client_auth`, `none` |

When the context is set to `McpServer`, the AM Console applies the following filters:

| UI Section | Behavior |
|:-----------|:---------|
| Token endpoint authentication methods | Only allowed methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`) are displayed |
| Refresh Token configuration | Section is hidden |
| PKCE configuration | Section is hidden |

These restrictions ensure that MCP Server resources use only the authentication methods and grant types appropriate for their context.

### Step 4: (Optional) Configure certificate for JWT signature verification <a href="#step-4-configure-certificate-optional" id="step-4-configure-certificate-optional"></a>

You can optionally specify a certificate ID for JWT signature verification. If provided, the system validates that the certificate exists in the domain.

{% hint style="info" %}
[Certificate deletion is blocked](#manage-mcp-server-secrets) if referenced by any Protected Resource. Attempting to delete a certificate used by a Protected Resource returns HTTP 400 with error `CertificateWithProtectedResourceException` and message `"You can't delete a certificate with existing protected resources."`
{% endhint %}

### Step 5: (Optional) Add MCP Tools <a href="#step-5-add-mcp-tools-optional" id="step-5-add-mcp-tools-optional"></a>

You can add tools during or after creation. To add a tool, complete the following steps:

1. Click **Add Tool** in the Tools section.
2. Configure the tool:
   * **Name**: Unique identifier for the tool (must contain only letters, numbers, hyphens and underscores). For example, `list_files`.
   * **Description**: What the tool does. For example, `List files from the repository`.
   * **Scopes**: One or more OAuth 2.0 scopes required to use this tool. For example, `files:read`.
3. Click **Add** to save the tool.

You can add multiple tools with different scope requirements.

{% hint style="info" %}
Scopes must be defined before using the MCP Tool. To define scopes, go to **Settings > Scopes** and create a new scope.
{% endhint %}

### Step 6: Create the MCP Server <a href="#step-6-create-the-mcp-server" id="step-6-create-the-mcp-server"></a>

1. Review your configuration.
2. Click **Create**.
3. Copy the Client Secret from the dialog that appears.
4. Click **Close**.

The MCP Server is now created and deployed to the Gateway.

## Create an MCP Server via the Management API <a href="#create-an-mcp-server-using-the-management-api" id="create-an-mcp-server-using-the-management-api"></a>

You can create an MCP Server programmatically using the Gravitee AM Management API (mAPI).

### Endpoint <a href="#endpoint" id="endpoint"></a>

```
POST /management/organizations/{organizationId}/environments/{environmentId}/domains/{domainId}/protected-resources
```

### Request body <a href="#request-body" id="request-body"></a>

The request body must contain the following fields:

**Required fields:**

* `name`: Display name for the Protected Resource
* `clientId`: OAuth 2.0 Client Identifier
* `type`: Resource type (e.g., `MCP_SERVER`)

**Optional fields:**

* `resourceIdentifiers`: Array of resource identifier URLs
* `certificate`: Certificate ID for JWT signature verification
* `description`: Additional information about the MCP Server
* `features`: Array of MCP Tools (each with `type`, `key`, `description`, and `scopes`)

If `settings.oauth` is omitted, the system applies default OAuth 2.0 settings as described in the table above.

### Example Request <a href="#example-request" id="example-request"></a>

```bash
curl -X POST \
  'https://am-api.example.com/management/organizations/DEFAULT/environments/DEFAULT/domains/my-domain/protected-resources' \
  -H 'Authorization: Bearer {access_token}' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "AI File Management Service",
    "resourceIdentifiers": [
      "https://mcp.example.com/api"
    ],
    "description": "Provides file management tools for AI agents",
    "type": "MCP_SERVER",
    "features": [
      {
        "type": "MCP_TOOL",
        "key": "list_files",
        "description": "List files from the repository",
        "scopes": ["files:read"]
      },
      {
        "type": "MCP_TOOL",
        "key": "create_file",
        "description": "Create a new file",
        "scopes": ["files:write"]
      }
    ]
  }'
```

### Example Response <a href="#example-response" id="example-response"></a>

```json
{
  "id": "mcp-server-123",
  "name": "AI File Management Service",
  "clientId": "auto-generated-client-id",
  "clientSecret": "abc123xyz789-COPY-THIS-NOW",
  "domainId": "my-domain",
  "description": "Provides file management tools for AI agents",
  "type": "MCP_SERVER",
  "resourceIdentifiers": [
    "https://mcp.example.com/api"
  ],
  "createdAt": 1700000000000,
  "updatedAt": 1700000000000,
  "features": [
    {
      "key": "list_files",
      "type": "MCP_TOOL",
      "description": "List files from the repository",
      "createdAt": 1700000000000,
      "scopes": ["files:read"]
    },
    {
      "key": "create_file",
      "type": "MCP_TOOL",
      "description": "Create a new file",
      "createdAt": 1700000000000,
      "scopes": ["files:write"]
    }
  ]
}
```

{% hint style="warning" %}
**Save the client secret immediately.** The `clientSecret` field in the response contains the raw secret. This is the only time you will see it. Store it securely, as you cannot retrieve it later.
{% endhint %}

## Search for MCP Servers <a href="#search-for-mcp-servers" id="search-for-mcp-servers"></a>

You can search for MCP Servers using the Management API.

### Endpoint <a href="#search-endpoint" id="search-endpoint"></a>

```
GET /management/organizations/{organizationId}/environments/{environmentId}/domains/{domainId}/protected-resources?q={query}
```

### Query behavior <a href="#query-behavior" id="query-behavior"></a>

The search endpoint supports wildcard queries:

* If the `q` parameter is present, the system searches `name` and `clientId` fields (case-insensitive).
* Exact matches use equality (e.g., `clientId123` matches `clientId: "clientId123"`).
* Wildcard queries use prefix matching (e.g., `client*` matches `clientId: "client_anything"`).
* If `q` is absent, all resources filtered by type are returned.

### Response <a href="#search-response" id="search-response"></a>

The response is a paginated list of `ProtectedResourcePrimaryData` objects.

## Manage MCP Server secrets <a href="#manage-mcp-server-secrets" id="manage-mcp-server-secrets"></a>

Secrets are managed via the Management API at `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/secrets`.

### Create a secret <a href="#create-a-secret" id="create-a-secret"></a>

To create a secret, POST a JSON body with `{"name": "string"}`. The response includes the plaintext secret value, which is returned only once.

**Endpoint:** `POST /secrets`

**Permission Required:** `PROTECTED_RESOURCE[CREATE]`

**Request Body:**
```json
{
  "name": "string"
}
```

**Response:** `ClientSecret` (includes plaintext secret on creation)

### Renew a secret <a href="#renew-a-secret" id="renew-a-secret"></a>

To renew a secret, POST to `/secrets/{secretId}/_renew`. A new secret value is generated and returned. The secret ID and settings ID remain unchanged.

**Endpoint:** `POST /secrets/{secretId}/_renew`

**Permission Required:** `PROTECTED_RESOURCE[UPDATE]`

**Response:** `ClientSecret` (new secret value)

### Delete a secret <a href="#delete-a-secret" id="delete-a-secret"></a>

To delete a secret, send DELETE to `/secrets/{secretId}`. The secret is removed from `clientSecrets`, and the associated `secretSettings` entry is removed only if no other secret references it.

**Endpoint:** `DELETE /secrets/{secretId}`

**Permission Required:** `PROTECTED_RESOURCE[DELETE]`

**Response:** `204 No Content`

### List secrets <a href="#list-secrets" id="list-secrets"></a>

To list secrets, GET `/secrets` returns an array of safe (redacted) metadata. No plaintext values are included.

**Endpoint:** `GET /secrets`

**Permission Required:** `PROTECTED_RESOURCE[LIST]`

**Response:** `Array<ClientSecret>` (safe secrets, no plaintext)

### Secret lifecycle events <a href="#secret-lifecycle-events" id="secret-lifecycle-events"></a>

Protected Resource secret lifecycle events are published to the event bus:

| Event Type | Action | Description |
|:-----------|:-------|:------------|
| `PROTECTED_RESOURCE_SECRET` | `CREATE` | Secret created |
| `PROTECTED_RESOURCE_SECRET` | `RENEW` | Secret renewed (new value generated) |
| `PROTECTED_RESOURCE_SECRET` | `DELETE` | Secret deleted |

## Manage MCP Server membership <a href="#manage-mcp-server-membership" id="manage-mcp-server-membership"></a>

Membership controls who can manage a Protected Resource.

### List members <a href="#list-members" id="list-members"></a>

To list members, GET `/organizations/{orgId}/environments/{envId}/domains/{domain}/protected-resources/{resourceId}/members`.

**Permission Required:** `PROTECTED_RESOURCE_MEMBER[LIST]`

**Response:** `Array<Membership>`

### Add a member <a href="#add-a-member" id="add-a-member"></a>

To add a member, POST to `/members` with a JSON body containing `memberId`, `memberType` (`USER` or `GROUP`), and `role`.

**Permission Required:** `PROTECTED_RESOURCE_MEMBER[CREATE]`

**Request Body:**
```json
{
  "memberId": "string",
  "memberType": "USER|GROUP",
  "role": "string"
}
```

### Remove a member <a href="#remove-a-member" id="remove-a-member"></a>

To remove a member, DELETE `/members/{memberId}`.

**Permission Required:** `PROTECTED_RESOURCE_MEMBER[DELETE]`

**Response:** `204 No Content`

### Retrieve permissions <a href="#retrieve-permissions" id="retrieve-permissions"></a>

To retrieve flattened permissions for the current user, GET `/members/permissions`.

**Permission Required:** `PROTECTED_RESOURCE[READ]`

**Response:** Flattened permission map


## Token introspection configuration <a href="#token-introspection-configuration" id="token-introspection-configuration"></a>

When introspecting a token, the system validates the `aud` claim against Protected Resources.

**Single-audience tokens:**

For single-audience tokens, the system:

1. Checks if `aud` matches an Application `clientId`
2. If not found, checks if `aud` matches a Protected Resource `clientId`
3. If still not found, falls back to resource identifier validation

**Multi-audience tokens:**

For multi-audience tokens, the system always uses resource identifier validation.

If a Protected Resource is matched, the system retrieves the associated certificate ID (or empty string for HMAC) to verify the JWT signature. If no client or resource is found, the system throws `InvalidTokenException` with message `"Client or resource not found: {aud}"`.
