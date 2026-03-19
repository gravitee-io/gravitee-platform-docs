# MCP Dashboard Widget Reference

## Dashboard Widgets

The MCP dashboard template includes the following widgets:

| Widget | Type | Description |
|:-------|:-----|:------------|
| MCP requests | `stats` | Total request count for MCP APIs |
| Average latency | `stats` | Mean gateway latency for MCP requests |
| Max latency | `stats` | Maximum observed gateway latency |
| P90 latency | `stats` | 90th percentile gateway latency |
| P99 latency | `stats` | 99th percentile gateway latency |
| Method usage | `vertical-bar` | Top 10 MCP methods by request count |
| Method usage over time | `time-series-line` | Method usage evolution over time |
| Most used Resources | `vertical-bar` | Top 5 MCP resources by request count |
| Response status repartition | `doughnut` | HTTP status code distribution |
| Most used Prompts | `vertical-bar` | Top 5 MCP prompts by request count |
| Most used Tools | `vertical-bar` | Top 5 MCP tools by request count |
| Average response time | `time-series-line` | Mean gateway response time over time |
