# Mcp Access Control

## Overview

This guide explains how to control access to MCP (Model Context Protocol) server functionalities using Access Control List (ACL) policies in Gravitee. ACL policies restrict access to MCP features including tools, resources, and prompts, enabling fine-grained control over which consumers can discover and use specific MCP capabilities.

## Prerequisites

Before you configure MCP access control, ensure you have:

* A Gravitee APIM API configured as an MCP proxy
* Access to the Policy Studio in Gravitee APIM
* An understanding of the MCP features (tools, resources, prompts) exposed by your MCP server

## Understanding ACL behavior

### Default deny policy

When you add an ACL policy to an MCP API without specifying any rules, the system adopts a restrictive "Deny All" approach by default.

To apply a default deny policy:

1. Navigate to your MCP API in APIM.

2. Open the **Policy Studio**.

3. Add the **ACL** policy to your API flow.

4. Save and deploy the API without configuring any rules.

**Result:** All MCP server functionalities become inaccessible. MCP clients can connect to the server through the Gateway, but the lists of tools, resources, and prompts appear empty.

### ACL rule structure

Each ACL rule controls access to a specific MCP feature type and can include:

* **Feature type**: Tools, resources, or prompts
* **Operations**: Which operations are allowed (for example, list, call, read)
* **Name pattern type**: How to match feature names (ANY or Literal)
* **Name pattern**: The specific name or pattern to match
* **Trigger condition**: Optional conditional logic using Gravitee Expression Language (EL)

## Configure tool access control

### Allow tool listing only

To allow clients to see available tools without being able to execute them:

1. Open the **Policy Studio** for your MCP API.

2. Add or edit the **ACL** policy.

3. Add a new rule with the following configuration:
    * **Feature**: Select **Tools**
    * **Operations**: Check **tools/list**
    * **Name Pattern Type**: Leave as **ANY** (default)

4. Save and deploy the API.

**Result:** MCP clients can list available tools but cannot call or execute them. Any attempt to invoke a tool is rejected.

### Allow specific tool access

To restrict access and execution to a single specific tool:

1. Open the **Policy Studio** for your MCP API.

2. Add or edit the **ACL** policy.

3. Add a new rule with the following configuration:
    * **Feature**: Select **Tools**
    * **Operations**: Check both **tools/list** and **tools/call**
    * **Name Pattern Type**: Select **Literal**
    * **Name Pattern**: Enter the exact tool name (for example, `get_weather`)

4. Save and deploy the API.

**Result:** Only the specified tool is visible to MCP clients and can be called. All other tools remain hidden and inaccessible.

### Allow multiple tools with pattern matching

To allow access to multiple tools:

1. Open the **Policy Studio** for your MCP API.

2. Add or edit the **ACL** policy.

3. Add separate rules for each tool you want to expose, following the specific tool access pattern above.

{% hint style="info" %}
Currently, the ACL policy supports two name pattern types:
* **ANY**: Matches all features of the selected type
* **Literal**: Matches an exact feature name

Regular expression or wildcard pattern matching is not currently supported.
{% endhint %}

## Configure resource access control

Resources in MCP represent data sources or content that agents can read. To control resource access:

1. Open the **Policy Studio** for your MCP API.

2. Add or edit the **ACL** policy.

3. Add a new rule with the following configuration:
    * **Feature**: Select **Resources**
    * **Operations**: Check **resources/list** and/or **resources/read**
    * **Name Pattern Type**: Select **ANY** or **Literal**
    * **Name Pattern**: If using Literal, enter the exact resource name

4. Save and deploy the API.

**Result:** MCP clients can only access the resources specified in your ACL rules. The configuration pattern mirrors tool access control.

## Configure prompt access control

Prompts in MCP are predefined templates that agents can use. To control prompt access:

1. Open the **Policy Studio** for your MCP API.

2. Add or edit the **ACL** policy.

3. Add a new rule with the following configuration:
    * **Feature**: Select **Prompts**
    * **Operations**: Check **prompts/list** and/or **prompts/get**
    * **Name Pattern Type**: Select **ANY** or **Literal**
    * **Name Pattern**: If using Literal, enter the exact prompt name

4. Save and deploy the API.

**Result:** MCP clients can only access the prompts specified in your ACL rules. The configuration pattern mirrors tool and resource access control.

## Use trigger conditions

Each ACL rule includes a **Trigger Condition** field that accepts Gravitee Expression Language (EL) expressions. Trigger conditions enable context-based access control by evaluating request attributes, user claims, or other runtime data.

### Common trigger condition examples

**Role-based access:**

```
{#request.headers['x-user-role'] == 'admin'}
```

**Token claim validation:**

```
{#context.attributes['jwt.claims']['scope'] contains 'mcp:tools:write'}
```

**Time-based access:**

```
{#context.attributes['request.timestamp'] > 1640000000000}
```

**Environment-based access:**

```
{#context.attributes['environment'] == 'production'}
```

**Subscription-based access:**

```
{#context.attributes['subscription.plan'] == 'premium'}
```

{% hint style="info" %}
For complete documentation on Gravitee Expression Language syntax and available context attributes, see the [Gravitee EL documentation](https://documentation.gravitee.io/apim/guides/policy-design/expression-language).
{% endhint %}

## Test ACL configurations

### Set up local testing environment

To validate ACL configurations without impacting production, use the official MCP example server "Everything":

1. Install and start the example server:

    ```bash
    npx @modelcontextprotocol/server-everything streamableHttp
    ```

    The server starts on port 3001 by default.

2. Configure your MCP API in APIM:
    * Navigate to your API configuration
    * Set the **Endpoint** to `http://localhost:3001/mcp`
    * Save and deploy the API

3. Configure your MCP client (for example, VS Code, Claude Desktop) to connect to your Gravitee API endpoint.

### Verify tool access control

1. Configure an ACL rule that allows listing but not calling tools.

2. Connect your MCP client to the API.

3. Verify that:
    * Tools appear in the client's tool list
    * Attempting to call a tool results in an access denied error

4. Modify the ACL rule to allow calling a specific tool.

5. Verify that:
    * Only the specified tool can be called
    * Other tools remain inaccessible

### Verify resource access control

1. Configure an ACL rule that allows listing but not reading resources.

2. Connect your MCP client to the API.

3. Verify that:
    * Resources appear in the client's resource list
    * Attempting to read a resource results in an access denied error

4. Modify the ACL rule to allow reading a specific resource.

5. Verify that:
    * Only the specified resource can be read
    * Other resources remain inaccessible

### Verify prompt access control

1. Configure an ACL rule that allows listing but not getting prompts.

2. Connect your MCP client to the API.

3. Verify that:
    * Prompts appear in the client's prompt list
    * Attempting to get a prompt results in an access denied error

4. Modify the ACL rule to allow getting a specific prompt.

5. Verify that:
    * Only the specified prompt can be retrieved
    * Other prompts remain inaccessible

### Verify trigger conditions

1. Configure an ACL rule with a trigger condition based on a request header.

2. Send requests with and without the required header value.

3. Verify that:
    * Requests meeting the condition are allowed
    * Requests not meeting the condition are denied

{% hint style="info" %}
The "Everything" example server exposes numerous tools, resources, and prompts, making it ideal for testing ACL filters across all feature types.
{% endhint %}

## Verification

To verify your ACL configuration:

1. Navigate to the **Policy Studio** for your MCP API.

2. Review the configured ACL rules and confirm:
    * Feature types are correctly specified
    * Operations match your access requirements
    * Name patterns are accurate
    * Trigger conditions are valid EL expressions

3. Test the configuration using an MCP client:
    * Verify that only allowed features are visible
    * Verify that only allowed operations can be executed
    * Verify that trigger conditions behave as expected

4. Monitor API logs to confirm access control is enforced:
    * Navigate to **APIs** > **Your MCP API** > **Logs**
    * Review request logs for denied access attempts

## Next steps

After configuring MCP access control, you can:

* [Secure the MCP server with OAuth2](secure-mcp-server.md)
* [Monitor MCP server usage through APIM analytics](mcp-analytics.md)
* Configure plan-based access control to tie tool access to subscription plans
* Implement rate limiting policies for MCP operations
* Set up alerts for unauthorized access attempts