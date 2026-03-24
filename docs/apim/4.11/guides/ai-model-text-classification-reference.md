# AI Model Text Classification Reference

## Overview

AI Model Text Classification provides pre-trained machine learning models for detecting toxic content and prompt injection attacks in API traffic. The feature includes nine ONNX-optimized models covering 15 languages for toxicity detection and 8 languages for prompt injection detection. Models range from ultra-lightweight (4.39M parameters) to high-accuracy (300M parameters), enabling administrators to balance latency, memory, and detection accuracy based on their deployment constraints.

## Key Concepts

### Toxicity Detection Models

Binary toxicity classifiers identify whether content is toxic or non-toxic. Multi-label classifiers provide granular categorization across toxicity dimensions and demographic attributes.

| Model Family | Parameters | Languages | Classification Type | Recommended Use Case |
|:-------------|:-----------|:----------|:--------------------|:---------------------|
| BERT-tiny | 4.39M | 15 | Binary | Ultra-low latency, memory-constrained environments |
| BERT-mini | 11.2M | 15 | Binary | Balanced latency and accuracy |
| BERT-small | 28.8M | 15 | Binary | Higher accuracy with moderate resource usage |
| DistilBERT-multilingual | 100M | 15 | Binary | Recommended for broad language support |
| Detoxify (XLM-RoBERTa) | 300M | 7 | Multi-label | Fine-grained toxicity analysis, highest accuracy |
| MiniLMv2 | 23M | 1 (English) | Multi-label | English-only fine-grained analysis |

The BERT family (tiny/mini/small) and DistilBERT multilingual classifier support 15 languages with binary classification. Detoxify supports 7 languages with multi-label classification. MiniLMv2 supports English only with multi-label classification.

### Prompt Injection Detection Models

Prompt Guard models detect attempts to override or manipulate system instructions through jailbreak or injection techniques. Both variants classify prompts as `BENIGN` or `MALICIOUS`. The 22M variant offers faster inference with higher accuracy in the optimized ONNX format used by Gravitee. The 86M variant suffers significant accuracy degradation after optimization (recall drops to 0.80, AUC-ROC to 0.75) and is not recommended for production use.

| Model Variant | Parameters | Languages | Optimized Accuracy | Optimized F1 | Recommended |
|:--------------|:-----------|:----------|:-------------------|:-------------|:------------|
| Prompt Guard 22M | 22M (70.8M ONNX F32) | 8 | 0.9579 | 0.9449 | ✓ Yes |
| Prompt Guard 86M | 86M (300M ONNX F32) | 8 | 0.8989 | 0.8900 | ✗ No (accuracy loss) |

### Classification Labels

**Binary Toxicity Labels** (BERT-tiny, BERT-mini, BERT-small, DistilBERT-multilingual):

| Label | Description |
|:------|:------------|
| `toxic` | Content classified as toxic |
| `not-toxic` | Content classified as non-toxic |

**Multi-Label Toxicity Labels** (Detoxify):

| Label | Description |
|:------|:------------|
| `toxicity` | Generally toxic or rude content |
| `severe_toxicity` | Extremely toxic content with strong harmful intent |
| `obscene` | Profane or vulgar language |
| `identity_attack` | Hateful content targeting identity groups (race, religion, gender) |
| `insult` | Personally insulting or demeaning language |
| `threat` | Content containing threats of violence or harm |
| `sexual_explicit` | Sexually explicit content |

**Multi-Label Toxicity Labels** (MiniLMv2):

| Label | Description |
|:------|:------------|
| `toxic` | Generally toxic or rude content |
| `severe_toxic` | Extremely toxic content with strong harmful intent |
| `obscene` | Profane or vulgar language |
| `threat` | Content containing threats of violence or harm |
| `insult` | Personally insulting or demeaning language |
| `identity_hate` | Hateful content targeting identity groups (race, religion, gender) |

**Demographic Attribute Labels** (Detoxify only):

| Label | Description |
|:------|:------------|
| `male` | Content targeting males |
| `female` | Content targeting females |
| `homosexual_gay_or_lesbian` | Content targeting homosexual/gay/lesbian people |
| `christian` | Content targeting Christians |
| `jewish` | Content targeting Jewish people |
| `muslim` | Content targeting Muslims |
| `black` | Content targeting Black people |
| `white` | Content targeting White people |
| `psychiatric_or_mental_illness` | Content targeting people with mental illness |

**Prompt Injection Labels** (Prompt Guard 22M, Prompt Guard 86M):

| Label | Description |
|:------|:------------|
| `BENIGN` | Prompt does not attempt to override or manipulate prior instructions |
| `MALICIOUS` | Prompt explicitly attempts to override developer or user instructions (injection/jailbreak) |

## Prerequisites

