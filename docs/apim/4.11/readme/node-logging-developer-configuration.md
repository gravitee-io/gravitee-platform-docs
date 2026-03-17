# Developer Configuration for Node Logging

## Developer Configuration

### Lombok Integration

Gravitee components use Lombok's `@CustomLog` annotation to inject loggers that automatically enrich MDC with node-specific information. Configure Lombok integration in `lombok.config`:

| Property | Value | Description |
|:---------|:------|:------------|
| `config.stopBubbling` | `true` | Stop searching for parent lombok.config files |
| `lombok.log.custom.declaration` | `org.slf4j.Logger io.gravitee.node.logging.NodeLoggerFactory.getLogger(TYPE)` | Custom logger factory for `@CustomLog` annotation |

Use `@CustomLog` in Java classes to inject a logger obtained via `NodeLoggerFactory.getLogger(MyClass.class)`. The logger is a `NodeAwareLogger` instance that enriches MDC with node-specific information.

**Example:**

```java
@CustomLog
public class MyClass {
    public void myMethod() {
        log.info("Hello world");
    }
}
```

### Maven Plugin Configuration

The `gravitee-archrules-maven-plugin` validates logging architecture rules during the Maven build. Configure the plugin behavior using the following property:

| Property | Description | Default |
|:---------|:------------|:--------|
| `gravitee.archrules.skip` | Skip ArchUnit architecture rules validation | `false` |

Add `-Dgravitee.archrules.skip=true` to Maven commands to skip ArchUnit validation in CI builds where it is not needed (e.g., release builds, snapshot deployments).

**Example:**

```bash
mvn clean verify -DskipTests=true -Dskip.validation=true -Dgravitee.archrules.skip=true -T 4
```

{% hint style="info" %}
The `gravitee-archrules-maven-plugin` version 1.0.0-alpha.2 replaces the deprecated `gravitee-node-archunit` module.
{% endhint %}
