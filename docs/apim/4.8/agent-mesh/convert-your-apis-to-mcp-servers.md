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
* The OpenAPI Specification describing your API, to generate the MCP tools definition.&#x20;

## Deploy your API as an MCP Server

1.  From the **Dashboard**, click **APIs**.  \


    <figure><img src="../.gitbook/assets/3AFC7359-4334-44DE-A2AA-3732BE173718_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
2.  Find the API that you want to convert into an MCP Server. \


    <figure><img src="../.gitbook/assets/EFADEF2D-0D48-41A3-9668-C4C2A6F806DA_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
3.  From the API menu, click **Entrypoints**. \


    <figure><img src="../.gitbook/assets/35CF5451-4B63-46D3-B173-BEBBB47EAC95_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
4. From the **Entrypoints** screen, click **MCP Entrypoint**.
5.  Click **Enable MCP**. \


    <figure><img src="../.gitbook/assets/98908DA2-8C19-43DB-B89F-7C6E5E020F22_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
6.  Click **+ Generate Tools from OpenAPI**.\


    <figure><img src="../.gitbook/assets/2AA002A5-4D84-419D-8340-7600F9A9C5CD_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
7.  In the **Generate Tools from OpenAPI** pop-up window, add your OpenAPI specification, and then click **Regenerate Tools**.\


    <figure><img src="../.gitbook/assets/FF3E9B42-CABD-400C-9C01-45D59D1239ED_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
8.  Click **Create**.\


    <figure><img src="../.gitbook/assets/624D7AEF-49B6-433E-9340-501DD3D348ED_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
9.  Click **Deploy API**.\


    <figure><img src="../.gitbook/assets/D4C34EEE-4E78-45A8-A220-94AFF9B6FC15_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
10. (Optional) In the **Deploy your API** pop-up window, enter a deployment label.
11. Click **Deploy**. You receive the message **API successfully deployed**. \


    <figure><img src="../.gitbook/assets/B3BAF69E-C256-402C-B4F2-C45D15B9CDC9_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
