---
hidden: false
noIndex: false
description: The context variable of GAPL, how to read it safely, and how the JSON values of a request become GAPL values.
---

# The context record

`context` is a record of request-time data, such as the API that was called or a value from a header. A policy reads it like any record:

```
context.caller == "pep"
context has tenant && context.tenant == "acme"
```

A key that isn't there is an error when you read it, and the statement is skipped. Guard every key you aren't sure of with `has`, as in the second example.

## What context holds

What `context` holds depends on who asks for the decision. Each way to ask sets some keys itself, such as `caller`, and lets you add your own. For the keys of each one, see:

* [Authorization PEP policy](../evaluate/ask-for-a-decision/authorization-pep-policy.md#keys-the-gateway-sets-in-context)
* [AuthZEN endpoint](../evaluate/ask-for-a-decision/authzen-endpoint.md#evaluate-a-request)
* [AuthZEN PDP policy](../evaluate/ask-for-a-decision/authzen-policy.md#requests-and-answers)

Properties sent with the action of a request are added to `context` too, and replace a key with the same name.

## How JSON values become GAPL values

Request data becomes GAPL values as follows. The same rules apply to `context`, to properties, and to entity attributes:

| JSON value | GAPL value |
|-----------|-----------|
| `true`, `false` | `Bool` |
| An integer, such as `42` | `Long` |
| A string, such as `"acme"` | `String` |
| A string shaped like an entity reference, such as `"AgentIdentity::\"planner\""` | Entity |
| `{ "__entity": { "type": "User", "id": "alice" } }` | Entity |
| A number with a fraction, such as `0.75` | No usable value: every operator on it is an error. Send `"0.75"` and use `decimal(...)` |
| An array | `Set` |
| Any other object | Record |
| `null` | No value: the key is left out |

To pass an IP address, a decimal, a date, or a duration, send it as a string and convert it in the policy with [`ip`](extension-functions.md#ip), [`decimal`](extension-functions.md#decimal), [`datetime`](extension-functions.md#datetime), or [`duration`](extension-functions.md#duration):

```
ip(context.clientIp).isInRange(ip("10.0.0.0/8"))
```
