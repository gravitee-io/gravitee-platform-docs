---
hidden: false
noIndex: false
---

# Create your LLM Proxy
<!-- GAP-STRUCTURAL: Missing procedural content source -->


This quickstart walks you through creating an LLM Proxy, connecting it to an upstream model provider, and sending a test prompt through the AI Gateway. You'll use the simplest configuration — a single model with API key authentication and a keyless consumer plan — to get a working LLM Proxy in under five minutes.

{% hint style="info" %}
The Gamma console refers to the LLM Proxy creation flow as the **LLM Router wizard**. The Router is the routing configuration of your LLM Proxy — they are the same artifact. For a complete reference on all configuration options, see [Create an LLM Proxy](../build/create-an-llm-proxy.md).
{% endhint %}

## Prerequisites

* Access to a running Gamma console instance
* An API key for an upstream model provider (e.g., Anthropic, OpenAI, Google, AWS Bedrock, Azure)

## Step 1: Open the LLM Proxy wizard

1. From the Gamma console sidebar, select **Agent Management**.
2. Navigate to **Build**.
3. Select **Create LLM Proxy**.

The console opens the LLM Router wizard.

## Step 2: Configure the model

The first wizard step connects the LLM Proxy to an upstream model provider.

| Field              | Value                                              | Notes                                                                                                |
| ------------------ | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Provider**       | Select your model provider (e.g., Anthropic)       | Required. The LLM Proxy supports Anthropic, OpenAI, Bedrock, Vertex AI, and Azure.                   |
| **Model**          | Select the specific model (e.g., Claude Sonnet)    | Required. Available models depend on the selected provider.                                          |
| **Authentication** | Choose **API Key** and enter your provider API key | Required. You can authenticate with an API key or bearer token. For this quickstart, use an API key. |

Select **Next** to proceed.

## Step 3: Set the context path

The second wizard step defines how consumers reach the LLM Proxy.

| Field            | Value                | Notes                                                                                         |
| ---------------- | -------------------- | --------------------------------------------------------------------------------------------- |
| **Context path** | `/my-llm-proxy`      | Required. The path segment appended to the AI Gateway URL that consumers use to send prompts. |
| **Proxy name**   | `My First LLM Proxy` | Required. Identifies this LLM Proxy in the console.                                           |

Select **Next** to proceed.

## Step 4: Select a consumer plan

The third wizard step controls how consumers authenticate when sending prompts through the LLM Proxy.

For this quickstart, select **Keyless**. A keyless plan requires no consumer authentication — any client can send prompts without credentials. This is the fastest way to verify your proxy works.

{% hint style="warning" %}
Keyless plans are intended for testing. For production use, select an API Key plan to track usage per consumer, enforce rate limits, and attribute costs. See [Configure an LLM Proxy](../build/configure-an-llm-proxy.md).
{% endhint %}

Select **Next** to proceed.

## Step 5: Review and create

Review the LLM Proxy configuration — provider, model, authentication, context path, and consumer plan — then select **Create**.

The console creates the LLM Proxy and deploys it to the AI Gateway.

## Step 6: Send a test prompt

Once the LLM Proxy is deployed, send a test prompt to confirm it works:

```bash
curl -X POST https://<your-gateway-host>/my-llm-proxy/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 256,
    "messages": [{"role": "user", "content": "Hello, world"}]
  }'
```

A successful response returns the model's reply, confirming that the AI Gateway is routing prompts through your LLM Proxy to the upstream provider.

## Next steps

* **Add more models** — Configure additional providers and routing strategies to distribute traffic. See [Configure an LLM Proxy](../build/configure-an-llm-proxy.md).
* **Secure with an API key plan** — Replace the keyless plan with an API key to track usage and enforce rate limits.
* **Route Claude Code through the proxy** — Set `ANTHROPIC_BASE_URL` to point at your LLM Proxy for zero-code integration. See [Connect Claude Code to the Edge Daemon](../edge-daemon/connect-claude-code-to-daemon.md).
* **Publish** — Make the LLM Proxy discoverable. See [Publish your LLM Proxy](../publish/publish-your-llm-proxy.md).
