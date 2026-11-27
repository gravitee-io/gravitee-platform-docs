---
hidden: false
noIndex: false
description: An LLM Proxy accepts requests in the OpenAI, Anthropic Messages, and Gemini generateContent formats. Find the endpoints and limits for each one.
---

# Accepted request formats

An LLM Proxy accepts inbound requests in three client API formats: OpenAI, Anthropic Messages, and Gemini `generateContent`. The proxy's internal format is OpenAI Responses. Requests in every format, OpenAI Chat Completions included, are converted to OpenAI Responses before the proxy's own policies and the provider mapping run, and the model's answer is converted back to the format the client used. Requests to `/embeddings` and `/models` aren't converted. For what the policies of the proxy receive, see [Request and response bodies in policies](#request-and-response-bodies-in-policies).

The practical consequence is that an OpenAI SDK, an Anthropic SDK, and a Gemini SDK can all point at the same LLM Proxy and each get answers in its own format. The provider behind the proxy doesn't change the format of a successful answer.

{% hint style="info" %}
This page covers the formats you send requests **in**, on the client side. For how the proxy maps a request **out** to each provider, and which OpenAI features each provider supports, see [LLM Proxy provider support](llm-proxy-provider-support.md).
{% endhint %}

The proxy doesn't check the request body against a schema. It matches the request to a client format and converts it, except on `/embeddings` and `/models`. On the paths it converts, a JSON body with no readable message is answered with `400` and doesn't reach the provider, and so is an OpenAI or Anthropic body with no model. A supported path called with an unsupported method returns `405`.

## Supported endpoints

The proxy matches an inbound request to a client format on the request path and method.

| Client format | Path | Method |
| --- | --- | --- |
| OpenAI Chat Completions | `/chat/completions` | `POST` |
| OpenAI Responses | `/responses` | `POST` |
| OpenAI Embeddings | `/embeddings` | `POST` |
| OpenAI Models | `/models` | `GET` |
| Anthropic Messages | `/v1/messages` | `POST` |
| Anthropic token counting | `/v1/messages/count_tokens` | `POST` |
| Gemini generate content | `/v1beta/models/{model}:generateContent` | `POST` |
| Gemini streaming generate content | `/v1beta/models/{model}:streamGenerateContent` | `POST` |

A request that sets `Content-Encoding: zstd` is decompressed automatically before the body is read, which exists for clients such as the Codex CLI. No other content encoding is decompressed.

## OpenAI format

The proxy converts `/chat/completions` and `/responses` requests to its internal format, like the Anthropic and Gemini formats, and builds the request it sends to the provider from that format. `/embeddings` and `/models` requests aren't converted.

Send the fields the provider expects: `model` and `messages` for `/chat/completions`, and `model` and `input` for `/responses` and `/embeddings`. Unknown top-level fields aren't rejected. They reach the provider only when the proxy calls it on the same OpenAI API as the client.

### Chat completions

When the request sets `"stream": true` and the proxy calls the provider's Chat Completions API, the proxy sets `stream_options.include_usage` to the value of the **Track tokens during stream mode** entrypoint option, which is on by default. An existing `stream_options` object is updated in place rather than replaced.

A minimal request body:

```json
{
  "model": "gpt-4o",
  "messages": [
    {"role": "user", "content": "Hello, how are you?"}
  ]
}
```

### Responses

When a `/responses` request carries `previous_response_id`, the conversation continues only when the request reaches the endpoint that created that response, and that endpoint calls its provider's Responses API. Otherwise, the endpoint either removes `previous_response_id` and logs a warning, which is the default, or refuses the request with `400`, depending on its configuration. To continue a conversation without `previous_response_id`, send the full history in `input`.

An answer carries `X-LLM-Proxy-Stateless: true` when its id can't be used to continue the conversation.

The answer comes back in Responses format, whatever API the proxy called. When the provider answers in Chat Completions format, its `finish_reason` sets the `status` of the response:

| Provider `finish_reason` | Response `status` |
| --- | --- |
| `length` or `max_tokens` | `incomplete`, with `incomplete_details.reason` set to `max_output_tokens` |
| `content_filter` | `incomplete`, with `incomplete_details.reason` set to `content_filter` |
| Any other value | `completed` |

### Embeddings and models

`/embeddings` requests aren't converted to the internal format. `/models` is a `GET` with no body. The proxy answers it without calling a provider, with the models that the endpoints of the LLM Proxy serve.

## Anthropic Messages format

The proxy accepts Anthropic Messages requests on `/v1/messages` and `/v1/messages/count_tokens`, converts them to its internal format, and converts the answer to a `/v1/messages` request back to Anthropic Messages format. An Anthropic provider's answer to `/v1/messages/count_tokens` is returned as the provider sent it.

Send `model` and `messages` in the body. Fields the proxy doesn't map reach the provider only when the proxy calls it in Anthropic Messages format. `top_k` reaches no provider.

These fields carry over to the internal format as follows:

| Anthropic field | Field in the internal format |
| --- | --- |
| `model` | `model` |
| `stream` | `stream` |
| `temperature` | `temperature` |
| `top_p` | `top_p` |
| `max_tokens` | `max_output_tokens` |
| `stop_sequences` | `stop` |

A top-level `system` string becomes `instructions`. The text blocks of a `system` array become `instructions` too, unless a block carries another field, such as `cache_control`. In that case they stay at the start of `input` with the `system` role. Non-text blocks of a `system` array are dropped. Each `user` and `assistant` entry in `messages` keeps its role. Content is handled as follows:

* A string content value is kept as-is.
* Each `text` block of an array stays a separate text part.
* A mixed content array keeps its `text` blocks. Its `image` and `document` blocks are handled by the entrypoint options of the proxy, which remove them by default. See [Configure LLM Proxy entrypoints](configure-llm-proxy-entrypoints.md#edit-the-entrypoint-options).

On the way back, the answer is converted from the internal format to Anthropic Messages format, whatever the provider. The stop reason comes from the first row that matches the answer:

| Answer | Anthropic `stop_reason` |
| --- | --- |
| Holds a refusal | `refusal` |
| Is incomplete, for example because it reached the token limit | `max_tokens` |
| Was cancelled, and isn't streamed | `end_turn` |
| Calls a tool | `tool_use` |
| Any other answer | `end_turn` |

Token usage is returned in `usage.input_tokens` and `usage.output_tokens`.

Streaming is supported. The proxy converts the streamed answer into the Anthropic Messages streaming protocol, with events such as `message_start`, `content_block_start`, `content_block_delta`, `content_block_stop`, `message_delta`, and `message_stop`.

## Gemini generateContent format

The proxy accepts Gemini requests on `/v1beta/models/{model}:generateContent` and `/v1beta/models/{model}:streamGenerateContent`, converts them to its internal format, and converts the answer back to Gemini format, streamed or not.

The model name comes from the URL path, not the body. Streaming is decided by the path: a `:streamGenerateContent` path sets `stream` to `true`. Query parameters aren't consulted.

A body requires `contents`. The main fields carry over to the internal format as follows:

| Gemini field | Field in the internal format |
| --- | --- |
| `contents` | `input` |
| `systemInstruction` | `instructions` |
| `tools` | `tools` |
| `toolConfig` | `tool_choice` |
| `generationConfig.maxOutputTokens` | `max_output_tokens` |
| `generationConfig.temperature` | `temperature` |
| `generationConfig.topP` | `top_p` |
| `generationConfig.stopSequences` | `stop` |
| `generationConfig.seed` | `seed` |
| `generationConfig.presencePenalty` | `presence_penalty` |
| `generationConfig.frequencyPenalty` | `frequency_penalty` |

Message handling:

* Each entry in `contents` that has a `role` and `parts` is carried into `input`, and the other entries are skipped. The `model` role becomes `assistant`, and any other role becomes `user`.
* Image, audio, video, and file parts, sent as inline data or file data, are read along with the text parts. The same entrypoint options decide what happens to them, and remove them by default.
* The text parts of `systemInstruction` are joined into `instructions`, with a newline between parts. Its other parts are dropped.

When the provider receives the request in Gemini format, it also gets `safetySettings`, `cachedContent`, and `labels`. Other top-level fields that the proxy doesn't map are dropped, and so is `generationConfig.topK`.

The answer is converted from the internal format to Gemini `generateContent` format. The finish reason depends on the answer:

| Answer | Gemini `finishReason` |
| --- | --- |
| Stopped by a content filter | `SAFETY` |
| Incomplete for another reason, for example because it reached the token limit | `MAX_TOKENS` |
| Failed | `SAFETY` |
| Any other answer, tool calls included | `STOP` |

Token usage is returned in `usageMetadata`, with `promptTokenCount`, `candidatesTokenCount`, and `totalTokenCount`. `candidatesTokenCount` leaves out reasoning tokens and is omitted when it's zero.

For a `:streamGenerateContent` request, the client receives server-sent events whose `data` lines each hold a Gemini `GenerateContentResponse` chunk.

## Request and response bodies in policies

The policies of an LLM Proxy read and change the prompt and the model's answer in the OpenAI Responses format, whatever format the client uses:

* Before the request phase, the proxy converts the request to the OpenAI Responses format. The conversation is in the `input` array. System messages at its start are moved to `instructions` when they hold nothing but text. Otherwise they stay in `input`, and so do developer messages.
* Before the response phase, the proxy converts the model's answer to the OpenAI Responses format. The answer is in the `output` array, and the token counts, when the provider reports them, are in `usage.input_tokens` and `usage.output_tokens`. A streamed answer reaches the response phase as OpenAI Responses streaming events.
* After the response phase, the proxy converts the answer to the format the client used.

For example, in the response phase, the answer to a `/chat/completions` request has no `choices` array, so a policy that reads `choices` finds nothing. Write the policies that read or change a body for the OpenAI Responses format.

Requests to `/embeddings` and `/models` aren't converted to the OpenAI Responses format, and neither are their answers. An answer the provider sends with a status of 300 or above isn't converted either. The policies of the response phase and the client receive that answer as the provider sent it.

## Limitations

* When the provider answers in Chat Completions format with several choices, only the first one reaches the client.
* `top_k` in an Anthropic request and `generationConfig.topK` in a Gemini request reach no provider.
* Top-level Gemini fields the proxy doesn't map are dropped, except `safetySettings`, `cachedContent`, and `labels` when the provider receives the request in Gemini format.

## Next steps

* [LLM Proxy provider support](llm-proxy-provider-support.md). See how each provider maps the normalized request, and which features it supports.
* [Create an LLM Proxy](create-an-llm-proxy.md). Configure providers, models, and the context path.
