# LLM Analytics Metrics and Dashboard Reference

## Overview

LLM Analytics and Dashboard Enhancements introduces six new metrics for tracking token consumption and costs in LLM-based APIs, along with a dedicated dashboard template for monitoring AI integrations. The feature enables API administrators to measure total tokens, token costs, and usage patterns across LLM providers and models. It replaces the previous AI Gateway template with an LLM-focused dashboard that provides real-time visibility into token usage, cost trends, and response status distribution.

## Key Concepts

### LLM Metrics

The feature introduces six metrics for tracking LLM usage and costs. Token metrics measure the number of tokens sent to and received from LLM providers, while cost metrics track the associated expenses. The `LLM_PROMPT_TOTAL_TOKEN` metric aggregates sent and received tokens, and `LLM_PROMPT_TOKEN_TOTAL_COST` aggregates sent and received costs. These metrics are computed using Elasticsearch scripted aggregations that sum values from the `additional-metrics` field in analytics documents.

| Metric | Description | Computation |
|:-------|:------------|:------------|
| `LLM_PROMPT_TOKEN_SENT` | Tokens sent to LLM provider | Direct field value |
| `LLM_PROMPT_TOKEN_RECEIVED` | Tokens received from LLM provider | Direct field value |
| `LLM_PROMPT_TOKEN_SENT_COST` | Cost of tokens sent | Direct field value |
| `LLM_PROMPT_TOKEN_RECEIVED_COST` | Cost of tokens received | Direct field value |
| `LLM_PROMPT_TOTAL_TOKEN` | Total tokens (sent + received) | Sum of sent and received tokens |
| `LLM_PROMPT_TOKEN_TOTAL_COST` | Total cost (sent + received) | Sum of sent and received costs |

### LLM Facets and Filters

Two facets enable grouping and filtering analytics data by LLM provider and model. The `LLM_PROXY_MODEL` facet groups data by the specific model used (e.g., `gpt-4`), while `LLM_PROXY_PROVIDER` groups by provider (e.g., `openai`). These facets can be used in dashboard widgets to analyze usage patterns across different models and providers. Corresponding filters allow users to narrow analytics queries to specific models or providers.

| Facet/Filter | Elasticsearch Field | Example Value |
|:-------------|:-------------------|:--------------|
| `LLM_PROXY_MODEL` | `additional-metrics.keyword_llm-proxy_model` | `gpt-4` |
| `LLM_PROXY_PROVIDER` | `additional-metrics.keyword_llm-proxy_provider` | `openai` |

### LLM Dashboard Template

The LLM dashboard template provides a pre-configured set of widgets for monitoring LLM usage, token consumption, and costs. It includes stats widgets for total requests, tokens, and costs, line charts for tracking token and cost trends over time, and doughnut charts for analyzing usage distribution by model and response status. The template replaces the previous AI Gateway template and is labeled with `Focus: LLM / Tokens` and `Theme: AI`.

The template includes the following widgets:

| Widget Title | Type | Metric | Measures | Filters |
|:-------------|:-----|:-------|:---------|:--------|
| LLM requests | stats | `HTTP_REQUESTS` | `COUNT` | `API_TYPE` = `LLM` |
| Total tokens | stats | `LLM_PROMPT_TOTAL_TOKEN` | `COUNT` | — |
| Total cost | stats | `LLM_PROMPT_TOKEN_TOTAL_COST` | `COUNT` | — |
| Average cost per request | stats | `LLM_PROMPT_TOKEN_TOTAL_COST` | `AVG` | — |
| Average tokens per request | stats | `LLM_PROMPT_TOTAL_TOKEN` | `AVG` | — |
| Total requests | stats | `HTTP_REQUESTS` | `COUNT` | — |
| Token count over time | line | `LLM_PROMPT_TOTAL_TOKEN`, `LLM_PROMPT_TOKEN_SENT`, `LLM_PROMPT_TOKEN_RECEIVED` | `COUNT` | — |
| Token cost over time | line | `LLM_PROMPT_TOKEN_TOTAL_COST`, `LLM_PROMPT_TOKEN_SENT_COST`, `LLM_PROMPT_TOKEN_RECEIVED_COST` | `COUNT` | — |
| Total tokens per model | doughnut | `LLM_PROMPT_TOTAL_TOKEN` | `COUNT` | — |
| Response status repartition | doughnut | `HTTP_REQUESTS` | `COUNT` | `API_TYPE` = `LLM` |

## Prerequisites

Before creating an LLM dashboard, ensure you have the following permissions:

* `Environment-dashboard-r`: View dashboards
* `Environment-dashboard-c`: Create dashboards
* `Environment-dashboard-u`: Update dashboards
* `Environment-dashboard-d`: Delete dashboards

<!-- GAP: Elasticsearch configuration requirements not documented in source materials -->
<!-- GAP: No information provided on how LLM-based APIs are instrumented to populate additional-metrics fields with token and cost data -->

## Gateway Configuration

## Querying LLM Analytics

<!-- GAP: Analytics API query procedures not documented in source materials -->

### Analytics API Schema Reference

The Analytics API supports the following LLM-specific elements:

**Facets**: `LLM_PROXY_MODEL`, `LLM_PROXY_PROVIDER`  
**Metrics**: `LLM_PROMPT_TOTAL_TOKEN`, `LLM_PROMPT_TOKEN_TOTAL_COST`, `LLM_PROMPT_TOKEN_SENT`, `LLM_PROMPT_TOKEN_RECEIVED`, `LLM_PROMPT_TOKEN_SENT_COST`, `LLM_PROMPT_TOKEN_RECEIVED_COST`  
**Filters**: `LLM_PROXY_MODEL`, `LLM_PROXY_PROVIDER`

For complete API usage, refer to the Analytics API documentation.

## End-User Configuration

## Restrictions

- `LLM_PROMPT_TOTAL_TOKEN` and `LLM_PROMPT_TOKEN_TOTAL_COST` metrics use Elasticsearch scripted aggregations, which may impact performance on large datasets.
- Scripted aggregations default missing fields to `0`. If `additional-metrics.long_llm-proxy_tokens-sent`, `additional-metrics.long_llm-proxy_tokens-received`, `additional-metrics.double_llm-proxy_sent-cost`, or `additional-metrics.double_llm-proxy_received-cost` are absent, the corresponding values are treated as zero.
- Widget-level filters are merged with dashboard-level filters at request time. There is no mechanism to override or exclude dashboard filters at the widget level.
- The `AVG` measure no longer displays a unit suffix. Stats widgets showing `AVG` measures will display raw values without automatic unit appending.

## Related Changes

The AI Gateway dashboard template has been renamed to LLM (template ID changed from `ai-gateway` to `llm`), and the preview image has been updated from `ai-gateway-preview.png` to `llm-preview.png`. The HTTP Proxy template has been updated with clarified widget titles (e.g., "Average Latency in ms" instead of "Average Latency") and a new filter (`API_TYPE` = `HTTP_PROXY`) on the HTTP_REQUESTS widget. TypeScript type definitions have been extended to include `LlmFacetName`, `LlmFilterName`, and `LlmMetricName` types, along with new `SortFilter` and `MetricRequest` interfaces for analytics requests.
