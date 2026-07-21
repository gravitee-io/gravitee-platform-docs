---
hidden: false
noIndex: false
---

# Create, update, and delete policies

This is the comprehensive reference for the Authorization Management policy editor. Policies are written in GAPL (Gravitee Authorization Policy Language) and enforced by the gateway's Policy Decision Point.

## Policy editor overview

The policy editor opens as a slide-out panel from any policy management page (MCPs, AI Models, APIs, or Custom Policies). It provides two editing modes:

| Mode | Description |
|------|-------------|
| **Visual** | Build policies using statement cards with chip pickers for principals, actions, and resources |
| **Code** | Edit GAPL directly in a Monaco editor with syntax highlighting |

Toggle between modes using the **Visual / Code** toggle in the editor header. If your GAPL uses features the visual editor cannot represent, the Visual toggle is disabled with the explanation: "This policy uses GAPL features that the visual editor cannot represent. Use the Code view to edit it directly."

## Creating a policy

### 1. Choose the policy category

Navigate to the appropriate page under **Policy Management**:

| Page | Policy type | Has target? | Resource groups |
|------|------------|-------------|-----------------|
| **MCPs** | `MCP` | Yes (MCP Server) | MCPServer, MCPTool, MCPPrompt, MCPResource |
| **AI Models** | `MODEL` | Yes (Model) | LLMProvider, Model |
| **APIs** | `API` | Yes (API) | API, Endpoint, DataField |
| **Custom Policies** | `CUSTOM` | No | User-defined |

### 2. Open the editor

Click the create button (for example, **Create Policy for MCP**). For service policies, you first select a **target** — the specific catalog entry the policy applies to.

### 3. Name the policy

Enter a **Policy name** (required). The status badge shows **Draft**. Add an optional **Description** in the sub-header.

### 4. Build statements

Each policy contains one or more statements. A statement has:

| Part | Visual editor | GAPL syntax |
|------|--------------|-------------|
| **Effect** | Toggle between `permit` and `forbid` | `permit (…)` or `forbid (…)` |
| **Principals** | Chip picker from Entities (Principals tab) | `principal == User::"alice"` |
| **Actions** | Chip picker from the Actions page | `action == Action::"invoke"` |
| **Resources** | Chip picker scoped by resource group | `resource == MCPTool::"search"` |
| **Condition** | Condition block with snippet insertion | `when { context.time.hour >= 9 }` |

#### Match modes

Each clause supports two match modes:

| Mode | Operator | Use case |
|------|----------|----------|
| **Exact** | `==` | Match this specific entity |
| **Includes** | `in` | Match this entity and its descendants |

For principal clauses, the default depends on the entity type:
- **Groups and Roles** → `includes` (membership containers)
- **Users, Service Accounts, Agent Identities** → `exact` (leaf principals)

#### Multiple entities in a clause

When multiple entities are selected in a single clause, they are joined with `in [list]`:

```
permit (
  principal in [User::"alice", User::"bob"],
  action == Action::"invoke",
  resource in [MCPTool::"search", MCPTool::"create-issue"]
);
```

### 5. Add conditions

Click **Add condition** on a statement card. The editor shows pre-built condition snippets specific to the policy category. You can also type custom conditions.

### 6. Set target gateways

Below the header, the **Target gateways** picker scopes the policy to specific PDP gateways. Select `*` for all gateways, or pick individual targets from registered PDP gateways.

### 7. Save or deploy

| Action | Status after | Toast message |
|--------|-------------|---------------|
| **Create policy** | `DRAFT` | — |
| **Create and Deploy policy** | `DEPLOYED` | "Policy created and deployed. Gateway sync expected within 30s." |
| **Update policy** | Unchanged | — |
| **Deploy to PDP Runtime** | `DEPLOYED` | "Policy deployed. Gateway sync expected within 30s." |
| **Undeploy** | `DISABLED` | "Policy undeployed. Gateway sync will drop it within 30s." |

## Updating a policy

1. On the policy list page, click a policy name to open the editor
2. Modify statements, conditions, or metadata
3. Click **Update policy** to save changes
4. If the policy is deployed, changes take effect after gateway sync (~30 seconds)

## Policy lifecycle states

| Status | Meaning | Transitions |
|--------|---------|-------------|
| **Draft** | Saved, not enforced | → Deployed |
| **Deployed** | Active, enforced by the gateway | → Disabled (via Undeploy) |
| **Disabled** | Suspended, not enforced | → Deployed (via Deploy) |

{% hint style="info" %}
There is no `DEPLOYED → DRAFT` transition. Undeploying writes `DISABLED`. To return to a draft-like state, undeploy and then edit.
{% endhint %}

## Deleting a policy

Delete policies from the policy list page using the row-level action menu. Deleting a deployed policy removes it from gateway enforcement on the next sync cycle.

## Visual ↔ Code round-tripping

| Scenario | Behavior |
|----------|----------|
| Visual → Code | The generated GAPL is populated in the Monaco editor |
| Code → Visual | The parser attempts to convert GAPL back to statement cards. If the GAPL uses unsupported features, the Visual toggle is disabled |
| Code edits while drafting | While drafting a new policy, the code editor mirrors the generated GAPL until you edit directly |

## GAPL template

New policies start with the default template:

```
permit (principal, action, resource);
```

## Permissions

| Action | Required permission |
|--------|-------------------|
| Create / Update policy | `ENVIRONMENT_AUTHZ_POLICY[CREATE]` or `[UPDATE]` |
| Deploy / Undeploy | `ENVIRONMENT_AUTHZ_PDP[UPDATE]` |
| Delete policy | `ENVIRONMENT_AUTHZ_POLICY[DELETE]` |

## Next steps

* [MCP policy examples](mcp-policy-examples.md) — Real-world MCP policy patterns
* [API policy examples](api-policy-examples.md) — API access control patterns
* [AI policy example](ai-policy-example.md) — Token budget and cost ceiling policies
* [Custom policies overview](custom-policies/custom-policies-overview.md) — Policies for non-routed resources
