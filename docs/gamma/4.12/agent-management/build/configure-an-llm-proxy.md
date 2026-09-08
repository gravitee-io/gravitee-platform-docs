---
hidden: false
noIndex: false
description: Configure guardrails, PII filtering, rate limiting, security plans, and structured output on an LLM Proxy. Follow the steps to add each policy.
---

# Configure an LLM Proxy

After you create an LLM Proxy, configure guardrails, PII filtering, rate limiting, security plans, and policies. This page covers the post-creation configuration options.

## Models

From Gamma 4.12.19, the **Models** page lists the providers of the LLM Proxy with their models, and changes them after creation. To open it, under **Design**, select **Models**.

Each provider is a collapsible card. Its header shows the provider name, the provider format, the number of models, and **From catalog** when the provider comes from the catalog. Expanded, the card lists the models of the provider.

To change the providers, complete the following steps:

1. Select **Add provider** to add an inline provider, or **Add models from catalog** to pick registered models. The cards are the ones of the creation wizard. See [Configure the models](create-an-llm-proxy.md#configure-the-models).
2. To change a provider, select its edit icon. An inline provider opens in place with its stored values, credentials included, and each valid change is applied to the page as you make it. Select **Done** to close the card, or **Cancel** to restore the values it opened with. A catalog provider opens with its credentials, model governance, and per-model settings, and **Done** applies them.
3. To remove a provider, select its delete icon.
4. Click **Save changes**, or **Discard** to drop every pending change.

While a card is open for editing, the other providers can't be edited or removed. The save bar appears as soon as the page differs from what's saved. **Save changes** stays disabled while the open card holds an invalid value, or while no provider is left, and the bar then reads **Finish editing the provider before saving.** or **At least one provider is required.** A save that fails shows **Failed to save providers** with the reason.

Saving replaces the providers of the proxy without deploying them. The **This deployable is out of sync.** banner appears at the top of the detail view. Click **Deploy** to push the change to the gateway.

When the aliases declared by two providers differ, the page shows **Model aliases differ across providers** with the aliases of each provider. An alias routes, and fails over, only across the providers that declare it, so align the aliases for cross-provider failover. The warning doesn't block saving.

<!-- TODO: Screenshot of the Models page of an LLM Proxy on a Gamma 4.12.19 stack, with one inline provider expanded and the save bar visible after an edit -->
<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-aim-llm-proxy-models-page.png" alt=""><figcaption><p>The Models page of an LLM Proxy</p></figcaption></figure>

## Guardrails, PII filtering, and rate limiting

Guardrails, PII filtering, and rate limiting are implemented using standard Gravitee policies. You configure them by attaching policies with the LLM Studio.

The LLM Studio uses the same policy studio as API Management and supports the request and response phases. To attach these controls, complete the following steps:

1. On the LLM Proxy detail page, under **Design**, open **LLM Studio**.
2. Under **Common Flows**, select the flow you want to govern: **Prompt**, **Embeddings**, or **Models**.
3. In the **Request Phase** or **Response Phase** section, click **Browse all...** to open the policy catalog. The **+ Security** and **+ Transformation** buttons open the same catalog filtered to that category.
4. In the **Add Policy** panel, search for the policy you want, such as **PII Filtering**, **Rate Limit**, or **AI - Prompt Guard Rails**, and then click **Add to flow**.
5. Configure the policy properties, and then click **Save**.
6. When the "This deployable is out of sync" message appears, click **Deploy** to push the changes to the API Gateway.

## Structured output

Structured output enforces response format constraints on model responses. You can enforce structured output natively by overriding model parameters.

When you add a provider or a model to the LLM Proxy, you can supply a JSON object in the **Parameters Override (JSON)** field of the model. This field supports Expression Language, and the evaluated result must be a JSON object. The connector merges the object into each request before it reaches the upstream provider, so you can transparently enforce formatting such as `{"response_format": { "type": "json_object" }}`. In the LLM Proxy definition, this field is `parametersOverride`.

## Security

Security plans control how consumers authenticate when they send prompts through the LLM Proxy. You can add plans after creation.

To add a security plan, complete the following steps:

1. On the LLM Proxy detail page, under **Consumer Access**, open **Plans**.
2. Click **Add plan**.
3. Complete the **General**, **Security**, **Configure**, and **Review** steps of the **Create Plan** wizard.

The LLM Proxy supports the same comprehensive plan types as API proxies. The **Security** step presents the following plan types in this order:

* **Keyless** (`KEY_LESS`)
* **API Key** (`API_KEY`)
* **JWT** (`JWT`)
* **OAuth 2.0** (`OAUTH2`)
* **mTLS** (`MTLS`)

See [Secure your API proxy](../../api-management/build/secure-your-api-proxy.md) for detailed plan type descriptions.

## CORS

From Gamma 4.12.18, the **CORS** page lets browser-based clients on other origins call the LLM Proxy. Enable CORS, then set the allowed origins, methods, and request headers, the exposed response headers, credentials, the preflight cache duration, and whether policies run on preflight requests. To open it, under **General**, select **CORS**. For the steps, see [Configure LLM Proxy CORS](configure-llm-proxy-cors.md).

## Cost visibility

The LLM Proxy provides real-time per-token cost attribution by provider and model. Every request records the model used, the input and output tokens consumed, and the cost based on the model's configured rate.

The **LLM — Overview** dashboard visualizes this data. It tracks `LLM_PROMPT_TOKEN_TOTAL_COST` alongside widgets such as **Requests by Provider** and **Tokens by Model**.

## Next steps

* [Create an LLM Proxy](create-an-llm-proxy.md). Create a new LLM Proxy if you haven't already.
* [Publish your LLM Proxy](../publish/publish-your-llm-proxy.md). Make the LLM Proxy discoverable.
* [Monitor AI Gateway usage from employee systems](../observe/monitor-ai-gateway-from-devices.md). View AI traffic from employee devices.
