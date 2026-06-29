---
hidden: false
noIndex: true
---

# Edge Daemon

The Edge Daemon is a lightweight process installed on employee devices that observes outgoing AI traffic, enforces local policies, and forwards requests to the Gravitee AI Gateway for enterprise-wide policy enforcement.

## What the Edge Daemon does

| Function                     | Description                                                                                                                                                                                                                                                                                     |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Shadow AI detection**      | Scans local network connections to detect any process communicating with a known AI provider. Runs regardless of whether traffic is routed through the Edge Daemon — its mission is to surface unmanaged AI usage.                                                                              |
| **Active routing**           | When an AI tool is configured to route through the Edge Daemon (e.g., `ANTHROPIC_BASE_URL=http://localhost:8990`), the Edge Daemon acts as a reverse proxy. It receives the request, applies local policies, and forwards it to the Gravitee AI Gateway for enterprise-wide policy enforcement. |
| **Local policy enforcement** | Pre-egress checks block sensitive data before it leaves the device — secrets, classified content, large prompt payloads, and disallowed models.                                                                                                                                                 |

## Traffic routing modes

### URL override

By setting a provider's base URL environment variable to point at the Edge Daemon's local address, AI tools send their API requests to the Edge Daemon instead of directly to the provider.

{% hint style="warning" %}
With URL override, only LLM traffic is redirected through the Edge Daemon. AI tools such as Claude Code also make direct calls to the provider for telemetry, authentication, and other non-LLM operations — these calls bypass the Edge Daemon and reach the provider directly.
{% endhint %}

### Interception mode (coming soon)

An interception mode is in development. It uses local DNS resolution to redirect traffic from the provider's domain (e.g., `api.anthropic.com`) to the Edge Daemon. This approach intercepts all traffic — including telemetry and authentication — but requires additional setup, including local certificate configuration.

## APIs in Edge Management

To handle the traffic forwarded by the Edge Daemon to the Gravitee AI Gateway, you need to create APIs in Edge Management:

| API type           | Purpose                                                                                                  |
| ------------------ | -------------------------------------------------------------------------------------------------------- |
| **LLM Proxy API**  | Handles LLM usage calls. Enables LLM-specific policies (token budgets, model allowlists, PII filtering). |
| **HTTP Proxy API** | Handles classic HTTP traffic (telemetry, authentication). Enables HTTP-specific policies.                |

{% hint style="info" %}
Detailed configuration instructions for these APIs aren't yet available. This feature is currently in active development.
{% endhint %}

## Next steps

* **Deploy the Edge Daemon** — Use an MDM solution to distribute the Edge Daemon to your device fleet. See [Configure Kandji to deploy the Edge Daemon](configure-kandji-daemon.md).
* **Connect AI tools** — Route Claude Code through the Edge Daemon. See [Connect Claude Code to the Edge Daemon](connect-claude-code-to-daemon.md).
