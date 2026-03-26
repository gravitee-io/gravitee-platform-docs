# AI Model Text Classification - Configuration and Usage

## Gateway Configuration

## Creating a Text Classification Policy

Configure a text classification policy by selecting a model identifier and specifying input text sources (request body, headers, or query parameters). For binary toxicity models, set a classification threshold (default: 0.5). For multi-label models, configure per-label thresholds or use the default 0.5 across all labels. Attach the policy to an API plan or flow to inspect traffic. The policy evaluates text against the selected model and returns classification labels with confidence scores. For prompt injection detection, configure the policy to inspect user prompts before forwarding to LLM backends.

## Managing Model Performance

Monitor model accuracy and latency using the metrics tables in the Dependencies section. Binary toxicity models report F1 scores per language. Multi-label models report accuracy, precision, recall, F1, and AUC-ROC. Prompt injection models report the same metrics plus per-language performance. If accuracy degrades on specific languages, switch to a larger model (BERT Mini → BERT Small → DistilBERT). If latency is unacceptable, downgrade to a smaller model or enable request sampling. For prompt injection detection, the 22M variant is faster and more accurate than the optimized 86M variant. Use the original 86M model only if deploying non-optimized versions.

## End-User Configuration

## Restrictions

* **Llama Prompt Guard 86M optimized version**: Significant accuracy degradation (recall: 0.80, AUC-ROC: 0.75) compared to original model. Use 22M variant or original 86M instead.
* **BERT Tiny Toxicity**: Lowest accuracy of BERT family. Hebrew F1: 0.52. Significant gap between English (0.94) and low-resource languages.
* **BERT Mini Toxicity**: Hebrew F1: 0.44 (lower than BERT Tiny). Overfitting on some languages (train-eval gap up to 0.11).
* **BERT Small Toxicity**: Overfitting on Spanish (Δ -0.124), Italian (Δ -0.116), Hindi (Δ -0.144).
* **DistilBERT Multilingual Toxicity**: Binary classification only. F1 range 0.62–0.96. Weaker on Hebrew, Amharic, Chinese.
* **Detoxify ONNX**: Largest toxicity model (300M parameters). Highest memory/latency. 7 languages only (no Arabic, Chinese, Hindi, Japanese, German).
* **MiniLMv2 Toxic Jigsaw**: English only. Trained on Wikipedia talk pages (may not generalize to social media, code, technical content).
* **Llama Prompt Guard (both variants)**: 512-token context window (longer prompts require segmentation). Focused on explicit attacks (may miss subtle/novel techniques). Meta recommends domain-specific fine-tuning for production.
* **All binary toxicity models**: No fine-grained toxicity categories.
* **All multi-label models**: Require threshold tuning per label for optimal precision/recall.
