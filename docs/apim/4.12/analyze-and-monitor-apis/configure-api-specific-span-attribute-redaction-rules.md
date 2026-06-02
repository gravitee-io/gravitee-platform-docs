# Configure API-Specific Span Attribute Redaction Rules

## Creating API-Specific Redaction Rules

Navigate to **API Console → Reporter Settings → API Redaction Rules** (visible only when tracing and verbose tracing are both enabled). The API Redaction Rules table displays existing rules with columns for rule index, attribute pattern, masking type (FULL or PARTIAL with detail text), value filter, and edit/delete actions. A banner at the top of the table states "Global redaction rules are always applied first. Rules defined here are API-specific and are appended after them." When no rules exist, an empty state displays the message "No redaction rules — span attributes are exported as-is."

<figure><img src="../.gitbook/assets/apim-span-attribute-redaction-for-opentelemetry-tracing-step-02.png" alt="Span Attribute Redaction section showing empty redaction rules table with Add rule button"><figcaption></figcaption></figure>

1. Click **Add rule** to open the redaction rule dialog.
2. Enter an **Attribute Name Pattern** (required). The hint text reads "Short name (no dots) matches any namespace · `*` = one segment · `**` = any depth · prefix with `regex:` for exact regex."
3. Select a **Masking Type** from the dropdown: "Full Mask — replace entire value" or "Partial Mask — keep prefix / suffix visible."
4. If FULL is selected, optionally enter **Replacement Text** (hint: "Leave blank to use the default: [REDACTED]").
5. If PARTIAL is selected, enter **Visible Prefix (chars)** (minimum `0`), **Visible Suffix (chars)** (minimum `0`), and **Mask Character** (single character, hint: "Single character"). A live preview displays below the fields (e.g., "Preview: `AB****1234`" for sample value `ABCDEFGHIJ1234`).
6. Optionally enter a **Value Filter (optional)** (hint: "Regex (partial match). Rule only fires when the attribute value matches this pattern.").
7. Click **Add** (or **Save** in edit mode) to save the rule.

| Field | Description | Example |
|:------|:------------|:--------|
| Attribute Name Pattern | Glob pattern, short name, or `regex:`-prefixed Java regex | `http.request.header.*` |
| Masking Type | FULL or PARTIAL | FULL |
| Replacement Text | FULL only: replacement string (default `[REDACTED]`) | `[HIDDEN]` |
| Visible Prefix (chars) | PARTIAL only: number of leading characters to keep visible | `2` |
| Visible Suffix (chars) | PARTIAL only: number of trailing characters to keep visible | `4` |
| Mask Character | PARTIAL only: single mask character (default `*`) | `*` |
| Value Filter (optional) | Java regex (partial match) | `^Bearer ` |

Deploy the API to apply the redaction rules. Rules are evaluated at span export time, and the first matching rule determines the replacement.

## Managing Redaction Rules

Edit an existing rule by clicking the **Edit** button in the Actions column of the API Redaction Rules table. The redaction rule dialog opens in edit mode with the title "Edit redaction rule" and pre-populated fields. Modify the fields as needed and click **Save**. Delete a rule by clicking the **Delete** button in the Actions column. The rule is removed immediately from the pending rules list. Changes take effect after deploying the API.

### Management API

