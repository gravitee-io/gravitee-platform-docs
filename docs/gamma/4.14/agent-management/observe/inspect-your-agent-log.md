---
hidden: false
noIndex: false
description: Inspect the logs of individual agent calls through the AI Gateway. Open a log entry to read who called, what happened, and which decisions applied.
---

# Inspect your agent log

The logs record each call that passes through the AI Gateway to an LLM Proxy, an MCP Proxy, or an A2A Proxy. A log entry shows who made the call, what the gateway did with it, and how long it took. The list holds only the calls of proxies that you have permission to read.

## Open the logs

1. In the Gamma console, open **Agent Management**.
2. In the **Observability** section of the sidebar, select **Logs**.
3. Select a log entry to open its detail.

## Read a log entry

A log entry records the following:

* The proxy that handled the call, with its name and type.
* The time of the call, and the request ID, transaction ID, and trace ID that identify it.
* The caller, as a client identifier, an application, a plan, and a subscription.
* The HTTP method, the URI, the status, and the endpoint the gateway called. For an MCP request, it also records the MCP method.
* The gateway response time.
* The error and the warnings, when the call raised any.
* The authorization decision and the guardrail decision, when the call went through them.
* The custom metrics of the request.

The detail of an entry adds the gateway latency and the endpoint response time. It also holds the size of the request and of the response, and the client's address.

### Read the payloads

The detail holds four payloads: the request and response at the entrypoint, and the request and response at the endpoint. Each one records the method, the URI, the status, the headers, and the body.

### Read the authorization decision

The authorization decision records the following:

* The decision and its outcome, and whether it was enforced.
* The rules that matched, each with its name, version, and effect.
* The reasons for the decision.
* The subject, the action, and the resource the decision applied to.
* How long the decision took.

### Read the guardrail decision

The guardrail decision records the following:

* The guardrail, its revision, and the checkpoint at which it ran.
* The outcome and the verdict, and whether it was enforced.
* The steps of the sequence, in the order they ran. Each step shows the guardrail policy, its verdict, and its reason.
* The findings, each with its guardrail policy, rule, location, and effect.

## Follow a call into its trace

Each log entry carries the trace ID of its call. To read the spans of that call, open the proxy's trace in the Trace Explorer. See [Trace an agent request and view its lineage](trace-an-agent-request.md).

## Next steps

* [Trace an agent request and view its lineage](trace-an-agent-request.md). Read the spans of a single call in the Trace Explorer.
* [Configure OpenTelemetry tracing and logs](../../platform-management/configure-opentelemetry-tracing-and-logs.md). Configure the pipeline that feeds the Trace Explorer.
* [Monitor your MCP servers](monitor-your-mcp-servers.md). View aggregate metrics for MCP Proxy traffic.
* [Monitor AI Gateway usage from employee systems](monitor-ai-gateway-from-devices.md). View per-device AI traffic from the Edge Management dashboard.
