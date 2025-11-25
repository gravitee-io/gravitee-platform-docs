---
description: An overview about discover and catalog ai agents (a2a).
---

# Discover and Catalog AI Agents (A2A)

## Overview

This guide explains how to add agents to your centralized **Agent Catalog** by importing or discovering their **Agent Cards,** even if those agents are not directly exposed through the Gravitee Gateway.

As enterprises begin adopting multiple platforms and frameworks to build, deploy, and run AI agents, the landscape quickly becomes fragmented. **Agents are often developed in isolation and spread across teams, clouds, or vendors, which leads to silos that limit collaboration, reuse, and governance.**

Much like APIs and event streams, **AI agents are becoming critical building blocks** in modern enterprise architectures. They expose powerful capabilities, data processing, automation, and decisioning that can be shared across use cases, but without visibility, these assets remain underutilized.

A centralized Agent Catalog solves this problem.

By discovering and cataloging agents, along with their metadata, capabilities, and interfaces, you lay the foundation for governance and reuse. Whether an agent is public, private, or platform-bound, registering its Agent Card gives platform teams control over what exists, what’s trusted, and how it's accessed.

This delivers two key benefits:

* **Governance:** Gain visibility into the agents operating in your ecosystem, enforce ownership, and apply standards related to security, compliance, and quality.
* **Developer Experience:** Enable developers and AI engineers to easily **discover** and **build on existing agents**, reducing duplication and accelerating time to value.

Even agents not exposed via the Gravitee Gateway can be made discoverable through the Agent Catalog. This lets you manage agents alongside synchronous and asynchronous APIs, giving your developers one place to find and consume what they need, regardless of where it runs.

In this guide, you'll learn how to import AI agents from their Agent Cards, enrich them with metadata, and make them available for internal or external discovery. It’s the first step toward unlocking a federated, governable ecosystem of AI agents at scale.

## Prerequisites

* You must have an Enterprise Edition license. For more information about an Enterprise License, see [enterprise-edition.md](../readme/enterprise-edition.md "mention").
* You must enable Federation. For more information about enabling Federation, see [federation](../govern-apis/federation/ "mention").

## Create an A2A protocol integration

1.  From the **Dashboard**, click **Integrations**.

    <figure><img src="../.gitbook/assets/EBC33357-568B-44A2-8B9F-5EBF80D99197_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
2. Click **Create Integration**.
3.  Click **A2A Protocol**, and then click **Next**.

    <figure><img src="../.gitbook/assets/4736E1B1-3027-4093-91FC-F91A8A3CB3C7_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
4. In the **Create Integration** screen, add the following information:
   1. The name of the integration.
   2. (Optional) A description of the integration.
   3. The **Well-known URL** for your Agent card.
5.  Click **Create Integration**.

    <figure><img src="../.gitbook/assets/image (282) (1).png" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
Your Integration appears in the **Integrations** screen.
{% endhint %}

<figure><img src="../.gitbook/assets/5EBDA5A1-E875-4861-BF6A-0F1A97464F6C_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

## View your Agent's APIs

1.  From the **Integrations page**, click your A2A integration.

    <figure><img src="../.gitbook/assets/76AD6B3F-28DB-44E1-899F-BF030327D9A0_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
2.  From the **Overview** screen, navigate to the **Agents** section, and then click the Agent that you want to view.

    <figure><img src="../.gitbook/assets/EEAF8CAF-BDD6-43E9-A3DB-FF3DDFE3DBC9_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
The configuration screen displays the agent card for the Agent.
{% endhint %}

## Add an API to your Agent Catalog

1.  From the **Dashboard**, click **Integrations**.

    <figure><img src="../.gitbook/assets/image (283) (1).png" alt=""><figcaption></figcaption></figure>
2.  From the **Integrations page**, click your A2A integration.

    <figure><img src="../.gitbook/assets/76AD6B3F-28DB-44E1-899F-BF030327D9A0_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
3.  Click **Configuration**.

    <figure><img src="../.gitbook/assets/7D196F24-CE07-4CE4-B177-6D3FFBEA5F20 (1).jpeg" alt=""><figcaption></figcaption></figure>
4.  Navigate to **Well-known URLs**, and then add your new well-known URL.

    <figure><img src="../.gitbook/assets/2B6478B3-B09B-42DE-BA57-E42C3AE4066F (1).jpeg" alt=""><figcaption></figcaption></figure>
5.  Click **Save**.

    <figure><img src="../.gitbook/assets/CBAADA4B-CF12-4064-9500-0C2658CCC65D_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
6.  Click **Overview**.

    <figure><img src="../.gitbook/assets/54891E06-44E2-4728-84F8-6BA6D33CC6E4_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
7.  Click **Discover**. The Agent appears in the **Agents** section.

    <figure><img src="../.gitbook/assets/405A036E-DCBD-40B1-BE02-4889C9E1375F_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
