# Configure LLM Analytics in Elasticsearch

## Dashboard Template

The LLM dashboard template (id: `llm`) replaces the previous AI Gateway template. It provides 10 pre-configured widgets monitoring token consumption, cost trends, and model-specific usage. The template targets APIs with `API_TYPE = 'LLM'` and includes time-series charts for token count and cost, faceted breakdowns by model and HTTP status, and summary statistics for total/average tokens and costs.

## Prerequisites

Before you configure LLM analytics in Elasticsearch, ensure the following:

* Gravitee API Management platform with Elasticsearch-backed analytics
* APIs configured with LLM proxy policies that populate `additional-metrics` fields (tokens-sent, tokens-received, sent-cost, received-cost, model, provider)
* Analytics data retention policy sufficient for cost tracking requirements
* User permissions:
 * `Environment-dashboard-r`: View dashboards
 * `Environment-dashboard-c`: Create dashboards
 * `Environment-dashboard-u`: Update dashboards
 * `Environment-dashboard-d`: Delete dashboards

## Gateway Configuration

### Elasticsearch Aggregation Scripts

The gateway uses Painless scripts to compute LLM metrics from additional-metrics fields. These scripts handle missing fields gracefully (defaulting to 0).

**LLM Total Token Script:**

```painless
(doc['additional-metrics.long_llm-proxy_tokens-sent'].size() > 0 ? doc['additional-metrics.long_llm-proxy_tokens-sent'].value : 0) + \
(doc['additional-metrics.long_llm-proxy_tokens-received'].size() > 0 ? doc['additional-metrics.long_llm-proxy_tokens-received'].value : 0)
```

**LLM Total Cost Script:**

```painless
(doc['additional-metrics.double_llm-proxy_sent-cost'].size() > 0 ? doc['additional-metrics.double_llm-proxy_sent-cost'].value : 0) + \
(doc['additional-metrics.double_llm-proxy_received-cost'].size() > 0 ? doc['additional-metrics.double_llm-proxy_received-cost'].value : 0)
```

Both scripts support `buildSum` and `buildAvg` aggregation types.

### Analytics Definition

The `analytics-definition.yaml` configuration includes metric, facet, and filter definitions for LLM analytics.

**Metric Configuration:**

| Property | LLM_PROMPT_TOTAL_TOKEN | LLM_PROMPT_TOKEN_COST |
|:---------|:----------------------|:---------------------|
| Label | Total token count | Total token cost |
| APIs | LLM | LLM |
| Type | COUNTER | GAUGE |
| Unit | (none) | NUMBER |
| Measures | COUNT, AVG | COUNT, AVG |

Both metrics support faceting and filtering by: API, APPLICATION, PLAN, GATEWAY, TENANT, ZONE, HTTP_METHOD, HTTP_STATUS_CODE_GROUP, HTTP_STATUS, HTTP_PATH, HTTP_PATH_MAPPING, HTTP_USER_AGENT_OS_NAME, HTTP_USER_AGENT_DEVICE, HOST, GEO_IP_COUNTRY, GEO_IP_REGION, GEO_IP_CITY, GEO_IP_CONTINENT, CONSUMER_IP, LLM_PROXY_MODEL, LLM_PROXY_PROVIDER.

Filters additionally include HTTP_ENDPOINT_RESPONSE_TIME, HTTP_GATEWAY_LATENCY, HTTP_GATEWAY_RESPONSE_TIME.

**Facet/Filter Configuration:**

| Property | Type | Operators | Elasticsearch Field |
|:---------|:-----|:----------|:-------------------|
| LLM_PROXY_MODEL | KEYWORD | EQ, IN | `additional-metrics.keyword_llm-proxy_model` |
| LLM_PROXY_PROVIDER | KEYWORD | EQ, IN | `additional-metrics.keyword_llm-proxy_provider` |

All existing HTTP and LLM metrics now support `LLM_PROXY_MODEL` and `LLM_PROXY_PROVIDER` as additional facets and filters.

## Creating LLM Analytics Queries

To query LLM token or cost metrics, construct a `MetricRequest` with the metric name (`LLM_PROMPT_TOTAL_TOKEN` or `LLM_PROMPT_TOKEN_COST`), desired measures (`COUNT` or `AVG`), and optional filters/facets.

1. Select the metric and measures in your analytics API request.
2. Add filters to scope the query (e.g., `API_TYPE = 'LLM'`, `LLM_PROXY_MODEL IN ['gpt-4', 'claude-3']`).
3. Specify facets to group results (e.g., by `LLM_PROXY_PROVIDER` or `LLM_PROXY_MODEL`).
4. (Optional) Add sorts using the `SortFilter` interface (measure + order).
5. Submit the request to the analytics API endpoint.

The response includes aggregated token counts, costs, or averages based on your configuration.

## Creating an LLM Dashboard

To create an LLM dashboard from the template:

1. Navigate to **Observability** > **Dashboards**.
2. Click **Create dashboard** > **Create from template**.
3. Select the **LLM** template in the left panel and click **Use template**.
4. The platform creates the dashboard and redirects to the new dashboard view.
5. Adjust filters or the timeframe to customize the dashboard view.

### Verification

To verify the dashboard was created successfully, navigate back to **Observability** > **Dashboards**. The new LLM dashboard appears in the dashboard list.

{% hint style="warning" %}
If the dashboard displays no data, verify that:
* The Elasticsearch backend is running
* LLM APIs are generating traffic and populating `additional-metrics` fields
{% endhint %}

### Next Steps

After creating an LLM dashboard, you can:

* Create additional custom dashboards
* Add filters to focus on specific models, providers, or cost ranges
* Monitor for abnormal behavior, increased errors, or unusual token consumption
