# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2024 -->
#### **LLM Analytics and Cost Tracking**

* Track token consumption and costs for LLM-proxied API traffic through new dashboard widgets and analytics queries.
* Monitor total token usage, per-request costs, and model-specific metrics with two new metrics (`LLM_PROMPT_TOTAL_TOKEN` and `LLM_PROMPT_TOKEN_COST`) and facets for provider and model filtering.
* Requires APIs configured with LLM proxy policies that populate `additional-metrics` fields and Elasticsearch-backed analytics.
* Includes a new LLM dashboard template with 10 pre-configured widgets for token count, cost trends, and model-specific usage analysis.
<!-- /PIPELINE:GKO-2024 -->

## Improvements

## Bug Fixes
