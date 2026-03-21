# Node-Aware Logger Integration for Developers

## Creating Node-Aware Loggers

Use `NodeLoggerFactory.getLogger()` instead of `LoggerFactory.getLogger()` to create loggers that participate in MDC enrichment. The logger automatically injects MDC values when log statements execute.

For execution context logging, call `ctx.withLogger(log).info("message")` instead of `log.info("message")` directly. This ensures the execution context's attributes (API ID, application ID, plan ID) are included in MDC.

When the log source is unavailable, MDC values default to `"unknown"`.

### Lombok Integration

Add `lombok.config` to your project root:

```properties
config.stopBubbling = true
lombok.log.custom.declaration = org.slf4j.Logger io.gravitee.node.logging.NodeLoggerFactory.getLogger(TYPE)
```

Annotate classes with `@CustomLog`:

```java
@CustomLog
public class MyClass {
    public void myMethod() {
        log.info("Hello world");
    }
}
```

This configures Lombok's `@CustomLog` annotation to inject `NodeLoggerFactory.getLogger()` instead of `LoggerFactory.getLogger()`.
