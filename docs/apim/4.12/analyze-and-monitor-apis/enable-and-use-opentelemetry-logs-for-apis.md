# Enable and Use OpenTelemetry Logs for APIs

## Creating an OTel Logs Configuration

1. Open the API in the Gravitee API Console and navigate to **Runtime Logs** settings under **Analytics** / **Reporter Settings**.
2. Ensure **OpenTelemetry Tracing** is enabled for the API.
3. Toggle **OTel Logs** on.

    <figure><img src="../.gitbook/assets/apim-opentelemetry-logs-integration-step-08.png" alt="API deployment reporter settings showing logging mode, logging phase, and content data configuration options"><figcaption></figcaption></figure>

4. Save and deploy the API.

{% hint style="info" %}
The **OTel Logs** toggle is disabled when Analytics is disabled or when Tracing is disabled. Disabling Tracing automatically disables OTel Logs.
{% endhint %}

When enabled, log records are exported asynchronously so there is no added latency on the request path. Enabling OTel Logs alongside existing logging (Elasticsearch, file) will result in both reporters receiving the same log record.

## Viewing Correlated Logs in Grafana

1. In Grafana, open **Explore** → **Tempo** and search for traces from your API.

    <figure><img src="../.gitbook/assets/apim-opentelemetry-logs-integration-step-06.png" alt="Grafana Tempo search interface showing trace query filters and results table"><figcaption></figcaption></figure>

2. Click on a trace to open it.

    <figure><img src="../.gitbook/assets/apim-opentelemetry-logs-integration-step-05.png" alt="Grafana Tempo trace view showing service spans and request flow with log correlation button"><figcaption></figcaption></figure>

3. View the detailed spans of your API (request/response phases, policy executions).

    <figure><img src="../.gitbook/assets/apim-opentelemetry-logs-integration-step-04.png" alt="Grafana trace span detail showing request phase attributes and log correlation link"><figcaption></figcaption></figure>

4. Click **Logs for this span** to navigate to the correlated log lines in your log backend.

    A pre-filtered log list appears with the detailed payload of all capture points.

    <figure><img src="../.gitbook/assets/apim-opentelemetry-logs-integration-step-03.png" alt="Grafana Loki logs view displaying JSON request and response payloads with trace correlation headers"><figcaption></figcaption></figure>

    <figure><img src="../.gitbook/assets/apim-opentelemetry-logs-integration-step-07.png" alt="Grafana Loki query builder showing LogQL query for trace ID correlation with log results"><figcaption></figcaption></figure>

## End-User Configuration

### Analytics Configuration (V4 APIs)

| Property | Description | Example |
|:---------|:------------|:--------|
| `analytics.enabled` | Enable analytics for the API. When `false`, `otelLogs.enabled` is ignored and no logs are emitted. | `true` |
| `analytics.tracing.enabled` | Enable OpenTelemetry tracing for the API. When `false`, `otelLogs.enabled` is disabled in the UI and forced to `false`. | `true` |
| `analytics.otelLogs.enabled` | Emit request and response payloads as OpenTelemetry log records correlated to the active trace. All requests generate log records when enabled; trace and span IDs are only populated for requests sampled by the tracer. For Message APIs, payload capture is also subject to `analytics.logging.messageSampling`. | `false` |

Example configuration:

```yaml
analytics:
  enabled: true
  tracing:
    enabled: true
  otelLogs:
    enabled: false
```

## Restrictions

- OTel Logs is disabled by default and must be explicitly enabled per API.
- The OTel Logs toggle is only available when OpenTelemetry Tracing is already enabled on the API.
- Disabling Tracing automatically disables OTel Logs.
- When `analytics.enabled = false`, `otelLogs.enabled` is ignored and no logs are emitted.
- When `tracing.enabled = false`, `otelLogs.enabled` is disabled in the UI and forced to `false`.
- Log records are always exported over HTTP/protobuf (not gRPC). The `logsEndpoint` must be an HTTP URL (e.g., `http://localhost:3100/otlp/v1/logs`). The SDK does not append the signal path automatically; the full URL including `/v1/logs` must be provided.
- Header capture is not widened by OTel Logs. When `otelLogs.enabled = true`, only payload capture is automatically enabled for all four directions. Header capture remains controlled by the Elasticsearch logging configuration (`logging.content.headers`).
- Trace ID and span ID are empty strings when tracing is disabled. When `tracing.enabled = false` or no span is active, trace ID and span ID return `""` (empty string).
- Span ID reliability in multiplexed flows: The returned IDs are only guaranteed to reflect the logically active span when spans on the same context are strictly LIFO-nested (e.g., classic request/response HTTP flows). In reactors that multiplex concurrent spans onto a single context — for example the Kafka native reactor, where many in-flight protocol requests share one duplicated context, or any flow that creates spans inside asynchronous operators — the slot can hold a sibling span, be restored to `null` by an out-of-order end, or otherwise not match the span the caller has in mind.
- If OTel is disabled globally on the gateway, the feature has zero overhead.

## Related Changes

The `gravitee-reporter-api` dependency is upgraded to `2.3.0` to add trace ID and span ID fields to Request, Response, and MessageLog. The `gravitee-node` dependency is upgraded to `9.0.0-alpha.10` to add the Logger API and OpenTelemetry log emission. The Console UI adds the OTel Logs toggle in the Reporter Settings for both Message APIs and Proxy APIs. The toggle is disabled when Analytics is disabled or when Tracing is disabled. When Tracing is toggled off, OTel Logs is disabled and unchecked. When Tracing is toggled on, OTel Logs becomes available but remains off by default — users must enable it explicitly. The `createTracer` method now uses node-level identifiers (`node.id()`, `node.application()`, runtime major version) instead of API-level identifiers. API-level attributes are now passed as additional resource attributes in a map with keys `gravitee.api.id` and `gravitee.api.name`.
