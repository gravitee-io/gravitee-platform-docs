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

The Node Logging Infrastructure provides context-aware logging with MDC (Mapped Diagnostic Context) enrichment for Gravitee Gateway and REST API components. It automatically injects request metadata (API ID, environment ID, organization ID, plan ID, user) into log entries and enforces logging best practices through ArchUnit rules. The infrastructure supports runtime pattern overrides, MDC filtering, and lazy logger initialization to minimize overhead in reactive code paths.

## Prerequisites

* Gravitee Node 8.0.0-alpha.15 or later
* Gravitee Gateway API 5.0.0 or later (for execution context logging)
* Logback 1.2.x or later
* SLF4J 1.7.x or later

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

## Context-aware logging

Loggers automatically enrich MDC with request and node metadata when logging within an execution context. The infrastructure extracts values from `ExecutionContext` attributes and caches them to avoid repeated lookups. When a log source is missing, MDC values default to `"-"` (configurable via `node.logging.mdc.nullValue`). In reactive code, use `ctx.withLogger(log).info(...)` instead of `log.info(...)` to ensure MDC enrichment occurs.

### MDC keys

The following MDC keys are automatically populated for Gateway and REST API components:

| MDC Key | Source | Caching | Description |
|:--------|:-------|:--------|:------------|
| `nodeId` | `Node.id()` | Cached | Unique node identifier |
| `nodeHostname` | `Node.hostname()` | Cached | Node hostname |
| `nodeApplication` | `Node.application()` | Cached | Application name |
| `apiId` | `context.getAttribute(ATTR_API)` | Cached | API identifier |
| `apiName` | `context.getAttribute(ATTR_API_NAME)` | Cached | API name |
| `apiType` | `context.getInternalAttribute(ATTR_INTERNAL_API_TYPE)` | Cached | API type (v2, v4, etc.) |
| `envId` | `context.getAttribute(ATTR_ENVIRONMENT)` | Cached | Environment identifier |
| `orgId` | `context.getAttribute(ATTR_ORGANIZATION)` | Cached | Organization identifier |
| `appId` | `context.getAttribute(ATTR_APPLICATION)` | Refreshable | Application identifier (changes per request) |
| `planId` | `context.getAttribute(ATTR_PLAN)` | Refreshable | Plan identifier (changes per request) |
| `user` | `context.getAttribute(ATTR_USER)` | Refreshable | User identifier |

REST API components include additional MDC keys:

| MDC Key | Source | Description |
|:--------|:-------|:------------|
| `correlationId` | `X-Correlation-ID` header | Request correlation ID |
| `traceParent` | `traceparent` header | W3C Trace Context |

### MDC filtering configuration

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `node.logging.mdc.format` | String | `"{key}: {value}"` | MDC key-value format pattern |
| `node.logging.mdc.separator` | String | `" "` | Separator between MDC entries |
| `node.logging.mdc.nullValue` | String | `"-"` | Value displayed when MDC entry is null |
| `node.logging.mdc.include` | List\<String> | `["nodeId", "apiId"]` (Gateway)<br>`["nodeId", "envId", "apiId", "appId"]` (REST API) | MDC keys to include in log output |

### Runtime pattern override

The `node.logging.pattern.overrideLogbackXml` setting replaces logback.xml encoder patterns at runtime without modifying the XML file. When enabled, the infrastructure walks the appender tree (including async wrappers) and replaces console and file patterns with values from `gravitee.yml`. This allows centralized pattern management in Kubernetes environments via ConfigMaps.

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `node.logging.pattern.overrideLogbackXml` | Boolean | `true` | Whether to override logback.xml patterns at runtime |
| `node.logging.pattern.console` | String | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` | Console log pattern when override is enabled |
| `node.logging.pattern.file` | String | `"%d{HH:mm:ss.SSS} %-5level %logger{36} [%mdcList] - %msg%n"` | File log pattern when override is enabled |

### %mdcList converter

The `%mdcList` conversion word filters and formats MDC entries based on `node.logging.mdc.include`. It is registered programmatically via `PatternLayout.DEFAULT_CONVERTER_SUPPLIER_MAP` and cannot be declared in `logback.xml` using `<conversionRule>` due to classloader visibility constraints. Output format is controlled by `node.logging.mdc.format`, `node.logging.mdc.separator`, and `node.logging.mdc.nullValue`.

Example output:

```
nodeId: gw-1 apiId: my-api envId: prod
```

## Helm chart configuration

### API (REST API)

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `api.logback.override` | Boolean | `false` | Use `api.logback.content` as complete logback.xml |
| `api.logback.content` | String | JSON-formatted logback config | Complete logback.xml content when override is true |
| `api.node.logging.mdc.format` | String | `"{key}: {value}"` | MDC key-value format pattern |
| `api.node.logging.mdc.separator` | String | `" "` | MDC entries separator |
| `api.node.logging.mdc.nullValue` | String | `"-"` | Value when MDC entry is null |
| `api.node.logging.mdc.include` | List\<String> | `["nodeId", "envId", "apiId", "appId"]` | MDC keys to include |
| `api.node.logging.pattern.overrideLogbackXml` | Boolean | `false` | Override logback.xml patterns at runtime |
| `api.node.logging.pattern.console` | String | `"%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"` | Console pattern |
| `api.node.logging.pattern.file` | String | `"%d %-5p [%t] %c [%mdcList] : %m%n"` | File pattern |

### Gateway

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `gateway.logback.override` | Boolean | `false` | Use `gateway.logback.content` as complete logback.xml |
| `gateway.logback.content` | String | JSON-formatted async logback config | Complete logback.xml content when override is true |
| `gateway.node.logging.mdc.format` | String | `"{key}: {value}"` | MDC key-value format pattern |
| `gateway.node.logging.mdc.separator` | String | `" "` | MDC entries separator |
| `gateway.node.logging.mdc.nullValue` | String | `"-"` | Value when MDC entry is null |
| `gateway.node.logging.mdc.include` | List\<String> | `["nodeId", "apiId"]` | MDC keys to include |
| `gateway.node.logging.pattern.overrideLogbackXml` | Boolean | `false` | Override logback.xml patterns at runtime |
| `gateway.node.logging.pattern.console` | String | `"%d{HH:mm:ss} %-5level %logger{36} [%mdcList] - %msg%n"` | Console pattern |
| `gateway.node.logging.pattern.file` | String | `"%d %-5p [%t] %c [%mdcList] : %m%n"` | File pattern |

### Usage pattern

When `logback.override` is `false`, the component uses its default logback.xml configuration. When `logback.override` is `true`, the component replaces the entire logback.xml with the content specified in `logback.content`.

The `node.logging.pattern.*` properties allow runtime pattern replacement when `overrideLogbackXml` is `true`. These properties modify existing appender patterns without requiring a full logback.xml replacement.

### MDC include differences

The default `mdc.include` list differs between components:

* **API (REST API)**: Includes `nodeId`, `envId`, `apiId`, and `appId` by default
* **Gateway**: Includes only `nodeId` and `apiId` by default

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

## Restrictions

* The `%mdcList` converter cannot be declared in `logback.xml` via `<conversionRule>` due to classloader visibility. It is registered programmatically and will fail with `PARSER_ERROR[mdcList]` if declared in XML.
* ArchUnit logging rules are enforced during `mvn install` but skipped during `mvn test` and `mvn deploy` via `-Dgravitee.archrules.skip=true`.
* Classes must use `NodeLoggerFactory.getLogger()` instead of `org.slf4j.LoggerFactory.getLogger()` unless explicitly allowed via `LoggingArchitectureRules.configure().allowIn(...)`.
* Methods with an `ExecutionContext` parameter must use `ctx.withLogger(log).info(...)` instead of `log.info(...)` directly, unless the class is in the ArchUnit allow list.
* MDC keys `appId`, `planId`, and `user` are refreshable and change per request. All other keys are cached for the lifecycle of the execution context.
