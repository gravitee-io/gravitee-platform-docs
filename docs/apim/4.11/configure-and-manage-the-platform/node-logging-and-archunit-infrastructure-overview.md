# Node Logging and ArchUnit Infrastructure Overview

## Overview

Node Logging and ArchUnit Infrastructure provides centralized logging configuration and architecture validation for Gravitee Gateway and Management API components. It enables runtime MDC (Mapped Diagnostic Context) enrichment with execution context metadata and enforces logging best practices through automated build-time checks. This feature is designed for platform administrators configuring log output and developers integrating context-aware logging in reactive code.

## Key Concepts

### MDC Enrichment

MDC enrichment automatically injects contextual metadata (node ID, API ID, environment ID, organization ID, application ID, plan ID) into log entries. The `%mdcList` converter formats these key-value pairs according to configurable patterns. When a log source is unavailable, MDC keys are set to `"unknown"`. The system avoids double enrichment when delegate loggers are already context-aware.

### Context-Aware Logging

Context-aware logging defers logger initialization until the log level is enabled and enriches MDC with execution context metadata. In reactive code, use `ctx.withLogger(log).info("message")` instead of `log.info("message")` to ensure MDC population. The `ExecutionContextLazyLogger` pattern creates loggers only when needed, reducing overhead in high-throughput scenarios.

### Architecture Validation

Architecture validation enforces logging standards at build time using ArchUnit rules. The `global-logging-check` goal fails builds if classes use `org.slf4j.LoggerFactory` directly instead of `NodeLoggerFactory`. The `execution-context-logging-check` goal detects reactive methods that log without enriching MDC via `ExecutionContext`. Both checks run during the Maven `verify` phase and can be disabled with `-Dgravitee.archrules.skip=true`.

### Logback Pattern Override

Logback pattern override replaces patterns defined in `logback.xml` at runtime when `node.logging.pattern.overrideLogbackXml` is enabled. This allows centralized control of log formats without modifying XML files. The `%mdcList` converter cannot be used directly in `logback.xml` — it is registered programmatically by the node container and only functions when pattern override is active.

### MDC Key Renaming

MDC keys were shortened in version 5.0.0 of `gravitee-gateway-api`: `environment` → `envId`, `organization` → `orgId`, `application` → `appId`, `plan` → `planId`. Existing log parsers and dashboards must be updated to reference the new key names.

## Prerequisites

- Gravitee Gateway or Management API version supporting `gravitee-node` 8.0.0-alpha.15 or later
- Logback 1.4+ (required for `MdcListConverter` supplier-based registration)
- Maven 3.6+ (if using `gravitee-archrules-maven-plugin` for build-time validation)
- For Helm deployments: Helm chart version supporting `node.logging` configuration block

## Gateway Configuration

### Node Logging Properties

Configure in `gravitee.yml` under the `node.logging` section:

| Property | Description | Example |
|:---------|:------------|:--------|
| `node.logging.mdc.format` | Template for each MDC key-value pair | `"{key}: {value}"` |
| `node.logging.mdc.separator` | Delimiter between MDC entries | `" "` (space) or `", "` |
| `node.logging.mdc.nullValue` | Placeholder when MDC value is null | `"-"` or `"N/A"` |
| `node.logging.mdc.include` | List of MDC keys to include in output | `["nodeId", "apiId"]` (Gateway)<br>`["nodeId", "envId", "apiId", "appId"]` (Management API) |
| `node.logging.pattern.overrideLogbackXml` | Enable runtime pattern replacement | `true` |
| `node.logging.pattern.console` | Console log pattern when override is enabled | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` |
| `node.logging.pattern.file` | File log pattern when override is enabled | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` |

### Example Configuration

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

## Helm Chart Configuration

### Deprecated Parameters

The following Helm chart parameters are deprecated. Use `logback.override` and `node.logging` instead:

**Gateway**:
- `gateway.logging.debug`
- `gateway.logging.graviteeLevel`
- `gateway.logging.jettyLevel`
- `gateway.logging.stdout.encoderPattern`
- `gateway.logging.file.enabled`
- `gateway.logging.file.rollingPolicy`
- `gateway.logging.file.encoderPattern`
- `gateway.logging.additionalLoggers`

**Management API**:
- `api.logging.debug`
- `api.logging.graviteeLevel`
- `api.logging.jettyLevel`
- `api.logging.stdout.encoderPattern`
- `api.logging.file.enabled`
- `api.logging.file.rollingPolicy`
- `api.logging.file.encoderPattern`
- `api.logging.additionalLoggers`

### New Parameters

**Gateway**:
- `gateway.node.logging.mdc.format`
- `gateway.node.logging.mdc.separator`
- `gateway.node.logging.mdc.nullValue`
- `gateway.node.logging.mdc.include`
- `gateway.node.logging.pattern.overrideLogbackXml`
- `gateway.node.logging.pattern.console`
- `gateway.node.logging.pattern.file`

**Management API**:
- `api.node.logging.mdc.format`
- `api.node.logging.mdc.separator`
- `api.node.logging.mdc.nullValue`
- `api.node.logging.mdc.include`
- `api.node.logging.pattern.overrideLogbackXml`
- `api.node.logging.pattern.console`
- `api.node.logging.pattern.file`

## Maven Plugin Configuration

### ArchUnit Validation

Configure in `pom.xml`:

```xml
<plugin>
 <groupId>io.gravitee.maven.plugins</groupId>
 <artifactId>gravitee-archrules-maven-plugin</artifactId>
 <version>1.0.0-alpha.2</version>
 <executions>
 <execution>
 <id>global-logging-check</id>
 <phase>verify</phase>
 <goals>
 <goal>global-logging-check</goal>
 </goals>
 <configuration>
 <failOnError>true</failOnError>
 <allowListSuffixes>
 <suffix>ConfigurationEvaluator</suffix>
 </allowListSuffixes>
 </configuration>
 </execution>
 <execution>
 <id>execution-context-logging-check</id>
 <phase>verify</phase>
 <goals>
 <goal>execution-context-logging-check</goal>
 </goals>
 <configuration>
 <failOnError>true</failOnError>
 </configuration>
 </execution>
 </executions>
</plugin>
```

### Skipping Validation

To skip ArchUnit checks during build:

```bash
mvn clean install -Dgravitee.archrules.skip=true
```

## Developer Integration

### Lombok @CustomLog Integration

Configure in `lombok.config`:

```properties
config.stopBubbling = true
lombok.log.custom.declaration = org.slf4j.Logger io.gravitee.node.logging.NodeLoggerFactory.getLogger
```

Usage:

```java
@CustomLog
public class MyClass {
 public void myMethod() {
 log.info("Hello world"); // Uses NodeLoggerFactory
 }
}
```

### Context-Aware Logging Pattern

In reactive code:

```java
// Lazy initialization - logger is only created if log level is enabled
Logger logger = ExecutionContextLazyLogger.lazy(
 delegate,
 context,
 (ctx, log) -> new MyContextAwareLogger(ctx, log)
);

// In reactive code
ctx.withLogger(log).info("Request processed"); // Enriches MDC with context
```

## Verification

Logs display MDC content formatted within the log line at the location of `%mdcList`. Example output:

```
15:44:17 INFO c.g.n.GraviteeNode [apiId: my-api] [appId: my-app] - Log message
```

## Common Pitfalls

- **Missing `overrideLogbackXml: true`**: Pattern override will not take effect if this property is not enabled.
- **Default Pattern Change**: The default log pattern is modified when pattern override is enabled. To retain the previous default pattern, explicitly configure it in `gravitee.yml`.
- **Startup Logs**: Pattern override is applied programmatically after logback parses `logback.xml`. Some startup logs will use the default configuration. If `%mdcList` is used in `logback.xml`, it will display nothing.
- **JSON/ECS Encoders**: `%mdcList` is only valid for pattern-based appenders. Encoders such as `JsonEncoder` or `EcsEncoder` log the full MDC list without filtering.
- **Plugin Migration**: Not all plugins have been migrated to support MDC enrichment. Some logs may lack contextual information until migration is complete in version 4.12.
