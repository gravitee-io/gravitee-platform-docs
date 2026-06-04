---
description: Span Attribute Redaction masks sensitive metadata in OpenTelemetry traces before the traces leave the API Gateway.
---

# Span Attribute Redaction Overview

## Overview

Span Attribute Redaction masks sensitive metadata in OpenTelemetry traces before they leave the API Gateway. You configure pattern-based rules to replace or partially obscure span attributes such as authorization headers, API keys, consumer identifiers, and query parameters. Redaction occurs in-process at the API Gateway before OTLP export. This ensures that sensitive observability data never reaches external collectors or tracing backends.

## Key Concepts

### Redaction Rules

A redaction rule matches span attribute keys using glob patterns, short names, or regular expressions, and applies a masking strategy when the key, and optionally the value, matches. The system evaluates rules in order. Global rules defined in `gravitee.yml` are applied first, followed by API-specific rules configured in the **Management Console**. The first matching rule wins.

The following table describes the components of a redaction rule:

| Component | Description |
|:----------|:------------|
| **Attribute Name Pattern** | Glob pattern (`*`, `**`), short name with no dots, or `regex:`-prefixed Java regex matching the span attribute key. Matching is case-insensitive. |
| **Masking Strategy** | `FULL` to replace the entire value or `PARTIAL` to keep the visible prefix or suffix. |
| **Value Pattern** | Optional Java regex using a partial match. This is case-sensitive. The rule fires only when the attribute value matches. |

### Masking Strategies

**FULL** replaces the entire attribute value with a replacement string. The default replacement is `[REDACTED]`. **PARTIAL** preserves a configurable number of leading and trailing characters, masking the middle section with a single mask character. The default mask character is `*`.

The following table describes the configuration and behavior of masking strategies:

| Strategy | Configuration | Example |
|:---------|:--------------|:--------|
| FULL | `replacement`. The default replacement is `[REDACTED]`. | `Bearer abc123` changes to `[REDACTED]`. |
| PARTIAL | **Prefix Length**, **Suffix Length**, and `replacement`. The default mask character is `*`. | `abcdef1234567890` changes to `ab******90` with a prefix length of 2 and a suffix length of 2. |

### Pattern Matching

Key patterns are case-insensitive. Value patterns are case-sensitive and use partial matching. Operators must use `^...$` anchors for full-string matching.

The following table describes the available pattern types:

| Pattern Type | Syntax | Behavior | Example |
|:-------------|:-------|:---------|:--------|
| Short name | No dots, no wildcards, and no `regex:` prefix. | Matches any namespace. This is equivalent to `regex:(.*[._])?<pattern>$`. | `api-key` matches `http.request.header.api-key`. |
| Glob with single `*` | `*` | Matches one segment. This pattern does not cross dot boundaries. | `http.request.header.*` matches `http.request.header.authorization`. |
| Glob with double `**` | `**` | Matches any depth. This pattern crosses dot boundaries. | `http.request.**` matches `http.request.header.authorization`. |
| Regex | `regex:<pattern>` | Exact Java regex using a partial match. | `regex:enduser\.(id\|email)` matches `enduser.id` or `enduser.email`. |

## Prerequisites

To configure Span Attribute Redaction, complete the following steps:

1. Enable OpenTelemetry tracing for the API Gateway or API.
2. For API-specific rules, deploy a v4 HTTP proxy API or v4 TCP proxy API with tracing enabled.
3. For global rules, ensure access to the `gravitee.yml` configuration file.

<figure><img src="../../.gitbook/assets/apim-span-attribute-redaction-for-opentelemetry-tracing-step-01.png" alt="API deployment reporter settings showing OpenTelemetry enabled with verbose mode"><figcaption><p>API deployment reporter settings</p></figcaption></figure>