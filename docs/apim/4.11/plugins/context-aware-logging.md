# Context-aware logging in plugins

## Overview

{% hint style="info" %}
This page is for plugin developers building custom Gravitee policies, endpoints, and entrypoints.
{% endhint %}

When developing Gateway plugins (policies, endpoints, entrypoints), use the context-aware logging API. Log entries are automatically enriched with request metadata such as API ID, environment, organization, application, and plan.

## Use `ctx.withLogger()` for request-scoped logging

In any method that receives an `ExecutionContext` parameter, wrap the logger before logging:

```java
@CustomLog
public class MyPolicy implements Policy {

    @Override
    public Completable onRequest(HttpExecutionContext ctx) {
        // Wraps the logger with MDC from the execution context
        ctx.withLogger(log).info("Processing request for API");
        return Completable.complete();
    }
}
```

The wrapped logger automatically populates MDC with the following keys extracted from the execution context:

* `apiId`
* `envId`
* `orgId`
* `appId`
* `planId`
* `user`

{% hint style="warning" %}
Don't call `log.info()` directly when an `ExecutionContext` is available. This bypasses MDC enrichment. The `gravitee-archrules-maven-plugin` enforces this rule at build time and fails the build on violations.
{% endhint %}

## Use `NodeLoggerFactory` instead of SLF4J

All Gravitee plugin classes use `NodeLoggerFactory.getLogger()` instead of SLF4J's `LoggerFactory.getLogger()`. This ensures node-level metadata (node ID, hostname) is always present in MDC.

Two options for obtaining a logger:

**Option 1 — `@CustomLog` annotation (recommended):**

```java
@CustomLog
public class MyPolicy implements Policy {
    // 'log' field is automatically created by Lombok
}
```

**Option 2 — Direct factory call:**

```java
import io.gravitee.node.logging.NodeLoggerFactory;

public class MyPolicy implements Policy {
    private static final Logger log = NodeLoggerFactory.getLogger(MyPolicy.class);
}
```

The `@CustomLog` annotation is configured in `lombok.config` to delegate to `NodeLoggerFactory`.

## Build-time enforcement

The `gravitee-archrules-maven-plugin` runs two checks during the Maven `verify` phase:

* **`global-logging-check`:** Fails the build if any class uses `org.slf4j.LoggerFactory` directly instead of `NodeLoggerFactory`.
* **`execution-context-logging-check`:** Fails the build if a method calls the logger directly when an `ExecutionContext` parameter is in scope (instead of using `ctx.withLogger(log)`).

To skip these checks during local development:

```bash
mvn clean package -Dgravitee.archrules.skip=true
```
