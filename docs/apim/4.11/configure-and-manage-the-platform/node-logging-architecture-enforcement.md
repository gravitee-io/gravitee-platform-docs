# Node Logging & Architecture Enforcement

## Overview

Gravitee Node Logging & Architecture Enforcement provides centralized logging infrastructure with MDC (Mapped Diagnostic Context) enrichment and compile-time architecture rules for API Gateway and Management API components. It enables context-aware logging that automatically includes request metadata (API ID, environment, organization, plan) and enforces consistent logging patterns across the platform through ArchUnit-based Maven plugin checks.

## Key Concepts

### Context-Aware Logging

Gravitee replaces standard SLF4J loggers with `NodeLoggerFactory` loggers that automatically populate MDC with request context. When an `ExecutionContext` is available, use `ctx.withLogger(log)` to inject API ID, environment ID, organization ID, application ID, plan ID, and user information into log entries. The lazy logger pattern defers context-aware logger instantiation until a log statement executes and the log level is enabled, avoiding overhead when logging is disabled.

| Component | Logger Factory | Context Method |
|:----------|:---------------|:---------------|
| Node-level | `NodeLoggerFactory.getLogger(Class)` | N/A (node metadata only) |
| Gateway/Management API | `NodeLoggerFactory.getLogger(Class)` | `ctx.withLogger(log)` |

### MDC Filtering and Formatting

The `%mdcList` conversion word renders selected MDC entries in log patterns. Configure which keys appear via `node.logging.mdc.include`, and control formatting with `mdc.format` (key-value template), `mdc.separator` (delimiter between entries), and `mdc.nullValue` (placeholder for missing values). Missing log sources populate MDC with `"unknown"` instead of being omitted.

| MDC Key | Source | Cached | Description |
|:--------|:-------|:-------|:------------|
| `nodeId` | `Node.id()` | Yes | Unique node identifier |
| `apiId` | `ATTR_API` | Yes | API identifier |
| `envId` | `ATTR_ENVIRONMENT` | Yes | Environment ID (renamed from `environment`) |
| `orgId` | `ATTR_ORGANIZATION` | Yes | Organization ID (renamed from `organization`) |
| `appId` | `ATTR_APPLICATION` | No | Application ID (renamed from `application`) |
| `planId` | `ATTR_PLAN` | No | Plan ID (renamed from `plan`) |

### Architecture Rules Enforcement

The `gravitee-archrules-maven-plugin` enforces logging patterns at compile time using ArchUnit. Rules prohibit direct use of `org.slf4j.LoggerFactory` in configured packages (must use `NodeLoggerFactory` instead) and require methods with `ExecutionContext` parameters to call `ctx.withLogger(log)` instead of logging directly. Exclude packages via `excludePackagesFromScan()` or exempt specific classes with `allowIn()` or `allowListSuffixes` (e.g., `*ConfigurationEvaluator`).

## Prerequisites

- Gravitee Node 8.0.0-alpha.2 or later
- Gravitee Gateway API 5.0.0-alpha.6 or later (for ExecutionContext logging)
- Gravitee Parent 24.0.0-alpha.1 or later (for ArchUnit plugin)
- Maven 3.6+ (for architecture rule enforcement)
- Logback 1.2+ (for `%mdcList` converter)

## Gateway Configuration

### Node Logging Properties

Configure MDC filtering and pattern overrides in `gravitee.yml`:

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `node.logging.mdc.format` | String | `"{key}: {value}"` | MDC key-value format pattern |
| `node.logging.mdc.separator` | String | `" "` | Separator between MDC entries |
| `node.logging.mdc.nullValue` | String | `"-"` | Value displayed when MDC entry is null |
| `node.logging.mdc.include` | List<String> | `["nodeId", "apiId"]` (Gateway)<br>`["nodeId", "envId", "apiId", "appId"]` (Management API) | MDC keys to include in log output |
| `node.logging.pattern.overrideLogbackXml` | Boolean | `true` | Override logback.xml patterns at runtime |
| `node.logging.pattern.console` | String | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` | Console appender pattern when override enabled |
| `node.logging.pattern.file` | String | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` | File appender pattern when override enabled |

### Helm Chart Configuration

#### Gateway Component

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `gateway.logback.override` | Boolean | `false` | Use `gateway.logback.content` as complete logback.xml |
| `gateway.logback.content` | String | JSON-formatted async logback config | Complete logback.xml content when override is true |
| `gateway.node.logging.mdc.format` | String | `"{key}: {value}"` | MDC key-value format pattern |
| `gateway.node.logging.mdc.separator` | String | `" "` | MDC entries separator |
| `gateway.node.logging.mdc.nullValue` | String | `"-"` | Value when MDC entry is null |
| `gateway.node.logging.mdc.include` | List<String> | `["nodeId", "apiId"]` | MDC keys to include |
| `gateway.node.logging.pattern.overrideLogbackXml` | Boolean | `false` | Override logback.xml patterns at runtime |
| `gateway.node.logging.pattern.console` | String | `"%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"` | Console pattern when override enabled |
| `gateway.node.logging.pattern.file` | String | `"%d %-5p [%t] %c [%mdcList] : %m%n"` | File pattern when override enabled |

#### Management API Component

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `api.logback.override` | Boolean | `false` | Use `api.logback.content` as complete logback.xml |
| `api.logback.content` | String | JSON-formatted logback config | Complete logback.xml content when override is true |
| `api.node.logging.mdc.format` | String | `"{key}: {value}"` | MDC key-value format pattern |
| `api.node.logging.mdc.separator` | String | `" "` | MDC entries separator |
| `api.node.logging.mdc.nullValue` | String | `"-"` | Value when MDC entry is null |
| `api.node.logging.mdc.include` | List<String> | `["nodeId", "envId", "apiId", "appId"]` | MDC keys to include |
| `api.node.logging.pattern.overrideLogbackXml` | Boolean | `false` | Override logback.xml patterns at runtime |
| `api.node.logging.pattern.console` | String | `"%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"` | Console pattern when override enabled |
| `api.node.logging.pattern.file` | String | `"%d %-5p [%t] %c [%mdcList] : %m%n"` | File pattern when override enabled |

### Maven Plugin Configuration

Add to `pom.xml` to enforce architecture rules:

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `gravitee.archrules.skip` | Boolean | `false` | Skip all ArchUnit rule checks |

## Creating Context-Aware Logs

1. Obtain a logger via `NodeLoggerFactory.getLogger(MyClass.class)` or use Lombok `@CustomLog` annotation (requires `lombok.config` with `lombok.log.custom.declaration = org.slf4j.Logger io.gravitee.node.logging.NodeLoggerFactory.getLogger(TYPE)`).
2. In methods with an `ExecutionContext` parameter, wrap the logger with `ctx.withLogger(log)` before calling log methods.
3. Use the wrapped logger for all log statements: `ctx.withLogger(log).info("Processing request")`.
4. Configure `node.logging.mdc.include` in `gravitee.yml` to control which MDC keys appear in output.
5. Use `%mdcList` in log patterns to render filtered MDC entries.

## Configuring MDC Output

1. Set `node.logging.mdc.include` to a list of MDC keys (e.g., `["nodeId", "apiId", "envId"]`) to filter which entries appear in logs.
2. Customize `node.logging.mdc.format` to control key-value rendering (default: `"{key}: {value}"`).
3. Set `node.logging.mdc.separator` to define the delimiter between entries (default: space).
4. Configure `node.logging.mdc.nullValue` to specify the placeholder for missing values (default: `"-"`).
5. Enable `node.logging.pattern.overrideLogbackXml: true` to apply `pattern.console` and `pattern.file` settings at runtime, overriding `logback.xml`.

Example output with default settings: `nodeId: gw-1 apiId: my-api envId: prod`.

## End-User Configuration

### Lombok Integration

Create [`lombok.config`](https://projectlombok.org/features/configuration) in the repository root to enable `@CustomLog` annotation:

```
config.stopBubbling = true
lombok.log.custom.declaration = org.slf4j.Logger io.gravitee.node.logging.NodeLoggerFactory.getLogger(TYPE)
```

Use `@CustomLog` on classes to inject `NodeLoggerFactory` loggers instead of SLF4J's `LoggerFactory`.

### Logback Pattern Conversion

The `%mdcList` conversion word is registered automatically via `PatternLayout.DEFAULT_CONVERTER_SUPPLIER_MAP`.

## Restrictions

- `%mdcList` converter requires pattern override via `gravitee.yml` (`node.logging.pattern.overrideLogbackXml: true`) — direct `<conversionRule>` registration in `logback.xml` fails due to classloader visibility
- Pattern override defaults to `true` in Gravitee Node 8.0.0-alpha.15+ — set `overrideLogbackXml: false` explicitly to use `logback.xml` patterns
- Architecture rules apply only to packages configured in `gravitee-archrules-maven-plugin` — excluded packages bypass enforcement
- Lombok `@Slf4j` annotation is not checked by architecture rules (removed in gravitee-node#489)
- Lazy logger instantiation occurs only when log level is enabled — level checks delegate to base logger without context overhead
- Execution context hierarchy caching uses concrete class as key — subclasses with identical hierarchies share cache entries
- MDC keys renamed in gravitee-gateway-api#328: `environment` → `envId`, `organization` → `orgId`, `application` → `appId`, `plan` → `planId`
- Deprecated Helm chart parameters (`*.logging.debug`, `*.logging.graviteeLevel`, `*.logging.stdout.encoderPattern`, etc.) replaced by `*.logback.override` and `*.node.logging.*` properties
- CI/CD pipelines must use `-Dgravitee.archrules.skip=true` for packaging/deployment, `-Dgravitee.archrules.skip=false` for build jobs

## Related Changes

Default log patterns now include milliseconds (`.SSS`) for improved precision. The `%mdcList` converter registration switched from `DEFAULT_CONVERTER_MAP` to `DEFAULT_CONVERTER_SUPPLIER_MAP` to avoid classloader resolution failures in standalone Docker deployments. Execution context hierarchy collection is cached per class to reduce reflection overhead during log source registration. Management API includes additional MDC keys (`correlationId` from `X-Correlation-ID` header, `traceParent` from W3C trace context). New context attributes added: `ATTR_SNI` (Server Name Indication from TLS handshake) and `ATTR_INTERNAL_SERVER_ID` (server ID for current request). Helm chart deprecates legacy `*.logging.*` parameters in favor of `*.logback.override` and `*.node.logging.*` configuration.
