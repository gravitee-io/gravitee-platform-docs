# Configuring Platform-Level Span Attribute Redaction Rules

## Gateway Configuration

### Platform-Level Redaction Rules

Configure redaction rules in `gravitee.yml` under `services.opentelemetry.redaction`. Platform-level rules are always applied first, before [API-specific rules](../analyze-and-monitor-apis/configuring-api-specific-span-attribute-redaction-rules-in-the-console.md#configuring-api-specific-span-attribute-redaction-rules-in-the-console).

| Property | Description | Example |
|:---------|:------------|:--------|
| `services.opentelemetry.redactionDefaultReplacement` | Fallback replacement text for FULL masking rules with no per-rule replacement. | `[REDACTED]` |
| `services.opentelemetry.redactionRules[N].attributeNamePattern` | Glob pattern, short name (no dots), or `regex:`-prefixed Java regex matching the span attribute key. | `http.request.header.authorization` |
| `services.opentelemetry.redactionRules[N].maskingStrategy.type` | `FULL` or `PARTIAL`. | `FULL` |
| `services.opentelemetry.redactionRules[N].maskingStrategy.replacement` | FULL: replacement text. PARTIAL: single mask character. | `[REDACTED]` (FULL) / `*` (PARTIAL) |
| `services.opentelemetry.redactionRules[N].maskingStrategy.prefixLength` | PARTIAL only: number of leading characters to keep visible. | `0` |
| `services.opentelemetry.redactionRules[N].maskingStrategy.suffixLength` | PARTIAL only: number of trailing characters to keep visible. | `0` |
| `services.opentelemetry.redactionRules[N].valuePattern` | Java regex (partial match). Rule only fires when the attribute value matches. | `^Bearer ` |

**Example YAML:**

```yaml
services:
  opentelemetry:
    redactionDefaultReplacement: "[HIDDEN]"
    redactionRules:
      - attributeNamePattern: "enduser.id"
        maskingStrategy:
          type: FULL
          replacement: "[REDACTED]"
      - attributeNamePattern: "payment.card"
        maskingStrategy:
          type: PARTIAL
          prefixLength: 0
          suffixLength: 4
          replacement: "*"
        valuePattern: "5[1-5][0-9]{14}"
```

### Environment Variable Overrides

Override platform-level redaction configuration using environment variables:

```bash
gravitee_services_tracing_otel_redaction_defaultReplacement=[REDACTED]
gravitee_services_tracing_otel_redaction_rules_0_attributeNamePattern=http.request.header.authorization
gravitee_services_tracing_otel_redaction_rules_0_maskingStrategy_type=FULL
```

### Docker Compose Setup

Mount `gravitee.yml` and configure environment variables:

```yaml
services:
  gateway:
    image: graviteeio/apim-gateway:4.12.0
    volumes:
      - ./gravitee.yml:/opt/graviteeio-gateway/config/gravitee.yml:ro
    environment:
      gravitee_services_tracing_enabled: true
      gravitee_services_tracing_type: opentelemetry
      gravitee_services_tracing_otel_endpoint: http://otel-collector:4317
```

### Helm Setup

Configure redaction rules in `values.yaml`:

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
```
