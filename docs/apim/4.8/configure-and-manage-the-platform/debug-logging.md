# Debug Logging

## Overview

{% hint style="danger" %}
&#x20;Debug logging can reduce performance. To avoid issues with performance, enable debug logging for only specific troubleshooting purposes.
{% endhint %}

Gravitee supports standard Java logging for each Gravitee component and debug logging for specific Java classes. For example:&#x20;

```
com.graviteesource.secretprovider.microsoft.keyvault.client.MicrosoftKeyVaultClientImpl
```

You can enable debug logging using the internal `logback.xml` file or the [Gravitee Helm chart](https://github.com/gravitee-io/gravitee-api-management/blob/master/helm/values.yaml) `values.yml` file.  After you had made your changes, you must start the specific Gravitee components.  Or, you can temporarily enable debug logging using the [#internal-api](debug-logging.md#internal-api "mention") without restarting the component or container. When you restart the component or container, the runtime configuration is lost and debug logging is disabled. You can enable component-based debug logging and java-class debug logging.

Component-based debug logging means that you enable debug logging for the following individual Gravitee components that make up the APIM platform:

* Management API
* Gateway

Java-class debug logging means the individual Java classes and packages that are included in the Gravitee components. Here are some examples of Java classes:

* io.gravitee
* org.springframework
* com.graviteesource.policy.kafka.acl.KafkaAclPolicy
* com.graviteesource.secretprovider.microsoft.keyvault.client.MicrosoftKeyVaultClientImpl

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

## Internal API

{% hint style="info" %}
Before you can use the Internal API to enable debug logging, you must [enable the Internal API](management-api/mapi-internal-api.md) .
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
