# Node Logging Infrastructure Overview

## Overview

The Node Logging Infrastructure provides centralized, context-aware logging for Gravitee Gateway and REST API components. It enriches log entries with execution metadata such as node ID, API ID, environment ID, and application ID, and enforces architecture rules to ensure consistent logger usage across the platform. This infrastructure is designed for platform administrators configuring log output and developers writing plugins or custom handlers.

## Key Concepts

### Context-Aware Logging

Execution context metadata (API ID, environment ID, application ID, plan ID) is automatically injected into log entries when using `ExecutionContext.withLogger(log)`. This allows correlation of log events with specific API requests, environments, and applications without manual MDC manipulation. The logger delegates to a context-aware wrapper that populates MDC keys before each log statement.

### MDC (Mapped Diagnostic Context)

MDC is a mechanism for enriching log entries with contextual information. The Node Logging Infrastructure uses MDC to store execution metadata that can be included in log output. MDC keys are populated automatically when using context-aware loggers and can be rendered in log patterns using the `%mdcList` token.

The following MDC keys are available:

* `nodeId`: Identifier of the Gateway or REST API node
* `apiId`: Identifier of the API handling the request
* `envId`: Identifier of the environment
* `orgId`: Identifier of the organization
* `appId`: Identifier of the application
* `planId`: Identifier of the plan

### MDC List Converter

The `%mdcList` pattern token renders selected MDC entries in a configurable format. Administrators control which keys appear (via `node.logging.mdc.include`), how they are formatted (`node.logging.mdc.format`), and how they are separated (`node.logging.mdc.separator`). When an MDC key is missing, the configured `node.logging.mdc.nullValue` (default `"-"`) is displayed.

{% hint style="warning" %}
Do not use `%mdcList` directly in `logback.xml` via `<conversionRule>`. The `MdcListConverter` class is not visible to Logback's classloader at parse time, causing `PARSER_ERROR[mdcList]`. Use pattern override via `gravitee.yml` instead.
{% endhint %}

The converter is registered programmatically at runtime using Logback 1.4+'s supplier-based API to avoid classloader conflicts in custom classloader hierarchies.

### Architecture Rule Enforcement

The `gravitee-archrules-maven-plugin` enforces two rules at build time:

1. **No Direct SLF4J LoggerFactory Usage**: Classes must use `NodeLoggerFactory.getLogger(TYPE)` instead of SLF4J's `LoggerFactory` directly.
2. **Context-Aware Logging**: Methods with an `ExecutionContext` parameter must call `ctx.withLogger(log)` instead of logging directly.

Violations fail the build unless the class is allow-listed or the package is excluded. Test classes are excluded by default.

## Prerequisites

* Gravitee Gateway or REST API version 4.6.0 or later (includes `gravitee-node` 8.0.0-alpha.2+)
* Logback 1.4+ (for supplier-based converter registration)
* Maven 3.6+ (if enforcing architecture rules during builds)
