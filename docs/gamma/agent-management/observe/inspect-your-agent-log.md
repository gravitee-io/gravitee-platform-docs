---
hidden: false
noIndex: false
---

# Inspect your agent log
<!-- GAP-STRUCTURAL: Missing procedural content source -->
<!-- GAP: 70 · Documentable · Document the lineage view UI — how to navigate traces, expand spans, filter. Needs: Demo session -->
<!-- GAP: 71 · Documentable · Document the search and filter capabilities in the agent log. Needs: UI verification -->

The agent log provides a detailed trace of every agent invocation through the AI Gateway, using OpenTelemetry (OTel) spans. Each span captures the full context of a single operation — who made the call, what tool was invoked, what data was sent and received, how long it took, what policies were evaluated, and what it cost.

## What a span contains

Each OTel span in the agent log records:

| Field               | Description                                                                        |
| ------------------- | ---------------------------------------------------------------------------------- |
| **Agent identity**  | The verified identity of the agent that initiated the invocation.                  |
| **Tool name**       | The specific tool invoked (for MCP traffic) or model called (for LLM traffic).     |
| **Inputs**          | The arguments or prompt sent to the tool or model.                                 |
| **Outputs**         | The response returned by the tool or model.                                        |
| **Latency**         | End-to-end duration of the invocation.                                             |
| **Policy decision** | Whether the invocation was permitted or denied, and which policies were evaluated. |
| **Cost**            | Token cost (for LLM traffic) or invocation cost based on configured rates.         |

## The lineage view

The lineage view provides a navigable trace of an agent's complete execution — from the initial user request through every tool invocation, model call, and sub-agent delegation.

A typical trace might show:

```
User request
  └── A2A Proxy → Agent (Customer Success bot)
        ├── LLM Proxy → Claude Sonnet (reasoning step)
        ├── MCP Proxy → HubSpot (lookup_contact)
        ├── MCP Proxy → Jira (create_ticket)
        └── LLM Proxy → Claude Sonnet (summarize result)
```

Each node in the lineage is a clickable span that expands to show the full detail (identity, inputs, outputs, latency, policy decision, cost).

## Search and filter

## Access the agent log

1. From the Gamma console sidebar, select **Agent Management**.
2. Navigate to **Observe** → **Agent Log**.
3. Select a trace to view the lineage.

## Next steps

* [Monitor your MCP servers](monitor-your-mcp-servers.md) — View aggregate metrics for MCP Proxy traffic.
* [Monitor AI Gateway usage from employee systems](monitor-ai-gateway-from-devices.md) — View per-device AI traffic from the Edge Management dashboard.
