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

Then add at least one provider with at least one model. You can add a provider inline or import models from the catalog. From Gamma 4.12.17, both cards render the configuration schema of the LLM Proxy endpoint plugin, with the labels and help text the plugin ships. A field that a later plugin version adds appears on the card without a console update. Until the schema is loaded, **Add provider** stays disabled.

#### Add a provider inline

To add a provider inline, select **Add provider**. On the **New provider** card, enter a **Provider name** that no other inline provider of the proxy uses, and then complete the fields of the plugin. With the plugin version bundled in Gamma 4.12.17 and later, the card carries the following fields.

| Field                  | Description |
| ---------------------- | ----------- |
| **Provider**           | The API format of the upstream provider: **OpenAI**, **OpenAI compatible**, **Gemini**, **Bedrock**, **Anthropic**, or **Vertex AI**. **OpenAI** is preselected. |
| **Provider URL**       | The URL the proxy calls, without whitespace. The field accepts Expression Language and secret references. |
| **Models**             | The models the provider serves, at least one. Select **Add** to add an entry, and enter the **Model** name. Optionally, add an **Entity ID**, the catalog entity ID of the model used for fine-grained authorization. Add the **Price per million tokens (input) sent to LLM ($)** and the **Price per million tokens (output) received from LLM ($)**. Add one or more **Aliases of this model**, and a **Parameters Override (JSON)**. Model names are unique within the provider, an alias can't contain `:`, and a price is greater than `0`. |
| **ModelGovernance**    | Select the **Alias** or the **Unregistered models** variant. Both carry **Prefix needs**. The options are **Models and aliases require the prefix**, the default, **Only aliases require the prefix**, **Only models require the prefix**, and **Models and aliases do not require a prefix**. **Alias** adds the **Only use alias** switch, which hides the real model names so that consumers use the aliases only. **Unregistered models** adds **Globbing to accept unregistered models**, a required pattern such as `*` for any model, `gpt*`, or `(opus\|haiku\|sonnet)*`. |
| **Authentication**     | **API Key**, **Bearer**, **Service account (GCP)**, or **None**. **API Key** takes the **Header name containing the API Key**, `x-api-key` by default, and the **API Key**. **Bearer** takes the **Bearer** token. **Service account (GCP)** takes the **Service Account Key (JSON)** in a code editor. The key and token fields accept Expression Language and secret references. |
| **Vertex AI Settings** | Shown for the **Vertex AI** provider only: the **GCP Project ID**, the **GCP Region**, `global` by default, and the **Publisher**, **Google (Gemini)** or **Anthropic (Claude)**. |

The card checks each field against the plugin schema as you type. **Add provider** at the bottom of the card stays disabled until the name and every field are valid. Select it to add the provider, or **Cancel** to drop the card. The added provider is listed with its models, and its bin icon removes it.

<!-- TODO: Screenshot of the New provider card of the Models step on a Gamma 4.12.19 stack, with the Provider, Provider URL, Models, and Authentication fields filled for an Anthropic provider -->
<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-aim-llm-proxy-new-provider.png" alt=""><figcaption><p>The New provider card of the Models step</p></figcaption></figure>

{% hint style="info" %}
The console keeps the API key, bearer token, or service account key as you enter it. The value is shown again when you edit the provider on the **Models** page of the proxy. For the API key and the bearer token, enter a secret reference in the field instead to keep the secret out of the proxy configuration.
{% endhint %}

#### Import models from the catalog

To import registered models instead, select **Add models from catalog** and complete the following steps:

1. Browse the registered providers, select one to view its available models, and then pick the models to import. The catalog source holds the provider's format, URL, and authentication type, so the card that opens asks only for what the source doesn't hold.
2. Under **Credentials**, enter the secret the authentication type of the source needs, for example the **API Key**. Credentials aren't stored in the catalog, so supply them for each LLM Proxy.
3. Optionally, set the model governance as for an inline provider, and for each picked model the **Aliases of this model** and the **Parameters Override (JSON)**. When **Only use alias** is on, every model needs at least one alias.
4. Select **Add provider**.

In the **Details** section of the same step, give the proxy a **Proxy name**, and optionally a **Version number** and **Description**. The **Entity ID** is generated from the name.

{% hint style="info" %}
You can configure multiple providers and models on a single LLM Proxy, and change them after creation on the **Models** page. See [Configure an LLM Proxy](configure-an-llm-proxy.md#models).
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
