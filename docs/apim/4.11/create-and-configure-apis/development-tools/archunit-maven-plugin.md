# Enforcing Logging Rules with ArchUnit Maven Plugin

## Maven Plugin Configuration

The `gravitee-archrules-maven-plugin` enforces logging architecture rules at build time. The plugin executes during the Maven `verify` phase and provides two goals:

* **`global-logging-check`**: Enforces `NodeLoggerFactory` usage and prohibits direct `org.slf4j.LoggerFactory` dependencies.
* **`execution-context-logging-check`**: Enforces `ctx.withLogger(log)` usage when `ExecutionContext` is available in method scope.

### Plugin Properties

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `gravitee.archrules.skip` | Boolean | `false` | Skip all ArchUnit rule checks |
| `global-logging-check.failOnError` | Boolean | `true` | Fail build on SLF4J `LoggerFactory` usage |
| `global-logging-check.allowListSuffixes` | List\<String> | `[ConfigurationEvaluator]` | Class name suffixes exempt from rule |
| `execution-context-logging-check.failOnError` | Boolean | `true` | Fail build on direct Logger calls when ExecutionContext available |

### Global Logging Check

The `global-logging-check` goal scans configured packages and fails the build if any class depends on `org.slf4j.LoggerFactory`. Classes must use `io.gravitee.node.logging.NodeLoggerFactory` instead.

**Exemptions:**

* Classes with names ending in `ConfigurationEvaluator` (generated classes)
* Packages excluded via `excludePackagesFromScan()` configuration

**Excluded Packages (not scanned):**

* `io.gravitee.node.reactive.api..`
* `io.gravitee.gateway.reactive.api..`
* `io.gravitee.gateway.api..`

### Execution Context Logging Check

The `execution-context-logging-check` goal scans reactive Gateway and plugin packages. It fails the build if a method calls `Logger.xxx()` directly when an `ExecutionContext` parameter is available in scope.

**Scanned Packages:**

* `io.gravitee.gateway.reactive.handlers..`
* `io.gravitee.gateway.reactive.core..`
* `io.gravitee.gateway.reactive.debug..`
* `io.gravitee.apim.plugin..`
* `io.gravitee.plugin.apiservice..`
* `io.gravitee.plugin.entrypoint..`
* `io.gravitee.plugin.endpoint..`

**Exemptions:**

* Classes ending with `ConfigurationEvaluator`
* Packages `io.gravitee.gateway.reactive.api..` and `io.gravitee.gateway.api..`

### Skipping Checks

To skip ArchUnit checks during packaging or deployment:

```bash
mvn clean package -Dgravitee.archrules.skip=true
```

**CI Pipeline Behavior:**

* Checks are **skipped** during packaging, staging, and deployment jobs.
* Checks are **enforced** during build and community build jobs.
