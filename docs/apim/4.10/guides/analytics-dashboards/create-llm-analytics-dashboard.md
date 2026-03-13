### Overview

This guide explains how to create and use an LLM analytics dashboard to monitor LLM proxy usage, token consumption, and costs across your environment.

The LLM dashboard template provides pre-configured widgets that track request volume, token usage, cost evolution, and response status distribution. Apply environment-level filters to refine the view by API, application, or plan.

### Prerequisites

Before creating an LLM analytics dashboard, ensure the following:

* Gravitee APIM with the new analytics engine enabled
* LLM proxy APIs configured and generating traffic
* Elasticsearch backend storing `additional-metrics` fields for LLM token and cost data
* Console UI access to environment-level analytics dashboards

### Create an LLM analytics dashboard

1. Navigate to the environment-level analytics section in the Console UI.
2. Select the **LLM** template.

The template pre-populates 10 widgets that display LLM usage metrics.

### Dashboard widgets

The LLM dashboard template includes the following widgets:

| Widget | Type | Description |
|:-------|:-----|:------------|
| LLM requests | Stats | Number of requests targeting LLM providers (filtered by `API_TYPE=LLM`) |
| Total tokens | Stats | Total number of tokens processed |
| Total cost | Stats | Total cost incurred by LLM usage |
| Average cost per request | Stats | Average cost per LLM request |
| Average tokens per request | Stats | Average tokens consumed per request |
| Total requests | Stats | Total HTTP requests processed |
| Token count over time | Line chart | Evolution of token consumption (total, sent, and received) |
| Token cost over time | Line chart | Evolution of LLM costs over time (total, sent, and received) |
| Total tokens per model | Doughnut chart | Distribution of tokens across models (top 5, sorted descending) |
| Response status repartition | Doughnut chart | Distribution of HTTP response statuses (filtered by `API_TYPE=LLM`) |

The template is tagged with **Focus: LLM / Tokens** and **Theme: AI**. A preview image displays at `assets/images/templates/llm-preview.png`.

### Apply filters

Apply environment-level filters to refine the dashboard view:

* Filter by API to view metrics for specific LLM proxy APIs
* Filter by application to view metrics for specific consumer applications
* Filter by plan to view metrics for specific subscription plans

Widget-level filters merge with dashboard-level filters at query time. Both sets of filters are sent to the backend. The original widget configuration remains unchanged.

### Filter by provider and model

Two dimensions enable grouping and filtering by LLM provider and model:

| Filter/Facet | Elasticsearch Field | Operators |
|:-------------|:-------------------|:----------|
| `LLM_PROXY_MODEL` | `additional-metrics.keyword_llm-proxy_model` | EQ, IN |
| `LLM_PROXY_PROVIDER` | `additional-metrics.keyword_llm-proxy_provider` | EQ, IN |

All LLM metrics support these filters and facets.

