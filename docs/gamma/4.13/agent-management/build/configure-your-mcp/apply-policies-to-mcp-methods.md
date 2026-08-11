---
hidden: false
noIndex: false
description: Apply policies to specific MCP methods such as resources/list, tools/call, or prompts/get. Follow the steps to create an MCP method flow.
---

# Apply policies to specific MCP methods

When you expose an MCP Proxy, you can apply policies at different levels of granularity. By default, policies attached to a **Common flow** are executed on every interaction with the MCP server, regardless of the method or tool. You can also target specific MCP protocol methods, such as `resources/list`, `tools/call`, or `prompts/get`, by creating an **MCP method flow**.

## Configure method-specific policies

To apply policies to a specific MCP method, complete the following steps:

1. In the Gamma console, navigate to **Agent Management**.
2. In the **Secure** section, select **MCP Proxies**, and then select your MCP proxy from the list.
3. In the proxy sidebar, under **Design**, select **Policy Studio**.
4. Under **MCP method flows**, select **Add MCP method flow**.
5. In the **Create a new MCP method flow** panel, complete the following fields:
    - **Flow name.** Enter a name for the flow.
    - **MCP methods.** Select one or more MCP methods to target, such as `tools/call`, `resources/list`, or `prompts/get`.
    - **Condition.** Enter an optional Expression Language condition that must evaluate to true for the flow to run.
6. Select **Create**.
7. In the **Request phase** or **Response phase**, select **Browse all...** or a suggested category button to open the **Add Policy** catalog. Choose a policy, and then add it to the phase.
8. Select **Save** to persist your changes.
