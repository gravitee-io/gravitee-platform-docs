# Configuring Span Attribute Redaction and Log Correlation for Individual APIs

## Creating API-Specific Redaction Rules

Open a v4 HTTP/Proxy or v4 TCP API in the Console and navigate to **Reporter Settings**. Enable tracing under **Analytics** → **Tracing** and select the **OpenTelemetry** exporter. In the **Reporter Settings** section, locate the **Span Attribute Redaction** area.

1. Click **Add Rule** to open the redaction rule dialog.
2. Enter an **Attribute Pattern** using glob-style wildcards (e.g., `http.request.header.*`, `gravitee.**`) or prefix with `regex:` for exact regex matching.
3. Select a **Masking** type: **FULL** (replaces the entire value) or **PARTIAL** (preserves prefix and suffix).
4. For **FULL** masking, optionally specify a **Replacement** text (defaults to `[REDACTED]`). For **PARTIAL** masking, configure **Prefix Length**, **Suffix Length**, and a single **Mask Character** (defaults to `*`).
5. Optionally enter a **Value Filter** (Java regex) to apply the rule only when the attribute value matches the pattern.
6. Click **Save** to add the rule.
7. Review the rule in the **API Redaction Rules** table. Each row displays the attribute pattern, masking type (badge), masking detail (e.g., `→ "[REDACTED]"` for FULL or `prefix 2 · suffix 4 · char "*"` for PARTIAL), value filter (if any), and Edit/Delete actions.
8. Deploy the API to activate the rules.

Global rules from `gravitee.yml` are always applied first; API-specific rules are appended after them.

| Field | Description | Example |
|:------|:------------|:--------|
| **Attribute Pattern** | Glob or regex pattern matching span attribute keys. Short names (no dots) match any namespace. `*` = one segment, `**` = any depth. Prefix with `regex:` for exact regex. | `http.request.header.*` |
| **Masking** | Masking type: **FULL** (replaces entire value) or **PARTIAL** (preserves prefix/suffix). | `FULL` |
| **Replacement** | FULL: replacement text. PARTIAL: single mask character. | `[REDACTED]` (FULL) / `*` (PARTIAL) |
| **Prefix Length** | PARTIAL only: number of leading characters to keep visible. | `2` |
| **Suffix Length** | PARTIAL only: number of trailing characters to keep visible. | `4` |
| **Value Filter** | Java regex (partial match). Rule only fires when the attribute value matches. | `Bearer *` |

## Enabling Log Correlation

Navigate to **Reporter Settings** → **OpenTelemetry** in a v4 HTTP/Proxy API.

1. Ensure **Analytics** and **Tracing** are both enabled.
2. Toggle **OTel Logs** to enable log correlation.
3. Deploy the API to activate log correlation.

When enabled, the Gateway emits request and response payloads as OpenTelemetry log records correlated to the active trace. Each log record includes `traceId` and `spanId` fields, enabling log-to-trace linking in Grafana and other OTel-compatible backends. For message APIs, capture is subject to the sampling strategy configured in Analytics settings. Ensure the OTLP HTTP log receiver (e.g., Loki) is configured at `services.opentelemetry.exporter.logsEndpoint` in `gravitee.yml`.

| Field | Description |
|:------|:------------|
| **OTel Logs** | Emit request and response payloads as OpenTelemetry log records correlated to the active trace. Enables log-to-trace linking in Grafana and other OTel-compatible backends. For message APIs, capture is subject to the sampling strategy configured above. |
