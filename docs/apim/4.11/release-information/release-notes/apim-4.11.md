# APIM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:APIM-12439 -->
#### **AI-Powered PII Filtering Policy**

* Automatically detects and redacts Personally Identifiable Information (PII) in API request and response payloads using AI token classification models
* Supports configurable redaction rules based on AI confidence thresholds (0.0–1.0) and PII categories (PERSON, LOCATION, EMAIL, etc.)
* Requires Enterprise license with `agent-mesh` pack, write permissions to `$GRAVITEE_HOME/models` directory for automatic model downloads, and sufficient heap memory for model loading
* Includes streaming detection safeguards that reject streaming requests when response filtering is enabled to prevent incomplete redaction
<!-- /PIPELINE:APIM-12439 -->


<!-- PIPELINE:APIM-12437 -->
#### **AI Semantic Caching for LLM Proxy APIs**

* Reduces LLM token consumption and API latency by caching responses based on semantic meaning rather than exact text matching.
* Uses AI text embedding models and vector stores to identify semantically similar prompts, even when phrased differently, and returns cached results when similarity exceeds the configured threshold.
* Supports cache partitioning via metadata parameters (for example, API, plan, user ID) to ensure context-appropriate responses for identical queries from different users.
* Requires an AI text embedding model resource (ONNX BERT, OpenAI, or HTTP provider) and a vector store resource (Redis or AWS S3) with compatible embedding dimensions.
* Available exclusively on LLM Proxy APIs deployed with Agent Mesh.
<!-- /PIPELINE:APIM-12437 -->

## Improvements

## Bug Fixes
