# Span Attribute Redaction Overview

## Overview

Span Attribute Redaction masks sensitive metadata in OpenTelemetry traces before they leave the Gateway. Administrators configure pattern-based rules to replace or partially obscure span attributes such as authorization headers, API keys, consumer identifiers, and query parameters. Redaction occurs in-process at the Gateway before OTLP export, ensuring that sensitive observability data never reaches external collectors or tracing backends.

## Key Concepts

### Redaction Rules

A redaction rule matches span attribute keys using glob patterns, short names, or regular expressions, and applies a masking strategy when the key (and optionally the value) matches. Rules are evaluated in order: global rules defined in `gravitee.yml` are applied first, followed by API-specific rules configured in the Console. The first matching rule wins.

| Component | Description |
|:----------|:------------|
| **Attribute Name Pattern** | Glob pattern (`*`, `**`), short name (no dots), or `regex:`-prefixed Java regex matching the span attribute key. Matching is case-insensitive. |
| **Masking Strategy** | `FULL` (replace entire value) or `PARTIAL` (keep visible prefix and/or suffix). |
| **Value Pattern** | Optional Java regex (partial match, case-sensitive). Rule fires only when the attribute value matches. |

### Masking Strategies

**FULL** replaces the entire attribute value with a replacement string (default `[REDACTED]`). **PARTIAL** preserves a configurable number of leading and trailing characters, masking the middle section with a single mask character (default `*`).

| Strategy | Configuration | Example |
|:---------|:--------------|:--------|
| FULL | `replacement` (default `[REDACTED]`) | `Bearer abc123` → `[REDACTED]` |
| PARTIAL | **Prefix Length**, **Suffix Length**, `replacement` (default `*`) | `abcdef1234567890` → `ab******90` (prefix 2, suffix 2) |

### Pattern Matching

| Pattern Type | Syntax | Behavior | Example |
|:-------------|:-------|:---------|:--------|
| Short name | No dots, no wildcards, no `regex:` prefix | Matches any namespace; equivalent to `regex:(.*[._])?<pattern>$` | `api-key` matches `http.request.header.api-key` |
| Glob (single `*`) | `*` | Matches one segment (does not cross `.` boundary) | `http.request.header.*` matches `http.request.header.authorization` |
| Glob (double `**`) | `**` | Matches any depth (crosses `.` boundaries) | `http.request.**` matches `http.request.header.authorization` |
| Regex | `regex:<pattern>` | Exact Java regex (partial match) | `regex:enduser\.(id\|email)` matches `enduser.id` or `enduser.email` |

Key patterns are case-insensitive. Value patterns are case-sensitive and use partial matching (operators must use `^…$` anchors for full-string matching).

## Prerequisites

Before configuring Span Attribute Redaction, complete the following steps:

* Enable OpenTelemetry tracing for the Gateway or API
* For API-specific rules: deploy a v4 HTTP/Proxy or v4 TCP API with tracing enabled
* For global rules: ensure access to `gravitee.yml` configuration

<figure><img src="../../.gitbook/assets/apim-span-attribute-redaction-for-opentelemetry-tracing-step-01.png" alt="API deployment reporter settings showing OpenTelemetry enabled with verbose mode"><figcaption></figcaption></figure>
