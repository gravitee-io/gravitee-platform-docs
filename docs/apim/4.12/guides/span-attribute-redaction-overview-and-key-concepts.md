# Span Attribute Redaction Overview and Key Concepts

## Overview

Span attribute redaction masks sensitive OpenTelemetry span metadata before traces leave the Gateway JVM via OTLP export. Administrators configure pattern-based rules to redact authorization headers, API keys, tokens, consumer identifiers, query parameters, and other sensitive attributes. Redaction occurs in-process inside the Gateway before spans reach OpenTelemetry collectors or tracing backends.

## Key Concepts

### Redaction Rules

A redaction rule matches span attribute keys using glob patterns, short names, or regular expressions, then applies a masking strategy (FULL or PARTIAL) to the attribute value. Rules are evaluated in order; the first matching rule wins. Platform-level rules (configured in `gravitee.yml`) are always applied first, followed by API-specific rules defined in the API analytics configuration.

| Component | Description |
|:----------|:------------|
| **Attribute Name Pattern** | Glob pattern, short name (no dots), or `regex:`-prefixed Java regex matching the span attribute key. Short names match any namespace (e.g., `api-key` matches `http.request.header.api-key`). Single wildcard `*` matches one segment; double wildcard `**` matches any depth. |
| **Masking Strategy** | FULL replaces the entire value with replacement text (default `[REDACTED]`). PARTIAL preserves a visible prefix and/or suffix and masks the middle section with a single mask character (default `*`). |
| **Value Pattern** | Optional Java regex (partial match). Rule only fires when the attribute value matches this pattern. Use `^` and `$` for full-string match. |
| **Default Replacement** | Fallback replacement text for FULL masking rules with no per-rule replacement. Defaults to `[REDACTED]`. |

### Pattern Matching

| Pattern Type | Syntax | Behavior | Example |
|:-------------|:-------|:---------|:--------|
| Short name | No dots, no wildcards | Matches any namespace | `api-key` matches `http.request.header.api-key` |
| Single wildcard | `*` | Matches one segment (does not cross dots) | `http.request.header.*` matches `authorization` but not `x.custom` |
| Double wildcard | `**` | Matches any depth | `http.request.**` matches `header.authorization` |
| Regex | `regex:` prefix | Exact Java regex | `regex:enduser\.(id\|email)` |

Attribute name patterns are case-insensitive. Value patterns are case-sensitive.

### Masking Strategies

**FULL Masking** replaces the entire attribute value with replacement text. Example: `Authorization: Bearer abc123` becomes `[REDACTED]`. The replacement text is taken from the rule's `replacement` property, or the global `defaultReplacement`, or `[REDACTED]` if neither is set.

**PARTIAL Masking** preserves a visible prefix and/or suffix and masks the middle section. Example: `abcdef1234567890` with `prefixLength: 2`, `suffixLength: 2`, and `replacement: *` becomes `ab**********90`. The `replacement` property must be exactly one character.

### Type coercion

When a non-string attribute (Long, Boolean, Double, StringArray) is redacted, it is coerced to a String. The original typed key is removed from the span.

| Original Type | Redacted Type |
|:--------------|:--------------|
| String | String |
| Long | String |
| Boolean | String |
| Double | String |
| StringArray | String |

## Prerequisites

- Gravitee API Management 4.12.0 or later
- OpenTelemetry tracing enabled (`services.tracing.enabled: true`, `services.tracing.type: opentelemetry`)
- v4 HTTP/Proxy or v4 TCP API
- [Verbose tracing](../analyze-and-monitor-apis/opentelemetry.md#viewing-tracing-data) enabled (`tracing.verbose: true`) for API-level configuration


<figure><img src="../../.gitbook/assets/apim-span-attribute-redaction-for-opentelemetry-tracing-step-01.png" alt="API Deployment page showing Reporter Settings tab with OpenTelemetry tracing enabled"><figcaption></figcaption></figure>
