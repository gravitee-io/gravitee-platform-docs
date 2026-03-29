# LLM Metrics, Filters, and Dashboard Templates Reference

## Overview

This reference documents the metrics, filters, facets, and dashboard templates for monitoring Large Language Model (LLM) usage, token consumption, and associated costs. The LLM analytics feature enables API platform administrators to track real-time LLM performance, analyze usage patterns by model and provider, and optimize AI integration costs through dedicated analytics and visualization tools.

## Key Concepts

### LLM Metrics

The platform provides two computed metrics for LLM monitoring:

| Metric | Computation | Supported Measures | Elasticsearch Fields |
|:-------|:------------|:-------------------|:---------------------|
| `LLM_PROMPT_TOTAL_TOKEN` | Sum of sent and received tokens | `COUNT`, `AVG` | `additional-metrics.long_llm-proxy_tokens-sent`, `additional-metrics.long_llm-proxy_tokens-received` |
| `LLM_PROMPT_TOKEN_COST` | Sum of sent and received token costs | `COUNT`, `AVG` | `additional-metrics.double_llm-proxy_sent-cost`, `additional-metrics.double_llm-proxy_received-cost` |

Both metrics are computed via Elasticsearch scripted aggregations that combine values from the specified fields.

### LLM Filters and Facets

Two filters and facets enable segmentation of analytics data by LLM provider and model:

| Filter/Facet Name | Elasticsearch Field | Scope |
|:------------------|:--------------------|:------|
| `LLM_PROXY_MODEL` | `additional-metrics.keyword_llm-proxy_model` | All HTTP, LLM, message, Kafka metrics |
| `LLM_PROXY_PROVIDER` | `additional-metrics.keyword_llm-proxy_provider` | All HTTP, LLM, message, Kafka metrics |

`LLM_PROXY_MODEL` filters or groups data by the specific LLM model invoked (e.g., GPT-4, Claude). `LLM_PROXY_PROVIDER` filters or groups data by the LLM service provider (e.g., OpenAI, Anthropic).

### LLM Dashboard Template

The **LLM** dashboard template (`llm`) replaces the previous `AI Gateway` template and provides a centralized view of LLM usage, token consumption, and costs. The template includes nine pre-configured widgets:

| Widget Title | Type | Metric | Measure | Description |
|:-------------|:-----|:-------|:--------|:------------|
| LLM requests | stats | `HTTP_REQUESTS` | `COUNT` | Number of requests targeting LLM providers (filtered by `API_TYPE = LLM`) |
| Total tokens | stats | `LLM_PROMPT_TOTAL_TOKEN` | `COUNT` | Total number of tokens processed (prompt and completion) |
| Total cost | stats | `LLM_PROMPT_TOKEN_TOTAL_COST` | `COUNT` | Total cost incurred by LLM usage |
| Average cost per request | stats | `LLM_PROMPT_TOKEN_TOTAL_COST` | `AVG` | Average cost incurred per LLM request |
| Average tokens per request | stats | `LLM_PROMPT_TOTAL_TOKEN` | `AVG` | Average number of tokens consumed per LLM request |
| Total requests | stats | `HTTP_REQUESTS` | `COUNT` | Total number of HTTP requests processed by the gateway |
| Token count over time | line | `LLM_PROMPT_TOTAL_TOKEN`, `LLM_PROMPT_TOKEN_SENT`, `LLM_PROMPT_TOKEN_RECEIVED` | `COUNT` | Evolution of token consumption (prompt, completion, and total) |
| Token cost over time | line | `LLM_PROMPT_TOKEN_TOTAL_COST`, `LLM_PROMPT_TOKEN_SENT_COST`, `LLM_PROMPT_TOKEN_RECEIVED_COST` | `COUNT` | Evolution of LLM costs over time, broken down by prompt and completion |
| Total tokens per model | doughnut | `LLM_PROMPT_TOTAL_TOKEN` | `COUNT` | Distribution of total tokens consumed across different LLM models (grouped by `LLM_PROXY_MODEL`, top 5) |
| Response status repartition | doughnut | `HTTP_REQUESTS` | `COUNT` | Distribution of HTTP response status codes for LLM requests (grouped by `HTTP_STATUS_CODE_GROUP`, filtered by `API_TYPE = LLM`) |

The template is labeled with `Focus: 'LLM / Tokens'` and `Theme: 'AI'` and uses the `API_TYPE = LLM` filter to isolate LLM-specific traffic.

## Prerequisites

- Elasticsearch cluster with scripting enabled (required for computed metrics `LLM_PROMPT_TOTAL_TOKEN` and `LLM_PROMPT_TOKEN_COST`)
- Analytics data indexed with `additional-metrics.keyword_llm-proxy_model`, `additional-metrics.keyword_llm-proxy_provider`, `additional-metrics.long_llm-proxy_tokens-sent`, `additional-metrics.long_llm-proxy_tokens-received`, `additional-metrics.double_llm-proxy_sent-cost`, and `additional-metrics.double_llm-proxy_received-cost` fields
- APIs configured with `API_TYPE = LLM` for dashboard template filtering

## Gateway Configuration

## Creating LLM Analytics Queries

To query LLM metrics via the Analytics API, construct a request with the `metrics` array containing one or more LLM metric names (`LLM_PROMPT_TOTAL_TOKEN`, `LLM_PROMPT_TOKEN_COST`) and specify the desired `measures` (`COUNT`, `AVG`). Apply filters using `LLM_PROXY_MODEL` or `LLM_PROXY_PROVIDER` to segment results by model or provider.

For faceted queries, include `by` with up to three facet names (minimum one, maximum three for facets; maximum two for time-series). For example, to retrieve average total tokens per model, set `metrics: [{ name: 'LLM_PROMPT_TOTAL_TOKEN', measures: ['AVG'] }]` and `by: ['LLM_PROXY_MODEL']`.

The Analytics API enforces `minItems: 1` on the `metrics` array and `minItems: 1`, `maxItems: 3` on facet `by` arrays.

{% hint style="info" %}
The `sorts` property in `MetricRequest` is defined in the TypeScript interface but not documented in the OpenAPI schema.

The `API_TYPE` filter is used in widget configurations but is not explicitly listed in the `FilterName` enum in the OpenAPI schema.
{% endhint %}
