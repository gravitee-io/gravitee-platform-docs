# OpenTelemetry Redaction and Logging Restrictions and Limitations

## Restrictions

- Redaction applies only to span attributes, event attributes, and resource attributes. Span names, event names, and link attributes are not redacted.
- Resource attributes are redacted once at tracer creation time. Changes to redaction rules after tracer initialization do not affect already-created tracers.
- PARTIAL masking with `prefixLength + suffixLength >= value.length()` returns the original value unchanged.
- `Tracer.spanId(Context)` and `Tracer.traceId(Context)` are unreliable in non-LIFO span nesting scenarios (e.g., Kafka native reactor, reactive deferred flows). Use `Span.spanId()` / `Span.traceId()` when the specific span is known.
- OTel Logs are always exported over HTTP/protobuf, not gRPC. Loki does not implement the gRPC LogsService.
- Log records are only emitted when `traceId` is set on the log entry. When `otelLogs.enabled = false`, regular Elasticsearch logging may still produce log objects but `traceId` will be null and no OTel log record is emitted.
- Redaction rules are evaluated in order; first match wins. Rule ordering matters when multiple patterns could match the same attribute.
- Short attribute name patterns (no dots, no wildcards) automatically match any namespace. E.g., `api-key` matches `http.request.header.api-key`, `custom.api-key`, etc.
- Regex patterns must be prefixed with `regex:` to be interpreted as exact regex. Otherwise, the pattern is treated as a glob.
- UI duplicate pattern validation is case-sensitive. Backend pattern matching is case-insensitive.
- PARTIAL mask character must be exactly one character. `prefixLength` and `suffixLength` must be >= 0.
- OTel Logs toggle is disabled when `analytics.enabled = false` or `analytics.tracing.enabled = false`.
- API Redaction Rules section is hidden when `definitionContext.origin === 'KUBERNETES'` (read-only mode).

## Related Changes

### Console UI

The Console UI adds an **API Redaction Rules** section to Reporter Settings for v4 HTTP/Proxy and v4 TCP APIs. The section displays a table of redaction rules with columns for pattern, masking type, value filter, and actions. A redaction rule dialog supports adding and editing rules with live preview for PARTIAL masking and duplicate pattern validation.

The **OTel Logs** toggle appears in the OpenTelemetry Tracing card for both Proxy and Message APIs, enabling payload capture as OpenTelemetry log records correlated to the active trace. The toggle is disabled when Analytics or Tracing is disabled.

### API Changes

The `TracerFactory` API adds a new `createTracer` overload accepting a `RedactionConfig` parameter, with a default implementation for backward compatibility. The `Span` API adds `spanId()` and `traceId()` methods returning W3C TraceContext identifiers. A new `Logger` API and `LoggerFactory` enable programmatic emission of OpenTelemetry log records with automatic attribute type mapping.

### Dependency Updates

| Artifact | Version |
|:---------|:--------|
| `gravitee-node` | `9.0.0-alpha.10` |
| `gravitee-reporter-api` | `2.3.0` |
| `gravitee-gateway-api` | `5.0.0-beta.3` |
| `io.opentelemetry:opentelemetry-exporter-otlp` | (added) |
