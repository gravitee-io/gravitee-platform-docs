---
hidden: false
noIndex: true
---

# Connect Claude Code to the Edge Daemon
<!-- GAP-STRUCTURAL: Missing procedural content source -->

Once the Edge Daemon is installed on an employee device, you can route Claude Code LLM traffic through it for local policy enforcement and centralized observability.

## Prerequisites

* Edge Daemon installed and running on the device (see [Configure Kandji to deploy the Edge Daemon](configure-kandji-daemon.md))
* Claude Code installed on the same device
* The Edge Daemon is listening on its default local port (`8990`)

## How it works

The Edge Daemon runs as a local reverse proxy on the employee's device. When you set the `ANTHROPIC_BASE_URL` environment variable to point at the Edge Daemon's local address, Claude Code sends LLM API requests to the Edge Daemon instead of directly to `api.anthropic.com`. The Edge Daemon then:

1. Applies local policies (secret detection, model allowlist, token budget)
2. Forwards the request to the Gravitee AI Gateway
3. The AI Gateway applies enterprise-wide policies (fine-grained authorization, rate limiting, PII filtering)
4. The response returns through the same chain

{% hint style="warning" %}
Only LLM traffic is redirected through the Edge Daemon using this method. Claude Code also makes direct calls to `api.anthropic.com` for telemetry, authentication, and other operations — these requests bypass the Edge Daemon and reach Anthropic directly.

An interception mode is in development that will redirect all traffic (including telemetry and auth) using local DNS resolution. This requires additional certificate configuration. See [Edge Daemon](README.md) for details.
{% endhint %}

No code changes are required in Claude Code — the base URL override is the only configuration needed.

## Step 1: Set the environment variable

Configure Claude Code to route LLM traffic through the Edge Daemon by setting the Anthropic base URL:

```bash
export ANTHROPIC_BASE_URL=http://localhost:8990
```

To persist this across sessions, add it to your shell profile (e.g., `~/.zshrc` or `~/.bashrc`):

```bash
echo 'export ANTHROPIC_BASE_URL=http://localhost:8990' >> ~/.zshrc
source ~/.zshrc
```

{% hint style="info" %}
For fleet-wide deployment, push this environment variable through your MDM solution as a configuration profile rather than requiring each employee to set it manually. This is the recommended approach once shadow AI detection has confirmed which tools are in use.
{% endhint %}

## Step 2: Verify the connection

Send a test prompt through Claude Code and confirm that traffic is routed through the Edge Daemon:

1. Open Claude Code and send any prompt.
2. In the Gamma console, navigate to **Agent Management** → **Edge Management**.
3. Check the **Recent device activity** panel for your device.
4. Confirm that the request appears as managed traffic (not shadow AI).

## Next steps

* **Monitor traffic** — View AI usage from this device in the Edge Management dashboard. See [Monitor AI Gateway usage from employee systems](../observe/monitor-ai-gateway-from-devices.md).
