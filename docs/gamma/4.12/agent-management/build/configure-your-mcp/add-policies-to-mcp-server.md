---
hidden: false
noIndex: false
---

# Add policies to your MCP server

Fine-grained authorization policies control which consumers can invoke which tools on your MCP Proxy. Policies are authored in Authorization Management and enforced at the wire level by the AI Gateway — evaluated at microsecond latency with no network hop.

## How policies work on MCP Proxies

The MCP Proxy integrates with Authorization Management's policy engine, which uses the Cedar policy language. When a consumer invokes a tool:

1. The AI Gateway extracts the consumer's identity from the request
2. The policy engine evaluates all applicable policies against the tool invocation
3. If the evaluation returns **permit**, the invocation proceeds to the upstream MCP server
4. If the evaluation returns **deny**, the invocation is rejected before reaching the upstream

Policies operate on typed MCP objects — tool name, arguments, and resource URI — not raw HTTP. This makes _"deny `delete_repository` on the GitHub MCP server"_ a one-line policy rather than a regex on a raw body.

## Create a policy

<!-- Source: mcp.ts (mcpServiceConfig), PolicyEditorSheet.tsx, PolicyStatementCard.tsx @ c07f5cdff9 -->

MCP policies are managed through the **MCP Policies** page in Authorization Management. You can also access this page from within an MCP Proxy's detail view.

1. From the Gamma console sidebar, select **Authorization**.
2. In the Authorization sidebar, select **MCPs** to open the **MCP Policies** page.
3. Select **+ Create policy**.
4. In the policy editor, enter a **Policy name** and optional **Description**.
5. If the policy targets a specific MCP server, the target is pre-filled from the Catalog.
6. Build the policy using either mode:

**Visual editor** (default):

   1. Each statement starts with an **effect** toggle — select **permit** or **forbid**.
   2. Pick **principals** — the users, groups, agents, or agent identities this policy applies to.
   3. Pick **actions** — choose from `invoke`, `list`, or `read`.
   4. Pick **resources** from the MCP resource groups:

      | Resource group | Entity type   | Description                         |
      | -------------- | ------------- | ----------------------------------- |
      | **MCP Server** | `MCPServer`   | The MCP server registered in the Catalog |
      | **Tools**      | `MCPTool`     | A tool exposed by the server        |
      | **Prompts**    | `MCPPrompt`   | A prompt template from the server   |
      | **Resources**  | `MCPResource` | A resource provided by the server   |

   5. Optionally insert a **condition snippet**:

      | Condition              | GAPL snippet                                       |
      | ---------------------- | -------------------------------------------------- |
      | **Business hours**     | `context.time.hour >= 9 && context.time.hour < 17` |
      | **Trusted device**     | `context.device.trusted == true`                   |
      | **Corporate IP range** | `context.source.ip.in_cidr("10.0.0.0/8")`          |

   6. Add additional statements as needed. Drag to reorder.

**Code editor** — Switch to the **Code** tab to write GAPL directly in a line-numbered editor.

7. Select **Create policy** to save as Draft, or **Create and Deploy policy** to save and deploy in one step.

## Deploy the policy

After creating a policy in Draft status:

1. Open the policy from the MCP Policies list.
2. Select **Deploy to PDP** to activate it. The AI Gateway syncs the new policy within 30 seconds — no restart required.
3. To suspend a deployed policy, select **Undeploy**. The gateway drops it within 30 seconds.

## SCIM integration for principals
<!-- GAP: 30 · Confirmable · Document the SCIM connector setup flow for use with MCP Proxy policies. Demo 2 (00:35:57) and May 22 demo (00:06:13, Stuart Clark) confirm SCIM synchronization is functional. Needs: Demo session, Engineering input, UI verification -->

You can sync users and groups from your enterprise identity provider into Authorization Management using SCIM (System for Cross-domain Identity Management) connectors. Synced users and groups become available as principals in your policies.

For SCIM connector configuration, users and groups synced through SCIM are managed by the connector — they cannot be deleted individually, and removing the connector removes the synced entities and their associated policies.

## Next steps

* [Configure your MCP proxy](README.md) — Set up mediation and credential management.
* [Create an agent identity](../create-an-agent-identity.md) — Assign identities to agents so policies can reference them as principals.
