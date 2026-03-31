# Consume your LLM proxy with the OpenAI Python SDK

## Overview&#x20;

This guide explains how to consume an LLM proxy with the OpenAI Python SDK.&#x20;

If you use the OpenAI SDK, you must update the client initialization to include a default header with the API Key.

## Prerequisites

* Access to one of the following LLM providers: OpenAI API, Gemini, or Bedrock, and an OpenAI-compatible LLM.
* A fully Self-Hosted Installation of APIM or a Hybrid Installation of APIM. For more information about installing APIM, see [self-hosted-installation-guides](../../self-hosted-installation-guides/ "mention") and [hybrid-installation-and-configuration-guides](../../hybrid-installation-and-configuration-guides/ "mention").
* An Enterprise License. For more information about obtaining an Enterprise license, see [enterprise-edition.md](../../readme/enterprise-edition.md "mention").
* An Open AI Python SDK. For more information about installing and configuring an OpenAI SDK, go to [Open AI Platform](https://platform.openai.com/docs/libraries?language=python).
* Complete the steps in [proxy-your-llms.md](proxy-your-llms.md "mention").

## Proxy your LLM with SDKs

*   In your SDK file, add the following configuration:<br>

    ```bash
    from openai import OpenAI

    # Configure the client with your custom header
    client = OpenAI(
        default_headers={
            "X-Gravitee-Api-Key": "YOUR_API_KEY_HERE",
            # You can add other custom headers here if needed
            # "X-Custom-Header": "CustomValue"
        },
        base_url="https://<GATEWAY_URL>/<CONTEXT_PATH>"
    )

    # Example API call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello!"}]
    )

    print(response.choices[0].message.content)
    ```

    * Replace `<YOUR_API_KEY_HERE>` with your API K.
    * Replace `<GATEWAY_URL>` with yourt GAteway URL.
    * Replace `<CONTEXT_PATH>` with the context path for LLM Proxy. For example, llmtest.

## Verification&#x20;

*   Call the proxy with the following command:<br>

    ```python
    py main.py
    ```

The response displays the content of your LLM.
