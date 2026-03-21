# Node Logging Infrastructure Overview

## Overview

The Gravitee Node Logging Infrastructure provides centralized, context-aware logging for API Gateway and Management API components. It enriches log entries with MDC (Mapped Diagnostic Context) values such as API ID, organization ID, and node ID, and enforces architecture rules to ensure consistent logging patterns across the platform. This feature is for platform administrators configuring log output and developers writing plugins or custom handlers.

## Key Concepts

### MDC Enrichment

The logging infrastructure automatically injects contextual metadata into log entries via SLF4J's MDC. Each log line can include values like `nodeId`, `apiId`, `envId`, `orgId`, `appId`, and `planId`. The `node.logging.mdc.include` property controls which keys appear in output. When a log source is unavailable, the MDC value defaults to `"unknown"` rather than being omitted. MDC keys were shortened in version 5.0.0-alpha.6: `environment` → `envId`, `organization` → `orgId`, `application` → `appId`, `plan` → `planId`.

### Logback Pattern Override

By default (`node.logging.pattern.overrideLogbackXml: true`), the platform applies runtime log patterns from `gravitee.yml` instead of those in `logback.xml`. This allows centralized control of console and file log formats without editing XML files. The `%mdcList` conversion word renders MDC entries using the format and separator defined in `node.logging.mdc.format` and `node.logging.mdc.separator`. Do NOT register `MdcListConverter` manually in `logback.xml` — it is registered programmatically after bootstrap to avoid classloader conflicts.

### Architecture Rules

Two ArchUnit-based rules enforce logging best practices at build time. The **global-logging-check** rule prohibits direct use of `org.slf4j.LoggerFactory`; classes must use `NodeLoggerFactory` instead (injectable via Lombok `@CustomLog`). The **execution-context-logging-check** rule requires methods with an `ExecutionContext` parameter to call `ctx.withLogger(log).info(...)` instead of `log.info(...)` directly, ensuring request context is included. Both rules run during Maven's `verify` phase and fail the build on violations unless `-Dgravitee.archrules.skip=true` is set.

### Helm Chart Logback Override

The Helm chart supports two logback configuration modes. When `api.logback.override` or `gateway.logback.override` is `false`, the chart uses legacy properties like `api.logging.debug` and `api.logging.graviteeLevel` (now deprecated). When set to `true`, the chart uses the complete `logback.xml` content from `api.logback.content` or `gateway.logback.content`, ignoring all legacy properties. The `node.logging.*` properties remain active in both modes for MDC and pattern configuration.

## Prerequisites

* Gravitee API Management 4.x or later
* Gravitee Node 8.0.0-alpha.2 or later
* Gravitee Gateway API 5.0.0-alpha.6 or later (for ExecutionContext logging)
* Gravitee Parent 24.0.0-alpha.1 or later (for ArchUnit plugin)
* Maven 3.6+ (for build-time architecture rule enforcement)
