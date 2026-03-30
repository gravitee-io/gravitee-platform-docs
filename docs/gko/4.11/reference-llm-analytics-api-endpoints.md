# Reference: LLM Analytics API Endpoints

## Querying LLM Metrics via Analytics API

To retrieve LLM metrics programmatically, submit a request to the Analytics API with the desired metric name (`LLM_PROMPT_TOTAL_TOKEN` or `LLM_PROMPT_TOKEN_COST`), measure (`COUNT` or `AVG`), and optional filters (`LLM_PROXY_MODEL`, `LLM_PROXY_PROVIDER`, `API_TYPE`). For time-series data, specify the interval (e.g., `1h`) and include the metric in the `metrics` array. For faceted aggregations, include the facet name in the `by` array (maximum 3 facets) and optionally sort results by measure value using the `sorts` field. The API returns aggregated token counts, costs, or averages grouped by the specified dimensions.

## End-User Configuration

### Analytics API Endpoints

#### Facets Request

| Property | Description | Example |
|:---------|:------------|:--------|
| `by` | Array of facet names (1–3 items) | `["LLM_PROXY_MODEL", "LLM_PROXY_PROVIDER"]` |
| `metrics` | Array of metric requests (minimum 1) | `[{ "name": "LLM_PROMPT_TOTAL_TOKEN", "measures": ["COUNT"] }]` |
| `filters` | Optional array of filter objects | `[{ "name": "API_TYPE", "operator": "EQ", "value": "LLM" }]` |

#### Time Series Request

| Property | Description | Example |
|:---------|:------------|:--------|
| `by` | Array of facet names (maximum 2) | `["LLM_PROXY_MODEL"]` |
| `metrics` | Array of metric requests (minimum 1) | `[{ "name": "LLM_PROMPT_TOKEN_COST", "measures": ["AVG"], "sorts": [{ "measure": "AVG", "order": "DESC" }] }]` |
| `filters` | Optional array of filter objects | `[{ "name": "LLM_PROXY_PROVIDER", "operator": "EQ", "value": "openai" }]` |

#### Metric Request

| Property | Description | Example |
|:---------|:------------|:--------|
| `name` | Metric name | `LLM_PROMPT_TOTAL_TOKEN` |
| `measures` | Array of measure names | `["COUNT", "AVG"]` |
| `filters` | Optional array of filter objects | `[{ "name": "LLM_PROXY_MODEL", "operator": "EQ", "value": "gpt-4" }]` |
| `sorts` | Optional array of sort filters | `[{ "measure": "COUNT", "order": "DESC" }]` |

## Restrictions

- `LLM_PROMPT_TOTAL_TOKEN` and `LLM_PROMPT_TOKEN_COST` metrics are computed using Elasticsearch scripted aggregations, which may impact performance on large datasets.
- Both metrics return `0` if either the sent or received field is missing in the analytics document.
- Widget-level filters merge with dashboard-level filters at request time; the UI does not indicate which filters originate from the widget configuration versus the dashboard context.
- The `API_TYPE` filter is used internally to distinguish LLM requests from HTTP proxy requests but is not exposed as a user-selectable facet in the dashboard UI.
- The `AVG` measure no longer appends a `ms` suffix by default; widgets displaying average values should specify units explicitly in titles or descriptions.
