# Using Context-Aware Loggers in Gateway Plugins

## Using Context-Aware Loggers in Gateway Plugins

When writing Gateway handlers or plugins that receive an `ExecutionContext` parameter:

1. Declare a logger using `@CustomLog` (Lombok) or `NodeLoggerFactory.getLogger(MyClass.class)`.
2. In methods with an `ExecutionContext ctx` parameter, call `ctx.withLogger(log)` to obtain a context-aware logger.
3. Use the returned logger for all subsequent log statements in that method:

```java
ctx.withLogger(log).info("Processing request");
```

The context-aware logger automatically populates MDC keys (`apiId`, `envId`, `appId`, `planId`) from the execution context before each log call.

{% hint style="warning" %}
Do NOT log directly via the original `log` instance when `ExecutionContext` is available. This bypasses MDC enrichment and triggers architecture rule violations during builds.
{% endhint %}

### Restrictions

* When a log source is unavailable (no class context), the MDC value is set to `"unknown"` rather than omitted.
* MDC key names changed from `environment`, `organization`, `application`, `plan` to `envId`, `orgId`, `appId`, `planId` in `gravitee-gateway-api` 5.0.0-alpha.6. Existing log parsers or dashboards filtering on old key names must be updated.
