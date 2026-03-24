# AI Model Text Classification Model Reference

## Language Support

**Table 1: Language Support by Model**

| Model | Supported Languages |
|:------|:-------------------|
| BERT Tiny Toxicity | English, French, German, Hindi, Italian, Spanish, Japanese, Ukrainian, Hinglish, Russian, Amharic, Tatar, Arabic, Chinese, Hebrew |
| BERT Mini Toxicity | English, French, German, Hindi, Russian, Ukrainian, Spanish, Italian, Tatar, Japanese, Hinglish, Arabic, Amharic, Chinese, Hebrew |
| BERT Small Toxicity | English, French, Russian, Hindi, German, Ukrainian, Tatar, Italian, Spanish, Japanese, Hinglish, Arabic, Amharic, Chinese, Hebrew |
| DistilBERT Multilingual | Russian, English, French, Hindi, Tatar, Ukrainian, German, Japanese, Spanish, Italian, Arabic, Hinglish, Chinese, Amharic, Hebrew |
| Detoxify ONNX | English, French, Spanish, Italian, Portuguese, Turkish, Russian |
| MiniLMv2 Toxic Jigsaw | English only |
| Llama Prompt Guard 22M | English, French, German, Hindi, Italian, Portuguese, Spanish, Thai |
| Llama Prompt Guard 86M | English, French, German, Hindi, Italian, Portuguese, Spanish, Thai |

## Prerequisites

- Gravitee API Management platform with resource plugin support
- Sufficient gateway memory to load selected model (4.39M to 300M parameters depending on model choice)
- Text payloads in supported languages for the selected model
- For prompt injection detection: LLM-powered APIs or endpoints accepting user-supplied prompts

## Creating AI Model Text Classification Resources

Configure an AI Model Text Classification resource by selecting a model identifier from the table above and attaching it to an API or gateway-level resource. The resource loads the ONNX model into memory on first use and caches it for subsequent requests. For toxicity detection, choose a model based on language requirements (15 languages for BERT/DistilBERT, 7 for Detoxify, 1 for MiniLMv2) and output granularity (binary vs multi-label). For prompt injection detection, use Llama Prompt Guard 22M for production deployments; avoid the 86M optimized variant due to accuracy degradation. Attach the resource to policies that inspect request or response payloads, such as content filtering or LLM gateway policies.

## Analyzing Model Performance

Evaluate model accuracy using the performance metrics below. All metrics compare the original model (pre-optimization) to the ONNX quantized version used by Gravitee. For toxicity models, F1 scores vary significantly by language; select models with strong F1 scores for your target languages. For prompt injection models, the 22M variant maintains stable accuracy after optimization (0.9579 accuracy, 0.9449 F1), while the 86M optimized variant shows significant degradation (0.8989 accuracy, 0.8900 F1, 0.7452 AUC-ROC). Use the original 86M model if maximum accuracy is required.

#### BERT Tiny Toxicity

- Memory footprint: Very low (~4.39M parameters, quantized)
- Relative latency: Very fast (smallest model available)
- Best F1 scores: English (0.94), French (0.88), German (0.87)
- Weakest F1 scores: Hebrew (0.51), Chinese (0.64), Arabic (0.64)

### BERT Mini Toxicity

- Memory footprint: Low (~11.2M parameters, quantized)
- Relative latency: Fast
- Best F1 scores: English (0.96), French (0.90), German (0.88)
- Weakest F1 scores: Hebrew (0.41), Chinese (0.63), Amharic (0.64)

### BERT Small Toxicity

- Memory footprint: Moderate-low (~28.8M parameters, quantized)
- Relative latency: Moderate-fast
- Best F1 scores: English (0.96), French (0.91), Russian (0.90), Hindi (0.89)
- Weakest F1 scores: Hebrew (0.56), Chinese (0.61), Amharic (0.63)

### DistilBERT Multilingual Toxicity Classifier

- Memory footprint: Medium (~100M parameters)
- Relative latency: Medium
- Best F1 scores: Russian (0.96), English (0.95), French (0.94), Tatar (0.91)
- Weakest F1 scores: Hebrew (0.62), Amharic (0.64), Chinese (0.67)

### Detoxify ONNX

| Metric | Original model | Optimized (used by Gravitee) |
|----------------|----------------|------------------------------|
| **Accuracy** | 0.8845 | 0.8880 |
| **Precision** | 0.6073 | 0.6408 |
| **Recall** | 0.7041 | 0.6179 |
| **F1** | 0.6521 | 0.6291 |
| **AUC-ROC** | 0.9345 | 0.9306 |

- Memory footprint: High (~300M parameters)
- Relative latency: Slow (largest toxicity model available)

### MiniLMv2 Toxic Jigsaw

| Metric | Original model | Optimized (used by Gravitee) |
|----------------------|----------------|------------------------------|
| **ROC-AUC** | 0.9864 | 0.9813 |

- Memory footprint: Low (~23M parameters)
- Relative latency: Fast (smallest model with multi-label output)
- Max sequence: 256 tokens

### Llama Prompt Guard 22M

| Metric | Original model | Optimized (used by Gravitee) |
|---------------|----------------|------------------------------|
| **Accuracy** | 0.9564 | 0.9579 |
| **Precision** | 0.9888 | 0.9967 |
| **Recall** | 0.9249 | 0.9204 |
| **F1** | 0.9558 | 0.9449 |
| **AUC-ROC** | 0.9234 | 0.9180 |

- Memory footprint: Low
- Relative latency: Fast (~19.3ms per classification on A100 GPU)
- Context window: 512 tokens (split longer inputs into segments)

### Llama Prompt Guard 86M

| Metric | Original model | Optimized (used by Gravitee) |
|---------------|----------------|------------------------------|
| **Accuracy** | 0.9801 | 0.8989 |
| **Precision** | 0.9984 | 1.0000 |
| **Recall** | 0.9625 | 0.8018 |
| **F1** | 0.9801 | 0.8900 |
| **AUC-ROC** | 0.9519 | 0.7452 |

{% hint style="warning" %}
The optimized version shows significant accuracy degradation compared to the original model. The 22M variant does not suffer from this issue.
{% endhint %}

- Memory footprint: High (~300M in ONNX F32)
- Relative latency: Medium
- Context window: 512 tokens (split longer inputs into segments)
