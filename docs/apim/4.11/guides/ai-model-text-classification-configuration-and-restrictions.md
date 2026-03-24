# AI Model Text Classification Configuration and Restrictions

## End-User Configuration

## Restrictions

- BERT Tiny/Mini/Small models are pre-trained primarily on English; multilingual transfer is limited, especially for non-European languages
- BERT Tiny/Mini/Small provide binary classification only; use Detoxify or MiniLMv2 for fine-grained toxicity categories
- BERT Mini shows very low Hebrew performance (0.44 F1), lower than BERT Tiny on the same language
- BERT Small shows notable overfitting on some languages (Spanish delta: -0.124, Italian: -0.116, Hindi: -0.144)
- DistilBERT Multilingual provides binary classification only; performance varies significantly by language (F1 range: 0.62 to 0.96)
- Detoxify ONNX supports 7 languages only (no Arabic, Chinese, Hindi, Japanese, German, or other languages); highest memory usage and latency of toxicity models
- MiniLMv2 Toxic Jigsaw is English-only; trained on Wikipedia talk page comments (may not generalize to social media slang, code, or technical content); requires threshold tuning per label
- Llama Prompt Guard models have a 512-token context window; longer prompts must be split into segments
- Llama Prompt Guard models focus on explicit attack patterns; may not catch subtle or novel injection techniques
- Llama Prompt Guard 86M optimized variant has significant accuracy loss (recall drops to 0.80, AUC-ROC to 0.75); use the 22M variant or the original 86M model for production
- Meta recommends domain-specific fine-tuning of Llama Prompt Guard models for production use to reduce false positives
- All models use ONNX quantized inference; minor accuracy degradation compared to original models is expected (typically <3% F1 impact, except Llama Prompt Guard 86M optimized)
- Model licenses vary: OpenRAIL++ (BERT/DistilBERT), Apache 2.0 (Detoxify/MiniLMv2), Llama 4 Community License (Prompt Guard)

## Related Changes

This feature adds nine pre-trained AI models as gateway resources. Administrators select models via resource configuration using model identifiers (`GRAVITEE_IO_BERT_TINY_TOXICITY`, `GRAVITEE_DETOXIFY_ONNX_MODEL`, `GRAVITEE_LLAMA_PROMPT_GUARD_22M_MODEL`, etc.). Models are loaded into gateway memory on first use and cached for subsequent requests. All models use ONNX quantized inference for reduced memory footprint and faster latency. Training datasets include gravitee-io/textdetox-multilingual-toxicity-dataset (BERT/DistilBERT models, 85% train / 15% validation per language) and Jigsaw Toxic Comment Classification Challenge (MiniLMv2). Llama Prompt Guard models were pre-trained by Meta; evaluation used jackhhao/jailbreak-classification dataset. 
