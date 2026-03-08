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

## Prerequisites

Before configuring an A2A Proxy Gateway, ensure the following requirements are met:

* You must have the Enterprise Edition of Gravitee with the `apim-ai` license pack enabled. For more information, see [Enterprise Edition](../readme/enterprise-edition.md).
* Gravitee API Management 4.10 or later
* APIM Gateway distribution path configured for plugin deployment
* APIM Management API distribution path configured for plugin deployment

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
9.  In the **Configure your API endpoints access** screen, provide the **Target URL**. The Target URL is the Agent's address and must be a non-null, non-blank string. The endpoint connector validates that the target URL is not null or blank and throws an `IllegalArgumentException` if validation fails.

    <figure><img src="../.gitbook/assets/4CA47921-5400-4EA4-97C4-43C928118657_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
10. Click **Validate my endpoints**.

    <figure><img src="../.gitbook/assets/0E388335-3808-408C-A522-94545A083810_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
11. In the **Security** screen, click **Validate my plans**.

    <figure><img src="../.gitbook/assets/B434E9CD-CE30-4CEF-9D51-260356E28546_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
12. In the **Review your API configuration** screen, click **Save & Deploy**.

    <figure><img src="../.gitbook/assets/E1E23126-57E1-4FCE-B265-7E0B896F0528_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

## Gateway configuration

### Endpoint target configuration

The A2A Proxy endpoint requires a valid target URL pointing to the agent service.

| Property | Description | Example |
|:---------|:------------|:--------|
| `target` | Target URL for the A2A proxy endpoint. Required, cannot be null or empty. | `https://agent.example.com/api` |

### Reactor plugin deployment

The reactor, entrypoint, and endpoint plugins are distributed as zip artifacts and must be deployed to the Gateway and Management API plugin directories.

| Property | Description | Example |
|:---------|:------------|:--------|
| `APIM_GW_DISTRIBUTION_PATH` | Path to APIM Gateway distribution for plugin deployment | `/opt/gravitee/gateway` |
| `APIM_MAPI_DISTRIBUTION_PATH` | Path to APIM Management API distribution for plugin deployment | `/opt/gravitee/management-api` |

## Flow phase compatibility

A2A Proxy APIs support REQUEST and RESPONSE flow phases, matching the capabilities of HTTP Proxy, HTTP Message, Native Kafka, MCP Proxy, and LLM Proxy API types. Policies compatible with these phases can be applied to A2A Proxy flows.

## Configuring flows with HTTP selectors

A2A Proxy APIs use HTTP selectors for flow routing.

1. In the flow definition, set `type: HTTP` in the selector configuration.
2. Optionally specify HTTP methods in the `methods` array to filter requests.
3. Define a path pattern if needed.
4. Attach policies to the `REQUEST` or `RESPONSE` phase arrays within the flow.

The flow validation service ensures only HTTP selectors are used. CHANNEL and CONDITION_FILTER selectors are rejected with a validation error.

## Configuring policies

Policies that support A2A Proxy APIs declare `a2a_proxy=REQUEST,RESPONSE` in their `plugin.properties` file. Compatible policies include:

* Rate limit
* Groovy
* Retry
* IP filtering
* Transform headers
* RBAC
* AI prompt guard rails
* JavaScript
* Interrupt
* HTTP callout

Configure policies in the flow definition by specifying the policy ID and configuration object in the appropriate phase array.

## Restrictions

* A2A Proxy APIs require Enterprise Edition with the `apim-ai` license pack
* Only HTTP selectors are supported; CHANNEL and CONDITION_FILTER selectors trigger validation errors
* The endpoint connector operates exclusively in REQUEST_RESPONSE mode
* Target URL must be a non-null, non-blank string
* Flow phases are limited to REQUEST and RESPONSE
* The reactor version is `1.0.0-alpha.1` (alpha release)
