---
description: The PII Filtering policy detects and redacts personally identifiable information in API Management 4.13 using token classification. Learn how.
---

# PII Filtering

## Overview

The PII Filtering Policy uses AI-powered token classification models to detect and redact Personally Identifiable Information (PII) in API request and response payloads. The policy operates in real-time, applying configurable redaction rules based on AI confidence scores and PII categories. It supports standard HTTP APIs and includes a bypass mode for streaming compatibility.

## Key concepts

### Token classification models

The policy uses pre-trained AI models to identify PII entities in text. Two models are supported:

- `dslim/distilbert-NER`: General named entity recognition
- `gravitee-io/bert-small-pii-detection`: PII-optimized detection

Models are loaded into memory at runtime and require write permissions to `$GRAVITEE_HOME/models` for automatic downloads. Each model outputs token-level predictions with confidence scores (0.0–1.0) and entity labels (for example, `B-PER`, `I-LOC`, `EMAIL`).

### Pattern-based detection

Before the model runs, the policy redacts values that match a fixed format. These matches don't depend on the confidence threshold, and a format is only checked when its category is selected in the policy. The following table lists the formats and the category each one counts toward:

| Format | Category |
|:-------|:---------|
| Email addresses | `EMAIL` |
| URLs with one of these schemes: `http`, `https`, `ws`, `wss`, `ftp`, `ftps`, `sftp`, `ldap`, `ldaps`, `ssh`, `telnet`, `postgres`, `postgresql`, `mysql`, `mongodb`, `redis`, `amqp`, `amqps`, `mqtt`, `mqtts`, `rtsp`, `rtsps`, `coap`, or `coaps` | `NETWORK_IDENTIFIER` |
| IPv4 and IPv6 addresses | `NETWORK_IDENTIFIER` |
| MAC addresses written with colons, hyphens, or dots | `NETWORK_IDENTIFIER` |
| Payment card numbers that pass the checksum and belong to Visa, Mastercard, American Express, Discover, Diners Club, JCB, or UnionPay | `FINANCIAL_ACCOUNT` |
| IBANs that pass the check-digit validation | `FINANCIAL_ACCOUNT` |
| US ABA routing numbers that pass the checksum | `FINANCIAL_ACCOUNT` |
| Bitcoin addresses in Bech32 or Bech32m format, starting with `bc1` | `CRYPTOCURRENCY_WALLET` |
| US Social Security numbers written with hyphens | `GOVERNMENT_ID` |
| 15-digit IMEI numbers that pass the checksum | `DEVICE_IDENTIFIER` |

Every other category, including `CREDENTIAL`, depends on the model alone. Pattern matches are redacted before the text reaches the model, and they're counted in the same metrics as model detections.

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
            <td><code>CRYPTOCURRENCY_WALLET</code></td>
            <td><code>long_pii_cryptoWallet</code></td>
            <td>Bitcoin addresses in Bech32 or Bech32m format</td>
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
            <td>Passwords that the <code>gravitee-io/bert-small-pii-detection</code> model labels as such. API keys and tokens are redacted only when the model classifies them as a password. No pattern covers this category, and <code>dslim/distilbert-NER</code> has no label for it.</td>
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

<!-- Verified from PiiCategory.java:17-58 at gravitee-policy-pii-filtering 3.1.0 (cd38048): all 14 categories and their exact metric key strings. -->

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

## Limitations

- Both models were trained on English text. The `gravitee-io/bert-small-pii-detection` [model card](https://huggingface.co/gravitee-io/bert-small-pii-detection) states that other languages degrade detection, and `dslim/distilbert-NER` was fine-tuned on the English CoNLL-2003 dataset, as described on its [model card](https://huggingface.co/dslim/distilbert-NER).
- The policy redacts only the characters that the model labels. When the model labels part of a value, the rest of the value isn't redacted.
- Lowering the threshold doesn't recover a value that the model didn't label as PII. The threshold filters out model detections with a low confidence score. It doesn't add detections, and pattern-based detection ignores it.
- The policy treats a threshold of 0 or less as not set and uses 0.5 instead. A threshold above 0 and below 0.01 is raised to 0.01. Neither adjustment causes an error or an execution warning.
- With `dslim/distilbert-NER`, the model detects only `PERSON`, `ORGANIZATION`, `LOCATION`, and `MISCELLANEOUS`. The other categories rely on pattern-based detection, so `PHONE`, `VEHICLE_ID`, `CREDENTIAL`, and `DEMOGRAPHIC` aren't detected with this model.

## Related changes

The Gateway console includes a new AI Model Token Classification resource type under Resources, with model selection for `dslim/distilbert-NER` and `gravitee-io/bert-small-pii-detection`.
