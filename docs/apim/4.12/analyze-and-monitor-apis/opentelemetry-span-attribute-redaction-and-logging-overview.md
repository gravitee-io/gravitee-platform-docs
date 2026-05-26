# OpenTelemetry Span Attribute Redaction and Logging Overview

## Overview

OpenTelemetry Span Attribute Redaction and OTel Logs protect sensitive observability data before traces and logs leave the Gateway. Span Attribute Redaction masks span attributes (headers, metadata, consumer identifiers) using configurable glob or regex patterns. OTel Logs emit request and response payloads as OpenTelemetry log records correlated to the active trace, enabling log-to-trace linking in Grafana and other OTel-compatible backends. Both features apply to v4 HTTP/Proxy and v4 TCP APIs.

## Key Concepts

### Span Attribute Redaction

Span attribute redaction masks sensitive span metadata before OTLP export. Redaction occurs in-process inside the Gateway and applies to span attributes, event attributes, and resource attributes. Resource attributes are redacted once at tracer creation time. If no rule matches, spans pass through unchanged with zero overhead. Rules are evaluated in order. [Platform-level rules configured in `gravitee.yml`](configure-gateway-for-opentelemetry-logs.md#redaction-rules) are evaluated first, followed by API-level rules. The first matching rule wins.

### Masking Strategies

Two masking strategies are available:

* **FULL** replaces the entire attribute value with a replacement string (default `[REDACTED]`).
* **PARTIAL** preserves a configurable number of leading and trailing characters and masks the middle section with a single mask character (default `*`). When `prefixLength + suffixLength >= value.length()`, the original value is returned unchanged.

### Attribute Name Patterns

Patterns match span attribute keys using glob-style syntax. Short names (no dots) automatically match any namespace (e.g., `api-key` matches `http.request.header.api-key` and `custom.api-key`). `*` matches one segment, `**` matches any depth. Prefix with `regex:` for exact regex matching. Pattern matching is case-insensitive.

Examples:

* `http.request.header.*`
* `gravitee.**`
* `regex:^Authorization$`

### Value Filters

An optional value pattern (Java regex, partial match) restricts when a rule fires. The rule applies only when the attribute value matches the pattern.

Example: `valuePattern: "Bearer *"` applies the rule only to values starting with "Bearer ".

### OTel Logs

OTel Logs emit request and response payloads as OpenTelemetry log records correlated to the active trace. Log records include `traceId` and `spanId` attributes for log-to-trace linking. When `analytics.otelLogs.enabled = true`, all four directions (entrypoint/endpoint × request/response) are captured. When `analytics.otelLogs.enabled = false`, only directions enabled by the Elasticsearch logging configuration produce log records. OTel Logs are always exported over HTTP/protobuf to the configured `logsEndpoint`.
