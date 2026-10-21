---
hidden: false
noIndex: false
description: Reference for the Gravitee Authorization Policy Language (GAPL), the language you write policies and schema documents in.
---

# GAPL reference

Gravitee Authorization Policy Language (GAPL) is the language of Authorization Management. You write GAPL in two places:

* In the **Code** view of the policy editor, where each policy holds one or more `permit` and `forbid` statements.
* In the **Schema text** of a schema document, where you declare entity types, actions, and their relationships.

The following policy lets members of the `engineering` group read the documents of their own department, unless a document is archived:

```
@id("engineering-reads-docs")
@reason("Engineers can read the documents of their department")
permit (
  principal in Group::"engineering",
  action == Action::"read",
  resource is Document
)
when { resource.department == principal.department }
unless { resource has archived && resource.archived };
```

## Pages in this section

* [**Policy statements**](policy-statements.md). The structure of a statement: its effect, its scope, its conditions, and its annotations.
* [**Values and types**](values-and-types.md). Literals, entity references, sets, records, and how console attribute types appear in GAPL.
* [**Operators and expressions**](operators-and-expressions.md). Every operator, method, and expression form, with its precedence.
* [**Extension functions**](extension-functions.md). The `ip`, `decimal`, `datetime`, and `duration` functions and their methods.
* [**The context record**](context.md). How to read `context`, and how the JSON values of a request become GAPL values.
* [**How statements are evaluated**](evaluation.md). How a decision is reached, and what happens when a statement can't be evaluated.
* [**Schema language**](schema-language.md). The syntax of schema documents.

## What the editor checks when you save

When you save a policy, Authorization Management parses its GAPL. A save is refused with **Could not save policy** when the text doesn't parse, for example in the following cases:

* The text has a syntax error. The message gives the line and the column, for example `line 1:56 mismatched input '}'`.
* Two statements of the policy declare the same `@id`. The message is `Duplicate policy ID: <id>`.
* A condition uses a name other than `principal`, `action`, `resource`, or `context` on its own, or a string with an escape sequence that doesn't exist.

A save checks only that the text is valid GAPL. It doesn't check that the policy makes sense.
