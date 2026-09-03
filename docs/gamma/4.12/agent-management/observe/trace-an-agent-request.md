---
hidden: false
noIndex: false
description: Open a trace for an LLM, MCP, or A2A Proxy in the Trace Explorer, read it as a span timeline or a lineage graph, and inspect a single span. Follow the steps to trace a request.
---

# Trace an agent request and view its lineage

The Trace Explorer lists the OpenTelemetry traces recorded for one proxy at a time. It opens each trace in two views. The **Timeline** lays the spans out as a waterfall, and the **Lineage** graph draws every span as a node linked to the span that called it. Selecting a span in either view shows its attributes, events, captured payloads, and the attribute changes a policy made.

## Prerequisites

* Tracing turned on for the proxy. On the proxy's **Reporter Settings** page, turn on **Trace enabled**. For an A2A Proxy, see [Configure logging and tracing](../build/configure-your-a2a-proxy/configure-logging-and-tracing.md).
* The Gateway exporting OpenTelemetry data and the Management API reading it back. Both are off by default: `services.opentelemetry.enabled` is `false` on the Gateway, and the `repositories.otel-traces.type` reader on the Management API is `none`. Until both are configured, the Trace Explorer stays empty.
* A started proxy. The API picker of the Trace Explorer lists started LLM, MCP, and A2A Proxies only.

## Open the traces of a proxy

1. From the Gamma console sidebar, select **Agent Management**.
2. In the **Observability** section of the sidebar, select **Tracing**.
3. In **Select an API…**, pick the proxy. Until you pick one, the table reads **Select an API above to view its traces.**
4. Optional: Change the time range with the time range picker.
5. Optional: Click **Add filter** to narrow the list by **HTTP method**, **HTTP status code**, or **HTTP route**. Each filter matches one exact value.

The table lists the traces of the proxy with their **Start Time**, **Status**, **Service**, **Operation**, and **Duration**. A trace's status is `error` when any of its spans is in error. Otherwise it's the status of the root span. When nothing matches, the table reads **No traces found**.

You can also open the Trace Explorer from a proxy. On the proxy's page, in the **Observability** group of the sidebar, select **Tracing**. The Trace Explorer opens in a new browser tab with that proxy selected.

## Read a trace

Select a row to open the trace beside the table. The header shows the trace's status, the operation of its root span, and its **Service**, **Duration**, **Spans**, **Started**, and **Trace ID**. Use **Previous trace** and **Next trace** to move through the traces of the current page, and **Full screen** to enlarge the view.

The **Trace view** tabs switch between two representations of the same spans:

* **Timeline**. A waterfall in which each span is a bar placed at its start offset within the trace and sized by its duration, indented under its parent span.
* **Lineage**. A graph with one node per span. A node shows the span's operation, its service, and its duration, and an edge runs from each span to the spans it started. A span in error and the edge that leads to it are marked as errors.

Selecting a bar or a node opens the span detail.

## Inspect a span

The **Span detail** panel opens below the trace view and has the following sections:

* **Overview**. The span's **Service**, **Operation**, **Span ID**, **Trace ID**, **Parent Span**, **Kind**, **Start**, and **Duration**.
* **Attributes**. The attributes the Gateway recorded on the span.
* **Policy Diff**. For a span that carries the events a policy recorded before and after it ran, a before-and-after table of the attributes the policy added, removed, or changed. The section says so when the policy changed nothing.
* **Events**. The events recorded on the span.
* **Payload Logs**. The request and response payloads captured for the span. They appear when the proxy's **OTel Logs** setting is on. The Management API also has to read OpenTelemetry log records.

Close the panel to return to the trace.

## What a trace covers

Every search and every trace in the Trace Explorer is scoped to the proxy you selected. The spans that other proxies recorded for the same request aren't shown. A request that passes through several proxies appears as one trace per proxy, and the lineage graph draws the spans of that proxy only.

## Next steps

* [Inspect your agent log](inspect-your-agent-log.md): Read the log entry of a single invocation.
* [Configure logging and tracing](../build/configure-your-a2a-proxy/configure-logging-and-tracing.md): Turn on tracing, verbose span events, and payload log records for an A2A Proxy.
