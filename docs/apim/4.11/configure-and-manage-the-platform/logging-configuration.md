# Configuring MDC and Log Patterns in gravitee.yml

## MDC Configuration

Configure MDC enrichment and log pattern formatting in `gravitee.yml` using the `node.logging.mdc.*` and `node.logging.pattern.*` properties.

### MDC Enrichment Properties

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `node.logging.mdc.format` | String | `"{key}: {value}"` | Key-value format pattern for MDC entries |
| `node.logging.mdc.separator` | String | `" "` (space) | Separator between MDC entries |
| `node.logging.mdc.nullValue` | String | `"-"` | Value displayed when MDC entry is null |
| `node.logging.mdc.include` | List<String> | `["nodeId", "apiId"]` (Gateway)<br>`["nodeId", "envId", "apiId", "appId"]` (Rest API) | MDC keys to include in log output |

When a log source is not available for a registered MDC key, the key is set to the value of `node.logging.mdc.nullValue` (default: `"-"`).

### Pattern Override Properties

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `node.logging.pattern.overrideLogbackXml` | Boolean | `true` | Override logback.xml patterns at runtime (enabled by default) |
| `node.logging.pattern.console` | String | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` | Console log pattern when override is enabled |
| `node.logging.pattern.file` | String | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` | File log pattern when override is enabled |

Pattern override is enabled by default. Console and file appender patterns are replaced at runtime with values from `gravitee.yml`.

## Using %mdcList in Log Patterns

Include `%mdcList` in log patterns to render MDC entries according to `node.logging.mdc.*` settings. The `%mdcList` conversion word formats MDC entries using the configured format, separator, and null value.

Example pattern:

```xml
<pattern>%d{HH:mm:ss.SSS} [%thread] [%mdcList] %-5level %logger{36} - %msg%n</pattern>
```

{% hint style="warning" %}
Do not use `<conversionRule conversionWord="mdcList" converterClass="..."/>` directly in `logback.xml`. The converter class is not visible to Logback's classloader at parse time. Use `node.logging.pattern.overrideLogbackXml=true` in `gravitee.yml` instead.
{% endhint %}

The `%mdcList` conversion word is registered programmatically via `PatternLayout.DEFAULT_CONVERTER_SUPPLIER_MAP` using the supplier-based API (Logback 1.4+).

## Disabling Pattern Override

To manage log patterns entirely in `logback.xml`, set `node.logging.pattern.overrideLogbackXml=false` in `gravitee.yml`. When disabled, console and file appender patterns are not replaced at runtime.

## Helm Chart Configuration

### Gateway Logging

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `gateway.logback.override` | Boolean | `false` | Use `gateway.logback.content` as complete logback.xml |
| `gateway.logback.content` | String | JSON-formatted logback config | Complete logback.xml content |
| `gateway.node.logging.mdc.format` | String | `"{key}: {value}"` | MDC key-value format pattern |
| `gateway.node.logging.mdc.separator` | String | `" "` | MDC entries separator |
| `gateway.node.logging.mdc.nullValue` | String | `"-"` | Value when MDC entry is null |
| `gateway.node.logging.mdc.include` | List<String> | `["nodeId", "apiId"]` | MDC keys to include |
| `gateway.node.logging.pattern.overrideLogbackXml` | Boolean | `false` | Override logback.xml patterns at runtime |
| `gateway.node.logging.pattern.console` | String | `"%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"` | Console pattern |
| `gateway.node.logging.pattern.file` | String | `"%d %-5p [%t] %c [%mdcList] : %m%n"` | File pattern |

### Management API Logging

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `api.logback.override` | Boolean | `false` | Use `api.logback.content` as complete logback.xml |
| `api.logback.content` | String | JSON-formatted logback config | Complete logback.xml content |
| `api.node.logging.mdc.format` | String | `"{key}: {value}"` | MDC key-value format pattern |
| `api.node.logging.mdc.separator` | String | `" "` | MDC entries separator |
| `api.node.logging.mdc.nullValue` | String | `"-"` | Value when MDC entry is null |
| `api.node.logging.mdc.include` | List<String> | `["nodeId", "envId", "apiId", "appId"]` | MDC keys to include |
| `api.node.logging.pattern.overrideLogbackXml` | Boolean | `false` | Override logback.xml patterns at runtime |
| `api.node.logging.pattern.console` | String | `"%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"` | Console pattern |
| `api.node.logging.pattern.file` | String | `"%d %-5p [%t] %c [%mdcList] : %m%n"` | File pattern |
