# LLM Analytics Migration and Related Changes

## Related Changes

### Dashboard Template Rename

The **AI Gateway** dashboard template has been renamed to **LLM**. The template ID changed from `ai-gateway` to `llm`, and the preview image changed from `ai-gateway-preview.png` to `llm-preview.png`. Users referencing the `ai-gateway` template by ID or name must update to `llm`.

### Proxy Generic Protocol Template Updates

The **Proxy Generic Protocol** template (`proxy-performance`) has been updated with the following changes:

**Widget title clarifications:**

| Before | After |
|:-------|:------|
| Average Latency | Average Latency in ms |
| Average Response Time | Average Response Time in ms |
| Response Time | Response Time (description: Average response time of the Endpoint and Gateway in ms) |

**Filter addition:**

The "HTTP Requests" widget now includes a filter: `API_TYPE = HTTP_PROXY`.

### Measure Unit Display Change

The `AVG` measure unit display has been changed from `ms` to an empty string. Existing dashboards displaying `AVG` measures will no longer show the `ms` suffix.

### Dashboard Filter Merging

Dashboard-level filters are now merged with widget-level filters at request time. Widget configurations are not mutated; filters are combined in the HTTP request body sent to the analytics API. This enables dynamic filter composition without modifying widget configurations.

### TypeScript Type Definition Extensions

TypeScript type definitions have been extended to support new analytics capabilities:

**New facet types:**

```typescript
export type LlmFacetName = 'LLM_PROXY_MODEL' | 'LLM_PROXY_PROVIDER';
export type McpFacetName = 'MCP_PROXY_METHOD' | 'MCP_PROXY_TOOL' | 'MCP_PROXY_RESOURCE' | 'MCP_PROXY_PROMPT';
```

**New filter types:**

```typescript
export type LlmFilterName = 'LLM_PROXY_MODEL' | 'LLM_PROXY_PROVIDER';
export type McpFilterName = 'MCP_PROXY_METHOD' | 'MCP_PROXY_TOOL' | 'MCP_PROXY_RESOURCE' | 'MCP_PROXY_PROMPT';
export type ApiFilterName = 'API_STATE' | 'API_LIFECYCLE_STATE' | 'API_VISIBILITY' | 'API_TYPE';
```

**New metric types:**

```typescript
export type LlmMetricName =
  | 'LLM_PROMPT_TOKEN_SENT'
  | 'LLM_PROMPT_TOKEN_RECEIVED'
  | 'LLM_PROMPT_TOKEN_SENT_COST'
  | 'LLM_PROMPT_TOKEN_RECEIVED_COST'
  | 'LLM_PROMPT_TOTAL_TOKEN'
  | 'LLM_PROMPT_TOKEN_TOTAL_COST';
```

**Updated request interface:**

```typescript
export interface SortFilter {
  measure: MeasureName;
  order: 'ASC' | 'DESC';
}

export interface MetricRequest {
  name: MetricName;
  measures: MeasureName[];
  filters?: RequestFilter[];
  sorts?: SortFilter[];
}
```
