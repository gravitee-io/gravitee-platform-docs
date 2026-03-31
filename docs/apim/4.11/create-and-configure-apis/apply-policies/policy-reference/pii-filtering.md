## Overview

The PII Filtering Policy uses AI-powered token classification models to detect and redact Personally Identifiable Information (PII) in API request and response payloads. The policy operates in real-time, applying configurable redaction rules based on AI confidence scores and PII categories. It supports standard HTTP APIs and includes a bypass mode for streaming compatibility.

## Key concepts

### Token classification models

The policy uses pre-trained AI models to identify PII entities in text. Two models are supported:

- `dslim/distilbert-NER`: General named entity recognition
- `gravitee-io/bert-small-pii-detection`: PII-optimized detection

Models are loaded into memory at runtime and require write permissions to `$GRAVITEE_HOME/models` for automatic downloads. Each model outputs token-level predictions with confidence scores (0.0–1.0) and entity labels (for example, `B-PER`, `I-LOC`, `EMAIL`).

### Dual-phase redaction

The policy operates in two phases:

- **Request phase**: PII in the request body is redacted before reaching the backend
- **Response phase**: PII in the response body is redacted before reaching the client

Both phases use the same AI model and configuration. While request filtering is always active, response filtering can be optionally disabled via the skipResponsePayloadFiltering option.

### Streaming detection

The policy automatically detects streaming requests by scanning for `"stream": true` (case-insensitive) in the request body. When streaming is detected:

- If `skipResponsePayloadFiltering=false`: The request is rejected with a 400 error
- If `skipResponsePayloadFiltering=true`: The request is allowed but only the request body is redacted

The policy detects streaming by scanning for the regex pattern `(['"])stream\1\s*:\s*true` (case-insensitive) in the request body.

### Redaction algorithm

The policy uses a BitSet to track character positions for redaction, ensuring overlapping entities are handled efficiently. Consecutive marked characters are grouped together and replaced by a single [REDACTED] placeholder, maintaining the original structure while masking the sensitive content.

### Metrics and diagnostics

The policy emits custom metrics for each detected PII category and a total count (`long_pii_total`). These metrics are added to the API analytics dashboard. For the full list of metric keys per category, see [Supported PII categories](pii-filtering.md#supported-pii-categories).

When PII is detected, the policy also logs an execution warning that includes the payload origin (request or response) and the detected labels:

```
PII detected in <request|response>: <labels>
```

The `<labels>` field lists the distinct PII categories found (for example, "PERSON, EMAIL").

<!-- Verified from PiiFilteringPolicy.java:146 — warning includes PayloadOrigin (REQUEST/RESPONSE). APIM-12708 confirmed. -->

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

| Model | Model file path | Additional files |
|:------|:----------------|:-----------------|
| `DSLIM_DISTILBERT_NER` | `onnx/model.onnx` | `tokenizer.json`, `config.json` |
| `GRAVITEE_BERT_SMALL_PII_DETECTION` | `model.quant.onnx` | `tokenizer.json`, `config.json` |

<!-- Verified from ModelEnum.java:23-29 — DSLIM uses onnx/model.onnx (subdirectory), BERT Small uses model.quant.onnx at root. -->

### Policy configuration

Configure the policy at the API plan level.

| Property | Description | Example |
|:---------|:------------|:--------|
| `resourceName` | Name of the AI Model Token Classification resource | `my-pii-detector` |
| `categories` | PII categories to detect (see [supported categories](pii-filtering.md#supported-pii-categories)) | `["PERSON", "EMAIL"]` |
| `threshold` | Minimum AI confidence score (0.0–1.0) to trigger redaction | `0.5` |
| `customMapping` | Custom label-to-category mappings | `{"CUSTOM_LABEL": "PERSON"}` |
| `skipResponsePayloadFiltering` | Skip PII filtering for response payload (required for streaming) | `false` |

The policy automatically handles BIO tagging prefixes (B-, I-, S-, E-). When a category is enabled (for example, PERSON), any model label matching that category after prefix stripping (for example, B-PERSON, I-PERSON) is redacted. Isolated I-tokens (tokens with an I- prefix that don't follow a corresponding B- token) are discarded to prevent false positives.

<!-- Verified from IOBTag.java:13-24 and RefineClassificationResults.java:51-82 — BIO entity reconstruction drops orphan I-tokens. -->

### Supported PII categories

The following table lists all supported PII categories and their corresponding analytics metric keys:

<table>
    <thead>
        <tr>
            <th width="250">Category</th>
            <th width="280">Metric key</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>PERSON</code></td>
            <td><code>long_pii_personName</code></td>
            <td>Personal names</td>
        </tr>
        <tr>
            <td><code>ORGANIZATION</code></td>
            <td><code>long_pii_organization</code></td>
            <td>Organization and company names</td>
        </tr>
        <tr>
            <td><code>LOCATION</code></td>
            <td><code>long_pii_location</code></td>
            <td>Physical addresses and location names</td>
        </tr>
        <tr>
            <td><code>EMAIL</code></td>
            <td><code>long_pii_email</code></td>
            <td>Email addresses</td>
        </tr>
        <tr>
            <td><code>PHONE</code></td>
            <td><code>long_pii_phone</code></td>
            <td>Phone numbers</td>
        </tr>
        <tr>
            <td><code>NETWORK_IDENTIFIER</code></td>
            <td><code>long_pii_networkIdentifier</code></td>
            <td>IP addresses, MAC addresses, and other network identifiers</td>
        </tr>
        <tr>
            <td><code>DEVICE_IDENTIFIER</code></td>
            <td><code>long_pii_deviceIdentifier</code></td>
            <td>Device serial numbers, IMEI, and similar identifiers</td>
        </tr>
        <tr>
            <td><code>FINANCIAL_ACCOUNT</code></td>
            <td><code>long_pii_financialAccount</code></td>
            <td>Bank account numbers, credit card numbers, and financial identifiers</td>
        </tr>
        <tr>
            <td><code>GOVERNMENT_ID</code></td>
            <td><code>long_pii_governmentId</code></td>
            <td>Passport numbers, national IDs, social security numbers, and similar</td>
        </tr>
        <tr>
            <td><code>VEHICLE_ID</code></td>
            <td><code>long_pii_vehicleId</code></td>
            <td>Vehicle identification numbers and license plates</td>
        </tr>
        <tr>
            <td><code>CREDENTIAL</code></td>
            <td><code>long_pii_credential</code></td>
            <td>Passwords, API keys, tokens, and authentication credentials</td>
        </tr>
        <tr>
            <td><code>DEMOGRAPHIC</code></td>
            <td><code>long_pii_demographic</code></td>
            <td>Age, gender, ethnicity, and other demographic data</td>
        </tr>
        <tr>
            <td><code>MISCELLANEOUS</code></td>
            <td><code>long_pii_miscellaneous</code></td>
            <td>Other PII that doesn't fit into the above categories</td>
        </tr>
    </tbody>
</table>

A total count metric (`long_pii_total`) is also emitted for every detection event.

<!-- Verified from PiiCategory.java:17-55 — all 13 categories and their exact metric key strings. -->

## Creating a PII Filtering Policy

To enable PII filtering:

1. Create an AI Model Token Classification resource in the Gateway console under Resources.

    Select a model type and save the resource.

2. Create or edit an API plan and add the PII Filtering Policy.

    Reference the resource by name, select the PII categories to detect (for example, PERSON, EMAIL), and set the confidence threshold.

3. If the API supports streaming, enable skipResponsePayloadFiltering to bypass the streaming rejection logic and allow response streams to pass through.

4. Save the plan and deploy the API.

## Creating a subscription with streaming support

For APIs that support streaming (for example, LLM APIs with `"stream": true`), configure the policy with `skipResponsePayloadFiltering=true`. This allows streaming requests to pass through while still redacting PII in the request body.

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

The Gateway console includes a new AI Model Token Classification resource type under Resources, with model selection for `dslim/distilbert-NER` and `gravitee-io/bert-small-pii-detection`.
