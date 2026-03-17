# Node Logging Infrastructure Configuration Reference

## Overview

The Node Logging Infrastructure enriches Gravitee application logs with contextual metadata (MDC keys) such as node identifiers, API details, and application information, enabling better traceability and simplified debugging in production environments. Administrators configure MDC filtering and log pattern overrides via `gravitee.yml`, eliminating the need to manually edit `logback.xml`. Available from APIM 4.11.

## Key Concepts

### MDC (Mapped Diagnostic Context)

MDC is a thread-local key-value store that attaches contextual information to log entries. Gravitee automatically populates MDC with identifiers like `nodeId`, `apiId`, `appId`, and `planId` when available. The `node.logging.mdc.include` property filters which keys appear in logs, and the `%mdcList` conversion word formats them according to configured patterns. MDC keys are cached per execution context to avoid repeated reflection overhead.

### Pattern Override

Pattern override replaces encoder patterns in `logback.xml` at runtime without modifying the file. When `node.logging.pattern.overrideLogbackXml` is enabled, Gravitee scans for `ConsoleAppender` and `RollingFileAppender` instances and applies the patterns defined in `gravitee.yml`. This mechanism wraps file appenders in `AsyncAppender` if not already async. Patterns use the `%mdcList` keyword to inject filtered MDC content.

### Context-Aware Logging

In reactive code paths, direct logger calls bypass execution context. The `ctx.withLogger(log)` pattern wraps the logger in a context-aware proxy that automatically populates MDC from the `ExecutionContext` before each log statement. This ensures API, application, and plan identifiers appear in logs even when processing asynchronous requests.

## Prerequisites

- APIM 4.11 or later
- Write access to `gravitee.yml` (or equivalent Helm chart values)

## Gateway Configuration

### MDC Filtering

| Property | Description | Example |
|:---------|:------------|:--------|
| `node.logging.mdc.format` | Template for each MDC key-value pair | `"[{key}: {value}]"` |
| `node.logging.mdc.separator` | Delimiter between MDC entries | `" "` (space) |
| `node.logging.mdc.nullValue` | Placeholder when MDC value is missing | `"-"` |
| `node.logging.mdc.include` | List of MDC keys to include in `%mdcList` output | `[nodeId, apiId, appId]` |

### Pattern Override

| Property | Description | Example |
|:---------|:------------|:--------|
| `node.logging.pattern.overrideLogbackXml` | Enable runtime pattern replacement | `true` |
| `node.logging.pattern.console` | Console appender pattern (when override enabled) | `"%d{HH:mm:ss} %-5level %logger{36} %mdcList - %msg%n"` |
| `node.logging.pattern.file` | File appender pattern (when override enabled) | `"%d %-5p [%t] %c %mdcList : %m%n"` |

### Helm Chart Logback Override

| Property | Description | Example |
|:---------|:------------|:--------|
| `gateway.logback.override` | Replace entire `logback.xml` with custom content | `false` |
| `gateway.logback.content` | Complete logback.xml configuration (JSON-formatted) | See Helm chart documentation |
| `api.logback.override` | Replace entire `logback.xml` for Management API | `false` |
| `api.logback.content` | Complete logback.xml configuration for Management API | See Helm chart documentation |

## Configuring MDC Filtering and Pattern Override

To enable rich logging, modify `gravitee.yml` to define which MDC keys appear in logs and how they are formatted. (1) Add the `node.logging.mdc` section and specify the `include` list with keys relevant to your deployment (e.g., `nodeId`, `apiId`, `appId`, `planId`). (2) Set `node.logging.pattern.overrideLogbackXml: true` to enable runtime pattern replacement. (3) Define `console` and `file` patterns using the `%mdcList` keyword to inject filtered MDC content. Example configuration:

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
    pattern:
      overrideLogbackXml: true
      console: "%d{HH:mm:ss} %-5level %logger{36} %mdcList - %msg%n"
      file: "%d %-5p [%t] %c %mdcList : %m%n"
```

After restarting the Gateway or Management API, logs will display filtered MDC keys in the configured format (e.g., `15:44:17 INFO c.g.n.GraviteeNode [nodeId: node-1] [apiId: my-api] - Log message`).

## Overriding Logback Configuration via Helm

For Kubernetes deployments, use the `logback.override` mechanism to replace the entire `logback.xml` file. (1) Set `gateway.logback.override: true` in your Helm values. (2) Provide the complete logback configuration in `gateway.logback.content` as a JSON-formatted string. (3) Deploy the Helm chart. This approach is useful when you need custom appenders or encoders beyond pattern overrides. Note that `logback.override` supersedes deprecated properties like `gateway.logging.debug`, `gateway.logging.graviteeLevel`, and `gateway.logging.stdout.encoderPattern`.

## Available MDC Keys

### Node Information (Gateway and Management API)

| Key | Description |
|:----|:------------|
| `nodeId` | Unique node identifier |
| `nodeHostname` | Node hostname |
| `nodeApplication` | Application name (e.g., `gio_apim_gateway`) |

### API Context (Gateway Only)

| Key | Description | Caching |
|:----|:------------|:--------|
| `apiId` | API identifier | Cached |
| `apiName` | API name | Cached |
| `apiType` | API type (v2/v4) | Cached |
| `envId` | Environment identifier | Cached |
| `orgId` | Organization identifier | Cached |
| `appId` | Application identifier | Refreshable per request |
| `planId` | Plan identifier | Refreshable per request |
| `user` | User identifier | Refreshable per request |

### Protocol-Specific Keys (Gateway Only)

#### HTTP, MESSAGE, A2A, LLM, MCP APIs

| Key | Description |
|:----|:------------|
| `serverId` | Server identifier |
| `contextPath` | API context path |
| `requestMethod` | HTTP request method |

#### TCP APIs

| Key | Description |
|:----|:------------|
| `serverId` | Server identifier |
| `sni` | Server Name Indication |

#### Kafka Native APIs

| Key | Description |
|:----|:------------|
| `connectionId` | Connection identifier |
| `Principal` | Kafka principal |

### Management API Additional Keys

| Key | Description |
|:----|:------------|
| `correlationId` | Request correlation ID (from `X-Correlation-ID` header) |
| `traceParent` | W3C trace context (from `traceparent` header) |
| `apiId` | API ID extracted from URL path |
| `appId` | Application ID extracted from URL path |

## Verification

After configuration, verify that MDC keys appear in logs. Example log entry with `nodeId` and `apiId` configured in `include`:

If `%mdcList` is empty or missing, check that `node.logging.pattern.overrideLogbackXml` is enabled and that the specified keys exist in the execution context.

## Restrictions and Known Limitations

- **%mdcList in logback.xml**: The `%mdcList` conversion word cannot be declared directly in `logback.xml` using `<conversionRule>` due to classloader visibility. Use pattern override via `gravitee.yml` instead.
- **Startup logs**: Logs generated during application startup use the default patterns defined in `logback.xml`. Pattern override applies only after the Gravitee node initializes.
- **JSON and ECS encoders**: Encoders such as `JsonEncoder` or `EcsEncoder` log the full MDC map without filtering. Use pattern-based encoders to apply MDC filtering.
- **Plugin migration**: Not all Gravitee plugins have been migrated to populate MDC keys in APIM 4.11. Some logs may lack contextual information. Full migration is planned for APIM 4.12.

## Next Steps

For Kubernetes deployments, see the Helm chart documentation for advanced logback configuration options. For developers implementing context-aware logging in reactive code, refer to the developer guide for usage of `ctx.withLogger(log)` and `ExecutionContextLazyLogger`.
