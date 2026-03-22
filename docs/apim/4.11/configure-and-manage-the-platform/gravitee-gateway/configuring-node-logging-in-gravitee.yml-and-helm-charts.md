# Configuring Node Logging in gravitee.yml and Helm Charts

## Prerequisites

- Gravitee or later (gravitee-node 8.0.0+, gravitee-gateway-api 5.0.0+)
- SLF4J-compatible logging backend (Logback recommended)
- For Helm deployments: Helm chart version supporting `logback.override` and `node.logging.*` values
- Write access to `gravitee.yml` or Helm values file

## Gateway Configuration

### Node Logging (gravitee.yml)

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `node.logging.mdc.format` | String | `"{key}: {value}"` | MDC key-value format pattern |
| `node.logging.mdc.separator` | String | `" "` | Separator between MDC entries |
| `node.logging.mdc.nullValue` | String | `"-"` | Value displayed when MDC entry is null |
| `node.logging.mdc.include` | List\<String\> | `["nodeId", "apiId"]` (Gateway)<br>`["nodeId", "envId", "apiId", "appId"]` (REST API) | MDC keys to include in log output |
| `node.logging.pattern.overrideLogbackXml` | Boolean | `true` | Override logback.xml patterns at runtime |
| `node.logging.pattern.console` | String | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` | Console log pattern when override enabled |
| `node.logging.pattern.file` | String | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` | File log pattern when override enabled |

### Helm Chart Values

**Gateway:**

| `gateway.logback.override` | Boolean | `false` | Use `gateway.logback.content` as complete logback.xml |
| `gateway.logback.content` | String | JSON-formatted config | Complete logback.xml content |
| `gateway.node.logging.mdc.format` | String | `"{key}: {value}"` | MDC key-value format |
| `gateway.node.logging.mdc.separator` | String | `" "` | MDC separator |
| `gateway.node.logging.mdc.nullValue` | String | `"-"` | Null value placeholder |
| `gateway.node.logging.mdc.include` | List\<String\> | `["nodeId", "apiId"]` | MDC keys to include |
| `gateway.node.logging.pattern.overrideLogbackXml` | Boolean | `false` | Override logback.xml patterns |
| `gateway.node.logging.pattern.console` | String | `"%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"` | Console pattern |
| `gateway.node.logging.pattern.file` | String | `"%d %-5p [%t] %c [%mdcList] : %m%n"` | File pattern |

**REST API:**

| `api.logback.override` | Boolean | `false` | Use `api.logback.content` as complete logback.xml |
| `api.logback.content` | String | JSON-formatted config | Complete logback.xml content |
| `api.node.logging.mdc.format` | String | `"{key}: {value}"` | MDC key-value format |
| `api.node.logging.mdc.separator` | String | `" "` | MDC separator |
| `api.node.logging.mdc.nullValue` | String | `"-"` | Null value placeholder |
| `api.node.logging.mdc.include` | List\<String\> | `["nodeId", "envId", "apiId", "appId"]` | MDC keys to include |
| `api.node.logging.pattern.overrideLogbackXml` | Boolean | `false` | Override logback.xml patterns |
| `api.node.logging.pattern.console` | String | `"%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"` | Console pattern |
| `api.node.logging.pattern.file` | String | `"%d %-5p [%t] %c [%mdcList] : %m%n"` | File pattern |

{% hint style="warning" %}
The following Helm properties are deprecated in favor of `logback.override` and `node.logging.*`:

- `api.logging.debug`
- `api.logging.graviteeLevel`
- `api.logging.jettyLevel`
- `api.logging.stdout.encoderPattern`
- `api.logging.file.enabled`
- `api.logging.file.rollingPolicy`
- `api.logging.file.encoderPattern`
- `api.logging.additionalLoggers`
- `gateway.logging.debug`
- `gateway.logging.graviteeLevel`
- `gateway.logging.jettyLevel`
- `gateway.logging.stdout.encoderPattern`
- `gateway.logging.file.enabled`
- `gateway.logging.file.rollingPolicy`
- `gateway.logging.file.encoderPattern`
- `gateway.logging.additionalLoggers`

Migrate to the new properties to ensure compatibility with future releases.
{% endhint %}

### Logback Pattern Configuration

The `%mdcList` conversion word formats MDC entries according to `node.logging.mdc.*` properties. Do NOT use `<conversionRule conversionWord="mdcList" converterClass="..."/>` in `logback.xml` — the class is not visible to Logback's classloader at parse time and will fail with `PARSER_ERROR[mdcList]`.

Example pattern:

```
%d{HH:mm:ss.SSS} [%thread] [%mdcList] %-5level %logger{36} - %msg%n
```

Example output:

```
14:32:01.123 [reactor-http-nio-2] [nodeId: gw-1 apiId: my-api] INFO i.g.gateway.MyHandler - Request processed
```

When `node.logging.pattern.overrideLogbackXml=true`, the system scans for `ConsoleAppender` and `RollingFileAppender` (including those nested in `AsyncAppender`) and replaces encoder patterns with values from `node.logging.pattern.console` and `node.logging.pattern.file`. This allows runtime pattern changes without modifying `logback.xml`.

{% hint style="info" %}
Pattern override is applied programmatically after Logback parses `logback.xml`. Some log entries generated during startup will use the default pattern from `logback.xml`. If the default pattern includes `%mdcList`, those entries will display an empty MDC section.
{% endhint %}

## Configuring MDC Filtering

Administrators control which MDC keys appear in logs by setting `node.logging.mdc.include` in `gravitee.yml` or Helm values. Gateway defaults to `["nodeId", "apiId"]`; REST API defaults to `["nodeId", "envId", "apiId", "appId"]`. Add or remove keys to match operational requirements (e.g., include `user` for audit trails, exclude `planId` to reduce log volume).

The `node.logging.mdc.format`, `node.logging.mdc.separator`, and `node.logging.mdc.nullValue` properties control how MDC entries are formatted in log output. For example, setting `format: "[{key}: {value}]"` and `separator: " "` produces output like `[nodeId: gw-1] [apiId: my-api]`.

### Available MDC Keys

**Node info (Gateway and REST API):**

- `nodeId`
- `nodeHostname`
- `nodeApplication`

**API (common keys, Gateway only):**

- `apiId`
- `apiName`
- `apiType`
- `envId`
- `orgId`
- `appId`
- `planId`
- `user`

**API (HTTP, MESSAGE, A2A, LLM, MCP, Gateway only):**

- `serverId`
- `contextPath`
- `requestMethod`

**API (TCP, Gateway only):**

- `serverId`
- `sni`

**API (Kafka Native, Gateway only):**

- `connectionId`
- `Principal`

**REST API additional keys:**

- `correlationId` (from `X-Correlation-ID` header)
- `traceParent` (from `traceparent` header)

{% hint style="info" %}
Not all plugins have been migrated to use context-aware logging. Some logs may lack contextual information. Full migration is planned for .
{% endhint %}

### ArchUnit Logging Rules

The `gravitee-archrules-maven-plugin` enforces two rules: (1) classes must not depend on `org.slf4j.LoggerFactory` (use `NodeLoggerFactory` instead), and (2) methods with an `ExecutionContext` parameter must call `ctx.withLogger(log)` before logging. Rules are configured per-project with package scans, exclusions, and allow-lists. CI/CD builds skip rule checks using `-Dgravitee.archrules.skip=true` to avoid blocking releases on legacy code violations.
