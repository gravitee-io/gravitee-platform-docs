---
hidden: false
noIndex: false
description: Compare the text classification models available to the AI - Prompt Guard Rails policy, and choose one based on accuracy, language coverage, label granularity, and resource footprint.
---

# Select a text classification model

The **AI Model Text Classification** resource provides pre-trained models that detect toxic content and prompt injection attempts in traffic passing through an LLM Proxy, MCP Proxy, or A2A Proxy. Eight models are available, covering binary toxicity detection, multi-label toxicity detection, and prompt injection detection, with support for up to 15 languages.

You don't call this resource directly. The **AI - Prompt Guard Rails** policy consumes it. The policy's **Resource Name** field points at a configured AI Model Text Classification resource. The model you select decides both what the policy can detect and which labels are valid in its **Content Checks** field.

This page covers how to choose between the eight models. For the policy itself, see [Configure an LLM Proxy](configure-an-llm-proxy.md).

## Toxicity detection

Toxicity detection models classify text as toxic or non-toxic, with optional fine-grained categorization. Binary models return a single `toxic` or `not-toxic` label. Multi-label models return scores across several toxicity categories, and one of them also scores demographic targets.

The following table compares the two model types:

| Model type  | Labels               | Languages | Use case                                                     |
| ----------- | -------------------- | --------- | ------------------------------------------------------------ |
| Binary      | 2, toxic and not-toxic | 15      | General-purpose filtering, multilingual support              |
| Multi-label | 6 to 16              | 1 to 7    | Fine-grained categorization, demographic targeting detection |

### Language support and F1 scores

The following scores are for the optimized, quantized ONNX builds, which are the builds the gateway runs. They differ from the figures published on the upstream model cards, which describe the original, unquantized models.

| Language  | BERT Tiny | BERT Mini | BERT Small | DistilBERT |
| --------- | --------- | --------- | ---------- | ---------- |
| English   | 0.9423    | 0.9557    | 0.9609     | 0.9495     |
| French    | 0.8768    | 0.8993    | 0.9120     | 0.9351     |
| German    | 0.8726    | 0.8750    | 0.8820     | 0.8842     |
| Hindi     | 0.8429    | 0.8663    | 0.8865     | 0.8940     |
| Russian   | 0.6932    | 0.8319    | 0.8959     | 0.9609     |
| Ukrainian | 0.6891    | 0.8016    | 0.8799     | 0.8988     |
| Spanish   | 0.7826    | 0.7837    | 0.8220     | 0.8439     |
| Italian   | 0.8066    | 0.8011    | 0.8263     | 0.8033     |
| Tatar     | 0.6421    | 0.7937    | 0.8285     | 0.9148     |
| Japanese  | 0.7503    | 0.7594    | 0.7165     | 0.8584     |
| Hinglish  | 0.6971    | 0.7238    | 0.7188     | 0.7260     |
| Arabic    | 0.6445    | 0.6788    | 0.6719     | 0.7535     |
| Amharic   | 0.6474    | 0.6410    | 0.6300     | 0.6377     |
| Chinese   | 0.6405    | 0.6328    | 0.6108     | 0.6697     |
| Hebrew    | 0.5075    | 0.4094    | 0.5631     | 0.6190     |

### Training data

The four binary models, BERT Tiny, BERT Mini, BERT Small, and DistilBERT Multilingual, are trained on the `gravitee-io/textdetox-multilingual-toxicity-dataset`, with an 85/15 train and validation split per language.

MiniLMv2 Toxic Jigsaw is trained on the Jigsaw Toxic Comment Classification Challenge dataset and knowledge-distilled from `unitary/toxic-bert`.

Detoxify ONNX is derived from `unitary/multilingual-toxic-xlm-roberta` through the Detoxify framework. Its training dataset isn't published.

## Prompt injection detection

Prompt injection detection models identify attempts to override or manipulate system instructions in a prompt. Both models return `BENIGN` for a safe prompt or `MALICIOUS` for an injection or jailbreak attempt. Both are Llama Prompt Guard 2 variants, support 8 languages, and use a 512-token context window.

The following table compares the two prompt injection models:

| Model                    | Parameters | Accuracy | Recommended |
| ------------------------ | ---------- | -------- | ----------- |
| Llama Prompt Guard 2 22M | 22M        | 0.9579   | Yes         |
| Llama Prompt Guard 2 86M | 86M        | 0.8989   | No          |

{% hint style="info" %}
Both figures are for the optimized builds, which are the only builds Gravitee ships. Each identifier resolves to a quantized ONNX artifact. In this form the 22M variant is both more accurate and smaller, so there's no case for choosing the 86M variant.
{% endhint %}

## Available models

The **Select model** field stores an identifier in the API definition and displays the HuggingFace repository that identifier maps to.

The following table lists every available model:

| Identifier                                                | Repository                                                | Parameters | Objective                 | Labels                          | Languages | Licence                   |
| --------------------------------------------------------- | --------------------------------------------------------- | ---------- | ------------------------- | ------------------------------- | --------- | ------------------------- |
| `GRAVITEE_IO_BERT_TINY_TOXICITY`                          | `gravitee-io/bert-tiny-toxicity`                          | 4.39M      | Binary, multilingual      | `toxic` and `not-toxic`         | 15        | OpenRAIL++                |
| `GRAVITEE_IO_BERT_MINI_TOXICITY`                          | `gravitee-io/bert-mini-toxicity`                          | 11.2M      | Binary, multilingual      | `toxic` and `not-toxic`         | 15        | OpenRAIL++                |
| `GRAVITEE_IO_BERT_SMALL_TOXICITY`                         | `gravitee-io/bert-small-toxicity`                         | 28.8M      | Binary, multilingual      | `toxic` and `not-toxic`         | 15        | OpenRAIL++                |
| `GRAVITEE_IO_DISTILBERT_MULTILINGUAL_TOXICITY_CLASSIFIER` | `gravitee-io/distilbert-multilingual-toxicity-classifier` | 100M       | Binary, multilingual      | `toxic` and `not-toxic`         | 15        | OpenRAIL++                |
| `GRAVITEE_DETOXIFY_ONNX_MODEL`                            | `gravitee-io/detoxify-onnx`                               | 300M       | Multi-label, multilingual | 16, 7 toxicity and 9 demographic | 7        | Apache 2.0                |
| `MINILMV2_TOXIC_JIGSAW_MODEL`                             | `minuva/MiniLMv2-toxic-jigsaw-onnx`                       | 23M        | Multi-label               | 6                               | English   | Apache 2.0                |
| `GRAVITEE_LLAMA_PROMPT_GUARD_22M_MODEL`                   | `gravitee-io/Llama-Prompt-Guard-2-22M-onnx`               | 22M        | Prompt injection          | `BENIGN` and `MALICIOUS`        | 8         | Llama 4 Community License |
| `GRAVITEE_LLAMA_PROMPT_GUARD_86M_MODEL`                   | `gravitee-io/Llama-Prompt-Guard-2-86M-onnx`               | 86M        | Prompt injection          | `BENIGN` and `MALICIOUS`        | 8         | Llama 4 Community License |

## Choose a model

The following table maps common use cases to a recommended model:

| Use case                                  | Recommended model                                         | Rationale                                                                                    |
| ----------------------------------------- | --------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Multilingual toxicity, binary             | `GRAVITEE_IO_DISTILBERT_MULTILINGUAL_TOXICITY_CLASSIFIER` | Best balance of accuracy, with F1 scores from 0.62 to 0.96 across 15 languages at 100M        |
| Ultra-low resource toxicity               | `GRAVITEE_IO_BERT_TINY_TOXICITY`                          | Smallest at 4.39M and fastest, with acceptable accuracy on English, French, and German        |
| Low-resource toxicity, better than Tiny   | `GRAVITEE_IO_BERT_MINI_TOXICITY`                          | 11.2M, improved accuracy over BERT Tiny on most languages with a still-modest footprint. Weakest on Hebrew at 0.41 |
| Mid-range toxicity, smaller than DistilBERT | `GRAVITEE_IO_BERT_SMALL_TOXICITY`                       | 28.8M, the best average accuracy of the three lightweight BERT variants at roughly 29% of DistilBERT's size |
| Multi-label toxicity, multilingual        | `GRAVITEE_DETOXIFY_ONNX_MODEL`                            | 16 labels across 7 languages. Highest memory and latency of the eight                        |
| Multi-label toxicity, English only        | `MINILMV2_TOXIC_JIGSAW_MODEL`                             | 6 labels, low memory at 23M, and fast                                                        |
| Prompt injection detection                | `GRAVITEE_LLAMA_PROMPT_GUARD_22M_MODEL`                   | More accurate than the 86M variant in the builds Gravitee ships, and smaller                 |

## Labels differ by model

The **Content Checks** field on the AI - Prompt Guard Rails policy takes a comma-separated list of model labels, and matches every label when left empty. The valid labels are the ones your selected model emits. They aren't shared across models, and a label that the running model doesn't emit silently never matches.

The following table shows the label sets for the two multi-label models:

| Model                 | Toxicity labels                                                                                   | Demographic labels                                                                                                              |
| --------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Detoxify ONNX         | `toxicity`, `severe_toxicity`, `obscene`, `threat`, `insult`, `identity_attack`, `sexual_explicit` | `male`, `female`, `homosexual_gay_or_lesbian`, `christian`, `jewish`, `muslim`, `black`, `white`, `psychiatric_or_mental_illness` |
| MiniLMv2 Toxic Jigsaw | `toxic`, `severe_toxic`, `obscene`, `threat`, `insult`, `identity_hate`                           | None                                                                                                                                 |

Note the difference between `severe_toxicity` and `severe_toxic`, and between `identity_attack` and `identity_hate`. Copying a Detoxify label into a **Content Checks** list while running MiniLMv2 produces a filter that never matches.

The binary models emit only `toxic` and `not-toxic`, and the prompt injection models emit only `BENIGN` and `MALICIOUS`.

## Resource requirements

**Models aren't bundled with the plugin.** On first use, the resource downloads the selected model from HuggingFace into `$GRAVITEE_HOME/models`. The gateway process needs write access to that directory. You can change the path with the `inference.path` property.

**Memory scales with model size and with the number of proxies using the resource.** Size the Java heap and any container memory limits accordingly. The spread across these models is large, because Detoxify ONNX is roughly 68 times the size of BERT Tiny.

**The first request after a gateway start is slower.** The ONNX runtime loads the model lazily, on the first request that needs it.

**A model is loaded once and shared.** The gateway caches the loaded model against its configuration rather than the resource name. Several proxies that select the same model therefore share one loaded instance.

## Prerequisites

Selecting a model requires the following:

* Gravitee Gamma with the **AI Model Text Classification** resource plugin deployed.
* Network access to the HuggingFace `gravitee-io` and `minuva` namespaces.
* Enough memory for the selected model, on every gateway that runs a proxy using it.

{% hint style="info" %}
Meta pre-trains the Llama Prompt Guard 2 models, and Gravitee converts them to ONNX. The gateway downloads only the Gravitee-hosted conversions, so an air-gapped or allowlisted deployment doesn't need access to Meta's HuggingFace namespace. The models remain subject to the Llama 4 Community License.
{% endhint %}
