# controlling mcp server access

## Overview

This guide explains how to control access to MCP (Model Context Protocol) server functionalities using an Access Control List (ACL) policy in Gravitee. The ACL policy restricts access to MCP features such as tools, resources, and prompts.

## Prerequisites

Before you configure MCP access control, complete the following steps:

* Create and deploy an MCP proxy API in Gravitee APIM
* Have access to the Policy Studio in the APIM Console

## Understand default ACL behavior

When you add the ACL policy without specifying any rules, the system adopts a restrictive "Deny All" approach by default. This means:

* All server functionalities are inaccessible
* MCP clients can connect to the server via the Gateway
* Lists of tools, resources, and prompts appear empty to the client

## Add an ACL policy

{% stepper %}
{% step %}
### Add the ACL policy to your API

* Navigate to your MCP proxy API in the APIM Console.
* Open the **Policy Studio**.
* Add the **ACL** policy to your API flow.
* Configure the policy rules as described in the following sections.
* Click **Save**.
* Click **Deploy** to apply the changes.
{% endstep %}
{% endstepper %}

## Authorize tool listing only

To allow a client to view available tools without executing them:

{% stepper %}
{% step %}
* Add a rule in the ACL policy configuration.
* Select the **Tools** feature option.
* Check the **tools/list** box.
* Leave the **Name Pattern Type** field set to **ANY**.
* Save and deploy the API.

After deployment, MCP clients can list available tools, but any attempt to execute a tool is rejected.
{% endstep %}
{% endstepper %}

## Authorize listing and calling a specific tool

To restrict access to a single specific tool:

{% stepper %}
{% step %}
* Add or modify a rule in the ACL policy configuration.
*   In the **Tools** feature option:

    * Check **tools/list** and **tools/call**
    * Set **Name Pattern Type** to **Literal**
    * Enter the exact tool name in the **Name Pattern** field

    For example, to allow only the `get_weather` tool:

    ```
    get_weather
    ```
* Save and deploy the API.

After deployment, only the specified tool is visible to MCP clients and can be executed. All other tools remain hidden and inaccessible.
{% endstep %}
{% endstepper %}

## Configure execution conditions

Each ACL rule includes a **Trigger Condition** field that allows you to add conditional logic. Use this field to apply context-based security policies.

{% hint style="info" %}
The Trigger Condition field accepts Gravitee Expression Language (EL) expressions. You can condition access to tools based on properties in the user's token or request attributes.
{% endhint %}

For example, you can restrict tool access based on a specific claim in the user's JWT token.

## Verification

{% stepper %}
{% step %}
* Configure an MCP client to connect to your Gravitee Gateway endpoint.
* Verify that only the authorized tools appear in the tool list.
* Attempt to call an unauthorized tool and confirm the request is rejected.
* Call an authorized tool and confirm the request succeeds.
{% endstep %}
{% endstepper %}

## Test with the MCP example server

The official MCP "Everything" example server exposes many functionalities, making it ideal for testing ACL filters.

{% stepper %}
{% step %}
1. Start the example server:

```bash
npx @modelcontextprotocol/server-everything streamableHttp
```

2. Configure your MCP proxy API endpoint to use:

```
http://localhost:3001/mcp
```

3. Save and redeploy the API.
4. Apply different ACL rules and verify that the tool filtering works as expected.
{% endstep %}
{% endstepper %}

## Next steps

* [Securing an MCP Server with Gravitee](/broken/pages/db79ab554282bba17c1e94ac6ca59ae7e37e3e39) - Add OAuth2 authentication using Gravitee Access Management
