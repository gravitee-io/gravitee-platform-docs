# APIM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:APIM-12437 -->
#### **AI Semantic Caching for LLM Proxy APIs**

* Reduces latency and cost by caching responses to semantically similar prompts using vector embeddings instead of exact text matching.
* Supports ONNX BERT, OpenAI, and custom HTTP embedding models with configurable similarity thresholds and context-aware metadata parameters.
* Requires Enterprise Edition, a deployed AI text embedding model resource, and a vector store resource (Redis with HNSW indexing or AWS S3).
* Enables per-API, per-tenant, or per-user caching with optional secure hashing of sensitive metadata values.
<!-- /PIPELINE:APIM-12437 -->

## Improvements

## Bug Fixes
