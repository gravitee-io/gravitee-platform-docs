---
hidden: false
noIndex: false
description: The value types of GAPL, how to write each literal, and how the attribute types of the console appear in policies.
---

# Values and types

Every GAPL expression evaluates to a value of one of the following types:

| Type | Example literal | Notes |
|------|-----------------|-------|
| `Bool` | `true`, `false` | |
| `Long` | `42`, `-7` | A 64-bit signed integer. There are no fractional literals |
| `String` | `"read-only"` | |
| Entity | `User::"alice"` | A reference to an entity, by type and ID |
| `Set` | `["a", "b"]` | Unordered, without duplicates |
| Record | `{ city: "Lyon", "zip code": "69001" }` | Named fields |
| Extension | `ip("10.0.0.1")` | IP addresses, decimals, datetimes, and durations, built with functions |

The type of a value comes from the value itself. Saving a policy only checks that its GAPL parses, and the schema isn't applied, so a comparison between two types isn't caught when you save. For how each operator treats each type, see [Operators and expressions](operators-and-expressions.md).

## Long

A `Long` literal is a sequence of digits, with `-` in front for a negative number. The range is from `-9223372036854775808` to `9223372036854775807`. A literal or a calculation outside that range is an error, and the statement is skipped.

GAPL has no fractional numbers. For a value such as `0.75`, use [`decimal`](extension-functions.md#decimal).

## String

A string is written between double quotes. The following escape sequences are supported:

| Sequence | Character |
|----------|-----------|
| `\"` | Double quote |
| `\\` | Backslash |
| `\'` | Single quote |
| `\*` | Asterisk, used in [`like`](operators-and-expressions.md#like) patterns |
| `\n`, `\r`, `\t` | Line feed, carriage return, tab |
| `\0` | Null character |
| `\u{263A}` | The Unicode character with that code point, from one to six hexadecimal digits |

Any other character after `\` is a syntax error. A string can't span lines: write `\n` for a line break.

## Entity references

An entity reference is a type and an ID joined by `::`, such as `User::"alice"`. A reference is a value: it can be compared with `==`, passed to `in`, and its attributes are read with `.`:

```
resource.owner == principal
principal in resource.editors
User::"alice".department == "finance"
```

Reading an attribute of a referenced entity requires the entity to exist on the gateway. For the syntax of references, see [Entity references](policy-statements.md#entity-references), and for namespaced types, see [Namespaces](policy-statements.md#namespaces).

## Sets

A set literal lists values between square brackets, separated by commas. A trailing comma is allowed, and `[]` is the empty set. A set can mix types, and duplicates are dropped:

```
["admin", "auditor"]
[User::"alice", User::"bob"]
```

Two sets are equal when they hold the same values, in any order. For the set methods, see [Operators and expressions](operators-and-expressions.md#set-methods).

## Records

A record literal lists fields between braces. A field name is an identifier, or a string when it contains other characters:

```
{ method: "GET", "x-tenant": "acme" }
```

Read a field with `.name`, or with `["name"]` when the name isn't an identifier or is a GAPL keyword, such as `context["x-tenant"]` or `context["action"]`. Two records are equal when they have the same field names and equal values.

## Console attribute types in GAPL

The attributes you give principals and resources in the console appear in GAPL as the following values:

| Console attribute type | GAPL value | Example condition |
|------------------------|-----------|-------------------|
| **String**, **Enum** | `String` | `principal.department == "finance"` |
| **Integer** | `Long` | `resource.level >= 3` |
| **Boolean** | `Bool` | `principal.active` |
| **Set&lt;String&gt;** | `Set` of `String` | `principal.roles.contains("auditor")` |
| **EntityRef** | Entity | `resource.owner == principal` |
| **Set&lt;EntityRef&gt;** | `Set` of entities | `principal in resource.editors` |
| **Decimal** | `String` | `decimal(principal.score).greaterThan(decimal("0.5"))` |
| **Timestamp** | `String` | `datetime(resource.expiresAt) > datetime("2026-01-01")` |
| **Duration** | `String` | `duration(resource.retention) <= duration("30d")` |
| **IP**, **CIDR** | `String` | `ip(principal.lastIp).isInRange(ip(resource.network))` |

**Decimal**, **Timestamp**, **Duration**, **IP**, and **CIDR** attributes are stored as text. Convert them with the matching function in your condition, as the examples show. The function accepts only the formats listed in [Extension functions](extension-functions.md). When a stored value doesn't match them, such as a timestamp without a time zone, the statement is skipped.
