# Create an MCP Server

## Overview

This guide describes how to create an MCP Server in Gravitee Access Management (AM).

Protected Resources in Gravitee Access Management support advanced secret management, certificate-based authentication, and token introspection workflows. These capabilities allow Protected Resources to participate in OAuth 2.0 token exchange flows (RFC 8693) and Model Context Protocol (MCP) server integrations. Full lifecycle management is available for client secrets, certificates, and membership permissions.

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

### Step 2: Configure basic settings

Provide the following required information:

* **Name:** A descriptive name for your MCP Server. For example, `AI File Management Service`.
* **Resource Identifier:** The URL of the MCP endpoint to protect. For example, `https://mcp.example.com/api`.
  * Must be unique in the domain.
  * Must be a valid URL without fragment identifiers.
* **Description:** (Optional) Additional information about the MCP Server. For example, `Provides file management tools for AI agents`.

### Step 3: (Optional) Configure OAuth 2.0 settings

By default, Gravitee AM automatically generates OAuth 2.0 credentials and applies the following defaults when settings are not explicitly provided:

| Field | Default Value | Applied When |
|:------|:--------------|:-------------|
| `grantTypes` | `["client_credentials"]` | Field is null or empty |
| `responseTypes` | `["code"]` | Field is null or empty |
| `tokenEndpointAuthMethod` | `"client_secret_basic"` | Field is null |
| `clientId` | Resource's `clientId` | Field is null |

You can optionally provide the following custom values:

* **Client ID:** A custom OAuth 2.0 Client Identifier.
  * If not provided, a secure random identifier is generated.
  * Must be unique within the domain.
* **Client Secret:** A custom OAuth 2.0 Client Secret.
  * If not provided, a secure random secret will be generated using cryptographically secure methods.

{% hint style="warning" %}
The Client Secret is shown only once during creation. Make sure to copy and store it securely. You cannot retrieve the raw secret later.
{% endhint %}

#### MCP Server Context

When a Protected Resource operates in MCP Server context, OAuth 2.0 configuration is restricted to grant types and authentication methods suitable for machine-to-machine communication. This ensures that MCP Servers use only secure, non-interactive flows.

**Allowed Grant Types**

The following grant types are available in MCP Server context:

| Grant Type | Label | Description |
|:-----------|:------|:------------|
| `client_credentials` | Client Credentials | Direct machine-to-machine authentication |
| `urn:ietf:params:oauth:grant-type:token-exchange` | Token Exchange | Exchange subject tokens for access tokens per RFC 8693 |

**Allowed Token Endpoint Authentication Methods**

The following authentication methods are available in MCP Server context:

| Method | Description |
|:-------|:------------|
| `client_secret_basic` | HTTP Basic authentication with client credentials |
| `client_secret_post` | Client credentials in POST body |
| `client_secret_jwt` | JWT signed with client secret |

**UI Behavior**

When configuring a Protected Resource in MCP Server context, the AM Console hides the following sections:

* Refresh Token configuration
* PKCE configuration

These sections are not applicable to machine-to-machine flows.

**Restrictions**

MCP Server context enforces the following restrictions:

* Grant types are limited to `client_credentials` and `urn:ietf:params:oauth:grant-type:token-exchange`.
* Token endpoint authentication methods are limited to `client_secret_basic`, `client_secret_post`, and `client_secret_jwt`.
* Other grant types (e.g., `authorization_code`, `password`) and authentication methods (e.g., `private_key_jwt`, `tls_client_auth`, `none`) are not available.

For more information about token exchange, see [RFC 8693](https://datatracker.ietf.org/doc/html/rfc8693).

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

## Protected Resource Secrets

Protected Resources can maintain multiple client secrets with independent lifecycles. Each secret includes:

* An identifier
* An expiration date
* Associated settings

The system enforces a minimum of one active secret per resource and generates cryptographically secure values using `SecureRandomString.generate()`.

### Secret Management Operations

You can perform the following operations on Protected Resource secrets:

* **Create**: Add a new secret to the resource
* **Renew**: Generate a new secret value while preserving existing settings
* **Delete**: Remove a secret from the resource

{% hint style="info" %}
Renewal operations automatically unregister old expiration notifications and register new ones.
{% endhint %}

## Database Schema

The database schema for protected resources varies depending on the database type.

{% tabs %}
{% tab title="JDBC" %}
The `protected_resources` table includes a `certificate` column with the following properties:

* **Type:** `nvarchar(64)`
* **Nullable:** Yes
{% endtab %}

{% tab title="MongoDB" %}
The `protected_resources` collection includes a `certificate` field with the following property:

* **Type:** `string`
{% endtab %}
{% endtabs %}


