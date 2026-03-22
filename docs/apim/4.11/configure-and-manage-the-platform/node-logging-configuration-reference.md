# Node Logging Configuration Reference

## Node Logging Configuration

Configure node logging properties in `gravitee.yml` to control MDC formatting, pattern override, and log output. These properties apply to both Gateway and Management API components.

### gravitee.yml Properties

| Property | Description | Example |
|:---------|:------------|:--------|
| `node.logging.mdc.format` | Template for each MDC key-value pair | `"{key}: {value}"` |
| `node.logging.mdc.separator` | Delimiter between MDC entries | `" "` (space) or `", "` |
| `node.logging.mdc.nullValue` | Placeholder when MDC value is null | `"-"` or `"N/A"` |
| `node.logging.mdc.include` | List of MDC keys to include in output | `["nodeId", "apiId"]` (Gateway)<br>`["nodeId", "envId", "apiId", "appId"]` (Management API) |
| `node.logging.pattern.overrideLogbackXml` | Enable runtime pattern replacement | `true` (default in gravitee.yml) |
| `node.logging.pattern.console` | Console log pattern when override enabled | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` |
| `node.logging.pattern.file` | File log pattern when override enabled | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` |

### Helm Chart Parameters

Configure in `values.yaml` under `api.node.logging` or `gateway.node.logging`:

| Parameter | Description | Example |
|:---------|:------------|:--------|
| `api.node.logging.mdc.format` | MDC key-value format for Management API | `"{key}: {value}"` |
| `api.node.logging.mdc.separator` | MDC separator for Management API | `" "` |
| `api.node.logging.mdc.nullValue` | Null value placeholder for Management API | `"-"` |
| `api.node.logging.mdc.include` | MDC keys for Management API | `["nodeId", "envId", "apiId", "appId"]` |
| `api.node.logging.pattern.overrideLogbackXml` | Enable pattern override for Management API | `false` (default in Helm) |
| `api.node.logging.pattern.console` | Console pattern for Management API | `"%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"` |
| `api.node.logging.pattern.file` | File pattern for Management API | `"%d %-5p [%t] %c [%mdcList] : %m%n"` |
| `gateway.node.logging.mdc.format` | MDC key-value format for Gateway | `"{key}: {value}"` |
| `gateway.node.logging.mdc.separator` | MDC separator for Gateway | `" "` |
| `gateway.node.logging.mdc.nullValue` | Null value placeholder for Gateway | `"-"` |
| `gateway.node.logging.mdc.include` | MDC keys for Gateway | `["nodeId", "apiId"]` |
| `gateway.node.logging.pattern.overrideLogbackXml` | Enable pattern override for Gateway | `false` (default in Helm) |
| `gateway.node.logging.pattern.console` | Console pattern for Gateway | `"%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"` |
| `gateway.node.logging.pattern.file` | File pattern for Gateway | `"%d %-5p [%t] %c [%mdcList] : %m%n"` |

{% hint style="warning" %}
The default value for `node.logging.pattern.overrideLogbackXml` differs between gravitee.yml (`true`) and Helm charts (`false`).
{% endhint %}

### Deprecated Helm Parameters

The following parameters under `api.logging` and `gateway.logging` are deprecated. Use `api.logback.override` / `gateway.logback.override` with `api.logback.content` / `gateway.logback.content` for complete logback.xml replacement, or use `node.logging` properties for pattern-level control:

* `debug`
* `graviteeLevel`
* `jettyLevel`
* `stdout.encoderPattern`
* `file.enabled`
* `file.rollingPolicy`
* `file.encoderPattern`
* `additionalLoggers`

## Logback Pattern Override

Logback pattern override replaces patterns defined in `logback.xml` at runtime when `node.logging.pattern.overrideLogbackXml` is enabled. This allows centralized control of log formats without modifying XML files. The `%mdcList` converter cannot be used directly in `logback.xml` — it is registered programmatically by the node container and only functions when pattern override is active.

## MDC Key Renaming

MDC keys were shortened in version 5.0.0 of `gravitee-gateway-api`: `environment` → `envId`, `organization` → `orgId`, `application` → `appId`, `plan` → `planId`. Existing log parsers and dashboards must be updated to reference the new key names.

## Maven Plugin Configuration

Add to `pom.xml` in the `<build><plugins>` section:

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

| Property | Description | Example |
|:---------|:------------|:--------|
| `failOnError` | Fail build if architecture rules are violated | `true` |
| `allowListSuffixes` | Class name suffixes exempt from global logging check | `<suffix>ConfigurationEvaluator</suffix>` |
| `gravitee.archrules.skip` | Skip all ArchUnit architecture rule checks | `-Dgravitee.archrules.skip=true` |
