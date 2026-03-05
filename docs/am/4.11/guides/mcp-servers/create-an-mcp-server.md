# Create an MCP Server

## Overview

This guide describes how to create an MCP Server in Gravitee Access Management (AM).

Protected Resources now support secret management, certificate-based authentication, and membership controls. Token introspection has been extended to validate Protected Resource audiences alongside traditional OAuth 2.0 clients. These enhancements enable Protected Resources to act as first-class OAuth 2.0 clients with full lifecycle management for credentials and access control.

## Prerequisites

Before creating an MCP Server, ensure you have the following:

* Access to Gravitee AM Console with `PROTECTED_RESOURCE[CREATE]` permission.
* The URL(s) of the MCP endpoint(s) you want to protect.

## Create an MCP Server using the AM Console

Complete the following steps to create an MCP Server using the AM Console.

### Step 1: Navigate to MCP Servers

1. Log in to the AM Console
2. Select your security domain
3. Click **MCP Servers** in the left navigation menu
4. Click the **+** (plus) icon to create a new MCP Server

### Step 2: Configure Basic Settings

Provide the following required information:

* **Name:** A descriptive name for your MCP Server. For example, `AI File Management Service`.
* **Resource Identifier:** The URL of the MCP endpoint to protect. For example, `https://mcp.example.com/api`.
  * Must be unique in the domain.
  * Must be a valid URL without fragment identifiers.
* **Description:** (Optional) Additional information about the MCP Server. For example, `Provides file management tools for AI agents`.

### Step 3: (Optional) Configure OAuth 2.0 settings

By default, Gravitee AM automatically generates OAuth 2.0 credentials. You can optionally provide the following custom values:

* **Client ID:** A custom OAuth 2.0 Client Identifier.
  * If not provided, a secure random identifier is generated.
  * Must be unique within the domain.
* **Client Secret:** A custom OAuth 2.0 Client Secret.
  * If not provided, a secure random secret will be generated.

{% hint style="warning" %}
The Client Secret is shown only once during creation. Make sure to copy and store it securely. You cannot retrieve the raw secret later.
{% endhint %}

#### Protected Resource Secrets

Protected Resources can maintain multiple client secrets with independent lifecycle management. Each secret is stored in the `clientSecrets` array and references a `secretSettings` entry via `settingsId`. Multiple secrets can share the same settings entry (algorithm, expiration policy). Secrets are generated server-side and returned in plaintext only on creation or renewal. List operations return safe metadata (no plaintext).

#### Certificate-Based Authentication

Protected Resources can reference a certificate by ID for JWT signature verification during token introspection. When a JWT's `aud` claim matches a Protected Resource's `clientId`, the introspection service retrieves the associated certificate for signature validation. Certificate deletion is blocked if any Protected Resource references it, returning HTTP 400 with error message `"You can't delete a certificate with existing protected resources."`.

#### MCP Server OAuth 2.0 Restrictions

Protected Resources with type `MCP_SERVER` have restricted OAuth 2.0 capabilities. Allowed grant types are `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange`. Allowed token endpoint authentication methods are `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`. Methods like `private_key_jwt`, `tls_client_auth`, and `none` are excluded. The refresh token and PKCE configuration sections are not available for MCP Server resources.

### Step 4: (Optional) Add MCP Tools

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

### Step 5: Create the MCP Server

1. Review your configuration.
2. Click **Create**.
3. Copy the Client Secret from the dialog that appears.
4. Click **Close**.

The MCP Server is now created and deployed to the Gateway.

## Create an MCP Server via the Management API

You can create an MCP Server programmatically using the Gravitee AM Management API (mAPI).

### Endpoint

```
POST /management/organizations/{organizationId}/environments/{environmentId}/domains/{domainId}/protected-resources
```

### Example Request

```bash
curl -X POST \
  'https://am-api.example.com/management/organizations/DEFAULT/environments/DEFAULT/domains/my-domain/protected-resources' \
  -H 'Authorization: Bearer {access_token}' \
  -H 'Content-Type: application/json' \
  -d @- <<'EOF'
```

```json
{
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
}
```

```bash
EOF
```

### Example Response

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

### Protected Resource Secrets

See [Protected Resource Secrets](#protected-resource-secrets) above for details.
### Certificate-Based Authentication

See [Certificate-Based Authentication](#certificate-based-authentication) above for details.
