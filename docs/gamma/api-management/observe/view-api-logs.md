---
hidden: false
noIndex: false
---

# View API logs
<!-- GAP-STRUCTURAL: Missing procedural content source -->
API logs provide a detailed record of every request processed by the API Gateway for a specific API proxy. Gamma exposes native log viewing and a **Trace Explorer** under the Observability section, giving you full request traces and span data to help you debug and analyze your API traffic.

## Access logs and traces

1. From the Gamma console sidebar, select **API Management**.
2. Navigate to the API detail page for your API proxy.
3. In the sidebar under **Monitoring**, select **Observability**.
4. Use the Observability navigation to switch between **Logs** and **Traces**.

## Log entry fields

Each trace log entry provides a comprehensive view of the request lifecycle, including:

| Field             | Description                                                      |
| ----------------- | ---------------------------------------------------------------- |
| **Timestamp**     | When the request was received (derived from root span start time). |
| **Method**        | HTTP method (GET, POST, PUT, DELETE, etc.).                      |
| **Path**          | The request path.                                                |
| **Status**        | HTTP response code. Trace-level status rolls up: if any span reports an error, the trace is marked as `error`. Otherwise, it falls back to the root span's status (`ok` or `unset`). |
| **Response time** | Time in nanoseconds/milliseconds from request receipt to response delivery. |
| **Span Count**    | The total number of spans involved in the trace.                 |
| **Plan**          | The security plan that authenticated the request.                |
| **Application**   | The application that made the request (if identified by a plan). |
| **Payloads**      | Full request and response body inspection (when configured).       |

## Search and filter

The Observability integration provides a robust set of native filters. You can filter your logs and traces by:

* **HTTP Method** — Filter by specific methods (e.g., `GET`, `POST`).
* **HTTP Status Code** — Filter by exact status code or a range of status codes.
* **HTTP Route** — Filter by request path.
* **Time Range** — Filter logs within a specific temporal window (e.g., last 24 hours, last 7 days).
* **Consumer Application** — Isolate traffic from a specific client.
* **Subscription Plan** — Isolate traffic secured by a specific API plan.

The logs view is strictly scoped to the specific API you are inspecting; cross-API log probing is securely blocked by design.

## Next steps

* [Monitor API usage](monitor-api-usage.md) — View aggregate metrics and dashboards for your API.
