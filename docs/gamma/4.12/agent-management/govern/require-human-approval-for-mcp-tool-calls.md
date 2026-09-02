---
description: >-
  Declare approval rules against the MCP tools in your catalog so that
  sensitive tool calls wait for a human decision before they execute.
---

# Require human approval for MCP tool calls

## Overview

Human-in-the-Loop approval makes human oversight a property of the action rather than a feature of the agent. You declare approval rules against the MCP tools in the catalog, and the Gateway enforces them inline. The agent that triggers a rule needs no client-side integration, no SDK change, and no cooperation from the platform it runs on. Oversight therefore applies to agents you didn't build.

When a rule fires, the Gateway holds the tool call open while a human decides. MCP clients tolerate a tool call taking time to return, so the calling agent perceives nothing more than a slow tool call. It doesn't receive a failure or a redirect.

## Create an approval rule

An approval rule carries a name, an optional description, and the conditions under which it triggers. A rule declares which tool calls it applies to, can be enabled and disabled, and can carry its own expiry date after which it stops participating in evaluation.

<!-- TODO: verify label in Console UI — rule creation surface and field labels are ahead of the build -->

<!-- TODO: Screenshot of creating an approval rule against an MCP tool -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-hitl-approval-rule-create.png" alt=""><figcaption><p>An approval rule declares which tool it guards and the conditions that trigger it.</p></figcaption></figure>

### Trigger on the call's arguments

A rule can condition on the tool call's own arguments, not only on the tool's identity. Each condition names an argument, an operator, and a value, and the supported operators cover equality, comparison, containment, and pattern matching. A transfer above a threshold you set and a transfer of any amount are therefore different rules, so approval lands only on the calls that need it.

## Set the approval window

Every rule sets how long a pending approval stays open. When the window lapses without a decision, the request expires, and the rule itself defines the outcome: deny the call, or allow it to proceed.

## Approve, reject, or modify a pending call

The approvals dashboard shows each pending request with the context needed to decide, and the approver takes one of three actions:

* **Approve**: the held call proceeds as the agent intended it.
* **Reject**: the held call is refused.
* **Modify**: the approver adjusts the tool call's arguments and approves the modified call instead.

<!-- TODO: Screenshot of the approvals dashboard with a pending request open -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-hitl-approvals-dashboard.png" alt=""><figcaption><p>A pending request carries the context the approver decides on.</p></figcaption></figure>

## Audit decisions and track volume

Every approval decision is recorded durably, so there's an auditable trace of who decided what and when. The insights view tracks how the mechanism behaves over time. It covers the volume of approval actions, the time taken to decide, the number still pending, and the split between approved and rejected.

<!-- TODO: Screenshot of the HITL insights dashboard -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-hitl-insights-dashboard.png" alt=""><figcaption><p>Insights cover volume, decision time, pending count, and approved against rejected.</p></figcaption></figure>
