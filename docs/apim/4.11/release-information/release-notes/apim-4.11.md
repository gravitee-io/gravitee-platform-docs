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

* Reduces LLM API costs and latency by caching semantically similar requests using vector embeddings, enabling intelligent cache hits even when prompt text differs slightly
* Supports multiple text embedding models (ONNX BERT, OpenAI, custom HTTP endpoints) and vector storage backends (Redis with HNSW indexing, AWS S3 with automatic encryption)
* Allows cache scoping using metadata parameters extracted via EL expressions for isolation per API, user, or custom dimension
* Requires Enterprise Edition license, Hazelcast cache/cluster plugins 8.0.0-alpha.3 or later, and configured text embedding and vector store resources
* Configurable similarity thresholds and distance metrics (e.g., COSINE) determine cache hit behavior
<!-- /PIPELINE:APIM-12437 -->

## Improvements

## Bug Fixes
