# Create an A2A Proxy

{% hint style="warning" %}
This feature only works with v4 message APIs.
{% endhint %}

## Overview

This guide explains how to create a Gravitee A2A Proxy.

## Prerequisites&#x20;

* You must have the Enterprise Edition of Gravitee. For more information about Gravitee Enterprise Edition, see [open-source-vs-enterprise-edition.md](../introduction/open-source-vs-enterprise-edition.md "mention").

## Create an A2A proxy

1.  From the **Dashboard**, click **APIs.** \


    <figure><img src="../.gitbook/assets/3AFC7359-4334-44DE-A2AA-3732BE173718_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
2.  Click **+Add API**.\


    <figure><img src="../.gitbook/assets/4C33F7FA-43E1-43DB-86E4-3322A25B012A_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
3.  Click **Create V4 API**.\


    <figure><img src="../.gitbook/assets/DAFCAA99-6D7F-4C42-9047-2B0B3DA12703_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
4. In the **Provide some details on your API** screen, enter the following details:
   1. API name
   2. Version number&#x20;
   3.  (Optional) Description\


       <figure><img src="../.gitbook/assets/9FB7738A-FEFA-4404-A90A-5C56373D57AE_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
5. In the **Select how you want your backend exposed** screen, select **Agent Proxy**.
6.  Click **Select my API architecture**. \


    <figure><img src="../.gitbook/assets/0CCBFFE7-216B-4568-99AC-BAA064FFF12E_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
7. In the **Configure your API entrypoints** screen, enter the following details:
   1. The **Context-path** for the entrypoint.
   2. (Optional) Define the interval at which heartbeats are sent to the client.&#x20;
8.  Click **Validate my entrypoints**. \


    <figure><img src="../.gitbook/assets/00 agent copy.png" alt=""><figcaption></figcaption></figure>
9.  In the **Configure your API endpoints access** screen, provide the **Target URL**. The Target URL is the Agent's address. \


    <figure><img src="../.gitbook/assets/4CA47921-5400-4EA4-97C4-43C928118657_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
10. Click **Validate my endpoints**. \


    <figure><img src="../.gitbook/assets/0E388335-3808-408C-A522-94545A083810_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
11. In the **Security** screen, click **Validate my plans**. \


    <figure><img src="../.gitbook/assets/B434E9CD-CE30-4CEF-9D51-260356E28546_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
12. In the **Review your API configuration** screen, click **Save & Deploy**. \


    <figure><img src="../.gitbook/assets/E1E23126-57E1-4FCE-B265-7E0B896F0528_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
