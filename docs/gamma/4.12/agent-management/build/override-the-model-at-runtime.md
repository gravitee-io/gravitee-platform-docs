---
hidden: false
noIndex: false
description: Route a request to a different model than the client asked for by setting a context attribute on an LLM Proxy flow. Follow the steps to override it.
---

# Override the model at runtime

An LLM Proxy routes each request to the model the client asks for. To send it somewhere else without changing the client, set the `llmproxy.model.override` context attribute in the request phase of a flow. When the attribute is set, the proxy uses its value in place of the model in the request, routes to the endpoint that serves that model, and calls the provider with it.

This is how you move traffic between models without touching the applications that consume the proxy — pinning an expensive model down to a cheaper one, steering a tenant to a regional deployment, or shifting traffic during a provider incident.

The proxy resolves the override as follows:

* If the client prefixes the model with an endpoint or endpoint group name, for example `llmtest:gpt-5-mini`, the prefix still applies. The override replaces only the model name after the prefix.
* If the attribute isn't set, the proxy uses the model from the client request.

<!-- TODO: the APIM page states that an override naming a model no endpoint serves returns 400 with error code model_not_found. That behavior did not reproduce on a proxy configured with NO_PREFIX model governance, so the claim is left out here pending a check against the PREFIXED_* and alias-only settings. -->

## Prerequisites

Before you begin, confirm that you have the following:

* A deployed LLM Proxy with more than one model available. For more information, see [Create an LLM Proxy](create-an-llm-proxy.md).

## Set the override attribute

1. On the LLM Proxy detail page, under **Design**, open **LLM Studio**.
2. Under **Common Flows**, select the flow the override applies to, usually **Prompt**.
3. In the **Request Phase** section, click **Browse all...** to open the policy catalog.
4. Search for **Assign attributes**, and then click **Add to flow**.
5. In the **Assign context attributes** section, add an attribute:
   1. In the **Name** field, enter `llmproxy.model.override`.
   2. In the **Value** field, enter the name of the model to use, or an Expression Language expression that resolves to it.
6. Click **Save**.
7. When the "This deployable is out of sync" message appears, click **Deploy** to push the change to the AI Gateway.

## Resolve the model at runtime

The **Value** field supports Expression Language, so the target model can be decided per request. To select it from a request header:

```text
{#request.headers['x-target-model'][0]}
```

{% hint style="warning" %}
Index the header value with `[0]`. Request headers are a multi-value map, so `{#request.headers['x-target-model']}` on its own resolves to a list rather than a string, and the request fails with a `500` response.
{% endhint %}

When the expression resolves to nothing — the header is absent, for example — no override is applied and the proxy uses the model from the client request. That makes a header-driven override safe to leave in place: clients that don't send the header are unaffected.

## Verify the override

Call the proxy asking for one model, with the override configured to send it to another:

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

Check the `model` field of the response. It reports the model that answered, which is the override model rather than the one you asked for.

If the proxy is configured with `injectTokenHeaders` enabled, the `X-LLM-Proxy-Model` response header also carries the model the proxy resolved. See [Accepted request formats](accepted-request-formats.md) for the other token usage headers.

## Next steps

* [Configure an LLM Proxy](configure-an-llm-proxy.md). Add guardrails, PII filtering, and rate limiting to the same flow.
* [LLM Proxy provider support](llm-proxy-provider-support.md). Check which providers and models a proxy can route to.
