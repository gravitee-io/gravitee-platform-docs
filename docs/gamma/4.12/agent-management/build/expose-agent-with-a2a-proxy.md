---
hidden: false
noIndex: false
description: Expose an upstream agent behind the AI Gateway with an A2A Proxy so other agents can discover and call it. Follow the steps to create the proxy.
---

# Expose your agent with the A2A Proxy

The Agent-to-Agent (A2A) Proxy makes an upstream agent reachable by other agents across trust boundaries, providers, and organizations. It implements the A2A protocol by serving the agent's `/.well-known/agent-card.json` descriptor through the gateway. The AI Gateway then governs every invocation.

## What the A2A Proxy does

When you expose an agent through the A2A Proxy, the proxy provides the following:

* **Agent card discovery**. The proxy serves the upstream agent's `/.well-known/agent-card.json` descriptor, the A2A standard for advertising agent capabilities. It rewrites the agent's endpoint URL in the descriptor so that callers reach the agent through the gateway instead of directly. Other URLs in the card, such as `documentationUrl`, pass through unchanged. The gateway handles the legacy `/.well-known/agent.json` path and the extended agent card endpoint the same way.
* **Client authentication**. The wizard secures the proxy with a default plan that uses either an API key or a client certificate. Every caller authenticates against a plan before the gateway forwards the request, so clients reach the agent through the gateway rather than calling it directly.
* **Wire-level governance**. Every invocation passes through the AI Gateway with full observability and policy enforcement. This is the same governance applied to MCP and LLM traffic.

## Create an A2A Proxy

1. From the Gamma console sidebar, select **Agent Management**.
2. Under **Secure**, select **A2A Proxies**.
3. To launch the wizard, select **Create A2A proxy**.
4. **Step 1: Define**: Provide a name and the **Context path** where clients reach the proxy on the gateway. The wizard derives the context path from the name, so you can accept the suggested value or replace it. A description is optional.
5. **Step 2: Secure**: Choose how clients authenticate to the gateway, either **API Key** or **mTLS**. A default plan is created and published with the proxy.
6. **Step 3: Connect**: Enter the **Target URL** of the upstream agent, and then choose how the gateway authenticates to it at runtime. **Static credential** injects a credential into a request header on every call, and **No upstream auth** calls the upstream without credentials.
7. **Step 4: Review**: Confirm the summary, and then select **Create A2A proxy**.

The A2A Proxy is created and starts running. Its **Overview** page shows the configured gateway URL and the upstream agent URL that the proxy forwards to.

## Give a client access

The proxy rejects unauthenticated requests, including requests for the agent card. To let a client call a proxy secured with an API key, complete the following steps:

1. In the APIM console, create an application, or open an existing one.
2. Subscribe the application to the proxy's default plan.
3. Approve the subscription. The default plan uses manual validation, so subscriptions start as pending.
4. Copy the API key from the subscription.

Clients send the key in the `Authorization` header as `Bearer <api-key>`. The `X-Gravitee-Api-Key` header is not accepted.

If you secured the proxy with mTLS instead, configure the trusted certificate authorities and the certificate validation rules in the gateway-level TLS settings.

## The `/.well-known/agent-card.json` descriptor

Clients fetch the agent card from the gateway at the following address:

```
https://<your-gateway-host>/<context-path>/.well-known/agent-card.json
```

The proxy returns the upstream agent's own card with its advertised endpoint URL rewritten to the gateway address. A client that discovers the agent this way sends every subsequent request through the proxy. The contents of the descriptor, including its declared skills, come from the upstream agent.

## Next steps

* **[Create an agent identity](create-an-agent-identity.md)**. Agent identities are managed under **Agent Identity**, in the **Catalog** section of Agent Management.
* **[Add policies to your A2A Proxy](configure-your-a2a-proxy/add-policies-to-a2a-proxy.md)**. Use the Policy Studio to apply security, transformation, and traffic policies to agent traffic.
* **[Author an authorization policy](../../authorization-management/configure/create-update-delete-policies.md)**. In Authorization Management, select **A2A Agents** to grant or restrict which principals can invoke an agent. Policies target an agent from the Catalog, so import the agent there first.
* **[Publish your agent to the Developer Portal](../publish/publish-your-agent-to-the-developer-portal.md)**. List the agent in the Developer Portal catalog so consumers can find it and subscribe.
