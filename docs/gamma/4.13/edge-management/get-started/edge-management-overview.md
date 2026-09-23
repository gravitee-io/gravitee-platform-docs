---
hidden: false
noIndex: false
description: >-
  Edge Management puts the Gravitee gateway between the AI agents on your
  managed devices and the providers they call. Learn what it governs in Gamma.
---

# Edge Management overview

Edge Management is Gravitee's product line for governing the AI traffic that leaves your managed devices. Gravitee doesn't replace the tools your engineers use. It puts the gateway between those tools and the AI providers they call, so a request that was previously invisible arrives at an API you own, carrying your policies, quotas, and analytics.

An **Edge Daemon** installed on each device intercepts the agents you choose and forwards their traffic to a target API on the gateway. The same daemon reports the AI providers that a device reached directly, without the gateway.

{% hint style="warning" %}
**Edge Management is a preview feature, and it isn't production-ready.** It's under active development, and authenticated, TLS-secured connections between a daemon and the gateway aren't available yet. The Edge Reactor listener is plain HTTP, and the Edge API that Edge Management publishes for an environment uses a keyless plan. That traffic is neither encrypted by the reactor nor authenticated. Don't expose these endpoints over networks you don't trust. Restrict them to a private network, a VPN, or an IP-allowlisted corporate network.
{% endhint %}

<!-- TODO: Screenshot of The Overview page of a configured environment -->

<figure><img src="../.gitbook/assets/PLACEHOLDER-edge-overview.png" alt="The Overview page of a configured environment, with the Edge API status, device, shadow AI, and proxied request counters, the Interception readiness card, and the recent activity cards"><figcaption><p>The Overview page of a configured environment.</p></figcaption></figure>

## Why Edge Management exists

Every other Gamma module governs traffic that already reaches a Gravitee endpoint. AI coding agents don't. Claude Code and the tools beside it call their provider straight from the laptop, over the engineer's own credential, and an estate that adopts them runs into the following problems:

* **The traffic never reaches your governance layer.** An LLM Proxy governs the calls that are sent to it. A tool that calls `api.anthropic.com` from a device sends nothing to it, so the policies, the quotas, and the model rules you wrote apply to none of that traffic.
* **Spend is invisible until the invoice arrives.** Tokens are billed per provider account, not per team or per repository, so nothing attributes a month's cost to the work that caused it.
* **Adoption is unmeasured.** Nobody can say which providers the fleet reaches, from how many devices, or which of them were ever approved.
* **Bringing a tool under governance means changing the tool.** Pointing each agent at a gateway by hand, on each device, doesn't survive a fleet of any size, and an engineer can undo it with one environment variable.

Edge Management answers these at the device, not at the tool. The daemon is deployed once through your MDM, and interception is configured centrally, per environment.

## What Edge Management does

Edge Management sits between your managed devices and the AI providers they call. The **Edge Daemon** runs on the device and captures traffic. The **Edge Reactor** serves each daemon its configuration and collects what it reports. The **Gamma console** is the control plane where you configure interception and read the results.

Edge Management provides the following key capabilities:

* **Interception per agent**. Declare the AI coding tools whose traffic the daemon captures, by the domains they call and the routes under those domains. See [Configure interception](../connect/configure-edge-management.md).
* **Routing to a governed API**. Each route names the target API on the gateway that receives its traffic, so an intercepted request is governed by an ordinary API with its own plans, policies, and analytics. See [Target API reference](../connect/proxy-api-reference.md).
* **Shadow AI detection**. Watch a list of provider domains and report the connections a device makes to them directly, without the gateway. See [Monitor detected shadow AI](../observe/monitor-shadow-ai-traffic.md).
* **Fleet visibility**. See which devices run a daemon, which version each one runs, and whether it still reports. See [Monitor your devices](../observe/monitor-devices.md).

{% hint style="info" %}
**The daemon doesn't apply policies on the device.** It captures the request and forwards it. Your policies, quotas, and analytics are applied by the gateway, on the target API of the route, so no request is checked or blocked before it leaves the device.
{% endhint %}

## The building blocks

Five objects carry the whole model, and each one builds on the one before it:

| Building block | What it is | Start here |
| --- | --- | --- |
| **Edge configuration** | The Edge Management configuration of one environment, created once through a guided setup. It holds the two gateway addresses, the intercepted agents, and the shadow AI domains. Creating it publishes an Edge API for the environment on the gateway. | [Set up Edge Management](../connect/set-up-edge-management.md) |
| **Edge Daemon** | A process on each managed device. It intercepts the agents you declared, forwards their traffic to the gateway, and reports its heartbeat, its metrics, and its shadow AI detections to the Edge Reactor. | [Configure Kandji to deploy the Edge Daemon](../connect/configure-kandji-daemon.md) |
| **Intercepted agent** | An AI coding tool whose traffic the daemon captures. It owns the domains it calls, the routes under those domains, the decoder format used to read its usage, and a vendor label used in reporting. | [Configure interception](../connect/configure-edge-management.md) |
| **Route** | A path under an intercepted domain, paired with the target API that receives it. The path matches exactly, unless it ends with `*`, which matches the path and everything under it. | [Configure interception](../connect/configure-edge-management.md#routes) |
| **Target API** | The gateway API a route forwards to. It's a standard API of your gateway, with its own page, plans, policies, and analytics. Edge Management points at it and doesn't own it. | [Target API reference](../connect/proxy-api-reference.md) |

A configuration governs nothing until the devices run the daemon, and a route intercepts nothing until its target API is started and deployed. Both are separate from creating the configuration.

## How the traffic flows

Once Edge Management is set up and the daemon runs on a device, the AI traffic that leaves the device takes one of two paths.

| Path | What happens |
| --- | --- |
| **Intercepted traffic** | The daemon captures the request and forwards it to the target API you chose on the gateway. The gateway applies your policies, quotas, and analytics, then relays the request to the AI provider. This traffic appears on the **Proxied Traffic** page. |
| **Shadow AI** | The device reached an AI provider directly, without the gateway. The daemon reports that the connection happened. No traffic content is read. These connections appear on the **Detected Shadow AI** page. |

Interception works per domain. The daemon captures every request that an intercepted agent sends to one of its domains, and what happens next depends on the routes you declared for that agent. A request whose path matches a route is forwarded to that route's target API. A request that matches no route passes through to the provider untouched, unless you choose to send everything else to an API. See [Configure interception](../connect/configure-edge-management.md).

On the device, the daemon installer sets up a DNS resolver that answers for the intercepted domains, a listener on port 443, and a certificate authority that the daemon uses for those connections. The installer also sets `NODE_EXTRA_CA_CERTS` so that Node.js tools such as Claude Code trust that certificate authority. No manual trust step is required. See [Connect Claude Code to the Edge Daemon](../connect-claude-code-to-daemon.md).

## What you configure

Interception is configured per intercepted agent. An agent owns the domains it calls and the routes under those domains, and each route names the target API on the gateway that receives its traffic.

* **Claude Code** is a preset. Its domain, decoder format, and vendor are fixed, and it declares one route, `/v1/messages`. You choose the target API of that route.
* **Custom agent** lets you declare the domains, the decoder format, the vendor, and the routes yourself.
* **Codex** is listed as coming soon and can't be configured yet.

A target API is a standard API on your gateway. Pick one you already have, or let Edge Management create one from the picker. See [Target API reference](../connect/proxy-api-reference.md).

Shadow AI detection has its own configuration: a list of provider domains to watch. Watching a domain and intercepting it are independent. A detection tells you that a device reached a provider directly, and nothing is routed.

## Where things live in the console

Edge Management is a module of the Gamma console. Its pages are grouped by what you do with them.

| Group | Pages |
| --- | --- |
| **General** | **Quick Start** while the environment has no configuration, then **Overview**: a dashboard with the Edge API status, the active daemons, the recent shadow AI detections, the recent device activity, and an **Interception readiness** card that shows the verdict of each configured agent. |
| **Configuration** | **Gateway**, **Interception**, **Shadow AI**, and **Daemon deployment**. |
| **Analytics** | **Detected Shadow AI**, **Proxied Traffic**, and **Devices**. |

Until the environment has a configuration, the sidebar offers only **Quick Start**. See [Set up Edge Management](../connect/set-up-edge-management.md).

## Gateway-side requirements

The daemon connects to two endpoints on the gateway side. Both must be reachable from the devices.

| Connection | Purpose |
| --- | --- |
| **Gateway URL** | Where the daemon sends the traffic it intercepts. The Edge API published for the environment and the target APIs are served from there. |
| **Reactor URL** | Where the daemon fetches its configuration, sends its heartbeat, and reports its metrics and its shadow AI detections. The Edge Reactor listens on its own port, `18093` by default. Set `edge.server.port` in the gateway configuration to change it. |

The Edge Reactor listener is separate from the gateway's main HTTP port, so it must be exposed explicitly. On Kubernetes, see [Configure Edge Ingress](../connect/configure-edge-ingress.md).

## Use cases for Edge Management

Each of the following tables pairs an outcome with the feature that delivers it.

### Bring device AI traffic under the gateway

| Outcome | Feature |
| --- | --- |
| The LLM calls that Claude Code makes on a managed device reach an API you own, instead of going straight to the provider. | [Configure interception](../connect/configure-edge-management.md) |
| A tool with no preset is intercepted by declaring its domains, its routes, and the format its usage is read in. | [Configure interception](../connect/configure-edge-management.md#configure-an-agent) |
| Intercepted traffic lands on an API that already carries your token budgets, model rules, and logging. | [Target API reference](../connect/proxy-api-reference.md) |
| A route that has nowhere to forward to is given a working target API without leaving the interception form. | [Create the target API from the picker](../connect/configure-edge-management.md#create-the-target-api-from-the-picker) |

### Find out what your devices already do with AI

| Outcome | Feature |
| --- | --- |
| The AI providers that your fleet reaches directly, outside every policy you wrote, become visible. | [Monitor detected shadow AI](../observe/monitor-shadow-ai-traffic.md) |
| The traffic that interception did capture is inspected request by request, with the model that answered and the tokens it cost. | [Monitor proxied traffic](../observe/monitor-proxied-traffic.md) |
| A provider is watched for direct connections without being intercepted, so you can measure adoption before you govern it. | [Choose the domains to watch for shadow AI](../connect/set-up-edge-management.md#choose-the-domains-to-watch-for-shadow-ai) |

### Roll out and keep a fleet healthy

| Outcome | Feature |
| --- | --- |
| The daemon reaches a device fleet through your existing MDM rather than a manual install per machine. | [Configure Kandji to deploy the Edge Daemon](../connect/configure-kandji-daemon.md) |
| An engineer starts using an intercepted tool with no per-tool setup and no certificate to trust by hand. | [Connect Claude Code to the Edge Daemon](../connect-claude-code-to-daemon.md) |
| A route that stopped intercepting, because its target API was stopped, renamed, or repathed, is caught from one card. | [Understand the route verdicts](../connect/configure-edge-management.md#understand-the-route-verdicts) |
| The daemon versions across the fleet are checked before a configuration change that older daemons can't read. | [Monitor your devices](../observe/monitor-devices.md) |
| The Edge Reactor port is reachable from the devices when the gateway runs on Kubernetes. | [Configure Edge Ingress](../connect/configure-edge-ingress.md) |

## How Edge Management fits into Gamma

Gamma unifies its product lines under one platform: API Management, Event Stream Management, Agent Management, Authorization Management, and Edge Management. They share the following foundations:

* **A common Catalog**. This catalog holds APIs, events, tools, agents, MCP servers, and models.
* **A common authorization engine**. [Authorization Management](../../authorization-management/get-started/authorization-management-overview.md) defines fine-grained policies against those cataloged assets.
* **Common enforcement points**. The AI Gateway, API Gateway, and Event Gateway evaluate the same policies at the wire level.

Edge Management is the one module that governs traffic which wasn't sent to Gravitee in the first place. It contributes no new enforcement layer of its own. Instead, it brings device traffic to an existing one: a route's target API is an ordinary gateway API, and for Claude Code it's an [LLM Proxy](../../agent-management/build/create-an-llm-proxy.md) governed exactly like the LLM traffic that [Agent Management](../../agent-management/get-started/ai-management-overview.md) already handles. A token budget, a model rule, or an authorization policy written there covers the device traffic the moment a route points at it.

The reverse direction is the reason to start here. Shadow AI detection is the only view in Gamma of traffic that no module governs yet, which makes it the starting point for deciding what to bring under the gateway next. See [Monitor detected shadow AI](../observe/monitor-shadow-ai-traffic.md).

For the platform as a whole, and for the modules Edge Management sits beside, see the [Gamma overview](../../platform-management/overview.md).

## Compatibility

The Edge Daemon is available for macOS only, on Apple Silicon and Intel. It supports interception for Claude Code through the Anthropic API.

## Next steps

If you're new to Edge Management, work through the following steps in order:

1. [**Set up Edge Management**](../connect/set-up-edge-management.md). Create the configuration of the environment through the guided setup.
2. [**Deploy the Edge Daemon**](../connect/configure-kandji-daemon.md). Distribute the daemon to your device fleet with Kandji.
3. [**Connect Claude Code**](../connect-claude-code-to-daemon.md). Check what, if anything, you have to do on the device, and confirm that interception works.
4. [**Read the results**](../observe/monitor-proxied-traffic.md). Check that intercepted requests arrive, then compare them with what the fleet still sends directly.

To install or configure the platform underneath, see the [installation guides](../../platform-management/install/README.md).
