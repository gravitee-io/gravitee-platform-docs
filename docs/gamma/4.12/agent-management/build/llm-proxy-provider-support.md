---
hidden: false
noIndex: false
description: Which OpenAI features each LLM Proxy provider supports, how requests map to each native API, and the limits that apply. Browse the full reference.
---

# LLM Proxy provider support

An LLM Proxy accepts requests in the OpenAI, Anthropic, and Gemini formats, and translates them to the native API of the provider you configured. Each provider supports a different subset of OpenAI's features, because each provider's own API does.

This page is the reference for those differences. To create a proxy, see [Create an LLM Proxy](create-an-llm-proxy.md).

## Supported providers

The following providers are available when you add a provider to a proxy:

* **OpenAI**. Direct passthrough, with full compatibility.
* **Anthropic**. The Anthropic Messages API, for Claude models.
* **Gemini**. Google's Gemini API.
* **Bedrock**. The AWS Bedrock Converse API.
* **Vertex AI**. Google Cloud's Gemini Enterprise Agent Platform, for both Gemini and Anthropic Claude models.

{% hint style="info" %}
The connector also defines an **OpenAI compatible** provider for services that follow the OpenAI API format. It isn't selectable in the console yet.
{% endhint %}

## Supported endpoints

Consumers reach these paths under the proxy's context path. The OpenAI paths carry no `/v1` segment, and the Anthropic path does. For the full explanation, see [Publish your LLM Proxy](../publish/publish-your-llm-proxy.md).

| Endpoint            | Gemini | Bedrock | OpenAI | OpenAI-Compatible | Anthropic | Vertex AI (Google) | Vertex AI (Anthropic) |
| ------------------- | ------ | ------- | ------ | ----------------- | --------- | ------------------ | --------------------- |
| `/chat/completions` | ✅      | ✅       | ✅      | ✅                 | ✅         | ✅                  | ✅                     |
| `/responses`        | ✅      | ✅       | ✅      | ✅                 | ✅         | ✅                  | ✅                     |
| `/embeddings`       | ✅      | ✅       | ✅      | ✅                 | ❌         | ✅                  | ❌                     |

To list the model identifiers a proxy accepts, send a `GET` request to `<context-path>/models`.

## Feature support matrix

The following legend applies to both matrices:

* ✅ Fully supported
* ⚠️ Partial support, described in the notes
* ❌ Not supported

### Chat completions and responses

The following table shows which request parameters each provider supports:

| Feature                | Parameter                 | Gemini | Bedrock | OpenAI | OpenAI-Compatible | Anthropic | Vertex AI (Google) | Vertex AI (Anthropic) | Notes                                    |
| ---------------------- | ------------------------- | ------ | ------- | ------ | ----------------- | --------- | ------------------ | --------------------- | ---------------------------------------- |
| **Messages**           | `messages` / `input`      | ✅      | ✅       | ✅      | ✅                 | ✅         | ✅                  | ✅                     |                                          |
| **Max tokens**         | `max_completion_tokens`   | ✅      | ✅       | ✅      | ✅                 | ✅         | ✅                  | ✅                     | Primary token limit parameter            |
|                        | `max_tokens`              | ✅      | ✅       | ✅      | ✅                 | ✅         | ✅                  | ✅                     | Fallback for chat completions            |
|                        | `max_output_tokens`       | ✅      | ✅       | ✅      | ✅                 | ✅         | ✅                  | ✅                     | For the responses endpoint               |
| **Temperature**        | `temperature`             | ✅      | ✅       | ✅      | ✅                 | ✅         | ✅                  | ✅                     | Controls randomness, 0.0 to 2.0 for Gemini |
| **Top P**              | `top_p`                   | ✅      | ✅       | ✅      | ✅                 | ✅         | ✅                  | ✅                     | Nucleus sampling, 0.0 to 1.0             |
| **Stop sequences**     | `stop`                    | ✅      | ✅       | ✅      | ✅                 | ✅         | ✅                  | ✅                     | Array of stop sequences                  |
| **Tool calling**       | `tools`                   | ✅      | ✅       | ✅      | ✅                 | ✅         | ✅                  | ✅                     | Chat completions only                    |
|                        | `tool_choice`             | ✅      | ✅       | ✅      | ✅                 | ✅         | ✅                  | ✅                     |                                          |
| **Seed**               | `seed`                    | ✅      | ❌       | ✅      | ✅                 | ❌         | ✅                  | ❌                     | Reproducible generation                  |
| **Streaming**          | `stream`                  | ✅      | ✅       | ✅      | ✅                 | ✅         | ✅                  | ✅                     | Server-Sent Events. Bedrock streams over the AWS EventStream protocol, decoded to Server-Sent Events |
| **Frequency penalty**  | `frequency_penalty`       | ❌      | ❌       | ✅      | ✅                 | ❌         | ❌                  | ❌                     |                                          |
| **Presence penalty**   | `presence_penalty`        | ❌      | ❌       | ✅      | ✅                 | ❌         | ❌                  | ❌                     |                                          |
| **Logit bias**         | `logit_bias`              | ❌      | ❌       | ✅      | ✅                 | ❌         | ❌                  | ❌                     |                                          |
| **Log probabilities**  | `logprobs`                | ❌      | ❌       | ✅      | ✅                 | ❌         | ❌                  | ❌                     |                                          |
|                        | `top_logprobs`            | ❌      | ❌       | ✅      | ✅                 | ❌         | ❌                  | ❌                     |                                          |
| **Multiple choices**   | `n`                       | ❌      | ❌       | ✅      | ✅                 | ❌         | ❌                  | ❌                     |                                          |
| **User ID**            | `user`                    | ❌      | ❌       | ✅      | ✅                 | ❌         | ❌                  | ❌                     |                                          |
| **Top K**              | `top_k`                   | ❌      | ❌       | ✅      | ✅                 | ❌         | ❌                  | ❌                     |                                          |

### Embeddings

The following table shows which embeddings parameters each provider supports:

| Feature             | Parameter         | Gemini | Bedrock | OpenAI | OpenAI-Compatible | Anthropic | Vertex AI (Google) | Vertex AI (Anthropic) | Notes                                |
| ------------------- | ----------------- | ------ | ------- | ------ | ----------------- | --------- | ------------------ | --------------------- | ------------------------------------ |
| **Input**           | `input`           | ✅      | ⚠️      | ✅      | ✅                 | ❌         | ✅                  | ❌                     | Bedrock takes a string only, not arrays. Gemini takes a string or an array |
| **Model**           | `model`           | ✅      | ✅       | ✅      | ✅                 | ❌         | ✅                  | ❌                     | Mapped to provider model identifiers |
| **Dimensions**      | `dimensions`      | ✅      | ⚠️      | ✅      | ✅                 | ❌         | ✅                  | ❌                     | Bedrock accepts 256, 512, or 1024 only. Gemini is flexible |
| **Encoding format** | `encoding_format` | ⚠️      | ⚠️      | ✅      | ✅                 | ❌         | ⚠️                  | ❌                     | Only `float` is supported            |
| **User ID**         | `user`            | ❌      | ❌       | ✅      | ✅                 | ❌         | ❌                  | ❌                     | Not mapped                           |

## Provider details

### Gemini

Requests transform to Gemini's `generateContent` and `streamGenerateContent` APIs. System messages are extracted to a separate `systemInstruction` field, and the assistant role converts to the `model` role.

The following table maps Gemini's finish reasons to their OpenAI equivalents:

| Gemini               | OpenAI           | Description                    |
| -------------------- | ---------------- | ------------------------------ |
| `STOP`               | `stop`           | Natural completion             |
| `MAX_TOKENS`         | `length`         | Token limit reached            |
| `PROHIBITED_CONTENT` | `content_filter` | Content filtered               |
| `SPII`               | `content_filter` | Sensitive information detected |

Gemini embeddings return no token usage information, and offer limited output format control. The streaming implementation assumes a single candidate response.

### Bedrock

Chat requests transform to the Bedrock Converse API at `POST /model/{id}/converse`. Embeddings use the InvokeModel API instead, at `POST /model/{id}/invoke`. Streaming arrives over the AWS EventStream protocol and is decoded to Server-Sent Events.

The following table maps Bedrock's finish reasons to their OpenAI equivalents:

| Bedrock                         | OpenAI           | Description               |
| ------------------------------- | ---------------- | ------------------------- |
| `end_turn`                      | `stop`           | Natural completion        |
| `stop_sequence`                 | `stop`           | Hit stop sequence         |
| `max_tokens`                    | `length`         | Token limit reached       |
| `model_context_window_exceeded` | `length`         | Context window exceeded   |
| `tool_use`                      | `tool_calls`     | Tool or function requested |
| `guardrail_intervened`          | `content_filter` | Guardrail blocked content |
| `content_filtered`              | `content_filter` | Content filtered          |

Bedrock model identifiers take an `anthropic.` prefix, such as `anthropic.claude-sonnet-5`. Model availability varies by AWS region, so confirm the identifier format for the region you target.

Bedrock embeddings are the most constrained of the providers. They accept a single string rather than an array, only the dimensions 256, 512, and 1024, and only `float` encoding. There is no batch processing, so process arrays client-side as multiple requests. Bedrock embeddings return input tokens only.

### Anthropic

Requests transform to the Anthropic Messages API at `POST /v1/messages`.

The following table maps Anthropic's finish reasons to their OpenAI equivalents:

| Anthropic       | OpenAI       | Description               |
| --------------- | ------------ | ------------------------- |
| `end_turn`      | `stop`       | Natural completion        |
| `stop_sequence` | `stop`       | Hit stop sequence         |
| `max_tokens`    | `length`     | Token limit reached       |
| `tool_use`      | `tool_calls` | Tool or function requested |

Anthropic doesn't support embeddings. The `/embeddings` endpoint returns a not-implemented response.

### Vertex AI

Vertex AI is a composite provider. It routes each request to a publisher based on the `publisher` setting, and each publisher reuses the matching Gravitee mapper with Gemini Enterprise Agent Platform path rewriting on top.

Configure it with the following settings:

* `projectId`. The Google Cloud project ID. Required.
* `location`. The GCP region, defaulting to `global`. Set it to a region where your model is available, because the default doesn't apply to all models.
* `publisher`. Use `google` for Gemini models, which is the default, or `anthropic` for Claude models.

Authenticate with a GCP service account key in JSON format. The proxy fetches an access token before each request. If authentication fails, the request returns `502 Bad Gateway` with the key `GCP_AUTHENTICATION_ERROR`.

With the `google` publisher, the Gemini path `/models/{model}:{action}` becomes `/v1/projects/{projectId}/locations/{location}/publishers/google/models/{model}:{action}`, and query strings such as `?alt=sse` are preserved through the rewrite.

With the `anthropic` publisher, embeddings and `seed` aren't supported, and `context_management` and `output_config` are removed from the request.

Only the `google` and `anthropic` publishers are supported. Other Gemini Enterprise Agent Platform publishers, such as Meta Llama or Mistral, aren't available.

## Response buffering

An LLM Proxy handles response bodies differently from a generic proxy, which forwards response bytes to the client as they arrive:

* For non-streaming requests, the proxy reads the complete provider response into memory and translates it to the client format before returning it. The client starts receiving the response only after the provider response is complete.
* For streaming requests, where `stream` is `true`, the proxy translates and forwards the response chunk by chunk as it arrives from the provider.

## Parameter handling

Unsupported optional parameters, such as `frequency_penalty` and `user` on a provider that doesn't accept them, are silently ignored rather than rejected. They aren't passed to the provider and don't cause an error.

Invalid or incompatible parameters return explicit errors. The proxy returns an error for the following:

* An array input for Bedrock embeddings.
* An invalid dimension value for Bedrock embeddings.
* An unsupported encoding format.
* An invalid endpoint path or HTTP method.
* A GCP service account authentication failure on Vertex AI, which returns `502 Bad Gateway` with `GCP_AUTHENTICATION_ERROR`.

## Token usage and tracing

All providers return token counts in their responses, which you can use for cost tracking. Bedrock embeddings return input tokens only, and Gemini embeddings return none.

For request tracing, Bedrock returns an AWS request ID in the `x-amzn-requestid` header, and Gemini returns a `responseId` field in the response.

A response that carries multiple content parts can generate a warning in the execution context, indicating potential data loss in the transformation.

## Next steps

* [Create an LLM Proxy](create-an-llm-proxy.md). Add a provider and expose it on a context path.
* [Configure an LLM Proxy](configure-an-llm-proxy.md). Attach policies to the proxy's flows.
* [Publish your LLM Proxy](../publish/publish-your-llm-proxy.md). Make it reachable, and learn which consumer paths to call.
