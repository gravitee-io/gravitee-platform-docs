---
hidden: false
noIndex: false
---

# Publish your LLM Proxy


Publishing an LLM Proxy makes it accessible to consumers through the AI Gateway. Once published, consumers can send prompts to the proxy's context path and the AI Gateway routes them to the configured upstream model providers with full governance.

## Prerequisites

* An LLM Proxy created and configured (see [Create an LLM Proxy](../build/create-an-llm-proxy.md))
* At least one consumer plan attached (API Key or Keyless)

## Publish the LLM Proxy

1. Navigate to the LLM Proxy detail page.
2. If the LLM Proxy was created without the **Deploy** option, or if you have unpublished changes, a banner indicates that the proxy is **Out of Sync**.
3. Select **Deploy** from the banner to push the configuration to the AI Gateway.
4. Once deployed, the LLM Proxy is live at its configured context path.

The Universal LLM Router exposes a single endpoint that simultaneously supports multiple formats (OpenAI API, Anthropic API, and Gemini API). You can send prompts using any of these native formats; the router will route across providers and convert the responses back to the format you requested.

Consumers can now send prompts to paths such as:

```
https://<your-gateway-host><context-path>/chat/completions
https://<your-gateway-host><context-path>/v1/messages
```

{% hint style="warning" %}
The OpenAI path has no `/v1` segment, but the Anthropic path does. The `/v1` in
`https://api.openai.com/v1` belongs to the provider URL you configured on the proxy,
not to the path your consumers call. A request to `<context-path>/v1/chat/completions`
returns `404`.

For an OpenAI SDK, this means `base_url` is the context path on its own, with no
`/v1`, because the SDK appends `/chat/completions` itself.
{% endhint %}

To discover the exact model identifiers this proxy accepts, send a `GET` request to
`<context-path>/models`. The response lists each model prefixed with the proxy name,
for example `llm-my-router:gpt-4o-mini`.

## Consumer access

How consumers authenticate depends on the plan attached to the LLM Proxy:

| Plan type   | Consumer action                                                                               |
| ----------- | --------------------------------------------------------------------------------------------- |
| **API Key** | Include the API key in request headers. The consumer obtains an API key through subscription. |
| **Keyless** | No authentication required. Any client can send prompts to the context path.                  |

For plan management and subscription workflows, see [Configure an LLM Proxy](../build/configure-an-llm-proxy.md).

## Next steps

* [Configure an LLM Proxy](../build/configure-an-llm-proxy.md): Add guardrails and additional security plans.
* [Monitor AI Gateway usage from employee systems](../observe/monitor-ai-gateway-from-devices.md): View traffic and cost attribution for published LLM Proxies.
