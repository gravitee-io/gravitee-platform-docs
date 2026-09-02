---
description: >-
  Define rates against the catalog entities that incur them, so every agent run
  carries a cost record you can explain and reproduce.
---

# Define rates with the price book

## Overview

An agent run consumes more than LLM tokens. Its MCP tool calls and the human approvals it triggers cross the Gateway too, and a cost figure that prices only the tokens omits the rest of the run.

The price book prices the whole run. Rates are defined once, against the catalog entities that incur them, rather than embedded in a telemetry pipeline. Because price is a property of the entity, a cost figure can be explained and reproduced later: an operator can point at the rate that produced it.

## Set the rates a run is priced with

The price book is a first-class entity. Rates are defined, stored, and edited in one place, and they cover the three priced event sources of a run.

<table><thead><tr><th width="220">Rate</th><th>What it prices</th></tr></thead><tbody><tr><td>Model token rates</td><td>LLM usage, with input, output, cache, and reasoning tokens priced separately per model.</td></tr><tr><td>Per-tool-call rates</td><td>Each call to an MCP tool in the catalog.</td></tr><tr><td>Per-approval rates</td><td>Each human approval decision, so human time enters the cost model as a priced resource.</td></tr></tbody></table>

The catalog already carries per-model input and output token prices ingested with the model definition. The price book builds on that by making rates editable and by extending pricing beyond model tokens.

<!-- TODO: verify label in Console UI — price book surface and field labels are ahead of the build -->

<!-- TODO: Screenshot of the price book with model, tool, and approval rates -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-price-book-rates.png" alt=""><figcaption><p>Rates live in one place, against the entities that incur them.</p></figcaption></figure>

## Read a run's decomposed cost record

Every run carries a cost record built from its three priced event sources: its LLM proxy requests, its MCP tool calls, and its human approval decisions. The record is decomposed rather than a single opaque figure, so each component of the cost traces back to the events that incurred it and the rates that priced them.

<!-- TODO: Screenshot of a run's decomposed cost record -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-run-cost-record.png" alt=""><figcaption><p>A run's cost decomposes into its priced components instead of one number.</p></figcaption></figure>
