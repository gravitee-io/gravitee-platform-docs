---
hidden: false
noIndex: false
description: The structure of a GAPL statement, covering its effect, its principal, action, and resource scope, its when and unless conditions, and its annotations.
---

# Policy statements

A policy holds one or more statements. Each statement ends with a semicolon and has the following parts, in this order:

1. Optional [annotations](#annotations), such as `@id("...")`.
2. An [effect](#effect), `permit` or `forbid`.
3. A [scope](#scope) between parentheses, which constrains the principal, the action, and the resource.
4. Optional [conditions](#conditions), `when { ... }` and `unless { ... }`.

```
@id("alice-reads-reports")
permit (
  principal == User::"alice",
  action == Action::"read",
  resource is Report
)
when { resource.status == "published" };
```

Spaces and line breaks between parts don't matter. A policy can hold any number of statements:

```
permit (principal in Group::"support", action == Action::"read", resource is Ticket);
forbid (principal, action == Action::"delete", resource is Ticket) unless { principal in Group::"admins" };
```

## Comments

A line comment starts with `//` and runs to the end of the line. A block comment starts with `/*` and ends with `*/`.

```
// Support staff read tickets
permit (principal in Group::"support", action == Action::"read", resource is Ticket); /* no condition */
```

## Effect

| Effect | Meaning when the statement matches |
|--------|------------------------------------|
| `permit` | The request is allowed, unless a `forbid` statement also matches |
| `forbid` | The request is denied, whatever `permit` statements match |

For how statements combine into one decision, see [How statements are evaluated](evaluation.md).

## Scope

The scope has three clauses, separated by commas, always in the order `principal`, `action`, `resource`. A clause written as the bare word, without a constraint, matches anything.

### Principal clause

| Constraint | Matches |
|-----------|---------|
| `principal` | Any principal |
| `principal == User::"alice"` | Exactly `User::"alice"` |
| `principal in Group::"support"` | `Group::"support"` itself, and every entity that has it as a parent, directly or through other parents |
| `principal is User` | Any principal of type `User` |
| `principal is User in Group::"support"` | Any `User` that is `Group::"support"` or one of its descendants |

### Resource clause

| Constraint | Matches |
|-----------|---------|
| `resource` | Any resource |
| `resource == Document::"q3-report"` | Exactly `Document::"q3-report"` |
| `resource in Folder::"public"` | `Folder::"public"` itself, and every entity that has it as a parent, directly or through other parents |
| `resource is Document` | Any resource of type `Document` |
| `resource is Document in Folder::"public"` | Any `Document` that is `Folder::"public"` or one of its descendants |

### Action clause

| Constraint | Matches |
|-----------|---------|
| `action` | Any action |
| `action == Action::"read"` | Exactly the `read` action |
| `action in Action::"edit"` | The `edit` action, and every action that a schema declares as a member of the `edit` group |
| `action in [Action::"read", Action::"list"]` | Any action in the list, or a member of any of them |

The `action` clause doesn't accept `is`. An empty list, `action in []`, matches no action.

Actions are entities of type `Action`. For action groups, see [Schema language](schema-language.md#action-groups).

## Namespaces

Entity types and actions can belong to a namespace declared in a schema document, such as `Sales`. For how to declare one, see [Schema language](schema-language.md#namespaces).

### Principals and resources

Write a namespaced principal or resource type in full in the policy:

```
permit (principal, action == Action::"refund", resource is Sales::Order);
permit (principal, action == Action::"refund", resource == Sales::Order::"o-1042");
```

The type that the request carries must match the type in the policy exactly. A request for an `Order` doesn't match `resource is Sales::Order`, and a request for a `Sales::Order` doesn't match `resource is Order`.

### Actions

An action declared inside a namespace has the type `<namespace>::Action`, such as `Sales::Action::"refund"`:

```
permit (principal, action == Sales::Action::"refund", resource is Sales::Order);
```

A request names its action, and the name becomes an action entity as follows:

| Action name in the request | Action entity |
|----------------------------|---------------|
| `read` | `Action::"read"` |
| `Sales::Action::"refund"` | `Sales::Action::"refund"` |
| `refund`, with the action property `type` set to `Sales::Action` | `Sales::Action::"refund"` |

A plain name never resolves to a namespaced action: `refund` alone matches `Action::"refund"`, not `Sales::Action::"refund"`.

## Conditions

A condition is a Boolean expression between braces:

* `when { ... }` requires the expression to be `true`.
* `unless { ... }` requires the expression to be `false`.

A statement can have several conditions, in any order. It matches only when its scope matches, every `when` is `true`, and every `unless` is `false`:

```
permit (principal, action == Action::"approve", resource is Invoice)
when { resource.amount <= 1000 }
when { principal.department == resource.department }
unless { resource.submittedBy == principal };
```

For what you can write inside a condition, see [Operators and expressions](operators-and-expressions.md).

## Annotations

An annotation is a name that starts with `@`, followed by an optional string value between parentheses. Annotations come before the effect, one or more per statement:

```
@id("contractors-no-delete")
@reason("Contractors can't delete records")
forbid (principal in Group::"contractors", action == Action::"delete", resource);
```

Two annotations change what a decision reports:

| Annotation | Effect |
|-----------|--------|
| `@id("<name>")` | Names the statement in decisions. The **Decisions** log and the `context.matchedPolicies[].policyName` of an AuthZEN response show this name. Two statements of one policy can't share an `@id` |
| `@reason("<text>")` | Replaces the reason of a decision this statement makes. The **Reason** column of the **Decisions** log and the `context.reason` of an AuthZEN response show this text |

A statement without `@id` is named after its policy and its position in it, counted from 0, such as `Orders access#2`. Without `@reason`, the reason names the statement, such as `Forbidden by policy 'contractors-no-delete'`, or `Permitted by policy '<name>'` for a `permit` statement. When several statements decide a request, their reasons are joined with `; `. The text of an `@reason` is cut to 512 characters, and its control characters, such as line breaks, are replaced with spaces.

An `@id` with a blank value, such as `@id("  ")`, counts as no `@id`. When one statement declares `@id` twice, the last one applies. The `@id` names of different policies aren't checked against each other, so two policies can report the same name.

Other annotations, such as `@owner("payments-team")`, are accepted and kept with the statement. They don't change decisions or what a decision reports.

{% hint style="info" %}
In MCP policies, the **ID** field under the policy name holds the `@id` of the first statement. The field is filled from the policy name until you edit it. When you save, the editor writes that field at the start of the GAPL, in place of an `@id` you typed there.
{% endhint %}

## Entity references

A statement refers to an entity by its type and its ID, joined by `::`. The ID is a string between double quotes:

```
User::"alice"
MCPTool::"search"
Sales::Order::"o-1042"
```

A type name can contain only letters, digits, and `_`, and can't start with a digit. For example, `User`, `MCPTool`, and `api_key` are valid type names, and `mcp-tool` and `2FA` aren't. The ID between the quotes can contain any characters.

Type names are case-sensitive: `User::"alice"` and `user::"alice"` are two different entities.
