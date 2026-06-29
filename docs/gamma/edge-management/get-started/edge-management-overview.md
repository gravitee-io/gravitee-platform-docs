---
hidden: false
noIndex: true
---

# Edge Daemon

The Edge Daemon is a lightweight process installed on employee devices that observes outgoing AI traffic, enforces local policies, and forwards requests to the Gravitee AI Gateway for enterprise-wide policy enforcement.

{% hint style="warning" %}
**Preview feature — not production-ready.** Edge Management is under active development. In particular, the connections between the Edge Daemon and the gateway — both the proxied API/LLM traffic and the Edge Reactor control plane — are **not yet secured**: they use plain HTTP, with no transport encryption and no authentication between the daemon and the gateway. Do not expose these endpoints over untrusted networks. Authenticated, TLS-secured connections (API key, OAuth2/JWT, mTLS) are planned but not yet available.
{% endhint %}

## What the Edge Daemon does

| Function                     | Description                                                                                                                                                                                                                                                                                     |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Shadow AI detection**      | Scans local network connections to detect any process communicating with a known AI provider. Runs regardless of whether traffic is routed through the Edge Daemon — its mission is to surface unmanaged AI usage.                                                                              |
| **Active routing**           | The Edge Daemon acts as a reverse proxy. By default it captures AI traffic transparently (interception mode); it can also receive traffic from tools explicitly pointed at it (proxy mode). It applies local policies and forwards the request to the Gravitee AI Gateway for enterprise-wide policy enforcement. |
| **Local policy enforcement** | Pre-egress checks block sensitive data before it leaves the device — secrets, classified content, large prompt payloads, and disallowed models.                                                                                                                                                 |

## Accessing Edge Management

Edge Management is a top-level application module within the Gamma console. You can access it by selecting the **Edge Management** application card from the console homepage or sidebar. This module provides a unified view of your deployed Edge Daemons and intercepted shadow AI traffic.

## Traffic routing modes

The Edge Daemon supports two routing modes. After an MDM-based install both listeners run simultaneously, with interception enabled by default.

### Interception mode (default)

This is the default, transparent mode — no per-tool configuration is required. The Edge Daemon runs a local DNS resolver that redirects configured AI provider domains (e.g., `api.anthropic.com`) to itself, where it **terminates the TLS connection locally** using a locally generated Certificate Authority. To present a valid certificate for the intercepted domain, the daemon installs that CA in the device trust store at startup. It then forwards the request to the gateway (see [Gateway-side requirements](#gateway-side-requirements) for the current security caveats on that connection).

Because interception works at the domain level, it captures all traffic to the configured domains — including non-LLM calls (telemetry, authentication) served from those domains.

{% hint style="info" %}
Node.js-based tools (Claude Code, Cursor) do not use the OS trust store by default, so they need the daemon's local CA trusted separately. The installer handles this automatically — it sets `NODE_EXTRA_CA_CERTS` (via `launchctl` and the user's shell profile) while the daemon installs the CA into the OS trust store at startup. No manual step is required.
{% endhint %}

### Proxy mode (manual alternative)

Alternatively, a tool can be pointed at the Edge Daemon explicitly by setting its provider base URL environment variable to the daemon's local address (e.g., `ANTHROPIC_BASE_URL=http://localhost:8990`). The AI tool then sends its API requests to the Edge Daemon instead of directly to the provider.

{% hint style="warning" %}
With proxy mode, only LLM traffic is redirected through the Edge Daemon. AI tools such as Claude Code also make direct calls to the provider for telemetry, authentication, and other non-LLM operations — these calls bypass the Edge Daemon and reach the provider directly. Interception mode does not have this limitation.
{% endhint %}

## APIs in Edge Management

The traffic forwarded by the Edge Daemon is captured by standard APIM APIs that you **create manually** on the AI Gateway — Edge Management does not create them for you:

| API type           | Purpose                                                                                                  |
| ------------------ | -------------------------------------------------------------------------------------------------------- |
| **LLM Proxy API**  | Handles LLM usage calls. Enables LLM-specific policies (token budgets, model allowlists, PII filtering). |
| **HTTP Proxy API** | Handles classic HTTP traffic (telemetry, authentication). Enables HTTP-specific policies.                |

{% hint style="info" %}
For the API types, context paths, and required keyless plan, see [Create the proxy APIs](../connect/create-proxy-apis.md). Routing of proxied traffic to these APIs is then configured from the Gamma console — see [Configure Edge Management](../connect/configure-edge-management.md).
{% endhint %}

## Gateway-side requirements

The Edge Daemon connects to two gateway-side endpoints, both of which must be reachable from employee devices:

| Connection        | Default target                          | Purpose                                                                                                              |
| ----------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **AI Gateway**    | gateway HTTP port (e.g., `8082`)        | Proxied LLM/HTTP traffic forwarded by the daemon, captured by the proxy APIs deployed on the gateway.               |
| **Edge Reactor**  | dedicated port `18093` (`edge.server.port`) | Daemon control plane: configuration polling (`GET /config`), heartbeat, metrics, and shadow AI reporting. |

The Edge Reactor runs as a **separate HTTP listener** on the gateway, not on the main gateway port. Its port (`18093` by default) must be explicitly exposed — for example through a dedicated Kubernetes Service and Ingress — so that daemons running on employee devices can reach it.

{% hint style="warning" %}
Because these endpoints are currently unencrypted and unauthenticated (see the preview note above), do not expose them to the public internet. Restrict access to a private network, VPN, or an IP-allowlisted corporate network.
{% endhint %}

The traffic the daemon forwards is captured by the proxy APIs deployed on the AI Gateway (see [APIs in Edge Management](#apis-in-edge-management) above): the daemon's routes map each request path to the matching API — an **LLM Proxy API** for LLM calls (e.g., `/v1/messages`) and an **HTTP Proxy API** for the remaining traffic. These routes are configured from the Gamma console.

## Next steps

* **Deploy the Edge Daemon** — Use an MDM solution to distribute the Edge Daemon to your device fleet. See [Configure Kandji to deploy the Edge Daemon](configure-kandji-daemon.md).
* **Connect AI tools** — Route Claude Code through the Edge Daemon. See [Connect Claude Code to the Edge Daemon](connect-claude-code-to-daemon.md).
