# Span Attribute Redaction Concepts and Rule Syntax

## Overview

Span attribute redaction masks sensitive OpenTelemetry span metadata before traces leave the Gateway JVM via OTLP export. The feature protects authorization headers, API keys, tokens, consumer identifiers, query parameters, and other sensitive span attributes by applying configurable masking rules at the Gateway level. Redaction occurs in-process before spans are exported to OpenTelemetry collectors or tracing backends, ensuring sensitive observability data never leaves the Gateway unmasked.

## Key Concepts

### Redaction Rules

A redaction rule matches span attribute keys using glob patterns, short names, or Java regex, and applies a masking strategy to the attribute value. Rules are evaluated in order (global rules first, then API-specific rules), and the first matching rule determines the replacement. Each rule consists of three components:

| Component | Description | Example |
|:----------|:------------|:--------|
| Attribute Name Pattern (required) | Glob, short name, or `regex:`-prefixed Java regex matching the span attribute key | `http.request.header.authorization` |
| Masking Strategy (optional) | FULL (replace entire value) or PARTIAL (keep prefix/suffix visible). Defaults to FULL with `[REDACTED]` | FULL → `[REDACTED]`, PARTIAL → `ab****90` |
| Value Pattern (optional) | Java regex (partial match). Rule fires only when the attribute value matches | `^Bearer ` |

### Masking Strategies

**FULL** replaces the entire attribute value with a replacement string (default `[REDACTED]`). **PARTIAL** preserves a visible prefix and/or suffix and masks the middle section with a single mask character (default `*`). PARTIAL masking requires **Visible Prefix (chars)** and **Visible Suffix (chars)** configuration (both default to `0`). When `prefixLength + suffixLength >= value.length`, the entire value is replaced with the mask character repeated `value.length` times.

| Strategy | Configuration | Example Input | Example Output |
|:---------|:--------------|:--------------|:---------------|
| FULL | `replacement: "[REDACTED]"` | `Bearer abc123` | `[REDACTED]` |
| PARTIAL | `prefixLength: 2, suffixLength: 4, replacement: "*"` | `abcdef1234567890` | `ab****90` |

### Pattern Matching

Attribute name patterns support four syntaxes. **Short names** (no dots, no wildcards, no `regex:` prefix) match any namespace and are equivalent to `regex:(.*[._])?<pattern>$`. **Single-segment globs** (`*`) match one segment and do not cross `.` boundaries. **Multi-segment globs** (`**`) match any depth and cross `.` boundaries. **Exact regex** patterns are prefixed with `regex:` and use Java regex partial matching. Key pattern matching is case-insensitive; value pattern matching is case-sensitive.

| Pattern Type | Syntax | Matches | Does Not Match |
|:-------------|:-------|:--------|:---------------|
| Short name | `api-key` | `http.request.header.api-key` | — |
| Single glob | `http.request.header.*` | `http.request.header.authorization` | `http.request.header.x.custom` |
| Multi glob | `http.request.**` | `http.request.header.authorization` | — |
| Exact regex | `regex:enduser\.(id\|email)` | `enduser.id`, `enduser.email` | `enduser.name` |

### Rule Evaluation

Global rules configured in `gravitee.yml` are applied before API-specific rules. When multiple rules match the same attribute key, the first matching rule's replacement is used. Each span's attributes are evaluated independently. Non-string attributes (Long, Boolean, Double, arrays) are coerced to String when redacted, and the original typed key is removed.
