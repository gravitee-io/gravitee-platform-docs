# Node Logging Infrastructure Overview

## Overview

The Node Logging Infrastructure provides context-aware logging with automatic MDC (Mapped Diagnostic Context) enrichment across Gravitee APIM components. It captures node, API, application, and request metadata in log entries, enabling correlation and filtering in centralized logging systems. Available in APIM 4.11 and later.

## Key Concepts

### MDC Enrichment

MDC enrichment automatically injects contextual metadata into log entries. The infrastructure registers log sources from execution contexts and node information, then formats them according to configurable patterns. When a log source is unavailable, the system sets the MDC value to `"unknown"`. Null values are replaced with the configured `node.logging.mdc.nullValue` (default: `"-"`). Context-aware loggers initialize lazily—only when the log level is enabled—to minimize overhead.

### Context-Aware Logging

Methods with access to an `ExecutionContext` parameter must use `ctx.withLogger(log).info(...)` instead of calling `log.info(...)` directly. This ensures MDC entries are populated from the execution context. The `ExecutionContextLazyLogger` defers logger initialization until a log method is called and the log level check passes. The `AbstractBaseExecutionContextAwareLogger` base class caches the full class hierarchy of execution contexts in a `ConcurrentHashMap`, allowing `LogEntry` instances to resolve values from any parent class or interface.

### Architecture Rules

The logging architecture enforces two rules via the `gravitee-archrules-maven-plugin`. First, classes must NOT depend directly on `org.slf4j.LoggerFactory`—use `io.gravitee.node.logging.NodeLoggerFactory` instead. Second, methods with `ExecutionContext` parameters must use `ctx.withLogger(log)` instead of direct logger calls. Entire sub-packages can be excluded using `excludePackagesFromScan`, and individual classes can be exempted via allow-lists. Test classes are excluded by default but can be included with `includeTests(boolean)`.

## Prerequisites

- APIM 4.11 or later
- Write access to `gravitee.yml` or Helm chart values
- For custom logback configuration: write access to `logback.xml`

## Related Changes

- **Helm Chart:** New `logback.override` and `logback.content` parameters replace deprecated `logging.*` parameters.
- **Architecture Validation:** `gravitee-archrules-maven-plugin` version `1.0.0-alpha.2` enforces logging rules.
- **MDC Key Renaming:** MDC keys shortened in PR #328 (e.g., `environment` → `envId`, `organization` → `orgId`, `application` → `appId`, `plan` → `planId`).
- **Default Log Pattern:** Updated to include milliseconds (`HH:mm:ss.SSS`).
- **Documentation:** New pages added to `gravitee-platform-docs` for node logging infrastructure and configuration.
