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

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
2. Click **Create Integration**.
3.  Click **A2A Protocol**, and then click **Next**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
4. In the **Create Integration** screen, add the following information:
   1. The name of the integration.
   2. (Optional) A description of the integration.
   3. The **Well-known URL** for your Agent card.
5.  Click **Create Integration**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
Your Integration appears in the **Integrations** screen.
{% endhint %}

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

## View your Agent's APIs

1.  From the **Integrations page**, click your A2A integration.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
2.  From the **Overview** screen, navigate to the **Agents** section, and then click the Agent that you want to view.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
The configuration screen displays the agent card for the Agent.
{% endhint %}

## Add an API to your Agent Catalog

1.  From the **Dashboard**, click **Integrations**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
2.  From the **Integrations page**, click your A2A integration.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
3.  Click **Configuration**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
4.  Navigate to **Well-known URLs**, and then add your new well-known URL.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
5.  Click **Save**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
6.  Click **Overview**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
7.  Click **Discover**. The Agent appears in the **Agents** section.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
