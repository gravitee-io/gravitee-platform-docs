# Query LLM Metrics and Configure LLM Dashboards

## Configuring LLM Dashboards

To create an LLM dashboard, select the LLM template (`llm`) from the dashboard template library. The template includes nine widgets pre-configured with LLM metrics, filters, and visualizations.

### Dashboard Template

The LLM template provides a centralized view of LLM usage, token consumption, and costs. The template includes the following widgets:

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

### Filter Merging

Dashboard-level filters (time range, environment) are merged with widget-level filters (e.g., `API_TYPE = LLM`) at query time. Widget configurations are not mutated; filters are combined in the HTTP request body sent to the Analytics API.

### Customization

Customize widget titles, metrics, or filters as needed. For example, the "Total tokens per model" widget groups `LLM_PROMPT_TOTAL_TOKEN` by `LLM_PROXY_MODEL` and displays the top five models. The "Token cost over time" line chart tracks `LLM_PROMPT_TOKEN_TOTAL_COST`, `LLM_PROMPT_TOKEN_SENT_COST`, and `LLM_PROMPT_TOKEN_RECEIVED_COST` over time.

{% hint style="info" %}
The `AVG` measure no longer displays a unit suffix. Verify metric semantics when interpreting average values.
{% endhint %}

## End-User Configuration

## Restrictions

`LLM_PROMPT_TOTAL_TOKEN` and `LLM_PROMPT_TOKEN_COST` are computed metrics requiring Elasticsearch scripted aggregations. Elasticsearch scripting must be enabled.

`LLM_PROXY_MODEL` and `LLM_PROXY_PROVIDER` filters and facets require `additional-metrics.keyword_llm-proxy_model` and `additional-metrics.keyword_llm-proxy_provider` fields to be indexed and populated. Queries return no results or empty facets if fields are missing.

Facet queries support a minimum of 1 and maximum of 3 facets (`by` array). Time-series queries support a maximum of 2 facets.

Metric queries require at least 1 metric in the `metrics` array.

