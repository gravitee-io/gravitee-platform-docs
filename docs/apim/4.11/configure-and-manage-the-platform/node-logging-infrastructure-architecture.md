
# Node logging infrastructure architecture

## Overview

The Node Logging Infrastructure uses `NodeLoggerFactory` instead of direct SLF4J calls, enriches logs with MDC data from execution contexts, and supports runtime pattern overrides. Architecture rules are enforced via the `gravitee-archrules-maven-plugin`.


## NodeLoggerFactory


`NodeLoggerFactory` replaces direct calls to `org.slf4j.LoggerFactory`. It creates loggers that automatically enrich MDC with node metadata (node ID, hostname, application name) and execution context attributes (API ID, environment ID, organization ID, plan ID, user). Developers annotate classes with `@CustomLog` (via Lombok) to inject a logger that uses `NodeLoggerFactory` under the hood.

## MDC Enrichment

MDC keys are populated from two sources: node metadata (cached once per logger instance) and execution context attributes (refreshed per request). The `%mdcList` conversion word formats MDC entries using configurable patterns (`mdc.format`, `mdc.separator`, `mdc.nullValue`). When a log source is unavailable, the system sets the MDC value to `"unknown"` instead of omitting it.

| MDC Key           | Source                      | Cached/Refreshable |
|-------------------|-----------------------------|--------------------|
| `nodeId`          | `Node.id()`                 | Cached             |
| `nodeHostname`    | `Node.hostname()`           | Cached             |
| `nodeApplication` | `Node.application()`        | Cached             |
| `apiId`           | `ATTR_API`                  | Cached             |
| `apiName`         | `ATTR_API_NAME`             | Cached             |
| `apiType`         | `ATTR_INTERNAL_API_TYPE`    | Cached             |
| `envId`           | `ATTR_ENVIRONMENT`          | Cached             |
| `orgId`           | `ATTR_ORGANIZATION`         | Cached             |
| `appId`           | `ATTR_APPLICATION`          | Refreshable        |
| `planId`          | `ATTR_PLAN`                 | Refreshable        |
| `user`            | `ATTR_USER`                 | Refreshable        |
| `correlationId`   | `X-Correlation-ID` header   | Refreshable        |
| `traceParent`     | `traceparent` header        | Refreshable        |

## Execution Context Logging

Methods that accept an `ExecutionContext` parameter must call `ctx.withLogger(log)` before logging. This wraps the logger in an `ExecutionContextLazyLogger`, which defers context-aware logger creation until a logging level is enabled. The lazy logger checks the delegate's level first, avoiding overhead when logging is disabled. Execution context hierarchies are cached per class to eliminate repeated reflection.

## Architecture Rules

ArchUnit rules enforce logging standards at build time. The `global-logging-check` goal fails builds when classes directly call `org.slf4j.LoggerFactory.getLogger()` instead of `NodeLoggerFactory`. The `execution-context-logging-check` goal fails when methods with `ExecutionContext` parameters log without calling `withLogger()`. Exemptions are granted via allow-lists (specific classes, suffix patterns like `ConfigurationEvaluator`) and package exclusions.

## Helm Chart Configuration

**Deprecated parameters** (use `logback.override` and `node.logging` instead):
- `api.logging.debug`
- `api.logging.graviteeLevel`
- `api.logging.jettyLevel`
- `api.logging.stdout.encoderPattern`
- `api.logging.file.enabled`
- `api.logging.file.rollingPolicy`
- `api.logging.file.encoderPattern`
- `api.logging.additionalLoggers`
- `gateway.logging.debug`
- `gateway.logging.graviteeLevel`
- `gateway.logging.jettyLevel`
- `gateway.logging.stdout.encoderPattern`
- `gateway.logging.file.enabled`
- `gateway.logging.file.rollingPolicy`
- `gateway.logging.file.encoderPattern`
- `gateway.logging.additionalLoggers`

**New parameters**:
- `api.logback.override`
- `api.logback.content`
- `gateway.logback.override`
- `gateway.logback.content`
