# AI Model Text Classification - Model Reference and Performance Metrics

## Available models

| Model ID | HuggingFace Repository | Architecture | Parameters | License |
|:---------|:-----------------------|:-------------|:-----------|:--------|
| `GRAVITEE_IO_BERT_TINY_TOXICITY` | `gravitee-io/bert-tiny-toxicity` | BERT-tiny (2 layers, 128 hidden) | 4.39M | OpenRAIL++ |
| `GRAVITEE_IO_BERT_MINI_TOXICITY` | `gravitee-io/bert-mini-toxicity` | BERT-mini (4 layers, 256 hidden) | 11.2M | OpenRAIL++ |
| `GRAVITEE_IO_BERT_SMALL_TOXICITY` | `gravitee-io/bert-small-toxicity` | BERT-small (4 layers, 512 hidden) | 28.8M | OpenRAIL++ |
| `GRAVITEE_IO_DISTILBERT_MULTILINGUAL_TOXICITY_CLASSIFIER` | `gravitee-io/distilbert-multilingual-toxicity-classifier` | DistilBERT-base-multilingual-cased | 100M | OpenRAIL++ |
| `GRAVITEE_DETOXIFY_ONNX_MODEL` | `gravitee-io/detoxify-onnx` | XLM-RoBERTa-base | 300M | Apache 2.0 |
| `MINILMV2_TOXIC_JIGSAW_MODEL` | `minuva/MiniLMv2-toxic-jigsaw-onnx` | MiniLMv2-L6-H384 | 23M | Apache 2.0 |
| `GRAVITEE_LLAMA_PROMPT_GUARD_22M_MODEL` | `gravitee-io/Llama-Prompt-Guard-2-22M-onnx` | DeBERTa-v2-xsmall | 22M (70.8M ONNX F32) | Llama 4 Community License |
| `GRAVITEE_LLAMA_PROMPT_GUARD_86M_MODEL` | `gravitee-io/Llama-Prompt-Guard-2-86M-onnx` | DeBERTa-v2 (12 layers, 768 hidden) | 86M (300M ONNX F32) | Llama 4 Community License |

## Classification labels

### Binary toxicity models

All binary toxicity models (`GRAVITEE_IO_BERT_TINY_TOXICITY`, `GRAVITEE_IO_BERT_MINI_TOXICITY`, `GRAVITEE_IO_BERT_SMALL_TOXICITY`, `GRAVITEE_IO_DISTILBERT_MULTILINGUAL_TOXICITY_CLASSIFIER`) return:

| Label | Description |
|:------|:------------|
| `toxic` | Content classified as toxic |
| `not-toxic` | Content classified as non-toxic |

### Multi-label toxicity: Detoxify ONNX

`GRAVITEE_DETOXIFY_ONNX_MODEL` returns 16 labels (7 toxicity + 9 demographic):

| Label | Description |
|:------|:------------|
| `toxicity` | Generally toxic or rude content |
| `severe_toxicity` | Extremely toxic content with strong harmful intent |
| `obscene` | Profane or vulgar language |
| `identity_attack` | Hateful content targeting identity groups (race, religion, gender) |
| `insult` | Personally insulting or demeaning language |
| `threat` | Content containing threats of violence or harm |
| `sexual_explicit` | Sexually explicit content |
| `male` | Content targeting males |
| `female` | Content targeting females |
| `homosexual_gay_or_lesbian` | Content targeting homosexual/gay/lesbian people |
| `christian` | Content targeting Christians |
| `jewish` | Content targeting Jewish people |
| `muslim` | Content targeting Muslims |
| `black` | Content targeting Black people |
| `white` | Content targeting White people |
| `psychiatric_or_mental_illness` | Content targeting people with mental illness |

### Multi-label toxicity: MiniLMv2 Toxic Jigsaw

`MINILMV2_TOXIC_JIGSAW_MODEL` returns 6 labels:

| Label | Description |
|:------|:------------|
| `toxic` | Generally toxic or rude content |
| `severe_toxic` | Extremely toxic content with strong harmful intent |
| `obscene` | Profane or vulgar language |
| `threat` | Content containing threats of violence or harm |
| `insult` | Personally insulting or demeaning language |
| `identity_hate` | Hateful content targeting identity groups (race, religion, gender) |

### Prompt injection detection

Both Llama Prompt Guard models (`GRAVITEE_LLAMA_PROMPT_GUARD_22M_MODEL`, `GRAVITEE_LLAMA_PROMPT_GUARD_86M_MODEL`) return:

| Label | Description |
|:------|:------------|
| `BENIGN` | Prompt doesn't attempt to override or manipulate prior instructions |
| `MALICIOUS` | Prompt explicitly attempts to override developer or user instructions (injection/jailbreak) |

## Performance metrics

### Binary toxicity models: language support and F1 scores

F1 scores from the optimized ONNX versions used by Gravitee:

| Language | BERT Tiny | BERT Mini | BERT Small | DistilBERT |
|:---------|:----------|:----------|:-----------|:-----------|
| English | 0.9423 | 0.9557 | 0.9609 | 0.9495 |
| French | 0.8768 | 0.8993 | 0.9120 | 0.9351 |
| German | 0.8726 | 0.8750 | 0.8820 | 0.8842 |
| Hindi | 0.8429 | 0.8663 | 0.8865 | 0.8940 |
| Russian | 0.6932 | 0.8319 | 0.8959 | 0.9609 |
| Ukrainian | 0.6891 | 0.8016 | 0.8799 | 0.8988 |
| Spanish | 0.7826 | 0.7837 | 0.8220 | 0.8439 |
| Italian | 0.8066 | 0.8011 | 0.8263 | 0.8033 |
| Tatar | 0.6421 | 0.7937 | 0.8285 | 0.9148 |
| Japanese | 0.7503 | 0.7594 | 0.7165 | 0.8584 |
| Hinglish | 0.6971 | 0.7238 | 0.7188 | 0.7260 |
| Arabic | 0.6445 | 0.6788 | 0.6719 | 0.7535 |
| Amharic | 0.6474 | 0.6410 | 0.6300 | 0.6377 |
| Chinese | 0.6405 | 0.6328 | 0.6108 | 0.6697 |
| Hebrew | 0.5075 | 0.4094 | 0.5631 | 0.6190 |

### Binary toxicity models: resource characteristics

| Model | Memory Footprint | Relative Latency | Parameters |
|:------|:-----------------|:-----------------|:-----------|
| BERT Tiny | Very low | Very fast | 4.39M |
| BERT Mini | Low | Fast | 11.2M |
| BERT Small | Moderate-low | Moderate-fast | 28.8M |
| DistilBERT | Medium | Medium | 100M |

### Multi-label toxicity: Detoxify ONNX

Threshold: 0.5

| Metric | Original Model | Optimized (Gravitee) |
|:-------|:---------------|:---------------------|
| Accuracy | 0.8845 | 0.8880 |
| Precision | 0.6073 | 0.6408 |
| Recall | 0.7041 | 0.6179 |
| F1 | 0.6521 | 0.6291 |
| AUC-ROC | 0.9345 | 0.9306 |

- **Memory footprint**: High (~300M parameters)
- **Relative latency**: Slow (largest toxicity model)
- **Languages**: English, French, Spanish, Italian, Portuguese, Turkish, Russian

### Multi-label toxicity: MiniLMv2 Toxic Jigsaw

| Metric | Original Model | Optimized (Gravitee) |
|:-------|:---------------|:---------------------|
| ROC-AUC (test) | 0.9864 | 0.9813 |

- **Memory footprint**: Low (~23M parameters)
- **Relative latency**: Fast
- **Languages**: English only
- **Max sequence**: 256 tokens

### Prompt injection detection: Llama Prompt Guard 22M

| Metric | Original Model | Optimized (Gravitee) |
|:-------|:---------------|:---------------------|
| Accuracy | 0.9564 | 0.9579 |
| Precision | 0.9888 | 0.9967 |
| Recall | 0.9249 | 0.9204 |
| F1 | 0.9558 | 0.9449 |
| AUC-ROC | 0.9234 | 0.9180 |

- **Memory footprint**: Low
- **Relative latency**: Fast (~19.3ms per classification on A100 GPU)
- **Context window**: 512 tokens
- **Languages**: English, French, German, Hindi, Italian, Portuguese, Spanish, Thai

### Prompt injection detection: Llama Prompt Guard 86M

| Metric | Original Model | Optimized (Gravitee) |
|:-------|:---------------|:---------------------|
| Accuracy | 0.9801 | 0.8989 |
| Precision | 0.9984 | 1.0000 |
| Recall | 0.9625 | 0.8018 |
| F1 | 0.9801 | 0.8900 |
| AUC-ROC | 0.9519 | 0.7452 |

{% hint style="warning" %}
The optimized 86M version shows significant accuracy degradation compared to the original model. Use the 22M variant or the original (non-optimized) 86M model instead.
{% endhint %}

- **Memory footprint**: High (~300M in ONNX F32)
- **Relative latency**: Medium
- **Context window**: 512 tokens
- **Languages**: English, French, German, Hindi, Italian, Portuguese, Spanish, Thai

## Model families and size-accuracy tradeoffs

### BERT toxicity family

Part of a size-accuracy tradeoff family with three variants:

| Model | Parameters | Memory | Latency | Best Use Case |
|:------|:-----------|:-------|:--------|:--------------|
| BERT Tiny | 4.39M | Very low | Very fast | Ultra-low resource, English-dominant |
| BERT Mini | 11.2M | Low | Fast | Moderate resource, European languages |
| BERT Small | 28.8M | Moderate-low | Moderate-fast | Better accuracy, still lightweight |

All three variants share:
- Binary classification (toxic / not-toxic)
- 15-language support
- ONNX quantized format
- OpenRAIL++ license
- Same training dataset (`gravitee-io/textdetox-multilingual-toxicity-dataset`)

### Llama Prompt Guard family

Two variants with different performance characteristics:

| Model | Parameters | Memory | Latency | Optimized version performance |
|:------|:-----------|:-------|:--------|:------------------------------|
| 22M | 22M (70.8M ONNX F32) | Low | Fast | Minimal degradation, **recommended** |
| 86M | 86M (300M ONNX F32) | High | Medium | **Significant degradation**, use original only |

Both variants share:
- Binary classification (BENIGN / MALICIOUS)
- 8-language support
- 512-token context window
- Llama 4 Community License
- Same evaluation dataset (jackhhao/jailbreak-classification)

## Training datasets

| Model Family | Training Dataset | Split |
|:-------------|:-----------------|:------|
| BERT Tiny/Mini/Small Toxicity | `gravitee-io/textdetox-multilingual-toxicity-dataset` | 85% train / 15% validation per language |
| DistilBERT Multilingual Toxicity | `gravitee-io/textdetox-multilingual-toxicity-dataset` | 85% train / 15% validation per language |
| Detoxify ONNX | Base model: `unitary/multilingual-toxic-xlm-roberta` | Pre-trained |
| MiniLMv2 Toxic Jigsaw | Jigsaw Toxic Comment Classification Challenge (Kaggle) | N/A |
| Llama Prompt Guard 22M/86M | `jackhhao/jailbreak-classification` (evaluation only) | Pre-trained by Meta |