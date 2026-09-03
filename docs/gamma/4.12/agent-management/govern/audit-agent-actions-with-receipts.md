---
description: >-
  Read one receipt per consequential agent action, carrying the decision chain
  that authorized it, the result it produced, and what it cost.
---

# Audit agent actions with receipts

## Overview

Every consequential action an agent takes crosses the Gateway, and the evidence for that action lands in several places:

* The authorization decision that permitted it.
* The Guardian verdict that judged it.
* The human approval that released it.
* The token and cost figures the LLM Proxy reported.

No single record answers what happened, on whose authority, with what outcome, and at what cost.

A receipt is that record. One receipt is emitted per consequential action, and it carries the decision chain, the result, and the cost together.

The same receipt serves two different readers. An auditor asks how human oversight was exercised. A finance team asks what a settled claim cost. Both read the receipt, one for the decision chain and the other for the cost and the outcome.

## Understand why a receipt is evidence

A receipt is emitted from the enforcement chain at the moment the action is decided, rather than reconstructed from logs afterward.

That distinction is what makes a receipt usable as evidence. A record assembled from logs after the fact is an inference about what happened, and an inference can be argued with. A record emitted by the policy enforcement point as it decides is a statement of what the platform did.

## Read what a receipt records

A receipt has four parts: the decision chain, the result, the cost, and the correlation ID that ties it to every other record for the same action.

<!-- TODO: verify label in Console UI — the receipt surface and its field labels are ahead of the build -->

<!-- TODO: Screenshot of a single receipt with its decision chain, result, and cost -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-receipt-detail.png" alt=""><figcaption><p>One receipt carries the decision chain, the result, and the cost for a single action.</p></figcaption></figure>

### The decision chain

The decision chain answers who acted, what they tried to do, and on whose authority the action proceeded.

<table><thead><tr><th width="260">What the receipt carries</th><th>What it records</th></tr></thead><tbody><tr><td>Agent identity and delegation chain</td><td>The agent that acted, and the chain of delegation it acted under.</td></tr><tr><td>Action fingerprint</td><td>The identity of the action that was attempted.</td></tr><tr><td>Bound arguments</td><td>The argument values the action was invoked with.</td></tr><tr><td>Authorization decision</td><td>The decision that permitted or refused the action, with the version of the policy that produced it.</td></tr><tr><td>Guardian verdict</td><td>The verdict returned by the Guardian Agent, with the revision of the Guardian definition that returned it.</td></tr><tr><td>Approver and timestamp</td><td>Who decided and when, for an action a human released.</td></tr></tbody></table>

For how the Guardian verdict is produced, see [Guard agent actions with Guardian Agents](guard-agent-actions-with-guardian-agents.md). For how a human decision is requested and taken, see [Require human approval for MCP tool calls](require-human-approval-for-mcp-tool-calls.md).

### The result

The result records the effect that was applied and what the action actually returned, so the receipt closes the loop between what was authorized and what happened.

A receipt records the outcome. It doesn't interpret it.

### The cost

The cost records what the action consumed, priced from the rates held in the price book.

* Model tokens.
* Tool calls.
* Human approval time.

The cost sits on the same record as the decision chain and the result. A cost figure is therefore bound to the authority the action ran under and to what it produced. For how these rates are set, see [Define rates with the price book](../cost-and-value/define-rates-with-the-price-book.md).

### The correlation ID

The correlation ID ties the receipt to the run it belongs to, the conversation that produced it, and every other record written for the same action. It's what turns a single receipt into a thread you can follow across the platform.

## Query receipts

Receipts are retrievable by agent, by action, by decision, by approver, and by time window. A question about one agent's behavior over a period is answered from the receipts themselves, not by correlating separate records by hand.

<!-- TODO: Screenshot of the receipt list filtered by agent and time window -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-receipt-query.png" alt=""><figcaption><p>Receipts are retrieved by agent, action, decision, approver, and time window.</p></figcaption></figure>
