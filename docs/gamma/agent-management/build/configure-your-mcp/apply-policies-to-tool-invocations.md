---
hidden: false
noIndex: true
---

# Apply policies to individual tool invocations

In addition to targeting specific MCP methods, you can apply policies directly to individual tool invocations within an MCP Proxy. This enables fine-grained governance, such as applying rate limits or role-based access control to a specific, high-value tool (like `database_query` or `execute_script`) while leaving other tools unconstrained.

## Configure tool-specific policies

To apply policies to a specific tool invocation:

1. In the Gamma console, navigate to **Agent Management**.
2. Select your MCP proxy from the proxy list.
3. In the sidebar, select **Policy Studio**.
4. Create a new flow or select an existing one.
5. In the flow configuration, define a selector for the target tool.
<!-- GAP: 130 · Documentable · Document the exact UI fields or flow selectors used to target individual tool invocations (e.g., tool name parameters) in Policy Studio. Needs: Demo session, Source code -->
6. Open the policy palette and drag your chosen policies onto the flow.
7. Click **Save** to persist your changes.

<!-- Source: PolicyStudioPage.tsx @ 2a91746280 -->
