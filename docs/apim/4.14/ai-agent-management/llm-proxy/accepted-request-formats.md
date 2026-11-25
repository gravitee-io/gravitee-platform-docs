---
description: The API Management 4.13 LLM Proxy accepts OpenAI, Anthropic Messages, and Gemini request formats. Compare the supported endpoints.
---

# Accepted request formats

The Gravitee LLM Proxy accepts inbound requests in three client API formats: OpenAI, Anthropic Messages, and Gemini `generateContent`. The LLM Proxy's internal format is OpenAI Responses. Requests in every format, OpenAI Chat Completions included, are converted to OpenAI Responses format before the policy chain and the backend provider mapping run. The model's answer is then converted back to the format the client used. Requests to `/embeddings` and `/models` aren't converted. For what the policies of the LLM Proxy receive, see [Request and response bodies in policies](#request-and-response-bodies-in-policies).

This means you can point an OpenAI, Anthropic, or Gemini SDK at the same LLM Proxy and get responses in that same format. The backend provider the LLM Proxy calls doesn't change the format of a successful response.

{% hint style="info" %}
This page covers the formats you can send requests **in**, on the client side. For how the LLM Proxy maps a request **out** to each backend provider (Gemini, Bedrock, OpenAI, Anthropic, and Vertex AI), see the provider details on the [LLM proxy](README.md) overview page. The **Vertex AI** provider connects to Google Cloud's Gemini Enterprise Agent Platform (formerly Vertex AI).
{% endhint %}

The LLM Proxy doesn't check the request body against a schema. It matches the request to a client format and converts it, except on `/embeddings` and `/models`. On the paths it converts, a JSON body with no model, or with no readable message, is answered with `400` and isn't sent to the provider. A supported path called with an unsupported HTTP method returns `405`.

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

A request that sets `Content-Encoding: zstd` is decompressed automatically before the body is read. This support exists for clients such as the Codex CLI. The LLM Proxy doesn't decompress other content encodings.

## OpenAI format

The LLM Proxy converts `/chat/completions` and `/responses` requests to its internal format, like the Anthropic and Gemini formats, and builds the request it sends to the backend provider from that format. `/embeddings` and `/models` requests aren't converted.

Send the fields the provider expects: `model` and `messages` for `/chat/completions`, and `model` and `input` for `/responses` and `/embeddings`. The LLM Proxy doesn't reject unknown top-level fields. They reach the provider only when the LLM Proxy calls it on the same OpenAI API as the client.

### Chat completions

When the request sets `"stream": true` and the LLM Proxy calls the provider's Chat Completions API, the LLM Proxy sets `stream_options.include_usage` to the value of the **Track tokens during stream mode** entrypoint option, which is on by default. If the request already includes a `stream_options` object, the LLM Proxy updates `include_usage` within it instead of replacing the object.

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

When a `/responses` request carries `previous_response_id`, the conversation continues only when the request reaches the endpoint that created that response, and that endpoint calls its provider's Responses API. Otherwise, the endpoint either removes `previous_response_id` and logs a warning, which is the default, or refuses the request with `400`, depending on its configuration. To continue a conversation without `previous_response_id`, include the full history in `input`.

A response includes the `X-LLM-Proxy-Stateless: true` header when its id can't be used to continue the conversation.

The response comes back in Responses API shape, whatever API the LLM Proxy called. When the backend returns a Chat Completions response, its `finish_reason` sets the `status` of the response:

| Backend `finish_reason` | Response `status` |
|---|---|
| `length` or `max_tokens` | `incomplete`, with `incomplete_details.reason` set to `max_output_tokens` |
| `content_filter` | `incomplete`, with `incomplete_details.reason` set to `content_filter` |
| Any other value | `completed` |

### Embeddings and models

The LLM Proxy doesn't convert `/embeddings` requests. The `/models` endpoint is a `GET` request with no body. The LLM Proxy answers it without calling a backend provider, with the models that the endpoints of the LLM Proxy serve.

## Anthropic Messages format

The LLM Proxy accepts requests in Anthropic Messages format on `/v1/messages` and `/v1/messages/count_tokens`. It converts the request to its internal format and converts the response back to Anthropic Messages format. An Anthropic provider's response to `/v1/messages/count_tokens` is returned as the provider sent it.

A request body requires `model` and `messages`. Fields the LLM Proxy doesn't map reach the backend only when the LLM Proxy calls it in Anthropic Messages format. `top_k` reaches no backend provider.

These fields carry over to the internal format as follows:

| Anthropic field | Field in the internal format |
|---|---|
| `model` | `model` |
| `stream` | `stream` |
| `temperature` | `temperature` |
| `top_p` | `top_p` |
| `max_tokens` | `max_output_tokens` |
| `stop_sequences` | `stop` |

A top-level `system` value becomes `instructions`, without the non-text blocks of a `system` array. Each `user` and `assistant` entry in `messages` keeps its role. Message content is handled as follows:

* A string content value is kept as-is.
* Each `text` block of an array stays a separate text part.
* A mixed content array keeps its `text` blocks. Its `image` and `document` blocks are handled by the **Images sent by the client** and **Files sent by the client** entrypoint options of the LLM Proxy, which remove them by default.

When the response comes back, the LLM Proxy converts it from the internal format to Anthropic Messages shape, whatever the backend provider. The stop reason comes from the first row that matches the response:

| Response | Anthropic `stop_reason` |
|---|---|
| Holds a refusal | `refusal` |
| Is incomplete, for example because it reached the token limit | `max_tokens` |
| Was cancelled | `end_turn` |
| Calls a tool | `tool_use` |
| Any other response | `end_turn` |

Token usage is returned in `usage.input_tokens` and `usage.output_tokens`.

Streaming Anthropic requests are supported. The LLM Proxy converts the streamed response into the Anthropic Messages streaming protocol, with events such as `message_start`, `content_block_start`, `content_block_delta`, `content_block_stop`, `message_delta`, and `message_stop`.

## Gemini generateContent format

The LLM Proxy accepts requests in Gemini `generateContent` format on `/v1beta/models/{model}:generateContent` and `/v1beta/models/{model}:streamGenerateContent`. It converts the request to its internal format and converts the response back to Gemini format, streamed or not.

The model name comes from the URL path, not the request body. Streaming is determined by the path: a `:streamGenerateContent` path sets `stream` to `true` in the normalized request. Query parameters aren't used to determine streaming.

A request body requires `contents`. The main fields carry over to the internal format as follows:

| Gemini field | Field in the internal format |
|---|---|
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
* Image, audio, video, and file parts, sent as inline data or file data, are read along with the text parts. The **Images sent by the client**, **Audio sent by the client**, **Video sent by the client**, and **Files sent by the client** entrypoint options decide what happens to them, and remove them by default.
* The text parts of `systemInstruction` are joined into `instructions`, with a newline between parts. Its other parts are dropped.

When the backend provider receives the request in Gemini format, it also gets `safetySettings`, `cachedContent`, and `labels`. Other top-level fields that the LLM Proxy doesn't map are dropped and not sent to the backend, and so is `generationConfig.topK`.

The LLM Proxy converts the response from the internal format to Gemini `generateContent` shape. The finish reason depends on the response:

| Response | Gemini `finishReason` |
|---|---|
| Stopped by a content filter | `SAFETY` |
| Incomplete for another reason, for example because it reached the token limit | `MAX_TOKENS` |
| Failed | `SAFETY` |
| Any other response, tool calls included | `STOP` |

Token usage is returned in `usageMetadata`, with `promptTokenCount`, `candidatesTokenCount`, and `totalTokenCount`. `candidatesTokenCount` leaves out reasoning tokens and is omitted when it's zero.

For a `:streamGenerateContent` request, the client receives server-sent events whose `data` lines each hold a Gemini `GenerateContentResponse` chunk.

## Token usage headers

When the LLM Proxy is configured with `injectTokenHeaders` set to `true`, which defaults to `false`, it adds these response headers when the matching value is available:

| Header | Content |
|---|---|
| `X-LLM-Proxy-Tokens-Sent` | Input (prompt) token count |
| `X-LLM-Proxy-Tokens-Received` | Output (completion) token count |
| `X-LLM-Proxy-Model` | Model name resolved by the LLM Proxy |
| `X-LLM-Proxy-Dropped-Parameters` | Comma-separated list of request parameters the backend mapper dropped |

## Request and response bodies in policies

The policies of the LLM Proxy read and change the prompt and the model's answer in the OpenAI Responses format, whatever format the client uses:

* Before the request phase, the LLM Proxy converts the request to the OpenAI Responses format. The conversation is in the `input` array. System instructions at the start of the conversation are in `instructions` when they hold only text.
* Before the response phase, the LLM Proxy converts the model's answer to the OpenAI Responses format. The answer is in the `output` array, and the token counts, when the provider reports them, are in `usage.input_tokens` and `usage.output_tokens`. A streamed answer reaches the response phase as OpenAI Responses streaming events.
* After the response phase, the LLM Proxy converts the answer to the format the client used.

For example, in the response phase, the answer to a `/chat/completions` request has no `choices` array, so a policy that reads `choices` finds nothing. Write the policies that read or change a body for the OpenAI Responses format.

Requests to `/embeddings` and `/models` aren't converted to the OpenAI Responses format, and neither are their answers. An answer the provider sends with a status of 300 or above isn't converted either. The policies of the response phase and the client receive the provider's own body.

## Limitations

* When the backend returns a Chat Completions response with several choices, only the first one reaches the client.
* `top_k` in an Anthropic request and `generationConfig.topK` in a Gemini request reach no backend provider.
* Top-level Gemini fields the LLM Proxy doesn't map are dropped, except `safetySettings`, `cachedContent`, and `labels` when the backend provider receives the request in Gemini format.
