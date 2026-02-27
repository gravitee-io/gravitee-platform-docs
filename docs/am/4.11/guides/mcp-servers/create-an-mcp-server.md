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
* **Resource Identifier:** The URL of the MCP endpoint to protect. For example,  `https://mcp.example.com/api`.
  * Must be unique in the domain.
  * Must be a valid URL without fragment identifiers.
* **Description:** (Optional) Additional information about the MCP Server. For example, `Provides file management tools for AI agents`.

### Step 3: (Optional) Configure OAuth 2.0 settings <a href="#step-3-configure-oauth-20-settings-optional" id="step-3-configure-oauth-20-settings-optional"></a>

By default, Gravitee AM automatically generates OAuth 2.0 credentials. You can optionally provide the following custom values:

* **Client ID:** A custom OAuth 2.0 Client Identifier.
  * If not provided, a secure random identifier is generated.
  * Must be unique within the domain.
*   **Client Secret:** A custom OAuth 2.0 Client Secret.

    * If not provided, a secure random secret will be generated.

    <div data-gb-custom-block data-tag="hint" data-style="warning" class="hint hint-warning"><p>The Client Secret is shown only once during creation. Make sure to copy and store it securely. You cannot retrieve the raw secret later.</p></div>

### Step 4: (Optional) Add MCP Tools  <a href="#step-4-add-mcp-tools-optional" id="step-4-add-mcp-tools-optional"></a>

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

### Step 5: Create the MCP Server <a href="#step-5-create-the-mcp-server" id="step-5-create-the-mcp-server"></a>

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
