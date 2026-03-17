# Node Logging Architecture Rule Enforcement

## Enforcing Architecture Rules

The `gravitee-archrules-maven-plugin` runs during the Maven `test` phase and enforces two logging architecture rules:

1. **NodeLoggerFactory requirement**: Classes must use `NodeLoggerFactory.getLogger` instead of SLF4J `LoggerFactory` directly.
2. **Context-aware logging requirement**: Methods with an `ExecutionContext` parameter must call `ctx.withLogger(log)` instead of logging directly.

Violations fail the build unless the class is allow-listed or the package is excluded.

### Skipping Rule Checks

To skip architecture rule checks (e.g., during CI packaging jobs), pass `-Dgravitee.archrules.skip=true` to Maven:

```bash
mvn clean install -Dgravitee.archrules.skip=true
```

CI/CD pipelines typically pass `-Dgravitee.archrules.skip=true` during build/deploy jobs and `-Dgravitee.archrules.skip=false` during test jobs.

### Allow-Listing Classes

To allow specific classes to violate rules, add them to the allow-list in the test configuration. See `ExecutionContextLoggingArchitectureTest` for examples.

Classes with suffixes matching `ALLOW_LIST_SUFFIXES` (e.g., `ConfigurationEvaluator`) are automatically exempted.

### Package Scope

Architecture rules apply only to the following packages:

* `io.gravitee.gateway.reactive.handlers.*`
* `io.gravitee.gateway.reactive.core.*`
* `io.gravitee.gateway.reactive.debug.*`
* `io.gravitee.apim.plugin.*`
* `io.gravitee.plugin.apiservice.*`
* `io.gravitee.plugin.entrypoint.*`
* `io.gravitee.plugin.endpoint.*`

The following packages are excluded:

* `io.gravitee.gateway.reactive.api.*`
* `io.gravitee.gateway.api.*`

### Test Class Handling

Test classes are excluded by default. To include them, configure `includeTests(true)` in the rule definition.

{% hint style="info" %}
The `gravitee-node-archunit` module was removed in `gravitee-node` 8.0.0-alpha.15. Architecture rules are now enforced exclusively via the Maven plugin.
{% endhint %}
