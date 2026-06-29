---
description: Reference for the LLM Proxy and HTTP proxy APIs in APIM that handle traffic intercepted by the Edge Daemon.
hidden: false
noIndex: true
---
 
# Proxy API reference
 
The Edge Daemon forwards the traffic it intercepts to APIs deployed on the AI Gateway. These proxy APIs are standard APIM v4 APIs and must be created manually in APIM—Edge Management doesn't create them. Saving an Edge Management configuration deploys only the daemon configuration; it does not deploy the proxy APIs.
 
For the Claude Code use case, two proxy APIs are required. The daemon's [routes](configure-edge-management.md#proxy) point at them by context path.
 
{% hint style="warning" %}
Both APIs must expose a **Keyless plan**. The connection between the daemon and the gateway isn't authenticated, as noted in the [Edge Management overview](../get-started/edge-management-overview.md), so a secured plan rejects the daemon's requests. Expose these APIs on trusted networks only.
{% endhint %}
 
## LLM Proxy API
 
Handles Claude Code's LLM calls on the daemon route from `/v1/messages` to `/interception/claude`.
 
| Setting      | Value                       |
| ------------ | --------------------------- |
| API type     | LLM Proxy                   |
| Context path | `/interception/claude`      |
| Endpoint     | `https://api.anthropic.com` |
| Plan         | Keyless                     |
 
As an LLM Proxy API, it supports LLM-specific policies on its flow phases (**Prompt**, **Embeddings**, **Models**)—for example, token budgets, model allowlists, or PII filtering.
 
## HTTP proxy API
 
Handles all non-LLM traffic on the daemon route from `/` to `/interception/passthrough`, including `/api/event_logging/v2/batch`, `/mcp-registry/v0/servers`, and other non-LLM endpoints.
 
| Setting      | Value                        |
| ------------ | ----------------------------- |
| API type     | HTTP proxy                   |
| Context path | `/interception/passthrough`  |
| Endpoint     | `https://api.anthropic.com`  |
| Plan         | Keyless                      |
 
## Shared capabilities
 
Both APIs are standard APIM v4 APIs and support:
 
* Any policies needed to enforce on the captured traffic.
* **Logging**, to inspect requests and responses. Request and response content is included when the logging mode is configured for it.
* Usage tracking under **API Traffic** metrics.
{% hint style="info" %}
The context path of each API must match the **API path** set in the corresponding Edge Management route. See [Configure Edge Management](configure-edge-management.md#proxy).
{% endhint %}