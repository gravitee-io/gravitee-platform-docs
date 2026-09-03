---
description: >-
  Declare the business value an MCP tool delivers, classify how each agent run
  ended, and read the value delivered against the cost incurred per agent and per tool.
---

# Attribute business value to agent runs

## Overview

Counting tokens shows what an agent run cost. It doesn't show what the spend bought. Value attribution adds the other half of the ledger. The business value an action delivers is declared on the catalog entity that does the work, and each run is classified by whether it achieved its outcome.

Together they produce a return on investment view: value delivered against cost incurred, per agent and per tool, with the provenance of every value figure visible.

## What the platform records today

An MCP tool in the Catalog carries a **Reference cost**, an informational figure shown on the tool's detail page. Cost metrics are recorded for LLM traffic only. The AI Gateway prices the tokens of each LLM Proxy call from the input and output prices of the model, and the **LLM — Overview** dashboard reports that cost. The **MCP — Overview** dashboard reports request counts, error rate, and latency, and it has no cost widget and no outcome classification. See [Monitor your LLM proxy](../observe/monitor-your-llm-proxy.md).

## Declare the value of an MCP tool

A value tag attaches a declared business value to an MCP tool in the Catalog. For a tool that settles a claim, that value is the handling cost a human would otherwise incur. The business owner of the tool declares the value. Gravitee doesn't derive it, and the console says so wherever the figure appears.

<!-- TODO: verify label in Console UI — value tag surface and field labels are ahead of the build -->

<!-- TODO: Screenshot of a value tag declared on an MCP tool -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-value-tag-mcp-tool.png" alt=""><figcaption><p>Value is declared on the tool that delivers it, by the owner who can answer for it.</p></figcaption></figure>

## Classify the outcome of a run

Each run is classified as **succeeded**, **failed**, **abandoned**, or **flagged hallucinated**. The classification is declared or rule-based. Runs that failed, were abandoned, or were flagged as hallucinated stay in the denominator of every cost-per-outcome figure. A figure that excludes them is worse than no figure at all.

<!-- TODO: verify label in Console UI — outcome classification labels are ahead of the build -->

## Read cost per outcome

The cost-per-outcome figure divides the cost of all runs, failures included, by the number of successful business outcomes. It's set against the manual baseline it replaces. The cost of failure appears on the same screen as the value of success.

<!-- TODO: Screenshot of the cost-per-outcome rollup -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-cost-per-outcome.png" alt=""><figcaption><p>Cost per successful outcome, with the cost of failure beside it.</p></figcaption></figure>

## Read the return on investment view

The return on investment view sets the value delivered against the cost incurred, per agent and per tool. Every value figure carries its provenance: the business owner declared it, and Gravitee didn't derive it.

<!-- TODO: Screenshot of the return on investment view -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-return-on-investment-view.png" alt=""><figcaption><p>Value delivered against cost incurred, per agent and per tool.</p></figcaption></figure>
