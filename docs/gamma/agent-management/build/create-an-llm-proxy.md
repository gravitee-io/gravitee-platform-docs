---
hidden: false
noIndex: true
---

# Create an LLM Proxy

An LLM Proxy routes traffic to upstream model providers (Anthropic, OpenAI, Bedrock, Vertex AI, Azure) through the AI Gateway, adding authentication, cost attribution, observability, guardrails, and fine-grained authorization to every model call.

{% hint style="info" %}
The Gamma console refers to the LLM Proxy creation flow as the **LLM Router wizard**. The Router is the routing configuration of your LLM Proxy — they are the same artifact. For a simplified quickstart, see [Create your LLM Proxy](../get-started/create-your-llm-proxy.md).
{% endhint %}

## Step 1: Open the LLM Proxy wizard

1. From the Gamma console sidebar, select **Agent Management**.
2. Navigate to **Build**.
3. Select **Create LLM Proxy**.

The console opens the LLM Router wizard.

## Step 2: Configure the model

The LLM Proxy supports two modes for selecting upstream models:

**Inline mode** — Configure the provider and model directly in the wizard:

<!-- Source: src/main/ui/app/features/secure/pages/llm-router-create/Step1Models.tsx -->
| Field                     | Required | Description                                                                                                      |
| ------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------- |
| **Provider**              | Yes      | The upstream model format (`OPEN_AI`, `GEMINI`, `ANTHROPIC`, or `BEDROCK`).                                      |
| **Model**                 | Yes      | The specific model to route traffic to, its aliases, and pricing (input/output per M tokens).                    |
| **Authentication method** | Yes      | How the LLM Proxy authenticates with the upstream provider. Options: **None**, **API key** (custom header), **Bearer token**, or **Service account**. |
| **Credentials**           | Depends  | The API key or bearer token for the selected provider. Not required if authentication is set to None.            |

**Catalog mode** — Select models already registered in the AI Models catalog:

1. Select **Use Catalog** to browse registered providers.
2. Select a provider to view its available models.
3. The provider name, target URL, and authentication type are pre-populated from the catalog entry.
4. Enter the provider-specific credentials (e.g., API key) — these are not stored in the catalog and must be supplied per LLM Proxy.

{% hint style="info" %}
You can configure multiple models on a single LLM Proxy to enable routing strategies like cost-based or latency-based routing. See [Configure an LLM Proxy](configure-an-llm-proxy.md) for post-creation routing configuration.
{% endhint %}

## Step 3: Set the context path and name

| Field            | Required | Description                                                                                                 |
| ---------------- | -------- | ----------------------------------------------------------------------------------------------------------- |
| **Proxy name**   | Yes      | A human-readable name that identifies this LLM Proxy in the console.                                        |
| **Context path** | Yes      | The path segment appended to the AI Gateway URL that consumers use to send prompts (e.g., `/my-llm-proxy`). |

## Step 4: Select a consumer plan

<!-- Source: src/main/ui/app/components/create-plan/types.ts -->
Choose how consumers authenticate when sending prompts through this LLM Proxy. The LLM Proxy supports the standard Gravitee API plan types:

| Plan type   | Description                                                                                       |
| ----------- | ------------------------------------------------------------------------------------------------- |
| **API Key** | (`API_KEY`) Consumers include an API key. Enables per-consumer tracking, rate limiting, and cost attribution. |
| **Keyless** | (`KEY_LESS`) No consumer authentication. Any client can send prompts without credentials.                      |
| **OAuth2**  | (`OAUTH2`) Validates OAuth2 access tokens from an identity provider. |
| **JWT**     | (`JWT`) Validates JSON Web Tokens locally without a network hop to the IdP. |
| **mTLS**    | (`MTLS`) Validates the consumer's mutual TLS certificate. |

{% hint style="warning" %}
Keyless plans provide no consumer identification. You cannot track usage per consumer, enforce per-consumer rate limits, or attribute costs. Use keyless only for internal testing.
{% endhint %}

## Step 5: Review and create

Review the LLM Proxy configuration — provider, model, authentication, context path, and consumer plan — then select **Create**.

The console creates the LLM Proxy and deploys it to the AI Gateway. All consumer traffic to this context path now flows through the AI Gateway with the configured authentication and observability.

## Zero-code integration

The LLM Proxy is API-compatible with the Anthropic and OpenAI Messages APIs. You can route existing AI tool traffic through the proxy by setting environment variables — no code changes required:

```bash
export ANTHROPIC_BASE_URL=https://<your-gateway-host>/my-llm-proxy
export OPENAI_BASE_URL=https://<your-gateway-host>/my-llm-proxy
```

This is the recommended path for routing Claude Code, Cursor, and other development tools through governance.

## After creation

* **Configure routing** — Add models and routing strategies. See [Configure an LLM Proxy](configure-an-llm-proxy.md).
* **Publish** — Make the LLM Proxy discoverable. See [Publish your LLM Proxy](../publish/publish-your-llm-proxy.md).
* **Route through Edge Daemon** — For employee device traffic, route through Edge Management. See [Connect Claude Code to the Edge Daemon](../edge-daemon/connect-claude-code-to-daemon.md).
