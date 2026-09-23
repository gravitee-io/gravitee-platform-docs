---
hidden: false
noIndex: false
description: >-
  Edge Management puts the Gravitee gateway between the AI tools on your
  employee devices and the providers they call. Learn what it governs in Gamma.
---

# Edge Management overview

Edge Management is Gravitee's product line for governing the AI traffic that leaves your employee devices. Gravitee doesn't replace the tools your engineers use. It puts the gateway between those tools and the AI providers they call, so a request that was previously invisible arrives at an API you own, carrying your policies, quotas, and analytics.

An **Edge Daemon** installed on each device captures outgoing AI traffic and forwards it to proxy APIs on the AI Gateway. The same daemon reports the AI providers that a device reaches directly, without the gateway.

{% hint style="warning" %}
**Edge Management is a preview feature, and it isn't production-ready.** It's under active development. In particular, the connections between the Edge Daemon and the gateway, both the proxied traffic and the Edge Reactor control plane, aren't yet secured. They use plain HTTP, with no transport encryption and no authentication between the daemon and the gateway. Don't expose these endpoints over networks you don't trust. Restrict them to a private network, a VPN, or an IP-allowlisted corporate network. Authenticated, TLS-secured connections such as API key, OAuth2/JWT, and mTLS are planned but not yet available.
{% endhint %}

## Why Edge Management exists

Every other Gamma module governs traffic that already reaches a Gravitee endpoint. AI coding tools don't. Claude Code and the tools beside it call their provider straight from the laptop, over the engineer's own credential, and an estate that adopts them runs into the following problems:

* **The traffic never reaches your governance layer.** An LLM Proxy governs the calls that are sent to it. A tool that calls `api.anthropic.com` from a device sends nothing to it, so the policies, the quotas, and the model rules you wrote apply to none of that traffic.
* **Spend is invisible until the invoice arrives.** Tokens are billed per provider account, not per team or per repository, so nothing attributes a month's cost to the work that caused it.
* **Adoption is unmeasured.** Nobody can say which providers the fleet reaches, from how many devices, or which of them were ever approved.
* **Bringing a tool under governance means changing the tool.** Pointing each tool at a gateway by hand, on each device, doesn't survive a fleet of any size, and an engineer can undo it with one environment variable.

Edge Management answers these at the device, not at the tool. The daemon is deployed once through your MDM, and what it intercepts is configured centrally, per environment.

## What Edge Management does

Edge Management sits between your employee devices and the AI providers they call. The **Edge Daemon** runs on the device and captures traffic. The **Edge Reactor** serves each daemon its configuration and collects what it reports. The **Gamma console** is the control plane where you configure the daemon and read the results.

Edge Management provides the following key capabilities:

* **Traffic interception**. The daemon runs a local DNS resolver for the domains you configure, so the AI tools on a device are captured transparently, with no per-tool setup. See [Configure Edge Management](../connect/configure-edge-management.md#configure-the-proxy).
* **Routing to governed APIs**. Ordered routes map each request path to a proxy API on the AI Gateway, so an intercepted request is governed by an ordinary APIM v4 API with its own plans, policies, and analytics. See [Proxy API reference](../connect/proxy-api-reference.md).
* **Shadow AI detection**. The daemon watches a list of provider domains and reports the connections a device makes to them directly, without the gateway. Detection is based on TCP connection monitoring, and no traffic content is inspected. See [Configure Shadow AI monitoring](../connect/configure-edge-management.md#configure-shadow-ai-monitoring).
* **Fleet deployment**. The daemon reaches your devices through your existing MDM rather than a manual install per machine. See [Configure Kandji to deploy the Edge Daemon](../connect/configure-kandji-daemon.md).

## The building blocks

Four objects carry the whole model, and each one builds on the one before it:

| Building block | What it is | Start here |
| --- | --- | --- |
| **Edge configuration** | The Edge Management configuration of one environment, created and edited on a single **Configuration** page. It holds the two gateway addresses, the DNS domains and routes, and the shadow AI settings. Saving it publishes the corresponding Edge API on the gateway. | [Configure Edge Management](../connect/configure-edge-management.md) |
| **Edge Daemon** | A process on each employee device. It intercepts the configured domains, forwards their traffic to the gateway, and reports its heartbeat, its metrics, and its shadow AI detections to the Edge Reactor. | [Configure Kandji to deploy the Edge Daemon](../connect/configure-kandji-daemon.md) |
| **Route** | An ordered rule that maps a request path prefix to the context path of a proxy API on the gateway, with an optional provider label. The first matching route wins. | [Configure the Proxy](../connect/configure-edge-management.md#configure-the-proxy) |
| **Proxy API** | The gateway API a route forwards to. It's a standard APIM v4 API that you create yourself, with its own page, plans, policies, and analytics. Edge Management points at it by context path and doesn't create it. | [Proxy API reference](../connect/proxy-api-reference.md) |

A configuration governs nothing until the devices run the daemon, and a route intercepts nothing until its proxy API is deployed. Both are separate from saving the configuration.

## How the traffic flows

Once Edge Management is configured and the daemon runs on a device, the AI traffic that leaves the device takes one of two paths.

| Path | What happens |
| --- | --- |
| **Proxied traffic** | The daemon captures the request and forwards it to the proxy API whose context path the matching route names. The gateway applies your policies, quotas, and analytics, then relays the request to the AI provider. |
| **Shadow AI** | The device reached an AI provider directly, without the gateway. The daemon reports that the connection happened. No traffic content is inspected. |

Interception works at the domain level, so it captures everything a tool sends to a configured domain, including non-LLM calls such as telemetry and authentication served from those domains. The routes decide where each of those requests goes.

## Traffic routing modes

The Edge Daemon supports two routing modes. After an MDM-based installation, both listeners run simultaneously, and interception is enabled by default.

### Interception mode

This is the default, transparent mode, and no per-tool configuration is required. The Edge Daemon runs a local DNS resolver that redirects the configured AI provider domains, such as `api.anthropic.com`, to itself. There, it **terminates the TLS connection locally** using a locally generated certificate authority. To present a valid certificate for the intercepted domain, the daemon installs that certificate authority in the device trust store at startup. It then forwards the request to the gateway.

{% hint style="info" %}
Node.js-based tools such as Claude Code don't use the OS trust store by default, so they need the daemon's local certificate authority trusted separately. The installer handles this automatically. It sets `NODE_EXTRA_CA_CERTS` through `launchctl` and your shell profile, while the daemon installs the certificate authority into the OS trust store at startup. No manual step is required.
{% endhint %}

### Proxy mode

Alternatively, you can point a tool at the Edge Daemon explicitly by setting its provider base URL environment variable to the daemon's local address, for example `ANTHROPIC_BASE_URL=http://localhost:8990`. The AI tool then sends its API requests to the Edge Daemon instead of directly to the provider.

{% hint style="warning" %}
With proxy mode, only LLM traffic is redirected through the Edge Daemon. AI tools such as Claude Code also make direct calls to the provider for telemetry, authentication, and other non-LLM operations. These calls bypass the Edge Daemon and reach the provider directly. Interception mode captures this traffic as well.
{% endhint %}

## Proxy APIs in Edge Management

The traffic forwarded by the Edge Daemon is captured by standard APIM v4 APIs that you **create manually** on the AI Gateway. Edge Management doesn't create them for you, and saving an Edge Management configuration deploys only the daemon configuration.

The following table describes the two API types:

| API type | Purpose |
| --- | --- |
| **LLM Proxy API** | Handles LLM usage calls, such as `/v1/messages`. Enables LLM-specific policies on the **Prompt**, **Embeddings**, and **Models** flow phases, such as token budgets, model allowlists, and PII filtering. |
| **HTTP proxy API** | Handles classic HTTP traffic such as telemetry and authentication. Enables HTTP-specific policies. |

Both APIs must expose a **Keyless** plan, because the connection between the daemon and the gateway isn't authenticated and a secured plan would reject the daemon's requests. For the context paths and the full reference, see [Proxy API reference](../connect/proxy-api-reference.md).

## Where things live in the console

Edge Management is a top-level application module within the Gamma console. To open it, select the **Edge Management** application card on the console home page, or select **Edge Management** from the product switcher in the sidebar.

Its configuration is gathered on a single **Configuration** page, split into the following sections:

| Section | What it covers |
| --- | --- |
| **Gateway** | The Gateway URL and the Reactor URL that every daemon of the environment is installed with. Both are locked once the configuration is created. |
| **Proxy** | The DNS domains the daemon intercepts, and the ordered routes that map each path prefix to the context path of a proxy API. |
| **Shadow AI monitoring** | The provider domains to watch for direct connections, and how often each daemon reports what it sees. |
| **Daemon Deployment** | What the devices are installed with, and the material needed to deploy the daemon across a fleet. |

The module also provides a unified view of your deployed Edge Daemons and of the intercepted and shadow AI traffic they report.

## Gateway-side requirements

The Edge Daemon connects to two gateway-side endpoints, both of which must be reachable from employee devices:

| Connection | Default target | Purpose |
| --- | --- | --- |
| **AI Gateway** | Gateway HTTP port | Proxied LLM and HTTP traffic forwarded by the daemon, captured by the proxy APIs deployed on the gateway. |
| **Edge Reactor** | Dedicated port `18093`, set by `edge.server.port` | Daemon control plane: configuration polling, heartbeat, metrics, and shadow AI reporting. |

The Edge Reactor runs as a **separate HTTP listener** on the gateway, not on the main gateway port. You must expose its port explicitly, `18093` by default, for example through a dedicated Kubernetes Service and Ingress, so that daemons running on employee devices can reach it. See [Configure Edge Ingress](../connect/configure-edge-ingress.md).

{% hint style="warning" %}
Because these endpoints are currently unencrypted and unauthenticated, as described in the preceding preview note, don't expose them to the public internet. Restrict access to a private network, VPN, or an IP-allowlisted corporate network.
{% endhint %}

## Use cases for Edge Management

Each of the following tables pairs an outcome with the feature that delivers it.

### Bring device AI traffic under the gateway

| Outcome | Feature |
| --- | --- |
| The LLM calls that Claude Code makes on an employee device reach an API you own, instead of going straight to the provider. | [Configure the Proxy](../connect/configure-edge-management.md#configure-the-proxy) |
| Intercepted LLM traffic lands on an API that already carries your token budgets, model rules, and logging. | [Proxy API reference](../connect/proxy-api-reference.md) |
| The telemetry and authentication calls a tool makes on the same domains are separated from its LLM calls and governed on their own API. | [Proxy API reference](../connect/proxy-api-reference.md) |
| An engineer starts using an intercepted tool with no per-tool setup and no certificate to trust by hand. | [Connect Claude Code to the Edge Daemon](../connect-claude-code-to-daemon.md) |

### Find out what your devices already do with AI

| Outcome | Feature |
| --- | --- |
| The AI providers that your fleet reaches directly, outside every policy you wrote, become visible. | [Configure Shadow AI monitoring](../connect/configure-edge-management.md#configure-shadow-ai-monitoring) |
| A provider is watched for direct connections without being intercepted, so you can measure adoption before you govern it. | [Configure Shadow AI monitoring](../connect/configure-edge-management.md#configure-shadow-ai-monitoring) |
| A shadow AI detection becomes a governed asset in the Catalog rather than a line on a report. | [Discover shadow AI agents from Edge Management](../../agent-management/import/discover-shadow-ai-agents-from-edge-management.md) |

### Roll out and keep a fleet healthy

| Outcome | Feature |
| --- | --- |
| The daemon reaches a device fleet through your existing MDM rather than a manual install per machine. | [Configure Kandji to deploy the Edge Daemon](../connect/configure-kandji-daemon.md) |
| The Edge Reactor port is reachable from the devices when the gateway runs on Kubernetes. | [Configure Edge Ingress](../connect/configure-edge-ingress.md) |
| A change to the routes or the watched domains reaches every daemon without touching a device. | [Save the configuration](../connect/configure-edge-management.md#save-the-configuration) |

## How Edge Management fits into Gamma

Gamma unifies its product lines under one platform: [API Management](../../api-management/get-started/api-management-overview.md), [Event Stream Management](../../event-stream-management/get-started/event-stream-management-overview.md), [Agent Management](../../agent-management/overview/README.md), Authorization Management, and Edge Management. They share the following foundations:

* **A common Catalog**. This catalog holds APIs, events, tools, agents, MCP servers, and models.
* **A common authorization engine**. [Authorization Management](../../authorization-management/get-started/authorization-management-overview.md) defines fine-grained policies against those cataloged assets.
* **Common enforcement points**. The AI Gateway, API Gateway, and Event Gateway evaluate the same policies at the wire level.

Edge Management is the one module that governs traffic which wasn't sent to Gravitee in the first place. It contributes no new enforcement layer of its own. Instead, it brings device traffic to an existing one: a route's proxy API is an ordinary gateway API, and for LLM calls it's an [LLM Proxy](../../agent-management/build/create-an-llm-proxy.md) governed exactly like the traffic that [Agent Management](../../agent-management/overview/README.md) already handles. A token budget, a model rule, or an authorization policy written there covers the device traffic the moment a route points at it.

The reverse direction is the reason to start here. Shadow AI detection is the only view in Gamma of traffic that no module governs yet, which makes it the starting point for deciding what to bring under the gateway next.

For the platform as a whole, and for the modules Edge Management sits beside, see the [Gamma overview](../../platform-management/overview.md).

## Compatibility

The Edge Daemon is available for macOS only, on Apple Silicon and Intel. It supports traffic interception for Claude Code through the Anthropic API.

## Next steps

If you're new to Edge Management, work through the following steps in order:

1. [**Create the proxy APIs**](../connect/proxy-api-reference.md). Create the LLM Proxy and HTTP proxy APIs that receive the traffic the daemon forwards.
2. [**Configure Edge Management**](../connect/configure-edge-management.md). Set the gateway addresses, the intercepted domains and routes, and the shadow AI settings.
3. [**Deploy the Edge Daemon**](../connect/configure-kandji-daemon.md). Distribute the daemon to your device fleet with Kandji.
4. [**Connect Claude Code**](../connect-claude-code-to-daemon.md). Route Claude Code through the Edge Daemon, and confirm that interception works.

To install or configure the platform underneath, see the [installation guides](../../platform-management/install/README.md).
