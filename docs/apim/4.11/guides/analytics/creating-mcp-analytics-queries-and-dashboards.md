# Creating MCP Analytics Queries and Dashboards

## Gateway Configuration

<!-- GAP: Gateway configuration steps for enabling MCP analytics collection -->

## Creating MCP Analytics Queries

To query MCP analytics, construct requests using the Analytics API with MCP-specific facets and filters:

1. Select a metric from the supported set (e.g., `HTTP_REQUESTS`, `HTTP_GATEWAY_LATENCY`).
2. Add one or more MCP facets to group results by `MCP_PROXY_METHOD`, `MCP_PROXY_TOOL`, `MCP_PROXY_RESOURCE`, or `MCP_PROXY_PROMPT`.
3. Apply filters to narrow results. For example:
   * `MCP_PROXY_METHOD EQ 'initialize'`
   * `MCP_PROXY_TOOL IN ['search', 'fetch']`
4. Combine with the `API_TYPE = MCP` filter to isolate MCP traffic.

All HTTP metrics (requests, errors, content length, response time, latency) support these dimensions.

## Creating MCP Dashboards

To create an MCP dashboard from the template:

1. Navigate to **Observability** > **Dashboards**.
2. Click **Create dashboard** > **Create from template**.
3. Select the **MCP** template from the left panel and click **Use template**.

The template includes 12 pre-configured widgets:

* Five latency stats: average, max, P90, P99, total requests
* Method usage charts: vertical bar and time-series line
* Top-5 resources, prompts, and tools: vertical bar
* Response status distribution: doughnut
* Average response time over time: time-series line

Upon creation, the dashboard receives a default 7-day time range and unique widget IDs. All widgets filter by `API_TYPE = MCP` to isolate MCP traffic. Customize widget filters, time ranges, and aggregation limits as needed.

## End-User Configuration

### Analytics API Facets and Filters

| Property | Description | Example |
|:---------|:------------|:--------|
| `FacetName.MCP_PROXY_METHOD` | Groups results by MCP proxy method (e.g., `initialize`, `tools/call`) | `facets: [MCP_PROXY_METHOD]` |
| `FacetName.MCP_PROXY_TOOL` | Groups results by MCP tool name (e.g., `search`, `fetch`) | `facets: [MCP_PROXY_TOOL]` |
| `FacetName.MCP_PROXY_RESOURCE` | Groups results by MCP resource URI (e.g., `file:///docs/readme.md`) | `facets: [MCP_PROXY_RESOURCE]` |
| `FacetName.MCP_PROXY_PROMPT` | Groups results by MCP prompt name (e.g., `summarize`) | `facets: [MCP_PROXY_PROMPT]` |
| `FilterName.MCP_PROXY_METHOD` | Filters results by MCP proxy method | `filters: [{ field: MCP_PROXY_METHOD, operator: EQ, value: 'initialize' }]` |
| `FilterName.MCP_PROXY_TOOL` | Filters results by MCP tool name | `filters: [{ field: MCP_PROXY_TOOL, operator: IN, value: ['search', 'fetch'] }]` |
| `FilterName.MCP_PROXY_RESOURCE` | Filters results by MCP resource URI | `filters: [{ field: MCP_PROXY_RESOURCE, operator: EQ, value: 'file:///docs/readme.md' }]` |
| `FilterName.MCP_PROXY_PROMPT` | Filters results by MCP prompt name | `filters: [{ field: MCP_PROXY_PROMPT, operator: EQ, value: 'summarize' }]` |
