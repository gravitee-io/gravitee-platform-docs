# Creating Context-Aware Loggers in Plugins and Policies

## Creating Context-Aware Loggers in Plugins and Policies

### Overview

This guide explains how to create context-aware loggers in Gravitee plugins and custom policies. Context-aware loggers automatically extract request metadata (API ID, environment ID, organization ID, application ID, plan ID, and user) from the `ExecutionContext` and add it to the Mapped Diagnostic Context (MDC) for structured logging.

### Prerequisites

Before creating context-aware loggers, ensure the following:

* Your project includes `io.gravitee.node:gravitee-node-logging` as a provided dependency.
* Lombok is configured in your project.
* A `lombok.config` file exists at the repository root.

### Configure Lombok for NodeLoggerFactory

1. Create or edit the `lombok.config` file at the repository root.
2. Add the following lines:

   ```properties
   config.stopBubbling = true
   lombok.log.custom.declaration = org.slf4j.Logger io.gravitee.node.logging.NodeLoggerFactory.getLogger(TYPE)
   ```

   This configuration tells Lombok to use `NodeLoggerFactory` instead of the standard SLF4J `LoggerFactory` when generating loggers via the `@CustomLog` annotation.

### Use @CustomLog to Generate Loggers

1. Add the `@CustomLog` annotation to your class:

   ```java
   @CustomLog
   public class MyPlugin {
       public void myMethod(ExecutionContext ctx) {
           ctx.withLogger(log).info("Processing request");
       }
   }
   ```

   Lombok generates the following field:

   ```java
   private static final Logger log = NodeLoggerFactory.getLogger(MyPlugin.class);
   ```

2. In methods with an `ExecutionContext` parameter, call `ctx.withLogger(log)` instead of `log` directly:

   ```java
   // Correct: includes request context in logs
   ctx.withLogger(log).info("Processing request");

   // Incorrect: does not include request context
   log.info("Processing request");
   ```

   The `ctx.withLogger(log)` method returns a context-aware logger that automatically extracts the following metadata from the `ExecutionContext` and adds it to MDC:

   * `apiId` — API identifier
   * `envId` — Environment identifier
   * `orgId` — Organization identifier
   * `appId` — Application identifier
   * `planId` — Plan identifier
   * `user` — User identifier

### Use ExecutionContextLazyLogger for Deferred Initialization

For performance-sensitive code, use `ExecutionContextLazyLogger` to defer creation of the context-aware logger until a log method is actually called and the log level is enabled.

```java
@CustomLog
public class MyPlugin {
    public void myMethod(ExecutionContext ctx) {
        Logger contextLogger = new ExecutionContextLazyLogger(log, ctx);
        contextLogger.debug("Debug message");
    }
}
```

Level checks (`isDebugEnabled()`, `isInfoEnabled()`, etc.) delegate directly to the base logger without initializing the context-aware logger.

### Automatic Log Source Registration

`AbstractBaseExecutionContextAwareLogger` automatically registers the full class hierarchy of the `ExecutionContext` as log sources. Manual log source registration is no longer required.

The logger collects all superclasses and interfaces of the execution context type, caches them in a `ConcurrentHashMap`, and registers each class as a log source pointing to the same context instance. Traversal stops at `BaseExecutionContext`.

### ArchUnit Enforcement Rules

Gravitee enforces logging architecture rules via ArchUnit:

* **No direct use of SLF4J `LoggerFactory`**: Classes in specified packages must not call `org.slf4j.LoggerFactory`. Use `io.gravitee.node.logging.NodeLoggerFactory` instead.
* **Mandatory `ctx.withLogger(log)` in reactive code**: Methods with an `ExecutionContext` parameter must not call `Logger.info()`, `Logger.debug()`, etc. directly. Use `ctx.withLogger(log).info(...)` to include request context in logs.

The `gravitee-archrules-maven-plugin` enforces these rules during the build. To skip ArchUnit checks, add `-Dgravitee.archrules.skip=true` to your Maven command.

### Verification

To verify that context-aware logging is working correctly:

1. Run your plugin or policy with an `ExecutionContext` that contains request metadata.
2. Check the log output for MDC entries. If `node.logging.pattern.overrideLogbackXml` is enabled and `%mdcList` is included in the log pattern, you should see entries like:

   ```
   apiId: my-api-id envId: my-env-id orgId: my-org-id
   ```

3. If MDC entries are missing, verify that:
   * You are calling `ctx.withLogger(log)` instead of `log` directly.
   * The `ExecutionContext` contains the expected metadata.
   * The `node.logging.mdc.include` property in `gravitee.yml` includes the MDC keys you expect to see.
