---
hidden: false
noIndex: false
description: Create an LLM Proxy that routes traffic to upstream model providers through the AI Gateway. Follow the steps in the wizard to configure and deploy it.
---

# Create an LLM Proxy

An LLM Proxy routes traffic to upstream model providers—OpenAI, Gemini, Anthropic, Bedrock, and Vertex AI—through the AI Gateway. It adds authentication, cost attribution, observability, guardrails, and fine-grained authorization to every model call.

{% hint style="info" %}
For a simplified quickstart, see [Create your first LLM Proxy](../get-started/create-your-llm-proxy.md).
{% endhint %}

## Create the LLM Proxy

To create an LLM Proxy, complete the following steps:

1. [Open the LLM Proxy wizard](#open-the-llm-proxy-wizard)
2. [Configure the models](#configure-the-models)
3. [Set the context path](#set-the-context-path)
4. [Select a consumer plan](#select-a-consumer-plan)
5. [Review and create](#review-and-create)

### Open the LLM Proxy wizard

1. From the Gamma console sidebar, select **Agent Management**.
2. Under **Secure**, select **LLM Proxies**.
3. Select **Create LLM proxy**.

The console opens the **Create an LLM proxy** wizard, which has four steps: **Models**, **Entrypoint**, **Plans**, and **Review & create**.

### Configure the models

On the **Models** step, first choose a proxy type. Select **Universal LLM Proxy** to aggregate models from multiple providers behind one endpoint that speaks the OpenAI, Anthropic, and Gemini APIs.

Then add at least one provider with at least one model. You can add a provider inline or import models from the catalog.

To add a provider inline, select **Add provider** and complete the following fields:

| Field              | Required | Description                                                                                                      |
| ------------------ | -------- | ---------------------------------------------------------------------------------------------------------------- |
| **Provider name**  | Yes      | A label that identifies this upstream provider, for example, `OpenAI`.                                          |
| **Request format** | Yes      | The upstream provider's API format: **OpenAI**, **Gemini**, **Anthropic**, **Bedrock**, or **Vertex AI**.        |
| **Target URL**     | Yes      | The provider's API base URL, for example, `https://api.openai.com/v1`.                                          |
| **Authentication** | Yes      | How the LLM Proxy authenticates with the upstream provider, and the credentials it uses: **No authentication**, **API key (custom header)**, or **Bearer token**. The **Vertex AI** request format instead requires a **Service account**. |
| **Model name**     | Yes      | The specific model to route traffic to. You can also add aliases and per-model pricing, that is, the input and output price per million tokens. |

To import registered models instead, select **Add models from catalog** and complete the following steps:

1. Browse the registered providers and select one to view its available models. The provider name, target URL, and authentication type are pre-populated from the catalog entry.
2. Enter the provider-specific credentials, for example, an API key. Credentials aren't stored in the catalog, so supply them for each LLM Proxy.

In the **Details** section of the same step, give the proxy a **Proxy name**, and optionally a **Version number** and **Description**. The **Entity ID** is generated from the name.

{% hint style="info" %}
You can configure multiple providers and models on a single LLM Proxy. See [Configure an LLM Proxy](configure-an-llm-proxy.md) for post-creation configuration options.
{% endhint %}

### Set the context path

On the **Entrypoint** step, define the public path that consumers call:

| Field            | Required | Description                                                                                                 |
| ---------------- | -------- | ----------------------------------------------------------------------------------------------------------- |
| **Context path** | Yes      | The path prefix appended to the AI Gateway URL that consumers use to send prompts, for example, `/my-llm-proxy`. |

You can also toggle **Track tokens during stream mode** and **Inject token usage headers** to control how token usage is reported.

### Select a consumer plan

On the **Plans** step, select **Add plan** to choose how consumers authenticate when sending prompts through this LLM Proxy. The LLM Proxy supports the standard Gravitee API plan types:

| Plan type   | Description                                                                                       |
| ----------- | ------------------------------------------------------------------------------------------------- |
| **Keyless** | `KEY_LESS`. No consumer authentication. Any client can send prompts without credentials.                      |
| **API Key** | `API_KEY`. Consumers include an API key. Enables per-consumer tracking, rate limiting, and cost attribution. |
| **JWT**     | `JWT`. Validates JSON Web Tokens locally without a network hop to the IdP. |
| **OAuth 2.0** | `OAUTH2`. Validates OAuth2 access tokens from an identity provider. |
| **mTLS**    | `MTLS`. Validates the consumer's mutual TLS certificate. |

{% hint style="warning" %}
Keyless plans provide no consumer identification. You cannot track usage per consumer, enforce per-consumer rate limits, or attribute costs. Use keyless only for internal testing.
{% endhint %}

### Review and create

Review the LLM Proxy configuration—type, providers and models, context path, identity, and plans—and then select one of the following:

* **Create only**. This creates the LLM Proxy without deploying it to the AI Gateway.
* **Create & deploy**. This creates the LLM Proxy and deploys it to the AI Gateway.

After you deploy the LLM Proxy, all consumer traffic to its context path flows through the AI Gateway with the configured authentication and observability.

## Zero-code integration

The LLM Proxy is API-compatible with the Anthropic and OpenAI Messages APIs. You can route existing AI tool traffic through the proxy by setting environment variables, with no code changes required:

```bash
export ANTHROPIC_BASE_URL=https://<your-gateway-host>/my-llm-proxy
export OPENAI_BASE_URL=https://<your-gateway-host>/my-llm-proxy
```

This is the recommended path for routing Claude Code, Cursor, and other development tools through governance. For a full Claude Code walkthrough that keeps the user's own Claude login, see [Connect Claude Code through an LLM Proxy](../publish/connect-claude-code-through-an-llm-proxy.md).

## Next steps

* **Configure your LLM Proxy**. Add guardrails, security plans, and policies. See [Configure an LLM Proxy](configure-an-llm-proxy.md).
* **Publish**. Make the LLM Proxy discoverable. See [Publish your LLM Proxy](../publish/publish-your-llm-proxy.md).
* **Route through Edge Daemon**. For employee device traffic, route through Edge Management. See [Connect Claude Code to the Edge Daemon](../../edge-management/connect-claude-code-to-daemon.md).
