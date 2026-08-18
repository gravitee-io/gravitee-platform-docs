---
hidden: false
noIndex: false
description: Add the Token Rate Limit policy to an LLM Proxy to cap the tokens a consumer spends over a rolling period. Follow the steps to configure it.
---

# Add the Token Rate Limit policy

A request rate limit counts calls. It doesn't tell you what those calls cost, because one prompt can consume a hundred tokens and the next can consume a hundred thousand. The **Token Rate Limit** policy counts tokens instead, so the budget you set is the budget the provider bills you for.

The policy counts input and output tokens together against a single allowance over a rolling period, and returns `429` once a consumer exceeds it.

## Prerequisites

Before you begin, confirm that you have the following:

* A self-hosted or hybrid Gamma installation. For more information, see [Self-hosted installation guides](../../platform-management/install/self-hosted-installation-guides/README.md) and [Hybrid installation guides](../../platform-management/install/hybrid-installation-guides/README.md).
* A deployed LLM Proxy. For more information, see [Create an LLM Proxy](create-an-llm-proxy.md).

## Add the policy

1. On the LLM Proxy detail page, under **Design**, open **LLM Studio**.
2. Under **Common Flows**, select the flow you want to limit, usually **Prompt**.
3. In the **Request Phase** section, click **Browse all...** to open the policy catalog.
4. Search for **Token Rate Limit**, and then click **Add to flow**.
5. Configure the policy using the settings described below.
6. Click **Save**.
7. When the "This deployable is out of sync" message appears, click **Deploy** to push the change to the AI Gateway.

## Settings

### Apply rate-limiting

| Setting | Description | Default |
| --- | --- | --- |
| **Max tokens (static)** | The number of tokens allowed per period. Used when the value is greater than `0` | - |
| **Max tokens (dynamic)** | An Expression Language expression that resolves to the limit. Used only when the static limit is `0` | - |
| **Time duration** | How long before the allowance resets | `1` |
| **Time unit** | `SECONDS` or `MINUTES` | `SECONDS` |
| **Key** | Identifies the consumer the limit applies to. Supports Expression Language. Leave it empty to count against the plan and subscription pair | Empty |
| **Use key only** | Counts against the key alone, ignoring the subscription and plan | `false` |
| **Reset strategy** | `ROLLING` starts the window at the first request. `CALENDAR` aligns the boundary to the calendar hour, day, week, or month | `ROLLING` |
| **Timezone** | The IANA identifier used for calendar-aligned boundaries, such as `UTC` or `Europe/Paris` | `UTC` |
| **Reservation strategy** | `NONE`, `FIXED`, or `ADAPTIVE`. Decides whether the budget is checked against an estimate before the model is called | `NONE` |
| **Reservation amount (tokens)** | The number of tokens reserved per request, for example `4000` | `0` |
| **Reservation ceiling (tokens)** | Bounds an adaptive reservation. `0` disables the ceiling | `0` |

By default the allowance belongs to a plan and subscription pair, not to a caller. When several identities share one subscription, they share one budget, and the first one to spend it exhausts it for everyone. Set **Key** to an expression that resolves the caller's identity, and enable **Use key only**, to give each identity its own allowance.

For longer windows, **Time unit** also accepts `HOURS` and `DAYS`.

With no reservation, the policy checks the limit against tokens already recorded, and the real usage of a request is only known after its response has been delivered. One large prompt can therefore overshoot the budget, and concurrent calls can overshoot it together. Set **Reservation strategy** to `FIXED` to reserve **Reservation amount** tokens before the model is called, or to `ADAPTIVE` to start from that amount and learn from what the same consumer actually spends, up to **Reservation ceiling**. Either way the reservation is reconciled against real usage once the response completes, and it's refunded before the rejection when the budget overflows. A reservation never exceeds the resolved limit, and a request that never reports usage, such as a client disconnect, is still charged. Enabling a reservation also makes the counter strict, even under `ASYNC_MODE`.

When a response is served from cache the model is never called, so the request counts as zero and any reservation is released. When token usage isn't available, the request is allowed and the budget isn't incremented.

### Strategy

**Strategy** decides how the policy executes and what happens when the rate-limit store is unreachable:

| Value | Behavior |
| --- | --- |
| `ASYNC_MODE` | The counter is updated asynchronously. The fastest option, and the default. Under bursts, a consumer can slightly overshoot the limit before the counter catches up |
| `BLOCK_ON_INTERNAL_ERROR` | If the policy can't reach the rate-limit store, the request is rejected. Choose this when overspending is worse than downtime |
| `FALLBACK_PASS_THROUGH` | If the policy can't reach the rate-limit store, the request is allowed. Choose this when availability matters more than the ceiling |

With `BLOCK_ON_INTERNAL_ERROR`, the rejection reports `Token rate limit blocked the query due to internal error`. With `FALLBACK_PASS_THROUGH` and with `ASYNC_MODE`, the request is allowed and the response headers report a counter of `0` and a reset of `-1`. If no rate-limit configuration is installed, the request fails with `No rate-limit config has been installed.`

### Response headers

Enable **Add response headers** to return the consumer's budget on every response:

| Header | Content |
| --- | --- |
| `X-Token-Rate-Limit-Limit` | The configured allowance |
| `X-Token-Rate-Limit-Remaining` | Tokens left in the current period |
| `X-Token-Rate-Limit-Reset` | When the allowance resets |

These let a well-behaved client back off before it's rejected, rather than discovering the limit through a `429`.

## Verify the limit

Send the same request twice, with a limit low enough that one call exhausts it:

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

The second call is rejected:

```json
{
  "message": "Rate limit exceeded! You reached the limit of 100 tokens per 1 minutes",
  "http_status_code": 429
}
```

## Next steps

* [Configure an LLM Proxy](configure-an-llm-proxy.md). Add guardrails, PII filtering, and security plans.
* [Publish your LLM Proxy](../publish/publish-your-llm-proxy.md). Make the proxy available to consumers.
