# Node Logging Configuration Reference

## Prerequisites

- Gravitee Gateway or REST API version 4.6.0 or later (includes `gravitee-node` 8.0.0-alpha.2+)
- Logback 1.4+ (for supplier-based converter registration)
- Maven 3.6+ (if enforcing architecture rules during builds)

## Gateway Configuration

### Node Logging Properties

Configure in `gravitee.yml` under the `node.logging` namespace.

| Property | Description | Example |
|:---------|:------------|:--------|
| `node.logging.mdc.format` | Template for each MDC key-value pair | `"{key}: {value}"` (default) |
| `node.logging.mdc.separator` | Separator between MDC entries | `" "` (default), `", "` |
| `node.logging.mdc.nullValue` | Placeholder when MDC value is null | `"-"` (default), `"N/A"` |
| `node.logging.mdc.include` | List of MDC keys to include in `%mdcList` output | `["nodeId", "apiId"]` (Gateway default)<br>`["nodeId", "envId", "apiId", "appId"]` (REST API default) |
| `node.logging.pattern.overrideLogbackXml` | When `true`, runtime patterns override `logback.xml` | `true` (default) |
| `node.logging.pattern.console` | Console log pattern (when override enabled) | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` |
| `node.logging.pattern.file` | File log pattern (when override enabled) | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` |

### Helm Chart Properties (Gateway)

Configure in `values.yaml` under the `gateway` namespace.

| Property | Description | Example |
|:---------|:------------|:--------|
| `gateway.logback.override` | When `true`, replaces entire `logback.xml` with `gateway.logback.content` | `false` (default) |
| `gateway.logback.content` | Complete logback.xml content (used only if override is `true`) | See Helm chart for JSON-formatted default |
| `gateway.node.logging.mdc.format` | MDC key-value format | `"{key}: {value}"` |
| `gateway.node.logging.mdc.separator` | MDC entry separator | `" "` |
| `gateway.node.logging.mdc.nullValue` | Null value placeholder | `"-"` |
| `gateway.node.logging.mdc.include` | MDC keys to include | `["nodeId", "apiId"]` |
| `gateway.node.logging.pattern.overrideLogbackXml` | Enable runtime pattern override | `false` (default) |
| `gateway.node.logging.pattern.console` | Console pattern (when override enabled) | `"%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"` |
| `gateway.node.logging.pattern.file` | File pattern (when override enabled) | `"%d %-5p [%t] %c [%mdcList] : %m%n"` |

## Configuring MDC Output

To customize which metadata appears in logs and how it is formatted:

1. Edit `gravitee.yml` and set `node.logging.mdc.include` to the desired MDC keys (e.g., `["nodeId", "apiId", "envId"]`).
2. Adjust `node.logging.mdc.format` to control the key-value template (e.g., `"{key}={value}"` for `nodeId=abc123`).
3. Set `node.logging.mdc.separator` to control spacing (e.g., `", "` for comma-separated entries).
4. Optionally override `node.logging.mdc.nullValue` to change the placeholder for missing values (default `"-"`).
5. Enable `node.logging.pattern.overrideLogbackXml: true` and configure `node.logging.pattern.console` and `node.logging.pattern.file` to include `%mdcList` in the desired position.
6. Restart the Gateway or REST API for changes to take effect.

{% hint style="warning" %}
The `%mdcList` pattern token cannot be declared in `logback.xml` via `<conversionRule>` due to classloader visibility. Use `pattern.overrideLogbackXml=true` and configure patterns in `gravitee.yml` instead.
{% endhint %}

## Deprecated Configuration

The following Helm chart properties remain functional but are discouraged:

**Gateway:**
- `gateway.logging.debug`
- `gateway.logging.graviteeLevel`
- `gateway.logging.jettyLevel`
- `gateway.logging.stdout.encoderPattern`
- `gateway.logging.file.enabled`
- `gateway.logging.file.rollingPolicy`
- `gateway.logging.file.encoderPattern`
- `gateway.logging.additionalLoggers`

**REST API:**
- `api.logging.debug`
- `api.logging.graviteeLevel`
- `api.logging.jettyLevel`
- `api.logging.stdout.encoderPattern`
- `api.logging.file.enabled`
- `api.logging.file.rollingPolicy`
- `api.logging.file.encoderPattern`
- `api.logging.additionalLoggers`

Use `gateway.logback.override` / `api.logback.override` and `gateway.node.logging.*` / `api.node.logging.*` instead.

## Architecture Rule Enforcement

The `gravitee-archrules-maven-plugin` enforces two rules at build time:

1. Classes must use `NodeLoggerFactory.getLogger(TYPE)` instead of SLF4J's `LoggerFactory` directly.
2. Methods with an `ExecutionContext` parameter must call `ctx.withLogger(log)` instead of logging directly.

Violations fail the build unless the class is allow-listed or the package is excluded. Test classes are excluded by default.

### Maven Plugin Configuration

Configure in `pom.xml` or via command-line properties:

| Property | Description | Default |
|:---------|:------------|:--------|
| `gravitee.archrules.skip` | Skip all architecture rule checks | `false` |
| `gravitee-archrules-maven-plugin.version` | Version of the architecture rules plugin | `1.0.0-alpha.2` |
