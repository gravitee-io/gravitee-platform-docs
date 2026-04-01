### AI resources

The following resources support AI-powered policies and features in APIM. They provide model inference and vector storage capabilities used by policies such as AI Prompt Guardrails and PII Filtering.

#### AI Model Text Classification

The AI Model Text Classification resource loads an AI-powered text classification model that evaluates text content against a set of classification labels. It is used by the AI Prompt Guard Rails policy to detect inappropriate or malicious content in user prompts, such as profanity, toxicity, harmful intent, and jailbreak prompt injections.

{% hint style="info" %}
When multiple APIs use the same **AI Model Text Classification Resource**, the gateway will only load it once into memory. So if you have 50 APIs, each with the same resource, then the gateway only loads that model once.
{% endhint %}

The model runs locally on the Gateway using the ONNX Runtime. The first request to this API resource will take longer than usual because the model is loaded into memory at that time. Subsequent requests are processed faster.

{% hint style="info" %}
You may encounter an error when using this resource with Gravitee's default Docker image. This is because the default images are based on Alpine Linux, which does not support the ONNX Runtime. To resolve this issue, use the Gravitee Docker image based on Debian, available at `graviteeio/apim-gateway:<version>-debian`.
{% endhint %}

<table><thead><tr><th width="167">Config param</th><th width="384.3046875">Description</th><th>Default</th></tr></thead><tbody><tr><td>Model</td><td>The AI model to use for text classification. Eight models are available across three families: binary toxicity detection (BERT Tiny, BERT Mini, BERT Small, DistilBERT Multilingual), multi-label toxicity detection (Detoxify ONNX, MiniLMv2 Toxic Jigsaw), and prompt injection detection (Llama Prompt Guard 22M, Llama Prompt Guard 86M). Binary toxicity models classify text as toxic or non-toxic. Multi-label toxicity models return scores across multiple toxicity categories (e.g., <code>severe_toxicity</code>, <code>obscene</code>, <code>threat</code>, <code>identity_attack</code>) and demographic targets. Prompt injection models identify attempts to override or manipulate system instructions in LLM prompts. All models are sourced from HuggingFace repositories (gravitee-io, minuva, meta-llama namespaces). For detailed model specifications, performance metrics, and language support, see <a href="../guides/ai-model-text-classification-overview-and-model-selection.md">AI Model Text Classification - Overview and Model Selection</a>.</td><td>-</td></tr></tbody></table>

{% code title="Example" %}
```json
{
    "name": "ai-model-text-classification-resource",
    "type": "ai-model-text-classification",
    "enabled": true,
    "configuration": {
        "model": {
            "type": "MINILMV2_TOXIC_JIGSAW_MODEL"
        }
    }
}
```
{% endcode %}

#### AI Model Token Classification

The AI Model Token Classification resource loads an AI-powered token classification model that identifies and labels individual tokens (words or subwords) in text. It is used by the PII Filtering Policy to detect personally identifiable information (PII) such as names, locations, email addresses, and phone numbers in API request and response payloads.

{% hint style="info" %}
When multiple APIs use the same **AI Model Token Classification Resource**, the Gateway loads it once into memory. If 50 APIs reference the same resource, the Gateway loads that model only once.
{% endhint %}

The model runs locally on the Gateway using the ONNX Runtime. The first request to an API using this resource takes longer than usual because the model is loaded into memory at that time. Subsequent requests are processed faster.

{% hint style="info" %}
You may encounter an error when using this resource with Gravitee's default Docker image. This is because the default images are based on Alpine Linux, which does not support the ONNX Runtime. To resolve this issue, use the Gravitee Docker image based on Debian, available at `graviteeio/apim-gateway:<version>-debian`.
{% endhint %}

<table><thead><tr><th width="167">Config param</th><th width="384.3046875">Description</th><th>Default</th></tr></thead><tbody><tr><td>Model</td><td>The AI model to use for token classification. Supported models include <code>dslim/distilbert-NER</code> (general named entity recognition) and <code>gravitee-io/bert-small-pii-detection</code> (PII-optimized). The <code>gravitee-io</code> model uses quantization (<code>model.quant.onnx</code>) for reduced memory footprint.</td><td>-</td></tr></tbody></table>

Models are automatically downloaded to `$GRAVITEE_HOME/models/<model-name>/` with the following files: `model.onnx` (or `model.quant.onnx`), `tokenizer.json`, and `config.json`.

**Model Output Format**

Each model outputs token-level predictions with confidence scores (0.0–1.0) and entity labels. Labels follow the BIO tagging scheme:
- `B-<entity>`: Beginning of an entity (e.g., `B-PER` for the first token of a person's name)
- `I-<entity>`: Inside an entity (e.g., `I-PER` for subsequent tokens of a person's name)
- `S-<entity>`: Single-token entity (e.g., `EMAIL` for a complete email address)

Common entity labels include `PER` (person), `LOC` (location), `ORG` (organization), `EMAIL`, and `PHONE`.

**Prerequisites**

- Write permissions to `$GRAVITEE_HOME/models` directory for model downloads
- Sufficient Java heap memory for model loading

{% code title="Example" %}
```json
{
    "name": "ai-model-token-classification-resource",
    "type": "ai-model-token-classification",
    "enabled": true,
    "configuration": {
        "model": {
            "type": "GRAVITEE_BERT_SMALL_PII_DETECTION"
        }
    }
}
```
{% endcode %}

#### AI Text Embedding Model

The AI Text Embedding Model resource converts text into vector representations (embeddings) for semantic comparison. This resource is used by AI policies such as AI Semantic Caching to enable semantic matching of user prompts.

The resource supports three provider types: ONNX BERT (local models), OpenAI (cloud-based embeddings), and HTTP (custom embedding services).

{% hint style="info" %}
When multiple APIs use the same AI Text Embedding Model resource, the Gateway loads it once into memory. If 50 APIs reference the same resource, the Gateway loads that model only once.
{% endhint %}

**ONNX BERT Provider**

The ONNX BERT provider runs embedding models locally on the Gateway using the ONNX Runtime. The first request to this resource will take longer than usual because the model is loaded into memory at that time. Subsequent requests are processed faster.

{% hint style="info" %}
You may encounter an error when using this resource with Gravitee's default Docker image. This is because the default images are based on Alpine Linux, which does not support the ONNX Runtime. To resolve this issue, use the Gravitee Docker image based on Debian, available at `graviteeio/apim-gateway:<version>-debian`.
{% endhint %}

<table><thead><tr><th width="167">Config param</th><th width="384.3046875">Description</th><th>Default</th></tr></thead><tbody><tr><td>model.type</td><td>Embedding model type. Supported values: <code>XENOVA_ALL_MINILM_L6_V2</code>, <code>XENOVA_BGE_SMALL_EN_V1_5</code>, <code>XENOVA_MULTILINGUAL_E5_SMALL</code></td><td>-</td></tr><tr><td>poolingMode</td><td>Pooling mode for embeddings</td><td><code>MEAN</code></td></tr><tr><td>padding</td><td>Whether to apply padding</td><td><code>true</code></td></tr></tbody></table>

All ONNX BERT models support a maximum sequence length of 512 tokens.

{% code title="ONNX BERT example" %}
```json
{
    "name": "ai-text-embedding-onnx-bert",
    "type": "ai-text-embedding-model",
    "enabled": true,
    "configuration": {
        "provider": "ONNX_BERT",
        "onnxBert": {
            "model": {
                "type": "XENOVA_ALL_MINILM_L6_V2"
            },
            "poolingMode": "MEAN",
            "padding": true
        }
    }
}
```
{% endcode %}

**OpenAI Provider**

The OpenAI provider generates embeddings using OpenAI's cloud-based API.

<table>
    <thead>
        <tr>
            <th width="167">Config param</th>
            <th width="384.3046875">Description</th>
            <th>Default</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>uri</td>
            <td>OpenAI API endpoint URI</td>
            <td>-</td>
        </tr>
        <tr>
            <td>apiKey</td>
            <td>OpenAI API key</td>
            <td>-</td>
        </tr>
        <tr>
            <td>organizationId</td>
            <td>Optional organization ID</td>
            <td>-</td>
        </tr>
        <tr>
            <td>projectId</td>
            <td>Optional project ID</td>
            <td>-</td>
        </tr>
        <tr>
            <td>modelName</td>
            <td>Name of the embedding model (e.g., <code>text-embedding-ada-002</code>)</td>
            <td>-</td>
        </tr>
        <tr>
            <td>dimensions</td>
            <td>Optional embedding dimensions (must be non-negative)</td>
            <td>-</td>
        </tr>
        <tr>
            <td>encodingFormat</td>
            <td>Encoding format. Supported values: <code>FLOAT</code>, <code>BASE64</code></td>
            <td>-</td>
        </tr>
    </tbody>
</table>


{% hint style="info" %}
Embedding dimensions must be compatible with the vector store configuration.
{% endhint %}

{% code title="OpenAI example" %}
```json
{
    "name": "ai-text-embedding-openai",
    "type": "ai-text-embedding-model",
    "enabled": true,
    "configuration": {
        "provider": "OPENAI",
        "openai": {
            "uri": "https://api.openai.com/v1/embeddings",
            "apiKey": "sk-...",
            "modelName": "text-embedding-ada-002",
            "encodingFormat": "FLOAT"
        }
    }
}
```
{% endcode %}

**HTTP Provider**

The HTTP provider generates embeddings using a custom HTTP endpoint.

<table><thead><tr><th width="167">Config param</th><th width="384.3046875">Description</th><th>Default</th></tr></thead><tbody><tr><td>uri</td><td>HTTP endpoint URI

## Next steps
* [AI model text classification overview and model selection](ai-model-text-classification-overview-and-model-selection.md)
* [AI model text classification configuration and usage](ai-model-text-classification-configuration-and-usage.md)