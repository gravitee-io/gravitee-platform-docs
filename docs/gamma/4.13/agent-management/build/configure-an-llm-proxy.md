---
hidden: false
noIndex: false
---

# Configure an LLM Proxy


After creating an LLM Proxy, configure guardrails, PII filtering, rate limiting, security plans, and policies. This page covers all post-creation configuration options.

## Guardrails, PII filtering, and Rate limiting

<!-- Source: src/main/ui/app/features/secure/pages/llm-router-detail/llm-studio/LlmStudioPage.tsx -->
Guardrails, PII filtering, and rate limiting are implemented using standard Gravitee policies. You configure them by attaching policies with the LLM Studio.

The LLM Studio operates just like the API Management policy studio, supporting request/response phases. To attach these controls:

1. Navigate to your LLM Proxy detail page and open **LLM Studio**.
2. Click **+** on the request or response flow, and then search for and select the desired policy, such as PII Filtering, Rate Limit, or AI – Prompt Guard Rails, to add it to the flow.
3. Configure the policy properties.
4. Save your flows to apply the changes.

## Structured output

<!-- Source: src/main/ui/lib/api/llm-proxy.types.ts -->
Structured output enforces response format constraints on model responses. You can enforce structured output natively by overriding model parameters.
When configuring a model within the LLM Proxy, you can supply a `parametersOverride` JSON object that supports Expression Language. The connector automatically merges this JSON object into the request payload before it reaches the upstream provider, so you can transparently enforce formatting such as `{"response_format": { "type": "json_object" }}`.

## Security

<!-- Source: src/main/ui/app/components/create-plan/types.ts -->
Security plans control how consumers authenticate when sending prompts through the LLM Proxy. You can add, modify, or replace plans after creation.

To manage security plans:

1. Navigate to the LLM Proxy detail page.
2. Open the **Plans** section.
3. Add a new plan or modify an existing one.

The LLM Proxy supports the following comprehensive plan types, the same as those available for API proxies:
* **Keyless** (`KEY_LESS`)
* **API Key** (`API_KEY`)
* **OAuth2** (`OAUTH2`)
* **JWT** (`JWT`)
* **mTLS** (`MTLS`)

See [Secure your API proxy](../../api-management/build/secure-your-api-proxy.md) for detailed plan type descriptions.

## Cost visibility

<!-- Source: src/main/ui/config/templates/llm.template.ts -->
The LLM Proxy provides real-time per-token cost attribution by provider and model. Every request records the model used, the input and output tokens consumed, and the cost based on the model's configured rate.

This data is visualized in the **LLM — Overview** dashboard, which tracks `LLM_PROMPT_TOKEN_TOTAL_COST` alongside metrics like Requests by Provider and Tokens by Model.

## Next steps

* [Create an LLM Proxy](create-an-llm-proxy.md): Create a new LLM Proxy if you haven't already.
* [Publish your LLM Proxy](../publish/publish-your-llm-proxy.md): Make the LLM Proxy discoverable.
* [Monitor AI Gateway usage from employee systems](../observe/monitor-ai-gateway-from-devices.md): View AI traffic from employee devices.
