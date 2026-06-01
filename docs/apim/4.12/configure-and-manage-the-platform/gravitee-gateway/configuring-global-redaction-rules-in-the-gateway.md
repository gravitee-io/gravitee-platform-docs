# Configuring Global Redaction Rules in the Gateway

## Gateway Configuration

### Global Redaction Rules

Configure platform-wide redaction rules in `gravitee.yml`. These rules apply to all APIs and are evaluated before API-specific rules.

| Property | Description | Example |
|:---------|:------------|:--------|
| `services.opentelemetry.redactionDefaultReplacement` | Fallback replacement text for FULL masking rules with no per-rule replacement | `[REDACTED]` |
| `services.opentelemetry.redactionRules[N].attributeNamePattern` | Glob pattern, short name (no dots), or `regex:`-prefixed Java regex matching the span attribute key | `http.request.header.authorization` |
| `services.opentelemetry.redactionRules[N].maskingStrategy.type` | Masking strategy: `FULL` or `PARTIAL` | `FULL` |
| `services.opentelemetry.redactionRules[N].maskingStrategy.replacement` | For FULL: replacement text. For PARTIAL: single mask character | `[HIDDEN]` (FULL) / `*` (PARTIAL) |
| `services.opentelemetry.redactionRules[N].maskingStrategy.prefixLength` | PARTIAL only — number of leading characters to keep visible | `2` |
| `services.opentelemetry.redactionRules[N].maskingStrategy.suffixLength` | PARTIAL only — number of trailing characters to keep visible | `4` |
| `services.opentelemetry.redactionRules[N].valuePattern` | Java regex (partial match). Rule only fires when the attribute value matches | `^Bearer ` |

Example configuration:

```yaml
services:
  opentelemetry:
    enabled: true
    redactionDefaultReplacement: "[REDACTED]"
    redactionRules:
      - attributeNamePattern: "http.request.header.authorization"
        maskingStrategy:
          type: FULL
          replacement: "[HIDDEN]"
        valuePattern: "^Bearer "
      - attributeNamePattern: "enduser.id"
        maskingStrategy:
          type: PARTIAL
          prefixLength: 0
          suffixLength: 4
          replacement: "*"
```

### Docker Compose Configuration

Override configuration using environment variables:

```bash
gravitee_services_tracing_otel_redaction_defaultReplacement=[REDACTED]
gravitee_services_tracing_otel_redaction_rules_0_attributeNamePattern=http.request.header.authorization
gravitee_services_tracing_otel_redaction_rules_0_maskingStrategy_type=FULL
```

Example Docker Compose configuration:

```yaml
services:
  gateway:
    image: graviteeio/apim-gateway:latest
    environment:
      - gravitee_services_tracing_otel_enabled=true
      - gravitee_services_tracing_otel_redaction_defaultReplacement=[REDACTED]
      - gravitee_services_tracing_otel_redaction_rules_0_attributeNamePattern=http.request.header.authorization
      - gravitee_services_tracing_otel_redaction_rules_0_maskingStrategy_type=FULL
      - gravitee_services_tracing_otel_redaction_rules_0_maskingStrategy_replacement=[HIDDEN]
      - gravitee_services_tracing_otel_redaction_rules_0_valuePattern=^Bearer 
      - gravitee_services_tracing_otel_redaction_rules_1_attributeNamePattern=enduser.id
      - gravitee_services_tracing_otel_redaction_rules_1_maskingStrategy_type=PARTIAL
      - gravitee_services_tracing_otel_redaction_rules_1_maskingStrategy_prefixLength=0
      - gravitee_services_tracing_otel_redaction_rules_1_maskingStrategy_suffixLength=4
      - gravitee_services_tracing_otel_redaction_rules_1_maskingStrategy_replacement=*
```

### Helm Configuration

Configure redaction rules in `values.yaml` under `gateway.services.tracing.otel.redaction`:

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
