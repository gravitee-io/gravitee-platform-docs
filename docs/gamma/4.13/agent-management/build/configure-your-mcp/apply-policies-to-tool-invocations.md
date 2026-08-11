---
hidden: false
noIndex: false
description: Apply policies to a single tool invocation on an MCP Proxy with a tools/call flow and a condition on the tool name. Follow the steps to create it.
---

# Apply policies to individual tool invocations

In addition to targeting specific MCP methods, you can apply policies directly to individual tool invocations within an MCP Proxy. This enables fine-grained governance, such as applying rate limits or role-based access control to a specific, high-value tool—for example, `database_query` or `execute_script`—while leaving other tools unconstrained.

## Configure tool-specific policies

To apply policies to a specific tool invocation:

1. In the Gamma console, navigate to **Agent Management**.
2. Select your MCP proxy from the proxy list.
3. In the sidebar, select **Policy Studio**.
4. Under **MCP Method Flows**, select **Add MCP method flow**.
5. Enter a **Flow name**, and then select the **`tools/call`** MCP method. To scope the flow to a single tool, add a **Condition** that matches the tool name, for example `{#context.attributes['mcp_tool_name'] == 'database_query'}`. Select **Create**.
6. In the flow's **Request** or **Response** phase, select **Browse all**, or a category such as **+ Security**, to open the **Add Policy** catalog. Search for and select the policy you want to apply.
7. Select **Save** to persist your changes.

