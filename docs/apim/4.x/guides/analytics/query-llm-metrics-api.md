### Querying LLM Metrics via Analytics API

To query LLM metrics programmatically, use the analytics API with the metric names `LLM_PROMPT_TOTAL_TOKEN` and `LLM_PROMPT_TOKEN_COST`. These computed metrics aggregate token counts and costs from underlying Elasticsearch fields.

#### Specifying Measures

Include the `measures` property in your metric request to define the aggregation type. Supported measures for computed LLM metrics are:

* `COUNT`: Total sum of the metric across all requests
* `AVG`: Average value of the metric per request

Example request structure:

```json
{
 "metrics": [
 {
 "name": "LLM_PROMPT_TOTAL_TOKEN",
 "measures": ["AVG"]
 }
 ]
}
```

#### Applying Filters

Use the `filters` property to narrow results by LLM-specific dimensions:

* `LLM_PROXY_MODEL`: Filter by model identifier (e.g., `gpt-4`)
* `LLM_PROXY_PROVIDER`: Filter by provider identifier (e.g., `openai`)

Filters support the `EQ` and `IN` (matches any) operators.

#### Grouping with Facets

Use the `by` parameter to group results by one or more dimensions. LLM-specific facets include:

* `LLM_PROXY_MODEL`: Group by model
* `LLM_PROXY_PROVIDER`: Group by provider

Example: To retrieve average total tokens grouped by model, set:

```json
{
 "metrics": [
 {
 "name": "LLM_PROMPT_TOTAL_TOKEN",
 "measures": ["AVG"]
 }
 ],
 "by": ["LLM_PROXY_MODEL"]
}
```

#### Sorting Results

Use the `sorts` property within a metric request to order results by a specific measure. Specify the measure name and sort order (`ASC` or `DESC`).

Example:

```json
{
 "metrics": [
 {
 "name": "LLM_PROMPT_TOTAL_TOKEN",
 "measures": ["COUNT"],
 "sorts": [
 {
 "measure": "COUNT",
 "order": "DESC"
 }
 ]
 }
 ]
}
```

#### Request Constraints

The analytics API enforces the following limits on grouping dimensions:

* **Facet requests**: Minimum 1 dimension (`minItems: 1`), maximum 3 dimensions (`maxItems: 3`)
* **Time series requests**: Maximum 2 dimensions (`maxItems: 2`)

The OpenAPI schema uses `minItems` and `maxItems` constraints for array properties (changed from `minimum` and `maximum` in earlier versions).

#### Field Mappings

LLM filters and facets map to Elasticsearch keyword fields:

| Filter/Facet Name | Elasticsearch Field |
|:------------------|:-------------------|
| `LLM_PROXY_MODEL` | `additional-metrics.keyword_llm-proxy_model` |
| `LLM_PROXY_PROVIDER` | `additional-metrics.keyword_llm-proxy_provider` |

These mappings are required for the analytics engine to resolve queries correctly.
