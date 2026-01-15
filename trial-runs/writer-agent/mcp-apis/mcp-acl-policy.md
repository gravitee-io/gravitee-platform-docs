---
description: Learn how to control access to MCP server features using the ACL policy.
---

# MCP ACL Policy

## Overview

This guide explains how to control access to Model Context Protocol (MCP) server functionalities using an Access Control List (ACL) policy in Gravitee. The MCP ACL policy restricts access to MCP features such as tools, resources, and prompts.

## Prerequisites

* A deployed MCP Proxy API in Gravitee APIM
* Access to the Policy Studio in your APIM Console

## Default behavior

By default, if you add the ACL policy to an MCP API without specifying any rules, the system adopts a restrictive **deny all** approach.

**Effect:**
* All server functionalities are inaccessible.
* An MCP client can connect to the server through the Gateway, but the lists of tools, resources, and prompts appear empty.

To configure the default behavior:

1. Open your MCP API in the APIM Console.
2. Navigate to **Policy Studio**.
3. Add the **ACL** policy to your API.
4. Save and deploy the API without adding any rules.

## Allow tool listing only

Use this configuration to let clients see available tools without the ability to execute them.

1. Open your MCP API in the APIM Console.
2. Navigate to **Policy Studio**.
3. Add the **ACL** policy or edit an existing ACL configuration.
4. Add a new rule.
5. Select the **Tools** feature option.
6. Check the **tools/list** box.
7. Leave **Name Pattern Type** set to **ANY** (default value).
8. Save and deploy the API.

<!-- NEED CLARIFICATION: Missing screenshot for ACL policy configuration showing tools/list checkbox -->

**Result:** MCP clients can list available tools, but any attempt to call (execute) a tool is rejected.

## Allow listing and calling a specific tool

Use this configuration to restrict access and execution to a single specific tool.

1. Open your MCP API in the APIM Console.
2. Navigate to **Policy Studio**.
3. Add the **ACL** policy or edit an existing ACL configuration.
4. Add or modify a rule.
5. In the **Tools** feature option, check both **tools/list** and **tools/call**.
6. In the **Name Pattern Type** field, select **Literal**.
7. In the **Name Pattern** field, enter the exact name of the tool. For example, `get_weather`.
8. Save and deploy the API.

<!-- NEED CLARIFICATION: Missing screenshot for ACL policy configuration showing literal name pattern -->

**Result:** Only the specified tool is visible to MCP clients and can be called. All other tools remain hidden and inaccessible.

## Advanced configuration

### Trigger conditions

Each ACL rule includes a **Trigger Condition** field that lets you add conditional logic to determine if the rule should be applied or ignored. This is useful for applying context-based security policies.

**Example use case:** Condition access to certain tools based on a specific claim in the user's token or a request attribute.

{% hint style="info" %}
The Trigger Condition field expects a Gravitee Expression Language (EL) expression.
{% endhint %}

## Local testing guide

To validate your ACL configurations without impacting a production environment, use the official MCP example server named "Everything." This server exposes many functionalities, making it ideal for testing filters.

### Prerequisites

The source code is available at the [MCP Servers Everything repository](https://github.com/modelcontextprotocol/servers/tree/main/src/everything).

### Start the example server

Run the following command to launch the server in HTTP mode:

```bash
npx @modelcontextprotocol/server-everything streamableHttp
```

The server starts on port 3001 by default.

### Configure the API endpoint

1. Open your MCP API in the APIM Console.
2. Navigate to the API endpoint configuration.
3. Set the endpoint URL to `http://localhost:3001/mcp`.
4. Save and redeploy the API.

### Validate the configuration

Connect an MCP client to your API and verify that your ACL policy correctly filters the visible and callable tools according to your rules.

## Next steps

* To learn how to expose MCP servers through the Gateway, see [Expose MCP Servers](expose-mcp-servers.md).
* To secure an unsecured MCP server using Gravitee Access Management, see [Secure an MCP Server with Gravitee AM](secure-mcp-server-with-am.md).
