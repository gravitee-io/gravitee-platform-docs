# Managing API-Specific Redaction Rules in the Console

## Creating API-Specific Redaction Rules

API-specific redaction rules are configured in the Console under **Reporter Settings → Proxy → Span Attribute Redaction**. This section is visible only when tracing is enabled and verbose mode is active. API-specific rules are appended after global rules and take precedence for matching attributes.

<figure><img src="../../.gitbook/assets/apim-span-attribute-redaction-for-opentelemetry-tracing-step-02.png" alt="Span attribute redaction section with empty rules table and add rule button"><figcaption></figcaption></figure>

1. Navigate to **Reporter Settings → Proxy → Span Attribute Redaction**.
2. Click **Add rule** to open the redaction rule dialog.
3. Enter an **Attribute Name Pattern** (e.g., `http.request.header.authorization`, `enduser.*`, `regex:payment\.(card|token)`).
4. Select a **Masking Type** (`FULL` to replace the entire value, or `PARTIAL` to keep prefix/suffix visible).
5. For FULL masking, optionally enter **Replacement Text** (leave blank to use the default `[REDACTED]`).
6. For PARTIAL masking, configure **Visible Prefix (chars)**, **Visible Suffix (chars)**, and **Mask Character** (single character, default `*`). A live preview displays the masking result.
7. Optionally enter a **Value Filter** (Java regex, partial match). The rule fires only when the attribute value matches this pattern.
8. Click **Add** to save the rule.

**Reference Table:**

| Field | Description | Example |
|:------|:------------|:--------|
| Attribute Name Pattern | Glob pattern, short name, or `regex:`-prefixed Java regex matching the span attribute key. Short names without dots match any namespace; `*` matches one segment; `**` matches any depth; prefix with `regex:` for exact regex. | `http.request.header.*` |
| Masking Type | `FULL` (replace entire value) or `PARTIAL` (keep prefix/suffix visible). | `FULL` |
| Replacement Text | For FULL: replacement text (default `[REDACTED]`). | `[REDACTED]` |
| Visible Prefix (chars) | PARTIAL only: number of leading characters to keep visible. | `2` |
| Visible Suffix (chars) | PARTIAL only: number of trailing characters to keep visible. | `4` |
| Mask Character | PARTIAL only: single character used for masking. | `*` |
| Value Filter | Optional Java regex (partial match). Rule fires only when the attribute value matches. | `Bearer .*` |

The Console displays existing rules in a table with columns for rule index, attribute pattern, masking strategy, value filter, and edit/delete actions. A banner notes that global redaction rules are always applied first, and API-specific rules are appended after them.

## Managing Redaction Rules

### Editing Rules

Click the **Edit** button in the rule table row to open the redaction rule dialog with pre-filled values. Modify the fields and click **Save** to update the rule.

### Deleting Rules

Click the **Delete** button in the rule table row to remove the rule. Changes take effect when the API configuration is saved and deployed.

### Rule Evaluation Order

Rules are evaluated in the order they appear in the configuration. The first matching rule wins; subsequent rules for the same attribute are ignored. Global (YAML) rules are applied first, followed by API-specific rules in the order they were added.

### Configuration Merge Behavior

When both global and API-specific rules are defined, the Gateway merges them by appending API rules after global rules. The `defaultReplacement` value from the global configuration is preserved unless the API configuration explicitly overrides it.

## Restrictions

* Partial mask character must be exactly one character; multi-character mask strings (e.g., `"XX"`) throw an error at construction time.
* Value patterns are case-sensitive, unlike key patterns (which are case-insensitive).
* Value patterns use partial matching; operators must use `^…$` anchors for full-string matching.
* Non-string attributes (Long, Boolean, Double, StringArray) are coerced to String when redacted; the original typed key is removed from the attributes map.
* First matching rule wins; if multiple rules match the same attribute key, only the first rule's masking strategy is applied.
* Short name expansion is automatic; patterns without dots, wildcards, or `regex:` prefix are treated as short names and expanded to `regex:(.*[._])?<pattern>$`.
* YAML rule index must be contiguous; configuration parsing stops at the first missing index.
* Redaction applies to span attributes and events only; span name, trace ID, span ID, and status are not redacted.
* Resource attributes (e.g., `service.instance.id`, `hostname`, `ip`) are redacted once at tracer creation time and reused for all spans; they are not re-evaluated per span.
* API-specific redaction rules are available only for v4 HTTP/Proxy and v4 TCP APIs.
* Read-only mode is triggered when the API definition context origin is `KUBERNETES`; the Console hides the "Add rule" button and row action buttons.

## Related Changes

The Console UI adds a **Span Attribute Redaction** section under Reporter Settings → Proxy, visible only when tracing is enabled and verbose mode is active. The section displays a table of redaction rules with columns for rule index, attribute pattern, masking strategy, value filter, and edit/delete actions. A redaction rule dialog supports adding and editing rules with live preview for partial masking. The Management API v2 schema includes new types `TracingRedactionConfig`, `TracingRedactionRule`, and `TracingMaskingStrategy` to support API-level redaction configuration. The `Tracing` model in the API definition includes an optional `redaction` field.
