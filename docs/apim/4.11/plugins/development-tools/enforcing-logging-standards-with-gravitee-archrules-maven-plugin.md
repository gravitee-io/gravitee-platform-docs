# Enforcing Logging Standards with gravitee-archrules-maven-plugin

## Restrictions

- The `%mdcList` conversion word cannot be declared in `logback.xml` using `<conversionRule>` — it is registered programmatically and will fail with `PARSER_ERROR[mdcList]` if declared manually.
- ArchUnit ExecutionContext logging rules apply only to packages `io.gravitee.gateway.reactive.handlers..`, `io.gravitee.gateway.reactive.core..`, `io.gravitee.gateway.reactive.debug..`, `io.gravitee.apim.plugin..`, `io.gravitee.plugin.apiservice..`, `io.gravitee.plugin.entrypoint..`, `io.gravitee.plugin.endpoint..` — classes in `io.gravitee.gateway.reactive.api..` and `io.gravitee.gateway.api..` are excluded.
- Classes ending with `ConfigurationEvaluator` are exempt from ExecutionContext logging rules (generated classes).
- Deprecated Helm chart properties (`api.logging.debug`, `api.logging.graviteeLevel`, `gateway.logging.stdout.encoderPattern`, etc.) are replaced by `logback.override` and `node.logging.*` — migration required for future releases.
- MDC keys renamed in gravitee-gateway-api 5.0.0: `environment` → `envId`, `organization` → `orgId`, `application` → `appId`, `plan` → `planId` — update log parsing tools accordingly.


