
# Developer Guide: Creating Context-Aware Logs

## Creating Context-Aware Logs

To emit logs enriched with request context, inject a logger using Lombok's `@CustomLog` annotation. In methods that receive an `ExecutionContext` parameter, call `ctx.withLogger(log).info("message")` instead of `log.info("message")` directly. This ensures the log entry includes MDC values like `apiId`, `envId`, and `orgId` from the execution context.

Example:

```java
@CustomLog
public class MyService {
    public void process(ExecutionContext ctx) {
        ctx.withLogger(log).info("Processing request");
    }
}
```

The architecture rules enforce this pattern at build time. Direct logger calls in methods with `ExecutionContext` parameters will fail the Maven `verify` phase unless the class name ends with `ConfigurationEvaluator` or is explicitly allow-listed.

{% hint style="warning" %}
Direct use of `org.slf4j.LoggerFactory` is prohibited by the `global-logging-check` rule. Use `NodeLoggerFactory` or Lombok `@CustomLog` instead.

Methods with an `ExecutionContext` parameter must use `ctx.withLogger(log)` instead of calling logger methods directly, enforced by the `execution-context-logging-check` rule.
{% endhint %}
