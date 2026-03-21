---
description: An overview about debug logging.
metaLinks:
  alternates:
    - debug-logging.md
---

# Debug Logging

## Overview

{% hint style="danger" %}
Debug logging can reduce performance. To avoid issues with performance, enable debug logging for only specific troubleshooting purposes.
{% endhint %}

Gravitee supports standard Java logging for each Gravitee component and debug logging for specific Java classes. For example:

```
com.graviteesource.secretprovider.microsoft.keyvault.client.MicrosoftKeyVaultClientImpl
```

You can enable debug logging using the internal `logback.xml` file or the [Gravitee Helm chart](https://github.com/gravitee-io/gravitee-api-management/blob/master/helm/values.yaml) `values.yml` file. After you have made your changes, you must start the specific Gravitee components. Or, you can temporarily enable debug logging using the [#internal-api](debug-logging.md#internal-api "mention") without restarting the component or container. When you restart the component or container, the runtime configuration is lost and debug logging is disabled. You can enable component-based debug logging and Java-class debug logging.

Component-based debug logging means that you enable debug logging for the following individual Gravitee components that make up the APIM platform:

* Management API
* Gateway

Java-class debug logging means the individual Java classes and packages that are included in the Gravitee components. Here are some examples of Java classes:

* io.gravitee
* org.springframework
* com.graviteesource.policy.kafka.acl.KafkaAclPolicy
* com.graviteesource.secretprovider.microsoft.keyvault.client.MicrosoftKeyVaultClientImpl

## Node Logging and MDC Enrichment

{% hint style="info" %}
Node Logging and Architecture Rules require Gravitee Node 8.0.0-alpha.2 or later, Gravitee Gateway API 5.0.0 or later, and Gravitee Parent 24.0.0 or later.
{% endhint %}

Gravitee provides centralized logging infrastructure with Mapped Diagnostic Context (MDC) enrichment and compile-time enforcement of logging patterns across Gravitee components. MDC automatically injects request-scoped metadata (API ID, application ID, organization ID, environment ID, node ID, plan ID) into log entries. The `%mdcList` pattern converter formats MDC entries according to configurable templates.

When a log source is available (e.g., an execution context), MDC values are resolved from context attributes. When missing, values default to `"unknown"`. MDC keys are shortened for readability: `envId`, `orgId`, `appId`, `planId` instead of full names.

### MDC Key Mapping

<table><thead><tr><th>MDC Key</th><th>Source Attribute</th><th>Caching Strategy</th></tr></thead><tbody><tr><td><code>nodeId</code></td><td>Node identifier</td><td>Cached</td></tr><tr><td><code>envId</code></td><td><code>ATTR_ENVIRONMENT</code></td><td>Cached</td></tr><tr><td><code>orgId</code></td><td><code>ATTR_ORGANIZATION</code></td><td>Cached</td></tr><tr><td><code>apiId</code></td><td><code>ATTR_API</code> or request path <code>/apis/{apiId}/...</code></td><td>Refreshable</td></tr><tr><td><code>appId</code></td><td><code>ATTR_APPLICATION</code> or request path <code>/applications/{appId}/...</code></td><td>Refreshable</td></tr><tr><td><code>planId</code></td><td><code>ATTR_PLAN</code></td><td>Refreshable</td></tr></tbody></table>

### Node Logging Configuration

Configure MDC formatting and pattern overrides in `gravitee.yml`:

<table><thead><tr><th>Property</th><th>Description</th><th>Example</th></tr></thead><tbody><tr><td><code>node.logging.mdc.format</code></td><td>Template for each MDC key-value pair</td><td><code>"{key}: {value}"</code></td></tr><tr><td><code>node.logging.mdc.separator</code></td><td>Separator between MDC entries</td><td><code>" "</code> (space)</td></tr><tr><td><code>node.logging.mdc.nullValue</code></td><td>Placeholder when MDC value is null</td><td><code>"-"</code></td></tr><tr><td><code>node.logging.mdc.include</code></td><td>List of MDC keys to include in output</td><td>Gateway: <code>["nodeId", "apiId"]</code><br>Management API: <code>["nodeId", "envId", "apiId", "appId"]</code></td></tr><tr><td><code>node.logging.pattern.overrideLogbackXml</code></td><td>Enable runtime pattern replacement</td><td><code>true</code></td></tr><tr><td><code>node.logging.pattern.console</code></td><td>Console log pattern when override is enabled</td><td><code>"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"</code></td></tr><tr><td><code>node.logging.pattern.file</code></td><td>File log pattern when override is enabled</td><td><code>"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"</code></td></tr></tbody></table>

### Logback Pattern Override

The pattern override mechanism replaces logback.xml encoder patterns at runtime without modifying the XML file. When `node.logging.pattern.overrideLogbackXml` is enabled, the system programmatically registers the `%mdcList` converter and applies configured console and file patterns. This avoids classloader issues that occur when `%mdcList` is declared directly in logback.xml via `<conversionRule>`, as the converter class is not visible to Logback's bootstrap classloader.

### Creating Node-Aware Loggers

Use `NodeLoggerFactory.getLogger()` instead of `LoggerFactory.getLogger()` to create loggers that participate in MDC enrichment. For Lombok users, configure `lombok.config` with `lombok.log.custom.declaration = org.slf4j.Logger io.gravitee.node.logging.NodeLoggerFactory.getLogger(TYPE)` and annotate classes with `@CustomLog`. The logger will automatically inject MDC values when log statements execute.

For execution context logging, call `ctx.withLogger(log).info("message")` instead of `log.info("message")` directly. This ensures the execution context's attributes (API ID, application ID, plan ID) are included in MDC.

### Architecture Rules

ArchUnit-based rules enforce logging patterns at compile time. The `LoggingArchitectureRules` class prohibits direct calls to `org.slf4j.LoggerFactory.getLogger()` in configured packages, requiring use of `NodeLoggerFactory.getLogger()` instead. The `ExecutionContextLoggingArchitectureTest` enforces that methods with `ExecutionContext` parameters use `ctx.withLogger(log).xxx(...)` instead of calling logger methods directly. Both rules support allow-lists for exceptions (e.g., `*ConfigurationEvaluator` classes).

Configure the `gravitee-archrules-maven-plugin` in your project's `pom.xml` to enforce logging patterns at build time. The plugin runs ArchUnit tests during the Maven `test` phase. To exclude specific packages from scanning, add them to the `excludePackagesFromScan` configuration. To allow specific classes to use `LoggerFactory.getLogger()` directly, add them to the allow-list or use suffix patterns (e.g., `*ConfigurationEvaluator`).

For detailed integration instructions, see the [Developer Guide](../../developer-guide/node-logging-and-mdc-enrichment.md). For build tooling configuration, see [Architecture Rules Enforcement](../../developer-guide/architecture-rules-enforcement.md).

Skip architecture rule checks during development or CI builds:

<table><thead><tr><th>Property</th><th>Description</th><th>Example</th></tr></thead><tbody><tr><td><code>gravitee.archrules.skip</code></td><td>Skip ArchUnit rule enforcement</td><td><code>-Dgravitee.archrules.skip=true</code></td></tr><tr><td><code>skip.validation</code></td><td>Skip Maven validation phase</td><td><code>-Dskip.validation=true</code></td></tr></tbody></table>

## Enable component-based debug logging

To enable debug logging for a specific Gravitee component, you can use the following example configurations as templates:

{% tabs %}
{% tab title="logback.xml" %}
* To enable debug logging for the Management API component, set `<logger name="io.gravitee" level="DEBUG" />` in your `/opt/graviteeio-management-api/config/logback.xml` file:

{% code title="logback.xml" %}
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] [%X{api}] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${gravitee.gateway.log.dir}/gravitee.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <!-- daily rollover -->
            <fileNamePattern>${gravitee.gateway.log.dir}/gravitee_%d{yyyy-MM-dd}.log</fileNamePattern>
            <!-- keep 30 days' worth of history -->
            <maxHistory>30</maxHistory>
        </rollingPolicy>
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] [%X{api}] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <appender name="async-file" class="ch.qos.logback.classic.AsyncAppender">
        <appender-ref ref="FILE" />
    </appender>

    <appender name="async-console" class="ch.qos.logback.classic.AsyncAppender">
        <appender-ref ref="STDOUT" />
    </appender>

    <logger name="io.gravitee" level="DEBUG" />
    <logger name="com.graviteesource.reactor" level="INFO" />
    <logger name="org.reflections" level="WARN" />
    <logger name="org.springframework" level="WARN" />
    <logger name="org.eclipse.jetty" level="WARN" />
    <root level="WARN">
        <appender-ref ref="async-console" />
        <appender-ref ref="async-file" />
    </root>
</configuration>
```
{% endcode %}

To enable debug logging for the Gateway component, you can apply the same edits to the `/opt/graviteeio-gateway/config/logback.xml` file.
{% endtab %}

{% tab title="Helm chart values.yml" %}
{% hint style="warning" %}
The legacy `logging.debug`, `logging.graviteeLevel`, and `logging.stdout.encoderPattern` parameters are deprecated. Use the new `node.logging` and `logback.override` parameters instead. See [#helm-chart-configuration-with-node-logging](debug-logging.md#helm-chart-configuration-with-node-logging "mention").
{% endhint %}

* To enable debug logging for the Management API, edit the following section of your [Gravitee Helm chart](https://github.com/gravitee-io/gravitee-api-management/blob/master/helm/values.yaml) `values.yml` file:

{% code title="values.yml" %}
```yaml
api:
  enabled: true
  name: api
  logging:
    debug: true
    contextualLoggingEnabled: false
    stdout:
      json: false
      encoderPattern: "%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n"
      contextualLoggingEncoderPattern: "%d{HH:mm:ss.SSS} [%thread] [%X{orgId} %X{envId}] %-5level %logger{36} - %msg%n"
    file:
      enabled: false
      rollingPolicy: |
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <!-- daily rollover -->
            <fileNamePattern>${gravitee.home}/logs/gravitee_%d{yyyy-MM-dd}.log</fileNamePattern>
            <!-- keep 30 days' worth of history -->
            <maxHistory>30</maxHistory>
        </rollingPolicy>
      encoderPattern: "%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n%n"
      contextualLoggingEncoderPattern: "%d{HH:mm:ss.SSS} [%thread] [%X{orgId} %X{envId}] %-5level %logger{36} - %msg%n%n"
    graviteeLevel: DEBUG
    jettyLevel: INFO
```
{% endcode %}

To enable debug logging for the Gateway component, you can apply the same edits to the `gateway:` section of the `values.yml` file.
{% endtab %}
{% endtabs %}

### Helm Chart Configuration with Node Logging

Use the new `node.logging` and `logback.override` parameters for enhanced logging control:

<table><thead><tr><th>Parameter</th><th>Description</th><th>Example</th></tr></thead><tbody><tr><td><code>api.logback.override</code></td><td>Replace entire logback.xml with custom content</td><td><code>false</code></td></tr><tr><td><code>api.logback.content</code></td><td>Complete logback.xml when override is enabled</td><td>(JSON-formatted XML string)</td></tr><tr><td><code>api.node.logging.mdc.include</code></td><td>MDC keys to include in Management API logs</td><td><code>["nodeId", "envId", "apiId", "appId"]</code></td></tr><tr><td><code>api.node.logging.pattern.overrideLogbackXml</code></td><td>Enable pattern override for Management API</td><td><code>false</code></td></tr><tr><td><code>api.node.logging.pattern.console</code></td><td>Console pattern for Management API</td><td><code>"%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"</code></td></tr><tr><td><code>gateway.logback.override</code></td><td>Replace entire logback.xml with custom content</td><td><code>false</code></td></tr><tr><td><code>gateway.logback.content</code></td><td>Complete logback.xml when override is enabled</td><td>(JSON-formatted XML with async appenders)</td></tr><tr><td><code>gateway.node.logging.mdc.include</code></td><td>MDC keys to include in Gateway logs</td><td><code>["nodeId", "apiId"]</code></td></tr><tr><td><code>gateway.node.logging.pattern.overrideLogbackXml</code></td><td>Enable pattern override for Gateway</td><td><code>false</code></td></tr><tr><td><code>gateway.node.logging.pattern.console</code></td><td>Console pattern for Gateway</td><td><code>"%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"</code></td></tr></tbody></table>

<details>

<summary>Example component-based debug logging output</summary>

```java
...
20:55:42,221 |-INFO in ch.qos.logback.classic.model.processor.LoggerModelHandler - Setting level of logger [io.gravitee] to DEBUG
...
20:55:42.587 [graviteeio-node] [] INFO  i.g.n.c.s.e.PropertiesConfiguration - Loading Gravitee configuration.
20:55:42.591 [graviteeio-node] [] INFO  i.g.n.c.s.e.PropertiesConfiguration - 	Gravitee configuration loaded from /opt/graviteeio-management-api/config/gravitee.yml
20:55:42.599 [graviteeio-node] [] INFO  i.g.n.c.s.e.PropertiesConfiguration - Loading Gravitee configuration. DONE
20:55:42.602 [graviteeio-node] [] DEBUG i.g.c.util.RelaxedPropertySource - PropertySource [envVariables] does not contain 'plugins.path[0]', but found equivalent 'plugins_path_0'
20:55:42.633 [graviteeio-node] [] DEBUG i.g.c.util.RelaxedPropertySource - PropertySource [envVariables] does not contain 'plugins.path[0]', but found equivalent 'plugins_path_0'
20:55:42.648 [graviteeio-node] [] DEBUG i.g.n.a.r.PropertyResolverFactoriesLoader - Loading instances for type io.gravitee.node.api.resolver.PropertyResolver
20:55:42.701 [graviteeio-node] [] DEBUG i.g.k.client.config.KubernetesConfig - Trying to configure client from Kubernetes config...
...
```

</details>

## Java class debug logging

To enable debug logging for only specific Java classes, you can use the following example configurations as templates.

{% tabs %}
{% tab title="logback.xml" %}
* To enable debug logging for only the `MicrosoftKeyVaultClientImpl` class of the Gravitee Gateway component, use the following snippet in your `/opt/graviteeio-gateway/config/logback.xml` file: `<logger name="com.graviteesource.secretprovider.microsoft.keyvault.client.MicrosoftKeyVaultClientImpl" level="DEBUG" />`

{% code title="logback.xml" %}
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] [%X{api}] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
 
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${gravitee.gateway.log.dir}/gravitee.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <!-- daily rollover -->
            <fileNamePattern>${gravitee.gateway.log.dir}/gravitee_%d{yyyy-MM-dd}.log</fileNamePattern>
            <!-- keep 30 days' worth of history -->
            <maxHistory>30</maxHistory>
        </rollingPolicy>
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] [%X{api}] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <appender name="async-file" class="ch.qos.logback.classic.AsyncAppender">
        <appender-ref ref="FILE" />
    </appender>

    <appender name="async-console" class="ch.qos.logback.classic.AsyncAppender">
        <appender-ref ref="STDOUT" />
    </appender>

    <logger name="io.gravitee" level="INFO" />
    <logger name="com.graviteesource.reactor" level="INFO" />
    <logger name="org.reflections" level="WARN" />
    <logger name="org.springframework" level="WARN" />
    <logger name="org.eclipse.jetty" level="WARN" />
    <logger name="com.graviteesource.secretprovider.microsoft.keyvault.client.MicrosoftKeyVaultClientImpl" level="DEBUG" />
    <root level="WARN">
        <appender-ref ref="async-console" />
        <appender-ref ref="async-file" />
    </root>
</configuration>
```
{% endcode %}

To also enable debug logging for this specific Java class in the Management API component, you can apply the same edits to the `/opt/graviteeio-management-api/config/logback.xml` file.
{% endtab %}

{% tab title="Helm chart values.yml" %}
* To enable debug logging for only the `MicrosoftKeyVaultClientImpl` class of the Gravitee Gateway component, use the following [Gravitee Helm chart](https://github.com/gravitee-io/gravitee-api-management/blob/master/helm/values.yaml) `values.yml` snippet:

{% code title="values.yml" %}
```yaml
gateway:
  logging:
    debug: false
    graviteeLevel: WARN
    additionalLoggers:
      - name: com.graviteesource.secretprovider.microsoft.keyvault.client.MicrosoftKeyVaultClientImpl
        level: DEBUG
    # - name: io.gravitee.test.infopackage
    #   level: DEBUG
```
{% endcode %}

To also enable debug logging for this specific Java class of the Management API component, you can apply the same edits to the `api:` section of the `values.yml` file.
{% endtab %}
{% endtabs %}

<details>

<summary>Example Java class debug logging output</summary>

```java
...
20:48:46,173 |-INFO in ch.qos.logback.classic.model.processor.LoggerModelHandler - Setting level of logger [com.graviteesource.secretprovider.microsoft.keyvault.client.MicrosoftKeyVaultClientImpl] to DEBUG
...
20:48:48.552 [graviteeio-node] [] DEBUG c.g.s.m.k.c.MicrosoftKeyVaultClientImpl - DEBUG: MicrosoftKeyVaultClientImpl - Starting the authentication connection...
20:48:48.553 [graviteeio-node] [] DEBUG c.g.s.m.k.c.MicrosoftKeyVaultClientImpl - DEBUG: Building clientid/clientsecret auth...
...
```

</details>

## Internal API

{% hint style="info" %}
Before you can use the Internal API to enable debug logging, you must [enable the Internal API](management-api/mapi-internal-api.md).
{% endhint %}

The [Internal API](../prepare-a-production-environment/production-best-practices/internal-apis.md) can be used to dynamically enable debug logging without restarting the component or container. When the component or container is restarted, the runtime configuration is lost and therefore debug logging is disabled.

For example, to dynamically enable debug logging for just the `MongoTemplate` class, run the following command:

```sh
curl "https://${INTERNAL_API_URL}:18093/_node/logging" \
     -X POST \
     -u "admin:adminadmin" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -d '{"org.springframework.data.mongodb.core.MongoTemplate": "DEBUG"}'
```

<details>

<summary>Example curl response</summary>

If your request is successful, the endpoint returns a `HTTP 200 OK` status and the current logging status:

```json
{
  "org.eclipse.jetty": "INFO",
  "ROOT": "WARN",
  "io.gravitee": "INFO",
  "io.gravitee.rest.api.service.impl.upgrade": "INFO",
  "org.springframework.data.mongodb.core.MongoTemplate": "DEBUG"
}
```

</details>
