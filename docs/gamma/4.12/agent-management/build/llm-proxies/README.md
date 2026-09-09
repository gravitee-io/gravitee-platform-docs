---
hidden: false
noIndex: false
description: Create, design, and publish an LLM Proxy that routes model traffic through the AI Gateway. Choose the LLM Proxy task you want to start with.
---

# LLM Proxies

An LLM Proxy routes traffic to upstream model providers through the AI Gateway. These guides follow the groups of the LLM Proxy sidebar in the Gamma console.

* [**Create an LLM Proxy**](../create-an-llm-proxy.md): Create an LLM Proxy that routes traffic to upstream model providers through the AI Gateway.
* [**AI resources**](../ai-resources.md): Supply the models and vector stores that Guard Rails, PII Filtering, and Semantic Caching policies call.
* [**Design**](design/README.md): Configure guardrails, rate limiting, text classification, and runtime model overrides.
* [**Consumer access**](consumer-access/README.md): Publish your LLM Proxy and manage the subscriptions that grant consumers access to it.
* [**LLM Proxy provider support**](../llm-proxy-provider-support.md): Which OpenAI features each provider supports, how requests map to each native API, and the limits that apply.
* [**Accepted request formats**](../accepted-request-formats.md): The endpoints and limits for the OpenAI, Anthropic Messages, and Gemini generateContent formats.
* [**Consume your LLM Proxy with LangChain**](../../publish/consume-your-llm-proxy-with-langchain.md): Route a LangChain chain through an LLM Proxy so the chain never holds a provider credential.
* [**Connect Claude Code through an LLM Proxy**](../../publish/connect-claude-code-through-an-llm-proxy.md): Configure Claude Code to reach Anthropic through an LLM Proxy while users keep their own OAuth login.
