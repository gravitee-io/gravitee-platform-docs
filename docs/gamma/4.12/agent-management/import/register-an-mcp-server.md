---
hidden: false
noIndex: false
---

# Register an MCP server
<!-- GAP-STRUCTURAL: Missing procedural content source -->

Registering an MCP server adds it to the Catalog as a first-class entity — along with its tools, resources, and prompts. Once registered, the server's capabilities become available for use in MCP Proxies, MCP Studios, and authorization policies.

This is the most common way to bring external MCP servers into Gamma's governance layer.

## Step 1: Start the import

1. From the Gamma console sidebar, select **Agent Management**.
2. Navigate to **Catalog** → **MCP Servers**.
3. Select **Add MCP server**.
4. **Select server**: Enter the Streamable HTTP endpoint URL of your MCP server (e.g., `https://mcp.example.com/mcp`).
5. Click **Verify URL** to verify the endpoint and discover its available capabilities.

## Step 2: Configure connection

If your server requires authentication to discover its capabilities, select an authentication method:

| Auth method            | Description                                                                                                                                           |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **OAuth**              | Authenticate with an OAuth client ID, token URL, and optional scopes. The secret is used once to fetch a discovery token and is never stored.         |
| **Static credential**  | Provide a Bearer token, Basic auth, or API key. Sent in the headers to read the server's capabilities and never persisted.                           |
| **No upstream sign-in**| Add the server without storing or injecting upstream credentials.                                                                                       |

After choosing an authentication method, click **Test connection** again to re-run discovery.

## Step 3: Review and import

Once the server URL is verified and discovery is successful, you will see a summary of the capabilities (e.g., the number of tools discovered).

Click **Import MCP Server**.

## Note on Credential Retention

The credentials provided during import are used strictly to discover and catalog the server's capabilities. **Secrets are never stored or persisted** by the catalog. When you later create an MCP Proxy in front of this server, you will need to configure upstream authentication separately to handle runtime invocations.

## After registration

The MCP server appears in the Catalog with its metadata:

| Field                 | Description                                                                               |
| --------------------- | ----------------------------------------------------------------------------------------- |
| **Entity ID**         | Unique identifier in the Catalog.                                                         |
| **Source**            | How it was registered (guided setup by URL).                                              |
| **Type**              | **Native** (an upstream server you registered) or **Composite** (authored in MCP Studio). |
| **Transport**         | Streamable HTTP.                                                                          |
| **Connection status** | Whether Gamma can currently reach the server.                                             |
| **Tool count**        | Number of tools discovered on this server.                                                |
| **Resource count**    | Number of resources discovered on this server.                                            |
| **Last sync**         | Timestamp of the most recent catalog refresh.                                             |

## Next steps

* **Create an MCP Proxy** — Put a governance layer in front of this server. See [Create an MCP proxy](../build/create-an-mcp-proxy.md).
* **Add policies** — Apply fine-grained authorization at the tool level. See [Add policies to your MCP server](../build/configure-your-mcp/add-policies-to-mcp-server.md).
* **Compose into a Studio** — Include this server's tools in a Composite MCP Server. See [Create an MCP Studio](../build/create-an-mcp-studio.md).
