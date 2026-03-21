# Logging Architecture Rules Enforcement

## Enforcing Architecture Rules

The `gravitee-archrules-maven-plugin` enforces logging patterns at build time. The plugin runs ArchUnit tests during the Maven `test` phase and is configured in `gravitee-parent` and inherited by child projects.

### Plugin Configuration

Configure the plugin in your project's `pom.xml`:

### Rule Enforcement

The plugin enforces two rules:

1. **LoggingArchitectureRules**: Prohibits direct `LoggerFactory.getLogger()` calls. Classes must use `NodeLoggerFactory.getLogger()` instead.
2. **ExecutionContextLoggingArchitectureTest**: Enforces `ctx.withLogger(log)` pattern for methods with `ExecutionContext` parameters. Methods with an `ExecutionContext` parameter must not call `Logger.info()`, `debug()`, `error()`, `warn()`, or `trace()` directly.

Build failures occur when violations are detected unless `-Dgravitee.archrules.skip=true` is set.

### Error Messages

When `LoggingArchitectureRules` is violated:

When `ExecutionContextLoggingArchitectureTest` is violated:

### Configuration Options

| Configuration | Description | Example |
|:--------------|:------------|:--------|
| `excludePackagesFromScan` | Exclude specific packages from rule checks | `com.example.excluded` |
| `allowedClassesForLoggerFactory` | Allow specific classes to use `LoggerFactory` directly | `*ConfigurationEvaluator` |

Skip architecture rule checks during development or CI builds:

| Property | Description | Example |
|:---------|:------------|:--------|
| `gravitee.archrules.skip` | Skip ArchUnit rule enforcement | `-Dgravitee.archrules.skip=true` |
| `skip.validation` | Skip Maven validation phase | `-Dskip.validation=true` |

{% hint style="info" %}
Requires Gravitee Parent 24.0.0 or later. The `gravitee-node-archunit` module was removed in PR #528 after rules were integrated into the Maven plugin.
{% endhint %}

## Restrictions

The `%mdcList` converter cannot be declared directly in `logback.xml` via `<conversionRule>`. It must be registered programmatically after the bootstrap classloader has initialized. Enable the pattern override via `gravitee.yml` instead:
