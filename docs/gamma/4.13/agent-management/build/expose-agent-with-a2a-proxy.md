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
* **Client authentication**. The wizard secures the proxy with a default plan of the security type you choose: **Keyless**, **API Key**, **JWT**, **OAuth 2.0**, or **mTLS**. Except with a Keyless plan, every caller authenticates against the plan before the gateway forwards the request, so clients reach the agent through the gateway rather than calling it directly.
* **Wire-level governance**. Every invocation passes through the AI Gateway with full observability and policy enforcement. This is the same governance applied to MCP and LLM traffic.

## Create an A2A Proxy

1. From the Gamma console sidebar, select **Agent Management**.
2. Under **Secure**, select **A2A Proxies**.
3. To launch the wizard, select **Create A2A proxy**.
4. **Step 1: Define**: Provide a name and the **Context path** where clients reach the proxy on the gateway. The wizard derives the context path from the name, so you can accept the suggested value or replace it. A description is optional.
5. **Step 2: Secure**: Choose how clients authenticate to the gateway: **Keyless**, **API Key**, **JWT**, **OAuth 2.0**, or **mTLS**. The settings of the selected type appear under the picker. A default plan of that type is created and published with the proxy.
   * **API Key**. Choose how consumers send the key: **Authorization: Bearer**, **Custom header**, or **Query parameter**.
   * **JWT**. Select the **Signature algorithm** and the **Public key resolver**, and then enter the **JWKS URL** or the **Public key (PEM)**.
   * **OAuth 2.0**. Select the **Provider**, **Generic OAuth2** or **Auth0**, and enter a **Name** for the OAuth2 resource. For **Generic OAuth2**, enter the **Issuer URL**, the **Introspection endpoint**, the **Client ID**, and the **Client secret**, and optionally the **User info endpoint**. Give the **Issuer URL** as a full URL including the scheme, for example `https://auth.example.com`, and give the two endpoints as paths under it, for example `/oauth2/introspect`. The gateway calls both endpoints on the authorization server, so an endpoint on another host, or outside the path of the issuer, is refused. For **Auth0**, enter the **Tenant domain** and the **API audience**. The wizard declares the provider as a resource on the proxy under that name, and the default plan references it. To use Gravitee Access Management instead, declare the resource on the **Resources** page after creating the proxy, and then add an OAuth2 plan from the **Plans** page.
   * **mTLS**. Clients present an X.509 certificate during the TLS handshake. Configure the trusted certificate authorities and the certificate validation rules in the gateway-level TLS settings.
   * **Keyless**. Any client that can reach the context path can call the upstream agent. Choose it only when access is controlled at the network level.

   For the settings of each type, see [Manage A2A Proxy plans](configure-your-a2a-proxy/manage-a2a-proxy-plans.md).
6. **Step 3: Connect**: Enter the **Target URL** of the upstream agent, and then choose how the gateway authenticates to it at runtime. **Static credential** injects a credential into a request header on every call, and **No upstream auth** calls the upstream without credentials.
7. **Step 4: Review**: Confirm the summary. For an OAuth 2.0 plan, an **Identity provider** card lists the provider details. Then select **Create A2A proxy**.

The A2A Proxy is created and starts running. Its **Overview** page shows the configured gateway URL and the upstream agent URL that the proxy forwards to. The default plan is named after its type, for example **Default API Key Plan**, and is listed on the **Plans** page of the proxy.

## Give a client access

With any plan other than Keyless, a client calls the proxy through a subscription. To let a client call the proxy, subscribe its application to the default plan:

1. Under **Consumer Access**, select **Consumers**.
2. Click **Create subscription**, select the application and the plan, and then click **Create subscription**.
3. Select the **Application** of the new subscription, and then click **Approve**. The default plan uses manual validation, so the subscription starts as pending.
4. For an API Key plan, copy the key from the **API Keys** card of the subscription. The key is generated when the subscription is approved.

Clients send the key the way the plan expects, for example `Authorization: Bearer <api-key>` for the **Authorization: Bearer** mode. For a JWT or OAuth 2.0 plan, the application needs a client ID before it can subscribe. For the full subscription lifecycle, see [Manage subscriptions](../publish/manage-subscriptions.md).

The gateway accepts the new subscription within a few seconds of the approval. If the first calls are rejected, wait a moment and try again.

If you secured the proxy with mTLS, configure the trusted certificate authorities and the certificate validation rules in the gateway-level TLS settings.

## The `/.well-known/agent-card.json` descriptor

Clients fetch the agent card from the gateway at the following address:

```
https://<your-gateway-host>/<context-path>/.well-known/agent-card.json
```

The proxy returns the upstream agent's own card with its advertised endpoint URL rewritten to the gateway address. A client that discovers the agent this way sends every subsequent request through the proxy. The contents of the descriptor, including its declared skills, come from the upstream agent.

## Next steps

* **[Create an agent identity](create-an-agent-identity.md)**. Agent identities are managed under **Agent Identity**, in the **Catalog** section of Agent Management.
* **[Manage A2A Proxy plans](configure-your-a2a-proxy/manage-a2a-proxy-plans.md)**. Add plans of other security types, publish them, and close them.
* **[Manage subscriptions](../publish/manage-subscriptions.md)**. Create, approve, reject, and close the subscriptions of the proxy.
* **[Add policies to your A2A Proxy](configure-your-a2a-proxy/add-policies-to-a2a-proxy.md)**. Use the Policy Studio to apply security, transformation, and traffic policies to agent traffic.
* **[Author an authorization policy](../../authorization-management/configure/create-update-delete-policies.md)**. In Authorization Management, select **A2A Agents** to grant or restrict which principals can invoke an agent. Policies target an agent from the Catalog, so import the agent there first.
