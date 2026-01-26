# Control MCP tool access

## Overview

This guide explains how to control access to MCP (Model Context Protocol) server functionalities using an Access Control List (ACL) policy in Gravitee. The ACL policy restricts which tools, resources, and prompts are available to MCP clients, enabling fine-grained security and governance over agent interactions.

## Prerequisites

Before configuring MCP tool access control, ensure you have:

* An MCP Proxy API deployed in Gravitee APIM
* Access to the Policy Studio for the API
* Understanding of which MCP features (tools, resources, prompts) you want to expose

## Default behavior (implicit deny)

When you add the ACL policy to an MCP Proxy API without specifying any rules, the system adopts a restrictive "deny all" approach by default.

1. Navigate to your MCP Proxy API in the APIM Console.
2. Open the **Policy Studio**.
3. Add the **ACL** policy to your API flow.
4. Save and deploy the API without configuring any rules.

    {% hint style="warning" %}
    With no ACL rules defined, all MCP server functionalities will be inaccessible. MCP clients can connect to the server via the Gateway, but the lists of tools, resources, and prompts will appear empty.
    {% endhint %}

## Authorize tool listing only

To allow MCP clients to discover available tools without being able to execute them:

1. Open the **Policy Studio** for your MCP Proxy API.
2. Add or edit the **ACL** policy.
3. Add a new rule with the following configuration:
    * **Feature**: Select **Tools**
    * **Permissions**: Check **tools/list**
    * **Name Pattern Type**: Leave as **ANY** (default value)
4. Save and deploy the API.

    MCP clients can now list available tools, but any attempt to call (execute) them will be rejected.

## Authorize listing and calling a specific tool

To restrict access and execution to a single specific tool (for example, `get_weather`):

1. Open the **Policy Studio** for your MCP Proxy API.
2. Add or edit the **ACL** policy.
3. Add a new rule with the following configuration:
    * **Feature**: Select **Tools**
    * **Permissions**: Check both **tools/list** and **tools/call**
    * **Name Pattern Type**: Select **Literal**
    * **Name Pattern**: Enter the exact tool name (for example, `get_weather`)
4. Save and deploy the API.

    Only the specified tool is visible to MCP clients and can be called. All other tools remain hidden and inaccessible.

## Advanced configuration: execution conditions

Each ACL rule includes a **Trigger Condition** field that allows you to add conditional logic to determine whether the rule should be applied or ignored. This is useful for applying context-based security policies.

You can condition access to certain tools based on:

* A specific claim present in the user's token
* A request attribute
* Any other context available through Gravitee Expression Language (EL)

The **Trigger Condition** field expects a Gravitee EL expression. For example:

```
{#request.headers['x-user-role'] == 'admin'}
```

This expression would only apply the ACL rule if the request includes a header `x-user-role` with the value `admin`.

## Test your configuration locally

To validate your ACL configurations without impacting a production environment, you can use the official MCP example server named "Everything." This server exposes a large number of functionalities, making it ideal for testing filters.

### Prerequisites

The source code is available at [GitHub - MCP Servers Everything](https://github.com/modelcontextprotocol/servers/tree/main/src/everything).

### Launch the server

1. Start the server in HTTP mode (streamable):

    ```bash
    npx @modelcontextprotocol/server-everything streamableHttp
    ```

    The server will start on port 3001 by default.

### Configure the API endpoint

1. Navigate to your MCP Proxy API in the APIM Console.
2. Configure the API endpoint to point to the local server URL:

    ```
    http://localhost:3001/mcp
    ```

3. Save and redeploy the API.

### Validate your ACL policy

You can now test your ACL policy. As the "Everything" server exposes many tools by default, you can effectively verify whether your policy correctly filters visible and callable tools according to your rules.

## Verification

To verify that your ACL policy is working correctly:

1. Configure an MCP client (such as VS Code with the Copilot extension) to connect to your MCP Proxy API.
2. Attempt to list available tools.
3. Attempt to call tools that should be accessible according to your ACL rules.
4. Attempt to call tools that should be blocked.

The client should only be able to list and call tools that match your configured ACL rules.

<!-- ASSETS USED (copy/rename exactly):
None
-->