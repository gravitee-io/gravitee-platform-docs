---
hidden: false
noIndex: true
---

# Edit MCP Studio composition

After creating an MCP Studio, you can modify its tool composition and upstream authentication settings to tailor the tools exposed to your agents.

## Select and alias tools

<!-- Source: gravitee-gamma-module-aim/src/main/ui/app/features/secure/pages/mcp-studio-wizard/steps/ComposeStep.tsx @ 167439e1 -->
When building an MCP Studio, you can select which tools from your registered MCP servers to include in the composition. 

If multiple upstream servers provide tools with identical names, you must configure an **Alias** for the colliding tools to ensure they can be uniquely identified by the Agent Identity. The Studio interface automatically flags colliding tool IDs and prevents saving the composition until unique aliases are provided.

To edit your tool composition:
1. Open your MCP Studio in the console.
2. Navigate to the **Tools** section.
3. Select or deselect the tools you want to expose.
4. For any tools flagged with a collision, enter a unique alias.
5. Save the configuration.

## Configure upstream authentication

<!-- Source: gravitee-gamma-module-aim/src/main/ui/app/features/secure/pages/mcp-studio-wizard/steps/UpstreamAuthStep.tsx @ 167439e1 -->
If the tools you selected originate from an MCP server that requires upstream authentication (such as an OAuth2 provider or API Key), you must configure the credentials before the Studio can be published.

The Studio automatically detects which upstream servers require authentication based on the selected tools.

To configure upstream authentication:
1. Navigate to the **Authentication** section of your MCP Studio.
2. Review the list of required servers.
3. For each required server, select **Edit**.
4. Provide the necessary credentials (e.g., OAuth2 Client ID, Client Secret, Token URL, or API Key).
5. Save the credentials. The server status will update to **Configured**.

Once all required servers are configured, the MCP Studio composition is valid and can be deployed to the gateway.
