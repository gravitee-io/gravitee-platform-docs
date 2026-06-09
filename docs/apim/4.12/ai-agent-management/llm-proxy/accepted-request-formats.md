# Accepted request formats

The Gravitee LLM Proxy accepts inbound requests in three client API formats: OpenAI, Anthropic Messages, and Gemini `generateContent`. OpenAI is the LLM Proxy's internal format, so OpenAI requests pass through with minimal change. Anthropic and Gemini requests are normalized to OpenAI Chat Completions format before the policy chain and the backend provider mapping run, and the response is converted back to the format the client used.

This means you can point an OpenAI, Anthropic, or Gemini SDK at the same LLM Proxy and get responses in that same format, regardless of which backend provider the LLM Proxy is configured to call.

{% hint style="info" %}
This page covers the formats you can send requests **in**, on the client side. For how the LLM Proxy maps a request **out** to each backend provider (Gemini, Bedrock, OpenAI, Anthropic, and Vertex AI), see the provider details on the [LLM proxy](README.md) overview page.
{% endhint %}

The LLM Proxy validates every request body against a JSON schema for the matched format before it forwards or normalizes the request. An invalid or empty body returns a `400` response with an OpenAI-style error object. A supported path called with an unsupported HTTP method returns `405`.

## Supported endpoints

The LLM Proxy matches an inbound request to a client format based on the request path and method.

| Client format | Path | Method |
|---|---|---|
| OpenAI Chat Completions | `/chat/completions` | `POST` |
| OpenAI Responses | `/responses` | `POST` |
| OpenAI Embeddings | `/embeddings` | `POST` |
| OpenAI Models | `/models` | `GET` |
| Anthropic Messages | `/v1/messages` | `POST` |
| Anthropic token counting | `/v1/messages/count_tokens` | `POST` |
| Gemini generate content | `/v1beta/models/{model}:generateContent` | `POST` |
| Gemini streaming generate content | `/v1beta/models/{model}:streamGenerateContent` | `POST` |

A request that sets `Content-Encoding: zstd` is decompressed automatically before validation. This support exists for clients such as the Codex CLI. The LLM Proxy doesn't decompress other content encodings.

## OpenAI format

OpenAI is the LLM Proxy's internal format, so OpenAI requests don't need normalization. The LLM Proxy validates the body against the OpenAI schema for the endpoint and forwards it, applying only the targeted changes described below.

Each OpenAI endpoint validates the body against a fixed set of fields. `model` and `messages` are required for `/chat/completions`. `model` and `input` are required for `/responses` and `/embeddings`. These endpoints don't allow unknown top-level fields, so a request that includes a field outside the OpenAI specification returns a `400` response.

### Chat completions

The `/chat/completions` endpoint forwards the request body unchanged, with one exception. When the request sets `"stream": true`, the LLM Proxy sets `stream_options.include_usage` to the value of the gateway `enforceUsage` setting, which defaults to `false`. This keeps token usage reporting consistent across streaming requests. If the request already includes a `stream_options` object, the LLM Proxy updates `include_usage` within it instead of replacing the object.

A minimal request body to `POST /chat/completions`:

```json
{
  "model": "gpt-4o",
  "messages": [
    {"role": "user", "content": "Hello, how are you?"}
  ]
}
```

### Responses

The `/responses` endpoint is stateless. The LLM Proxy removes `previous_response_id` from the request before forwarding it and logs a warning. The backend receives a standalone request with no server-side conversation history. To continue a conversation, include the full history in `input`.

Every response to a `/responses` request includes the `X-LLM-Proxy-Stateless: true` header.

If the backend returns a Chat Completions response (`"object": "chat.completion"`), the LLM Proxy converts it to Responses API shape before returning it. A response that's already in Responses shape is returned unchanged. The conversion maps the first choice only and maps text content. The output item status comes from the backend finish reason:

| Backend `finish_reason` | Output item `status` |
|---|---|
| `stop` | `completed` |
| `length` | `incomplete` |
| `tool_calls` | `requires_action` |
| Any other value | `completed` |

### Embeddings and models

The `/embeddings` endpoint validates `model` and `input` and forwards the body unchanged. The `/models` endpoint is a `GET` request with no body, and the backend response is returned unchanged.

## Anthropic Messages format

The LLM Proxy accepts requests in Anthropic Messages format on `/v1/messages` and `/v1/messages/count_tokens`. It normalizes the request to OpenAI Chat Completions format and converts the response back to Anthropic Messages format.

A request body requires `model`, `messages`, and `max_tokens`. Unlike the OpenAI endpoints, the Anthropic format allows additional fields. Any field the LLM Proxy doesn't map explicitly is preserved and re-applied to the request sent to the backend.

The LLM Proxy renames these fields during normalization:

| Anthropic field | OpenAI pivot field |
|---|---|
| `model` | `model` |
| `stream` | `stream` |
| `temperature` | `temperature` |
| `top_p` | `top_p` |
| `max_tokens` | `max_completion_tokens` |
| `stop_sequences` | `stop` |

A top-level `system` value becomes the first message with the `system` role. Each entry in `messages` keeps its role. Message content is handled as follows:

* A string content value is kept as-is.
* An array of `text` blocks is joined into a single string with a newline between blocks.
* A mixed content array keeps `text` blocks and converts `image` blocks to OpenAI `image_url` blocks using a base64 data URL. Block types the LLM Proxy doesn't recognize are passed through unchanged.

When the response comes back, the LLM Proxy converts a Chat Completions response to Anthropic Messages shape. A response that's already in Anthropic shape is passed through. The stop reason is mapped from the backend finish reason:

| Backend `finish_reason` | Anthropic `stop_reason` |
|---|---|
| `stop` | `end_turn` |
| `length` | `max_tokens` |
| `tool_calls` | `tool_use` |
| Any other value | `end_turn` |

Token usage maps `prompt_tokens` to `input_tokens` and `completion_tokens` to `output_tokens`.

Streaming Anthropic requests are supported. The LLM Proxy converts the backend Chat Completions event stream into the Anthropic Messages streaming protocol, emitting `message_start`, `content_block_start`, `content_block_delta`, `content_block_stop`, `message_delta`, and `message_stop` events.

## Gemini generateContent format

The LLM Proxy accepts requests in Gemini `generateContent` format on `/v1beta/models/{model}:generateContent` and `/v1beta/models/{model}:streamGenerateContent`. It normalizes the request to OpenAI Chat Completions format and converts non-streaming responses back to Gemini format.

The model name comes from the URL path, not the request body. Streaming is determined by the path: a `:streamGenerateContent` path sets `stream` to `true` in the normalized request. Query parameters aren't used to determine streaming.

A request body requires `contents`. The Gemini format allows additional fields, but the LLM Proxy maps only a defined subset and drops the rest during normalization. There's no passthrough for unmapped Gemini fields.

The LLM Proxy maps these fields:

| Gemini field | OpenAI pivot field |
|---|---|
| `contents` | `messages` |
| `systemInstruction` | first `system` message |
| `generationConfig.maxOutputTokens` | `max_completion_tokens` |
| `generationConfig.temperature` | `temperature` |
| `generationConfig.topP` | `top_p` |
| `generationConfig.stopSequences` | `stop` |

Message handling:

* Each entry in `contents` maps to a message. The `model` role becomes `assistant`. Other roles are kept, and a missing role defaults to `user`.
* Only `text` parts are read. The text parts of a message are concatenated into a single string. Non-text parts aren't included.
* The text parts of `systemInstruction` are concatenated into the first `system` message.

Fields the LLM Proxy doesn't map are dropped and not sent to the backend. This includes `tools`, `toolConfig`, `safetySettings`, `cachedContent`, and the `generationConfig` fields `topK`, `seed`, `candidateCount`, `responseMimeType`, `presencePenalty`, and `frequencyPenalty`.

For a non-streaming request, the LLM Proxy converts a Chat Completions response to Gemini `generateContent` shape. The finish reason is mapped:

| Backend `finish_reason` | Gemini `finishReason` |
|---|---|
| `stop` | `STOP` |
| `length` | `MAX_TOKENS` |
| `tool_calls` | `TOOL_CALLS` |
| `content_filter` | `SAFETY` |
| Any other value | `STOP` |

The converted response sets `usageMetadata.promptTokenCount` from `prompt_tokens` and `usageMetadata.candidatesTokenCount` from `completion_tokens`. It doesn't include `totalTokenCount`.

For a `:streamGenerateContent` request, the LLM Proxy doesn't convert the streaming events. The client receives the backend Chat Completions event stream, with `chat.completion.chunk` events, not Gemini streaming events. A client that requires the Gemini streaming event format can't use the Gemini streaming path through the LLM Proxy.

## Token usage headers

When the LLM Proxy is configured with `injectTokenHeaders` set to `true`, which defaults to `false`, it adds these response headers when the matching value is available:

| Header | Content |
|---|---|
| `X-LLM-Proxy-Tokens-Sent` | Input (prompt) token count |
| `X-LLM-Proxy-Tokens-Received` | Output (completion) token count |
| `X-LLM-Proxy-Model` | Model name resolved by the LLM Proxy |
| `X-LLM-Proxy-Dropped-Parameters` | Comma-separated list of request parameters the backend mapper dropped |

## Limitations

* The `/responses` conversion maps the first choice and text content only. Tool calls and structured outputs aren't converted.
* For a `/responses` request with streaming, the event stream passes through from the backend and isn't converted to Responses streaming events.
* Gemini normalization reads `text` parts only. Other part types, such as inline data, file data, and function calls, aren't sent to the backend.
* Gemini has no passthrough. Unmapped Gemini fields, including `tools`, `toolConfig`, `safetySettings`, and most `generationConfig` fields, are dropped.
* Gemini streaming responses aren't converted to Gemini event format. The client receives OpenAI Chat Completions stream events.
* The Gemini converted response doesn't include `usageMetadata.totalTokenCount`.
