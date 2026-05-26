# OpenTelemetry Span Attribute Redaction and Log Correlation Overview

## Overview

OpenTelemetry Span Attribute Redaction masks sensitive span metadata before export to tracing backends. Log Correlation emits request and response payloads as OpenTelemetry log records linked to the active trace, enabling log-to-trace navigation in Grafana and other OTel-compatible backends. These features protect authorization headers, API keys, tokens, consumer identifiers, and PII data from leaving the Gateway JVM via OTLP export.

## Key Concepts

### Span Attribute Redaction

Redaction applies pattern-based masking rules to span attributes, event attributes, and resource attributes before OTLP export. Rules are evaluated in order; the first matching rule wins. YAML-configured rules (operator-level) are always applied first, followed by API-specific rules defined in the Console UI. If no rule matches, spans pass through unchanged with zero overhead. Redaction applies only to span attributes and resource attributes — span names, event names, and link attributes are not redacted.

### Masking Strategies

| Strategy | Behavior | Example |
|:---------|:---------|:--------|
| **FULL** | Replaces the entire value with a replacement string (default: `[REDACTED]`). | `Authorization: Bearer abc123` → `[REDACTED]` |
| **PARTIAL** | Preserves a configurable prefix and suffix, masking the middle section with a single character (default: `*`). | `abcdef1234567890` → `ab******90` (prefix=2, suffix=2) |

### Pattern Syntax

| Pattern | Interpretation | Example Match |
|:--------|:---------------|:--------------|
| Short name (no dots) | Matches any namespace: `(.*[._])?<name>$` (case-insensitive) | `api-key` matches `http.request.header.api-key` |
| `*` | Single segment wildcard | `http.request.header.*` matches `http.request.header.authorization` |
| `**` | Multi-segment wildcard (any depth) | `gravitee.**` matches `gravitee.consumer.id` |
| `regex:<pattern>` | Exact regex | `regex:^Bearer ` matches values starting with `Bearer ` |

### Log Correlation

When the **OTel Logs** toggle is enabled, the Gateway emits request and response payloads as OpenTelemetry log records. Each log record includes `traceId` and `spanId` fields that link it to the active span. Logs are exported to the configured `logsEndpoint` (default: `http://localhost:3100/otlp/v1/logs`) over HTTP/protobuf. Log correlation is subject to the sampling strategy configured in Reporter Settings.

### Redaction Rule Dialog

The Console UI provides a dialog for creating and editing redaction rules. Each rule specifies an **Attribute Name Pattern** (glob or regex), a **Masking Type** (FULL or PARTIAL), and an optional **Value Filter** (Java regex). PARTIAL rules include a live preview showing how the masking will appear (e.g., `ABCXXXXXXXX234`). The dialog validates for duplicate patterns and non-negative prefix/suffix lengths.
