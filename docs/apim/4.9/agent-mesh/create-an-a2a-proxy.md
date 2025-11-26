---
description: An overview about set up an ai agent (a2a) proxy.
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

Gravitee’s A2A (Agent-to-Agent) Proxy addresses this challenge by **enabling structured, secure, and observable interactions between agents**, no matter where or how they’re running.

Much like any other type of API, A2A interactions benefit from being discoverable, consumable, secured, and governed via Gravitee.

Truly intelligent agents need access to both synchronous (request-response) and asynchronous (event-driven) APIs to operate effectively. Gravitee’s A2A Proxy supports both, enabling agents to communicate and react in real time or over streaming protocols and empowering use cases from real-time decisioning to autonomous workflows.

## Prerequisites

* You must have the Enterprise Edition of Gravitee. For more information about Gravitee Enterprise Edition, see [enterprise-edition.md](../readme/enterprise-edition.md "mention").

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
9.  In the **Configure your API endpoints access** screen, provide the **Target URL**. The Target URL is the Agent's address.

    <figure><img src="../.gitbook/assets/4CA47921-5400-4EA4-97C4-43C928118657_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
10. Click **Validate my endpoints**.

    <figure><img src="../.gitbook/assets/0E388335-3808-408C-A522-94545A083810_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
11. In the **Security** screen, click **Validate my plans**.

    <figure><img src="../.gitbook/assets/B434E9CD-CE30-4CEF-9D51-260356E28546_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
12. In the **Review your API configuration** screen, click **Save & Deploy**.

    <figure><img src="../.gitbook/assets/E1E23126-57E1-4FCE-B265-7E0B896F0528_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
