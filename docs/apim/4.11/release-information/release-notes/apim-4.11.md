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

* Reduces LLM API costs and latency by reusing responses for semantically similar requests using vector embeddings instead of exact string matching.
* Integrates with Redis or AWS S3 vector stores and supports multiple embedding model providers (ONNX BERT, OpenAI, custom HTTP endpoints).
* Enables multi-tenant caching through metadata filtering with optional MurmurHash3 encoding for secure parameter indexing.
* Supports automatic cache eviction with configurable time-to-live and similarity thresholds (cosine or euclidean distance metrics).
* Requires Gravitee APIM Enterprise Edition, Redis 8.4.0+, and configured AI embedding model and vector store resources.
<!-- /PIPELINE:APIM-12437 -->

## Improvements

## Bug Fixes
