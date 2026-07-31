---
description: Learn how to set the target URL for an OpenAI-compatible provider on an LLM proxy endpoint.
---

# Configure an OpenAI-compatible provider

## Overview

This guide explains how to set the target URL when an LLM proxy endpoint uses the **OpenAI-compatible** provider.

Any service that exposes the OpenAI API format can back an LLM proxy endpoint, including a self-hosted model server or a managed model-serving platform. The LLM proxy calls that service the same way it calls OpenAI itself.

The target you configure is a **base URL**. The LLM proxy appends the API path from the consumer's request to that base URL when it calls the provider. A consumer calling `/chat/completions` on your LLM proxy causes the LLM proxy to call `/chat/completions` on the target. This means the target must not already end with an API path.

## Prerequisites

Before you begin, confirm that you have the following:

* A fully Self-Hosted Installation of APIM or a Hybrid Installation of APIM. For more information about installing APIM, see [self-hosted-installation-guides](../../self-hosted-installation-guides/ "mention") and [hybrid-installation-and-configuration-guides](../../hybrid-installation-and-configuration-guides/ "mention").
* An Enterprise License. For more information about obtaining an Enterprise license, see [enterprise-edition.md](../../introduction/enterprise-edition.md "mention").
* A completed LLM proxy. For more information, see [proxy-your-llms.md](proxy-your-llms.md "mention").
* A provider that exposes the OpenAI API format, and a credential that authenticates to it.

## Set the target URL

1. Log in to your APIM Management Console.
2. Select **APIs** from the left nav.
3. Select your API from the list.
4. Select **Endpoints** from the inner left nav.
5. Open the endpoint to edit.
6. From the provider list, select **OpenAI-compatible**.
7. In the target field, enter the base URL of your provider, without a trailing API path.
8. Enter the credential that authenticates to your provider.
9. Save and redeploy the API.

{% hint style="warning" %}
Don't include `/chat/completions`, `/responses`, or `/embeddings` in the target. The LLM proxy appends the path from the consumer's request, so a target that already ends with an API path produces a malformed provider URL.
{% endhint %}

Your provider's base URL is the part of its documented endpoint that precedes the API path. Some providers publish a base URL that includes a version segment, and others don't. Check your provider's own documentation for the exact base URL, and use it unchanged.

## Verify the target

1. Send a chat completion request to your LLM proxy.
2. Confirm that the response returns successfully.
3. Confirm that the response names the model your endpoint resolved. For more information about model resolution, see [override-the-model-at-runtime.md](override-the-model-at-runtime.md "mention").

## Next steps

After your provider responds through the LLM proxy, govern the traffic with the following policies:

* [add-the-guard-rails-policy-to-your-llm-proxy.md](add-the-guard-rails-policy-to-your-llm-proxy.md "mention"). This policy screens prompts for malicious content before they reach a provider.
* [add-the-token-rate-limit-policy-to-your-llm-proxy.md](add-the-token-rate-limit-policy-to-your-llm-proxy.md "mention"). This policy caps the number of tokens a consumer can use over a period of time.
* [pii-filtering.md](../../create-and-configure-apis/apply-policies/policy-reference/pii-filtering.md "mention"). This policy redacts personally identifiable information from payloads.
