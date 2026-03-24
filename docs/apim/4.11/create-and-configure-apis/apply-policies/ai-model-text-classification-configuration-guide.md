# AI Model Text Classification Configuration Guide

## Prerequisites

## Gateway Configuration

### Model Selection

Configure the model identifier to select the classification model. Use the exact model ID from the table below.

| Model ID | Purpose | Parameters | Languages |
|:---------|:--------|:-----------|:----------|
| `GRAVITEE_IO_BERT_TINY_TOXICITY` | Ultra-lightweight binary toxicity | 4.39M | 15 |
| `GRAVITEE_IO_BERT_MINI_TOXICITY` | Lightweight binary toxicity | 11.2M | 15 |
| `GRAVITEE_IO_BERT_SMALL_TOXICITY` | Mid-range binary toxicity | 28.8M | 15 |
| `GRAVITEE_IO_DISTILBERT_MULTILINGUAL_TOXICITY_CLASSIFIER` | Binary toxicity (recommended) | 100M | 15 |
| `GRAVITEE_DETOXIFY_ONNX_MODEL` | Multi-label multilingual toxicity | 300M | 7 |
| `MINILMV2_TOXIC_JIGSAW_MODEL` | Multi-label English-only toxicity | 23M | 1 |
| `GRAVITEE_LLAMA_PROMPT_GUARD_22M_MODEL` | Prompt injection detection | 22M | 8 |
| `GRAVITEE_LLAMA_PROMPT_GUARD_86M_MODEL` | Prompt injection detection (not recommended) | 86M | 8 |

### Language Support

Verify the target language is supported by the selected model.

**15-Language Models** (BERT-tiny, BERT-mini, BERT-small, DistilBERT-multilingual):
English, French, German, Hindi, Italian, Spanish, Japanese, Ukrainian, Hinglish, Russian, Amharic, Tatar, Arabic, Chinese, Hebrew

**7-Language Model** (Detoxify):
English, French, Spanish, Italian, Portuguese, Turkish, Russian

**8-Language Models** (Prompt Guard 22M, Prompt Guard 86M):
English, French, German, Hindi, Italian, Portuguese, Spanish, Thai

**English-Only Model** (MiniLMv2):
English

## Creating a Text Classification Policy

## Managing Classification Results

## End-User Configuration

## Restrictions

- **Context window limits**: Prompt Guard models support 512 tokens maximum; MiniLMv2 supports 256 tokens maximum. Split longer inputs into segments.
- **Language-specific accuracy**: BERT-tiny Hebrew F1 is 0.51; BERT-mini Hebrew F1 is 0.41; performance on low-resource languages (Hebrew, Amharic, Chinese) is significantly lower than European languages across all models.
- **Optimized model degradation**: Prompt Guard 86M optimized variant shows significant accuracy loss (recall 0.80, AUC-ROC 0.75) compared to the original model. Use Prompt Guard 22M instead.
- **Domain limitations**: MiniLMv2 is trained on Wikipedia talk page comments and may not generalize to social media slang, code, or technical content.
- **Explicit attack focus**: Prompt Guard models detect explicit injection patterns; subtle or novel techniques may not be caught. Meta recommends domain-specific fine-tuning for production use.
- **Multi-label threshold tuning**: Detoxify and MiniLMv2 require per-label threshold configuration to optimize precision/recall tradeoffs.
- **Overfitting indicators**: BERT-small shows train-eval F1 gaps up to 0.14 on Spanish, Italian, and Hindi; BERT-mini shows gaps up to 0.11 on some languages.
- **License constraints**: Prompt Guard models use Llama 4 Community License; BERT and DistilBERT models use OpenRAIL++; Detoxify and MiniLMv2 use Apache 2.0.

## Related Changes

All models are distributed as ONNX quantized formats for optimized inference. Model files are hosted on HuggingFace repositories under the `gravitee-io` organization (BERT family, DistilBERT, Detoxify, Prompt Guard) or third-party repositories (MiniLMv2). Training datasets include the Gravitee `textdetox-multilingual-toxicity-dataset` (BERT family, DistilBERT), Jigsaw Toxic Comment Classification Challenge (MiniLMv2), and Meta's Llama Prompt Guard datasets (Prompt Guard family). Performance metrics are provided for optimized ONNX variants, not original PyTorch models. The DistilBERT multilingual classifier is the recommended default for binary toxicity detection with broad language support. Detoxify is the recommended model for multi-label toxicity analysis despite higher memory usage. Prompt Guard 22M is the recommended model for prompt injection detection; the 86M variant should not be used in production due to optimization-induced accuracy loss.
