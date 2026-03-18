# Enabling Context-Aware Logging in Code

## Enabling Context-Aware Logging in Code

Integrate the `@CustomLog` annotation and `NodeLoggerFactory` into your modules to enable node-aware logging with automatic MDC enrichment.

### Configure lombok.config

Add the following configuration to `lombok.config` in your module:

```properties
config.stopBubbling = true
lombok.log.custom.declaration = org.slf4j.Logger io.gravitee.node.logging.NodeLoggerFactory.getLogger(TYPE)
```

This configuration instructs Lombok to inject `NodeLoggerFactory.getLogger(TYPE)` as the `log` field when you use the `@CustomLog` annotation.

### Annotate classes with @CustomLog

Replace `@Slf4j` with `@CustomLog` in classes that require node-aware logging:

```java
@CustomLog
public class MyClass {
    public void myMethod() {
        log.info("Hello world");
    }
}
```

The `@CustomLog` annotation injects a logger instance created via `NodeLoggerFactory.getLogger(MyClass.class)`, which automatically enriches MDC with node metadata.

### Use ctx.withLogger(log) in reactive code

In methods that accept an `ExecutionContext` parameter, call `ctx.withLogger(log)` instead of `log` directly to ensure request-scoped MDC enrichment:

```java
public Completable handle(ExecutionContext ctx) {
    ctx.withLogger(log).info("Processing request");
    return Completable.complete();
}
```

Use `ctx.withLogger(log).info(...)` when the execution context is available. Use `log.info(...)` directly when no execution context is present.

### Verify ArchUnit rules

Run `mvn install` to verify that ArchUnit rules pass. ArchUnit rules enforce the use of `NodeLoggerFactory` instead of `org.slf4j.LoggerFactory` and require `ctx.withLogger(log)` in methods with an `ExecutionContext` parameter.

If ArchUnit rules fail, review the error messages and update your code accordingly. To exclude legacy classes from ArchUnit checks, configure the rules in your test class:

```java
LoggingArchitectureRules
    .configure()
    .allowIn(Set.of("com.example.LegacyClass"))
    .resideInAnyPackage("com.example..")
    .checkNoSlf4jLoggerFactory();
```
