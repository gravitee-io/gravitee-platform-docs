# Configuring Node-Aware Logging for Gateway and REST API

## Prerequisites

Before configuring node-aware logging, ensure the following requirements are met:

* Gravitee Gateway or REST API version 4.6.0 or later
* Logback 1.4+ (bundled with the platform)
* For custom policies or plugins: `gravitee-node` 8.0.0-alpha.15+ and `gravitee-gateway-api` 5.0.0+

## Gateway Configuration

### MDC Filtering

Control which MDC keys appear in log output using `node.logging.mdc.include`. The Gateway defaults to `[nodeId, apiId]`. The REST API defaults to `[nodeId, envId, apiId, appId]`.

| Property | Description | Example |
| --- | --- | --- |
| `node.logging.mdc.include` | List of MDC keys to render in `%mdcList` | `[nodeId, apiId, planId]` |
| `node.logging.mdc.format` | Key-value format pattern | `"{key}: {value}"` |
| `node.logging.mdc.separator` | Separator between MDC entries | `" "` (space) |
| `node.logging.mdc.nullValue` | Placeholder for null values | `"-"` |

### Log Pattern Override

Set `node.logging.pattern.overrideLogbackXml` to `true` (default since 4.6.0) to replace logback.xml patterns at runtime. This allows centralized pattern management via `gravitee.yml` without editing XML files.

| Property | Description | Example |
|:---------|:------------|:--------|
| `node.logging.pattern.overrideLogbackXml` | Enable runtime pattern override | `true` |
| `node.logging.pattern.console` | Console appender pattern | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` |
| `node.logging.pattern.file` | File appender pattern | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` |

{% hint style="info" %}
The `%mdcList` converter is registered programmatically and cannot be used directly in `logback.xml`. It only functions when `overrideLogbackXml` is enabled.
{% endhint %}

## Configuring Logging in Helm Deployments

Add node logging configuration to your Helm values file under `gateway.node.logging` or `api.node.logging`.

1. Set `logback.override` to `false` to use `gravitee.yml` patterns, or provide custom `logback.content` for full XML control.
2. Configure `node.logging.mdc.include` to filter MDC keys (e.g., `[nodeId, apiId, planId]` for the Gateway).
3. Adjust `node.logging.pattern.console` and `node.logging.pattern.file` to match your log aggregation format.
4. Set `node.logging.pattern.overrideLogbackXml` to `true` to apply these patterns at runtime.

The default Gateway pattern includes milliseconds (`%d{HH:mm:ss.SSS}`) for high-resolution timestamps.

**Example (Gateway):**

```yaml
gateway:
  logback:
    override: false
  node:
    logging:
      mdc:
        include: [nodeId, apiId, planId]
        format: "{key}={value}"
        separator: ", "
      pattern:
        overrideLogbackXml: true
        console: "%d{HH:mm:ss.SSS} %-5level [%mdcList] %logger{36} - %msg%n"
```

### Deprecated Helm Properties

The following Helm properties are deprecated and replaced by `logback.override` and `node.logging.*` properties:

* `*.logging.debug`
* `*.logging.graviteeLevel`
* `*.logging.jettyLevel`
* `*.logging.stdout.encoderPattern`
* `*.logging.file.enabled`
* `*.logging.file.rollingPolicy`
* `*.logging.file.encoderPattern`
* `*.logging.additionalLoggers`

## Writing Context-Aware Logs in Policies

Use `NodeLoggerFactory.getLogger()` to obtain a logger instance, then call `ctx.withLogger(log)` when an ExecutionContext is available.

1. Import `io.gravitee.node.logging.NodeLoggerFactory` and create a logger field.
2. In reactive handlers (e.g., `onRequest`, `onResponse`), wrap the logger with `ctx.withLogger(log)` before logging.
3. Use standard SLF4J methods (`info`, `debug`, `error`) on the wrapped logger.

The system automatically enriches logs with `nodeId`, `apiId`, and other context attributes.

For Lombok users, add `@CustomLog` to the class and configure `lombok.config` with:
