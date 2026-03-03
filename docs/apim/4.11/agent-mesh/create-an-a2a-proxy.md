---
description: An overview about set up an ai agent (a2a) proxy.
metaLinks:
  alternates:
    - create-an-a2a-proxy.md
---

# Set Up an AI Agent (A2A) Proxy

{% hint style="warning" %}
This feature only works with v4 message APIs.
{% endhint %}

## Overview

{% hint style="info" %}
What is A2A?

* The Agent-to-Agent (A2A) protocol enables standardized communication between AI agents across different platforms and frameworks.
* A2A operates through a structured client-server model, where a "client" agent creates and communicates tasks and a "remote" agent processes those tasks to provide information or execute actions.
* A2A enables dynamic, multimodal communication between different agents functioning as peers. It's how agents collaborate, delegate, and manage shared tasks.
{% endhint %}

As organizations begin to adopt AI agents across various platforms and ecosystems, a new challenge emerges to securely connect, coordinate, and control communication between autonomous agents.

Gravitee's A2A (Agent-to-Agent) Proxy addresses this challenge by **enabling structured, secure, and observable interactions between agents**, no matter where or how they're running.

Much like any other type of API, A2A interactions benefit from being discoverable, consumable, secured, and governed via Gravitee.

Truly intelligent agents need access to both synchronous (request-response) and asynchronous (event-driven) APIs to operate effectively. Gravitee's A2A Proxy supports both, enabling agents to communicate and react in real time or over streaming protocols and empowering use cases from real-time decisioning to autonomous workflows.

The A2A Proxy reactor extends the standard HTTP proxy model with agent-specific routing capabilities. It consists of three components:

* **Reactor plugin** (`gravitee-reactor-a2a-proxy`)
* **Entrypoint connector** (`gravitee-entrypoint-a2a-proxy`)
* **Endpoint connector** (`gravitee-endpoint-a2a-proxy`)

All three components are distributed as runtime-scoped ZIP artifacts and share version `1.0.0-alpha.1`.

A2A Proxy APIs support REQUEST and RESPONSE flow phases, matching the capabilities of HTTP_PROXY and LLM_PROXY API types. Policies attached to these phases execute during request ingress and response egress. Flow selectors use HTTP path extraction logic identical to standard proxy APIs.

In the console UI, A2A Proxy appears as "A2A Proxy" with the icon identifier `gio-literal:a2a-proxy`. The API list filter uses the value `V4_A2A_PROXY` to isolate these APIs from other types.

## Prerequisites

Before creating an A2A Proxy API, ensure the following requirements are met:

* You must have the Enterprise Edition of Gravitee with an enterprise license that includes the `apim-a2a-proxy-reactor` feature enabled (AI pack). For more information about Gravitee Enterprise Edition, see [enterprise-edition.md](../readme/enterprise-edition.md "mention").
* Gravitee APIM 4.x distribution with A2A Proxy reactor plugin installed
* Target backend service accessible via HTTP or HTTPS

## Create an A2A proxy

1.  From the **Dashboard**, click **APIs.**

    <figure><img src="../.gitbook/assets/3AFC7359-4334-44DE-A2AA-3732BE173718_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
2.  Click **+Add API**.

    <figure><img src="../.gitbook/assets/4C33F7FA-43E1-43DB-86E4-3322A25B012A_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
3.  Click **Create V4 API**.

    <figure><img src="../.gitbook/assets/DAFCAA99-6D7F-4C42-9047-2B0B3DA12703_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
4. In the **Provide some details on your API** screen, enter the following details:
   1. API name
   2. Version number
   3.  (Optional) Description

       <figure><img src="../.gitbook/assets/9FB7738A-FEFA-4404-A90A-5C56373D57AE_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
5. In the **Select how you want your backend exposed** screen, select **Agent Proxy**.
6.  Click **Select my API architecture**.

    <figure><img src="../.gitbook/assets/0CCBFFE7-216B-4568-99AC-BAA064FFF12E_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
7. In the **Configure your API entrypoints** screen, enter the following details:
   1. The **Context-path** for the entrypoint.
   2. (Optional) Define the interval at which heartbeats are sent to the client.
8.  Click **Validate my entrypoints**.

    <figure><img src="../.gitbook/assets/00 agent copy (1).png" alt=""><figcaption></figcaption></figure>
9.  In the **Configure your API endpoints access** screen, provide the **Target URL**. The Target URL is the Agent's address and is mandatory. It must be a valid non-empty URL.

    <figure><img src="../.gitbook/assets/4CA47921-5400-4EA4-97C4-43C928118657_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
10. Click **Validate my endpoints**.

    <figure><img src="../.gitbook/assets/0E388335-3808-408C-A522-94545A083810_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
11. In the **Security** screen, click **Validate my plans**.

    <figure><img src="../.gitbook/assets/B434E9CD-CE30-4CEF-9D51-260356E28546_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
12. In the **Review your API configuration** screen, click **Save & Deploy**.

    <figure><img src="../.gitbook/assets/E1E23126-57E1-4FCE-B265-7E0B896F0528_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

The reactor validates that the target URL is non-null and non-empty before deployment.

## Applying policies to A2A Proxy APIs

Attach policies to A2A Proxy APIs using the policy studio interface. Flow selectors follow standard HTTP path matching rules. The following policies are supported:

| Policy | Supported Phases |
|:-------|:----------------|
| `transform-headers` | REQUEST, RESPONSE |
| `assign-attributes` | REQUEST, RESPONSE |
| `callout-http` | REQUEST, RESPONSE |
| `interrupt` | REQUEST, RESPONSE |
| `role-based-access-control` | REQUEST |
| `ipfiltering` | REQUEST |
| `ai-prompt-guard-rails` | REQUEST |
| `ratelimit` | REQUEST |
| `javascript` | REQUEST, RESPONSE |
| `groovy` | REQUEST, RESPONSE |
| `retry` | REQUEST |

Policy compatibility is enforced at design time through the policy studio UI.

## Gateway configuration

### Reactor plugin version

| Property | Description | Example |
|:---------|:------------|:--------|
| `gravitee-reactor-a2a-proxy.version` | Version of the A2A Proxy reactor plugin | `1.0.0-alpha.1` |

### Endpoint connector configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `target` | Target URL for the A2A proxy endpoint (required, cannot be null or empty) | `https://agent-backend.example.com` |

## Restrictions

* Requires enterprise license with AI pack (`apim-a2a-proxy-reactor` feature)
* Current version is `1.0.0-alpha.1` (alpha release)
* Endpoint `target` property is mandatory and must be a valid non-empty URL
* Flow selectors are limited to HTTP path-based matching (same as HTTP_PROXY and LLM_PROXY)
* Only REQUEST and RESPONSE flow phases are supported (no MESSAGE phase)
* Policy support is limited to the 11 policies explicitly updated for A2A_PROXY compatibility

