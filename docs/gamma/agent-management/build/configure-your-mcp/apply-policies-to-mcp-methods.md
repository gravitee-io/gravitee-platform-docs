---
hidden: false
noIndex: true
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
<!-- GAP: 129 · Documentable · Document the exact UI fields or flow selectors used to target MCP methods (e.g., path operators, headers, or method types) in Policy Studio. Needs: Demo session, Source code -->
6. Open the policy palette and drag your chosen policies onto the flow.
7. Click **Save** to persist your changes.

<!-- Source: PolicyStudioPage.tsx @ 2a91746280 -->
