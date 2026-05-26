# Enable and Use OpenTelemetry Logs for APIs

## Create an OpeneTelemetry Logs Configuration

1. From the **Dashboard**, click **APIs**.
2. Select the API that you want to enable OpenTelemetry for.
3. From the API menu, click **Deployment**, and then click **Reporter Settings**.
4. Navigate to the **OpenTelemetry** section, and then turn on the **Enable OpenTelemetry tracing** toggle.
5. In the **You have unsaved changes** pop-up box, click **Save**.
6. In the **This API is out of sync.** pop-up box, click **Deploy API**.

    <figure><img src="../.gitbook/assets/apim-opentelemetry-logs-integration-step-08.png" alt="API deployment reporter settings showing logging mode, logging phase, and content data configuration options"><figcaption></figcaption></figure>

{% hint style="info" %}
The **OpenTelemetry Logs** toggle is disabled when Analytics is disabled or when Tracing is disabled. Disabling Tracing disables OTel Logs.
{% endhint %}

When you enable OpenTelemetry, log records are exported asynchronously to avoid added latency on the request path. Enabling OpenTelemetry Logs alongside existing logging results in both reporters receiving the same log record.

## View Correlated Logs in Grafana

1. In Grafana, open **Explore**, and then click **Tempo**.
2. Search for traces from your API.

    <figure><img src="../.gitbook/assets/apim-opentelemetry-logs-integration-step-06.png" alt="Grafana Tempo search interface showing trace query filters and results table"><figcaption></figcaption></figure>

3. Click a trace.

    <figure><img src="../.gitbook/assets/apim-opentelemetry-logs-integration-step-05.png" alt="Grafana Tempo trace view showing service spans and request flow with log correlation button"><figcaption></figcaption></figure>

4. View the detailed spans of your API.

    <figure><img src="../.gitbook/assets/apim-opentelemetry-logs-integration-step-04.png" alt="Grafana trace span detail showing request phase attributes and log correlation link"><figcaption></figcaption></figure>

5. To view the correlated log lines in your log backend, click **Logs for this span**.

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

Here is an example configuration:

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
- OTel Logs are supported for v4 HTTP/Proxy and v4 Message APIs only.
- Span attribute redaction is supported for v4 HTTP/Proxy and v4 TCP APIs only.
- The OTel Logs toggle is only available when OpenTelemetry Tracing is already enabled on the API.
- Disabling Tracing automatically disables OTel Logs.
- When `analytics.enabled = false`, `otelLogs.enabled` is ignored and no logs are emitted.
- When `tracing.enabled = false`, `otelLogs.enabled` is disabled in the UI and forced to `false`.
- Log records are always exported over HTTP/protobuf (not gRPC). The `logsEndpoint` must be an HTTP URL (e.g., `http://localhost:3100/otlp/v1/logs`). The SDK does not append the signal path automatically; the full URL including `/v1/logs` must be provided. OTel Logs are always exported over HTTP/protobuf (not gRPC) because Loki does not implement the gRPC LogsService.
- Log records are only emitted when `traceId` is set on the log entry. When OTel Logs is disabled for an API, regular logging may still produce log objects but `traceId` will be `null` and no OTLP log record is emitted.
- Header capture is not widened by OTel Logs. When `otelLogs.enabled = true`, only payload capture is automatically enabled for all four directions. Header capture remains controlled by the Elasticsearch logging configuration (`logging.content.headers`).
- Trace ID and span ID are empty strings when tracing is disabled. When `tracing.enabled = false` or no span is active, trace ID and span ID return `""` (empty string).
- Span ID reliability in multiplexed flows: The returned IDs are only guaranteed to reflect the logically active span when spans on the same context are strictly LIFO-nested (e.g., classic request/response HTTP flows). In reactors that multiplex concurrent spans onto a single context — for example the Kafka native reactor, where many in-flight protocol requests share one duplicated context, or any flow that creates spans inside asynchronous operators — the slot can hold a sibling span, be restored to `null` by an out-of-order end, or otherwise not match the span the caller has in mind. In non-LIFO flows, `Tracer#spanId(Context)` reads from a single per-context slot that behaves like a stack. In reactors that multiplex concurrent spans onto one Vert.x context (e.g., Kafka native reactor, or flows creating spans inside `doOnSubscribe` / `Completable.defer`), the slot may hold a sibling span or be restored to `null` by an out-of-order end. In those cases, resolve the specific `Span` and use `Span#spanId()` instead.
- Redaction applies to span attributes, event attributes, and resource attributes only. Span names, event names, and log record bodies are not redacted.
- PARTIAL masking with `prefixLength + suffixLength >= value.length()` returns the original value unchanged.
- Redaction rules are evaluated in order; the first matching rule wins. Rule ordering matters when multiple patterns could match the same attribute.
- Duplicate `attributeNamePattern` within the same API is rejected by the UI with the error: "A rule with this pattern already exists." The backend does not enforce uniqueness; duplicate patterns in YAML or merged configs will result in the first rule firing.
- APIs with `definitionContext.origin === 'KUBERNETES'` display redaction rules in read-only mode. Add, edit, and delete actions are hidden.
- The **Mask Character** field for PARTIAL masking must be exactly one character. Values longer than one character are rejected with the error: `PARTIAL mask character must be exactly one character, got: "<value>"`.
- `prefixLength` and `suffixLength` must be non-negative integers. Negative values are rejected with the error: `prefixLength must be >= 0, got: <value>` or `suffixLength must be >= 0, got: <value>`.
- If OTel is disabled globally on the gateway, the feature has zero overhead.

{% hint style="info" %}
No specific guidance on how to resolve Span in non-LIFO flows or which reactor patterns are affected beyond Kafka native reactor and doOnSubscribe/Completable.defer examples.
{% endhint %}

### Related Changes

#### UI Behavior

* The **OTel Logs** toggle is disabled when **Analytics** or **Tracing** is disabled. When **Tracing** is toggled off, **OTel Logs** is unchecked and disabled. When **Tracing** is toggled back on, **OTel Logs** is re-enabled.
* The redaction rules table displays an empty state message when no rules are configured: "No redaction rules — span attributes are exported as-is."
* A banner at the top of the table informs users: "Global redaction rules are always applied first. Rules defined here are API-specific and are appended after them."
* The masking display pipe shows FULL rules as `FULL → "[replacement]"` and PARTIAL rules as `PARTIAL prefix N · suffix M · char "C"`.
* The redaction rule dialog provides a live preview for PARTIAL masking, showing the masking applied to the sample string `ABCDEFGHIJ1234`.

#### API Changes

* The `Tracer` interface now exposes `traceId(Context)` and `spanId(Context)` methods, returning W3C TraceContext IDs (32 hex chars for traceId, 16 hex chars for spanId) or `""` if no span is active.
* The `Span` interface now exposes `traceId()` and `spanId()` methods.
* The `TracerFactory.createTracer` method signature now includes a `RedactionConfig` parameter. Existing implementations continue to work via a default method. Passing `RedactionConfig.EMPTY` or `null` disables API-specific redaction but still applies YAML-configured rules.

#### Dependency Updates

This release upgrades the following dependencies:

* `gravitee-node` to `9.0.0-alpha.10`
* `gravitee-reporter-api` to `2.3.0`
* Adds `io.opentelemetry:opentelemetry-exporter-otlp` for OTLP HTTP log export

