---
description: Manage API-specific span attribute redaction rules in the Management Console.
hidden: true
noIndex: true
---

# Manage API-Specific Redaction Rules in the Management Console

## Create API-Specific Redaction Rules

You configure API-specific redaction rules in the Management Console under **Reporter Settings**, **Proxy**, and then **Span Attribute Redaction**. This section is visible only when tracing is enabled and verbose mode is active. The system appends API-specific rules after global rules. They take precedence for matching attributes.

<figure><img src="../../.gitbook/assets/apim-span-attribute-redaction-for-opentelemetry-tracing-step-02.png" alt="Span attribute redaction section with empty rules table and add rule button"><figcaption></figcaption></figure>

To create API-specific redaction rules, complete the following steps:
1. Navigate to **Reporter Settings**, **Proxy**, and then **Span Attribute Redaction**.
2. Click **Add rule** to open the redaction rule dialog.
3. Enter an **Attribute Name Pattern**. Here are some examples: `http.request.header.authorization`, `enduser.*`, and `regex:payment\.(card|token)`.
4. Select a **Masking Type**. Select `FULL` to replace the entire value, or select `PARTIAL` to keep the prefix and suffix visible.
5. (Optional) If you select FULL masking, enter **Replacement Text**. Leave this blank to use the default `[REDACTED]`.
6. If you select PARTIAL masking, configure **Visible Prefix (chars)**, **Visible Suffix (chars)**, and **Mask Character**. The default mask character is a single `*`. A live preview displays the masking result.
7. (Optional) Enter a **Value Filter**. This uses a Java regex for a partial match. The rule fires only when the attribute value matches this pattern.
8. Click **Add** to save the rule.

The following table describes the fields for redaction rules:

| Field | Description | Example |
|:------|:------------|:--------|
| Attribute Name Pattern | This is a glob pattern, short name, or `regex:`-prefixed Java regex that matches the span attribute key. Short names without dots match any namespace. `*` matches one segment. `**` matches any depth. Prefix with `regex:` for exact regex. | `http.request.header.*` |
| Masking Type | `FULL` or `PARTIAL`. `FULL` replaces the entire value. `PARTIAL` keeps the prefix and suffix visible. | `FULL` |
| Replacement Text | For FULL masking, this is the replacement text. The default is `[REDACTED]`. | `[REDACTED]` |
| Visible Prefix (chars) | For PARTIAL masking only, this is the number of leading characters to keep visible. | `2` |
| Visible Suffix (chars) | For PARTIAL masking only, this is the number of trailing characters to keep visible. | `4` |
| Mask Character | For PARTIAL masking only, this is the single character used for masking. | `*` |
| Value Filter | Optional Java regex partial match. The rule fires only when the attribute value matches. | `Bearer .*` |

The Management Console displays existing rules in a table with columns for rule index, attribute pattern, masking strategy, value filter, and edit and delete actions. A banner notes that global redaction rules always apply first, and API-specific rules append after them.

## Manage Redaction Rules

To manage redaction rules, complete the following steps:
1. [Editing Rules](#editing-rules)
2. [Deleting Rules](#deleting-rules)

### Editing Rules

1. Click **Edit** in the rule table row to open the redaction rule dialog with pre-filled values.
2. Modify the fields, and then click **Save** to update the rule.

### Delete Rules

* Click **Delete** in the rule table row to remove the rule. Changes take effect when you save and deploy the API configuration.

### Rule Evaluation Order

Rules evaluate in the order they appear in the configuration. The first matching rule wins, and the system ignores subsequent rules for the same attribute. The system applies global (YAML) rules first, followed by API-specific rules in the order you added them.

### Configuration Merge Behavior

When you define both global and API-specific rules, the API Gateway merges them by appending API rules after global rules. The system preserves the `defaultReplacement` value from the global configuration unless the API configuration explicitly overrides it.

## Restrictions

Review the following restrictions for redaction rules:
* The partial mask character must be exactly one character. Multi-character mask strings throw an error at construction time.
* Value patterns are case-sensitive, and key patterns are case-insensitive.
* Value patterns use partial matching. Operators must use `^…$` anchors for full-string matching.
* Non-string attributes are coerced to String when redacted. The original typed key is removed from the attributes map. Non-string attributes include Long, Boolean, Double, and StringArray.
* The first matching rule wins. If multiple rules match the same attribute key, only the first rule's masking strategy applies.
* Short name expansion is automatic. The system treats patterns without dots, wildcards, or the `regex:` prefix as short names and expands them to `regex:(.*[._])?<pattern>$`.
* The YAML rule index must be contiguous. Configuration parsing stops at the first missing index.
* Redaction applies only to span attributes and events. The system does not redact the span name, trace ID, span ID, and status.
* The system redacts resource attributes once at tracer creation time and reuses them for all spans. It does not re-evaluate them per span. Resource attributes include `service.instance.id`, `hostname`, and `ip`.
* API-specific redaction rules are available only for v4 HTTP proxy APIs and v4 TCP proxy APIs.
* Read-only mode triggers when the API definition context origin is `Kubernetes`. The Management Console hides the **Add rule** button and row action buttons.

## Related Changes

The Management Console UI adds a **Span Attribute Redaction** section under **Reporter Settings** and **Proxy**. This is visible only when tracing is enabled and verbose mode is active. The section displays a table of redaction rules with columns for rule index, attribute pattern, masking strategy, value filter, and edit and delete actions. A redaction rule dialog supports adding and editing rules with a live preview for partial masking. The Management API (mAPI) v2 schema includes new types to support API-level redaction configuration. These types include `TracingRedactionConfig`, `TracingRedactionRule`, and `TracingMaskingStrategy`. The `Tracing` model in the API definition includes an optional `redaction` field.