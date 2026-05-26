# OpenTelemetry Span Attribute Redaction and Log Correlation Overview

## Overview

OpenTelemetry Span Attribute Redaction masks sensitive span metadata before export to OTLP collectors or tracing backends. Log Correlation emits request and response payloads as OpenTelemetry log records linked to the active trace, enabling log-to-trace navigation in Grafana and other OTel-compatible backends. Both features protect sensitive observability data (authorization headers, API keys, tokens, consumer identifiers, PII) by performing masking fully in-process inside the Gateway before export.

## Key Concepts

### Span Attribute Redaction

Span attribute redaction applies configurable masking rules to span attributes, event attributes, and resource attributes before OTLP export. Rules are defined using glob-style patterns (e.g., `http.request.header.*`, `gravitee.**`) and support two masking strategies: **FULL** (replaces the entire value with a replacement string) and **PARTIAL** (preserves a configurable prefix and suffix, masking the middle section with a single character). Global rules from `gravitee.yml` are applied first; API-specific rules configured in the Console are appended after them. If no rule matches, spans pass through unchanged with zero overhead.

| Masking Type | Behavior | Example |
|:-------------|:---------|:--------|
| **FULL** | Replaces entire value with replacement text (default `[REDACTED]`) | `Authorization: Bearer abc123` → `[REDACTED]` |
| **PARTIAL** | Preserves prefix/suffix, masks middle with single character (default `*`) | `abcdef1234567890` → `ab******90` |

### Log Correlation

Log Correlation emits request and response payloads as OpenTelemetry log records correlated to the active trace. Each log record includes `traceId` and `spanId` fields, enabling log-to-trace linking in Grafana and other OTel-compatible backends. Log records are sent to the OTLP HTTP endpoint configured in `services.opentelemetry.exporter.logsEndpoint`. Capture is subject to the sampling strategy configured in Analytics settings. Log records are only emitted when `analytics.otelLogs.enabled` is `true` and `traceId` is set on the log entry.

### Pattern Matching

Attribute name patterns support glob-style wildcards and regex. Short names (no dots) automatically match any namespace. `*` matches one segment (e.g., `http.request.header.*` matches `http.request.header.authorization`). `**` matches any depth (e.g., `gravitee.**` matches `gravitee.consumer.id` and `gravitee.api.plan.name`). Prefix with `regex:` for exact regex matching (e.g., `regex:^shortname$` matches the literal short name only). Value patterns are Java regex (partial match) and filter rule application: the rule only fires when the attribute value matches the pattern.

## Prerequisites

- Gravitee API Management 4.12.0 or later
- OpenTelemetry tracing enabled (`services.tracing.enabled: true`, `services.tracing.type: opentelemetry`)
- OTLP exporter endpoint configured (`services.tracing.otel.endpoint`)
- For Log Correlation: OTLP HTTP log receiver (e.g., Loki) configured at `services.opentelemetry.exporter.logsEndpoint`
- v4 HTTP/Proxy or v4 TCP API (Span Attribute Redaction)
- v4 HTTP/Proxy API (Log Correlation)

## Restrictions

- **API type support**: Span Attribute Redaction is supported for v4 HTTP/Proxy and v4 TCP APIs. Log Correlation is supported for v4 HTTP/Proxy APIs only. v2 APIs, v4 Message APIs, Federated APIs, and Native Kafka APIs are not supported.
- **Log emission conditions**: Log records are only emitted when `analytics.otelLogs.enabled` is `true` **and** `traceId` is set on the log entry.
- **Redaction scope**: Redaction applies to span attributes and event attributes. Span names, trace IDs, and span IDs are not redacted.
- **Resource attribute redaction timing**: Resource attributes (service.instance.id, hostname, ip) are redacted once at tracer creation time. Changes to redaction rules require a tracer restart (API redeployment) to take effect on resource attributes.
- **Short name matching**: Short names (no dots) are automatically expanded to match any namespace. To match a literal short name, use `regex:^shortname$`.
- **PARTIAL masking edge case**: If `prefixLength + suffixLength >= value.length()`, the original value is preserved (nothing to mask). This is by design to avoid producing an empty or invalid masked value.
- **Tracer context slot limitations**: `Tracer#spanId` and `Tracer#traceId` read from a single per-context slot and are only guaranteed to reflect the logically active span when spans on the same Vert.x context are strictly LIFO-nested. In multiplexed flows (e.g., Kafka native reactor, reactive deferred spans), the slot may hold a sibling span or be restored to `null` by an out-of-order end. In those cases, resolve the specific `Span` and use `Span#spanId()` / `Span#traceId()` instead.
- **UI validation rules**: The Console UI enforces duplicate pattern validation (no two rules can have the same `attributeNamePattern`), non-negative `prefixLength` and `suffixLength` for PARTIAL rules, and single-character `maskChar` constraints.
- **Kubernetes origin read-only mode**: When `definitionContext.origin === 'KUBERNETES'`, all redaction rule controls are disabled in the Console UI.
- **Mask character constraints**: The PARTIAL masking strategy requires a single-character `maskChar`. If `maskChar` is null or empty, it defaults to `*`. If `maskChar` is longer than one character, the Gateway throws an `IllegalArgumentException`.
