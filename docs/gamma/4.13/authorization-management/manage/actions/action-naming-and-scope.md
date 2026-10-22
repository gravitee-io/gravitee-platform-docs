---
hidden: false
noIndex: false
description: How action Entity IDs are structured and how the policy engine resolves them against policy types and resource scopes. Browse the naming reference.
---

# Action naming and scope

Understand how action Entity IDs are structured and how the policy engine resolves them against policy types and resource scopes.

## Entity ID format

An action's Entity ID is the action name exactly as a request carries it, with no prefix. A policy refers to it as `Action::"<Entity ID>"`. For example:

* An Authorization PEP policy whose action expression reads the HTTP method sends `GET` or `POST`, so the policy uses `Action::"GET"`.
* An MCP Studio with fine-grained authorization sends the tool as `<server>.<tool>`, so the policy uses `Action::"weather.get_forecast"`.

An Entity ID holds at most 255 characters, isn't `.` or `..`, and holds no whitespace, control or formatting character, double quote, backslash, `/`, `%`, `;`, `?`, or `#`.

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
- The `Action::"<Entity ID>"` reference

The visual editor supports two match modes for action clauses:

| Mode | GAPL syntax | Meaning |
|------|------------|---------|
| **Exact** (`==`) | `action == Action::"invoke"` | Match this specific action |
| **Set** (`in`) | `action in [Action::"read", Action::"write"]` | Match any action in the list |

## Naming conventions

| Pattern | Example | When to use |
|---------|---------|-------------|
| Simple verb | `invoke`, `read`, `write` | General-purpose actions |
| Domain-qualified verb | `model-query` | Actions specific to a service type |
| CRUD pattern | `create`, `read`, `update`, `delete` | REST-style API actions |

{% hint style="info" %}
Action names are case-sensitive in GAPL, and the Entity ID is used as it is. `Action::"GET"` doesn't match a request that carries `get`.
{% endhint %}

## Next steps

* [Schema documents](../schemas/schema-generation.md). See how actions relate to the schema's `appliesTo` declarations
* [Create, update, and delete policies](../../configure/create-update-delete-policies.md). Use actions in policy statements
