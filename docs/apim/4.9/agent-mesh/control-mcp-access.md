# Control MCP Access

## Overview

This guide explains how to control access to MCP (Model Context Protocol) servers and tools in Gravitee Access Management. Access control allows you to define which consumers can discover and use specific MCP tools, ensuring secure and compliant agent-to-tool interactions.

MCP tool access control operates at two levels:
- **Server-level access**: Controls which consumers can connect to an MCP server
- **Tool-level access**: Controls which specific tools within an MCP server a consumer can invoke

## Prerequisites

Before you configure MCP access control, complete the following steps:

- Configure at least one MCP server in Access Management
- Define one or more applications or consumers that will access MCP tools
- Understand your organization's security and compliance requirements for AI tool usage

## Configure MCP server settings

1. Navigate to **Access Management** in the Gravitee Console.

    ![Access Management navigation](.gitbook/assets/apim-mcp-access-step-01.png)

2. Select **MCP Servers** from the left navigation menu.

3. Click on an existing MCP server or create a new one by clicking **New MCP server**.

    ![New MCP server form](.gitbook/assets/apim-mcp-access-step-02.png)

4. Complete the **MCP Server Settings** section:
   - **Domain**: Enter the security domain for the MCP server (for example, `/agentic`)
   - **Name**: Enter a descriptive name for the MCP server
   - **MCP Resource Identifier**: Enter the canonical resource identifier (for example, `https://banking.example.com`)
   - **Description**: Enter an optional description of the MCP server's purpose

5. Click **Save** to create or update the MCP server configuration.

## Define tool access control

Tool access control determines which consumers can use specific tools provided by an MCP server. This prevents unauthorized or unintended tool usage by AI agents.

1. Navigate to the **Tools Configuration** section of your MCP server.

2. Click **Add tool** to define a new tool or select an existing tool to modify its access settings.

3. Configure the tool's access control settings:
   - Define which applications or consumer groups can invoke this tool
   - Set usage quotas or rate limits specific to this tool
   - Specify any additional security constraints

4. Click **Save** to apply the tool access control configuration.

{% hint style="info" %}
Tool-level access control works in conjunction with server-level access. A consumer must have both server access and tool-specific permissions to successfully invoke a tool.
{% endhint %}

## Configure authorization

MCP servers in Gravitee support RFC 9728 for OAuth 2.0 authorization. This ensures that MCP clients can securely authenticate on behalf of end users.

1. Navigate to the **Authorization** section of your MCP server configuration.

2. Enable OAuth 2.0 authorization by toggling the **Enable Authorization** switch.

3. Configure the OAuth 2.0 settings:
   - **Authorization Endpoint**: The URL where users will be redirected to authenticate
   - **Token Endpoint**: The URL where access tokens will be obtained
   - **Scopes**: Define the OAuth scopes required for tool access

4. Click **Save** to apply the authorization configuration.

When an MCP client attempts to use a tool without a valid OAuth token, it will receive a 401 error response with information about where to redirect the user for authentication. After successful authentication, the client can pass the obtained token on subsequent calls.

## Verification

To verify that MCP access control is working correctly:

1. Attempt to connect to the MCP server using an authorized consumer application.
2. Verify that the consumer can discover only the tools for which it has been granted access.
3. Attempt to invoke a tool using an unauthorized consumer and confirm that access is denied.
4. Review the MCP analytics dashboard to monitor tool usage and access patterns.

## Next steps

After configuring MCP access control, consider the following additional steps:

- Set up monitoring and alerts for unauthorized access attempts
- Review and update tool access permissions regularly based on usage patterns
- Configure rate limiting and quotas to prevent excessive tool consumption
- Integrate with Gravitee Access Management for centralized agent identity management

<!-- ASSETS USED (copy/rename exactly):
- screenshot1.png -> .gitbook/assets/apim-mcp-access-step-01.png | alt: "Access Management navigation showing MCP Servers menu option"
- screenshot2.png -> .gitbook/assets/apim-mcp-access-step-02.png | alt: "New MCP server form with server settings fields"
-->