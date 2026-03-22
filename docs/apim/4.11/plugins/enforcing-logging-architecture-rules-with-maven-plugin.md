# Enforcing Logging Architecture Rules with Maven Plugin

## Enforcing Architecture Rules

The `gravitee-archrules-maven-plugin` runs two checks during the `verify` phase:

1. **global-logging-check**: Scans configured packages and fails if any class calls `org.slf4j.LoggerFactory.getLogger()` directly.
2. **execution-context-logging-check**: Scans methods with `ExecutionContext` parameters and fails if they log without calling `withLogger()` first.

### Exemption Mechanisms

Exempt specific classes by adding them to the `allowIn()` set:

```java
LoggingArchitectureRules
    .configure()
    .allowIn(Set.of("io.gravitee.myproject.LegacyClass"))
    .resideInAnyPackage("io.gravitee.myproject..")
    .checkNoSlf4jLoggerFactory();
```

Exempt classes matching a suffix (e.g., `ConfigurationEvaluator`) via `allowListSuffixes`:

```xml
<allowListSuffixes>
    <suffix>ConfigurationEvaluator</suffix>
</allowListSuffixes>
```

Exclude entire packages from scanning using `excludePackagesFromScan()`:

```java
LoggingArchitectureRules
    .configure()
    .resideInAnyPackage("io.gravitee.myproject..")
    .excludePackagesFromScan("io.gravitee.myproject.api..")
    .checkNoSlf4jLoggerFactory();
```

### Exempted Classes

The following classes are exempted from execution context logging rules:

* `io.gravitee.plugin.endpoint.http.proxy.configuration.HttpProxyEndpointConnectorConfigurationEvaluator`
* `io.gravitee.plugin.endpoint.http.proxy.configuration.HttpProxyEndpointConnectorSharedConfigurationEvaluator`
* `io.gravitee.plugin.endpoint.tcp.proxy.configuration.TcpProxyEndpointConnectorSharedConfigurationEvaluator`

### Skipping ArchUnit Checks in CI Builds

Skip all ArchUnit checks in CI builds by passing `-Dgravitee.archrules.skip=true` to Maven:

```bash
mvn verify -Dgravitee.archrules.skip=true
```

## End-User Configuration

End users do not configure logging infrastructure directly. Platform administrators set `node.logging.*` properties in `gravitee.yml` or Helm values. Developers writing plugins or custom handlers must follow architecture rules (use `@CustomLog`, call `withLogger()` in execution context methods) to ensure logs are enriched with MDC data.

## Restrictions

* The `%mdcList` conversion word cannot be used in `logback.xml` directly—it is registered programmatically after bootstrap.
* Deprecated Helm parameters (`api.logging.debug`, `gateway.logging.graviteeLevel`, etc.) will be removed in a future release; migrate to `logback.override` and `node.logging.*`.
* ArchUnit rules apply only to packages specified in `resideInAnyPackage()` and not excluded via `excludePackagesFromScan()`.
* Execution context logging rules exempt classes in the allow-list (`HttpProxyEndpointConnectorConfigurationEvaluator`, `HttpProxyEndpointConnectorSharedConfigurationEvaluator`, `TcpProxyEndpointConnectorSharedConfigurationEvaluator`) and classes matching `allowListSuffixes`.

{% hint style="info" %}
The `gravitee-archrules-maven-plugin` was introduced in `gravitee-parent` 24.0.0. The `gravitee-node-archunit` module was removed in gravitee-node#528; rules are now enforced via Maven plugin. The Lombok `@Slf4j` annotation check was removed from `LoggingArchitectureRules` in gravitee-node#489.
{% endhint %}
