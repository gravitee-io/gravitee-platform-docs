---
hidden: true
noIndex: true
description: >-
  Attach prices to the catalog items agents consume, meter LLM traffic at the
  AI Gateway as it flows, and cap token usage at the Gateway.
---

# Agent FinOps

## Overview

There's no separate price list to maintain. Each catalog item carries its own cost attributes, and the AI Gateway prices LLM traffic against them as requests flow through it.

## Cost model in the catalog

Cost attributes live on the catalog items that incur them.

<table><thead><tr><th width="220">Catalog item</th><th>Cost attributes</th></tr></thead><tbody><tr><td>Model</td><td>An input price and an output price per million tokens, with the currency and the date the prices apply from.</td></tr><tr><td>MCP tool</td><td>A reference cost, shown as <strong>Reference cost</strong> on the tool's detail page.</td></tr></tbody></table>

An LLM Proxy carries the prices of the models it exposes in its definition. Its models page lists them as **Input price /M tokens** and **Output price /M tokens**.

## Metered at the AI Gateway

Every request through an LLM Proxy is priced as it passes through the AI Gateway. The Gateway applies the model's input and output prices to the input and output token counts of the request. It records the input cost and the output cost as metrics of that request. When the request's model has no price, the Gateway raises a `COST_CALCULATION_MODEL_NOT_FOUND` execution warning instead of recording a cost.

## Read what a proxy cost

The Overview page of an LLM Proxy shows a **Cost (24h)** card. See [Monitor proxy activity on the Overview page](../observe/monitor-proxy-activity.md) and [Monitor your LLM proxy](../observe/monitor-your-llm-proxy.md).

## Cap token usage at the Gateway

The Token Rate Limit policy caps the inbound and outbound tokens accepted over a period of minutes or seconds. See [Add the Token Rate Limit policy](../build/add-the-token-rate-limit-policy.md).
