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
#### **AI Semantic Caching Policy**

* Reduces latency and token consumption for LLM proxy APIs by caching responses based on semantic similarity rather than exact string matching.
* Uses configurable AI model resources (OpenAI, ONNX BERT, or custom HTTP endpoints) to generate vector embeddings and queries a vector store (Redis or AWS S3) to find semantically similar cached entries above a similarity threshold (default: 0.7 cosine similarity).
* Supports metadata-based cache partitioning with EL expressions and optional hashing to isolate cache entries across tenants or user segments.
* Requires Gravitee APIM 4.10.1+, Gravitee Node 8.0.0-alpha.3+, and Hazelcast cluster plugins for distributed caching support.
* Only available for LLM proxy APIs (API type: `llm-proxy`, definition version: `4.0.0`).
<!-- /PIPELINE:APIM-12437 -->

## Improvements

## Bug Fixes
