# Convert your APIs to MCP Servers

{% include "../.gitbook/includes/v4-proxy-only-feature.md" %}

## Overview

This guide explains how to convert an API into an MCP server.

## Prerequisites

* Create a v4 proxy API. For more information about creating a v4 proxy API, see [v4-api-creation-wizard.md](../create-apis/v4-api-creation-wizard.md "mention").
* An OpenAPI Specification to generate the MCP tools definition.&#x20;

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


    <figure><img src="../.gitbook/assets/2AA002A5-4D84-419D-8340-7600F9A9C5CD_1_201_a (2).jpeg" alt=""><figcaption></figcaption></figure>
7.  In the **Generate Tools from OpenAPI** pop-up window, add your OpenAPI specification, and then click **Regenerate Tools**.\


    <figure><img src="../.gitbook/assets/FF3E9B42-CABD-400C-9C01-45D59D1239ED_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
8.  Click **Create**.\


    <figure><img src="../.gitbook/assets/624D7AEF-49B6-433E-9340-501DD3D348ED_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
9.  Click **Deploy API**.\


    <figure><img src="../.gitbook/assets/D4C34EEE-4E78-45A8-A220-94AFF9B6FC15_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
10. (Optional) In the **Deploy your API** pop-up window, enter a deployment label.
11. Click **Deploy**. You receive the message **API successfully deployed**. \


    <figure><img src="../.gitbook/assets/B3BAF69E-C256-402C-B4F2-C45D15B9CDC9_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
