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

By default, Gravitee AM automatically generates OAuth 2.0 credentials and applies the following default settings:

| Property | Default Value | Description |
|----------|---------------|-------------|
| `grantTypes` | `["client_credentials"]` | Allowed OAuth grant types |
| `responseTypes` | `["code"]` | Allowed OAuth response types |
| `tokenEndpointAuthMethod` | `"client_secret_basic"` | Default authentication method for token endpoint |
| `clientId` | (copied from resource) | OAuth client identifier |
| `clientSecret` | (preserved or generated) | OAuth client secret |

You can optionally provide the following custom values:

* **Client ID:** A custom OAuth 2.0 Client Identifier.
  * If not provided, a secure random identifier is generated.
  * Must be unique within the domain.
*   **Client Secret:** A custom OAuth 2.0 Client Secret.

    * If not provided, a secure random secret will be generated.

    {% hint style="warning" %}
    The Client Secret is shown only once during creation. Make sure to copy and store it securely. You cannot retrieve the raw secret later.
    {% endhint %}

{% hint style="info" %}
These defaults ensure that MCP Servers are configured with standard OAuth 2.0 settings. You can override these values during resource creation or update them later.
{% endhint %}

### Step 4: (Optional) Configure certificate-based authentication <a href="#step-4-configure-certificate-based-authentication-optional" id="step-4-configure-certificate-based-authentication-optional"></a>

MCP Servers support certificate-based JWT verification for token introspection.

1. Upload a certificate to the domain via the certificate management API.
2. Update the MCP Server with the certificate ID in the `certificate` field.
3. During token introspection, if the audience matches the MCP Server's `clientId` and a certificate is configured, the system uses that certificate for JWT signature verification.
4. If no certificate is configured, the system assumes HMAC-signed tokens.

{% hint style="warning" %}
Certificates cannot be deleted while referenced by any MCP Server. Deletion attempts return HTTP 400 with error message "You can't delete a certificate with existing protected resources."
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
Scopes must be defined before using the MCP Tool. To define scopes, go to [**Settings > Scopes**](../settings/scopes/) and create a new scope.
{% endhint %}

### Step 6: Create the MCP Server <a href="#step-6-create-the-mcp-server" id="step-6-create-the-mcp-server"></a>

1. Review your configuration.
2. Click **Create**.
3. Copy the Client Secret from the dialog that appears.
4. Click **Close**.

The MCP Server is now created and deployed to the Gateway. The system generates a default secret and applies OAuth settings according to the defaults table. The secret expiration notification is registered based on domain-level `SecretExpirationSettings`.

## Create an MCP Server via the Management API <a href="#create-an-mcp-server-using-the-management-api" id="create-an-mcp-server-using-the-management-api"></a>

You can create an MCP Server programmatically using the Gravitee AM Management API (mAPI).

### Endpoint <a href="#endpoint" id="endpoint"></a>

```
POST /management/organizations/{organizationId}/environments/{environmentId}/domains/{domainId}/protected-resources
```

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
**Save the client secret immediately.** The `clientSecret` field in the response contains the raw secret. This is the only time you will see it. Store it securely, as you cannot retrieve it later. The plaintext secret appears only in the creation response. Subsequent retrievals return redacted secrets.
{% endhint %}

## Manage MCP Server secrets <a href="#manage-mcp-server-secrets" id="manage-mcp-server-secrets"></a>

Secret rotation follows a create-renew-delete cycle.

1. List existing secrets via GET `/secrets` to identify the target secret.
2. To rotate, POST to `/secrets/{secretId}/_renew`. This generates a new secret value and updates the expiration timestamp.
3. Delete obsolete secrets via DELETE `/secrets/{secretId}`. The system enforces that at least one secret remains.
4. If the deleted secret was the last reference to a specific OAuth settings object, those settings are also removed.
5. All secret operations emit events that update expiration notifications in the background.

## Manage MCP Server membership <a href="#manage-mcp-server-membership" id="manage-mcp-server-membership"></a>

Membership controls access to MCP Server management operations.

1. Add members via POST `/members` with `memberId`, `memberType` (USER or GROUP), and `role`.
2. List members via GET `/members` to view current assignments.
3. Remove members via DELETE `/members/{member}`.
4. Query flattened permissions via GET `/members/permissions` to see effective access rights.

All membership operations require `PROTECTED_RESOURCE_MEMBER` permissions at the resource, domain, environment, or organization level.

## Search MCP Servers <a href="#search-mcp-servers" id="search-mcp-servers"></a>

The search API supports wildcard queries across resource names and client IDs.

* **Endpoint:** GET `/protected-resources?q={query}`
* **Query Parameter:** `q` (optional) - Search query supporting wildcards (`*`)
* **Behavior:**
  * If `q` is present: searches by name or clientId (case-insensitive, wildcard support)
  * If `q` is absent: returns all resources filtered by type
* **Response:** `Page<ProtectedResourcePrimaryData>`
