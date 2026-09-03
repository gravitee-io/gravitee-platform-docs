---
hidden: false
noIndex: false
description: Trace every agent invocation through the AI Gateway with spans that record identity, inputs, latency, and cost. Learn how to read the agent log.
---

# Inspect your agent log

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
| **Cost**            | Token cost. Recorded for LLM traffic only.                                         |

## The lineage view

The Trace Explorer opens each trace recorded for a proxy as a span timeline or as a lineage graph of its spans. See [Trace an agent request and view its lineage](trace-an-agent-request.md).

## Access the agent log

1. From the Gamma console sidebar, select **Agent Management**.
2. In the **Observability** section of the sidebar, select **Logs**.
3. Select an entry to open its detail.

## Next steps

* [Monitor your MCP servers](monitor-your-mcp-servers.md) — View aggregate metrics for MCP Proxy traffic.
* [Monitor AI Gateway usage from employee systems](monitor-ai-gateway-from-devices.md) — View per-device AI traffic from the Edge Management dashboard.
