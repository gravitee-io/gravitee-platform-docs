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

* Reduces redundant LLM backend calls by caching responses based on semantic similarity rather than exact string matching, lowering token consumption and response latency.
* Uses vector embeddings to identify semantically equivalent prompts (e.g., "What is the capital of France?" and "Capital of France?") and returns cached responses when similarity exceeds a configurable threshold.
* Supports ONNX (local inference), OpenAI, and custom HTTP embedding providers, with Redis or AWS S3 as vector store backends.
* Enables context-aware caching through metadata filtering (e.g., per-API, per-tenant) using EL expressions and optional MurmurHash3 encoding for privacy.
* Requires Enterprise Edition license and configuration of both a text embedding model resource and a vector store resource at the gateway level.
<!-- /PIPELINE:APIM-12437 -->

## Improvements

## Bug Fixes
