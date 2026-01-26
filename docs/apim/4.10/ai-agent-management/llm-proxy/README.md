# LLM proxy

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>Proxy your LLMs</td><td><a href="proxy-your-llms.md">proxy-your-llms.md</a></td></tr><tr><td>Add the Token Rate Limit policy to your LLM Proxy</td><td><a href="add-the-token-rate-limit-policy-to-your-llm-proxy.md">add-the-token-rate-limit-policy-to-your-llm-proxy.md</a></td></tr><tr><td>Add the Guard Rails policy to your LLM proxy</td><td><a href="add-the-guard-rails-policy-to-your-llm-proxy.md">add-the-guard-rails-policy-to-your-llm-proxy.md</a></td></tr><tr><td>Proxy your LLMs with SDKs</td><td><a href="consume-your-llm-proxy-with-the-openai-python-sdk.md">consume-your-llm-proxy-with-the-openai-python-sdk.md</a></td></tr></tbody></table>

## What is an LLM Proxy?

An LLM Proxy is an API that is dedicated to proxying calls between an LLM consumer and an LLM provider. For example, between an AI agent and OpenAI.

The proxy exposes an OpenAI-compatible API so that the consumer does not have to adapt their APIs calls.&#x20;

The Gravitee LLM Proxy accepts OpenAI-compatible API requests and translates them to provider-specific formats. Each provider has different levels of support for OpenAI features based on their underlying API capabilities. We support only text generation.

## What Issues does it solve?

Developers might not know the details of the APIs for each LLM provider or know which LLM providers that their company has access to. The LLM proxy provides developers with a single API that they can call.

## How does it work?

The proxy automatically routes requests to the right provider and model, which depends on the consumer's request. The proxy automatically maps the request to match the format of the targeted provider.

## LLM Proxy Provider Feature Support

### **Supported Providers**

* **Gemini** - Google's Gemini API
* **Bedrock** - AWS Bedrock Converse API
* **OpenAI** - Direct passthrough (full compatibility)
* **OpenAI-compatible** - Providers following OpenAI API format

### Supported Endpoints

| Endpoint            | Gemini | Bedrock | OpenAI | OpenAI-Compatible |
| ------------------- | ------ | ------- | ------ | ----------------- |
| `/chat/completions` | ✅      | ✅       | ✅      | ✅                 |
| `/responses`        | ✅      | ✅       | ✅      | ✅                 |
| `/embeddings`       | ✅      | ✅       | ✅      | ✅                 |

### Feature Support Matrix

**Legend:**

* ✅ Fully supported
* ⚠️ Partially supported (see notes)
* ❌ Not supported

#### Chat Completions and Responses

| Feature                                                                                      | Parameter                      | Gemini | Bedrock | OpenAI | OpenAI-Compatible | Notes                                    |
| -------------------------------------------------------------------------------------------- | ------------------------------ | ------ | ------- | ------ | ----------------- | ---------------------------------------- |
| **Messages**                                                                                 | `messages` / `input`           | ✅      | ✅       | ✅      | ✅                 |                                          |
| **Max Tokens**                                                                               | `max_completion_tokens`        | ✅      | ✅       | ✅      | ✅                 | Primary token limit parameter            |
|                                                                                              | `max_tokens`                   | ✅      | ✅       | ✅      | ✅                 | Fallback for chat completions            |
|                                                                                              | `max_output_tokens`            | ✅      | ✅       | ✅      | ✅                 | For responses endpoint                   |
| **Temperature**                                                                              | `temperature`                  | ✅      | ✅       | ✅      | ✅                 | Controls randomness (0.0-2.0 for Gemini) |
| **Top P**                                                                                    | `top_p`                        | ✅      | ✅       | ✅      | ✅                 | Nucleus sampling (0.0-1.0)               |
| **Stop Sequences**                                                                           | `stop`                         | ✅      | ✅       | ✅      | ✅                 | Array of stop sequences                  |
| <p><strong>Tool calling</strong><br><br>Note: This feature is for only chat completions.</p> | <p><code>tools</code> <br></p> | ✅      | ✅       | ✅      | ✅                 |                                          |
|                                                                                              | `tool_choice`                  | ✅      | ✅       | ✅      | ✅                 |                                          |
| **Seed**                                                                                     | `seed`                         | ✅      | ❌       | ✅      | ✅                 | Reproducible generation                  |
| **Streaming**                                                                                | `stream`                       | ✅      | ❌       | ✅      | ✅                 | SSE streaming                            |
| **Frequency Penalty**                                                                        | `frequency_penalty`            | ❌      | ❌       | ✅      | ✅                 |                                          |
| **Presence Penalty**                                                                         | `presence_penalty`             | ❌      | ❌       | ✅      | ✅                 |                                          |
| **Logit Bias**                                                                               | `logit_bias`                   | ❌      | ❌       | ✅      | ✅                 |                                          |
| **Log Probabilities**                                                                        | `logprobs`                     | ❌      | ❌       | ✅      | ✅                 |                                          |
|                                                                                              | `top_logprobs`                 | ❌      | ❌       | ✅      | ✅                 |                                          |
| **Multiple Choices**                                                                         | `n`                            | ❌      | ❌       | ✅      | ✅                 |                                          |
| **User ID**                                                                                  | `user`                         | ❌      | ❌       | ✅      | ✅                 |                                          |
| **Top K**                                                                                    | `top_k`                        | ❌      | ❌       | ✅      | ✅                 |                                          |

#### Embeddings

| Feature             | Parameter         | Gemini | Bedrock | OpenAI | OpenAI-Compatible | Notes                                |
| ------------------- | ----------------- | ------ | ------- | ------ | ----------------- | ------------------------------------ |
| **Input**           | `input`           | ✅      | ⚠️      | ✅      | ✅                 | Bedrock: string only, no arrays      |
|                     |                   |        |         |        |                   | Gemini: string or array              |
| **Model**           | `model`           | ✅      | ✅       | ✅      | ✅                 | Mapped to provider model identifiers |
| **Dimensions**      | `dimensions`      | ✅      | ⚠️      | ✅      | ✅                 | Bedrock: only 256, 512, 1024         |
|                     |                   |        |         |        |                   | Gemini: flexible                     |
| **Encoding Format** | `encoding_format` | ⚠️     | ⚠️      | ✅      | ✅                 | Only "float" supported by both       |
| **User ID**         | `user`            | ❌      | ❌       | ✅      | ✅                 | Not mapped                           |

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
**Not Available:**

* Streaming mode (`stream: true`) is not implemented for any endpoint
* Returns error when streaming is requested
* All responses use direct (non-streaming) mode only
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

These constraints come from the underlying Bedrock embedding models.
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
{% tab title="No Streaming" %}
* Streaming not implemented for any endpoint
* Requires AWS EventStream format support (future work)
* All responses are complete, non-streaming only
{% endtab %}

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

#### Error Handling

**Explicit Errors Returned For:**

* Unsupported streaming when requested on Bedrock
* Array input for Bedrock embeddings
* Invalid dimension values for Bedrock embeddings
* Unsupported encoding formats
* Invalid endpoint paths or HTTP methods

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
