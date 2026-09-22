---
description: An API Management 4.11 LLM proxy exposes an OpenAI-compatible API you can plug into any compatible client. Follow the steps to proxy your LLM.
---

# Proxy your LLMs

## Overview

The LLM proxy exposes an OpenAI compatible API to the consumer, which you can easily plug in any OpenAI-compatible client. On the backend, the LLM proxy automatically maps and adapts requests to different LLM providers.

This allows you to leverage the Gravitee ecosystem with your LLMs. You can apply our policies, manage subscriptions and track analytics, but you also have new features tailored to LLMs such as statistics and rate limiting based on LLM tokens.

This guide explains how to set up your LLM in Gravitee.

## Prerequisites

* Access to one of the following LLM providers: OpenAI API, Gemini, or Bedrock, and an OpenAI-compatible LLM.
* A fully Self-Hosted Installation of APIM or a Hybrid Installation of APIM. For more information about installing APIM, see [self-hosted-installation-guides](../../self-hosted-installation-guides/ "mention") and [hybrid-installation-and-configuration-guides](../../hybrid-installation-and-configuration-guides/ "mention").
* An Enterprise License. For more information about obtaining an Enterprise license, see [enterprise-edition.md](../../readme/enterprise-edition.md "mention").

## Proxy your LLM

### Access the Gravitee Creation Wizard&#x20;

1.  From the **Dashboard**, click **APIs**.<br>

    <figure><img src="../../.gitbook/assets/D4FF13B1-55FB-4234-9FB6-01652747B792_1_201_a.jpeg" alt="The console dashboard with APIs highlighted in the left navigation, showing 2,642 APIs and 854 applications."><figcaption></figcaption></figure>
2.  From the **APIs** screen, click **+ Add API**.<br>

    <figure><img src="../../.gitbook/assets/DC8D3A06-3F1D-4D2B-8BC0-04F4C05592AB_1_201_a.jpeg" alt="The APIs list with the Add API button highlighted above the first page of 2,638 APIs."><figcaption></figcaption></figure>

### Create an LLM proxy API

1.  Click **Create V4 API**. <br>

    <figure><img src="../../.gitbook/assets/EFD66FA9-D429-42DB-9B38-ADD19A542064_1_201_a.jpeg" alt="The Choose API creation method page, with the Create V4 API button highlighted in the Create New API panel."><figcaption></figcaption></figure>
2. In the **Provide some details on your API**, complete the following sub-steps:
   1. In the **API name** field, type the name of your API. For example, Test.
   2. In the **Version number field**, type the version of your API. For example, 1.1
3.  Click **Validate my API details.**<br>

    <figure><img src="../../.gitbook/assets/6BF440B9-173A-4764-9B30-A46A34EE1F95_1_201_a.jpeg" alt="Step 1 of the API creation wizard, with an API name and version entered and the Validate my API details button highlighted."><figcaption></figcaption></figure>
4.  Select **AI Gateway**, and then click **Select my API architecture**.<br>

    <figure><img src="../../.gitbook/assets/E5B87DAA-DF72-4D7A-8B7D-89F6ADD383DA_1_201_a.jpeg" alt="Step 2 of the API creation wizard, with AI Gateway selected among Proxy Generic Protocol, Protocol Mediation, and Kafka Protocol."><figcaption></figcaption></figure>
5.  Select **LLM Proxy**, and click **Select my entrypoints**.<br>

    <figure><img src="../../.gitbook/assets/5DEA4566-1AC1-4878-8347-CBA831D60B94.jpeg" alt="Step 2 of the API creation wizard, with LLM Proxy selected among Agent To Agent, LLM Proxy, and MCP Proxy entrypoints."><figcaption></figcaption></figure>
6. In the **Configure your API entrypoints** screen, complete the following sub-steps:
   1. In the **Context-path** field, type the context path for your proxy. For example, llmtest.&#x20;
   2. (Optional) Turn off the **Track tokens during stream mode** toggle. If you turn off **Track tokens during stream mode**, some usage statistics and rate limiting functionality might not function correctly because some token usage is hidden.&#x20;
7.  Click **Validate my entrypoints**.<br>

    <figure><img src="../../.gitbook/assets/C2ABE3E7-EBAB-4AD8-950E-2C5203A59493_1_201_a.jpeg" alt="Step 2 of the API creation wizard at the configure stage, with virtual hosts enabled, a context path entered, and token tracking during stream mode switched on."><figcaption></figcaption></figure>
8. In the **Configure your API endpoints access** screen, complete the following sub-steps:
   1. In the **Name** field, type the name of your endpoint.&#x20;
   2. From the **Select option** dropdown menu, select the LLM provider.&#x20;
   3.  In the **Model** field, type the name of the model. <br>

       <figure><img src="../../.gitbook/assets/733F2212-3B15-4388-9CDE-500765E56935_1_201_a.jpeg" alt="Step 3 of the API creation wizard, with an OpenAI provider selected, a provider URL entered, and one model named with empty input and output token prices."><figcaption></figcaption></figure>
9.  Click **Validate my endpoints**.<br>

    <figure><img src="../../.gitbook/assets/CFF1E664-80C6-4695-A29F-1D874FE0752C_1_201_a.jpeg" alt="Step 3 of the API creation wizard scrolled to the proxy and SSL options, with no proxy, host verification on, trust all off, and the Validate my endpoints button highlighted."><figcaption></figcaption></figure>
10. Click **Validate my plans.** <br>

    <figure><img src="../../.gitbook/assets/3BA1733E-53B8-4B47-9786-DCE63E54DD37_1_201_a.jpeg" alt="Step 4 of the API creation wizard, listing one default keyless plan in standard mode with the Validate my plans button highlighted."><figcaption></figcaption></figure>
11. Click **Save and Deploy API**.<br>

    <figure><img src="../../.gitbook/assets/A9781236-67FC-4FE1-9238-7FCEE6768038_1_201_a.jpeg" alt="Step 5 of the API creation wizard, summarising the entrypoints, endpoints, model provider, and keyless plan, with the Save and Deploy API button highlighted."><figcaption></figcaption></figure>

## Verification&#x20;

To verify that your proxied your LLM, call your API using the following command:

```shellscript
curl <GATEWAY_URL>/<CONTEXT_PATH>/models
```

* Replace `<GATEWAY_URL>` with your Gateway's URL.
* Replace `<CONTEXT_PATH>` with the context path for your API.&#x20;

The response lists all of the models that you can call with that API:

```
{"object":"list","data":[{"id":"llmtest:gpt-5-mini","object":"model","owned_by":"llmtest"}]}% 
```

## Next steps

* [add-the-token-rate-limit-policy-to-your-llm-proxy.md](add-the-token-rate-limit-policy-to-your-llm-proxy.md "mention")
* [add-the-guard-rails-policy-to-your-llm-proxy.md](add-the-guard-rails-policy-to-your-llm-proxy.md "mention")
