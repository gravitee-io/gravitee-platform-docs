
# Reporter Settings — OpenTelemetry Section (Native APIs)

The Reporter Settings page of a V4 native API includes an **OpenTelemetry** section with **Enabled** and **Verbose** toggles for configuring per-API tracing.

## API Redaction Rules

The **API Redaction Rules** section allows you to configure span attribute redaction rules that apply only to this API. Rules mask sensitive span metadata (headers, consumer identifiers, query parameters) before OTLP export. API-level rules are evaluated after platform-level rules configured in `gravitee.yml`.

To add a redaction rule:

1. Click **Add Rule** to open the redaction rule dialog.
2. Enter an **Attribute Name Pattern** (e.g., `http.request.header.authorization`). Short names without dots match any namespace. Use `*` for one segment or `**` for any depth. Prefix with `regex:` for exact regex matching.
3. Select a **Masking Type** (`FULL` or `PARTIAL`).
4. For **FULL** masking, optionally enter **Replacement Text** (leave blank to use the default `[REDACTED]`).
5. For **PARTIAL** masking, configure **Visible Prefix** (number of leading characters to keep), **Visible Suffix** (number of trailing characters to keep), and **Mask Character** (single character, default `*`).
6. Optionally enter a **Value Filter** (Java regex, partial match) to restrict the rule to values matching the pattern.
7. Click **Save**. The rule appears in the API Redaction Rules table.
8. Deploy the API to apply the rules.

**Redaction Rule Fields:**

| Field | Description | Example |
|:------|:------------|:--------|
| **Attribute Name Pattern** | Glob or regex pattern matching span attribute keys. Short names (no dots) match any namespace. `*` = one segment, `**` = any depth. Prefix with `regex:` for exact regex. | `http.request.header.*` |
| **Masking Type** | `FULL` or `PARTIAL`. | `FULL` |
| **Replacement Text** (FULL) | Replacement text for FULL masking. Leave blank to use the default `[REDACTED]`. | `[REDACTED]` |
| **Visible Prefix** (PARTIAL) | Number of leading characters to keep visible. | `2` |
| **Visible Suffix** (PARTIAL) | Number of trailing characters to keep visible. | `4` |
| **Mask Character** (PARTIAL) | Single mask character. | `*` |
| **Value Filter** | Java regex (partial match). Rule only fires when the attribute value matches. | `Bearer *` |

## OTel Logs

The **OTel Logs** toggle enables payload capture as OpenTelemetry log records correlated to the active trace. When enabled, request and response payloads for all four directions (entrypoint/endpoint × request/response) are emitted as log records with `traceId` and `spanId` attributes for log-to-trace linking in Grafana and other OTel-compatible backends.

To enable OTel Logs:

1. Ensure **Analytics** and **Tracing** are both enabled.
2. Toggle **OTel Logs** to enable payload capture.
3. Deploy the API to apply the change.

For complete configuration details and the full attribute reference, see:

* [OpenTelemetry — Per-API tracing configuration for V4 native APIs](../../analyze-and-monitor-apis/opentelemetry.md#per-api-tracing-configuration-for-v4-native-apis)
* [Enable OpenTelemetry tracing for a Kafka API](../../kafka-gateway/create-and-configure-kafka-apis/configure-kafka-apis/enable-opentelemetry-tracing-for-a-kafka-api.md)

