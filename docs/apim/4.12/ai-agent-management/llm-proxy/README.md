# LLM proxy

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>Proxy your LLMs</td><td><a href="proxy-your-llms.md">proxy-your-llms.md</a></td></tr><tr><td>Add the Token Rate Limit policy to your LLM Proxy</td><td><a href="add-the-token-rate-limit-policy-to-your-llm-proxy.md">add-the-token-rate-limit-policy-to-your-llm-proxy.md</a></td></tr><tr><td>Add the Guard Rails policy to your LLM proxy</td><td><a href="add-the-guard-rails-policy-to-your-llm-proxy.md">add-the-guard-rails-policy-to-your-llm-proxy.md</a></td></tr><tr><td>Proxy your LLMs with SDKs</td><td><a href="consume-your-llm-proxy-with-the-openai-python-sdk.md">consume-your-llm-proxy-with-the-openai-python-sdk.md</a></td></tr></tbody></table>

## What is an LLM Proxy?

An LLM Proxy is an API that is dedicated to proxying calls between an LLM consumer and an LLM provider. For example, between an AI agent and OpenAI.

The proxy exposes an OpenAI-compatible API so that the consumer does not have to adapt their APIs calls.

The Gravitee LLM Proxy accepts OpenAI-compatible API requests and translates them to provider-specific formats. Each provider has different levels of support for OpenAI features based on their underlying API capabilities. The LLM Proxy supports only text generation.

## What Issues does it solve?

Developers might not know the details of the APIs for each LLM provider or know which LLM providers that their company has access to. The LLM proxy provides developers with a single API that they can call.

The LLM proxy also reduces token consumption and API latency through semantic caching. When users submit queries that are semantically equivalent to previously processed prompts, even if phrased differently, the proxy serves cached results without invoking the LLM backend. This reduces costs and improves response times for common or similar queries.

## How does it work?

The proxy automatically routes requests to the right provider and model, which depends on the consumer's request. The proxy automatically maps the request to match the format of the targeted provider.

## LLM Proxy Provider Feature Support

### **Supported Providers**

* **Gemini** - Google's Gemini API
* **Bedrock** - AWS Bedrock Converse API
* **OpenAI** - Direct passthrough (full compatibility)
* **OpenAI-compatible** - Providers following OpenAI API format
* **Anthropic** - Anthropic Messages API (Claude models)
* **Vertex AI** - Google Cloud Vertex AI (Gemini and Anthropic Claude models)

### Supported Endpoints

| Endpoint | Gemini | Bedrock | OpenAI | OpenAI-Compatible | Anthropic | Vertex AI (Google) | Vertex AI (Anthropic) |
| ------------------- | ------ | ------- | ------ | ----------------- | --- | ------------------ | --------------------- |
| `/chat/completions` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `/responses` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `/embeddings` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |

### Feature Support Matrix

**Legend:**

* ✅ Fully supported
* ⚠️ Partial support (see notes)
* ❌ Not supported

#### Chat Completions and Responses

| Feature | Parameter | Gemini | Bedrock | OpenAI | OpenAI-Compatible | Anthropic | Vertex AI (Google) | Vertex AI (Anthropic) | Notes |
| -------------------------------------------------------------------------------------------- | ----------------------------- | ------ | ------- | ------ | ----------------- | --- | ------------------ | --------------------- | ---------------------------------------- |
| **Messages** | `messages` / `input` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |  |
| **Max Tokens** | `max_completion_tokens` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Primary token limit parameter |
|  | `max_tokens` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Fallback for chat completions |
|  | `max_output_tokens` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | For responses endpoint |
| **Temperature** | `temperature` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Controls randomness (0.0-2.0 for Gemini) |
| **Top P** | `top_p` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Nucleus sampling (0.0-1.0) |
| **Stop Sequences** | `stop` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Array of stop sequences |
| <p><strong>Tool calling</strong><br><br>Note: This feature is for only chat completions.</p> | <p><code>tools</code><br></p> | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |  |
|  | `tool_choice` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |  |
| **Seed** | `seed` | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ | ❌ | Reproducible generation |
| **Streaming** | `stream` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | SSE streaming. Bedrock streams over the AWS EventStream protocol, decoded to SSE. |
| **Frequency Penalty** | `frequency_penalty` | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |  |
| **Presence Penalty** | `presence_penalty` | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |  |
| **Logit Bias** | `logit_bias` | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |  |
| **Log Probabilities** | `logprobs` | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |  |
|  | `top_logprobs` | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |  |
| **Multiple Choices** | `n` | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |  |
| **User ID** | `user` | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |  |
| **Top K** | `top_k` | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |  |

#### Embeddings

| Feature | Parameter | Gemini | Bedrock | OpenAI | OpenAI-Compatible | Anthropic | Vertex AI (Google) | Vertex AI (Anthropic) | Notes |
| ------------------- | ----------------- | ------ | ------- | ------ | ----------------- | --- | ------------------ | --------------------- | ------------------------------------ |
| **Input** | `input` | ✅ | ⚠️ | ✅ | ✅ | ❌ | ✅ | ❌ | Bedrock: string only, no arrays |
|  |  |  |  |  |  |  |  |  | Gemini: string or array |
| **Model** | `model` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | Mapped to provider model identifiers |
| **Dimensions** | `dimensions` | ✅ | ⚠️ | ✅ | ✅ | ❌ | ✅ | ❌ | Bedrock: only 256, 512, 1024 |
|  |  |  |  |  |  |  |  |  | Gemini: flexible |
| **Encoding Format** | `encoding_format` | ⚠️ | ⚠️ | ✅ | ✅ | ❌ | ⚠️ | ❌ | Only "float" supported by both |
| **User ID** | `user` | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | Not mapped |

### Provider-Specific Details

#### Gemini

{% tabs %}
{% tab title="Request format" %}
* Accepts OpenAI-compatible requests on all endpoints
* Transforms to Gemini's `generateContent` and `streamGenerateContent` APIs
* System messages extracted to separate `systemInstruction` field
* Assistant role automatically converted to "model" role
{% endtab %}

{% tab title="Streaming support" %}
**Chat completions**

* Full streaming support via Server-Sent Events (SSE)
* Each chunk contains incremental text deltas
* Final chunk includes finish reason and token usage
* Terminated with `[DONE]` marker

**Responses**

* Advanced multi-event streaming
* Event types: `response.output_text.delta`, `response.content_part.done`, `response.output_item.done`, `response.completed`
* Provides detailed metadata and event ordering
* Final event includes complete usage statistics

**Embeddings**

No streaming support (batch processing only)
{% endtab %}

{% tab title="Token usage" %}
All endpoints return accurate token counts:

* Chat Completions: `prompt_tokens`, `completion_tokens`, `total_tokens`
* Responses: `input_tokens`, `output_tokens`
* Embeddings: No token usage provided by Gemini API
{% endtab %}

{% tab title="Message handling" %}
* System messages: Multiple system messages concatenated into single instruction
* User/Assistant messages: Preserved in conversation flow with role conversion
{% endtab %}

{% tab title="Embeddings" %}
* Supports both single string and array inputs
* Flexible dimension control
* Uses batch API internally for multiple inputs
* Each input generates separate embedding in response array
{% endtab %}

{% tab title="Example" %}
**Request from the client (OpenAI format)**

```json
{
  "model": "Gemini:gemini-2.0-flash",
  "messages": [
    { "role": "system", "content": "You are a helpful assistant." },
    { "role": "user", "content": "Hello world" }
  ],
  "max_completion_tokens": 12,
  "temperature": 0.314159,
  "top_p": 0.271828,
  "stop": ["stop"],
  "seed": 1
}
```

**Request forwarded to Gemini** (`POST /v1beta/models/gemini-2.0-flash:generateContent`)

```json
{
  "contents": [
    { "role": "user", "parts": [ { "text": "Hello world" } ] }
  ],
  "systemInstruction": { "parts": [ { "text": "You are a helpful assistant." } ] },
  "generationConfig": {
    "maxOutputTokens": 12,
    "temperature": 0.314159,
    "topP": 0.271828,
    "stop": ["stop"],
    "seed": 1
  }
}
```

**Response from Gemini**

```json
{
  "candidates": [
    {
      "content": { "parts": [ { "text": "Hello world! How can I help you today?" } ], "role": "model" },
      "finishReason": "STOP"
    }
  ],
  "usageMetadata": { "promptTokenCount": 8, "candidatesTokenCount": 11, "totalTokenCount": 19 },
  "modelVersion": "gemini-2.0-flash",
  "responseId": "xWsgabPOOPClvdIP1rmqqAE"
}
```

**Response returned to the client (OpenAI format)**

```json
{
  "id": "xWsgabPOOPClvdIP1rmqqAE",
  "object": "chat.completion",
  "created": 0,
  "model": "gemini-2.0-flash",
  "choices": [
    {
      "index": 0,
      "message": { "role": "assistant", "content": "Hello world! How can I help you today?" },
      "finish_reason": "stop"
    }
  ],
  "usage": { "prompt_tokens": 8, "completion_tokens": 11 }
}
```
{% endtab %}
{% endtabs %}

**Finish Reasons**

| Gemini               | OpenAI           | Description                    |
| -------------------- | ---------------- | ------------------------------ |
| `STOP`               | `stop`           | Natural completion             |
| `MAX_TOKENS`         | `length`         | Token limit reached            |
| `PROHIBITED_CONTENT` | `content_filter` | Content filtered               |
| `SPII`               | `content_filter` | Sensitive information detected |

#### Bedrock

{% tabs %}
{% tab title="Request Format" %}
* Accepts OpenAI-compatible requests on all endpoints
* Transforms to AWS Bedrock Converse API format
* System messages extracted to separate `system` array
* Uses unified Converse API for chat and responses endpoints
{% endtab %}

{% tab title="Streaming support" %}
**Chat completions**

* Streaming support with AWS EventStream binary protocol
* Each chunk contains incremental text deltas
* Final chunk contains reason and token usage
* Terminated with `[DONE]` marker

**Responses**

* Advanced multi-event streaming
* Event types: `response.output_text.delta` and `response.completed`&#x20;
* Provides detailed metadata and event ordering.
* Final event includes complete usage statistics.
{% endtab %}

{% tab title="Token usage" %}
All endpoints extract and return token counts:

* Chat Completions: `prompt_tokens`, `completion_tokens`
* Responses: `input_tokens`, `output_tokens`
* Embeddings: `prompt_tokens` only (from `inputTextTokenCount`)

Token data extracted from Bedrock's usage metadata.
{% endtab %}

{% tab title="Message Handling" %}
* System messages: Each system message becomes separate content object in `system` array
* User/Assistant messages: Role names preserved (no conversion needed)
* Content: Text-only (no multi-modal support currently)
{% endtab %}

{% tab title="Embeddings" %}
**Significant Limitations:**

* Only single string input supported
* Array inputs return error
* Limited dimension support: only 256, 512, or 1024
* Each embedding requires separate API call
* Only "float" encoding format
* No streaming support. Streaming applies to chat completions and responses only

These constraints come from the underlying Bedrock embedding models.
{% endtab %}

{% tab title="Example" %}
**Request from the client (OpenAI format)**

```json
{
  "model": "Bedrock:anthropic.claude-3-sonnet-20240229-v1:0",
  "messages": [
    { "role": "system", "content": "You are a helpful assistant." },
    { "role": "user", "content": "Explain how the Bedrock API works." }
  ]
}
```

**Request forwarded to Bedrock** (`POST /model/anthropic.claude-3-sonnet-20240229-v1:0/converse`)

```json
{
  "messages": [
    { "role": "user", "content": [ { "text": "Explain how the Bedrock API works." } ] }
  ],
  "system": [ { "text": "You are a helpful assistant." } ]
}
```

**Response from Bedrock**

```json
{
  "output": {
    "message": {
      "role": "assistant",
      "content": [ { "text": "The Bedrock API exposes a unified Converse endpoint." } ]
    }
  },
  "stopReason": "end_turn",
  "usage": { "inputTokens": 26, "outputTokens": 615, "totalTokens": 641 }
}
```

**Response returned to the client (OpenAI format)**

The `id` is taken from the Bedrock `x-amzn-requestid` response header.

```json
{
  "id": "5cfbb8ff-3977-4502-80f6-d4a2b29a376a",
  "object": "chat.completion",
  "created": 0,
  "model": "anthropic.claude-3-sonnet-20240229-v1:0",
  "choices": [
    {
      "index": 0,
      "message": { "role": "assistant", "content": "The Bedrock API exposes a unified Converse endpoint." },
      "finish_reason": "stop"
    }
  ],
  "usage": { "prompt_tokens": 26, "completion_tokens": 615 }
}
```
{% endtab %}
{% endtabs %}

**Finish Reasons**

| Bedrock                         | OpenAI           | Description               |
| ------------------------------- | ---------------- | ------------------------- |
| `end_turn`                      | `stop`           | Natural completion        |
| `stop_sequence`                 | `stop`           | Hit stop sequence         |
| `max_tokens`                    | `length`         | Token limit reached       |
| `model_context_window_exceeded` | `length`         | Context window exceeded   |
| `tool_use`                      | `tool_calls`     | Tool/function requested   |
| `guardrail_intervened`          | `content_filter` | Guardrail blocked content |
| `content_filtered`              | `content_filter` | Content filtered          |

**Model Identifiers**

Bedrock requires specific model ID formats:

* Example: `anthropic.claude-3-sonnet-20240229-v1:0`
* Model availability varies by AWS region
* Ensure correct model ID format for your region

#### Anthropic

{% tabs %}
{% tab title="Request format" %}
* Accepts OpenAI-compatible requests on the `/chat/completions` and `/responses` endpoints
* Transforms to Anthropic's Messages API (`POST /v1/messages`)
* System messages are hoisted to the top-level `system` array
* Assistant role is preserved
* `tool` messages are mapped to `user` messages with `tool_result` content blocks
* Adds the required `anthropic-version` header (default `2023-06-01`)
* `max_tokens` is required by Anthropic and optional in OpenAI, so the proxy injects a default of `4096` when the request omits a token limit
{% endtab %}

{% tab title="Streaming support" %}
**Chat completions**

* Streaming support via Server-Sent Events (SSE) when `stream` is `true`
* Each chunk contains incremental text deltas
* Streaming tool calls are supported through `input_json_delta` events
* Final chunk includes the finish reason and token usage
* Terminated with the `[DONE]` marker

**Responses**

* Multi-event streaming
* Event types: `response.created`, `response.output_text.delta`, `response.function_call_arguments.delta`, `response.output_item.added`, and `response.completed`
* Final event includes complete usage statistics
* Terminated with the `[DONE]` marker
{% endtab %}

{% tab title="Token usage" %}
All supported endpoints return token counts mapped from Anthropic's `input_tokens` and `output_tokens`:

* Chat completions: `prompt_tokens`, `completion_tokens`, and `total_tokens`
* Responses: `input_tokens`, `output_tokens`, and `total_tokens`
{% endtab %}

{% tab title="Message handling" %}
* System messages: hoisted to the top-level `system` array
* User and assistant messages: preserved with role conversion
* Tool results: mapped to `user` messages with `tool_result` content blocks
{% endtab %}

{% tab title="Embeddings" %}
Embeddings aren't supported for Anthropic. The `/embeddings` endpoint returns a not-implemented response.
{% endtab %}

{% tab title="Example" %}
**Request from the client (OpenAI format)**

```json
{
  "model": "Anthropic:claude-3-5-sonnet-20240620",
  "messages": [
    { "role": "system", "content": "You are a helpful assistant." },
    { "role": "user", "content": "Hello world" }
  ],
  "max_completion_tokens": 12,
  "temperature": 0.314159,
  "top_p": 0.271828,
  "stop": ["stop"],
  "seed": 1
}
```

**Request forwarded to Anthropic** (`POST /v1/messages`, header `anthropic-version: 2023-06-01`)

The `seed` parameter is dropped because Anthropic doesn't support it.

```json
{
  "system": [ { "type": "text", "text": "You are a helpful assistant." } ],
  "messages": [
    { "role": "user", "content": [ { "type": "text", "text": "Hello world" } ] }
  ],
  "model": "claude-3-5-sonnet-20240620",
  "max_tokens": 12,
  "temperature": 0.314159,
  "top_p": 0.271828,
  "stop_sequences": ["stop"]
}
```

**Response from Anthropic**

```json
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEE",
  "type": "message",
  "role": "assistant",
  "content": [ { "type": "text", "text": "Hello! How can I help you today?" } ],
  "model": "claude-3-5-sonnet-20240620",
  "stop_reason": "end_turn",
  "usage": { "input_tokens": 12, "output_tokens": 10 }
}
```

**Response returned to the client (OpenAI format)**

```json
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEE",
  "object": "chat.completion",
  "created": 0,
  "model": "claude-3-5-sonnet-20240620",
  "choices": [
    {
      "index": 0,
      "message": { "role": "assistant", "content": "Hello! How can I help you today?" },
      "finish_reason": "stop"
    }
  ],
  "usage": { "prompt_tokens": 12, "completion_tokens": 10, "total_tokens": 22 }
}
```
{% endtab %}
{% endtabs %}

**Finish Reasons**

| Anthropic | OpenAI | Description |
| --------------- | ------------ | ----------------------- |
| `end_turn` | `stop` | Natural completion |
| `stop_sequence` | `stop` | Hit stop sequence |
| `max_tokens` | `length` | Token limit reached |
| `tool_use` | `tool_calls` | Tool/function requested |

#### Vertex AI

Vertex AI is a composite provider. It routes each request to a Vertex AI publisher based on the `publisher` setting: `google` for Gemini models (the default) or `anthropic` for Claude models. Each publisher reuses the matching Gravitee mapper and adds Vertex AI path rewriting on top.

{% tabs %}
{% tab title="Configuration" %}
* Set `provider` to `VERTEX_AI`.
* `projectId` (GCP Project ID): the Google Cloud project ID. Required.
* `location` (GCP Region): the GCP region. Default `global`. Set it to a region where your model is available.
* `publisher`: the model publisher. Use `google` for Gemini models (the default) or `anthropic` for Claude models.
* Authenticate with a GCP service account key in JSON format. The proxy fetches an access token before each request. If authentication fails, the request returns `502 Bad Gateway` with the key `GCP_AUTHENTICATION_ERROR`.
{% endtab %}

{% tab title="Publisher: google" %}
* Reuses the Gemini transformation. See the Gemini provider details above for request format, streaming, token usage, and message handling.
* Rewrites the request path to Vertex AI format. The Gemini path `/models/{model}:{action}` becomes `/v1/projects/{projectId}/locations/{location}/publishers/google/models/{model}:{action}`.
* Preserves query strings such as `?alt=sse` through the rewrite.
* Supports `/chat/completions`, `/responses`, and `/embeddings`.

**Example**

Request from the client (OpenAI format):

```json
{
  "model": "VertexAI:gemini-2.0-flash",
  "messages": [
    { "role": "system", "content": "You are a test assistant." },
    { "role": "user", "content": "Hello world" }
  ]
}
```

Gravitee forwards the request to `POST /v1/projects/{projectId}/locations/{location}/publishers/google/models/gemini-2.0-flash:generateContent`. The body uses the Gemini-native format shown in the Gemini example above.

Response from Vertex AI:

```json
{
  "candidates": [
    {
      "content": { "parts": [ { "text": "Hello from Vertex AI!" } ], "role": "model" },
      "finishReason": "STOP"
    }
  ],
  "usageMetadata": { "promptTokenCount": 8, "candidatesTokenCount": 5, "totalTokenCount": 13 },
  "modelVersion": "gemini-2.0-flash",
  "responseId": "vertex-ai-test-id"
}
```

Response returned to the client (OpenAI format):

```json
{
  "id": "vertex-ai-test-id",
  "object": "chat.completion",
  "created": 0,
  "model": "gemini-2.0-flash",
  "choices": [
    {
      "index": 0,
      "message": { "role": "assistant", "content": "Hello from Vertex AI!" },
      "finish_reason": "stop"
    }
  ],
  "usage": { "prompt_tokens": 8, "completion_tokens": 5 }
}
```
{% endtab %}

{% tab title="Publisher: anthropic" %}
* Reuses the Anthropic transformation. See the Anthropic provider details above for request format, streaming, token usage, and message handling.
* Rewrites the request path to `/v1/projects/{projectId}/locations/{location}/publishers/anthropic/models/{model}:rawPredict` for non-streaming requests, and `:streamRawPredict` for streaming requests. The action suffix comes from the `stream` field.
* Adapts the request body for Vertex AI. Removes `model` and `stream` because both come from the path, removes `context_management` and `output_config`, and adds `anthropic_version: "vertex-2023-10-16"`.
* Doesn't set the `anthropic-version` HTTP header. Vertex AI uses the body-level `anthropic_version` field instead.
* Supports `/chat/completions` and `/responses`. Embeddings aren't supported.

**Example**

Request from the client (OpenAI format):

```json
{
  "model": "VertexAI:claude-sonnet-4-20250514",
  "messages": [
    { "role": "user", "content": "Hello Claude" }
  ]
}
```

Gravitee forwards the request to `POST /v1/projects/{projectId}/locations/{location}/publishers/anthropic/models/claude-sonnet-4-20250514:rawPredict`. The body uses the Anthropic Messages format shown in the Anthropic example above, with `model` and `stream` removed and `anthropic_version: "vertex-2023-10-16"` added.

Response from Vertex AI:

```json
{
  "id": "msg_vertex_test_01",
  "type": "message",
  "role": "assistant",
  "content": [ { "type": "text", "text": "Hello from Claude on Vertex AI!" } ],
  "model": "claude-sonnet-4-20250514",
  "stop_reason": "end_turn",
  "usage": { "input_tokens": 12, "output_tokens": 8 }
}
```

Response returned to the client (OpenAI format):

```json
{
  "id": "msg_vertex_test_01",
  "object": "chat.completion",
  "created": 0,
  "model": "claude-sonnet-4-20250514",
  "choices": [
    {
      "index": 0,
      "message": { "role": "assistant", "content": "Hello from Claude on Vertex AI!" },
      "finish_reason": "stop"
    }
  ],
  "usage": { "prompt_tokens": 12, "completion_tokens": 8, "total_tokens": 20 }
}
```
{% endtab %}
{% endtabs %}

**Finish Reasons**

Finish reasons follow the configured publisher. For `google`, they match the Gemini finish reasons. For `anthropic`, they match the Anthropic finish reasons.

### Limitations and Constraints

#### Common Limitations (All Providers)

**Not Implemented Features**

The following OpenAI features are not currently supported by any provider:

* Function/tool calling
* Multi-modal inputs (images, audio, video)
* Multiple completion choices (`n` parameter)
* Logit bias control
* Log probabilities output
* Top-k sampling parameter

**Parameter Handling**

* Unsupported parameters are silently ignored (not passed to provider)
* Invalid/incompatible parameters return explicit errors
* Provider-specific constraints may limit parameter ranges

**Response Buffering**

The LLM Proxy handles response bodies differently from a generic v4 proxy API, which forwards response bytes to the client as they arrive:

* For non-streaming requests, the LLM Proxy reads the complete provider response into memory and translates it to the client format before it returns the response. The client starts receiving the response only after the provider response is complete.
* For streaming requests (`"stream": true`), the LLM Proxy translates and forwards the response chunk by chunk as it arrives from the provider.

#### Gemini-Specific Limitations

{% tabs %}
{% tab title="Embeddings" %}
* No token usage information returned
* Limited output format control
{% endtab %}

{% tab title="Streaming" %}
* Current implementation assumes single candidate response
* Multiple candidate streaming not fully implemented
{% endtab %}
{% endtabs %}

#### Bedrock-Specific Limitations

{% tabs %}
{% tab title="Embeddings" %}
* No array input support (single strings only)
* Very limited dimension options (256, 512, 1024 only)
* No batch processing
* Only "float" encoding
{% endtab %}

{% tab title="Content" %}
Warning generated if multiple content parts exist
{% endtab %}
{% endtabs %}

#### Anthropic-Specific Limitations

{% tabs %}
{% tab title="Embeddings" %}
* Embeddings aren't supported
* The `/embeddings` endpoint returns a not-implemented response
{% endtab %}
{% endtabs %}

#### Vertex AI-Specific Limitations

{% tabs %}
{% tab title="Publisher: google" %}
* Inherits all Gemini limitations
{% endtab %}

{% tab title="Publisher: anthropic" %}
* Embeddings aren't supported
* `seed` isn't supported
* `context_management` and `output_config` are removed from the request
{% endtab %}

{% tab title="Platform" %}
* Supports only the `google` and `anthropic` publishers. Other Vertex AI publishers, for example Meta Llama or Mistral, aren't supported
* The default region `global` doesn't apply to all models. Set `location` to a region where your model is available
{% endtab %}
{% endtabs %}

#### Error Handling

**Explicit Errors Returned For:**

* Unsupported streaming when requested on Bedrock
* Array input for Bedrock embeddings
* Invalid dimension values for Bedrock embeddings
* Unsupported encoding formats
* Invalid endpoint paths or HTTP methods
* GCP service account authentication failure on Vertex AI (`502 Bad Gateway`, `GCP_AUTHENTICATION_ERROR`)

**Silent Ignoring:**

* Unsupported optional parameters (e.g., `frequency_penalty`, `user`)
* These parameters are not passed to the provider but don't cause errors

#### Parameter Configuration

1. **Always specify:**
   * `model` - Ensure valid model identifier for provider
   * `max_tokens` / `max_completion_tokens` - Control output length
   * `temperature` - Control randomness
2. **Test provider compatibility:**
   * Verify required features are supported
   * Check dimension limits for embeddings
   * Validate streaming requirements
3. **Handle errors gracefully:**
   * Implement fallback for unsupported features
   * Check response for warnings about data loss
   * Monitor token usage for cost tracking

#### Embeddings Best Practices

**For Bedrock:**

* Use single string inputs only
* Stick to supported dimensions (256, 512, 1024)
* Process arrays client-side with multiple requests
* Expect higher latency for batch processing

**For Gemini:**

* Leverage array input support for batch processing
* Use flexible dimension control as needed
* Note: No token usage returned

#### Monitoring and Debugging

**Token Usage:**

* All providers return token counts in responses
* Use for cost tracking and monitoring
* Bedrock embeddings return input tokens only

**Request Tracing:**

* Bedrock: Check `x-amzn-requestid` header for AWS request ID
* Gemini: Check `responseId` field in response
* Use for debugging and support cases

**Warnings:**

* Multi-content responses may generate warnings
* Check execution context for warning messages
* Indicates potential data loss in transformation
