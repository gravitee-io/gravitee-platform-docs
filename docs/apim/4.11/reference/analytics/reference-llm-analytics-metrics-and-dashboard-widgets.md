# Reference: LLM Analytics Metrics and Dashboard Widgets

## Overview

LLM Analytics and Dashboard Enhancements introduces token consumption and cost tracking for Large Language Model (LLM) integrations, along with a dedicated dashboard template for monitoring AI usage. This feature enables API platform administrators to measure total and average token counts, track associated costs over time, and analyze usage patterns by model and provider. The AI Gateway template has been renamed to LLM and now includes widgets tailored to LLM-specific metrics.

## Key Concepts

### LLM Metrics

The platform computes two aggregate metrics from token and cost data captured during LLM requests:

| Metric | Aggregation | Description |
|:-------|:------------|:------------|
| `LLM_PROMPT_TOTAL_TOKEN` | COUNT, AVG | Total or average tokens (sent + received) |
| `LLM_PROMPT_TOKEN_COST` | COUNT, AVG | Total or average cost (sent + received) |

`LLM_PROMPT_TOTAL_TOKEN` sums the tokens sent (prompt) and received (completion) for each request. `LLM_PROMPT_TOKEN_COST` sums the associated costs for sent and received tokens. Both metrics support count (total) and average aggregations.

### LLM Facets and Filters

Administrators can filter and group analytics data by **LLM Proxy Model** (e.g., `gpt-4`) and **LLM Proxy Provider** (e.g., `openai`). These facets enable cost and usage analysis per model or provider. The **API Type** filter distinguishes LLM requests from generic HTTP proxy traffic, ensuring accurate scoping of LLM-specific metrics.

### Dashboard Widgets

The LLM dashboard template includes ten widgets:

| Widget Title | Type | Metrics | Description |
|:-------------|:-----|:--------|:------------|
| LLM requests | stats | `HTTP_REQUESTS` (COUNT, filtered by `API_TYPE=LLM`) | Number of requests targeting LLM providers. |
| Total tokens | stats | `LLM_PROMPT_TOTAL_TOKEN` (COUNT) | Total number of tokens processed (prompt and completion). |
| Total cost | stats | `LLM_PROMPT_TOKEN_TOTAL_COST` (COUNT) | Total cost incurred by LLM usage. |
| Average cost per request | stats | `LLM_PROMPT_TOKEN_TOTAL_COST` (AVG) | Average cost incurred per LLM request. |
| Average tokens per request | stats | `LLM_PROMPT_TOTAL_TOKEN` (AVG) | Average number of tokens consumed per LLM request. |
| Total requests | stats | `HTTP_REQUESTS` (COUNT) | Total number of HTTP requests processed by the gateway. |
| Token count over time | line | `LLM_PROMPT_TOTAL_TOKEN`, `LLM_PROMPT_TOKEN_SENT`, `LLM_PROMPT_TOKEN_RECEIVED` (COUNT) | Evolution of token consumption (prompt, completion, and total). |
| Token cost over time | line | `LLM_PROMPT_TOKEN_TOTAL_COST`, `LLM_PROMPT_TOKEN_SENT_COST`, `LLM_PROMPT_TOKEN_RECEIVED_COST` (COUNT, 1h interval) | Evolution of LLM costs over time, broken down by prompt and completion. |
| Total tokens per model | doughnut | `LLM_PROMPT_TOTAL_TOKEN` (COUNT, grouped by `LLM_PROXY_MODEL`, limit 5, sorted by COUNT DESC) | Distribution of total tokens consumed across different LLM models. |
| Response status repartition | doughnut | `HTTP_REQUESTS` (COUNT, grouped by `HTTP_STATUS_CODE_GROUP`, filtered by `API_TYPE=LLM`) | Distribution of HTTP response status codes for LLM requests. |

Widgets display token consumption trends, cost evolution, and model-level distribution, providing a centralized view of AI integration performance.

## Prerequisites

Before creating LLM analytics dashboards, ensure the following:

* Elasticsearch index includes the following keyword fields:
  * `additional-metrics.keyword_llm-proxy_model`
  * `additional-metrics.keyword_llm-proxy_provider`
* Analytics records populate the following fields for LLM requests:
  * `additional-metrics.long_llm-proxy_tokens-sent`
  * `additional-metrics.long_llm-proxy_tokens-received`
  * `additional-metrics.double_llm-proxy_sent-cost`
  * `additional-metrics.double_llm-proxy_received-cost`
* User has the following permissions:
  * `Environment-dashboard-r`: View dashboards
  * `Environment-dashboard-c`: Create dashboards
  * `Environment-dashboard-u`: Update dashboards
  * `Environment-dashboard-d`: Delete dashboards

## Gateway Configuration

## Creating LLM Analytics Dashboards

1. Navigate to **Observability** > **Dashboards**. For detailed instructions, see [How-To: Create an LLM Dashboard from Template](../../guides/observability/how-to-create-an-llm-dashboard-from-template.md).
2. Click **Create dashboard** > **Create from template**.
3. Select the **LLM** template in the left panel and click **Use template**.
4. (Optional) Apply filters at the dashboard level (e.g., filter by specific models or providers) or at the widget level. Dashboard-level filters merge with widget-level filters at query time.
5. (Optional) Adjust the timeframe for the dashboard.
6. Click **Save**.

The dashboard initializes with a default configuration named `New LLM Dashboard - {timestamp}` and includes ten pre-configured widgets. You can customize the dashboard by applying filters to scope the entire dashboard to a subset of LLM traffic while preserving widget-specific constraints.

## Querying LLM Metrics via Analytics API

To retrieve LLM metrics programmatically, submit a request to the Analytics API with the desired metric name (`LLM_PROMPT_TOTAL_TOKEN` or `LLM_PROMPT_TOKEN_COST`), measure (`COUNT` or `AVG`), and optional filters (`LLM_PROXY_MODEL`, `LLM_PROXY_PROVIDER`, `API_TYPE`).

### Facets Request

| Property | Description | Example |
|:---------|:------------|:--------|
| `by` | Array of facet names (1–3 items) | `["LLM_PROXY_MODEL", "LLM_PROXY_PROVIDER"]` |
| `metrics` | Array of metric requests (minimum 1) | See metric request structure below |
| `sorts` | (Optional) Array of sort filters | `[{ "measure": "COUNT", "order": "DESC" }]` |

For time-series data, specify the interval (e.g., `1h`) and include the metric in the `metrics` array. For faceted aggregations, include the facet name in the `by` array (maximum 3 facets) and optionally sort results by measure value using the `sorts` field. The API returns aggregated token counts, costs, or averages grouped by the specified dimensions.

{% hint style="info" %}
`LLM_PROMPT_TOTAL_TOKEN` and `LLM_PROMPT_TOKEN_COST` metrics are computed using Elasticsearch scripted aggregations, which may have performance implications on large datasets.
{% endhint %}

{% hint style="warning" %}
The `LLM_PROMPT_TOTAL_TOKEN` and `LLM_PROMPT_TOKEN_COST` metrics return `0` if either the sent or received field is missing in the document.
{% endhint %}

{% hint style="info" %}
Widget-level filters are merged with dashboard-level filters at request time. There is no UI indication of which filters originate from the widget configuration versus the dashboard context.
{% endhint %}

