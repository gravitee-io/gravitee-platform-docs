# Controlling Access to MCP Tools with ACL Policies

## Overview

This guide explains how to use the ACL policy in Gravitee Policy Studio to restrict access to MCP server features (tools, resources, prompts) with granular control.

## Prerequisites

Before you configure ACL policies for MCP tools, complete the following steps:

* Ensure you have an active MCP API deployed in Gravitee.
* Verify that you have access to the Policy Studio for the API.
* (Optional) Set up the Everything MCP server for local testing.

## Default behavior

When you add the ACL policy to an MCP API without specifying any rules, the system adopts a restrictive "Deny All" approach by default.

* All server functionalities will be inaccessible.
* An MCP client will be able to connect to the server via the Gateway, but the lists of tools, resources, and prompts will appear empty.

## Authorize tool listing only

To allow a client to see available tools without being able to execute them:

1. Log in to your APIM Console.
2. Select **APIs** from the left nav.
3. Select the MCP API you want to configure.
4. Select **Policies** from the inner left nav.
5. Click the **+** icon to add a policy to your flow.
6. Select the **ACL** policy from the list.
7. In the policy configuration:
    * Select the **Tools** feature option.
    * Check the **tools/list** box.
    * Leave the **Name Pattern Type** field on **ANY** (default value).
8. Click **Add policy**.
9. Click **Save** on the **Policies** page.
10. Redeploy the API.

{% hint style="info" %}
If you configure an MCP client, it will only be able to list available tools, but any attempt to call (execute) them will be rejected.
{% endhint %}

## Authorize listing and calling a specific tool

To restrict access and execution to a single specific tool (e.g., get_weather):

1. Log in to your APIM Console.
2. Select **APIs** from the left nav.
3. Select the MCP API you want to configure.
4. Select **Policies** from the inner left nav.
5. Click the **+** icon to add a policy to your flow (or edit an existing ACL policy).
6. In the policy configuration:
    * Select the **Tools** feature option.
    * Check both **tools/list** AND **tools/call**.
    * In the **Name Pattern Type** field, select **Literal**.
    * In the **Name Pattern** field, enter the exact name of the tool (for example: `get_weather`).
7. Click **Add policy** (or **Save** if editing).
8. Click **Save** on the **Policies** page.
9. Redeploy the API.

{% hint style="success" %}
Only this specific tool is visible to the MCP client and can be called. All other tools remain hidden and inaccessible.
{% endhint %}

## Advanced configuration: Execution conditions

Each ACL rule has a **Trigger Condition** field. This field allows you to add conditional logic to determine if the rule should be applied or ignored.

This is particularly useful for applying context-based security policies.

**Usage example:** You can condition access to certain tools based on a specific property (claim) present in the user's token or a request attribute.

{% hint style="info" %}
The field generally expects a Gravitee EL (Expression Language) expression.
{% endhint %}

## Local testing guide

To validate your ACL configurations without impacting a production environment, you can use the official example MCP server named "Everything." This server exposes a large number of functionalities, making it ideal for testing filters.

### Prerequisites and installation

The source code is available here: [GitHub - MCP Servers Everything](https://github.com/modelcontextprotocol/servers/tree/main/src/everything).

To launch the server in HTTP mode (streamable):

```bash
npx @modelcontextprotocol/server-everything streamableHttp
```

### API configuration

Once the local server is launched, return to your Gravitee API configuration.

1. Log in to your APIM Console.
2. Select **APIs** from the left nav.
3. Select the MCP API you want to configure.
4. Select **Configuration** from the inner left nav.
5. Select the **Endpoints** tab.
6. Configure the API Endpoint to point to the local URL of the created server: `http://localhost:3001/mcp`
7. Click **Save**.
8. Redeploy the API.

### Validation

You can now test your ACL policy. As the "Everything" server exposes many tools by default, you will be able to effectively verify if your policy correctly filters visible and callable tools according to your rules.