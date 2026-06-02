# Span Attribute Redaction Restrictions and Implementation Notes

## Restrictions

Span attribute redaction is available only for v4 HTTP/Proxy and v4 TCP APIs. Verbose tracing must be enabled to capture span attributes for redaction.

Short name patterns (no dots) are expanded to `regex:(.*[._])?<pattern>$`. Use explicit `regex:` prefix for custom anchoring. Value pattern matching uses Java regex partial match (`Pattern.find()`) and is case-sensitive.

Non-string attributes (Long, Boolean, Double, arrays) are coerced to String when redacted, and the original typed key is removed. Resource attributes (e.g., `service.instance.id`, `hostname`) are redacted once at tracer creation time, not per-span. Event attributes are redacted using the same rules as span attributes — no separate configuration.

Key patterns are case-insensitive and value patterns are case-sensitive. When **Visible Prefix (chars)** + **Visible Suffix (chars)** >= value.length, the entire value is replaced with the mask character repeated value.length times. PARTIAL masking strategy enforces single-character `maskChar` — multi-character strings throw `IllegalArgumentException` at construction time.

Redaction rules are read-only in the UI for APIs with `definitionContext.origin === 'KUBERNETES'`. Duplicate attribute name patterns within the same API are rejected with the error "A rule with this pattern already exists." Invalid regex key patterns or value patterns throw `IllegalArgumentException` at construction time. Negative **Visible Prefix (chars)** or **Visible Suffix (chars)** values throw `IllegalArgumentException` at construction time.

## Related Changes

The Console UI adds a new **API Redaction Rules** component under Reporter Settings, visible only when tracing and verbose tracing are both enabled. The component includes a table displaying rule index, attribute pattern, masking type with detail text (FULL displays `→ "<replacement>"`; PARTIAL displays `prefix <N> · suffix <N> · char "<char>"`), value filter, and edit/delete actions. A new redaction rule dialog supports adding and editing rules with live preview for PARTIAL masking.

The Management API v2 schema is extended with `TracingRedactionConfig`, `TracingRedactionRule`, and `TracingMaskingStrategy` definitions under the `Tracing` object. The API definition model adds `TracingRedactionConfig`, `TracingRedactionRule`, `TracingMaskingStrategy`, and `MaskingType` classes to `gravitee-apim-definition-model`.

The Gateway integrates a new `RedactSpanExporter` that wraps the configured OpenTelemetry exporter and applies redaction rules before span export. Global redaction rules from `gravitee.yml` are merged with API-specific rules at tracer creation time, with global rules applied first.
