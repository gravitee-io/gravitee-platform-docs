# Node Logging Infrastructure Overview

## Overview

The Node Logging Infrastructure provides context-aware logging for Gravitee Gateway and Management API components. It enriches log entries with request metadata (API ID, organization, environment, application, plan) via MDC (Mapped Diagnostic Context) and enforces consistent logging patterns across the platform through ArchUnit rules. This infrastructure is designed for platform administrators configuring log output and developers writing reactive Gateway plugins.

## Key Concepts

### Context-Aware Logging

Gravitee components operate in multi-tenant, multi-API environments where a single log line may relate to a specific API, organization, environment, application, or subscription plan. Context-aware logging automatically injects this metadata into MDC so operators can filter and correlate logs without manual instrumentation. The Gateway uses `ExecutionContext` to carry request metadata; the Management API uses HTTP path segments and headers.

### NodeLoggerFactory

`NodeLoggerFactory` replaces direct SLF4J `LoggerFactory` usage. It wraps SLF4J loggers with `NodeAwareLogger`, which enriches MDC with node-level metadata (node ID, hostname, application name) and delegates to extensible MDC registration hooks. Developers use `NodeLoggerFactory.getLogger(MyClass.class)` or Lombok's `@CustomLog` annotation (configured to call `NodeLoggerFactory` via `lombok.config`).

### MDC Filtering and Formatting

The `%mdcList` Logback converter formats selected MDC keys into log output. Administrators configure which keys to include (`node.logging.mdc.include`), how to format each entry (`node.logging.mdc.format`), and how to separate entries (`node.logging.mdc.separator`). This avoids cluttering logs with unused context fields. The converter is registered programmatically at runtime, not via `<conversionRule>` in `logback.xml`.

## Prerequisites

- Gravitee Gateway or Management API 4.x (alpha.2 or later)
- Logback 1.4+
- Maven 3.6+ (if enforcing ArchUnit rules during build)
- Helm chart 4.x (if deploying via Kubernetes)


For configuration details, see [Node Logging Configuration](node-logging-configuration.md).
