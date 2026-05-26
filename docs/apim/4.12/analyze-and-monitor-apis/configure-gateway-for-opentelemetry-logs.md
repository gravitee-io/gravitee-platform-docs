# Configure Gateway for OpenTelemetry Logs

## Gateway Configuration

### OpenTelemetry Service

To enable OpenTelemetry tracing and configure the logs export endpoint, configure the following properties in your `gravitee.yaml`:

| Property | Description | Example |
|:---------|:------------|:--------|
| `services.opentelemetry.enabled` | Enable OpenTelemetry globally on the Gateway | `true` |
| `services.opentelemetry.traces.enabled` | Enable OpenTelemetry tracing | `true` |
| `services.opentelemetry.exporter.logsEndpoint` | OTLP HTTP endpoint for log records. This must be the full URL including signal path, for example, `/v1/logs`. Log records are always exported over HTTP/Protobuf and not gRPC. | `http://localhost:3100/otlp/v1/logs` |
| `services.opentelemetry.exporter.compression` | Compression algorithm for log export | `none` |
| `services.opentelemetry.exporter.timeout` | Export timeout | `10s` |

**Environment variable equivalent:** `gravitee_services_opentelemetry_exporter_logsEndpoint=http://<loki>:3100/otlp/v1/logs`

{% hint style="warning" %}
When you run the Gateway inside Docker, use the container hostname, for example, `http://loki:3100/otlp/v1/logs`, not `localhost` because `localhost` resolves to the Gateway container itself.
{% endhint %}

{% hint style="info" %}
If OTel is disabled globally on the Gateway, the feature has zero overhead.
{% endhint %}

### Redaction Rules

Define redaction rules under `services.tracing.otel.redaction` to apply gateway-level protection to all APIs. Rules configured here apply to all APIs and are evaluated before API-level rules.

| Property | Description | Example |
|:---------|:------------|:--------|
| `services.tracing.otel.redaction.defaultReplacement` | Fallback replacement text for FULL rules with no per-rule replacement. | `[REDACTED]` |
| `services.tracing.otel.redaction.rules[N].attributeNamePattern` | Glob or regex pattern matching span attribute keys. Short names (no dots) match any namespace. `*` = one segment, `**` = any depth. Prefix with `regex:` for exact regex. | `http.request.header.authorization` |
| `services.tracing.otel.redaction.rules[N].maskingStrategy.type` | Masking strategy: `FULL` or `PARTIAL`. | `FULL` |
| `services.tracing.otel.redaction.rules[N].maskingStrategy.replacement` | FULL: replacement text. PARTIAL: single mask character. | `[REDACTED]` (FULL) / `*` (PARTIAL) |
| `services.tracing.otel.redaction.rules[N].maskingStrategy.prefixLength` | PARTIAL only: number of leading characters to keep visible. | `2` |
| `services.tracing.otel.redaction.rules[N].maskingStrategy.suffixLength` | PARTIAL only: number of trailing characters to keep visible. | `4` |
| `services.tracing.otel.redaction.rules[N].valuePattern` | Java regex (partial match). Rule only fires when the attribute value matches. | `Bearer *` |

**Example:**

```yaml
services:
  tracing:
    enabled: true
    type: opentelemetry
    otel:
      endpoint: http://otel-collector:4317
      redaction:
        defaultReplacement: "[REDACTED]"
        rules:
          - attributeNamePattern: "http.request.header.authorization"
            maskingStrategy:
              type: FULL
              replacement: "[REDACTED]"
          - attributeNamePattern: "http.request.header.**"
            maskingStrategy:
              type: FULL
          - attributeNamePattern: "url.query"
            valuePattern: "*token=*"
            maskingStrategy:
              type: FULL
          - attributeNamePattern: "enduser.id"
            maskingStrategy:
              type: PARTIAL
              prefixLength: 0
              suffixLength: 4
              replacement: "*"
```

**Environment variable equivalent:**

```bash
gravitee_services_tracing_otel_redaction_defaultReplacement=[REDACTED]
gravitee_services_tracing_otel_redaction_rules_0_attributeNamePattern=http.request.header.authorization
gravitee_services_tracing_otel_redaction_rules_0_maskingStrategy_type=FULL
```

**Helm configuration:**

```yaml
gateway:
  services:
    tracing:
      enabled: true
      type: opentelemetry
      otel:
        endpoint: http://otel-collector:4317
        redaction:
          defaultReplacement: "[REDACTED]"
          rules:
            - attributeNamePattern: "http.request.header.authorization"
              maskingStrategy:
                type: FULL
            - attributeNamePattern: "gravitee.consumer.**"
              maskingStrategy:
                type: PARTIAL
                prefixLength: 2
                suffixLength: 2
                replacement: "*"
    opentelemetry:
      exporter:
        logsEndpoint: http://loki:3100/otlp/v1/logs
```

#### Environment Variable Overrides

Override configuration properties using environment variables:

```bash
gravitee_services_tracing_otel_redaction_defaultReplacement=[REDACTED]
gravitee_services_tracing_otel_redaction_rules_0_attributeNamePattern=http.request.header.authorization
gravitee_services_tracing_otel_redaction_rules_0_maskingStrategy_type=FULL
gravitee_services_opentelemetry_exporter_logsEndpoint=http://loki:3100/otlp/v1/logs
```

