---
hidden: false
noIndex: false
description: Add the Cost Rate Limit policy to an LLM Proxy to cap what a consumer spends in dollars over a period. Follow the steps to configure it.
---

# Add the Cost Rate Limit policy

## Overview

A token allowance is a count with no stable price. The same five million tokens cost a few dollars on one model and several hundred on another, so a token cap can't express a spending ceiling. The **Cost Rate Limit** policy counts money instead, and returns `429` once a consumer exceeds the budget you set.

The policy reads the cost the LLM Proxy computes for each request from the prices configured on the models it serves, and charges it against a budget in dollars. Budgets accept decimals, so `0.05` is five cents and `50` is fifty dollars.

Cost Rate Limit runs on an LLM Proxy in the request phase, and it coexists with [Token Rate Limit](add-the-token-rate-limit-policy.md) on the same flow. This page doesn't cover per-model or per-provider sub-limits, which the policy doesn't support.

## Prerequisites

Before you begin, confirm that you have the following:

* A self-hosted or hybrid Gamma installation. For more information, see [Self-hosted installation guides](../../platform-management/install/self-hosted-installation-guides/README.md) and [Hybrid installation guides](../../platform-management/install/hybrid-installation-guides/README.md).
* A deployed LLM Proxy. For more information, see [Create an LLM Proxy](create-an-llm-proxy.md).
* A price on every model the proxy serves. Set **Price per million tokens (input) sent to LLM ($)** and **Price per million tokens (output) received from LLM ($)** on each model in the LLM Proxy endpoint configuration. A model with no price publishes no cost, and **Missing price policy** decides what happens to it.

## Add the policy

1. On the LLM Proxy detail page, under **Design**, open **LLM Studio**.
2. Under **Common Flows**, select the flow you want to limit, usually **Prompt**.
3. In the **Request Phase** section, click **Browse all...** to open the policy catalog.
4. Search for **Cost Rate Limit**, and then click **Add to flow**.
5. Configure the policy using the settings in [Settings](#settings).
6. Click **Save**.
7. When the "This deployable is out of sync" message appears, click **Deploy** to push the change to the AI Gateway.

## Settings

### Cost budget

The **Cost budget** section sets the amount, the window it runs over, and who it belongs to:

| Setting | Description | Default |
| --- | --- | --- |
| **Max budget (dollars)** | The amount allowed per period, in dollars. Enter `5` for five dollars and `0.05` for five cents. Leave it at `0` to use the dynamic budget instead | - |
| **Max budget (dynamic, dollars)** | An Expression Language expression that resolves to the budget, in dollars. Used only when the static budget is `0` | - |
| **Time duration** | How long before the budget resets | `1` |
| **Time unit** | `MINUTES`, `HOURS`, or `DAYS` | `DAYS` |
| **Key** | Identifies the consumer the budget applies to. Supports Expression Language. Leave it empty to count against the plan and subscription pair | Empty |
| **Use key only** | Counts against the key alone, ignoring the subscription and plan. Ignored while **Key** is empty | `false` |
| **Reset strategy** | `ROLLING` starts the window at the consumer's first request. `CALENDAR` aligns every consumer to the same clock boundary | `ROLLING` |
| **Timezone** | The IANA identifier used for calendar-aligned boundaries, such as `UTC` or `Europe/Paris` | `UTC` |
| **Reservation strategy** | `NONE`, `FIXED`, or `ADAPTIVE`. Decides whether the budget is checked against an estimate before the model is called | `NONE` |
| **Reservation amount (dollars)** | The amount held per request while the model answers. Must be greater than `0` whenever a reservation strategy is set | - |
| **Reservation ceiling (dollars)** | The largest amount `ADAPTIVE` may hold. Leave it empty for no ceiling | - |

A budget of `0` with no dynamic budget is rejected when the API is deployed, so set one or the other.

By default the budget belongs to a plan and subscription pair, not to a caller. When several identities share one subscription, they share one budget, and the first one to spend it exhausts it for everyone. Set **Key** to an expression that resolves the caller's identity, and enable **Use key only**, to give each identity its own budget.

`CALENDAR` only aligns a window that matches a calendar period. Set **Time duration** and **Time unit** to exactly 1 hour, 1 day, 7 days, or 30 days. Any other period is rejected when the API is deployed, so use `ROLLING` instead.

### Reservations

With no reservation, the policy checks the budget against spend already recorded. The real cost of a request is only known after its response has been delivered. One expensive call can therefore overshoot the budget, and concurrent calls can overshoot it together.

Two **Reservation strategy** values hold budget up front. `FIXED` holds **Reservation amount** before the model is called. `ADAPTIVE` starts from that amount and learns from what the same consumer actually spends, up to **Reservation ceiling**. Either way the reservation is reconciled against the real cost once the response completes, and it's refunded before the rejection when the budget overflows. Estimation accuracy affects only how tightly the budget is held, never the recorded spend, because reconciliation applies the exact difference.

A reservation never exceeds the resolved budget. Enabling a reservation also makes the counter strict, even under `ASYNC_MODE`. Adaptive estimates are held per gateway node and are lost on restart, so keep **Reservation amount** meaningful on its own.

When a response is served from a semantic cache the model is never called, so no cost is recorded and any reservation is released.

### Missing price policy

**Missing price policy** decides what a request costs when a model answered but carried no price. The price is only known after the answer, so neither option can reject the request in front of you. Both decide what the next request sees:

| Setting | Description | Default |
| --- | --- | --- |
| **Missing price policy** | `FAIL_OPEN` records nothing and releases any reservation. `FAIL_CLOSED` charges the fallback cost | `FAIL_OPEN` |
| **Fallback cost when price is unknown (dollars)** | The amount charged per request under `FAIL_CLOSED`. Enter `0.05` for five cents | - |

Under `FAIL_CLOSED`, set a fallback cost unless a reservation strategy is configured. Without either, `FAIL_CLOSED` charges nothing and behaves like `FAIL_OPEN`.

A model priced at `0` is free, is billed as `0`, and never reaches this setting.

### Strategy

**Strategy** decides how the counter is kept and what happens when the rate-limit store is unreachable:

| Value | Behavior |
| --- | --- |
| `FALLBACK_PASS_THROUGH` | Counts exactly, so every request checks the counter before it proceeds. If the policy can't reach the rate-limit store, the request is allowed. The default, and the choice when availability matters more than the ceiling |
| `BLOCK_ON_INTERNAL_ERROR` | Counts exactly. If the policy can't reach the rate-limit store, the request is rejected. Choose this when overspending is worse than downtime |
| `ASYNC_MODE` | Counts approximately, buffering counts and flushing them in the background. The fastest option and the lightest on the store, but concurrent requests can pass the budget before the flush catches up |

Because a money budget is the kind of ceiling you don't want overshot, `FALLBACK_PASS_THROUGH` is the default rather than `ASYNC_MODE`.

With `BLOCK_ON_INTERNAL_ERROR`, the rejection reports `Cost rate limit blocked the query due to internal error`. With `FALLBACK_PASS_THROUGH` and with `ASYNC_MODE`, the request is allowed. When **Add response headers** is enabled, `X-Cost-Rate-Limit-Remaining` then reports the full budget and `X-Cost-Rate-Limit-Reset` reports `-1`. If no rate-limit configuration is installed, the request fails with `No rate-limit config has been installed.`

### Response headers

Enable **Add response headers** to return the consumer's budget on every response:

| Header | Content |
| --- | --- |
| `X-Cost-Rate-Limit-Limit` | The configured budget |
| `X-Cost-Rate-Limit-Remaining` | Budget left in the current period |
| `X-Cost-Rate-Limit-Reset` | When the budget resets |

These let a well-behaved client back off before it's rejected, rather than discovering the budget through a `429`.

## Verification

Send requests until the budget is exhausted, with a budget low enough that a few calls reach it:

```bash
curl -X POST \
  https://<GATEWAY_URL>/<CONTEXT_PATH>/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "<MODEL_ID>",
    "messages": [
      {"role": "user", "content": "Hello"}
    ]
  }'
```

* Replace `<GATEWAY_URL>` with your AI Gateway URL.
* Replace `<CONTEXT_PATH>` with the context path of your LLM Proxy.
* Replace `<MODEL_ID>` with a model the proxy serves.

The call that exceeds the budget is rejected:

```json
{
  "message": "Cost budget exceeded! Limit is $5 per 1 days. Current spend: $5.12.",
  "http_status_code": 429
}
```

## Next steps

* [Add the Token Rate Limit policy](add-the-token-rate-limit-policy.md). Cap tokens as well as dollars on the same flow.
* [Configure an LLM Proxy](configure-an-llm-proxy.md). Add guardrails, PII filtering, and security plans.
* [Publish your LLM Proxy](../publish/publish-your-llm-proxy.md). Make the proxy available to consumers.
