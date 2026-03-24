
# LLM Analytics API Reference

For configuration guidance, see [Query LLM Metrics and Configure Dashboards](query-llm-metrics-and-configure-dashboards.md).


## Restrictions

- LLM metrics require Elasticsearch-backed analytics (not available with in-memory or other analytics backends)
- `LLM_PROMPT_TOTAL_TOKEN` and `LLM_PROMPT_TOKEN_COST` only populate when LLM proxy policies write to `additional-metrics` fields
- Facet requests limited to 3 dimensions (`by` maxItems: 3)
- Time-series requests limited to 2 grouping dimensions (`by` maxItems: 2)
- `LLM_PROXY_MODEL` and `LLM_PROXY_PROVIDER` filters support only `EQ` and `IN` operators
- Average measure (`AVG`) no longer displays unit suffix in stats widgets (changed from "ms" to empty string)

## Related Changes

The HTTP Proxy dashboard template now filters the HTTP_REQUESTS widget by `API_TYPE = 'HTTP_PROXY'` to exclude LLM traffic. Widget titles in the HTTP Proxy template updated for clarity: "Average Latency" → "Average Latency in ms", "Average Response Time" → "Average Response Time in ms". The stats component formatting changed to remove unit suffixes from `AVG` measures.
