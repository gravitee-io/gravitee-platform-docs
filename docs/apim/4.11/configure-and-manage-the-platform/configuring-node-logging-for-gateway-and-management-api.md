# Configuring Node Logging for Gateway and Management API

### Helm Chart Logback Override

The Helm chart supports two logback configuration modes. When `api.logback.override` or `gateway.logback.override` is `false`, the chart uses legacy properties like `api.logging.debug` and `api.logging.graviteeLevel`. When set to `true`, the chart uses the complete `logback.xml` content from `api.logback.content` or `gateway.logback.content`, ignoring all legacy properties. The `node.logging.*` properties remain active in both modes for MDC and pattern configuration.

## Prerequisites

- Gravitee API Management 4.11 or later
- Write access to `gravitee.yml` or Helm chart values
- Maven 3.6+ (for build-time architecture rule enforcement)

## Gateway Configuration

### Node Logging Properties

Configure in `gravitee.yml` for both Gateway and Management API components.

| Property | Description | Example |
|:---------|:------------|:--------|
| `node.logging.mdc.format` | Template for rendering each MDC key-value pair | `"{key}: {value}"` |
| `node.logging.mdc.separator` | String inserted between MDC entries | `" "` (space) |
| `node.logging.mdc.nullValue` | Placeholder when MDC value is null | `"-"` |
| `node.logging.mdc.include` | List of MDC keys to include in log output | Gateway: `["nodeId", "apiId"]`<br>Management API: `["nodeId", "envId", "apiId", "appId"]` |
| `node.logging.pattern.overrideLogbackXml` | Whether to override logback.xml patterns at runtime | `true` (default since 8.0.0-alpha.15) |
| `node.logging.pattern.console` | Console log pattern when override is enabled | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` |
| `node.logging.pattern.file` | File log pattern when override is enabled | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` |

### Helm Chart Properties

#### API Component

| Property | Description | Example |
|:---------|:------------|:--------|
| `api.logback.override` | Use `api.logback.content` as complete logback.xml | `false` |
| `api.logback.content` | Complete logback.xml content when override is true | JSON-formatted XML string |
| `api.node.logging.mdc.format` | MDC key-value format pattern | `"{key}: {value}"` |
| `api.node.logging.mdc.separator` | MDC entries separator | `" "` |
| `api.node.logging.mdc.nullValue` | Value when MDC entry is null | `"-"` |
| `api.node.logging.mdc.include` | MDC keys to include | `["nodeId", "envId", "apiId", "appId"]` |
| `api.node.logging.pattern.overrideLogbackXml` | Override logback.xml patterns at runtime | `false` |
| `api.node.logging.pattern.console` | Console pattern | `"%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"` |
| `api.node.logging.pattern.file` | File pattern | `"%d %-5p [%t] %c [%mdcList] : %m%n"` |

#### Gateway Component

| Property | Description | Example |
|:---------|:------------|:--------|
| `gateway.logback.override` | Use `gateway.logback.content` as complete logback.xml | `false` |
| `gateway.logback.content` | Complete logback.xml content when override is true | JSON-formatted async XML string |
| `gateway.node.logging.mdc.format` | MDC key-value format pattern | `"{key}: {value}"` |
| `gateway.node.logging.mdc.separator` | MDC entries separator | `" "` |
| `gateway.node.logging.mdc.nullValue` | Value when MDC entry is null | `"-"` |
| `gateway.node.logging.mdc.include` | MDC keys to include | `["nodeId", "apiId"]` |
| `gateway.node.logging.pattern.overrideLogbackXml` | Override logback.xml patterns at runtime | `false` |
| `gateway.node.logging.pattern.console` | Console pattern | `"%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"` |
| `gateway.node.logging.pattern.file` | File pattern | `"%d %-5p [%t] %c [%mdcList] : %m%n"` |

### Maven Plugin Properties

| Property | Description | Example |
|:---------|:------------|:--------|
| `gravitee.archrules.skip` | Skip all ArchUnit rule checks | `true` |

## Configuring Log Patterns

Set `node.logging.pattern.overrideLogbackXml: true` in `gravitee.yml` (the default since version 8.0.0-alpha.15). Define your desired patterns in `node.logging.pattern.console` and `node.logging.pattern.file`, using the `%mdcList` conversion word to render MDC entries. For example: `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` includes milliseconds and MDC context. The platform applies these patterns at runtime, overriding the defaults in `logback.xml`. Customize MDC rendering via `node.logging.mdc.format` and `node.logging.mdc.separator`. Control which MDC keys appear in logs via `node.logging.mdc.include`.

{% hint style="warning" %}
Do not use `<conversionRule conversionWord="mdcList" converterClass="..."/>` directly in `logback.xml`. The converter is registered programmatically after bootstrap. Use `node.logging.pattern.overrideLogbackXml` instead.
{% endhint %}
