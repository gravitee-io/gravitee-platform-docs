# Implementing Context-Aware Logging and Build Validation

## Configuring MDC Logging

Configure MDC (Mapped Diagnostic Context) logging to enrich log entries with contextual metadata such as `nodeId`, `apiId`, and `appId`. This improves traceability and simplifies debugging by embedding key information directly into log lines.

### Configure MDC Formatting and Filtering

Edit the `gravitee.yml` configuration file to define how MDC values are formatted and which keys are included in log output.

**Management API**:

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
```

**Gateway**:

```yaml
node:
  logging:
    mdc:
      format: "{key}: {value}"
      separator: " "
      nullValue: "-"
      include:
        - nodeId
        - apiId
```

| Property | Description | Default |
|:---------|:------------|:--------|
| `node.logging.mdc.format` | Format pattern for MDC key-value pairs | `"{key}: {value}"` |
| `node.logging.mdc.separator` | Separator between MDC entries | `" "` |
| `node.logging.mdc.nullValue` | Placeholder when MDC value is null | `"-"` |
| `node.logging.mdc.include` | List of MDC keys to include in log output | `["nodeId", "apiId"]` (Gateway)<br>`["nodeId", "envId", "apiId", "appId"]` (Management API) |

### Override Log Patterns

Override the default console and file log patterns from `logback.xml` by enabling pattern override in `gravitee.yml`. Use the `%mdcList` converter to inject formatted MDC keys into log entries.

```yaml
node:
  logging:
    pattern:
      overrideLogbackXml: true
      console: "%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"
      file: "%d %-5p [%t] %c [%mdcList] : %m%n"
```

| Property | Description | Default |
|:---------|:------------|:--------|
| `node.logging.pattern.overrideLogbackXml` | Enable pattern override | `false` (Helm charts)<br>`true` (`gravitee.yml`) |
| `node.logging.pattern.console` | Console log pattern when override is enabled | `"%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"` |
| `node.logging.pattern.file` | File log pattern when override is enabled | `"%d %-5p [%t] %c [%mdcList] : %m%n"` |

### Helm Chart Configuration

Configure MDC logging via Helm chart parameters. The following parameters are available for both Management API (`api.node.logging`) and Gateway (`gateway.node.logging`).

**Management API**:

| Parameter | Description | Default |
|:---------|:------------|:--------|
| `api.node.logging.mdc.format` | MDC key-value format pattern | `"{key}: {value}"` |
| `api.node.logging.mdc.separator` | MDC separator | `" "` |
| `api.node.logging.mdc.nullValue` | Null value placeholder | `"-"` |
| `api.node.logging.mdc.include` | MDC keys for Management API | `["nodeId", "envId", "apiId", "appId"]` |
| `api.node.logging.pattern.overrideLogbackXml` | Enable pattern override for Management API | `false` |
| `api.node.logging.pattern.console` | Console pattern for Management API | `"%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"` |
| `api.node.logging.pattern.file` | File pattern for Management API | `"%d %-5p [%t] %c [%mdcList] : %m%n"` |

**Gateway**:

| Parameter | Description | Default |
|:---------|:------------|:--------|
| `gateway.node.logging.mdc.format` | MDC key-value format pattern | `"{key}: {value}"` |
| `gateway.node.logging.mdc.separator` | MDC separator | `" "` |
| `gateway.node.logging.mdc.nullValue` | Null value placeholder | `"-"` |
| `gateway.node.logging.mdc.include` | MDC keys for Gateway | `["nodeId", "apiId"]` |
| `gateway.node.logging.pattern.overrideLogbackXml` | Enable pattern override for Gateway | `false` |
| `gateway.node.logging.pattern.console` | Console pattern for Gateway | `"%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"` |
| `gateway.node.logging.pattern.file` | File pattern for Gateway | `"%d %-5p [%t] %c [%mdcList] : %m%n"` |

{% hint style="warning" %}
The following Helm parameters under `api.logging` and `gateway.logging` are deprecated. Use `api.logback.override` / `gateway.logback.override` with `api.logback.content` / `gateway.logback.content` for complete `logback.xml` replacement, or use `node.logging` properties for pattern-level control: `debug`, `graviteeLevel`, `jettyLevel`, `stdout.encoderPattern`, `file.enabled`, `file.rollingPolicy`, `file.encoderPattern`, `additionalLoggers`.
{% endhint %}

## Implementing Context-Aware Logging in Reactive Code

Integrate context-aware logging in reactive Gateway and Management API code to populate MDC with execution context metadata.

### Create Context-Aware Loggers

Replace direct logger calls with `ExecutionContext`-enriched calls to populate MDC with context metadata.

1. Obtain the `ExecutionContext` instance (typically named `ctx`).
2. Replace `log.info("message")` with `ctx.withLogger(log).info("message")`.
3. For deferred initialization, use `ExecutionContextLazyLogger.lazy(delegate, context, (ctx, log) -> new MyContextAwareLogger(ctx, log))` to create loggers only when the log level is enabled.
4. Verify MDC keys appear in log output by checking for patterns such as `[nodeId: xyz, apiId: abc]`.
5. Run `mvn verify` to ensure `execution-context-logging-check` passes without violations.

### Configure Lombok @CustomLog

Use Lombok's `@CustomLog` annotation with `NodeLoggerFactory` to ensure compliance with architecture rules.

1. Create a `lombok.config` file in the project root:

   ```properties
   lombok.log.custom.declaration = org.slf4j.Logger io.gravitee.node.logging.NodeLoggerFactory.getLogger(TYPE)
   config.stopBubbling = true
   ```

2. Annotate classes with `@CustomLog` instead of `@Slf4j`:

   ```java
   @CustomLog
   public class MyClass {
       public void myMethod() {
           log.info("Hello world"); // Uses NodeLoggerFactory
       }
   }
   ```

## Configuring Build-Time Architecture Validation

Add the `gravitee-archrules-maven-plugin` to enforce logging architecture rules at build time.

### Add Maven Plugin

Add the following configuration to the `<build><plugins>` section of `pom.xml`:

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

### Plugin Configuration Properties

| Property | Description | Example |
|:---------|:------------|:--------|
| `gravitee.archrules.skip` | Skip all ArchUnit checks (system property) | `-Dgravitee.archrules.skip=true` |
| `failOnError` | Fail build on rule violations | `true` |
| `allowListSuffixes` | Class name suffixes exempt from `global-logging-check` | `<suffix>ConfigurationEvaluator</suffix>` |

### Architecture Rules

**Global Logging Check** (`global-logging-check` goal):
- Fails build if classes use `org.slf4j.LoggerFactory` directly.
- Exempts classes ending with `ConfigurationEvaluator`.

**Execution Context Logging Check** (`execution-context-logging-check` goal):
- Fails build if methods with `ExecutionContext` parameter call `log.info()` directly instead of `ctx.withLogger(log).info()`.
- Scans packages: `io.gravitee.gateway.reactive.handlers..`, `io.gravitee.gateway.reactive.core..`, `io.gravitee.gateway.reactive.debug..`, `io.gravitee.apim.plugin..`, `io.gravitee.plugin.apiservice..`, `io.gravitee.plugin.entrypoint..`, `io.gravitee.plugin.endpoint..`.
- Excludes API packages: `io.gravitee.gateway.reactive.api..`, `io.gravitee.gateway.api..`.

## Available MDC Keys

The following MDC keys are available for logging configuration.

**Node Information** (Management API and Gateway):
- `nodeId`
- `nodeHostname`
- `nodeApplication`

**API Common Keys** (Gateway only):
- `apiId`
- `apiName`
- `apiType`
- `envId`
- `orgId`
- `appId`
- `planId`
- `user`

**API HTTP, MESSAGE, A2A, LLM, MCP** (Gateway only):
- `serverId`
- `contextPath`
- `requestMethod`

**API TCP** (Gateway only):
- `serverId`
- `sni`

**API Kafka Native** (Gateway only):
- `connectionId`
- `Principal`

## Restrictions

- The `%mdcList` converter cannot be used directly in `logback.xml`. It is registered programmatically and only functions when `node.logging.pattern.overrideLogbackXml` is enabled.
- `MdcListConverter` requires Logback 1.4+ due to supplier-based registration.
- MDC key names changed in `gravitee-gateway-api` 5.0.0: `environment` → `envId`, `organization` → `orgId`, `application` → `appId`, `plan` → `planId`.
- The `gravitee-node-archunit` module was removed. Use `gravitee-archrules-maven-plugin` instead.
- `execution-context-logging-check` scans only specific packages and excludes API packages.
- Classes ending with `ConfigurationEvaluator` are exempt from `global-logging-check` by default.
- Pattern override defaults to `true` in `gravitee.yml` but `false` in Helm charts.
- Some logs at startup may use the default `logback.xml` configuration before programmatic pattern override takes effect. If `%mdcList` is used, these early log entries will display an empty MDC list.
- JSON encoders such as `JsonEncoder` or `EcsEncoder` log the full MDC list without filtering. The `%mdcList` converter is only valid for pattern-based appenders.

## Verification

Verify MDC logging is configured correctly by checking log output for formatted MDC entries.

**Example log entry**:

```
15:44:17 INFO c.g.n.GraviteeNode [nodeId: node-1, apiId: my-api, appId: my-app] - Log message
```

If `node.logging.pattern.overrideLogbackXml` is disabled, verify MDC keys appear using individual placeholders such as `%X{nodeId}`.

## Related Changes

- Helm chart parameters under `api.logging` and `gateway.logging` are deprecated. Use `api.logback.override` / `gateway.logback.override` for complete `logback.xml` replacement or `node.logging` properties for pattern-level control.
- CircleCI Maven commands now include `-Dgravitee.archrules.skip=true` to avoid duplicate validation in build/deploy jobs.
- `gravitee-parent` POM version 24.0.0 integrates `gravitee-archrules-maven-plugin` 1.0.0-alpha.2 for all child projects.
- Dependency versions updated: `gravitee-node` to 8.0.0-alpha.15, `gravitee-gateway-api` to 5.0.0, `gravitee-reactor-native-kafka` to 6.0.0-alpha.7, and Hazelcast plugins to 8.0.0-alpha.2.
