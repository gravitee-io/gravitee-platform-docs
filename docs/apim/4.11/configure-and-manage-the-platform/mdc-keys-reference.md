# MDC Keys Reference and Migration Notes

## MDC Keys Reference

### Standard Keys

| Key | Source | Description |
|:----|:-------|:------------|
| `nodeId` | `Node.id()` | Unique identifier of the Gravitee Node |
| `nodeHostname` | `Node.hostname()` | Hostname where the node is running |
| `nodeApplication` | `Node.application()` | Name of the application |
| `apiId` | `ATTR_API` | API identifier (cached) |
| `apiName` | `ATTR_API_NAME` | API name (cached) |
| `apiType` | `ATTR_INTERNAL_API_TYPE` | API type (cached) |
| `envId` | `ATTR_ENVIRONMENT` | Environment identifier (cached) |
| `orgId` | `ATTR_ORGANIZATION` | Organization identifier (cached) |
| `appId` | `ATTR_APPLICATION` | Application identifier (refreshable) |
| `planId` | `ATTR_PLAN` | Plan identifier (refreshable) |
| `user` | `ATTR_USER` | User identifier (refreshable) |

### Rest API Additional Keys

| Key | Source | Description |
|:----|:-------|:------------|
| `correlationId` | `X-Correlation-ID` header | Request correlation ID |
| `traceParent` | `traceparent` header | W3C Trace Context |

The Rest API extracts `apiId` and `appId` from request paths matching `/apis/{apiId}` and `/applications/{appId}`.

## Restrictions

- The `%mdcList` conversion word cannot be registered via `<conversionRule>` in `logback.xml` due to classloader visibility constraints. Use `node.logging.pattern.overrideLogbackXml=true` instead.
- Pattern override is enabled by default. Disable it by setting `node.logging.pattern.overrideLogbackXml=false` if you manage patterns entirely in `logback.xml`.
- Deprecated Helm chart parameters (`*.logging.debug`, `*.logging.graviteeLevel`, `*.logging.jettyLevel`, `*.logging.stdout.*`, `*.logging.file.*`, `*.logging.additionalLoggers`) are replaced by `*.logback.override` and `*.node.logging.*` settings.
- ArchUnit logging rules require `gravitee-parent` 24.0.0-alpha.2 or later and are skipped in release builds via `-Dgravitee.archrules.skip=true`.
- Manual log source registration in execution contexts is no longer required — `AbstractBaseExecutionContextAwareLogger` automatically registers the full class hierarchy.
