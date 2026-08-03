# Configure Global Redaction Rules

## Gateway configuration

### Global redaction rules

Before any API-specific rule, configure platform-wide redaction rules in `gravitee.yml` under `services.opentelemetry.redaction`. Global rules are applied first.

| Property | Description | Example |
|:---------|:------------|:--------|
| `services.opentelemetry.redactionDefaultReplacement` | Fallback replacement text for FULL masking rules with no per-rule replacement. Defaults to `[REDACTED]`. | `[HIDDEN]` |
| `services.opentelemetry.redactionRules[N].attributeNamePattern` | Glob pattern, short name (no dots), or `regex:`-prefixed Java regex matching the span attribute key. | `http.request.header.authorization` |
| `services.opentelemetry.redactionRules[N].maskingStrategy.type` | `FULL` or `PARTIAL`. | `FULL` |
| `services.opentelemetry.redactionRules[N].maskingStrategy.replacement` | For FULL: replacement text. For PARTIAL: single mask character. | `[REDACTED]` (FULL) / `*` (PARTIAL) |
| `services.opentelemetry.redactionRules[N].maskingStrategy.prefixLength` | PARTIAL only: number of leading characters to keep visible. | `0` |
| `services.opentelemetry.redactionRules[N].maskingStrategy.suffixLength` | PARTIAL only: number of trailing characters to keep visible. | `4` |
| `services.opentelemetry.redactionRules[N].valuePattern` | Optional Java regex (partial match). Rule only fires when the attribute value matches. | `5[1-5][0-9]{14}` |

**Example:**

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

**Rule Evaluation Order:**

Rules are evaluated in the order they appear in the configuration. The first matching rule wins. Subsequent rules for the same attribute are ignored.

**Configuration Merge Behavior:**

When both global (YAML) and API-specific rules are defined:
- Global rules are applied first
- API-specific rules are appended after global rules
- The `defaultReplacement` from the global configuration is preserved unless the API configuration explicitly overrides it

### Docker

You can't define redaction rules with environment variables. The Gateway reads them from the `gravitee.yml` file. For a Docker deployment, mount a `gravitee.yml` file that contains your redaction rules into the container:

```yaml
services:
  gateway:
    image: graviteeio/apim-gateway:<version>
    volumes:
      - ./gravitee.yml:/opt/graviteeio-gateway/config/gravitee.yml
```

### Helm

Configure the rules under `gateway.services.opentelemetry` in your Helm values. The chart writes this block into the Gateway's `gravitee.yml`:

```yaml
gateway:
  services:
    opentelemetry:
      enabled: true
      exporter:
        endpoint: http://otel-collector:4317
      redactionDefaultReplacement: "[REDACTED]"
      redactionRules:
        - attributeNamePattern: "http.request.header.authorization"
          maskingStrategy:
            type: FULL
        - attributeNamePattern: "http.request.header.x-api-key"
          maskingStrategy:
            type: PARTIAL
            prefixLength: 2
            suffixLength: 2
            replacement: "*"
```
