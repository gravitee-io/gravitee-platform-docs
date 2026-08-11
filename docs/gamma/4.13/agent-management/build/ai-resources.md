---
hidden: false
noIndex: false
description: AI resources supply the models and vector stores that Guard Rails, PII Filtering, and Semantic Caching policies call. Compare the resource types.
---

# AI resources

AI resources are the components that AI policies call at runtime. They supply the model inference and the vector storage a policy needs to do its work: the **AI - Prompt Guard Rails** policy can't classify a prompt without a classification model behind it, and the **PII Filtering** policy can't redact a response without a token classification model.

You don't invoke a resource directly. You configure it once, and a policy references it by name. Every policy that needs one exposes a **Resource Name** field listing the resources of the type it requires. A policy configured without its resource fails rather than passing traffic through unchecked.

## Available resource types

| Resource | Used by | Purpose |
| --- | --- | --- |
| **AI Model Text Classification** | AI - Prompt Guard Rails | Classifies a whole text against a set of labels, to detect toxicity, harmful intent, and prompt injection |
| **AI Model Token Classification** | PII Filtering | Labels individual tokens within a text, so that personal data such as names, locations, and email addresses can be redacted |
| **AI Model Text Embedding** | AI Semantic Caching | Converts text into vectors, so that prompts that mean the same thing can be matched even when they're worded differently |
| **Redis Vector Store** | Policies that persist embeddings | Stores and queries embedding vectors in Redis |
| **AWS S3 Vector Store** | Policies that persist embeddings | Stores and queries embedding vectors in Amazon S3 |

## How the AI Gateway loads a model

The classification and ONNX embedding models run locally on the AI Gateway using the ONNX Runtime, which has three consequences worth planning for:

* **Models aren't bundled with the plugin.** On first use, the resource downloads the model into `$GRAVITEE_HOME/models`, so the gateway process needs write access to that directory. The `inference.path` property changes the location.
* **The first request after a gateway start is slower.** The runtime loads a model lazily, on the first request that needs it. Requests after that are fast.
* **A model is loaded once and shared.** The gateway caches a loaded model against its configuration rather than against the resource name, so fifty proxies selecting the same model share one loaded instance. Memory scales with model size and with how many distinct models you run, not with how many proxies reference them.

{% hint style="warning" %}
The ONNX Runtime doesn't run on Alpine Linux, which the default Gravitee Docker images are based on. Use the Debian-based gateway image instead, available at `graviteeio/apim-gateway:<version>-debian`.
{% endhint %}

## AI Model Text Classification

The AI Model Text Classification resource loads a model that evaluates a text against a set of classification labels. The **AI - Prompt Guard Rails** policy uses it to detect inappropriate or malicious content in prompts, including toxicity, harmful intent, and jailbreak prompt injections.

Eight models are available, covering binary toxicity detection, multi-label toxicity detection, and prompt injection detection. Choosing between them is a real decision, because they differ in accuracy, language coverage, label set, and memory footprint. See [Select a text classification model](select-a-text-classification-model.md) for the comparison, and [Configure text classification](configure-text-classification.md) for the policy settings.

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

## AI Model Token Classification

The AI Model Token Classification resource loads a model that labels individual tokens, that is, words or subwords, within a text. The **PII Filtering** policy uses it to locate personal data such as names, locations, email addresses, and phone numbers in request and response payloads, and replace each detected span with `[REDACTED]`.

Two models are supported:

* `dslim/distilbert-NER`, for general named entity recognition.
* `gravitee-io/bert-small-pii-detection`, optimized for personal data. This model is quantized, as `model.quant.onnx`, for a smaller memory footprint.

Each model returns token-level predictions with a confidence score between `0.0` and `1.0`, plus an entity label. Labels follow the BIO tagging scheme:

* `B-<entity>` marks the beginning of an entity, for example `B-PER` for the first token of a person's name.
* `I-<entity>` marks a token inside an entity, for example `I-PER` for the tokens that follow.
* `S-<entity>` marks a single-token entity, for example `EMAIL` for a complete email address.

Common entity labels are `PER` for a person, `LOC` for a location, `ORG` for an organization, `EMAIL`, and `PHONE`.

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

## AI Model Text Embedding

The AI Model Text Embedding resource converts text into vector representations, so that two texts can be compared by meaning rather than by wording. The **AI Semantic Caching** policy uses it to match a new prompt against prompts it has already answered.

The resource supports three providers.

### ONNX BERT

The ONNX BERT provider runs the embedding model locally on the AI Gateway, with the loading behavior described above. All ONNX BERT models support a maximum sequence length of 512 tokens.

| Config parameter | Description | Default |
| --- | --- | --- |
| `model.type` | The embedding model. Supported values are `XENOVA_ALL_MINILM_L6_V2`, `XENOVA_BGE_SMALL_EN_V1_5`, and `XENOVA_MULTILINGUAL_E5_SMALL` | - |
| `poolingMode` | The pooling mode used to produce the embedding | `MEAN` |
| `padding` | Whether to apply padding | `true` |

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

### OpenAI

The OpenAI provider generates embeddings through the OpenAI API rather than on the gateway.

| Config parameter | Description | Default |
| --- | --- | --- |
| `uri` | The API endpoint | - |
| `apiKey` | The API key | - |
| `organizationId` | The organization ID. Optional | - |
| `projectId` | The project ID. Optional | - |
| `modelName` | The embedding model, for example `text-embedding-ada-002` | - |
| `dimensions` | The embedding dimensions. Must be non-negative. Optional | - |
| `encodingFormat` | The encoding format. Supported values are `FLOAT` and `BASE64` | - |

{% hint style="info" %}
The embedding dimensions must be compatible with the vector store the embeddings are written to.
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
            "apiKey": "sk-000000000000000000000000",
            "modelName": "text-embedding-ada-002",
            "encodingFormat": "FLOAT"
        }
    }
}
```
{% endcode %}

### HTTP

The HTTP provider generates embeddings through a custom endpoint. It takes a single `uri` parameter.

## Next steps

* [Select a text classification model](select-a-text-classification-model.md). Compare the eight models by accuracy, language coverage, and footprint.
* [Configure text classification](configure-text-classification.md). Set the sensitivity threshold and decide whether to block or log.
* [Configure an LLM Proxy](configure-an-llm-proxy.md). Attach the policies that use these resources.
