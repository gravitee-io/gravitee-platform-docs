---
hidden: false
noIndex: false
---

# Create your LLM Proxy


This quickstart walks you through creating an LLM Proxy, connecting it to an upstream model provider, and sending a test prompt through the AI Gateway. You'll use the simplest configuration, a single model with API key authentication and a keyless consumer plan, to get a working LLM Proxy in under five minutes.

{% hint style="info" %}
For a complete reference on all configuration options, see [Create an LLM Proxy](../build/create-an-llm-proxy.md).
{% endhint %}

## Prerequisites

* Access to a running Gamma console instance
* An API key for an upstream model provider, such as Anthropic, OpenAI, Google, or AWS Bedrock

## Step 1: Open the LLM Proxy wizard

1. From the Gamma console sidebar, select **Agent Management**.
2. Under **Secure**, select **LLM Proxies**.
3. Select **+ Create LLM proxy**.

The console opens the **Create an LLM proxy** wizard, which has four steps: **Models**, **Entrypoint**, **Plans**, and **Review & create**.

## Step 2: Choose the proxy type and add a model

The **Models** step sets the proxy type, connects the LLM Proxy to an upstream model provider, and names the proxy.

1. Under **Choose a proxy type**, select **Universal LLM Proxy**. It aggregates models from multiple providers behind one endpoint that speaks the OpenAI, Anthropic, and Gemini APIs.
2. Under **Models**, select **Add provider**, and then configure the following:

| Field              | Value                                              | Notes                                                                                                |
| ------------------ | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Provider**       | Select your model provider, such as Anthropic       | Required. Route targets are **OpenAI**, **Anthropic**, **Google**, and **AWS Bedrock**.              |
| **Model**          | Enter the model to route to, such as Claude Sonnet  | Required. Available models depend on the selected provider.                                          |
| **Authentication** | Choose **API Key** and enter your provider API key | Required. You can authenticate with an API key or bearer token. For this quickstart, use an API key. |

3. Under **Details**, enter a **Proxy name**, such as `My First LLM Proxy`. The server generates the **Entity ID** from the name and checks that it is still free. **Version number** defaults to `1.0`.

Select **Next** to proceed.

## Step 3: Set the context path

The **Entrypoint** step defines how consumers reach the LLM Proxy.

| Field            | Value                | Notes                                                                                         |
| ---------------- | -------------------- | --------------------------------------------------------------------------------------------- |
| **Context path** | `/my-llm-proxy`      | Required. The path segment appended to the AI Gateway URL that consumers use to send prompts. |

Select **Next** to proceed.

## Step 4: Select a consumer plan

The third wizard step controls how consumers authenticate when sending prompts through the LLM Proxy.

For this quickstart, select **Keyless**. A keyless plan requires no consumer authentication. Any client can send prompts without credentials. This is the fastest way to verify your proxy works.

{% hint style="warning" %}
Keyless plans are intended for testing. For production use, select an API Key plan to track usage per consumer, enforce rate limits, and attribute costs. See [Configure an LLM Proxy](../build/configure-an-llm-proxy.md).
{% endhint %}

Select **Next** to proceed.

## Step 5: Review and create

Review the LLM Proxy configuration (provider, model, authentication, context path, and consumer plan), then select one of the following:

* **Create only**. This creates the LLM Proxy without deploying it to the AI Gateway.
* **Create & deploy**. This creates the LLM Proxy and deploys it to the AI Gateway.

For this quickstart, select **Create & deploy** so that you can send a test prompt in the next step.

## Step 6: Send a test prompt

Once the LLM Proxy is deployed, send a test prompt to confirm it works:

```bash
curl -X POST https://<your-gateway-host>/my-llm-proxy/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-5",
    "max_tokens": 256,
    "messages": [{"role": "user", "content": "Hello, world"}]
  }'
```

A successful response returns the model's reply, confirming that the AI Gateway is routing prompts through your LLM Proxy to the upstream provider.

{% hint style="info" %}
This example uses the Anthropic message format, whose path includes the `/v1` segment. The OpenAI format does not: it is `<context-path>/chat/completions`. See [Publish your LLM Proxy](../publish/publish-your-llm-proxy.md).

To list the model identifiers your proxy accepts, send a `GET` request to `<context-path>/models`.
{% endhint %}

## Next steps

* **Add more models**: Configure additional providers. See [Configure an LLM Proxy](../build/configure-an-llm-proxy.md).
* **Secure with an API key plan**: Replace the keyless plan with an API key to track usage and enforce rate limits.
* **Route Claude Code through the proxy**: Set `ANTHROPIC_BASE_URL` to point at your LLM Proxy for zero-code integration. See [Connect Claude Code to the Edge Daemon](../../edge-management/connect-claude-code-to-daemon.md).
* **Publish**: Make the LLM Proxy discoverable. See [Publish your LLM Proxy](../publish/publish-your-llm-proxy.md).
