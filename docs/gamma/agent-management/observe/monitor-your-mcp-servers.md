---
hidden: false
noIndex: true
---

# Monitor your MCP servers
<!-- GAP-STRUCTURAL: Missing procedural content source -->
<!-- GAP: 73 · Investigable · No source material covers the MCP-specific observability UI. Needs: Demo session, Source code, Engineering input, UI verification -->
<!-- GAP: 74 · Documentable · Document the MCP server metrics dashboard. Needs: Investigation -->

Monitor tool invocation metrics, error rates, and latency for your MCP Proxies through the AI Gateway observability layer.

## What you can monitor

The AI Gateway emits observability data for every tool invocation through an MCP Proxy. Expected metrics include:

| Metric               | Description                                                                |
| -------------------- | -------------------------------------------------------------------------- |
| **Tool invocations** | Total invocations per tool, per server, per consumer.                      |
| **Error rate**       | Percentage of invocations that return errors, by tool.                     |
| **Latency**          | P50, P95, and P99 latency per tool invocation.                             |
| **Auth failures**    | Invocations rejected by consumer authentication or authorization policies. |
| **Upstream health**  | Connection status and response times for upstream MCP servers.             |

## View MCP server metrics

1. From the Gamma console sidebar, select **Agent Management**.
2. Navigate to **Observe** → **MCP Servers**.
3. Select an MCP Proxy to view its metrics dashboard.

## Next steps

* [Inspect your agent log](inspect-your-agent-log.md) — Trace individual agent invocations through the AI Gateway.
* [Add policies to your MCP server](../build/configure-your-mcp/add-policies-to-mcp-server.md) — Respond to monitoring signals by adjusting authorization policies.
