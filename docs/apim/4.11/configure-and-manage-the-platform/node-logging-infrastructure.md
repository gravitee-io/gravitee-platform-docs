# Node Logging Restrictions and Migration Guide

## Deprecated Helm Chart Properties

The following Helm chart properties are deprecated and will be removed in a future release:

| Deprecated Property | Replacement |
|:-------------------|:------------|
| `api.logging.debug` | `api.logback.override` |
| `api.logging.graviteeLevel` | `api.logback.content` |
| `api.logging.stdout.encoderPattern` | `api.node.logging.pattern.console` |
| `gateway.logging.debug` | `gateway.logback.override` |
| `gateway.logging.graviteeLevel` | `gateway.logback.content` |
| `gateway.logging.stdout.encoderPattern` | `gateway.node.logging.pattern.console` |

## Related Changes

The following changes are part of the Node Logging Infrastructure update:

* The Helm chart now includes `logback.override` and `node.logging` configuration sections for both API and Gateway components.
* The `gravitee-archrules-maven-plugin` (version 1.0.0-alpha.2) is integrated into the parent POM to enforce logging architecture rules during builds.
* The `@CustomLog` Lombok annotation is configured via `lombok.config` to inject `NodeLoggerFactory.getLogger(TYPE)` instead of the default SLF4J logger.
* Default logback.xml patterns in the Helm chart no longer include `%mdcList` directly. Runtime pattern override is the recommended approach.
* The REST API now includes `correlationId` and `traceParent` MDC keys extracted from request headers.
