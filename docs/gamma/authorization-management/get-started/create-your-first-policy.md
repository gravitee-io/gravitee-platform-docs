---
hidden: false
noIndex: false
---

# Create your first policy

This guide walks you through creating and deploying your first authorization policy using the visual policy editor. By the end, you will have a working `permit` rule that the gateway enforces within approximately 30 seconds.

## Prerequisites

* At least one principal created or synced (see [Create your first user](create-your-first-user.md))
* At least one resource imported or created (see [Import your first resource from the AI Catalog](import-your-first-resource-from-agent-catalog.md))
* The `ENVIRONMENT_AUTHZ_POLICY[CREATE]` permission

## Steps

### 1. Choose a policy category

From the Authorization Management sidebar, select a page under **Policy Management**:

| Page | What it governs |
|------|----------------|
| **MCPs** | MCP servers, tools, prompts, and resources |
| **AI Models** | AI providers and models |
| **APIs** | API proxies, endpoints, and data fields |
| **Custom Policies** | Anything not routed through MCP, API, Agent, or AI Model |

For this guide, select **MCPs**.

### 2. Create a new policy

Click **Create Policy for MCP**. The policy editor opens as a slide-out panel.

### 3. Name your policy

The cursor lands on the **Policy name** field. Enter a descriptive name (required). Below the name, you can add an optional **Description**.

### 4. Select a target (service policies only)

For MCP, AI Model, and API policies, you select a **target** — the specific catalog entry the policy applies to (for example, a particular MCP server). Custom policies have no target.

### 5. Build your first statement

The visual editor starts with one empty `permit` statement. Each statement has four clauses:

| Clause | What it specifies | GAPL keyword |
|--------|------------------|--------------|
| **Effect** | Whether to allow or deny | `permit` or `forbid` |
| **Principals** | Who the policy applies to | `principal` |
| **Actions** | What operations are governed | `action` |
| **Resources** | What entities are protected | `resource` |

Click the chip picker for **Principals** and select one or more principals. The picker shows all entities in the Principals tab by type. Repeat for **Actions** and **Resources**.

{% hint style="info" %}
Each clause supports two match modes:
- **Exact** (`==`) — matches the entity itself
- **Includes** (`in`) — matches the entity and its descendants (for example, all members of a group)

Groups and roles default to `includes`; individual users and service accounts default to `exact`.
{% endhint %}

### 6. Add conditions (optional)

Click **Add condition** on any statement card. The editor inserts a `when { }` block and shows pre-built condition snippets specific to the policy category. For MCP policies:

| Snippet | GAPL |
|---------|------|
| Business hours | `context.time.hour >= 9 && context.time.hour < 17` |
| Trusted device | `context.device.trusted == true` |
| Corporate IP range | `context.source.ip.in_cidr("10.0.0.0/8")` |

### 7. Add more statements

Click **Add statement** to add additional `permit` or `forbid` statements. Each policy can contain multiple statements; the engine evaluates all of them.

### 8. Switch to Code view (optional)

Toggle between **Visual** and **Code** view using the toggle in the header. The Code view shows the generated GAPL in a Monaco editor. You can edit the GAPL directly; if your edits use features the visual editor cannot represent, the visual toggle becomes disabled with an explanation.

A generated GAPL policy looks like:

```
// Policy: restrict-hr-tools
// Target: demo-hr-mcp

permit (
  principal == User::"alice",
  action == Action::"invoke",
  resource == MCPTool::"demo-hr-mcp.search"
)
when {
  context.time.hour >= 9 && context.time.hour < 17
};
```

### 9. Set target gateways (optional)

Below the header, the **Target gateways** picker lets you scope the policy to specific PDP gateways. Select individual gateways, `*` for all, or leave empty to deploy to all gateways.

### 10. Save or deploy

The footer provides three options:

| Action | Result |
|--------|--------|
| **Create policy** | Saves the policy as **Draft**. It is not enforced |
| **Create and Deploy policy** | Saves and immediately sets the status to **Deployed** |
| **Deploy to PDP Runtime** | Available after the first save. Sets the status to **Deployed** |

{% hint style="info" %}
A deployed policy is picked up by the gateway within approximately 30 seconds. The toast confirms: "Policy deployed. Gateway sync expected within 30s."
{% endhint %}

## Policy lifecycle

After creation, you can manage the policy through three states:

| Status | Description | Available actions |
|--------|-------------|-------------------|
| **Draft** | Saved but not enforced | Deploy, Edit, Delete |
| **Deployed** | Active and enforced by the gateway PDP | Undeploy, Edit |
| **Disabled** | Previously deployed, now suspended | Deploy, Edit, Delete |

To undeploy, click **Undeploy** in the editor header. The engine writes a `DISABLED` status — there is no `DEPLOYED → DRAFT` transition.

## Next steps

* [Create, update, and delete policies](../configure/create-update-delete-policies.md) — Full reference for the policy editor
* [MCP policy examples](../configure/mcp-policy-examples.md) — Real-world MCP policy patterns
* [AI policy example](../configure/ai-policy-example.md) — Token budget and cost ceiling examples
