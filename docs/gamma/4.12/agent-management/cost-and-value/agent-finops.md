---
hidden: true
noIndex: true
description: >-
  Attach prices to the catalog models and MCP tools agents consume, price human
  decisions, and read what a proxy or an agent cost at the AI Gateway.
---

# Agent FinOps

## Overview

There's no separate price list to maintain. Each catalog item carries its own cost attributes, a human decision carries the rate you set on its rule or on the environment, and the AI Gateway prices traffic against them as it flows. The figures then roll up per proxy on the dashboards and per agent on the agent's **Cost** page.

## Cost model in the catalog

Cost attributes live on the catalog items that incur them.

<table><thead><tr><th width="220">Catalog item</th><th>Cost attributes</th></tr></thead><tbody><tr><td>Model</td><td>An input price and an output price per million tokens, with the currency and the date the prices apply from. The model form labels them <strong>Input price</strong> and <strong>Output price</strong>, each followed by the currency and <strong>per 1M tokens</strong>. The form explains that your price is used for cost estimates and, once a proxy is republished, for cost tracking, and that a catalog refresh never changes it.</td></tr><tr><td>MCP tool</td><td>A <strong>Reference cost</strong> in US dollars per call, and a <strong>Reference value</strong> in US dollars per successful call. Both are optional and edited inline on the tool's page. A tool that carries no cost reads <strong>Not priced</strong>, which isn't the same as a price of zero.</td></tr></tbody></table>

To price an MCP tool, follow these steps:

1. From the Gamma console sidebar, select **Agent Management**.
2. In the **Catalog** section of the sidebar, select **Tools**.
3. Click the tool's name.
4. Next to **Reference cost**, click the edit button, enter the amount in US dollars per call, and save. Leave the field blank to leave the tool unpriced. A negative amount is refused.

The notification that confirms the change also says when it takes effect: the price applies on the next deployment of the MCP servers that use the tool. Saving a changed price rewrites the price book of every MCP Studio proxy that references the tool, and each proxy picks it up when you deploy it next. The **Reference value** row works the same way. See [Attribute business value to agent runs](attribute-business-value-to-agent-runs.md).

An LLM Proxy carries the prices of the models it exposes in its definition. Its models page shows them in a **Pricing** column, with a **Custom** badge for a price you set yourself and a dash for a model that has none.

## Price a human decision

A tool call held for human approval can carry a price too. Set the environment's rate as **Cost per decision (USD)** in the rule defaults of the **HITL** rules, or a rate on one rule as **Cost (USD)**. The rate is fixed on the approval when the call is held and charged when a person decides. See [Require human approval for MCP tool calls](../govern/require-human-approval-for-mcp-tool-calls.md).

## Metered at the AI Gateway

Every request through an LLM Proxy is priced as it passes through the AI Gateway. The Gateway applies the model's input and output prices to the input and output token counts of the request and records the input cost and the output cost as metrics of that request. Tool calls served by an MCP Studio proxy are priced against the price book the proxy carries, and the **MCP — Overview** dashboard reports that cost. Its **Tool Price Coverage** widget shows which billed calls carried a rate and which didn't, within the proxies that price at least one tool.

## Read what a proxy or an agent cost

* The **Overview** page of an LLM Proxy shows a **Cost (24h)** card. See [Monitor proxy and agent activity](../observe/monitor-proxy-activity.md) and [Monitor your LLM proxy](../observe/monitor-your-llm-proxy.md).
* The **MCP — Overview** dashboard shows **Tool Cost**, **Avg Cost / Billed Call**, **Top 5 Tools by Cost**, and **Tool Cost Over Time**.
* An agent's **Cost** page and the **Agent — Overview** dashboard add model spend, tool spend, and human decisions up for one agent. See [Read what an agent cost](read-what-an-agent-cost.md).

## Cap token usage at the Gateway

The Token Rate Limit policy caps the inbound and outbound tokens accepted over a period of minutes or seconds. See [Add the Token Rate Limit policy](../build/add-the-token-rate-limit-policy.md).
