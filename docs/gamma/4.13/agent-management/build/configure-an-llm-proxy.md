---
hidden: false
noIndex: false
description: Configure guardrails, PII filtering, rate limiting, security plans, and structured output on an LLM Proxy. Follow the steps to add each policy.
---

# Configure an LLM Proxy

After you create an LLM Proxy, configure guardrails, PII filtering, rate limiting, security plans, and policies. This page covers the post-creation configuration options.

## Guardrails, PII filtering, and rate limiting

Guardrails, PII filtering, and rate limiting are implemented using standard Gravitee policies. You configure them by attaching policies with the LLM Studio.

The LLM Studio uses the same policy studio as API Management and supports the request and response phases. To attach these controls, complete the following steps:

1. On the LLM Proxy detail page, under **Design**, open **LLM Studio**.
2. Under **Common Flows**, select the flow you want to govern: **Prompt**, **Embeddings**, or **Models**.
3. In the **Request Phase** or **Response Phase** section, click **Browse all...** to open the policy catalog. The **+ Security** and **+ Transformation** buttons open the same catalog filtered to that category.
4. In the **Add Policy** panel, search for the policy you want, such as **PII Filtering**, **Rate Limit**, or **AI - Prompt Guard Rails**, and then click **Add to flow**.
5. Configure the policy properties, and then click **Save**.
6. When the "This deployable is out of sync" message appears, click **Deploy** to push the changes to the API Gateway.

## Resources

Policies that depend on shared infrastructure reference a resource configured on the proxy. The **AI - Prompt Guard Rails** policy references an **AI Model Text Classification** resource, and the **PII Filtering** policy references an **AI Model Token Classification** resource.

To manage the resources of the LLM Proxy, under **Design**, select **Resources**. For the steps to add, edit, or remove a resource, see [Configure resources for your proxies](configure-resources-for-your-proxies.md), and for the resource types themselves, see [AI resources](ai-resources.md).

## Structured output

Structured output enforces response format constraints on model responses. You can enforce structured output natively by overriding model parameters.

When you add a provider or a model to the LLM Proxy, you can supply a JSON object in the **Parameters override** field. This field supports Expression Language, and the evaluated result must be a JSON object. The connector merges the object into each request before it reaches the upstream provider, so you can transparently enforce formatting such as `{"response_format": { "type": "json_object" }}`. In the LLM Proxy definition, this field is `parametersOverride`.

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

## Broadcasts

To send a one-way announcement to the consumers of the LLM Proxy, under **Consumer Access**, select **Broadcasts**. For the steps to compose and send one, see [Broadcast messages to proxy consumers](broadcast-messages-to-proxy-consumers.md).

## Cost visibility

The LLM Proxy provides real-time per-token cost attribution by provider and model. Every request records the model used, the input and output tokens consumed, and the cost based on the model's configured rate.

The **LLM — Overview** dashboard visualizes this data. It tracks `LLM_PROMPT_TOKEN_TOTAL_COST` alongside widgets such as **Requests by Provider** and **Tokens by Model**.

## Next steps

* [Create an LLM Proxy](create-an-llm-proxy.md). Create a new LLM Proxy if you haven't already.
* [Configure LLM Proxy logging and tracing](configure-llm-proxy-logging-and-tracing.md). Control the reported request and response data, and enable OpenTelemetry tracing.
* [Publish your LLM Proxy](../publish/publish-your-llm-proxy.md). Make the LLM Proxy discoverable.
* [Monitor AI Gateway usage from employee systems](../observe/monitor-ai-gateway-from-devices.md). View AI traffic from employee devices.
