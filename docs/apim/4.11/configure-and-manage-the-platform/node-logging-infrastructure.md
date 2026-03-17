# Node Logging Infrastructure Concepts

## Overview

The Node Logging Infrastructure enriches Gravitee application logs with contextual metadata such as node identifiers, API details, and application information. Administrators can configure MDC filtering, format patterns, and log output directly in `gravitee.yml`, eliminating the need to modify `logback.xml` for common use cases. This feature is available from APIM 4.11 and improves traceability and debugging in production environments.

## Key Concepts

### Mapped Diagnostic Context (MDC)

MDC is a logging mechanism that attaches contextual key-value pairs to log statements. Gravitee automatically populates MDC with node and request-specific information when available. Administrators control which keys appear in logs using the `node.logging.mdc.include` property. Keys are formatted using the `%mdcList` conversion word in log patterns.

#### MDC Key Reference

| MDC Key | Source | Description |
|:--------|:-------|:------------|
| `nodeId` | Node | Unique node identifier |
| `nodeHostname` | Node | Node hostname |
| `nodeApplication` | Node | Application name (e.g., `gio_apim_gateway`) |
| `apiId` | Gateway | API identifier |
| `apiName` | Gateway | API name |
| `apiType` | Gateway | API type (v2, v4, etc.) |
| `envId` | Gateway | Environment identifier |
| `orgId` | Gateway | Organization identifier |
| `appId` | Gateway | Application identifier |
| `planId` | Gateway | Plan identifier |
| `user` | Gateway | User identifier |
| `serverId` | Gateway (HTTP/MESSAGE/A2A/LLM/MCP) | Server identifier |
| `contextPath` | Gateway (HTTP/MESSAGE/A2A/LLM/MCP) | Request context path |
| `requestMethod` | Gateway (HTTP/MESSAGE/A2A/LLM/MCP) | HTTP request method |
| `sni` | Gateway (TCP) | Server Name Indication |
| `connectionId` | Gateway (Kafka Native) | Connection identifier |
| `Principal` | Gateway (Kafka Native) | Kafka principal |
| `correlationId` | HTTP Header | `X-Correlation-ID` header value |
| `traceParent` | HTTP Header | `traceparent` header value |

{% hint style="info" %}
MDC keys are populated only when the corresponding information is available. If a key is not available, the value specified in `node.logging.mdc.nullValue` is used (default: `"-"`). When a log source is not available for a registered key, the MDC value is set to `"unknown"`.
{% endhint %}

### Pattern Override

Pattern override allows administrators to replace the default console and file log patterns defined in `logback.xml` at runtime. When `node.logging.pattern.overrideLogbackXml` is set to `true`, Gravitee applies the patterns specified in `gravitee.yml` to the STDOUT and FILE appenders. This feature uses the `%mdcList` conversion word to inject filtered and formatted MDC entries into log lines.

{% hint style="warning" %}
Pattern override is applied programmatically after logback parses `logback.xml`. Logs emitted during early startup use the default patterns from `logback.xml`. If `%mdcList` is used in the override pattern, early startup logs will display an empty MDC section.
{% endhint %}

### Custom Conversion Word: `%mdcList`

The `%mdcList` conversion word formats and filters MDC entries based on the `node.logging.mdc.include` configuration. It replaces manual `%X{key}` references with a single, configurable placeholder. The converter is registered programmatically after logback parses `logback.xml`.

**Example pattern:**

```
%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n
```

**Example output:**

```
10:15:30.123 INFO  i.g.gateway.MyClass [nodeId: gw-1 apiId: my-api] - Processing request
```

{% hint style="danger" %}
Do NOT declare `<conversionRule conversionWord="mdcList" .../>` in `logback.xml`. The converter class is not visible at parse time and will cause a `PARSER_ERROR[mdcList]` failure.
{% endhint %}

{% hint style="info" %}
The `%mdcList` conversion word is only valid for pattern-based appenders. JSON encoders (e.g., `JsonEncoder`, `EcsEncoder`) log the full MDC list without filtering.
{% endhint %}

## Prerequisites

- Gravitee APIM 4.11 or later
- Write access to `gravitee.yml` (or equivalent Helm chart values)
- For Helm deployments: Gravitee Helm chart version supporting `node.logging` configuration

## Management API Configuration

The Management API uses the same configuration structure as the Gateway. The default `node.logging.mdc.include` list for the Management API is `[nodeId, envId, apiId, appId]`.

**Example configuration:**

```yaml
node:
  logging:
    mdc:
      format: "{key}: {value}"
      separator: " "
      nullValue: "-"
      include:
        - nodeId
        - envId
        - apiId
        - appId
    pattern:
      overrideLogbackXml: true
      console: "%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"
      file: "%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"
```

## Verification

After applying the configuration, verify that MDC keys appear in log output.

**Example log output:**

```
15:44:17.123 INFO  c.g.n.GraviteeNode [nodeId: gw-1] [apiId: my-api] [appId: my-app] - Log message
```

If `%mdcList` is used in the pattern, the MDC content is formatted according to the `node.logging.mdc.format` and `node.logging.mdc.separator` properties. If a key is not available, the value specified in `node.logging.mdc.nullValue` is displayed.

## Restrictions and Known Limitations

- **Plugin migration status**: Not all Gravitee plugins have been migrated to populate MDC keys. Some logs may lack contextual information. Full migration is planned for APIM 4.12.
- **Early startup logs**: Logs emitted during early startup (before pattern override is applied) use the default patterns from `logback.xml`. If `%mdcList` is used in the override pattern, early startup logs will display an empty MDC section.
- **JSON encoder behavior**: The `%mdcList` conversion word is only valid for pattern-based appenders. JSON encoders (e.g., `JsonEncoder`, `EcsEncoder`) log the full MDC list without filtering.
- **Logback.xml converter registration**: Do NOT declare `<conversionRule conversionWord="mdcList" .../>` in `logback.xml`. The converter class is not visible at parse time and will cause a `PARSER_ERROR[mdcList]` failure.

## Related Changes

- **Millisecond timestamps**: Default log patterns now include milliseconds (`.SSS`) in the timestamp format for both console and file appenders.
- **Deprecated Helm parameters**: Old logging configuration parameters (`gateway.logging.*`, `api.logging.*`) are deprecated. Use `logback.override` and `node.logging` configuration instead.
- **Management API MDC population**: The Management API now populates MDC keys extracted from request path segments (e.g., `apiId` from `/apis/{apiId}/...`, `appId` from `/applications/{appId}/...`).
- **ArchUnit rules enforcement**: ArchUnit rules enforce the use of `NodeLoggerFactory` instead of direct SLF4J `LoggerFactory` usage. Methods with an `ExecutionContext` parameter must use `ctx.withLogger(log)` instead of calling `Logger.info()` directly.
