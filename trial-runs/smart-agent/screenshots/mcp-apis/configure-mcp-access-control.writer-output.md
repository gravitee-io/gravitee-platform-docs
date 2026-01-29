# configure mcp access control.writer output

## Overview

This guide explains how to control access to Model Context Protocol (MCP) server functionality using an Access Control List (ACL) policy in Gravitee. The ACL policy restricts access to MCP features including tools, resources, and prompts.

## Prerequisites

Before you configure MCP access control, ensure the following:

* You have an MCP Proxy API deployed in Gravitee
* You have access to the Policy Studio in the APIM Console

## Default behavior

When you add the ACL policy without specifying any rules, the system adopts a restrictive "Deny All" approach by default.

Result: All server functionality is inaccessible. An MCP client can connect to the server through the Gateway, but the lists of tools, resources, and prompts appear empty.

## Allow tool listing only

{% stepper %}
{% step %}
### Step 1

Navigate to your MCP Proxy API in the APIM Console.
{% endstep %}

{% step %}
### Step 2

Select **Policy Studio** from the left menu.
{% endstep %}

{% step %}
### Step 3

Add the **ACL** policy to the appropriate flow.
{% endstep %}

{% step %}
### Step 4

Click **+ Add Rule** in the policy configuration.
{% endstep %}

{% step %}
### Step 5

Select the **Tools** feature option.
{% endstep %}

{% step %}
### Step 6

Check the **tools/list** box.
{% endstep %}

{% step %}
### Step 7

Leave the **Name Pattern Type** field set to **ANY**.
{% endstep %}

{% step %}
### Step 8

Click **Save**.
{% endstep %}

{% step %}
### Step 9

Click **Deploy** to apply the changes.
{% endstep %}
{% endstepper %}

Result: MCP clients can list available tools, but attempts to execute tools are rejected.

## Allow listing and execution of a specific tool

{% stepper %}
{% step %}
### Step

Navigate to your MCP Proxy API in the APIM Console.
{% endstep %}

{% step %}
### Step

Select **Policy Studio** from the left menu.
{% endstep %}

{% step %}
### Step

Add or modify the **ACL** policy in the appropriate flow.
{% endstep %}

{% step %}
### Step

Click **+ Add Rule** in the policy configuration.
{% endstep %}

{% step %}
### Step

Select the **Tools** feature option.
{% endstep %}

{% step %}
### Step

Check both **tools/list** and **tools/call** boxes.
{% endstep %}

{% step %}
### Step

Set the **Name Pattern Type** field to **Literal**.
{% endstep %}

{% step %}
### Step

Enter the exact tool name in the **Name Pattern** field. For example: `get_weather`.
{% endstep %}

{% step %}
### Step

Click **Save**.
{% endstep %}

{% step %}
### Step

Click **Deploy** to apply the changes.
{% endstep %}
{% endstepper %}

Result: Only the specified tool is visible and callable. All other tools remain hidden and inaccessible.

## Add execution conditions

Each ACL rule includes a **Trigger Condition** field that allows you to add conditional logic to determine if the rule applies.

Use execution conditions to apply context-based security policies. For example, you can condition access to certain tools based on a specific claim in the user's token or a request attribute.

{% hint style="info" %}
The **Trigger Condition** field expects a Gravitee Expression Language (EL) expression.
{% endhint %}

## Test with the example MCP server

To validate ACL configurations without impacting a production environment, use the official MCP example server. This server exposes many tools, making it ideal for testing filters.

{% stepper %}
{% step %}
### Step 1

Install and start the example server:

```bash
npx @modelcontextprotocol/server-everything streamableHttp
```
{% endstep %}

{% step %}
### Step 2

Navigate to your Gravitee MCP Proxy API configuration.
{% endstep %}

{% step %}
### Step 3

Update the backend endpoint to point to the local server:

```
http://localhost:3001/mcp
```
{% endstep %}

{% step %}
### Step 4

Save and redeploy the API.
{% endstep %}

{% step %}
### Step 5

Connect an MCP client and verify that the ACL policy correctly filters the visible and callable tools.
{% endstep %}
{% endstepper %}

## Next steps

* [Secure an MCP server with Access Management](/broken/pages/34e029d160ee033a8f9950ebde0f7edd19c12eec)
