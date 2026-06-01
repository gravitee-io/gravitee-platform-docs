# Span Attribute Redaction Runtime Behavior and Restrictions

## Restrictions

{% hint style="warning" %}
The following restrictions apply to span attribute redaction runtime behavior and configuration.
{% endhint %}

* Redaction rules are evaluated in order. The first matching rule wins — subsequent rules for the same attribute are ignored.
* Value patterns use `Pattern.find()` (partial match). Operators must use `^…$` anchors for full-string match.
* Short-name patterns (e.g., `api-key`) match the final segment after any separator (`.` or `_`). They do NOT partially match hyphenated names (e.g., `api-key` does not match `x-api-key`).
* Resource attributes (e.g., `service.instance.id`, `hostname`) are redacted once at tracer creation time and baked into the `SdkTracerProvider`. They are not visible to per-span redaction.
* When a non-string attribute is redacted, it is coerced to a string attribute. The original typed key is removed from the span.
* PARTIAL masking with `prefixLength + suffixLength >= value.length` results in the original value being preserved (no masking applied).
* Multi-character `replacement` strings for PARTIAL masking are rejected at construction time with `IllegalArgumentException`.
* Invalid regex key patterns (e.g., `regex:[unclosed-bracket`) throw `IllegalArgumentException` at redactor construction.
* Invalid regex value patterns (e.g., `[bad-value-regex`) throw `IllegalArgumentException` at redactor construction.
* `prefixLength` and `suffixLength` must be `>= 0`. Negative values throw validation errors.
* PARTIAL mask character must be exactly one character. Multi-character values throw validation errors.
* APIs with no `redaction` block in `analytics.tracing` continue to export spans without redaction.
* API-specific redaction rules are supported only for v4 HTTP/Proxy and v4 TCP APIs.
* The Span Attribute Redaction section is visible in the Console only when both `tracing.enabled` and `tracing.verbose` are `true`.
* When the API definition context origin is `KUBERNETES`, the Span Attribute Redaction section is read-only.

### Validation Error Conditions

| Condition | Error Type | Error Message |
|:----------|:-----------|:--------------|
| Invalid regex key pattern | `IllegalArgumentException` | Thrown at `SpanAttributeRedactor` construction |
| Invalid regex value pattern | `IllegalArgumentException` | Thrown at `SpanAttributeRedactor` construction |
| Negative `prefixLength` | Validation error | `prefixLength must be >= 0, got: {value}` |
| Negative `suffixLength` | Validation error | `suffixLength must be >= 0, got: {value}` |
| Multi-character PARTIAL `replacement` | `IllegalArgumentException` | `PARTIAL mask character must be exactly one character, got: "{value}"` |

## Related Changes

The Span Attribute Redaction section is added to the Reporter Settings → Proxy page for v4 HTTP/Proxy and v4 TCP APIs. The section displays a table of redaction rules with columns for rule index, attribute pattern, masking type and details, value filter, and actions. A banner informs users that global redaction rules are always applied first and API-specific rules are appended after them. When no rules are configured, an empty state message indicates that span attributes are exported as-is.

The redaction rule dialog provides fields for attribute name pattern, masking type, replacement text (FULL), visible prefix/suffix/mask character (PARTIAL), and value filter, with real-time preview for PARTIAL masking. Duplicate pattern validation prevents adding rules with identical attribute name patterns. The dialog displays hints for pattern syntax and validation constraints. Masking type badges use `gio-badge-neutral` for FULL and `gio-badge-accent` for PARTIAL.

The API definition model is extended with a `TracingRedactionConfig` object containing `defaultReplacement` and a list of `TracingRedactionRule` objects, each with `attributeNamePattern`, `maskingStrategy`, and optional `valuePattern`. The `TracingMaskingStrategy` object includes `type`, `replacement`, `prefixLength`, and `suffixLength` fields.
