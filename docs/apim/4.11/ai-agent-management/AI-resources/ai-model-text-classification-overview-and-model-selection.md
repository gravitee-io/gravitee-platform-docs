# AI - Model Text Classification - Overview and Model Selection

## Overview

AI Model Text Classification provides pre-trained models for detecting toxic content and prompt injection attacks in API traffic. Eight models are available, spanning toxicity detection (binary and multi-label) and prompt injection detection, with support for up to 15 languages. Administrators select models based on accuracy requirements, resource constraints, and language coverage.

For the complete list of model identifiers, classification labels, and performance benchmarks, see [Model Reference and Performance Metrics](../../create-and-configure-apis/apply-policies/policy-reference/ai-model-text-classification-model-reference-and-performance-metrics.md).

## Key concepts

### Toxicity detection

Toxicity detection models classify text as toxic or non-toxic, with optional fine-grained categorization. Binary models return a single `toxic` or `not-toxic` label. Multi-label models return scores across multiple toxicity categories (for example, `severe_toxicity`, `obscene`, `threat`, `identity_attack`) and demographic targets (for example, `male`, `female`, `christian`, `muslim`).

All toxicity models are trained on the `gravitee-io/textdetox-multilingual-toxicity-dataset` or the Jigsaw Toxic Comment Classification Challenge dataset.

| Model Type  | Labels               | Languages | Use Case                                                     |
| ----------- | -------------------- | --------- | ------------------------------------------------------------ |
| Binary      | 2 (toxic, not-toxic) | 15        | General-purpose filtering, multilingual support              |
| Multi-label | 6–16                 | 1–7       | Fine-grained categorization, demographic targeting detection |

**Language support and F1 scores (binary models):**

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

### Prompt injection detection

Prompt injection detection models identify attempts to override or manipulate system instructions in LLM prompts. Models return `BENIGN` (safe prompt) or `MALICIOUS` (injection/jailbreak attempt). Both Llama Prompt Guard variants support 8 languages and a 512-token context window. The 22M variant is recommended for production use. The 86M optimized version suffers significant accuracy degradation.

| Model                  | Parameters | Accuracy (Optimized) | Recommended            |
| ---------------------- | ---------- | -------------------- | ---------------------- |
| Llama Prompt Guard 22M | 22M        | 0.9579               | Yes                    |
| Llama Prompt Guard 86M | 86M        | 0.8989               | No (use original only) |

### Model selection criteria

Model selection balances accuracy, resource footprint, language coverage, and label granularity:

| Use Case                            | Recommended Model                                         | Rationale                                                                    |
| ----------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Multilingual toxicity (binary)      | `GRAVITEE_IO_DISTILBERT_MULTILINGUAL_TOXICITY_CLASSIFIER` | Best balance of accuracy (F1: 0.62–0.96), 15 languages, moderate size (100M) |
| Ultra-low resource toxicity         | `GRAVITEE_IO_BERT_TINY_TOXICITY`                          | Smallest (4.39M), fastest, acceptable accuracy on English/French/German      |
| Multi-label toxicity (multilingual) | `GRAVITEE_DETOXIFY_ONNX_MODEL`                            | 16 labels (7 toxicity + 9 demographic), 7 languages, highest memory/latency  |
| Multi-label toxicity (English only) | `MINILMV2_TOXIC_JIGSAW_MODEL`                             | 6 labels, low memory (23M), fast                                             |
| Prompt injection detection          | `GRAVITEE_LLAMA_PROMPT_GUARD_22M_MODEL`                   | Optimized version outperforms 86M, faster, lower memory                      |

## Prerequisites

* Gravitee API Management platform with AI Model Text Classification resource plugin installed
* Access to HuggingFace model repositories (`gravitee-io`, `minuva`, `meta-llama` namespaces)
* Sufficient memory and compute resources for selected model (see [Model Reference](../../create-and-configure-apis/apply-policies/policy-reference/ai-model-text-classification-model-reference-and-performance-metrics.md) for model sizes)
