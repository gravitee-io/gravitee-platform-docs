---
hidden: true
noIndex: true
description: >-
  Read one activity log entry per consequential agent action, carrying the
  decision chain that authorized it, the result it produced, and what it cost.
---

# Audit agent activity logs

## Overview

Every consequential action an agent takes crosses the Gateway, and the evidence for that action lands in several places:

* The authorization decision that permitted it.
* The Guardian verdict that judged it.
* The human approval that released it.
* The token and cost figures the LLM Proxy reported.

No single record answers what happened, on whose authority, with what outcome, and at what cost.

An activity log entry is that record. One entry is written per consequential action, and it carries the decision chain, the result, and the cost together.

The same entry serves two different readers. An auditor asks how human oversight was exercised. A finance team asks what a settled claim cost. Both read the entry, one for the decision chain and the other for the cost and the outcome.

## Understand why an activity log entry is evidence

An activity log entry is written from the enforcement chain at the moment the action is decided, rather than reconstructed afterward from other records.

That distinction is what makes an entry usable as evidence. A record assembled from other records after the fact is an inference about what happened, and an inference can be argued with. A record emitted by the policy enforcement point as it decides is a statement of what the platform did.

## Read what an activity log entry records

An entry has four parts: the decision chain, the result, the cost, and the correlation ID that ties it to every other record for the same action.

<!-- TODO: verify label in Console UI — the activity log surface and its field labels are ahead of the build -->

<!-- TODO: Screenshot of a single activity log entry with its decision chain, result, and cost -->

<figure><img src="../.gitbook/assets/PLACEHOLDER-activity-log-entry.png" alt=""><figcaption><p>One entry carries the decision chain, the result, and the cost for a single action.</p></figcaption></figure>

### The decision chain

The decision chain answers who acted, what they tried to do, and on whose authority the action proceeded.

<table><thead><tr><th width="260">What the entry carries</th><th>What it records</th></tr></thead><tbody><tr><td>Agent identity and delegation chain</td><td>The agent that acted, and the chain of delegation it acted under.</td></tr><tr><td>Action fingerprint</td><td>The identity of the action that was attempted.</td></tr><tr><td>Bound arguments</td><td>The argument values the action was invoked with.</td></tr><tr><td>Authorization decision</td><td>The decision that permitted or refused the action, with the version of the policy that produced it.</td></tr><tr><td>Guardian verdict</td><td>The verdict returned by the Guardian Agent, with the revision of the Guardian definition that returned it.</td></tr><tr><td>Approver and timestamp</td><td>Who decided and when, for an action a human released.</td></tr></tbody></table>

For how the Guardian verdict is produced, see [Guard agent actions with Guardian Agents](guard-agent-actions-with-guardian-agents.md). For how a human decision is requested and taken, see [Require human approval for MCP tool calls](require-human-approval-for-mcp-tool-calls.md).

### The result

The result records the effect that was applied and what the action actually returned, so the entry closes the loop between what was authorized and what happened.

An entry records the outcome. It doesn't interpret it.

### The cost

The cost records what the action consumed, priced from the cost attributes on the catalog items it used.

* Model tokens.
* Tool calls.
* Human approval time.

The cost sits on the same record as the decision chain and the result. A cost figure is therefore bound to the authority the action ran under and to what it produced. For where those cost attributes live, see [Agent FinOps](../cost-and-value/agent-finops.md).

### The correlation ID

The correlation ID ties the entry to the run it belongs to, the conversation that produced it, and every other record written for the same action. It's what turns a single entry into a thread you can follow across the platform.

## Query the activity log

Activity log entries are retrievable by agent, by action, by decision, by approver, and by time window. A question about one agent's behavior over a period is answered from the activity log itself, not by correlating separate records by hand.

<!-- TODO: Screenshot of the activity log filtered by agent and time window -->

<figure><img src="../.gitbook/assets/PLACEHOLDER-activity-log-query.png" alt=""><figcaption><p>Entries are retrieved by agent, action, decision, approver, and time window.</p></figcaption></figure>
