# Node logging configuration

Configure MDC filtering, log patterns, and Logback overrides for the Gravitee Gateway and Management API via `gravitee.yml`.

## MDC filtering and formatting

The `%mdcList` custom Logback converter formats selected MDC keys into log output. Configure which keys to include, how to format each entry, and how to separate entries.

<table>
    <thead>
        <tr>
            <th width="280">Property</th>
            <th width="120">Type</th>
            <th width="150">Default</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>node.logging.mdc.format</code></td>
            <td>String</td>
            <td><code>{key}: {value}</code></td>
            <td>Template for formatting each MDC key-value pair</td>
        </tr>
        <tr>
            <td><code>node.logging.mdc.separator</code></td>
            <td>String</td>
            <td><code>" "</code> (space)</td>
            <td>Separator between formatted MDC entries</td>
        </tr>
        <tr>
            <td><code>node.logging.mdc.nullValue</code></td>
            <td>String</td>
            <td><code>""</code> (empty)</td>
            <td>Placeholder when an MDC value is null</td>
        </tr>
        <tr>
            <td><code>node.logging.mdc.include</code></td>
            <td>List&lt;String&gt;</td>
            <td><code>[]</code> (empty — all keys included)</td>
            <td>MDC keys to include in <code>%mdcList</code> output. When empty, all available MDC keys are included.</td>
        </tr>
    </tbody>
</table>

**Example `gravitee.yml`:**

```yaml
node:
  logging:
    mdc:
      format: "[{key}: {value}]"
      separator: " "
      nullValue: "-"
      include:
        - apiId
        - appId
        - planId
        - envId
```

With this configuration and a request to an API called "my-api", the `%mdcList` output would look like:

```
[apiId: my-api-id] [appId: my-app-id] [planId: my-plan-id] [envId: DEFAULT]
```

## Pattern override

Override Logback appender patterns at runtime without modifying `logback.xml`.

<table>
    <thead>
        <tr>
            <th width="350">Property</th>
            <th width="100">Type</th>
            <th width="100">Default</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>node.logging.pattern.overrideLogbackXml</code></td>
            <td>Boolean</td>
            <td><code>false</code></td>
            <td>Override logback.xml patterns at runtime</td>
        </tr>
        <tr>
            <td><code>node.logging.pattern.console</code></td>
            <td>String</td>
            <td>-</td>
            <td>Console (STDOUT) appender pattern when override is enabled</td>
        </tr>
        <tr>
            <td><code>node.logging.pattern.file</code></td>
            <td>String</td>
            <td>-</td>
            <td>File appender pattern when override is enabled</td>
        </tr>
    </tbody>
</table>

**Example `gravitee.yml`:**

```yaml
node:
  logging:
    pattern:
      overrideLogbackXml: true
      console: "%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} [%mdcList] - %msg%n"
      file: "%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} [%mdcList] - %msg%n"
```

When `overrideLogbackXml` is `true`, the runtime patterns replace those defined in `logback.xml` for the STDOUT and FILE appenders.

{% hint style="warning" %}
The `%mdcList` converter is registered programmatically at runtime, **after** Logback parses `logback.xml`. Don't use `<conversionRule>` in `logback.xml` to register it — the converter class isn't visible to Logback's classloader at parse time. Use the pattern override via `gravitee.yml` instead.
{% endhint %}

{% hint style="info" %}
Because the pattern override is applied programmatically after startup, some early log lines (during application initialization) use the default pattern from `logback.xml` before the override takes effect. If using `%mdcList` in the override pattern, these early lines display an empty MDC list.
{% endhint %}

## Default logback.xml patterns

The following are the default patterns in the shipped `logback.xml` files. These patterns don't include `%mdcList` — enable the pattern override to add MDC context.

**Gateway:**

```
STDOUT: %d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n
FILE:   %d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n
```

**Management API:**

```
STDOUT: %d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n
FILE:   %d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n
```

To retain these patterns while adding MDC context, set the override pattern to include `%mdcList` at the desired position:

```yaml
node:
  logging:
    mdc:
      include:
        - apiId
        - appId
    pattern:
      overrideLogbackXml: true
      console: "%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} [%mdcList] - %msg%n"
      file: "%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} [%mdcList] - %msg%n"
```

**Expected output:**

```
15:44:17.123 [vert.x-eventloop-thread-0] INFO i.g.MyPolicy [apiId: my-api-id] [appId: my-app-id] - Processing request
```

## Individual MDC keys in patterns

As an alternative to `%mdcList`, reference individual MDC keys directly in Logback patterns using the standard `%X{key}` syntax:

```xml
<pattern>%d{HH:mm:ss.SSS} [%thread] [%X{nodeId}] [%X{apiId}] %-5level %logger{36} - %msg%n</pattern>
```

This approach works in `logback.xml` directly without requiring the pattern override.

{% hint style="info" %}
`%mdcList` filters and formats only the keys listed in `node.logging.mdc.include`. Structured encoders (for example, `JsonEncoder` or `EcsEncoder`) log the full MDC map regardless of the include list.
{% endhint %}

## Limitations

* Not all Gravitee plugins have been migrated to the context-aware logging infrastructure yet. Some logs may lack MDC context until the migration is complete in 4.12.
* The `%mdcList` converter is only valid for pattern-based encoders. Structured encoders (`JsonEncoder`, `EcsEncoder`) log the full unfiltered MDC map.
* Early startup log lines use the default `logback.xml` pattern before the runtime override takes effect.
