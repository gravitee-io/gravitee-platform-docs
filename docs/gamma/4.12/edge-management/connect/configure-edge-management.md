---
description: >-
  How to configure the Edge Management settings, proxy routes, and shadow AI
  monitoring in the Gamma console.
---

# Configure Edge Management

## Overview

Edge Management is configured from a single **Configuration** page in the Gamma console. The page is split into the following sections: Gateway, Proxy, Shadow AI monitoring, and a Daemon Deployment section used to deploy the daemon to devices. For more information about using Kandji to deploy the Edge Daemon, see [Configure Kandji to deploy the Edge Daemon](configure-kandji-daemon.md).

The first time you open the page, there is no configuration. Configure the fields, and then save to create the configuration. When you save the configuration, the corresponding Edge API is published on the Gateway so the daemon's traffic can be captured.

## Configure Edge Management

To configure Edge Management, complete the following steps:

1. [Configure the Gateway](configure-edge-management.md#configure-the-gateway)
2. [Configure the Proxy](configure-edge-management.md#configure-the-proxy)
3. [Configure Shadow AI monitoring](configure-edge-management.md#configure-shadow-ai-monitoring)
4. [Save the configuration](configure-edge-management.md#save-the-configuration)

### Configure the Gateway

The Edge Daemon uses connection URLs to communicate with the Gravitee API Gateway and the Edge Reactor. To configure the Edge Daemon for the Gateway, complete the following fields:

<figure><img src="../../.gitbook/assets/edge-config-gateway (1).png" alt="Gateway section: Gateway URL and Reactor URL, locked after creation"><figcaption><p>The Gateway and Reactor URLs are locked once the configuration is created.</p></figcaption></figure>

The following table describes each field:

| Field           | Description                                                                                   |
| --------------- | --------------------------------------------------------------------------------------------- |
| **Gateway URL** | Base URL of the Gravitee API Gateway that the daemon routes traffic to.                       |
| **Reactor URL** | URL of the Edge Reactor that serves daemon configuration and collects heartbeats and metrics. |

{% hint style="info" %}
The Gateway URL and Reactor URL are locked after the configuration is first created. They cannot be changed afterwards.
{% endhint %}

### Configure the Proxy

Configure how the daemon intercepts traffic and routes it to gateway APIs.

<figure><img src="../../.gitbook/assets/edge-config-proxy (1).png" alt="Proxy section: DNS domains and routes mapping paths to gateway APIs"><figcaption><p>DNS domains to intercept, and routes mapping each path to a gateway API.</p></figcaption></figure>

Configure the following settings:

* **DNS domains (interception mode).** The domains the daemon's DNS resolver intercepts. For example, `api.anthropic.com`. Traffic to these domains is captured and routed according to the route configuration.
* **Routes.** Ordered rules that map a request path to a Gateway API. **First match wins.** Each route has the following properties:
  * A **path prefix**. For example, `/v1/messages`.
  * An **API path**. The gateway API endpoint that handles it. For example, `/interception/claude`.
  * A **provider**. This property is optional. For example, `anthropic`.

A typical Claude Code setup uses the following two routes:

| Path prefix    | API path                    | Provider    | Captured by    |
| -------------- | --------------------------- | ----------- | -------------- |
| `/v1/messages` | `/interception/claude`      | `anthropic` | LLM Proxy API  |
| `/`            | `/interception/passthrough` | `anthropic` | HTTP Proxy API |

LLM calls to `/v1/messages` are routed to the **LLM Proxy API**. All other traffic reaches the **HTTP Proxy API**.

### Configure Shadow AI monitoring

Detect direct connections to AI providers that bypass the Gateway.

<figure><img src="../../.gitbook/assets/edge-config-shadow-ai (1).png" alt="Shadow AI monitoring section: monitored domains and report interval"><figcaption><p>Monitored domains and report interval for shadow AI detection.</p></figcaption></figure>

Configure the following settings:

* **Monitored domains.** Domains to watch for non-proxied direct connections. For example, `api.openai.com`. Detection is based on TCP connection monitoring. No traffic content is inspected.
* **Report interval (seconds).** How often the daemon aggregates and reports detections. The minimum is 10 seconds and the default is 120 seconds.

### Save the configuration

The **Configuration** page has a single save action. Depending on whether a configuration already exists, the button displays one of the following labels:

* **Create configuration**. This label appears the first time you configure Edge Management. Select it to create and deploy the configuration.
* **Save changes**. This label appears when you edit an existing configuration. Select it to update and redeploy the configuration.

To discard unsaved edits and restore the last saved values, select **Reset**.

Saving always deploys the configuration. The DNS domains, routes, and shadow AI settings are pushed to daemons the next time they poll the Edge Reactor for configuration. The configuration applies without restarting the daemon.

## Next steps

* **Deploy the Edge Daemon.** See [Configure Kandji to deploy the Edge Daemon](configure-kandji-daemon.md).
* **Connect AI tools.** See [Connect Claude Code to the Edge Daemon](../connect-claude-code-to-daemon.md).
