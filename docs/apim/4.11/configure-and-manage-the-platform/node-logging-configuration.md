# Configuring Node Logging in Gateway and Management API

## Prerequisites

- APIM 4.11 or later
- Write access to `gravitee.yml` or Helm chart values
- For custom logback configuration: write access to `logback.xml`

## Gateway Configuration

### MDC Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `node.logging.mdc.format` | Format pattern for MDC key-value pairs | `"{key}: {value}"` (default) |
| `node.logging.mdc.separator` | Separator between MDC entries | `" "` (default) |
| `node.logging.mdc.nullValue` | Value displayed when MDC entry is null or log source is missing | `"-"` (default) |
| `node.logging.mdc.include` | MDC keys to include in log output | `[nodeId, apiId]` (Gateway default)<br>`[nodeId, envId, apiId, appId]` (Management API default) |

### Pattern Override Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `node.logging.pattern.overrideLogbackXml` | Whether to override logback.xml patterns at runtime | `true` (default in APIM 4.11+) |
| `node.logging.pattern.console` | Console appender pattern when override is enabled | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` |
| `node.logging.pattern.file` | File appender pattern when override is enabled | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` |

### Helm Chart Configuration

| Parameter | Description | Example |
|:----------|:------------|:--------|
| `gateway.logback.override` | Use `gateway.logback.content` as the complete logback.xml | `false` (default) |
| `gateway.logback.content` | Complete logback.xml content when override is enabled | See Helm chart values for default JSON-formatted configuration |
| `gateway.node.logging.mdc.format` | MDC format pattern | `"{key}: {value}"` |
| `gateway.node.logging.mdc.separator` | MDC separator | `" "` |
| `gateway.node.logging.mdc.nullValue` | MDC null value | `"-"` |
| `gateway.node.logging.mdc.include` | MDC keys to include | `[nodeId, apiId]` |
| `gateway.node.logging.pattern.overrideLogbackXml` | Override logback patterns | `false` (default) |
| `gateway.node.logging.pattern.console` | Console pattern | `"%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"` |
| `gateway.node.logging.pattern.file` | File pattern | `"%d %-5p [%t] %c [%mdcList] : %m%n"` |

Management API parameters follow the same structure with the `api.` prefix.

## Configuring MDC Enrichment

1. Edit `gravitee.yml` and set `node.logging.mdc.include` to the list of MDC keys you want to capture (e.g., `[nodeId, apiId, envId, appId]`).
2. Adjust `node.logging.mdc.format` to control how key-value pairs are formatted (default: `"{key}: {value}"`).
3. Set `node.logging.mdc.separator` to define the delimiter between entries (default: space).
4. To override logback.xml patterns at runtime, set `node.logging.pattern.overrideLogbackXml` to `true` and define `node.logging.pattern.console` and `node.logging.pattern.file` with patterns that include `%mdcList`.
5. Restart the Gateway or Management API for changes to take effect.

## Configuring Custom Logback Patterns

1. Set `node.logging.pattern.overrideLogbackXml` to `false` in `gravitee.yml`.
2. Edit `logback.xml` and include `%mdcList` in your appender patterns (e.g., `<pattern>%d{HH:mm:ss.SSS} [%thread] [%mdcList] %-5level %logger{36} - %msg%n</pattern>`).
3. Do NOT use `<conversionRule conversionWord="mdcList" converterClass="..."/>` in `logback.xml`—the `%mdcList` converter is registered programmatically and will fail with `PARSER_ERROR[mdcList]` if declared as a conversion rule.
4. Restart the Gateway or Management API for changes to take effect.

## Configuring Logging via Helm

1. Set `gateway.logback.override` to `true` and provide a complete logback configuration in `gateway.logback.content` (e.g., JSON-formatted ECS encoder configuration).
2. Configure MDC enrichment using `gateway.node.logging.mdc.include`, `gateway.node.logging.mdc.format`, and `gateway.node.logging.mdc.separator`.
3. To override logback patterns at runtime, set `gateway.node.logging.pattern.overrideLogbackXml` to `true` and define `gateway.node.logging.pattern.console` and `gateway.node.logging.pattern.file`.
4. Apply the Helm chart changes and restart the Gateway or Management API pods.

## Restrictions

- Not all plugins have been migrated to support MDC enrichment. Some logs may lack contextual information.
- Logs emitted during early startup (before `MdcListConverter` is registered) will not display `%mdcList` content.
- As of APIM 4.11, the following Helm parameters are deprecated:
  - `api.logging.debug` → Use `api.logback.override` instead
  - `api.logging.graviteeLevel` → Use `api.logback.override` instead
  - `api.logging.jettyLevel` → Use `api.logback.override` instead
  - `api.logging.stdout.encoderPattern` → Use `api.logback.override` instead
  - `api.logging.file.enabled` → Use `api.logback.override` instead
  - `api.logging.file.rollingPolicy` → Use `api.logback.override` instead
  - `api.logging.file.encoderPattern` → Use `api.logback.override` instead
  - `api.logging.additionalLoggers` → Use `api.logback.override` instead
