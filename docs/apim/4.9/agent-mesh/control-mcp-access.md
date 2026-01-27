# Control MCP Access

## Overview

This guide explains how to control access to MCP (Model Context Protocol) server capabilities using the MCP ACL (Access Control List) policy in Gravitee APIM. The ACL policy allows you to define granular permissions for tools, resources, and prompts exposed by an MCP server.

## Prerequisites

Before you configure MCP access control, ensure you have:

* An MCP API configured in Gravitee APIM
* The MCP ACL policy available in your Gravitee installation

## Understand default behavior

When you add the MCP ACL policy to an API without specifying any rules, the system adopts a restrictive "Deny All" approach by default.

1. Add the MCP ACL policy to your MCP API.
2. Save the API configuration.
3. Deploy the API.

After deployment, all server functionalities will be inaccessible. An MCP client will be able to connect to the server via the Gateway, but the lists of tools, resources, and prompts will appear empty.

## Authorize tool listing only

To allow a client to see available tools without being able to execute them:

1. Navigate to your MCP API in the Gravitee Console.
2. Add an ACL rule in the MCP ACL policy configuration.
3. Select the **Tools** feature option.
4. Check the **tools/list** box.
5. Leave the **Name Pattern Type** field set to **ANY** (default value).
6. Save the policy configuration.
7. Deploy the API.

After deployment, an MCP client will be able to list available tools, but any attempt to call (execute) them will be rejected.

## Authorize a specific tool

To restrict access and execution to a single specific tool (for example, `get_weather`):

1. Navigate to your MCP API in the Gravitee Console.
2. Add or modify an ACL in the MCP ACL policy configuration.
3. In the **Tools** feature option:
    * Check both **tools/list** and **tools/call**.
    * In the **Name Pattern Type** field, select **Literal**.
    * In the **Name Pattern** field, enter the exact name of the tool (for example, `get_weather`).
4. Save the policy configuration.
5. Deploy the API.

After deployment, only the specified tool is visible to the MCP client and can be called. All other tools remain hidden and inaccessible.

## Add conditional access rules

Each ACL rule includes a **Trigger Condition** field. This field allows you to add conditional logic to determine if the rule should be applied or ignored. This is useful for applying context-based security policies.

The **Trigger Condition** field expects a Gravitee EL (Expression Language) expression. You can condition access to certain tools based on a specific property (claim) present in the user's token or a request attribute.

## Test your configuration locally

To validate your ACL configurations without impacting a production environment, you can use the official example MCP server named "Everything." This server exposes a large number of functionalities, making it ideal for testing filters.

### Install the test server

1. Install the "Everything" MCP server using npm:

    ```bash
    npx @modelcontextprotocol/server-everything streamableHttp
    ```

    The server will start in HTTP mode (streamable).

### Configure your API

1. Navigate to your Gravitee API configuration.
2. Configure the API endpoint to point to the local URL of the test server:

    ```
    http://localhost:3001/mcp
    ```

3. Save the API configuration.
4. Deploy the API.

### Validate your policy

Test your ACL policy using an MCP client. The "Everything" server exposes many tools by default, allowing you to verify that your policy correctly filters visible and callable tools according to your rules.

<!-- NEED CLARIFICATION: The source material mentions "resources" and "prompts" as MCP server capabilities that can be controlled via ACL, but does not provide configuration details for these features. Only tools are documented. -->

<!-- NEED CLARIFICATION: The source material references a "Gravitee-generated MCP tool server" but does not explain what this is or how it differs from proxying an existing MCP server. -->

<!-- ASSETS USED (copy/rename exactly):
- screenshot-01.png -> trial-runs/.gitbook/assets/apim-mcp-acl-step-01.png | alt: "New MCP server form showing domain, name, resource identifier, and description fields"
-->