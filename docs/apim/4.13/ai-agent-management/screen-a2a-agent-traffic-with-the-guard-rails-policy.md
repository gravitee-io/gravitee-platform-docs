---
description: Learn how to apply the Guard Rails policy to agent-to-agent traffic carried on a plain proxy API, by pointing the policy at the instruction inside the A2A envelope.
---

# Screen A2A agent traffic with the Guard Rails policy

## Overview

An A2A agent-to-agent request carries its instruction inside a JSON-RPC envelope, not as a flat prompt. A `message/send` call places the user's words at `params.message.parts[0].text`, several levels deeper than a typical LLM request body. The Guard Rails policy's `promptLocation` field accepts an Expression Language (EL) expression, so you can point it at that exact path and screen the instruction inside the envelope instead of the envelope itself.

This works on a plain `PROXY` API. You don't need the `A2A_PROXY` API type to apply the policy to agent-to-agent traffic. For what the `A2A_PROXY` type adds instead, see [A2A Proxy API Type Overview](../create-and-configure-apis/gravitee-api-definitions/a2a-proxy-api-type.md "mention").

## Prerequisites

Before you begin, confirm that you have the following:

* A fully Self-Hosted Installation of APIM or a Hybrid Installation of APIM. For more information about installing APIM, see [self-hosted-installation-guides](../self-hosted-installation-guides/ "mention") and [hybrid-installation-and-configuration-guides](../hybrid-installation-and-configuration-guides/ "mention").
* An Enterprise License. For more information about obtaining an Enterprise license, see [enterprise-edition.md](../introduction/enterprise-edition.md "mention").
* A proxy API in front of an A2A agent that accepts JSON-RPC `message/send` requests.
* Sufficient Java heap on the Gateway to load the selected text classification model, and the Debian-based Gateway image rather than the default Alpine-based image, since Alpine doesn't support the ONNX Runtime. For more information, see [Guard Rails policy reference](../create-and-configure-apis/apply-policies/policy-reference/ai-prompt-guard-rails.md "mention").

## Set the prompt location for a JSON-RPC envelope

1. Add an **AI Model Text Classification** resource to your API, and select a Llama Prompt Guard model.
2. Add the **Guard Rails** policy to the API's request flow.
3. Set **Prompt Location** to an EL expression that reaches into the envelope:

```
{#request.content.contains('"params"')
  ? #jsonPath(#request.content, '$.params.message.parts[0].text')
  : #jsonPath(#request.content, '$.message')}
```

This ternary checks whether the body carries a `params` block. If it does, the request is a JSON-RPC A2A envelope, and the expression pulls the instruction from `params.message.parts[0].text`. If it doesn't, the expression falls back to a flat `{"message": "..."}` shape. Adjust the fallback branch, or remove it, to match the request shapes your own API actually receives.

4. Set **Content Checks** to `MALICIOUS` to match against the Llama Prompt Guard model's output label, or leave it empty to evaluate every label the model returns.
5. Set **Request Policy** to `BLOCK_REQUEST` to reject a flagged request at the gateway, or `LOG_REQUEST` to allow it through and log the result.

{% hint style="warning" %}
An A2A message can carry more than one entry in its `parts` array. The expression above reads only `parts[0]`, so content placed in a second or later part isn't screened by this policy. Pair it with a policy that inspects the whole payload, such as JSON Threat Protection, if your agents can receive multi-part messages.
{% endhint %}

## Order this policy after payload validation

Run cheaper, deterministic checks before the Guard Rails policy, not after. A classification model call has a real cost per request, and a request an earlier policy would have rejected anyway, such as a malformed or oversized payload, shouldn't reach the model first. Place JSON Threat Protection and any request validation policies earlier in the flow than the Guard Rails policy.

## Next steps

* [A2A Proxy API Type Overview](../create-and-configure-apis/gravitee-api-definitions/a2a-proxy-api-type.md "mention"). The `A2A_PROXY` API type rewrites the agent card's advertised URL to the gateway's own on a card fetch, for both the `url` field and the `supportedInterfaces` array. It doesn't route by JSON-RPC method or by the card's `skills` array.
* [JSON Threat Protection](../create-and-configure-apis/apply-policies/policy-reference/json-threat-protection.md "mention"). This policy screens the request payload's structure before it reaches your agent or an AI classification model.
