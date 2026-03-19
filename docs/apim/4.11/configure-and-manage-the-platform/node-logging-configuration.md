# Configuring Node Logging for Gateway and Management API

Gravitee Gateway and Management API use a centralized logging infrastructure that enriches log output with node-level and request-level metadata. Administrators configure MDC filtering, log patterns, and Logback overrides via `gravitee.yml` or Helm chart parameters.

### MDC Filtering and Formatting

The `%mdcList` Logback converter formats selected MDC keys into log output. Administrators configure which keys to include (`node.logging.mdc.include`), how to format each entry (`node.logging.mdc.format`), and how to separate entries (`node.logging.mdc.separator`). This avoids cluttering logs with unused context fields. The converter is registered programmatically at runtime, not via `<conversionRule>` in `logback.xml`.

**MDC Filtering Configuration**

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `node.logging.mdc.format` | String | `"{key}: {value}"` | Template for formatting each MDC key-value pair |
| `node.logging.mdc.separator` | String | `" "` (space) | Separator between MDC entries |
| `node.logging.mdc.nullValue` | String | `"-"` | Placeholder when MDC value is null |
| `node.logging.mdc.include` | List<String> | `[nodeId, apiId]` (Gateway)<br/>`[nodeId, envId, apiId, appId]` (Management API) | MDC keys to include in `%mdcList` output |

**Example `gravitee.yml`:**

```yaml
node:
  logging:
    mdc:
      format: "{key}={value}"
      separator: ", "
      nullValue: "N/A"
      include:
        - nodeId
        - apiId
        - envId
        - appId
```

### Pattern Override

Override Logback appender patterns at runtime without modifying `logback.xml`.

**Pattern Override Configuration**

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `node.logging.pattern.overrideLogbackXml` | Boolean | `true` (as of 4.0.0-alpha.2) | Whether to override logback.xml patterns at runtime |
| `node.logging.pattern.console` | String | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` | Console appender pattern when override is enabled |
| `node.logging.pattern.file` | String | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` | File appender pattern when override is enabled |

**Example `gravitee.yml`:**

```yaml
node:
  logging:
    pattern:
      overrideLogbackXml: true
      console: "%d{HH:mm:ss.SSS} [%thread] [%mdcList] %-5level %logger{36} - %msg%n"
      file: "%d %-5p [%t] %c [%mdcList] : %m%n"
```

When `overrideLogbackXml` is `true`, the runtime patterns replace those defined in `logback.xml`. The `%mdcList` converter is always registered programmatically, regardless of this setting.

{% hint style="warning" %}
Do not use `<conversionRule>` in `logback.xml` to register the `%mdcList` converter. The converter class is not visible to Logback's classloader at parse time. Enable pattern override via `gravitee.yml` instead.
{% endhint %}

### Helm Chart Configuration

The Helm chart exposes `node.logging.*` properties under `api.node.logging.*` and `gateway.node.logging.*`.

**Node Logging Parameters**

| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `api.node.logging.mdc.format` | String | `"{key}: {value}"` | MDC key-value format |
| `api.node.logging.mdc.separator` | String | `" "` | MDC separator |
| `api.node.logging.mdc.nullValue` | String | `"-"` | Null value placeholder |
| `api.node.logging.mdc.include` | List<String> | `[nodeId, envId, apiId, appId]` | MDC keys to include |
| `api.node.logging.pattern.overrideLogbackXml` | Boolean | `false` | Override logback.xml patterns |
| `api.node.logging.pattern.console` | String | `%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n` | Console pattern |
| `api.node.logging.pattern.file` | String | `%d %-5p [%t] %c [%mdcList] : %m%n` | File pattern |

For complete Logback customization, use `api.logback.override` and `api.logback.content` to replace the entire `logback.xml` file.

**Deprecated Parameters**

The following parameters are deprecated. Use `api.logback.override` and `api.node.logging.*` instead:

| Deprecated Parameter | Replacement |
|:--------------------|:------------|
| `api.logging.debug` | `api.logback.override` + custom logback.xml |
| `api.logging.graviteeLevel` | Custom logback.xml |
| `api.logging.jettyLevel` | Custom logback.xml |
| `api.logging.stdout.encoderPattern` | `api.node.logging.pattern.console` |
| `api.logging.file.enabled` | Custom logback.xml |
| `api.logging.file.rollingPolicy` | Custom logback.xml |
| `api.logging.file.encoderPattern` | `api.node.logging.pattern.file` |
| `api.logging.additionalLoggers` | Custom logback.xml |

### MDC Key Renames in 4.0.0-alpha.2

The following MDC keys were renamed to shorter forms:

| Old Key | New Key |
|:--------|:--------|
| `api` | `apiId` |
| `environment` | `envId` |
| `organization` | `orgId` |
| `application` | `appId` |
| `plan` | `planId` |

Existing log queries that filter on the old key names must be updated.
