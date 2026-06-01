# Span Attribute Redaction Restrictions and Related Changes

## Restrictions

- Redaction rules apply only to v4 HTTP/Proxy and v4 TCP APIs.
- Resource attributes (e.g., `service.instance.id`, `hostname`) are redacted once during tracer creation and baked into the `SdkTracerProvider`. They are not visible to per-span redaction inside the exporter.
- Non-string attributes (Long, Boolean, Double, StringArray) are coerced to String when redacted. The original typed key is removed from the span.
- Invalid regex patterns in **Attribute Name Pattern** or **Value Pattern** throw `IllegalArgumentException` at construction time, preventing tracer initialization.
- Short names (no dots, no wildcards) are automatically expanded to match any namespace. To disable this, use a full dotted pattern or prefix with `regex:`.
- Value patterns are case-sensitive (unlike key patterns). Use `(?i)` flag for case-insensitive value matching.
- PARTIAL masking strategy `replacement` must be exactly one character. Multi-character strings throw `IllegalArgumentException`.
- Negative **Prefix Length** or **Suffix Length** values throw `IllegalArgumentException`.
- The redaction rules UI is only visible when both `tracing.enabled` and `tracing.verbose` are true. Disabling either hides the section but preserves existing rules in the API definition.
- APIs with `definitionContext.origin === 'KUBERNETES'` are read-only in the UI. Redaction rules cannot be added, edited, or deleted through the console.
- Duplicate attribute name patterns are rejected by the UI with the error message: "A rule with this pattern already exists."

## Related Changes

The Management API v2 schema includes new `TracingRedactionConfig`, `TracingRedactionRule`, and `TracingMaskingStrategy` entities. The `Tracing` entity now includes an optional `redaction` property. The Console UI adds the `ApiRedactionRulesComponent` to the Reporter Settings page, visible when tracing is enabled and verbose. The component displays a table of redaction rules with add, edit, and delete actions, and a dialog for configuring rule properties. The `TracerFactory` interface includes a new default method accepting `RedactionConfig`, maintaining backward compatibility with existing implementations. APIs without a `redaction` block continue to work unchanged; empty `rules` arrays are equivalent to no redaction.
