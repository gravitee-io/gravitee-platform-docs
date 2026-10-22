---
hidden: false
noIndex: false
description: Every GAPL operator, method, and expression form, with the types each one accepts and the order in which they apply.
---

# Operators and expressions

Conditions are expressions that evaluate to `true` or `false`. An expression combines values with the operators on this page. An operator applied to a type it doesn't accept is an error, and the statement is skipped. For what skipping means, see [How statements are evaluated](evaluation.md).

## Variables

| Variable | Value |
|----------|-------|
| `principal` | The entity that makes the request |
| `action` | The action requested, an entity of type `Action` |
| `resource` | The entity the request is about |
| `context` | A record of request-time data. See [The context record](context.md) |

Any other name on its own, such as `department`, is refused when you save.

## Precedence

Operators apply in the following order, from first to last. Use parentheses to change the order:

| Order | Operators |
|-------|-----------|
| 1 | `.attribute`, `["attribute"]`, method calls such as `.contains(...)` |
| 2 | `!`, unary `-` |
| 3 | `*` |
| 4 | `+`, `-` |
| 5 | `==`, `!=`, `<`, `<=`, `>`, `>=`, `in`, `has`, `like`, `is` |
| 6 | `&&` |
| 7 | `\|\|` |
| 8 | `if ... then ... else ...` |

Operators of order 5 don't chain: `a < b < c` is a syntax error. Write `a < b && b < c` instead.

## Equality

`==` and `!=` accept values of any type. Values of different types are never equal, and comparing them isn't an error: `1 == "1"` is `false`.

| Type | Two values are equal when |
|------|---------------------------|
| `Bool`, `Long`, `String` | They're the same value. Strings compare case-sensitively |
| Entity | They have the same type and the same ID |
| `Set` | They hold the same values, in any order |
| Record | They have the same fields with equal values |
| `ip` | Same address and same prefix length |
| `decimal` | Same number: `decimal("1.50") == decimal("1.5")` is `true` |
| `datetime` | Same instant: `datetime("2026-01-01T10:00:00+02:00") == datetime("2026-01-01T08:00:00Z")` is `true` |
| `duration` | Same length |

## Comparison

`<`, `<=`, `>`, and `>=` compare two `Long` values, two `datetime` values, or two `duration` values. Any other pair is an error, including two strings and two decimals. To compare decimals, use the [decimal methods](extension-functions.md#decimal).

```text
resource.level >= 3
datetime(context.requestedAt) < datetime("2027-01-01")
duration(resource.retention) <= duration("30d")
```

## Arithmetic

`+`, `-`, and `*` take two `Long` values and give a `Long`. Unary `-` negates a `Long`. A result outside the `Long` range is an error. GAPL has no division.

```text
principal.failedLogins + 1 < 5
```

## Logical operators

`&&`, `||`, and `!` take `Bool` values. A value of another type is an error: `context.count && true` fails when `count` is a number.

`&&` and `||` stop as soon as the left side decides the result. The right side of `false && ...` and of `true || ...` isn't evaluated, so it can't cause an error. This is how you read an attribute only when it's present:

```text
context has mfa && context.mfa
```

## in

`a in b` is `true` when the entity `a` is the entity `b`, or a descendant of it through parents. `b` can also be a set of entities, and then `a in b` is `true` when it's `true` for any of them:

```text
principal in Group::"finance"
principal in resource.editors
resource in [Folder::"shared", Folder::"public"]
```

`a` must be an entity, and `b` an entity or a set of entities. When `a` doesn't exist on the gateway, it has no parents, so `a in b` is `true` only when `a` and `b` are the same entity.

To test whether a set holds a value, use [`contains`](#set-methods), not `in`.

## has

`e has name` is `true` when the record or entity `e` has the field or attribute `name`. For a name that isn't an identifier or is a GAPL keyword, write it as a string:

```text
principal has department
context has "x-tenant"
```

On an entity that doesn't exist on the gateway, `has` is `false`. Reading a field or an attribute that isn't there is an error, so guard optional data with `has` and `&&`.

## like

`s like "pattern"` matches the whole string `s` against a pattern, where `*` stands for any sequence of characters, including none. Write `\*` for a literal asterisk:

```text
context.path like "/api/*/orders"
resource.name like "draft-*"
context.label like "a\*b"
```

The pattern must be a string literal. `s` must be a `String`. The match is case-sensitive.

## is

`e is Type` is `true` when the entity `e` has exactly that type. Namespaced types are written in full. `e is Type in f` adds the condition `e in f`:

```text
resource is Invoice
resource is Sales::Order
principal is User in Group::"finance"
```

## Attribute access

`e.name` reads a field of a record or an attribute of an entity. `e["name"]` does the same for any name, such as `context["x-tenant"]`. Use it for names that are GAPL keywords too: `principal`, `action`, `resource`, `context`, `in`, `is`, `has`, `like`, `if`, `then`, `else`, `true`, `false`, `permit`, `forbid`, `when`, and `unless`. For example, `context.action` is a syntax error, and `context["action"]` works. Accesses chain: `resource.owner.department` reads the `department` of the entity in the `owner` attribute.

Reading a field or an attribute that isn't there, or an attribute of an entity that doesn't exist on the gateway, is an error.

## Set methods

| Method | Result |
|--------|--------|
| `s.contains(v)` | `true` when the set `s` holds the value `v` |
| `s.containsAll(t)` | `true` when `s` holds every value of the set `t` |
| `s.containsAny(t)` | `true` when `s` holds at least one value of the set `t` |
| `s.isEmpty()` | `true` when `s` holds no value |

Both `s` and `t` must be sets. Values are compared with the rules of [equality](#equality).

```text
principal.roles.contains("auditor")
principal.roles.containsAny(["admin", "owner"])
!resource.labels.isEmpty()
```

## if then else

`if c then a else b` evaluates `a` when `c` is `true`, and `b` when it's `false`. Only the chosen branch is evaluated. `c` must be a `Bool`:

```text
if resource has classification then resource.classification != "secret" else true
```

`if` has the lowest precedence. Inside `&&`, `||`, or a comparison, put it between parentheses:

```text
principal.active && (if context has n then context.n > 3 else false)
```
