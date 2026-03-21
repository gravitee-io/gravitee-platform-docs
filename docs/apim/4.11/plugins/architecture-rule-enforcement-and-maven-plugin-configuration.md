# Architecture Rule Enforcement and Maven Plugin Configuration

## End-User Configuration

### Lombok Integration

Add a `lombok.config` file to your project root with:

```properties
config.stopBubbling = true
lombok.log.custom.declaration = org.slf4j.Logger io.gravitee.node.logging.NodeLoggerFactory.getLogger(TYPE)
```

Use `@CustomLog` on classes instead of `@Slf4j` to inject a `NodeLoggerFactory`-based logger.

### ArchUnit Rule Customization

To allow specific classes to use `LoggerFactory` directly, configure the `gravitee-archrules-maven-plugin` in your `pom.xml`:

```xml
<plugin>
  <groupId>io.gravitee.maven.plugins</groupId>
  <artifactId>gravitee-archrules-maven-plugin</artifactId>
  <configuration>
    <allowListClasses>
      <class>io.gravitee.myproject.LegacyClass</class>
    </allowListClasses>
    <excludePackages>
      <package>io.gravitee.myproject.api..</package>
    </excludePackages>
  </configuration>
</plugin>
```

Classes ending with `ConfigurationEvaluator` are automatically allow-listed.

## Restrictions

- The `%mdcList` conversion word must NOT be registered manually in `logback.xml` via `<conversionRule>` — it is registered programmatically after bootstrap to avoid classloader conflicts in Docker deployments.
- Direct use of `org.slf4j.LoggerFactory` is prohibited by the global-logging-check rule; use `NodeLoggerFactory` or Lombok `@CustomLog` instead.
- Methods with an `ExecutionContext` parameter must use `ctx.withLogger(log)` instead of calling logger methods directly, enforced by the execution-context-logging-check rule.
- The execution-context-logging-check rule scans packages `io.gravitee.gateway.reactive.handlers..`, `io.gravitee.gateway.reactive.core..`, `io.gravitee.gateway.reactive.debug..`, `io.gravitee.apim.plugin..`, `io.gravitee.plugin.apiservice..`, `io.gravitee.plugin.entrypoint..`, `io.gravitee.plugin.endpoint..` and excludes `io.gravitee.gateway.reactive.api..`, `io.gravitee.gateway.api..`.
- The Lombok `@Slf4j` annotation check was removed in version 8.0.0-alpha.9; only `LoggerFactory` dependency checks remain.
- The `gravitee-node-archunit` module was removed in version 8.0.0-alpha.13; architecture rules are now enforced via the `gravitee-archrules-maven-plugin`.
