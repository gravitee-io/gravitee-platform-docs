---
hidden: false
noIndex: false
description: An LLM Proxy accepts requests in the OpenAI, Anthropic Messages, and Gemini generateContent formats. Find the endpoints and limits for each one.
---

# Accepted request formats

An LLM Proxy accepts inbound requests in three client API formats: OpenAI, Anthropic Messages, and Gemini `generateContent`. OpenAI is the proxy's internal format, so OpenAI requests pass through with minimal change. Anthropic and Gemini requests are normalized to OpenAI Chat Completions before the policy chain and the provider mapping run, and the response is converted back to the format the client used.

The practical consequence is that an OpenAI SDK, an Anthropic SDK, and a Gemini SDK can all point at the same LLM Proxy and each get answers in its own format. The provider behind the proxy doesn't change the format the client receives.

{% hint style="info" %}
This page covers the formats you send requests **in**, on the client side. For how the proxy maps a request **out** to each provider, and which OpenAI features each provider supports, see [LLM Proxy provider support](llm-proxy-provider-support.md).
{% endhint %}

The proxy doesn't validate the request body. It matches the request to a client format, normalizes it if needed, and forwards it. An empty, malformed, or incomplete body reaches the provider, which returns its own error. A supported path called with an unsupported method returns `405`.

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

OpenAI is the internal format, so these requests need no normalization. The proxy forwards the body, applying only the changes described below.

Send the fields the provider expects: `model` and `messages` for `/chat/completions`, and `model` and `input` for `/responses` and `/embeddings`. Unknown top-level fields aren't rejected — they're forwarded, and the provider decides whether to accept them.

### Chat completions

The body is forwarded unchanged, with one exception. When the request sets `"stream": true`, the proxy sets `stream_options.include_usage` from the gateway's `enforceUsage` setting, so that token reporting stays consistent across streaming requests. An existing `stream_options` object is updated in place rather than replaced.

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

The `/responses` endpoint is stateless. The proxy removes `previous_response_id` before forwarding and logs a warning, so the backend receives a standalone request with no server-side conversation history. To continue a conversation, send the full history in `input`.

Every response to a `/responses` request carries `X-LLM-Proxy-Stateless: true`.

If the backend answers with a Chat Completions response, that is `"object": "chat.completion"`, the proxy converts it to Responses shape. A response already in Responses shape is returned unchanged. The conversion maps the first choice only, and text content only. The output item status comes from the backend finish reason:

| Backend `finish_reason` | Output item `status` |
| --- | --- |
| `stop` | `completed` |
| `length` | `incomplete` |
| `tool_calls` | `requires_action` |
| Any other value | `completed` |

### Embeddings and models

`/embeddings` forwards the body unchanged. `/models` is a `GET` with no body, and the backend response is returned unchanged.

## Anthropic Messages format

The proxy accepts Anthropic Messages requests on `/v1/messages` and `/v1/messages/count_tokens`, normalizes them to OpenAI Chat Completions, and converts the response back.

A body requires `model`, `messages`, and `max_tokens`. Unlike the OpenAI endpoints, the Anthropic format allows additional fields: anything the proxy doesn't map explicitly is preserved and re-applied to the request sent to the backend.

These fields are renamed during normalization:

| Anthropic field | OpenAI pivot field |
| --- | --- |
| `model` | `model` |
| `stream` | `stream` |
| `temperature` | `temperature` |
| `top_p` | `top_p` |
| `max_tokens` | `max_completion_tokens` |
| `stop_sequences` | `stop` |

A top-level `system` value becomes the first message with the `system` role. Each entry in `messages` keeps its role. Content is handled as follows:

* A string content value is kept as-is.
* An array of `text` blocks is joined into one string, with a newline between blocks.
* A mixed content array keeps `text` blocks and converts `image` blocks to OpenAI `image_url` blocks using a base64 data URL. Unrecognized block types pass through unchanged.

On the way back, a Chat Completions response is converted to Anthropic Messages shape, and a response already in Anthropic shape passes through. The stop reason is mapped:

| Backend `finish_reason` | Anthropic `stop_reason` |
| --- | --- |
| `stop` | `end_turn` |
| `length` | `max_tokens` |
| `tool_calls` | `tool_use` |
| Any other value | `end_turn` |

Token usage maps `prompt_tokens` to `input_tokens` and `completion_tokens` to `output_tokens`.

Streaming is supported. The proxy converts the backend Chat Completions event stream into the Anthropic Messages streaming protocol, emitting `message_start`, `content_block_start`, `content_block_delta`, `content_block_stop`, `message_delta`, and `message_stop` events.

## Gemini generateContent format

The proxy accepts Gemini requests on `/v1beta/models/{model}:generateContent` and `/v1beta/models/{model}:streamGenerateContent`, normalizes them to OpenAI Chat Completions, and converts non-streaming responses back.

The model name comes from the URL path, not the body. Streaming is decided by the path: a `:streamGenerateContent` path sets `stream` to `true`. Query parameters aren't consulted.

A body requires `contents`. The Gemini format allows additional fields, but the proxy maps only the subset below and **drops the rest** — there's no passthrough on this path.

| Gemini field | OpenAI pivot field |
| --- | --- |
| `contents` | `messages` |
| `systemInstruction` | first `system` message |
| `generationConfig.maxOutputTokens` | `max_completion_tokens` |
| `generationConfig.temperature` | `temperature` |
| `generationConfig.topP` | `top_p` |
| `generationConfig.stopSequences` | `stop` |

Message handling:

* Each entry in `contents` becomes a message. The `model` role becomes `assistant`, other roles are kept, and a missing role defaults to `user`.
* Only `text` parts are read, and the text parts of a message are concatenated into one string. Non-text parts are not included.
* The text parts of `systemInstruction` are concatenated into the first `system` message.

Dropped fields include `tools`, `toolConfig`, `safetySettings`, `cachedContent`, and the `generationConfig` fields `topK`, `seed`, `candidateCount`, `responseMimeType`, `presencePenalty`, and `frequencyPenalty`.

For a non-streaming request, the Chat Completions response is converted to Gemini `generateContent` shape, with the finish reason mapped:

| Backend `finish_reason` | Gemini `finishReason` |
| --- | --- |
| `stop` | `STOP` |
| `length` | `MAX_TOKENS` |
| `tool_calls` | `TOOL_CALLS` |
| `content_filter` | `SAFETY` |
| Any other value | `STOP` |

The converted response sets `usageMetadata.promptTokenCount` from `prompt_tokens` and `usageMetadata.candidatesTokenCount` from `completion_tokens`. It doesn't include `totalTokenCount`.

For a `:streamGenerateContent` request, the streaming events aren't converted. The client receives the backend Chat Completions event stream, with `chat.completion.chunk` events rather than Gemini streaming events, so a client that requires Gemini streaming events can't use this path.

## Limitations

* The `/responses` conversion maps the first choice and text content only. Tool calls and structured outputs aren't converted.
* A streaming `/responses` request passes the backend event stream through without converting it to Responses streaming events.
* Gemini normalization reads `text` parts only. Inline data, file data, and function calls aren't sent to the backend.
* Gemini has no passthrough, so unmapped fields are dropped.
* Gemini streaming responses aren't converted to Gemini event format.
* The converted Gemini response omits `usageMetadata.totalTokenCount`.

## Next steps

* [LLM Proxy provider support](llm-proxy-provider-support.md). See how each provider maps the normalized request, and which features it supports.
* [Create an LLM Proxy](create-an-llm-proxy.md). Configure providers, models, and the context path.
