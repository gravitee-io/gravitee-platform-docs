---
hidden: false
noIndex: false
description: Apply policies to specific MCP methods such as resources/list, tools/call, or prompts/get with a flow selector. Follow the steps in the Policy Studio.
---

# Apply policies to specific MCP methods

When exposing an MCP Proxy, you can apply policies at different levels of granularity. By default, policies attached to the "Common flow" are executed on every interaction with the MCP server. However, you can also target specific MCP protocol methods (such as `resources/list`, `tools/call`, or `prompts/get`) using flow selectors.

## Configure method-specific policies

To apply policies to a specific MCP method:

1. In the Gamma console, navigate to **Agent Management**.
2. Select your MCP proxy from the proxy list.
3. In the sidebar, select **Policy Studio**.
4. Create a new flow or select an existing one.
5. In the flow configuration, define a selector for the target MCP method.
6. Open the policy palette and drag your chosen policies onto the flow.
7. Click **Save** to persist your changes.

