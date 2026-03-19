# Implementing Context-Aware Logging in Gateway Plugins and Management API

## Creating Context-Aware Logs in Gateway Plugins

Developers writing reactive Gateway plugins (policies, endpoints, entrypoints) must use `ctx.withLogger(log)` when an `ExecutionContext` is available. This ensures that MDC is automatically enriched with request-specific metadata.

### Five-step pattern

1. **Obtain a logger** via `NodeLoggerFactory.getLogger(MyClass.class)` or `@CustomLog`.
2. **Wrap the logger** in methods receiving an `ExecutionContext` parameter: `ctx.withLogger(log).info("Processing request")`.
3. **Automatic MDC enrichment** occurs when the wrapped logger is created. The following keys are extracted from the context:
   - `apiId`
   - `envId`
   - `orgId`
   - `appId`
   - `planId`
   - `user`
4. **Use the wrapped logger** for all subsequent log calls within that method.
5. **Do NOT call `log.info()` directly** when `ctx` is available. This bypasses MDC enrichment and violates the ArchUnit rule enforced at build time.

## Related Changes

### Removed Manual Context Registration

The following components no longer require manual hierarchy collection:

- `DefaultExecutionContext`: Removed `collectParentClasses()` method and static `CONTEXT_CLASSES` field.
- `DefaultKafkaConnectionContext`: Removed `registerExecutionContextClasses()` static method.
- `DefaultKafkaExecutionContext`: Removed static initializer calling `registerExecutionContextClasses()`.
- `DefaultKafkaMessageExecutionContext`: Removed static initializer calling `registerExecutionContextClasses()`.
- `KafkaEntrypointConnectContextInternal`: Removed static `CONTEXT_CLASSES` field and manual `registerLogSources()` override.

### Hierarchy Caching Automation

`AbstractBaseExecutionContextAwareLogger` now automatically collects and caches the full class hierarchy (interfaces and superclasses) for each context type. The cache stops at `BaseExecutionContext` and does not include `Object`.

### Dependency Updates

| Artifact | Version Change | Purpose |
|:---------|:---------------|:--------|
| `io.gravitee.node:gravitee-node-logging` | Added (8.0.0-alpha.2) | Provides `NodeLoggerFactory` and `NodeAwareLogger` |
| `io.gravitee.gateway:gravitee-gateway-api` | 5.0.0-alpha.6 → 5.0.0 | Adds `ExecutionContextLazyLogger` and `AbstractBaseExecutionContextAwareLogger` |
| `io.gravitee.reactor:gravitee-reactor-native-kafka` | 6.0.0-alpha.6 → 6.0.0-alpha.7 | Removes manual context class registration |
| `io.gravitee.maven:gravitee-archrules-maven-plugin` | Added (1.0.0-alpha.1 → 1.0.0-alpha.2) | Enforces logging architecture rules |

### Removed Module

The `gravitee-node-archunit` module was removed. Its functionality was moved to `gravitee-archrules-maven-plugin`.
