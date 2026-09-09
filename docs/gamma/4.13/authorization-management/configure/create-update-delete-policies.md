---
hidden: false
noIndex: false
description: Reference for the Authorization Management policy editor, covering how to create, name, build, deploy, and delete a policy. Browse the full reference.
---

# Create, update, and delete policies

This is the comprehensive reference for the Authorization Management policy editor. Policies are written in Gravitee Authorization Policy Language (GAPL) and enforced by the gateway's Policy Decision Point (PDP).

## Policy editor overview

The policy editor opens as a slide-out panel from any policy management page: **MCPs**, **AI Models**, **APIs**, **A2A Agents**, or **Custom Policies**. It provides the following two editing modes:

| Mode | Description |
|------|-------------|
| **Visual** | Build policies using statement cards with chip pickers for principals, actions, and resources |
| **Code** | Edit GAPL directly in a Monaco editor with syntax highlighting |

Toggle between modes using the **Visual / Code** toggle in the editor header. If your GAPL uses features the visual editor cannot represent, the **Visual** toggle is disabled with the explanation: "This policy uses GAPL features that the visual editor cannot represent. Use the Code view to edit it directly."

## Create a policy

To create a policy, complete the following steps:

1. [Choose the policy category](#choose-the-policy-category)
2. [Open the editor](#open-the-editor)
3. [Name the policy](#name-the-policy)
4. [Build statements](#build-statements)
5. [Add conditions](#add-conditions)
6. [Set target gateways](#set-target-gateways)
7. [Save or deploy](#save-or-deploy)

### Choose the policy category

Navigate to the appropriate page under **Policy Management**. The following table lists each page, the policy type it creates, the target it applies to, and the resource groups available to it:

| Page | Policy type | Target | Resource groups |
|------|------------|--------|-----------------|
| **MCPs** | `MCP` | MCP Server | MCPServer, MCPTool, MCPPrompt, MCPResource |
| **AI Models** | `MODEL` | Model | LLMProvider, Model |
| **APIs** | `API` | API | API, Endpoint, DataField |
| **A2A Agents** | `AGENT` | Agent | Agent |
| **Custom Policies** | `CUSTOM` | None | User-defined |

### Open the editor

On the **MCPs**, **AI Models**, **APIs**, or **A2A Agents** page, click **Create policy**. A **Create policy for** dialog opens so you can pick the catalog entry the policy applies to, and then the editor opens.

On the **Custom Policies** page, click **Create Custom Policy**. The editor opens straight away, because a custom policy has no target.

### Name the policy

Enter a **Policy name**. The name is required, and the status badge shows **Draft**. The **Description** field is optional.

### Build statements

Each policy contains one or more statements. Each statement is built from the following parts:

| Part | Visual editor | GAPL syntax |
|------|--------------|-------------|
| **Effect** | Toggle between `permit` and `forbid` | `permit (…)` or `forbid (…)` |
| **Principal** | Chip picker from the **Principals** tab of the **Entities** page | `principal == User::"alice"` |
| **Action** | Chip picker from the **Actions** page | `action == Action::"invoke"` |
| **Resource** | Chip picker scoped by resource group | `resource == MCPTool::"search"` |
| **Agents** | Chip picker of imported agent identities | `context.agent == AgentIdentity::"planner"` |
| **Condition** | Condition block with snippet insertion | `when { context.time.hour >= 9 }` |

The **Agents** picker does not add a clause of its own. It writes a `context.agent` expression into the **Condition** field and joins it to any text already there with `&&`, so the agent restriction and your own condition are emitted together in a single `when { }` block.

#### Match modes

Each clause supports the following two match modes:

| Mode | Operator | Use case |
|------|----------|----------|
| **Exact** | `==` | Match this specific entity |
| **Includes** | `in` | Match this entity and its descendants |

For principal clauses, the default depends on the following entity types:

* **Groups and Roles** default to **Includes**. They are membership containers.
* **Users**, **Service Accounts**, and **Agent Identities** default to **Exact**. They are leaf principals.

#### Multiple entities in a clause

A GAPL principal or resource scope binds a single entity, so the **Principal** and **Resource** pickers each hold one entity and a new selection replaces the current one. The **Action** and **Agents** pickers accept several entities. When a clause holds multiple entities, GAPL joins them with `in [list]`:

```
permit (
  principal == User::"alice",
  action in [Action::"invoke", Action::"read"],
  resource == MCPTool::"search"
);
```

### Add conditions

On a statement card, expand the **Condition** section, which is marked **Optional**. The editor shows pre-built condition snippets specific to the policy category, each one a chip prefixed with a plus sign. You can also type custom conditions.

### Set target gateways

The **Target gateways** picker scopes the policy to specific PDP gateways. Select **\* (all gateways)** to cover every gateway, or pick individual targets from registered PDP gateways.

### Save or deploy

The following table lists each save and deploy action, the status it produces, and the toast message it shows:

| Action | Status after | Toast message |
|--------|-------------|---------------|
| **Create policy** | `DRAFT` | — |
| **Create and Deploy policy** | `DEPLOYED` | "Policy created and deployed. Gateway sync expected within 30s." |
| **Update policy** | Unchanged | — |
| **Deploy to PDP Runtime** | `DEPLOYED` | "Policy deployed. Gateway sync expected within 30s." |
| **Undeploy** | `DISABLED` | "Policy undeployed. Gateway sync will drop it within 30s." |

## Update a policy

1. On the policy list page, click a policy name to open the editor.
2. Modify statements, conditions, or metadata.
3. Click **Update policy** to save your changes.
4. If the policy is deployed, changes take effect after gateway sync, which takes about 30 seconds.

## Policy lifecycle states

The following table lists each policy status, what it means, and the transitions available from it:

| Status | Meaning | Transitions |
|--------|---------|-------------|
| **Draft** | Saved, not enforced | Deployed |
| **Deployed** | Active, enforced by the gateway | Disabled, by clicking **Undeploy** |
| **Disabled** | Suspended, not enforced | Deployed, by clicking **Deploy to PDP Runtime** |

{% hint style="info" %}
A `DEPLOYED` policy never returns to `DRAFT`. Undeploy writes `DISABLED` instead. To return to a draft-like state, undeploy the policy, and then edit it.
{% endhint %}

## Delete a policy

On the policy list page, delete a policy using the row-level action menu. When you delete a deployed policy, the gateway drops it from enforcement on the next sync cycle.

## Round-trip between the Visual and Code views

The following table describes what happens when you switch between the **Visual** and **Code** views:

| Scenario | Behavior |
|----------|----------|
| Visual to Code | The generated GAPL is populated in the Monaco editor |
| Code to Visual | The parser attempts to convert GAPL back to statement cards. If the GAPL uses unsupported features, the **Visual** toggle is disabled |
| Code edits while drafting | While drafting a new policy, the code editor mirrors the generated GAPL until you edit directly |

## GAPL template

A new policy starts with a single empty `permit` statement. The **Code** view renders it as the following GAPL, with the policy name as a comment:

```
// Policy: <policy name>
// Target: <target name>

permit (
  principal,
  action,
  resource
);
```

The `// Target:` comment is only present for the categories that have a target, which are **MCPs**, **AI Models**, **APIs**, and **A2A Agents**. A custom policy has no target, so its template opens with the `// Policy:` comment alone.

## Permissions

The following table lists the permission each policy action requires:

| Action | Required permission |
|--------|-------------------|
| Create policy | `ENVIRONMENT_AUTHZ_POLICIES[CREATE]` |
| Update policy | `ENVIRONMENT_AUTHZ_POLICIES[UPDATE]` |
| Deploy or undeploy | `ENVIRONMENT_AUTHZ_PDP[UPDATE]` |
| Delete policy | `ENVIRONMENT_AUTHZ_POLICIES[DELETE]` |

## Next steps

* [MCP policy examples](mcp-policy-examples.md). Real-world MCP policy patterns.
* [API policy examples](api-policy-examples.md). API access control patterns.
* [AI policy example](ai-policy-example.md). Token budget and cost ceiling policies.
* [Custom policies overview](custom-policies/custom-policies-overview.md). Policies for non-routed resources.
