---
description: How authorization, rate limits, and response redaction combine to govern what a caller can do through a Composite MCP Server.
---

# Layered governance for MCP tools

When you give an agent an MCP server, the agent inherits every permission the upstream credential holds. A Composite MCP Server closes that gap with three independent controls. Each answers a different question: which tools a caller may invoke, how often, and what the response is allowed to contain.

## Overview

The following table lists the three controls, the question each one answers, and where you configure it:

| Control | Question it answers | Where you configure it |
|---|---|---|
| Fine-Grained Authorization | Which tools may this caller invoke? | Authorization Management, enabled on the MCP Studio |
| Rate Limit policy | How many calls may this caller make? | Policy Studio, on the MCP proxy flow |
| PII Filtering policy | What may the response contain? | Policy Studio, on the MCP proxy flow |

You configure each control separately and can adopt them one at a time. Because all three act on the MCP call rather than on the upstream server, they don't depend on what the upstream server supports.

Curation is the control that comes before all of them. A tool you never compose into the server is a tool no policy has to defend against.

## Authorization decides which tools a caller reaches

To govern tool access by identity, enable Fine-Grained Authorization on a Composite MCP Server. The gateway then adds the GAPL Authorization PEP to the server's flow. On every tool call, the gateway resolves the caller and the tool into an authorization request, and then asks the in-gateway Policy Decision Point for a decision.

Policies are written in Gravitee Authorization Policy Language, a subset of the Cedar policy language. The caller becomes the subject, and the tool becomes the resource:

```
permit (
  principal in Group::"<group-id>",
  action,
  resource
);

forbid (
  principal in Group::"<group-id>",
  action,
  resource == MCPTool::"github-mcp-server.create_or_update_file"
);
```

Each entity reference in a policy is a unique identifier, not a display name:

* **`principal`** takes the group's identifier, not the group's name.
* **`resource`** takes the server-qualified tool identifier, in the form `MCPTool::"<server>.<tool>"`.
* **`action`** takes the same server-qualified tool identifier that the gateway sends at runtime. Leave `action` unconstrained unless you intend to match one specific tool invocation.

A clause that references a name where an identifier is expected doesn't match. Because an unmatched call is denied rather than permitted, the mistake surfaces as an unexplained denial.

The following three properties of that evaluation matter when you design a policy set:

* **A call with no matching permit is denied.** The gateway denies an explicit forbid and a request that matched no policy at all, so nothing is allowed by omission.
* **`forbid` beats `permit`.** A broad grant can't reopen a tool you've explicitly closed, however many policies you add later.
* **The upstream server is never called on a denial.** The decision runs in the request phase, so a denied call returns before the gateway forwards anything upstream. A Composite MCP Server created through MCP Studio returns `403` on a denial.

{% hint style="warning" %}
Constrain a policy only on values the gateway actually sends. A clause that constrains `action` or `resource` to any other vocabulary matches nothing, and the call is then denied by default rather than reported as a malformed policy.
{% endhint %}

You can also enable decision logging on the server. Each evaluated call then records the subject, the action, the resource, the decision, and the policies that determined it. That gives you a per-caller record that a shared upstream credential can't produce.

## Rate limits decide how often

Authorization doesn't constrain a caller that stays inside its permissions. An agent that retries or loops can call a permitted tool far more often than you intended, so cap the volume as well as the surface.

The **Rate Limit** policy supports MCP proxies and returns `429` once a caller exceeds its allowance. The following two policies also support MCP proxies:

* **Quota**. Use it for allowances measured over longer periods.
* **Spike Arrest**. Use it to smooth bursts rather than to enforce a total.

The **Token Bucket Rate Limit** policy doesn't support MCP proxies.

By default, the Rate Limit policy counts against the plan and subscription pair rather than the caller. To give each identity its own budget, set **Key** to an expression that resolves the caller's identity. Each identity then gets its own allowance, so one runaway agent doesn't consume everyone else's headroom.

**Use key only** additionally removes the plan and subscription from the counter, so a single identity draws on one allowance no matter which subscription the call arrives on. Leave it disabled to keep separate allowances per subscription.

To apply a limit to one high-value tool instead of the whole server, scope the flow to that tool. See [Apply policies to individual tool invocations](apply-policies-to-tool-invocations.md).

## Redaction decides what comes back

A permitted read is not the same as a safe response. A tool that returns a file, a record, or a ticket can hand the agent, and the model behind it, personal data that then flows into a context window and onward.

The **PII Filtering** policy classifies the payload and replaces each detected span with `[REDACTED]`. The following three points matter before you add it:

* **It filters responses by default.** The policy applies to the request body and to the response body. To pass a response through unfiltered, enable **Skip Response Payload Filtering**. Server-sent events are filtered in place, so streaming responses are scanned rather than rejected.
* **It needs an AI Resource.** Select an AI Model Token Classification resource on the API. Without one, the policy fails rather than passing the payload through.
* **You choose the categories.** Categories are a required setting with no default. The available categories are person, organization, location, email, phone, network identifier, device identifier, financial account, government ID, vehicle ID, credential, demographic, and miscellaneous.

**Confidence Threshold** sets the minimum classification score that triggers redaction, and defaults to `0.5`. A higher threshold redacts less and risks letting data through. A lower threshold redacts more and risks removing the content that made the response useful.

## Use cases

The following scenarios show the controls working together:

* **A read-mostly engineering role.** Permit the whole server, and then forbid the individual tools that write. Two statements turn a fully privileged role into a constrained one without minting a second credential.
* **A narrowly scoped triage agent.** Permit only the tools the agent needs. Everything else falls through to denial, so the role is defined by a short list of what it can do.
* **A support tool that returns customer records.** Add PII Filtering to the response path so contact details are redacted before the agent sees them, while the rest of the record passes through.

## Next steps

* [Create an MCP Studio](../create-an-mcp-studio.md). Compose a Composite MCP Server and enable Fine-Grained Authorization.
* [Add policies to your MCP server](add-policies-to-mcp-server.md). Author and deploy the authorization policies.
* [Apply policies to individual tool invocations](apply-policies-to-tool-invocations.md). Scope a rate limit or a redaction policy to one tool.
* [MCP policy examples](../../../authorization-management/configure/mcp-policy-examples.md). Worked policy patterns.
