# Node Logging Configuration Reference

## Prerequisites

- Gravitee APIM 4.11 or later
- Write access to `gravitee.yml` (or equivalent Helm chart values)
- For Helm deployments: Gravitee Helm chart version supporting `node.logging` configuration

## Gateway Configuration

### MDC Filtering and Formatting

Configure MDC key inclusion, formatting, and null value handling in the `node.logging.mdc` section of `gravitee.yml`.

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `node.logging.mdc.format` | String | `"{key}: {value}"` | Format pattern for MDC key-value pairs |
| `node.logging.mdc.separator` | String | `" "` (space) | Separator between MDC entries |
| `node.logging.mdc.nullValue` | String | `"-"` | Value displayed when MDC entry is null |
| `node.logging.mdc.include` | List\<String> | `[nodeId, apiId]` (Gateway)<br>`[nodeId, envId, apiId, appId]` (Management API) | MDC keys to include in log output |

**Example configuration:**

```yaml
node:
  logging:
    mdc:
      format: "[{key}: {value}]"
      separator: " "
      nullValue: "-"
      include:
        - nodeId
        - apiId
        - appId
        - planId
```

### Log Pattern Override

Override the default console and file log patterns defined in `logback.xml` using the `node.logging.pattern` section.

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `node.logging.pattern.overrideLogbackXml` | Boolean | `true` | Whether to override logback.xml patterns at runtime |
| `node.logging.pattern.console` | String | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` | Console appender pattern when override is enabled |
| `node.logging.pattern.file` | String | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` | File appender pattern when override is enabled |

**Example configuration:**

```yaml
node:
  logging:
    pattern:
      overrideLogbackXml: true
      console: "%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"
      file: "%d{HH:mm:ss.SSS} [%thread] [%mdcList] %-5level %logger{36} - %msg%n"
```

### Helm Chart Configuration

Use the `api.node.logging` and `gateway.node.logging` sections in Helm chart values to configure MDC and pattern overrides.

| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `api.node.logging.mdc.format` | String | `"{key}: {value}"` | MDC format pattern |
| `api.node.logging.mdc.separator` | String | `" "` | MDC separator |
| `api.node.logging.mdc.nullValue` | String | `"-"` | MDC null value |
| `api.node.logging.mdc.include` | List\<String> | `[nodeId, envId, apiId, appId]` | MDC keys to include |
| `api.node.logging.pattern.overrideLogbackXml` | Boolean | `false` | Override logback patterns |
| `api.node.logging.pattern.console` | String | `"%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"` | Console pattern |
| `api.node.logging.pattern.file` | String | `"%d %-5p [%t] %c [%mdcList] : %m%n"` | File pattern |

Gateway parameters follow the same structure with the `gateway.` prefix.

**Example Helm values:**

```yaml
api:
  node:
    logging:
      mdc:
        include:
          - nodeId
          - apiId
          - appId
      pattern:
        overrideLogbackXml: true
        console: "%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"
```

## Available MDC Keys

The following MDC keys are available for logging configuration:

**Node information (Management API and Gateway):**

- `nodeId`
- `nodeHostname`
- `nodeApplication`

**API information (Gateway only):**

- `apiId`
- `apiName`
- `apiType`
- `envId`
- `orgId`
- `appId`
- `planId`
- `user`

**HTTP, MESSAGE, A2A, LLM, MCP APIs (Gateway only):**

- `serverId`
- `contextPath`
- `requestMethod`

**TCP APIs (Gateway only):**

- `serverId`
- `sni`

**Kafka Native APIs (Gateway only):**

- `connectionId`
- `principal`

{% hint style="info" %}
Not all plugins have been migrated to support MDC enrichment. Some logs may lack contextual information. Full plugin migration is planned for APIM 4.12.
{% endhint %}
