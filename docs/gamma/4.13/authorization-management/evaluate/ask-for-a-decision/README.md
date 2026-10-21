---
hidden: false
noIndex: false
description: The three ways to ask a PDP gateway for an authorization decision, and how each one builds the principal, action, resource, and context that your policies read.
---

# Ask for a decision

A gateway evaluates your policies when something asks it for a decision. Authorization Management offers three ways to ask:

| Way to ask | What it is | Engine it asks | `context.caller` |
|------------|-----------|----------------|------------------|
| [**Authorization PEP policy**](authorization-pep-policy.md) | A policy in the flow of an API, MCP proxy, LLM proxy, or A2A proxy. It asks for a decision on every request and lets the request through only on a permit | The default engine of the gateway | `"pep"` |
| [**AuthZEN endpoint**](authzen-endpoint.md) | An AuthZEN 1.0 API that a PDP gateway exposes on a path you choose. Applications and agents outside the gateway call it | The engine of that PDP gateway | `"gateway"` |
| [**AuthZEN PDP policy**](authzen-policy.md) | A policy that answers AuthZEN 1.0 requests on a v4 API you already have, on its path and its plan | The default engine of the gateway | `"authzen"` |

An action property named `caller` replaces the value of `context.caller`. Each way builds the same request for the engine: a principal, an action, a resource, and a `context` record. Your policies read them as `principal`, `action`, `resource`, and `context`. For the language, see [GAPL reference](../../gapl-reference/README.md).

{% hint style="info" %}
The Authorization PEP policy and the AuthZEN PDP policy always ask the default engine of the gateway. Policies and entities targeted only at a named PDP gateway don't apply to their requests. To ask a named PDP gateway, call its AuthZEN endpoint.
{% endhint %}

Each decision appears on the **Decisions** page, with the way it was asked under **Caller kind**. For details, see [Review authorization decisions](../../observe/review-authorization-decisions.md).
