---
hidden: false
noIndex: false
description: How the policy engine combines GAPL statements into one decision, and what happens to a statement that can't be evaluated.
---

# How statements are evaluated

For each request, the engine evaluates every statement of every policy deployed to it. The order of statements, and of policies, doesn't matter.

## How a decision is reached

A statement matches a request when its scope matches, every `when` condition is `true`, and every `unless` condition is `false`. The decision then follows from the statements that match:

| Statements that match | Decision | AuthZEN `decision` |
|-----------------------|----------|--------------------|
| At least one `forbid` | **Forbid** | `false` |
| At least one `permit`, and no `forbid` | **Permit** | `true` |
| None | **Not applicable** | `false` |

A `forbid` always wins: one matching `forbid` denies the request, whatever the number of matching `permit` statements. A request that no statement matches is denied too, with the reason `No applicable policy`.

The decision lists the statements that decided it. For a **Forbid**, both the `forbid` and the `permit` statements that matched are listed, and the reason comes from the `forbid` statements. For how statements are named, see [Annotations](policy-statements.md#annotations).

## When a statement can't be evaluated

Evaluating a statement can fail. A failed statement is skipped: it counts as a statement that doesn't match, and the other statements decide the request. The decision doesn't say that a statement was skipped. When no other statement matches, the reason is `No applicable policy`.

The following table lists what makes a statement fail:

| Cause | Example |
|-------|---------|
| A context key or a record field that isn't there | `context.mfa`, when the request has no `mfa` |
| An attribute that the entity doesn't have | `principal.department`, when the principal has no `department` attribute |
| An attribute of an entity that doesn't exist on the gateway | `resource.owner`, when the resource isn't an entity |
| An operator applied to a type it doesn't accept | `"a" < "b"`, `context.count && true`, `principal.name.contains("x")` |
| A string that an extension function doesn't accept | `datetime("2026-06-30T17:00:00")`, which has no time zone |
| A function or a method that doesn't exist | `ip(context.clientIp).isPrivate()` |
| The wrong number of arguments | `ip("10.0.0.1", "10.0.0.2")` |
| A `Long` result outside the `Long` range | `9223372036854775807 + 1` |

None of these causes stops a save. They show up only when the statement is evaluated.

## Write forbid statements that can't be skipped

A skipped `forbid` denies nothing. When a `forbid` reads data that can be missing, a request without that data is decided by your `permit` statements alone.

The following statement is skipped for every request without an `mfa` key, so those requests aren't denied:

```text
forbid (principal, action == Action::"delete", resource)
unless { context.mfa };
```

Read the key only when it's there, so that a missing key gives `false` and the `forbid` applies:

```text
forbid (principal, action == Action::"delete", resource)
unless { context has mfa && context.mfa };
```

The same applies to attributes: guard them with `has`, for example `resource has classification && resource.classification == "public"`.

## Check a statement before you deploy it

To see whether a statement can be evaluated, run it in the Policy Simulator. When a policy can't be evaluated and no other policy decides the call, the simulator shows **Not evaluated** and lists the cause under **Engine errors**. For the steps, see [Simulate policy decisions](../test/simulate-policy-decisions.md).
