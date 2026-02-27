## Overview

The PII Filtering Policy uses AI-powered token classification models to detect and redact Personally Identifiable Information (PII) in API request and response payloads. The policy operates in real-time, applying configurable redaction rules based on AI confidence scores and PII categories. It supports both standard HTTP APIs and streaming APIs with appropriate safeguards.

## Key concepts

### Token classification models

The policy uses pre-trained AI models to identify PII entities in text. Two models are supported:

- `dslim/distilbert-NER`: General named entity recognition
- `gravitee-io/bert-small-pii-detection`: PII-optimized detection

Models are loaded into memory at runtime and require write permissions to `$GRAVITEE_HOME/models` for automatic downloads. Each model outputs token-level predictions with confidence scores (0.0–1.0) and entity labels (e.g., `B-PER`, `I-LOC`, `EMAIL`).

### Dual-phase redaction

The policy operates in two phases:

- **Request phase**: PII in the request body is redacted before reaching the backend
- **Response phase**: PII in the response body is redacted before reaching the client

Both phases use the same AI model and configuration but can be independently controlled via the `skipResponsePayloadFiltering` option.

### Streaming detection

The policy automatically detects streaming requests by scanning for `"stream": true` (case-insensitive) in the request body. When streaming is detected:

- If `skipResponsePayloadFiltering=false`: The request is rejected with a 400 error
- If `skipResponsePayloadFiltering=true`: The request is allowed but only the request body is redacted

The policy detects streaming by scanning for the regex pattern `(['"])stream\1\s*:\s*true` (case-insensitive) in the request body.

### Redaction algorithm

The policy uses a `BitSet` to track which characters in the payload should be redacted. When the AI model identifies a PII entity, the corresponding character positions are marked in the `BitSet`. Overlapping entities are automatically handled: each character is redacted exactly once. Consecutive tokens with the same base label (e.g., `B-LOC`, `I-LOC`) are merged into a single redaction. The final redacted payload replaces all marked characters with `[REDACTED]`.

### Metrics and diagnostics

The policy emits custom metrics for each detected PII category (e.g., `long_pii_person`, `long_pii_email`) and a total count (`long_pii_total`). These metrics are added to the API analytics dashboard.

When PII is detected, the policy also logs an execution warning with the format:

```
PII detected in <request|response>: <labels>
```

The `<labels>` field lists the distinct PII categories found (e.g., "PERSON, EMAIL").

### Model loading and memory

AI models are loaded into memory when the resource is first used. Model files are downloaded to `$GRAVITEE_HOME/models/<model-name>/` if not already present. The `dslim/distilbert-NER` model uses `model.onnx`, while `gravitee-io/bert-small-pii-detection` uses the quantized `model.quant.onnx` for reduced memory footprint.

Increase Java heap size and Kubernetes resource limits based on the number of APIs using the policy and the selected model size.

## Prerequisites

- Gravitee APIM 4.10.3 or later
- Enterprise license with `agent-mesh` pack (includes `apim-policy-pii-filtering` and `apim-ai-resource-token-classification` features)
- Write permissions to `$GRAVITEE_HOME/models` directory for model downloads
- Sufficient Java heap memory for model loading
- Kubernetes resource limits increased if deploying in containerized environments

## Gateway configuration

### AI resource configuration

Create an AI Model Token Classification resource before configuring the policy.

| Property | Description | Example |
|:---------|:------------|:--------|
| `model.type` | Model selection: `DSLIM_DISTILBERT_NER` or `GRAVITEE_BERT_SMALL_PII_DETECTION` | `GRAVITEE_BERT_SMALL_PII_DETECTION` |

Models are automatically downloaded to `$GRAVITEE_HOME/models/<model-name>/` with the following files:

- `model.onnx` (or `model.quant.onnx`)
- `tokenizer.json`
- `config.json`

### Policy configuration

Configure the policy at the API plan level.

| Property | Description | Example |
|:---------|:------------|:--------|
| `resourceName` | Name of the AI Model Token Classification resource | `my-pii-detector` |
| `categories` | Standard PII categories to detect (PERSON, LOCATION, EMAIL, etc.) | `["PERSON", "EMAIL"]` |
| `piiTypes` | Custom AI model labels to detect (e.g., `B-PER`, `S-EMAIL`) | `["B-PER", "I-PER", "EMAIL"]` |
| `threshold` | Minimum AI confidence score (0.0–1.0) to trigger redaction | `0.5` |
| `customMapping` | Custom label-to-category mappings | `{"CUSTOM_LABEL": "PERSON"}` |
| `skipResponsePayloadFiltering` | Skip PII filtering for response payload (required for streaming) | `false` |

The `categories` and `piiTypes` properties work together: a token is redacted if its label matches either a configured category (after normalization) or an explicit `piiTypes` entry. For example, if `categories=["PERSON"]`, both `B-PER` and `I-PER` labels are redacted.

## Creating a PII Filtering Policy

To enable PII filtering:

1. Create an AI Model Token Classification resource in the Gateway console under Resources.

    Select a model type and save the resource.

2. Create or edit an API plan and add the PII Filtering Policy.

    Reference the resource by name, select the PII categories to detect (e.g., PERSON, EMAIL), and set the confidence threshold.

3. If the API supports streaming, enable `skipResponsePayloadFiltering` to allow streaming requests while still redacting request bodies.

4. Save the plan and deploy the API.

## Creating a subscription with streaming support

For APIs that support streaming (e.g., LLM APIs with `"stream": true`), configure the policy with `skipResponsePayloadFiltering=true`. This allows streaming requests to pass through while still redacting PII in the request body.

Without this setting, streaming requests are rejected with a 400 error:

```json
{
  "error": {
    "message": "Streaming is not supported.",
    "type": "invalid_request_error",
    "param": "stream"
  }
}
```

## Restrictions

- Requires Enterprise license with `agent-mesh` pack (includes `apim-policy-pii-filtering` and `apim-ai-resource-token-classification` features)
- Supported API types: `http-proxy`, `llm-proxy`, `mcp-proxy`
- Streaming APIs require `skipResponsePayloadFiltering=true` or requests are rejected with 400 error
- Models must be downloaded to `$GRAVITEE_HOME/models` (requires write permissions)
- Confidence threshold must be between 0.0 and 1.0
- At least one PII category must be configured
- AI resource name is required and must reference an existing AI Model Token Classification resource
- Response filtering is skipped when `skipResponsePayloadFiltering=true` (only request body is redacted)
- Overlapping PII entities are merged using `BitSet` to prevent double-redaction
- Custom label mappings override default category mappings

## Related changes

The policy introduces new custom metrics (`long_pii_total`, `long_pii_<category>`) visible in the API analytics dashboard. Execution warnings are logged when PII is detected, with the format "PII detected in <request|response>: <labels>".

The Gateway console includes a new AI Model Token Classification resource type under Resources, with model selection UI for `dslim/distilbert-NER` and `gravitee-io/bert-small-pii-detection`. The policy configuration UI includes:

- Resource selector (filtered to `ai-model-token-classification` type)
- Category multi-select
- Threshold slider (0.0–1.0)
- Checkbox for `skipResponsePayloadFiltering`

Dependencies include:

- `gravitee-resource-ai-model-api` (2.2.0)
- `gravitee-inference-service` (1.3.3)
- APIM core (4.10.3)

The policy and resource are distributed as separate ZIP artifacts in the APIM distribution.
