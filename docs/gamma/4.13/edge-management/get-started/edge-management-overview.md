---
description: >-
  Overview of the Gravitee Edge Daemon, its traffic routing modes, and the
  gateway-side endpoints it connects to.
hidden: false
noIndex: false
---

# Edge Daemon

The Edge Daemon is a lightweight process installed on employee devices that observes outgoing AI traffic, enforces local policies, and forwards requests to the Gravitee AI Gateway for enterprise-wide policy enforcement.

{% hint style="warning" %}
**Preview feature—not production-ready.** Edge Management is under active development. In particular, the connections between the Edge Daemon and the gateway—both the proxied API and LLM traffic and the Edge Reactor control plane—are **not yet secured**. They use plain HTTP, with no transport encryption and no authentication between the daemon and the gateway. Do not expose these endpoints over untrusted networks. Authenticated, TLS-secured connections such as API key, OAuth2/JWT, and mTLS are planned but not yet available.
{% endhint %}

{% hint style="info" %}
**Compatibility.** The Edge Daemon is currently available for **macOS only**—Apple Silicon and Intel. It supports traffic interception for Claude Code through the Anthropic API.
{% endhint %}

## What the Edge Daemon does

The Edge Daemon performs the following functions:

| Function                     | Description                                                                                                                                                                                                                                                    |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Shadow AI detection**      | Scans local network connections to detect any process that connects directly to a monitored AI provider domain and bypasses the gateway. This surfaces unmanaged AI usage.                                                                                     |
| **Active routing**           | The Edge Daemon acts as a reverse proxy. By default, it captures AI traffic transparently in interception mode. It can also receive traffic from tools that are explicitly pointed at it in proxy mode. It applies local policies and forwards the request to the Gravitee AI Gateway for enterprise-wide policy enforcement. |
| **Local policy enforcement** | Pre-egress checks block sensitive data before it leaves the device, including secrets, classified content, large prompt payloads, and disallowed models.                                                                                                        |

## Access Edge Management

Edge Management is a top-level application module within the Gamma console. To open it, select the **Edge Management** application card on the console home page, or select **Edge Management** from the product switcher in the sidebar. This module provides a unified view of your deployed Edge Daemons and intercepted shadow AI traffic.

## Traffic routing modes

The Edge Daemon supports two routing modes. After an MDM-based installation, both listeners run simultaneously, and interception is enabled by default.

### Interception mode

This is the default, transparent mode, and no per-tool configuration is required. The Edge Daemon runs a local DNS resolver that redirects configured AI provider domains, such as `api.anthropic.com`, to itself. There, it **terminates the TLS connection locally** using a locally generated Certificate Authority. To present a valid certificate for the intercepted domain, the daemon installs that CA in the device trust store at startup. It then forwards the request to the gateway. For the current security caveats on that connection, see [Gateway-side requirements](#gateway-side-requirements).

Because interception works at the domain level, it captures all traffic to the configured domains, including non-LLM calls such as telemetry and authentication served from those domains.

{% hint style="info" %}
Node.js-based tools such as Claude Code do not use the OS trust store by default, so they need the daemon's local CA trusted separately. The installer handles this automatically. It sets `NODE_EXTRA_CA_CERTS` through `launchctl` and your shell profile, while the daemon installs the CA into the OS trust store at startup. No manual step is required.
{% endhint %}

### Proxy mode

Alternatively, you can point a tool at the Edge Daemon explicitly by setting its provider base URL environment variable to the daemon's local address, for example `ANTHROPIC_BASE_URL=http://localhost:8990`. The AI tool then sends its API requests to the Edge Daemon instead of directly to the provider.

{% hint style="warning" %}
With proxy mode, only LLM traffic is redirected through the Edge Daemon. AI tools such as Claude Code also make direct calls to the provider for telemetry, authentication, and other non-LLM operations. These calls bypass the Edge Daemon and reach the provider directly. Interception mode captures this traffic as well.
{% endhint %}

## APIs in Edge Management

The traffic forwarded by the Edge Daemon is captured by standard APIM APIs that you **create manually** on the AI Gateway. Edge Management does not create them for you. The following table describes the two API types:

| API type           | Purpose                                                                                                        |
| ------------------ | ---------------------------------------------------------------------------------------------------------------- |
| **LLM Proxy API**  | Handles LLM usage calls. Enables LLM-specific policies such as token budgets, model allowlists, and PII filtering. |
| **HTTP proxy API** | Handles classic HTTP traffic such as telemetry and authentication. Enables HTTP-specific policies.               |

{% hint style="info" %}
For the API types, context paths, and required keyless plan, see [Proxy API reference](../connect/proxy-api-reference.md). Routing of proxied traffic to these APIs is then configured from the Gamma console. See [Configure Edge Management](../connect/configure-edge-management.md).
{% endhint %}

## Gateway-side requirements

The Edge Daemon connects to two gateway-side endpoints, both of which must be reachable from employee devices:

| Connection       | Default target                              | Purpose                                                                                                             |
| ---------------- | ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **AI Gateway**   | gateway HTTP port, for example `8082`       | Proxied LLM and HTTP traffic forwarded by the daemon, captured by the proxy APIs deployed on the gateway.           |
| **Edge Reactor** | dedicated port `18093`, set by `edge.server.port` | Daemon control plane: configuration polling with `GET /config`, heartbeat, metrics, and shadow AI reporting.  |

The Edge Reactor runs as a **separate HTTP listener** on the gateway, not on the main gateway port. You must explicitly expose its port, `18093` by default, for example through a dedicated Kubernetes Service and Ingress, so that daemons running on employee devices can reach it.

{% hint style="warning" %}
Because these endpoints are currently unencrypted and unauthenticated, as described in the preceding preview note, do not expose them to the public internet. Restrict access to a private network, VPN, or an IP-allowlisted corporate network.
{% endhint %}

The traffic the daemon forwards is captured by the proxy APIs deployed on the AI Gateway, as described in [APIs in Edge Management](#apis-in-edge-management). The daemon's routes map each request path to the matching API: an **LLM Proxy API** for LLM calls such as `/v1/messages`, and an **HTTP proxy API** for the remaining traffic. You configure these routes from the Gamma console.

## Next steps

Complete the following tasks:

* **Deploy the Edge Daemon.** Use an MDM solution to distribute the Edge Daemon to your device fleet. See [Configure Kandji to deploy the Edge Daemon](../connect/configure-kandji-daemon.md).
* **Connect AI tools.** Route Claude Code through the Edge Daemon. See [Connect Claude Code to the Edge Daemon](../connect-claude-code-to-daemon.md).
