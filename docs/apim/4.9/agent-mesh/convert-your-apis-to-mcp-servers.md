---
description: An overview about expose your apis as ai-ready tools with mcp.
---

# Expose Your APIs as AI-Ready Tools with MCP

{% hint style="warning" %}
This feature only works with v4 proxy APIs.
{% endhint %}

## Overview

{% hint style="info" %}
**What is MCP?**\
The Model Context Protocol (MCP) is an emerging standard that enables AI agents to understand and interact with external tools and APIs. It defines a common interface for describing operations, authentication, and capabilities, which bridges the gap between LLMs and real-world services (APIs).
{% endhint %}

**Effortlessly transform your existing RESTful APIs into powerful, AI-ready tools for AI agents, without writing a single line of new code.** With just your OpenAPI Specification (OAS) as input, Gravitee automatically interprets and exposes your API operations as structured, actionable tools through the embedded MCP server running at the Gateway level.

This seamless process **allows AI agents to discover and invoke your APIs intelligently**, enabling use cases like automation, data analysis, and decision-making in AI-driven environments. There's no need for custom wrappers or additional configuration; your documented API becomes instantly accessible to AI agents.

In this guide, you’ll learn how to publish and expose your API operations through the Gravitee MCP server, making your APIs discoverable and usable by AI agents while preserving governance, observability, and control.

## Prerequisites

* Create a v4 proxy API. For more information about creating a v4 proxy API, see .
* The OpenAPI Specification describing your API, to generate the MCP tools definition.

## Deploy your API as an MCP Server

1.  From the **Dashboard**, click **APIs**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
2.  Find the API that you want to convert into an MCP Server.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
3.  From the API menu, click **Entrypoints**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
4. From the **Entrypoints** screen, click **MCP Entrypoint**.
5.  Click **Enable MCP**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
6.  Click **+ Generate Tools from OpenAPI**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
7.  In the **Generate Tools from OpenAPI** pop-up window, add your OpenAPI specification, and then click **Regenerate Tools**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
8.  Click **Create**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
9.  Click **Deploy API**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
10. (Optional) In the **Deploy your API** pop-up window, enter a deployment label.
11. Click **Deploy**. You receive the message **API successfully deployed**.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
