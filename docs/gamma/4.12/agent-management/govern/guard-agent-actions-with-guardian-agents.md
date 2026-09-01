---
description: >-
  Bind a Guardian Agent into the MCP proxy policy chain so every intended agent
  action is judged in context and receives a bounded verdict before it executes.
---

# Guard agent actions with Guardian Agents

## Overview

Deterministic rules enforced in the request path, for example prompt guardrails and classification resources, bound what an agent is allowed to attempt. They can't judge whether a permitted action is the right one in context.

A Guardian Agent does that second job. It inspects an intended action in full context and returns a bounded verdict before the action executes. The Guardian's reasoning is returned alongside the verdict, so a decision is always explainable.

## Verdicts

A Guardian returns one of four bounded verdicts:

<table><thead><tr><th width="140">Verdict</th><th>What it means</th></tr></thead><tbody><tr><td><code>ALLOW</code></td><td>The action proceeds as the agent intended it.</td></tr><tr><td><code>DENY</code></td><td>The action is blocked.</td></tr><tr><td><code>MODIFY</code></td><td>A safer version of the action is proposed instead of a plain block, with the modified arguments visible.</td></tr><tr><td><code>STEP_UP</code></td><td>The decision is escalated to a named human for approval rather than decided by the Guardian alone.</td></tr></tbody></table>

## Understand when a Guardian is invoked

A Guardian is bound natively into the MCP proxy policy chain, so it's invoked during MCP tool call processing and always before the action executes.

Deterministic rules keep the first word. A request that a deterministic rule denies is blocked without invoking the Guardian at all. The Guardian only narrows what the deterministic rules already permitted, which keeps its latency and its non-determinism out of the requests that never needed judgment.

{% hint style="warning" %}
Guardian enforcement fails closed. If the Guardian can't be reached, the action is blocked. This is a deliberate default: an unreachable judge must not become an open gate.
{% endhint %}

## Understand the context a Guardian sees

The platform assembles the context the Guardian judges with. You don't wire it by hand. The context carries:

* The agent's original mandate.
* The agent's history of prior calls.
* The agent's identity and delegation chain.
* The fingerprint of the intended action.

## Use a pre-configured Guardian Agent

A small set of pre-configured Guardian Agents ships with the platform, each solving a specific, recognizable problem.

<!-- TODO: verify from code — the hosting surface for pre-configured Guardians and its product name (the epic hosts them on the Agent Control Tower) -->

<!-- TODO: Screenshot of binding a Guardian Agent to an MCP proxy -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-guardian-agent-binding.png" alt=""><figcaption><p>A Guardian Agent is bound to the MCP proxy and judges every tool call before it executes.</p></figcaption></figure>

## Review Guardian decisions

Every Guardian decision is logged with the context that was available to the Guardian when it decided, the tool that was called, and the verdict. Use the log to troubleshoot a blocked action, to audit decisions, and to measure over time whether a client agent is performing well or drifting away from its initial intent.

<!-- TODO: Screenshot of the Guardian decision log with a DENY verdict expanded -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-guardian-decision-log.png" alt=""><figcaption><p>Each decision carries its verdict, the tool called, and the context the Guardian judged with.</p></figcaption></figure>
