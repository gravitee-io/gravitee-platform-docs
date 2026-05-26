# Creating API-Specific Redaction Rules and Enabling Log Correlation in the Console

## Creating API-Specific Redaction Rules

Open a v4 HTTP/Proxy or v4 TCP API in the Console and navigate to **Analytics → Tracing**. Select **OpenTelemetry** as the exporter. Navigate to **Reporter Settings → API Redaction Rules**. Follow these steps to configure redaction rules:

1. Click **Add rule** to open the redaction rule dialog. The **Add rule** button is disabled for Kubernetes-origin APIs.
2. Enter an **Attribute Name Pattern** in the text field (e.g., `api-key`, `http.request.header.*`, `gravitee.**`). Short names (no dots) match any namespace. Use `*` for single-segment wildcards, `**` for multi-segment wildcards, or prefix with `regex:` for exact regex patterns.
3. Select a **Masking Type** from the dropdown: choose **Full Mask — replace entire value** or **Partial Mask — keep prefix / suffix visible**.
4. If **Full Mask** is selected, optionally enter **Replacement Text** (defaults to `[REDACTED]`).
5. If **Partial Mask** is selected, enter **Visible Prefix (chars)** (minimum 0), **Visible Suffix (chars)** (minimum 0), and **Mask Character** (single character, defaults to `*`). A live preview displays the masking result (e.g., `ABCXXXXXXXX234`).
6. Optionally enter a **Value Filter** regex (e.g., `^Bearer `) to apply the rule only when the attribute value matches the pattern.
7. Click **Add** (or **Save** when editing) to save the rule.
8. Deploy the API to activate the redaction rules.

**Reference Table:**

| Field | Description | Example |
|:------|:------------|:--------|
| **Attribute Name Pattern** | Glob or regex pattern matching span attribute keys. Short names (no dots) match any namespace. `*` = one segment, `**` = any depth. Prefix with `regex:` for exact regex. | `http.request.header.authorization` |
| **Masking Type** | `FULL` (replace entire value) or `PARTIAL` (keep prefix/suffix visible). | `FULL` |
| **Replacement Text** | FULL only: replacement string (defaults to `[REDACTED]`). | `[REDACTED]` |
| **Visible Prefix (chars)** | PARTIAL only: number of leading characters to keep visible (minimum 0). | `2` |
| **Visible Suffix (chars)** | PARTIAL only: number of trailing characters to keep visible (minimum 0). | `2` |
| **Mask Character** | PARTIAL only: single character used for masking (defaults to `*`). | `*` |
| **Value Filter** | Optional Java regex (partial match). Rule only fires when the attribute value matches. | `^Bearer ` |

## Enabling Log Correlation

Navigate to **Reporter Settings** for a v4 HTTP/Proxy or v4 Message API. Follow these steps to enable log correlation:

1. Ensure **Analytics** is enabled.
2. Ensure **Tracing** is enabled.
3. Toggle **OTel Logs** to **ON**. For Proxy APIs, request and response payloads are emitted as OpenTelemetry log records correlated to the active trace. For Message APIs, message payloads are emitted as log records subject to the configured sampling strategy.
4. Deploy the API.
5. Verify that `services.opentelemetry.exporter.logsEndpoint` is configured in `gravitee.yml` (defaults to `http://localhost:3100/otlp/v1/logs`).

**Reference Table:**

| Field | Description |
|:------|:------------|
| **OTel Logs** | Emit request and response payloads (Proxy APIs) or message payloads (Message APIs) as OpenTelemetry log records correlated to the active trace. Enables log-to-trace linking in Grafana and other OTel-compatible backends. Disabled when Tracing or Analytics is off. |
