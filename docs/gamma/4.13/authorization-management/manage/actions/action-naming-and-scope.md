---
hidden: false
noIndex: false
---

# Action naming and scope

Understand how action Entity IDs are structured and how the policy engine resolves them against policy types and resource scopes.

## Entity ID format

Every action Entity ID uses the `action.` prefix followed by a slug:

```
action.<slug>
```

For example: `action.invoke`, `action.read`, `action.tools-call`.

The slug must match `[a-z0-9_-]+` — lowercase letters, digits, underscores, and dashes. No dots, no spaces.

## Built-in action constants

The backend defines standard action identifiers used by Gamma's routing layer:

| Constant | Entity ID | Used by |
|----------|-----------|---------|
| `TOOLS_CALL_METHOD` | `action.tools-call` | MCP tool invocations |

Additional actions can be defined for any operation your policies need to govern.

## Action scope: GLOBAL vs RESOURCE

Policies in Authorization Management are classified into two kinds (from `AuthzPolicyKind`):

| Kind | Scope | Example |
|------|-------|---------|
| **GLOBAL** | Applies across all entities of a type | A custom policy with no target |
| **RESOURCE** | Applies to a specific catalog entry | An MCP policy targeting a specific MCP server |

Actions themselves are not scoped — they are universal verbs. The scoping happens at the policy level through the **target** field, which binds a policy to a specific catalog entry.

## Actions in the policy editor

When building a policy in the visual editor, the **Actions** clause uses chip pickers populated from the Actions page. Each action chip shows:

- The action's display name
- The canonical `Action::"<slug>"` reference

The visual editor supports two match modes for action clauses:

| Mode | GAPL syntax | Meaning |
|------|------------|---------|
| **Exact** (`==`) | `action == Action::"invoke"` | Match this specific action |
| **Set** (`in`) | `action in [Action::"read", Action::"write"]` | Match any action in the list |

## Naming conventions

| Pattern | Example | When to use |
|---------|---------|-------------|
| Simple verb | `invoke`, `read`, `write` | General-purpose actions |
| Domain-qualified verb | `tools-call`, `model-query` | Actions specific to a service type |
| CRUD pattern | `create`, `read`, `update`, `delete` | REST-style API actions |

{% hint style="info" %}
Action names are case-sensitive in GAPL. The Entity ID is always lowercase, and the canonical reference uses `Action::"<slug>"` with the slug from the Entity ID.
{% endhint %}

## Next steps

* [Schema generation](../schemas/schema-generation.md) — See how actions relate to the schema's `appliesTo` declarations
* [Create, update, and delete policies](../../configure/create-update-delete-policies.md) — Use actions in policy statements
