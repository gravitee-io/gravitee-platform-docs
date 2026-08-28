---
hidden: false
noIndex: false
description: Monitor token usage, cost, and model and provider mix for your LLM Proxies on the LLM Overview dashboard. Learn what each widget and metric shows.
---

# Monitor your LLM proxy

Every call that passes through an LLM Proxy is metered by the AI Gateway. The gateway records which provider served the call, which model answered it, how many tokens went in and out, and what those tokens cost. The **LLM — Overview** dashboard in the Gamma console turns that raw record into usage, cost, and latency you can read at a glance.

Use this dashboard to answer questions such as: which model is burning the budget, which provider is slowest, whether a spike in cost is a spike in traffic or a shift to a more expensive model, and whether errors are concentrated on one proxy.

## What the gateway records

Each metered request writes a set of additional metrics onto the request record. The dashboard, the log viewer, and the token and cost rate limit policies all read from the following set:

| Metric                            | Type    | Published when                                                     | Value                                                                                                          |
| --------------------------------- | ------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| `keyword_llm-proxy_provider`      | Keyword | The invoker resolved a target, on every routed call                | The provider the call was routed to. Technically the endpoint group name, or the endpoint name on routes the gateway passes through without resolving a model. |
| `keyword_llm-proxy_model`         | Keyword | Any metered response, whether it carried a usage block or not      | The model named in the response body, falling back to the model the caller requested.                          |
| `long_llm-proxy_tokens-sent`      | Long    | The response body carried an input token count                     | The whole prompt, including any cache-read and cache-write tokens.                                             |
| `long_llm-proxy_tokens-received`  | Long    | The response body carried an output token count                    | The output tokens the model produced.                                                                          |
| `double_llm-proxy_sent-cost`      | Double  | The model is declared on the endpoint **and** both prices are set  | Cost of the input tokens.                                                                                      |
| `double_llm-proxy_received-cost`  | Double  | Same as above                                                      | Cost of the output tokens.                                                                                     |

Note the following two points before you read any number on the dashboard:

* **The model is the response model, not the request model.** A caller that asks for `gpt-5.6-sol` may be answered by `gpt-5.6-sol-20260712`, and it is the second name that is recorded. This is what you want for cost attribution, because that is the name the price is attached to, but it means the model breakdown will not always match the model names your consumers think they are calling.
* **`tokens-sent` is the whole prompt.** Cache reads and cache writes are already inside it. Do not add a cached-token figure on top of it.

### Where cost comes from

Cost is not reported by the provider. The gateway computes it from the token counts and the input and output prices recorded on the model:

```
cost = tokens × price / 1,000,000
```

Prices are configured per million tokens on the AI model in the Catalog and are carried onto the LLM Proxy endpoint when the proxy is published. See [Add an AI model](../import/add-an-ai-model.md).

Both prices must be set for cost to be published. A price of `0` is valid and means free. An absent price means *unknown*, which is not the same thing, and no cost is recorded for that call.

## Open the LLM Overview dashboard

You can open the dashboard across every LLM Proxy in the environment, or pre-filtered to a single proxy.

### Across all LLM Proxies

1. From the Gamma console sidebar, select **Agent Management**.
2. In the **Observability** section of the sidebar, select **Dashboards**.
3. Select the **LLM — Overview** dashboard.

The dashboard opens scoped to LLM traffic only. It opens on a short relative time range — **Last 5 minutes** — so widen it with the time range control in the dashboard header before you read anything into an empty chart.

### For a single LLM Proxy

1. From the Gamma console sidebar, select **Agent Management**.
2. Select **LLM Proxies**, then select your proxy.
3. In the **Observability** group of the proxy sidebar, select **Dashboard**.

The dashboard opens in a new tab with the **API** filter already set to that proxy, so every widget on the page describes that proxy alone. The neighbouring **Logs** and **Tracing** items open the same way, pre-filtered to the same proxy — useful when a widget shows you *that* something went wrong and you need the individual requests that caused it.

## What each widget shows

### Key Metrics

A row of seven headline figures summarizes the current filter and time range:

| Figure                | What it means                                                                                                   |
| --------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Requests**          | Total requests through the LLM Proxies in scope.                                                                |
| **Total Tokens**      | Sent plus received tokens, summed. A derived figure — there is no single total-token metric on the request record. |
| **Total Cost**        | Sent cost plus received cost, summed. Also derived, and it only counts calls that carried a usable price.        |
| **Avg Cost / Req**    | Total cost divided across requests. The number to watch when traffic is flat but spend is not.                  |
| **Avg Tokens / Req**  | Total tokens divided across requests. A proxy for prompt size and answer length.                                |
| **P95 Response Time** | 95th percentile gateway response time. Latency for LLM traffic is dominated by the provider, so this mostly tracks provider health. |
| **Error Rate**        | Percentage of requests that returned an error status.                                                           |

Because **Total Cost** and **Avg Cost / Req** ignore calls with no price, they read low rather than wrong when part of your traffic is unpriced. Confirm the model prices are set before you treat either figure as a bill.

### Traffic and latency

Four widgets describe request volume and how fast those requests were served:

| Widget                            | What it shows                                                                                                                    |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Requests vs Avg Response Time** | Request volume as bars against average gateway response time as a line. Use it to separate a rise in traffic from a slowdown at the provider. |
| **Top 5 LLM Proxies**             | The most-used LLM Proxies by request count. On the environment-wide view this is your first cut at *who is generating the traffic*. |
| **Requests by Model + P95**       | Per-model request volume, stacked, with P95 response time overlaid. This is the widget that shows a traffic shift between models and what it did to latency. |
| **Requests by Provider**         | Request share per provider.                                                                        |

### Tokens and cost

Four widgets describe token consumption and what it cost:

| Widget                        | What it shows                                                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Token Usage Over Time**     | Sent, received, and total tokens as three lines. Divergence between sent and received is the shape of your workload: retrieval-heavy prompts push the sent line up, long generations push the received line up. |
| **Tokens by Model**            | Total token share per model.                                                             |
| **Cost Over Time**            | Sent cost, received cost, and total cost over time. Read it beside **Token Usage Over Time** — cost that climbs while tokens stay flat means traffic moved to a pricier model. |
| **Cost by Provider**           | Total cost share per provider, with a per-model breakdown on hover.                    |

### Errors

Two widgets describe the response status of LLM traffic:

| Widget                    | What it shows                                                                                       |
| ------------------------- | ----------------------------------------------------------------------------------------------------- |
| **Status Over Time**      | Response status groups — `1xx` Informational, `2xx` Success, `3xx` Redirection, `4xx` Client Error, and `5xx` Server Error — stacked over time, with a total on hover. |
| **Status Distribution**   | Share of responses by status group, with individual status codes on hover.                          |

A rise in `4xx` usually points at consumers — a rate limit policy biting, an expired key, a malformed request format. A rise in `5xx` usually points upstream at the provider. Hover to get the exact code, then open **Logs** for the same time range to see the requests behind it.

## Filter and scope the dashboard

Every widget on the page honours the filter bar and the time range picker, so a filter you apply narrows the whole dashboard at once, not one chart.

Alongside the filters shared by all traffic — API, application, plan, status code, response time, gateway, and country among them — LLM traffic adds two of its own:

| Filter           | Field                                | Use it to                                                    |
| ---------------- | ------------------------------------ | -------------------------------------------------------------- |
| **LLM Model**    | `keyword_llm-proxy_model`            | Isolate one model across every proxy and provider that serves it. |
| **LLM Provider** | `keyword_llm-proxy_provider`         | Compare the cost and latency of one provider against a second.       |

Both are also available in the log viewer, so a filter you settle on here transfers directly to the logs.

## Troubleshooting

**A model shows requests and tokens, but no cost.** Cost needs both an input and an output price on the model. Check the model in the Catalog under **AI Models**: if only one price is set, or neither is, no cost is recorded for that model's traffic. Set both — use `0` for a model you are genuinely not billed for. After a price changes, republish any LLM Proxy that consumes that model so cost tracking picks up the new rate.

**A model shows requests, but no tokens and no cost.** The response carried no usage block, so there was nothing to meter. The gateway raises a `KEY_WARN_NO_TOKENS_TRACKING` warning on the request when this happens. It is normal for error responses and for providers or response formats that omit usage, and it is worth investigating if it appears on successful calls.

**Cost is missing for a model that is priced in the Catalog.** The gateway can only price a model that is declared on the LLM Proxy endpoint. If a caller overrides the model at runtime to one the endpoint does not declare, the response is proxied but the cost is not computed, and the gateway raises a `COST_CALCULATION_MODEL_NOT_FOUND` warning. Declare the model on the endpoint, or restrict which models callers may request. See [Override the model at runtime](../build/override-the-model-at-runtime.md).

**The dashboard is empty.** Confirm the proxy is deployed and has received traffic inside the selected time range, then widen the time range. If the environment-wide dashboard has data but the per-proxy view does not, the **API** filter is pinned to a proxy with no traffic.

**Token and cost figures look lower than the provider's own bill.** Only metered calls contribute. Requests that failed before reaching the provider, and responses with no usage block, carry no tokens. Prompt caching does not account for a shortfall, because cached tokens are already counted inside `tokens-sent`.

## Next steps

* [Add the Token Rate Limit policy](../build/add-the-token-rate-limit-policy.md). Cap token consumption once monitoring shows you where it concentrates.
* [Inspect your agent log](inspect-your-agent-log.md). Drop from an aggregate figure to the individual invocations behind it.
* [Monitor your MCP servers](monitor-your-mcp-servers.md). The equivalent view for MCP Proxy traffic.
