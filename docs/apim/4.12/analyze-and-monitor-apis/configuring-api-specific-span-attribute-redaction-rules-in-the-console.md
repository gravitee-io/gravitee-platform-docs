# Configuring API-Specific Span Attribute Redaction Rules in the Console

## Creating API-Specific Redaction Rules

Navigate to **API Console → Reporter Settings → API Redaction Rules**. The redaction rules section is visible only when both **Tracing** and **Verbose** are enabled in the API analytics configuration. API-specific rules are appended after [platform-level rules](../guides/configuring-platform-level-span-attribute-redaction-rules.md#configuring-platform-level-span-attribute-redaction-rules); the first matching rule wins.

<figure><img src=".gitbook/assets/apim-span-attribute-redaction-for-opentelemetry-tracing-step-02.png" alt="Span Attribute Redaction section showing empty redaction rules table with Add rule button"><figcaption></figcaption></figure>

1. Click **Add Rule** to open the redaction rule dialog.
2. Enter an **Attribute Name Pattern**. Short names (no dots) match any namespace; `*` matches one segment; `**` matches any depth; prefix with `regex:` for exact Java regex.
    
    Examples:
    * `http.request.header.authorization`
    * `enduser.*`
    * `regex:gravitee\.(consumer|api)\.id`
3. Select a **Masking Type** from the dropdown: **FULL** (replaces entire value) or **PARTIAL** (preserves prefix/suffix).
4. (Optional) Enter **Replacement Text** for FULL masking. Leave blank to use the default `[REDACTED]`.
5. (PARTIAL only) Enter **Visible Prefix (chars)** to specify the number of leading characters to keep visible (minimum 0).
6. (PARTIAL only) Enter **Visible Suffix (chars)** to specify the number of trailing characters to keep visible (minimum 0).
7. (PARTIAL only) Enter a **Mask Character** (single character, default `*`).
8. (Optional) Enter a **Value Filter** regex. The rule only fires when the attribute value matches this pattern (e.g., `^Bearer ` for authorization headers).
9. Click **Add** to save the rule.

The redaction rules table displays each rule's attribute pattern, masking strategy (FULL or PARTIAL with detail text), and value filter. Use the **Edit** and **Delete** icon buttons to modify or remove rules. Click **Save** in the save bar to deploy the updated API configuration.

| Field | Description |
|:------|:------------|
| **Attribute Name Pattern** | Glob pattern, short name (no dots), or `regex:`-prefixed Java regex matching the span attribute key. |
| **Masking Type** | FULL or PARTIAL. |
| **Replacement Text** | FULL: replacement text (default `[REDACTED]`). PARTIAL: single mask character (default `*`). |
| **Visible Prefix (chars)** | PARTIAL only: number of leading characters to keep visible. |
| **Visible Suffix (chars)** | PARTIAL only: number of trailing characters to keep visible. |
| **Mask Character** | PARTIAL only: single character used to mask the middle section. |
| **Value Filter** | Optional Java regex (partial match). Rule only fires when the attribute value matches. |

## Managing Redaction Rules

### Editing Rules

Click the **Edit** icon button in the redaction rules table to open the rule dialog with pre-filled values. Modify the fields and click **Save** to update the rule. The rule's position in the evaluation order is preserved.

### Deleting Rules

Click the **Delete** icon button in the redaction rules table to remove a rule. Click **Save** in the save bar to deploy the updated API configuration.

### Resetting Changes

Click **Reset** in the save bar to discard pending changes and restore the last saved redaction rules configuration.
