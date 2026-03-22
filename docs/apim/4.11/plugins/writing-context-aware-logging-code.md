# Writing Context-Aware Logging Code

### Helm Chart Configuration

Use `logback.override` and `logback.content` to replace the entire `logback.xml` file, or configure `node.logging.*` properties to override patterns only. Deprecated parameters (`api.logging.debug`, `gateway.logging.graviteeLevel`, etc.) are replaced by:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api.logback.override` | Boolean | `false` | Use complete custom logback.xml |
| `api.logback.content` | String | JSON-formatted logback config | Complete logback.xml content |
| `gateway.logback.override` | Boolean | `false` | Use complete custom logback.xml |
| `gateway.logback.content` | String | JSON-formatted logback config with async appenders | Complete logback.xml content |

## Creating Context-Aware Loggers

Add a `lombok.config` file at the repository root with the following declaration:

```properties
lombok.log.custom.declaration = org.slf4j.Logger io.gravitee.node.logging.NodeLoggerFactory.getLogger(TYPE)
```

Annotate classes with `@CustomLog` to inject a logger that uses `NodeLoggerFactory`. In methods that accept an `ExecutionContext` parameter, call `Logger contextLogger = ctx.withLogger(log)` before logging. The `withLogger()` method returns an `ExecutionContextLazyLogger` that enriches MDC with execution context attributes only when the logging level is enabled.

Example:

```java
public void handle(ExecutionContext ctx) {
    Logger ctxLog = ctx.withLogger(log);
    ctxLog.info("Processing request");
}
```
